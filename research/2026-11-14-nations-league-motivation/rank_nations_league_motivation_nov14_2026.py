#!/usr/bin/env python3
"""Rank 'must-win vs indifferent opponent' fixtures (Nations League MD5-6, as of 2026-11-14 13:55 CET)
and test whether the market has already priced the motivation gap. Output: CSV, JSON summary, PNG chart."""
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
MV = ROOT / 'output/nations_league_2026-11-14_motivation_vs_market.csv'
OUT = ROOT / 'output/nations_league_2026-11-14_motivation_ranked.csv'
SUMMARY = ROOT / 'output/nations_league_2026-11-14_motivation_summary.json'
CHART = ROOT / 'output/nations_league_2026-11-14_motivation_chart.png'

# Multi-book 90-minute 1X2 seen 13:47-13:50 CET by sub-agent checks (home/draw/away).
BOOKS = {
    ('Germany', 'Netherlands'): [('DraftKings', 1.833, 4.00, 3.50), ('Betfred', 1.83, 3.75, 4.00),
                                 ('1xbet', 1.80, 4.12, 3.49), ('Betsson', 1.82, 3.85, 3.95)],
    ('North Macedonia', 'Slovenia'): [('DraftKings', 5.75, 3.65, 1.571), ('1xbet', 6.33, 3.86, 1.50),
                                      ('Betfred', 6.00, 3.60, 1.53), ('Paddy Power', 6.00, 3.70, 1.50)],
    # Comparison-site Swiss prices (1.50/4.33/6.50; 1.49/4.37/6.87) show last update 13 Nov 05:19, i.e. before
    # Switzerland clinched promotion that evening -> treated as stale; only DraftKings 12:30 UTC 14 Nov used.
    ('Switzerland', 'Scotland'): [('DraftKings', 1.667, 3.65, 5.00)],
}
MOTIVATED = {  # (home, away): motivated side
    ('Germany', 'Netherlands'): 'home', ('North Macedonia', 'Slovenia'): 'away', ('Switzerland', 'Scotland'): 'away',
    ('Portugal', 'Denmark'): 'away', ('Estonia', 'Bulgaria'): 'home', ('Bosnia-Herzegovina', 'Romania'): 'home',
    ('Wales', 'Portugal'): 'home',
}
ZH = {'Germany': '德国', 'Netherlands': '荷兰', 'North Macedonia': '北马其顿', 'Slovenia': '斯洛文尼亚',
      'Switzerland': '瑞士', 'Scotland': '苏格兰', 'Portugal': '葡萄牙', 'Denmark': '丹麦', 'Estonia': '爱沙尼亚',
      'Bulgaria': '保加利亚', 'Bosnia-Herzegovina': '波黑', 'Romania': '罗马尼亚', 'Wales': '威尔士'}
MIN_ODDS_USER = 1.50


def no_vig(h, d, a):
    inv = np.array([1 / h, 1 / d, 1 / a])
    return inv / inv.sum()


