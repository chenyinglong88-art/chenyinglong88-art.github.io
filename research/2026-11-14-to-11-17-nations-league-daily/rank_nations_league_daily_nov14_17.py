#!/usr/bin/env python3
"""Day-by-day 'must-win vs indifferent' classification for Nations League 14-17 Nov 2026 (as of 14:15 CET).
Inputs: 30k Monte Carlo motivation file (1415 snapshot) and market-vs-Elo table. Outputs CSV, JSON, PNG."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path('/home/ubuntu/football_betting_backtest')
X = ROOT / 'output/nations_league_2026-11-14_1415_motivation_vs_market.csv'
OUT = ROOT / 'output/nations_league_2026-11-14_to_11-17_daily_motivation.csv'
SUMMARY = ROOT / 'output/nations_league_2026-11-14_to_11-17_daily_motivation_summary.json'
CHART = ROOT / 'output/nations_league_2026-11-14_to_11-17_daily_motivation_chart.png'
ZH = {'Kosovo': '科索沃', 'Israel': '以色列', 'Georgia': '格鲁吉亚', 'Hungary': '匈牙利', 'Norway': '挪威', 'Wales': '威尔士',
      'Austria': '奥地利', 'Republic of Ireland': '爱尔兰', 'Northern Ireland': '北爱尔兰', 'Ukraine': '乌克兰',
      'Portugal': '葡萄牙', 'Denmark': '丹麦', 'Romania': '罗马尼亚', 'Poland': '波兰', 'Sweden': '瑞典',
      'Bosnia-Herzegovina': '波黑', 'Cyprus': '塞浦路斯', 'Montenegro': '黑山', 'Latvia': '拉脱维亚', 'Armenia': '亚美尼亚',
      'Belarus': '白俄罗斯', 'Albania': '阿尔巴尼亚', 'Finland': '芬兰', 'San Marino': '圣马力诺', 'Belgium': '比利时',
      'Italy': '意大利', 'Croatia': '克罗地亚', 'Czechia': '捷克', 'France': '法国', 'Türkiye': '土耳其', 'Spain': '西班牙',
      'England': '英格兰', 'Faroe Islands': '法罗群岛', 'Moldova': '摩尔多瓦', 'Kazakhstan': '哈萨克斯坦', 'Slovakia': '斯洛伐克',
      'Estonia': '爱沙尼亚', 'Bulgaria': '保加利亚', 'Iceland': '冰岛', 'Luxembourg': '卢森堡', 'Lithuania': '立陶宛',
      'Liechtenstein': '列支敦士登', 'Germany': '德国', 'Netherlands': '荷兰', 'Gibraltar': '直布罗陀', 'Malta': '马耳他',
      'Greece': '希腊', 'Serbia': '塞尔维亚', 'North Macedonia': '北马其顿', 'Slovenia': '斯洛文尼亚', 'Switzerland': '瑞士',
      'Scotland': '苏格兰'}
# Extra multi-book consensus already verified for three 16 Nov fixtures (sub-agent checks 13:47-13:50 CET)
MULTI = {('Germany', 'Netherlands'): (0.5122, 1.833, 4), ('North Macedonia', 'Slovenia'): (0.6002, 1.571, 4)}
GAP_MIN, OPP_MAX = 3.0, 6.5


def classify(r) -> str:
    sh, sa = r.stakeH, r.stakeA
    if max(sh, sa, r.needH, r.needA) <= 1.0:
        return '双方无所谓'
    if r.gapH >= GAP_MIN and sa <= OPP_MAX:
        return '主队必须赢·客队无所谓'
    if r.gapA >= GAP_MIN and sh <= OPP_MAX:
        return '客队必须赢·主队无所谓'
    if min(sh, sa) >= 10:
        return '双方都在乎'
    return '一方在乎·另一方轻度'


def main() -> None:
    x = pd.read_csv(X)
    rows = []
    for r in x.itertuples():
        cls = classify(r)
        if cls.startswith('主队必须赢'):
            side = 'H'
        elif cls.startswith('客队必须赢'):
            side = 'A'
        else:
            side = 'H' if r.needH >= r.needA else 'A'
        team, opp = (r.home, r.away) if side == 'H' else (r.away, r.home)
        gap = r.gapH if side == 'H' else r.gapA
        need = r.needH if side == 'H' else r.needA
        opp_stake = r.stakeA if side == 'H' else r.stakeH
        p_mkt = r.mktH if side == 'H' else r.mktA
        p_elo = r.eloH if side == 'H' else r.eloA
        price = r.bestH if side == 'H' else r.bestA
        resid = r.residH_pp if side == 'H' else r.residA_pp
        nbooks = 1 if r.src == 'DK' else (14 if r.src.startswith('Odds') else 0)
        if (r.home, r.away) in MULTI:
            p_mkt, price, nbooks = MULTI[(r.home, r.away)]
        ev = p_mkt * price - 1 if pd.notna(p_mkt) and pd.notna(price) else np.nan
        rows.append(dict(
            date=f"2026-{r.t[:5]}", kickoff_cet=r.t, group=r.g, home=r.home, away=r.away,
            match_zh=f"{ZH[r.home]} vs {ZH[r.away]}", classification=cls,
            motivated_side=team, motivated_zh=ZH[team], opponent_zh=ZH[opp], motivation_gap=gap,
            need_win=need, opponent_stake=opp_stake, price_source=r.src, books=nbooks, best_price=price,
            market_no_vig_prob=p_mkt, elo_prob=p_elo, market_premium_vs_normal_pp=resid, ev_vs_market=ev,
            min_price_1pct=1.01 / p_mkt if pd.notna(p_mkt) and p_mkt > 0 else np.nan,
            passes_min_odds_150=bool(pd.notna(price) and price >= 1.50),
            formal_approved=False, stake_cny=0,
        ))
    df = pd.DataFrame(rows)
    df['day_rank'] = np.nan
    for d, g in df[df.classification.str.contains('必须赢')].groupby('date'):
        order = g.sort_values('motivation_gap', ascending=False).index
        df.loc[order, 'day_rank'] = range(1, len(order) + 1)
    df = df.sort_values(['date', 'day_rank', 'kickoff_cet']).reset_index(drop=True)
    key = df.classification.str.contains('必须赢')
    df.to_csv(OUT, index=False, encoding='utf-8-sig')
    pd.set_option('display.width', 260); pd.set_option('display.max_rows', 100)
    print(df[['date', 'kickoff_cet', 'match_zh', 'classification', 'motivated_zh', 'motivation_gap', 'need_win', 'opponent_stake',
              'price_source', 'best_price', 'market_no_vig_prob', 'elo_prob', 'market_premium_vs_normal_pp', 'ev_vs_market',
              'min_price_1pct', 'day_rank']].to_string(index=False, float_format=lambda v: f'{v:.3f}'))
    counts = df.groupby(['date', 'classification']).size().unstack(fill_value=0)
    print(counts)
    summary = dict(as_of='2026-11-14T14:15:00+01:00', fixtures=int(len(df)), five_league_fixtures=0,
                   formal_approved=0, approved_stake_cny=0,
                   class_counts={d: {k: int(v) for k, v in row.items()} for d, row in counts.iterrows()},
                   must_win=df[key][['date', 'kickoff_cet', 'match_zh', 'motivated_zh', 'motivation_gap', 'opponent_stake',
                                     'best_price', 'market_no_vig_prob', 'ev_vs_market', 'min_price_1pct']].to_dict(orient='records'))
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=float), encoding='utf-8')

    for f in font_manager.findSystemFonts():
        if 'NotoSansCJK' in f or 'NotoSansSC' in f or 'wqy' in f.lower():
            font_manager.fontManager.addfont(f)
    cjk = [f.name for f in font_manager.fontManager.ttflist if 'CJK' in f.name or 'WenQuanYi' in f.name or 'Noto Sans SC' in f.name]
    if cjk:
        plt.rcParams['font.family'] = cjk[0]
    plt.rcParams['axes.unicode_minus'] = False
    k = df[key].copy()
    day_zh = {'2026-11-14': '14日(今天)', '2026-11-15': '15日', '2026-11-16': '16日', '2026-11-17': '17日'}
    labels = [f"{day_zh[r.date]} {r.motivated_zh}（对{r.opponent_zh}）" for r in k.itertuples()]
    fig, ax = plt.subplots(figsize=(11.5, 0.62 * len(k) + 1.8))
    y = np.arange(len(k))[::-1]
    colors = ['#c0392b' if pd.notna(e) else '#bdc3c7' for e in k.ev_vs_market]
    ax.barh(y, k.motivation_gap, color=colors)
    for yy, r in zip(y, k.itertuples()):
        txt = (f"赔率 {r.best_price:.2f} · 市场胜率 {r.market_no_vig_prob*100:.0f}% · EV {r.ev_vs_market*100:+.1f}% · 转正需 ≥{r.min_price_1pct:.2f}"
               if pd.notna(r.ev_vs_market) else '尚未开盘，开盘后重评')
        ax.text(r.motivation_gap + 0.4, yy, f"+{r.motivation_gap:.1f}  {txt}", va='center', fontsize=9.5)
    ax.set_yticks(y, labels, fontsize=10)
    ax.set_xlim(0, 52)
    ax.set_xlabel('战意差 = 己方赢球需求 − 对手胜负利害（启发式，未回测）')
    ax.set_title('14–17日"必须赢 vs 对手无所谓"逐日清单：全部按市场价为负EV', fontsize=13)
    fig.text(0.01, 0.01, '数据：ESPN/DraftKings（14:14 CET）、Oddschecker（17日场次，页面更新14日01:06–01:07）、eloratings.net；3万次蒙特卡洛。仅研究。',
             fontsize=8, color='#555')
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(CHART, dpi=160)
    print('chart', CHART)


if __name__ == '__main__':
    main()
