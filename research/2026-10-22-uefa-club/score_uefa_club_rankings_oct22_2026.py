#!/usr/bin/env python3
"""UEFA Europa League / Conference League 2026-10-22 transparent ranking score.

This reuses the frozen Nations League observation formula (score_nations_league_rankings_sep24_sep28_2026.py)
with ClubElo club ratings (page snapshot dated 2026-10-21, created 2026-10-22 09:49) instead of national-team Elo.
It is an OBSERVATION ranking only: there is no frozen, historically validated model for UEFA club competitions,
so formal approval is always False and the formal stake is 0.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "output" / "uefa_club_2026-10-22_screenshot_odds.csv"
ELO_JSON = ROOT / "xg_data" / "raw" / "clubelo_oct22" / "clubelo_2026-10-21_parsed.json"
ESPN_DIR = ROOT / "xg_data" / "raw" / "espn_uefa_oct22"
OUTPUT = ROOT / "output" / "uefa_club_2026-10-22_rank_scores.csv"

NAME_MAP = {
    "Ararat-Armenia": "Ararat-Armenia", "AZ Alkmaar": "AZ", "Dinamo Zagreb": "Dinamo Zagreb",
    "NEC Nijmegen": "Nijmegen", "Ferencvaros": "Ferencvaros", "Torreense": "Torreense",
    "Juventus": "Juventus", "Rennes": "Rennes", "Lech Poznan": "Lech", "Sunderland": "Sunderland",
    "OFI Crete": "OFI", "Leverkusen": "Leverkusen", "Union SG": "St Gillis",
    "Hapoel Beer Sheva": "Beer-Sheva", "Sturm Graz": "Sturm Graz", "Marseille": "Marseille",
    "Besiktas": "Besiktas", "Crystal Palace": "Crystal Palace", "Bournemouth": "Bournemouth",
    "Milan": "Milan", "Celje": "Celje", "Salzburg": "RB Salzburg", "Celtic": "Celtic",
    "Celta Vigo": "Celta", "Hoffenheim": "Hoffenheim", "Lyon": "Lyon", "Jagiellonia": "Jagiellonia",
    "Anderlecht": "Anderlecht", "Lillestrom": "Lillestrøm", "Real Sociedad": "Real Sociedad",
    "Olympiacos": "Olympiakos", "Sparta Praha": "Sparta Praha", "Omonia": "Omonia", "Benfica": "Benfica",
    "Plzen": "Viktoria Plzeň", "Levski Sofia": "Levski", "Getafe": "Getafe", "Lugano": "Lugano",
    "Iberia 1999": "FC Iberia 1999", "Mjallby": "Mjällby", "Inter Escaldes": "Escaldes",
    "Universitatea Craiova": "Craiova", "Jablonec": "Jablonec", "Brighton": "Brighton",
    "Kauno Zalgiris": "Kauno Zalgiris", "Brann": "Brann", "Nordsjaelland": "Nordsjaelland",
    "CSKA Sofia": "CSKA Sofia", "Pafos": "Paphos", "Riga FC": "FK Riga",
    "Red Star Belgrade": "Crvena Zvezda", "FC Copenhagen": "FC Kobenhavn", "Trabzonspor": "Trabzonspor",
    "Hearts": "Hearts", "Aarhus": "Aarhus", "Egnatia": "Egnatia Rrogozhi", "Ajax": "Ajax",
    "Atalanta": "Atalanta", "Borac Banja Luka": "Borac Banja Luka", "KuPS": "Kuopio", "Braga": "Braga",
    "Gent": "Gent", "Lincoln Red Imps": "Lincoln", "Twente": "Twente", "Midtjylland": "Midtjylland",
    "Sint-Truiden": "St Truiden", "Monaco": "Monaco", "Freiburg": "Freiburg", "Thun": "Thun",
    "Hajduk Split": "Hajduk",
}
HOME_ADVANTAGE_ELO = 65.0  # same constant as the frozen Nations League observation score
USER_MIN_ODDS = 1.50
USER_MIN_SCORE = 84.0


def american_to_decimal(value) -> float | None:
    try:
        v = float(str(value).replace("+", ""))
    except (TypeError, ValueError):
        return None
    if v == 0:
        return None
    return 1 + v / 100 if v > 0 else 1 + 100 / abs(v)


def espn_lines() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for f in sorted(ESPN_DIR.glob("*.json")):
        for event in json.loads(f.read_text()).get("events", []):
            comp = event["competitions"][0]
            odds = (comp.get("odds") or [{}])[0] or {}
            ml = odds.get("moneyline") or {}
            get = lambda side: american_to_decimal(((ml.get(side) or {}).get("close") or {}).get("odds"))
            out[str(event["id"])] = {"dk_home": get("home"), "dk_draw": get("draw"), "dk_away": get("away"),
                                     "dk_status": event["status"]["type"]["name"]}
    return out


def price_points(odds: float) -> float:
    if 1.50 <= odds <= 2.00:
        return 15.0
    if 2.00 < odds <= 2.50:
        return 10.0
    if 1.30 <= odds < 1.50 or 2.50 < odds <= 3.00:
        return 5.0
    return 0.0


def main() -> None:
    elo_raw = json.loads(ELO_JSON.read_text(encoding="utf-8"))
    elo = {k: float(v[0]) for k, v in elo_raw.items()}
    dk = espn_lines()
    rows = []
    for r in pd.read_csv(INPUT, dtype={"espn_id": str}).to_dict("records"):
        h, d, a = float(r["home_odds"]), float(r["draw_odds"]), float(r["away_odds"])
        implied = np.array([1 / h, 1 / d, 1 / a])
        overround = implied.sum()
        fair = implied / overround
        venue = "H" if h <= a else "A"
        sel = r["home_team"] if venue == "H" else r["away_team"]
        opp = r["away_team"] if venue == "H" else r["home_team"]
        sel_odds = h if venue == "H" else a
        p_mkt = float(fair[0] if venue == "H" else fair[2])
        p_draw_mkt = float(fair[1])
        e_sel, e_opp = elo[NAME_MAP[sel]], elo[NAME_MAP[opp]]
        gap = e_sel - e_opp + (HOME_ADVANTAGE_ELO if venue == "H" else -HOME_ADVANTAGE_ELO)
        expectancy = 1 / (1 + 10 ** (-gap / 400))
        # Elo expectancy = P(win) + 0.5 P(draw); draw share taken from the de-vigged market (transparent assumption)
        p_win_elo = float(np.clip(expectancy - 0.5 * p_draw_mkt, 0.01, 0.98))
        ev_elo = p_win_elo * sel_odds - 1
        strength = float(np.clip((expectancy - 0.50) / 0.35, 0, 1) * 45)
        market = float(np.clip((p_mkt - 1 / 3) / (0.72 - 1 / 3), 0, 1) * 30)
        price = price_points(sel_odds)
        align = 10.0 if gap >= 0 else 0.0
        score = strength + market + price + align
        espn = dk.get(str(r.get("espn_id") or ""), {})
        dk_sel = espn.get("dk_home") if venue == "H" else espn.get("dk_away")
        rows.append({
            **r,
            "selection": sel, "selection_cn": "主胜" if venue == "H" else "客胜", "opponent": opp,
            "selection_odds": sel_odds, "dk_selection_odds": round(dk_sel, 3) if dk_sel else None,
            "draw_odds_sel_match": d, "overround": round(overround, 4),
            "selection_elo": int(e_sel), "opponent_elo": int(e_opp), "adjusted_elo_gap": round(gap, 1),
            "elo_expectancy": round(expectancy, 4), "market_fair_prob": round(p_mkt, 4),
            "market_fair_draw": round(p_draw_mkt, 4), "elo_win_prob": round(p_win_elo, 4),
            "elo_edge_pp": round((p_win_elo - p_mkt) * 100, 2), "elo_ev": round(ev_elo, 4),
            "elo_breakeven_odds": round(1 / p_win_elo, 3),
            "strength_points_45": round(strength, 2), "market_points_30": round(market, 2),
            "price_points_15": price, "alignment_points_10": align, "ranking_score_100": round(score, 2),
            "user_min_odds_pass": sel_odds >= USER_MIN_ODDS, "user_score84_pass": score >= USER_MIN_SCORE,
            "formal_strategy_eligible": False, "formal_stake_cny": 0,
            "formal_status": "观察：欧战无冻结验证模型；评分为未经历史验证的透明观察分",
        })
    out = pd.DataFrame(rows).sort_values(["user_min_odds_pass", "ranking_score_100"], ascending=[False, False])
    out.insert(0, "rank", np.arange(1, len(out) + 1))
    out.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    cols = ["rank", "competition", "kickoff_gmt8", "home_team", "away_team", "selection_cn", "selection_odds",
            "dk_selection_odds", "selection_elo", "opponent_elo", "adjusted_elo_gap", "elo_expectancy",
            "market_fair_prob", "elo_win_prob", "elo_ev", "ranking_score_100", "user_min_odds_pass"]
    pd.set_option("display.width", 260)
    print(out[cols].to_string(index=False))
    print("score>=84 & odds>=1.50:", int((out.user_min_odds_pass & out.user_score84_pass).sum()))


if __name__ == "__main__":
    main()