def main() -> None:
    mv = pd.read_csv(MV)
    rows = []
    for (home, away), side in MOTIVATED.items():
        r = mv[(mv.home == home) & (mv.away == away)].iloc[0]
        team, opp = (home, away) if side == 'home' else (away, home)
        s, o = ('H', 'A') if side == 'home' else ('A', 'H')
        need = r[f'need{s}']; opp_stake = r[f'stake{o}']
        books = BOOKS.get((home, away))
        if books is None and pd.notna(r.dkH):
            books = [('DraftKings', r.dkH, r.dkD, r.dkA)]
        idx = 0 if side == 'home' else 2
        if books:
            nv = np.array([no_vig(*b[1:])[idx] for b in books])
            prices = [(b[0], b[1 + idx]) for b in books]
            best_book, best = max(prices, key=lambda x: x[1])
            p_cons = float(nv.mean())
            ev_best = p_cons * best - 1
            min_price_1pct = 1.01 / p_cons
        else:
            p_cons = best = ev_best = min_price_1pct = np.nan; best_book = '未开盘'
        p_elo = r[f'elo{s}']
        rows.append(dict(
            kickoff_cet=r.t, home=home, away=away, motivated_team=team, motivated_zh=ZH[team], opponent=opp,
            opponent_zh=ZH[opp], side=side, need_win=need, motivated_stake=r[f'stake{s}'], opponent_stake=opp_stake,
            motivation_gap=need - opp_stake, elo_win_prob=p_elo, consensus_no_vig_prob=p_cons,
            market_minus_elo_pp=(p_cons - p_elo) * 100 if pd.notna(p_cons) else np.nan,
            best_price=best, best_book=best_book, ev_at_best_vs_consensus=ev_best, min_price_for_1pct_ev=min_price_1pct,
            n_books=len(books) if books else 0,
            passes_user_min_odds=bool(pd.notna(best) and best >= MIN_ODDS_USER),
            formal_approved=False, stake_cny=0,
        ))
    df = pd.DataFrame(rows).sort_values('motivation_gap', ascending=False).reset_index(drop=True)
    df.insert(0, 'motivation_rank', range(1, len(df) + 1))
    df.to_csv(OUT, index=False, encoding='utf-8-sig')

    mvm = mv[mv.mktH.notna() & (mv.home != 'Finland')]
    summary = dict(
        as_of='2026-11-14T13:55:00+01:00', fixtures_remaining=int(len(mv)), with_dk_odds=int(mv.mktH.notna().sum()),
        elo_bias_home_pp=float(mvm.premH_pp.mean()), elo_bias_away_pp=float(mvm.premA_pp.mean()),
        formal_approved=0, approved_stake_cny=0,
        top=df[['motivation_rank', 'motivated_team', 'opponent', 'motivation_gap', 'best_price',
                'consensus_no_vig_prob', 'ev_at_best_vs_consensus', 'min_price_for_1pct_ev',
                'market_minus_elo_pp']].to_dict(orient='records'),
        utility_note='Heuristic stakes weights, not backtested; rules from UEFA 12 Nov 2026 article.',
    )
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=float), encoding='utf-8')
    pd.set_option('display.width', 250)
    print(df.drop(columns=['home', 'away', 'motivated_team', 'opponent', 'side']).to_string(
        index=False, float_format=lambda v: f'{v:.3f}'))
    print(json.dumps({k: v for k, v in summary.items() if k != 'top'}, ensure_ascii=False, default=float))

    # chart
    for f in font_manager.findSystemFonts():
        if 'NotoSansCJK' in f or 'wqy' in f.lower() or 'NotoSansSC' in f:
            font_manager.fontManager.addfont(f)
    cjk = [f.name for f in font_manager.fontManager.ttflist if 'CJK' in f.name or 'WenQuanYi' in f.name or 'Noto Sans SC' in f.name]
    if cjk:
        plt.rcParams['font.family'] = cjk[0]
    plt.rcParams['axes.unicode_minus'] = False
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.6), gridspec_kw={'width_ratios': [1.15, 1]})
    labels = [f"{r.motivated_zh}（对{r.opponent_zh}）" for r in df.itertuples()]
    y = np.arange(len(df))[::-1]
    ax1.barh(y, df.need_win, color='#c0392b', label='己方"赢球比平局多得的价值"')
    ax1.barh(y, -df.opponent_stake, color='#7f8c8d', label='对手"胜负差"（越小越无所谓）')
    for yy, g, nw in zip(y, df.motivation_gap, df.need_win):
        ax1.text(nw + 1.0, yy, f'战意差 {g:+.1f}', va='center', fontsize=10)
    ax1.set_yticks(y, labels); ax1.axvline(0, color='black', lw=0.8)
    ax1.set_xlim(-35, 42); ax1.set_xlabel('目标效用（0–100，启发式权重，未回测）')
    ax1.set_title('谁更"必须赢"、对手更"无所谓"', fontsize=13)
    ax1.legend(loc='lower left', fontsize=8.5)
    p = df[df.consensus_no_vig_prob.notna()].copy()
    x2 = np.arange(len(p))
    ax2.bar(x2 - 0.2, p.elo_win_prob * 100, 0.4, color='#95a5a6', label='Elo基准胜率（不含战意）')
    ax2.bar(x2 + 0.2, p.consensus_no_vig_prob * 100, 0.4, color='#2c7fb8', label='市场去水胜率')
    for xx, r in zip(x2, p.itertuples()):
        ax2.text(xx + 0.2, r.consensus_no_vig_prob * 100 + 1.2, f'{r.market_minus_elo_pp:+.1f}pp\nEV {r.ev_at_best_vs_consensus*100:+.1f}%',
                 ha='center', fontsize=8.5)
    ax2.set_xticks(x2, [r.motivated_zh for r in p.itertuples()], fontsize=9.5)
    ax2.set_ylabel('胜率 %'); ax2.set_ylim(0, 75)
    ax2.set_title('市场已把战意计入价格（最佳价EV均为负）', fontsize=13)
    ax2.legend(fontsize=8.5, loc='upper right')
    fig.text(0.01, 0.01, '数据：ESPN/DraftKings与多家比价页1X2（2026-11-14 13:30–13:50 CET）、eloratings.net 2026-11-14、UEFA规则；蒙特卡洛3万次模拟。仅研究，非投注建议。',
             fontsize=8, color='#555')
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(CHART, dpi=160)
    print('chart', CHART)


if __name__ == '__main__':
    main()
