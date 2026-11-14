#!/usr/bin/env python3
"""Nations League 2026/27 MD5-MD6 motivation (stakes) simulator, as of 2026-11-14 13:40 CET.

For every remaining fixture we estimate, for each team, the expected 'objective utility' conditional on
winning / drawing / losing that fixture, simulating all other remaining fixtures (Poisson goals) and
applying UEFA group tie-breakers + League A cross-group ranking of 3rd/4th placed teams.

Utility weights (transparent heuristic, NOT backtested; 0-100):
  League A: 1st 100 | 2nd 85 (QF) | 3rd 60 if top-2 third (stay A, Pot 1) else 45 (A/B play-off, Pot 1)
            4th 30 if top-2 fourth (A/B play-off) else 0 (relegated)
  League B: 1st 100 (promoted, Pot 2) | 2nd 60 (A/B play-off, Pot 2) | 3rd 30 | 4th 10 (B/C play-off)
  League C: 1st 100 (promoted, Pot 3) | 2nd 55 (B/C play-off) | 3rd 12 | 4th 10
  League D: 1st 20 | 2nd 15 | 3rd 10 (all promoted)
Rules source: UEFA '2026/27 UEFA Nations League: All you need to know' (12 Nov 2026); EURO 2028 pots per AS (11 Nov 2026).
Match probabilities: DraftKings no-vig 1X2 where posted (ESPN API 2026-11-14 12:30 UTC), otherwise Elo 2026-11-14
(home advantage 65, Israel home neutral). Lambdas fitted so Poisson 1X2 reproduces those probabilities.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import poisson

ROOT = Path('/home/ubuntu/football_betting_backtest')
RES = ROOT / 'output/nations_league_2026-09-24_to_10-06_all_results_espn.csv'
SNAP = ROOT / 'output/nations_league_2026-11-14_1415_scoreboard_snapshot.csv'
OUT = ROOT / 'output/nations_league_2026-11-14_1415_motivation_by_fixture.csv'
OUT_POS = ROOT / 'output/nations_league_2026-11-14_1415_final_position_probabilities.csv'
N_SIM = 30000
rng = np.random.default_rng(20261114)

GROUPS = {
    'A1': ['France', 'Italy', 'Belgium', 'Türkiye'], 'A2': ['Germany', 'Netherlands', 'Serbia', 'Greece'],
    'A3': ['Spain', 'Croatia', 'England', 'Czechia'], 'A4': ['Portugal', 'Denmark', 'Norway', 'Wales'],
    'B1': ['Scotland', 'Switzerland', 'Slovenia', 'North Macedonia'], 'B2': ['Hungary', 'Ukraine', 'Georgia', 'Northern Ireland'],
    'B3': ['Israel', 'Austria', 'Republic of Ireland', 'Kosovo'], 'B4': ['Poland', 'Bosnia-Herzegovina', 'Romania', 'Sweden'],
    'C1': ['Albania', 'Finland', 'Belarus', 'San Marino'], 'C2': ['Montenegro', 'Armenia', 'Cyprus', 'Latvia'],
    'C3': ['Kazakhstan', 'Slovakia', 'Faroe Islands', 'Moldova'], 'C4': ['Iceland', 'Bulgaria', 'Estonia', 'Luxembourg'],
    'D1': ['Gibraltar', 'Malta', 'Andorra'], 'D2': ['Lithuania', 'Azerbaijan', 'Liechtenstein'],
}
TEAM_GROUP = {t: g for g, ts in GROUPS.items() for t in ts}
ELO = {  # international-football.net (eloratings.net) UEFA table as on 2026-11-14
    'Spain': 2282, 'England': 2144, 'France': 2104, 'Portugal': 2055, 'Netherlands': 1974, 'Switzerland': 1972,
    'Belgium': 1956, 'Italy': 1910, 'Norway': 1900, 'Germany': 1895, 'Croatia': 1861, 'Denmark': 1861, 'Austria': 1841,
    'Greece': 1804, 'Sweden': 1774, 'Türkiye': 1768, 'Scotland': 1746, 'Hungary': 1725, 'Ukraine': 1724,
    'Republic of Ireland': 1711, 'Kosovo': 1710, 'Slovenia': 1690, 'Poland': 1685, 'Serbia': 1683, 'Wales': 1681,
    'Bosnia-Herzegovina': 1672, 'Northern Ireland': 1672, 'Slovakia': 1665, 'Czechia': 1658, 'Georgia': 1628,
    'Israel': 1619, 'Albania': 1612, 'Iceland': 1603, 'Romania': 1554, 'Finland': 1552, 'North Macedonia': 1536,
    'Belarus': 1515, 'Montenegro': 1490, 'Luxembourg': 1422, 'Bulgaria': 1411, 'Estonia': 1400, 'Kazakhstan': 1393,
    'Faroe Islands': 1392, 'Armenia': 1354, 'Cyprus': 1346, 'Azerbaijan': 1326, 'Moldova': 1301, 'Lithuania': 1278,
    'Malta': 1263, 'Latvia': 1246, 'Andorra': 1056, 'Gibraltar': 1036, 'Liechtenstein': 887, 'San Marino': 820,
}
NEUTRAL_HOME = {'Israel'}
HA = 65.0


def util(league: str, pos: int, a_extra_ok: bool) -> float:
    if league == 'A':
        return {1: 100, 2: 85}.get(pos, (60 if a_extra_ok else 45) if pos == 3 else (30 if a_extra_ok else 0))
    if league == 'B':
        return {1: 100, 2: 60, 3: 30, 4: 10}[pos]
    if league == 'C':
        return {1: 100, 2: 55, 3: 12, 4: 10}[pos]
    return {1: 20, 2: 15, 3: 10}[pos]


def probs_from_lambdas(lh, la, kmax=12):
    k = np.arange(kmax + 1)
    m = np.outer(poisson.pmf(k, lh), poisson.pmf(k, la))
    return np.tril(m, -1).sum(), np.trace(m), np.triu(m, 1).sum()


def fit_lambdas(ph, pd_, pa):
    def loss(x):
        lh, la = np.exp(x)
        h, d, a = probs_from_lambdas(lh, la)
        return (h - ph) ** 2 + (d - pd_) ** 2 + (a - pa) ** 2
    r = minimize(loss, np.log([1.3, 1.1]), method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-10})
    return tuple(np.exp(r.x))


def elo_lambdas(home, away, total=2.6):
    gap = ELO[home] - ELO[away] + (0.0 if home in NEUTRAL_HOME else HA)
    exp = 1.0 / (1.0 + 10 ** (-gap / 400.0))
    def loss(s):
        lh, la = max(0.05, total / 2 + s / 2), max(0.05, total / 2 - s / 2)
        h, d, a = probs_from_lambdas(lh, la)
        return (h + 0.5 * d - exp) ** 2
    r = minimize(lambda x: loss(x[0]), [0.5], method='Nelder-Mead')
    s = r.x[0]
    return max(0.05, total / 2 + s / 2), max(0.05, total / 2 - s / 2)


def rank_group(teams, matches):
    """matches: list of (h, a, hg, ag). Return teams ordered per UEFA tie-breakers (simplified, one h2h pass)."""
    st = {t: dict(p=0, gd=0, gf=0, agf=0, w=0, aw=0) for t in teams}
    for h, a, hg, ag in matches:
        st[h]['gf'] += hg; st[a]['gf'] += ag; st[a]['agf'] += ag
        st[h]['gd'] += hg - ag; st[a]['gd'] += ag - hg
        if hg > ag: st[h]['p'] += 3; st[h]['w'] += 1
        elif hg < ag: st[a]['p'] += 3; st[a]['w'] += 1; st[a]['aw'] += 1
        else: st[h]['p'] += 1; st[a]['p'] += 1
    by_pts = defaultdict(list)
    for t in teams:
        by_pts[st[t]['p']].append(t)
    order = []
    for pts in sorted(by_pts, reverse=True):
        tied = by_pts[pts]
        if len(tied) == 1:
            order += tied; continue
        h2h = {t: dict(p=0, gd=0, gf=0) for t in tied}
        for h, a, hg, ag in matches:
            if h in h2h and a in h2h:
                h2h[h]['gf'] += hg; h2h[a]['gf'] += ag; h2h[h]['gd'] += hg - ag; h2h[a]['gd'] += ag - hg
                if hg > ag: h2h[h]['p'] += 3
                elif hg < ag: h2h[a]['p'] += 3
                else: h2h[h]['p'] += 1; h2h[a]['p'] += 1
        key = lambda t: (h2h[t]['p'], h2h[t]['gd'], h2h[t]['gf'], st[t]['gd'], st[t]['gf'], st[t]['agf'], st[t]['w'],
                         st[t]['aw'], rng.random())
        order += sorted(tied, key=key, reverse=True)
    return order, st


def main() -> None:
    res = pd.read_csv(RES)
    snap = pd.read_csv(SNAP)
    played, remaining = [], []
    for r in res.itertuples():
        played.append((r.home_team, r.away_team, int(r.home_score), int(r.away_score)))
    for r in snap.itertuples():
        if r.status == 'STATUS_FULL_TIME':
            played.append((r.home, r.away, int(r.hs), int(r.as_)))
        else:
            if pd.notna(r.H) and pd.notna(r.D) and pd.notna(r.A):
                inv = np.array([1 / r.H, 1 / r.D, 1 / r.A]); nv = inv / inv.sum()
                lh, la = fit_lambdas(*nv); src = 'DraftKings no-vig'
            else:
                lh, la = elo_lambdas(r.home, r.away); nv = np.array(probs_from_lambdas(lh, la)); src = 'Elo 2026-11-14'
            remaining.append(dict(t=r.t, home=r.home, away=r.away, lh=lh, la=la, pH=nv[0], pD=nv[1], pA=nv[2], src=src,
                                  H=r.H, D=r.D, A=r.A, id=r.id))
    assert len(played) == 122, len(played)
    for h, a, *_ in played:
        assert TEAM_GROUP[h] == TEAM_GROUP[a], (h, a)
    print('played', len(played), 'remaining', len(remaining))

    base = defaultdict(list)
    for m in played:
        base[TEAM_GROUP[m[0]]].append(m)
    nrem = len(remaining)
    lh = np.array([m['lh'] for m in remaining]); la = np.array([m['la'] for m in remaining])
    HG = rng.poisson(lh, size=(N_SIM, nrem)); AG = rng.poisson(la, size=(N_SIM, nrem))
    rem_by_group = defaultdict(list)
    for j, m in enumerate(remaining):
        rem_by_group[TEAM_GROUP[m['home']]].append(j)

    teams = list(TEAM_GROUP)
    U = np.zeros((N_SIM, len(teams))); POS = np.zeros((N_SIM, len(teams)), dtype=int)
    tidx = {t: i for i, t in enumerate(teams)}
    for s in range(N_SIM):
        a_info = {}
        for g, ts in GROUPS.items():
            ms = list(base[g]) + [(remaining[j]['home'], remaining[j]['away'], int(HG[s, j]), int(AG[s, j]))
                                  for j in rem_by_group[g]]
            order, st = rank_group(ts, ms)
            for p, t in enumerate(order, 1):
                POS[s, tidx[t]] = p
                if g[0] == 'A' and p in (3, 4):
                    a_info.setdefault(p, []).append((st[t]['p'], st[t]['gd'], st[t]['gf'], st[t]['agf'], st[t]['w'],
                                                     rng.random(), t))
            if g[0] != 'A':
                for p, t in enumerate(order, 1):
                    U[s, tidx[t]] = util(g[0], p, False)
        for p in (3, 4):
            ranked = sorted(a_info[p], reverse=True)
            for k, row in enumerate(ranked):
                U[s, tidx[row[-1]]] = util('A', p, k < 2)
        for g, ts in GROUPS.items():
            if g[0] == 'A':
                for t in ts:
                    if POS[s, tidx[t]] in (1, 2):
                        U[s, tidx[t]] = util('A', POS[s, tidx[t]], False)

    pos_rows = []
    for t in teams:
        i = tidx[t]
        row = dict(group=TEAM_GROUP[t], team=t, exp_utility=U[:, i].mean())
        for p in range(1, 5):
            row[f'p_pos{p}'] = (POS[:, i] == p).mean()
        pos_rows.append(row)
    pd.DataFrame(pos_rows).sort_values(['group', 'exp_utility'], ascending=[True, False]).to_csv(
        OUT_POS, index=False, encoding='utf-8-sig')

    rows = []
    for j, m in enumerate(remaining):
        hw, dr, aw = HG[:, j] > AG[:, j], HG[:, j] == AG[:, j], HG[:, j] < AG[:, j]
        out = dict(kickoff_cet=m['t'], group=TEAM_GROUP[m['home']], home=m['home'], away=m['away'], prob_source=m['src'],
                   dk_home=m['H'], dk_draw=m['D'], dk_away=m['A'], p_home=m['pH'], p_draw=m['pD'], p_away=m['pA'])
        for side, team, win, lose in [('home', m['home'], hw, aw), ('away', m['away'], aw, hw)]:
            i = tidx[team]
            uw, ud, ul = U[win, i].mean(), U[dr, i].mean(), U[lose, i].mean()
            out.update({f'{side}_U_win': uw, f'{side}_U_draw': ud, f'{side}_U_loss': ul,
                        f'{side}_need_win': uw - ud, f'{side}_stake': uw - ul,
                        f'{side}_exp_utility': U[:, i].mean()})
        rows.append(out)
    df = pd.DataFrame(rows)
    for side, opp in [('home', 'away'), ('away', 'home')]:
        df[f'{side}_motivation_gap'] = df[f'{side}_need_win'] - df[f'{opp}_stake']
    df.to_csv(OUT, index=False, encoding='utf-8-sig')
    pd.set_option('display.width', 260)
    cols = ['kickoff_cet', 'group', 'home', 'away', 'dk_home', 'dk_draw', 'dk_away', 'home_need_win', 'home_stake',
            'away_need_win', 'away_stake', 'home_motivation_gap', 'away_motivation_gap']
    print(df[cols].to_string(index=False, float_format=lambda v: f'{v:.1f}'))


if __name__ == '__main__':
    main()
