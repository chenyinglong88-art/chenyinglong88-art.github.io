#!/usr/bin/env python3
"""Risk-adjusted ranking / observation approval: UEFA Nations League MD5 2026-11-12..14 (as of 2026-11-09 23:35 CET).

Fixed, transparent deductions on top of score_nations_league_nov12_nov17_2026.py (heuristic, NOT backtested):
  absence penalty   = max(0, 2.5 x selection key absences - 1.5 x opponent key absences)
  motivation penalty = 3 if a draw already satisfies the selection's immediate group objective
  other penalty      = 2 for a new-coach first match on the opponent side (uncertainty)
Heuristic win probability = Elo expectancy - 0.5 x no-vig market draw probability (uncalibrated).
Nations League has no frozen validated model and no reproducible 84-point scorer -> formal stake is always 0.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path('/home/ubuntu/football_betting_backtest')
SCORES = ROOT / 'output/nations_league_2026-11-12_to_11-17_rank_scores_asof1109.csv'
OUT = ROOT / 'output/nations_league_2026-11-12_to_11-14_ranked_observations_asof1109.csv'
SUMMARY = ROOT / 'output/nations_league_2026-11-12_to_11-14_ranked_observations_summary.json'
AS_OF = '2026-11-09 23:35 CET'
BANKROLL = 10836.26
REQUIRED_SCORE = 84.0

# (selection key absences, opponent key absences, motivation penalty, other penalty,
#  best verified decimal price, best-price bookmaker, short CN note)
REVIEW = {
    ('Slovenia', 'Switzerland'): (2, 3, 3.0, 0.0, 1.70, '22bet/Shangrila（Wincomparator）',
        '瑞士缺扎卡（小腿）、巴尔加斯；斯洛文尼亚缺谢什科、停赛扬扎与泽茨；瑞士平局即锁定直接升A，赢球动机打折'),
    ('Austria', 'Republic of Ireland'): (3, 2, 0.0, 0.0, 1.62, 'Shangrila（SportyTrader）',
        '奥地利缺阿拉巴、萨比策、维默等8人；爱尔兰缺卡伦、弗格森；奥地利主场赢球即升A'),
    ('Sweden', 'Bosnia and Herzegovina'): (4, 3, 0.0, 0.0, 1.58, 'Stake（SportyTrader）',
        '瑞典缺霍尔姆、斯塔费尔特、泽内利、贝里瓦尔；波黑缺停赛穆哈雷莫维奇、门将瓦西利，哲科已退役；瑞典赢球即升A'),
    ('Kosovo', 'Israel'): (3, 3, 0.0, 0.0, 2.05, 'Stake（SportyTrader）',
        '科索沃缺拉赫马尼、哈伊达里、穆斯利亚；以色列缺佩雷茨、巴里博、哈利拉伊利；科索沃争第二'),
    ('Italy', 'France'): (7, 4, 3.0, 0.0, 1.99, 'Pinnacle（直接页面）',
        '法国缺登贝莱、孔德、萨利巴、卡卢卢等，近期首发7人缺阵；意大利缺迪洛伦佐、基恩等4人；法国平局即进八强'),
    ('Bulgaria', 'Iceland'): (3, 3, 0.0, 0.0, 2.08, 'Stake/1xbet（SportyTrader）',
        '冰岛缺阿尔伯特·古德蒙德松、英加松、奥拉夫松；保加利亚缺明切夫、德斯波多夫等；冰岛领先第二2分'),
    ('Albania', 'Finland'): (2, 1, 0.0, 0.0, 2.17, '1xBet（SportyTrader）',
        '阿尔巴尼亚缺门将斯特拉科沙、布罗亚；芬兰缺洛德、卡马拉（纪律原因）；首回合芬兰2-1胜'),
    ('Türkiye', 'Belgium'): (2, 3, 0.0, 2.0, 2.00, 'Mozzart（Futbol24）',
        '比利时缺库尔图瓦、奥纳纳、停赛拉维亚；土耳其缺伊尔迪兹、停赛巴尔达克奇；土耳其新帅亚尔琴首秀'),
}


def main() -> None:
    f = pd.read_csv(SCORES)
    f.columns = [c.lstrip('\ufeff') for c in f.columns]
    f = f[f.has_full_1x2.astype(bool)].copy()
    for col in ['external_risk_penalty', 'absence_penalty', 'motivation_penalty', 'other_penalty',
                'best_price', 'heuristic_win_prob', 'heuristic_fair_odds', 'heuristic_ev_best_price']:
        f[col] = np.nan
    f['best_price_bookmaker'] = ''
    f['review_note'] = '未做逐场外部复核（排名第8之后）'
    f['risk_adjusted_score'] = f['ranking_score_100']
    for i, r in f.iterrows():
        key = (r.home_team, r.away_team)
        if key not in REVIEW:
            continue
        sk, ok, mot, oth, best, book, note = REVIEW[key]
        absence = max(0.0, 2.5 * sk - 1.5 * ok)
        total = absence + mot + oth
        draw = float(r.nv_draw)
        hw = float(r.elo_expectancy) - 0.5 * draw
        f.at[i, 'absence_penalty'] = absence
        f.at[i, 'motivation_penalty'] = mot
        f.at[i, 'other_penalty'] = oth
        f.at[i, 'external_risk_penalty'] = total
        f.at[i, 'risk_adjusted_score'] = max(0.0, float(r.ranking_score_100) - total)
        f.at[i, 'best_price'] = best
        f.at[i, 'best_price_bookmaker'] = book
        f.at[i, 'heuristic_win_prob'] = hw
        f.at[i, 'heuristic_fair_odds'] = 1.0 / hw
        f.at[i, 'heuristic_ev_best_price'] = hw * best - 1.0
        f.at[i, 'review_note'] = note
    f['score_gap_to_84'] = REQUIRED_SCORE - f['risk_adjusted_score']
    f['formal_approved'] = False
    f['formal_stake_cny'] = 0.0
    f['formal_blocker'] = ('欧国联无冻结历史验证模型；排名分为未回测启发式；风险调整分<84；'
                           '首发未公布；用户实际可成交价未提供')
    f = f.sort_values(['user_min_odds_pass', 'risk_adjusted_score'], ascending=[False, False]).reset_index(drop=True)
    f.insert(0, 'risk_adjusted_rank', np.arange(1, len(f) + 1))
    f.to_csv(OUT, index=False, encoding='utf-8-sig')

    top = f[f.best_price.notna()].head(8)
    summary = {
        'as_of': AS_OF, 'bankroll_cny': BANKROLL, 'fixtures_scored': int(len(f)),
        'fixtures_reviewed': int(f.best_price.notna().sum()), 'formal_approved': 0, 'formal_stake_cny': 0,
        'required_score': REQUIRED_SCORE,
        'top8': [
            {k: (round(float(v), 4) if isinstance(v, (float, np.floating)) else v) for k, v in {
                'rank': int(r.risk_adjusted_rank), 'date': r.date_cet, 'kickoff_cet': r.kickoff_cet,
                'kickoff_beijing': r.kickoff_beijing, 'match': f'{r.home_team} vs {r.away_team}',
                'selection': r.selection, 'dk_price': r.selection_odds, 'best_price': r.best_price,
                'best_price_bookmaker': r.best_price_bookmaker, 'base_score': r.ranking_score_100,
                'penalty': r.external_risk_penalty, 'risk_adjusted_score': r.risk_adjusted_score,
                'elo_expectancy': r.elo_expectancy, 'market_win_prob': r.no_vig_market_probability,
                'heuristic_win_prob': r.heuristic_win_prob, 'heuristic_fair_odds': r.heuristic_fair_odds,
                'heuristic_ev_best_price': r.heuristic_ev_best_price, 'note': r.review_note}.items()}
            for r in top.itertuples()],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    pd.set_option('display.width', 260)
    print(f[['risk_adjusted_rank', 'date_cet', 'home_team', 'away_team', 'selection', 'selection_odds', 'best_price',
             'ranking_score_100', 'external_risk_penalty', 'risk_adjusted_score', 'heuristic_win_prob',
             'heuristic_fair_odds', 'heuristic_ev_best_price']].head(14).to_string(
        index=False, float_format=lambda v: f'{v:.3f}'))


if __name__ == '__main__':
    main()
