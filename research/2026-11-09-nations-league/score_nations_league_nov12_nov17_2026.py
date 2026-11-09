#!/usr/bin/env python3
"""Transparent ranking for UEFA Nations League 2026-11-12..17 (as of 2026-11-09 CET).

Same heuristic as score_nations_league_rankings_sep24_sep28_2026.py (NOT backtested):
  strength 45 (Elo expectancy incl. 65 Elo home advantage) + market 30 (no-vig prob)
  + price band 15 + Elo/market alignment 10, minus 5 for matchday-6 fixtures whose
  matchday-5 results are still unknown. Only the market favourite of each fixture is scored.
Fixtures without a full public 1X2 are kept as Elo-only "pending" rows.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path('/home/ubuntu/football_betting_backtest')
LINES = ROOT / 'output/nations_league_2026-11-12_to_11-17_lines_asof1109.csv'
STANDINGS = ROOT / 'output/nations_league_2026-11-09_standings_espn.csv'
OUT = ROOT / 'output/nations_league_2026-11-12_to_11-17_rank_scores_asof1109.csv'
HOME_ADVANTAGE_ELO = 65.0
USER_MIN_ODDS = 1.50
STANDING_ALIAS = {'Bosnia-Herzegovina': 'Bosnia and Herzegovina'}


def price_points(odds: float) -> float:
    if 1.50 <= odds <= 2.00:
        return 15.0
    if 2.00 < odds <= 2.50:
        return 10.0
    if 1.30 <= odds < 1.50 or 2.50 < odds <= 3.00:
        return 5.0
    return 0.0


def elo_expectancy(gap: float) -> float:
    return 1.0 / (1.0 + 10.0 ** (-gap / 400.0))


def main() -> None:
    lines = pd.read_csv(LINES)
    lines.columns = [c.lstrip('\ufeff') for c in lines.columns]
    st = pd.read_csv(STANDINGS)
    st.columns = [c.lstrip('\ufeff') for c in st.columns]
    st['team'] = st['team'].replace(STANDING_ALIAS)
    table = st.set_index('team')
    rows = []
    for r in lines.to_dict('records'):
        has_odds = all(pd.notna(r[k]) for k in ('home_dec', 'draw_dec', 'away_dec'))
        home_gap = float(r['elo_home']) - float(r['elo_away']) + HOME_ADVANTAGE_ELO
        if has_odds:
            venue = 'H' if r['home_dec'] <= r['away_dec'] else 'A'
        else:
            venue = 'H' if home_gap >= 0 else 'A'
        selection = r['home_team'] if venue == 'H' else r['away_team']
        opponent = r['away_team'] if venue == 'H' else r['home_team']
        gap = home_gap if venue == 'H' else -home_gap
        exp = elo_expectancy(gap)
        out = {**r, 'selection': selection, 'opponent': opponent, 'venue': venue,
               'adjusted_elo_gap': gap, 'elo_expectancy': exp, 'has_full_1x2': has_odds}
        for side, team in (('sel', selection), ('opp', opponent)):
            if team in table.index:
                t = table.loc[team]
                out[f'{side}_group'] = t['group'].replace('Group ', '')
                out[f'{side}_pts'] = int(t['pts'])
                out[f'{side}_record'] = f"{int(t['w'])}胜{int(t['d'])}平{int(t['l'])}负 {int(t['gf'])}-{int(t['ga'])}"
                out[f'{side}_group_rank'] = int(t['rank'])
        md6 = str(r['date_cet']) >= '2026-11-15'
        out['matchday'] = 6 if md6 else 5
        if has_odds:
            odds = float(r['home_dec'] if venue == 'H' else r['away_dec'])
            mkt = float(r['nv_home'] if venue == 'H' else r['nv_away'])
            # Elo expectancy = P(win) + 0.5*P(draw); compare with the same market quantity.
            mkt_expectancy = mkt + 0.5 * float(r['nv_draw'])
            strength = float(np.clip((exp - 0.50) / 0.35, 0, 1) * 45)
            market = float(np.clip((mkt - 1 / 3) / (0.72 - 1 / 3), 0, 1) * 30)
            price = price_points(odds)
            align = 10.0 if gap >= 0 else 0.0
            base = strength + market + price + align
            penalty = 5.0 if md6 else 0.0
            out.update({'selection_odds': odds, 'no_vig_market_probability': mkt,
                        'market_expectancy_win_plus_half_draw': mkt_expectancy,
                        'elo_minus_market_expectancy_pp': (exp - mkt_expectancy) * 100,
                        'strength_points_45': strength, 'market_points_30': market,
                        'price_points_15': price, 'alignment_points_10': align,
                        'base_score_100': base, 'matchday6_uncertainty_penalty': penalty,
                        'ranking_score_100': max(0.0, base - penalty),
                        'user_min_odds_pass': odds >= USER_MIN_ODDS})
        else:
            out.update({'selection_odds': np.nan, 'ranking_score_100': np.nan,
                        'user_min_odds_pass': False})
        out['formal_strategy_eligible'] = False
        out['formal_status'] = '观察：欧国联无冻结验证模型与可复现84分评分链'
        rows.append(out)
    frame = pd.DataFrame(rows)
    priced = frame[frame.has_full_1x2].sort_values(['user_min_odds_pass', 'ranking_score_100'],
                                                    ascending=[False, False])
    pending = frame[~frame.has_full_1x2].sort_values('elo_expectancy', ascending=False)
    frame = pd.concat([priced, pending]).reset_index(drop=True)
    frame.insert(0, 'rank', np.where(frame.has_full_1x2, np.arange(1, len(frame) + 1), np.nan))
    frame.to_csv(OUT, index=False, encoding='utf-8-sig')
    pd.set_option('display.width', 250)
    cols = ['rank', 'date_cet', 'kickoff_cet', 'home_team', 'away_team', 'selection', 'selection_odds',
            'elo_expectancy', 'no_vig_market_probability', 'elo_minus_market_expectancy_pp', 'ranking_score_100',
            'user_min_odds_pass', 'sel_record', 'opp_record']
    print(frame[frame.has_full_1x2][cols].to_string(index=False, float_format=lambda v: f'{v:.3f}'))
    print('\nPENDING (no full 1X2 yet):')
    print(frame[~frame.has_full_1x2][['date_cet', 'home_team', 'away_team', 'selection', 'elo_expectancy',
                                      'sel_record', 'opp_record']].to_string(index=False,
                                                                              float_format=lambda v: f'{v:.3f}'))


if __name__ == '__main__':
    main()
