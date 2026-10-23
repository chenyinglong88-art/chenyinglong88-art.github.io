#!/usr/bin/env python3
"""Risk-adjusted observation ranking for five-league fixtures 2026-10-23..29 (as of 2026-10-23 07:00 CEST).

This is a transparent, NOT historically validated observation score (0-100). It never creates formal approval:
the user's reproducible 84 (EPL 88) score does not exist, so formal stake stays 0 CNY.

Base score (DraftKings price from ESPN, same source for every match):
- B model edge          30 * clip(EV_B / 0.20, 0, 1)
- Bayes agreement       25 * clip(1 + EV_Bayes / 0.20, 0, 1)   (Bayes EV 0 -> 25, -20% -> 0)
- Market support        15 * clip((p_mkt_fair - 1/3) / (0.72 - 1/3), 0, 1)
- Model consistency     15 * clip(1 - |pB - pBayes| / 25pp, 0, 1)
- Price band            15 if 1.50-2.00, 10 if 2.00-2.50, 5 if 2.50-3.00, else 0
Fixed research adjustments (written before outcomes):
- home side >=4 listed absentees -6; 2-3 absentees -2; away side >=4 absentees +3
- home played European match within 3 days -3; away side did +2
- home side <=1 win in last five -5
- home price lengthened >=0.05 from DraftKings open -3
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
APPROVAL = OUT / "oct23_oct29_2026_asof1023_approval.csv"
LINES = OUT / "oct23_oct29_2026_asof1023_espn_lines.csv"
MODELS = OUT / "oct23_oct29_2026_asof1023_models_with_lines.csv"
OUT_CSV = OUT / "oct23_oct29_2026_asof1023_risk_ranking.csv"
OUT_JSON = OUT / "oct23_oct29_2026_asof1023_risk_ranking_summary.json"

# research findings (workflow 5f3b681dda3f, 2026-10-23 ~07:00 CEST); see output/oct23_2026_external_notes.md
RESEARCH = {
    ("Como", "Sassuolo"): dict(
        best=1.526, best_src="BetMGM 1.526；DK/bet365 1.50；Fanatics 1.476；FanDuel 1.455",
        home_out=3, away_out=4, home_euro_3d=True, away_euro_3d=False, home_wins_last5=2,
        notes="Como周三欧冠4–1胜曼联，仅休3天；缺Chalobah、J. Rodríguez、Diao，Kean存疑；Sassuolo缺Koné、Idzes、Boloca、Leysen；Como第5（14分）、Sassuolo第13（8分）"),
    ("Vallecano", "Elche"): dict(
        best=1.78, best_src="Bovada 1.78；DK/BetMGM 1.769",
        home_out=2, away_out=1, home_euro_3d=False, away_euro_3d=False, home_wins_last5=2,
        notes="Rayo缺Luiz Felipe、Batalla，Ratiu、Nteka存疑，Ciss停赛与否说法冲突；Elche缺Aguado、近3场不败（2连平）；Rayo第14（9分）、Elche第18（7分）"),
    ("Athletic Club", "Getafe"): dict(
        best=1.606, best_src="DK 1.606（ESPN当前−165）；FanDuel 1.588",
        home_out=4, away_out=4, home_euro_3d=False, away_euro_3d=True, home_wins_last5=1,
        notes="Athletic近5场1胜（联赛4场不胜，刚1–3负Levante）；缺Guruzeta、Sancet、Djaló、Egiluz；Getafe周四欧协联2–5负Lugano，缺Romero、Mangala、Uche、Juanmi，Ünal存疑"),
    ("Barcelona", "Real Madrid"): dict(
        best=1.65, best_src="1xBet 1.65；DK 1.645；bet365 1.613–1.62",
        home_out=4, away_out=4, home_euro_3d=False, away_euro_3d=False, home_wins_last5=4,
        notes="巴萨周二欧冠2–4负PSG；缺Olmo、Bardghji、Christensen、Eric García，Koundé重大存疑；皇马缺Rodrygo、Mendy、Asencio，Vinícius停赛；巴萨9战全胜第1（27分）"),
    ("Sociedad", "Levante"): dict(
        best=1.667, best_src="DK 1.667；FanDuel 1.588",
        home_out=4, away_out=0, home_euro_3d=True, away_euro_3d=False, home_wins_last5=4,
        notes="皇家社会周四客场欧联6–0胜Lillestrøm（挪威往返，约72小时）；缺Odriozola、Aramburu、Beitia、Herrera；Levante两人小伤存疑"),
}


def clip01(x: float) -> float:
    return float(np.clip(x, 0, 1))


def price_points(o: float) -> float:
    if 1.50 <= o <= 2.00:
        return 15.0
    if 2.00 < o <= 2.50:
        return 10.0
    if 2.50 < o <= 3.00:
        return 5.0
    return 0.0


def beijing(utc: str) -> str:
    t = pd.Timestamp(utc)
    t = t.tz_localize("UTC") if t.tzinfo is None else t.tz_convert("UTC")
    return t.tz_convert("Asia/Shanghai").strftime("%m-%d %H:%M")


def local_eu(utc: str) -> str:
    t = pd.Timestamp(utc)
    t = t.tz_localize("UTC") if t.tzinfo is None else t.tz_convert("UTC")
    return t.tz_convert("Europe/Paris").strftime("%m-%d %H:%M %Z")


def main() -> None:
    a = pd.read_csv(APPROVAL)
    m = pd.read_csv(MODELS)
    m.columns = [c.lstrip("\ufeff") for c in m.columns]
    rows = []
    for _, r in a[a["status"].eq("条件观察，未批准")].iterrows():
        mm = m[(m.home_team == r.home_team) & (m.away_team == r.away_team)].iloc[0]
        res = RESEARCH[(r.home_team, r.away_team)]
        o = float(r.odds)
        ev_b, ev_z = r.p_b * o - 1, r.p_bayes_same * o - 1
        gap = abs(r.p_b - r.p_bayes_same) * 100
        comp = {
            "b_edge_30": 30 * clip01(ev_b / 0.20),
            "bayes_agree_25": 25 * clip01(1 + ev_z / 0.20),
            "market_15": 15 * clip01((r.p_mkt_fair - 1 / 3) / (0.72 - 1 / 3)),
            "consistency_15": 15 * clip01(1 - gap / 25),
            "price_15": price_points(o),
        }
        base = sum(comp.values())
        adj = {}
        if res["home_out"] >= 4:
            adj["主队缺阵≥4人"] = -6
        elif res["home_out"] >= 2:
            adj["主队缺阵2–3人"] = -2
        if res["away_out"] >= 4:
            adj["客队缺阵≥4人"] = +3
        if res["home_euro_3d"]:
            adj["主队3天内踢欧战"] = -3
        if res["away_euro_3d"]:
            adj["客队3天内踢欧战"] = +2
        if res["home_wins_last5"] <= 1:
            adj["主队近5场≤1胜"] = -5
        opened = float(mm.home_open_dec) if pd.notna(mm.home_open_dec) else o
        if o - opened >= 0.05:
            adj[f"主胜由{opened:.3f}漂至{o:.3f}"] = -3
        total = base + sum(adj.values())
        rows.append({
            "kickoff_beijing": beijing(mm.kickoff_utc), "kickoff_local": local_eu(mm.kickoff_utc),
            "league": r.league, "match": f"{r.home_team} vs {r.away_team}", "selection": "主胜",
            "dk_odds": round(o, 3), "dk_open": round(opened, 3), "best_odds": res["best"], "best_src": res["best_src"],
            "p_b": round(r.p_b, 4), "p_bayes": round(r.p_bayes_same, 4), "p_mkt_fair": round(r.p_mkt_fair, 4),
            "ev_b": round(ev_b, 4), "ev_bayes": round(ev_z, 4), "ev_b_best": round(r.p_b * res["best"] - 1, 4),
            "ev_bayes_best": round(r.p_bayes_same * res["best"] - 1, 4), "model_gap_pp": round(gap, 2),
            "b_min_odds_ev1": round(1.01 / r.p_b, 3), "both_min_odds_ev1": round(1.01 / min(r.p_b, r.p_bayes_same), 3),
            **{k: round(v, 2) for k, v in comp.items()}, "base_score": round(base, 2),
            "adjustments": "；".join(f"{k}{v:+d}" for k, v in adj.items()), "adjust_total": sum(adj.values()),
            "risk_score": round(total, 2), "formal_core_path": bool(mm.division != "E0" and o <= 1.50 + 1e-9),
            "required_score": 88 if mm.division == "E0" else 84, "formal_stake_cny": 0,
            "status": "条件观察，未批准：可复现84分评分不存在；动态贝叶斯EV为负；首发未公布",
            "notes": res["notes"], "odds_url": r.odds_url,
        })
    out = pd.DataFrame(rows).sort_values("risk_score", ascending=False).reset_index(drop=True)
    out.insert(0, "risk_rank", np.arange(1, len(out) + 1))
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    # notable high-EV directions outside formal authorisation (both models positive), for transparency
    ev = pd.read_csv(OUT / "oct23_oct29_2026_asof1023_conservative_ev_ranking.csv")
    lines = pd.read_csv(LINES)
    both_pos = ev[(ev.ev_b > 0.05) & (ev.ev_bayes > 0.05) & (ev.odds <= 3.0)].copy()
    summary = {
        "as_of": "2026-10-23 07:05 CEST",
        "fixtures_modelled": int(len(a)), "fixtures_priced": int(a.odds.notna().sum()),
        "conditional_watch": int(len(out)), "formal_approved": 0, "formal_stake_cny": 0,
        "top": out[["risk_rank", "kickoff_beijing", "match", "dk_odds", "best_odds", "ev_b", "ev_bayes",
                    "risk_score"]].to_dict("records"),
        "both_models_positive_not_authorised": both_pos[["kickoff_gmt2", "league", "home_team", "away_team",
                                                         "selection_cn", "odds", "ev_b", "ev_bayes"]]
        .round(4).to_dict("records"),
        "espn_lines_rows": int(len(lines)),
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    pd.set_option("display.width", 260)
    print(out[["risk_rank", "kickoff_beijing", "kickoff_local", "league", "match", "dk_odds", "dk_open", "best_odds",
               "p_b", "p_bayes", "p_mkt_fair", "ev_b", "ev_bayes", "model_gap_pp", "both_min_odds_ev1",
               "base_score", "adjust_total", "risk_score", "formal_core_path"]].to_string(index=False))
    for _, r in out.iterrows():
        print(r.risk_rank, r.match, r.adjustments)
    print(both_pos[["kickoff_gmt2", "league", "home_team", "away_team", "selection_cn", "odds", "p_b", "p_bayes",
                    "p_mkt_fair", "ev_b", "ev_bayes"]].to_string(index=False))


if __name__ == "__main__":
    main()
