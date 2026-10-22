#!/usr/bin/env python3
"""Risk-adjusted ranked observation list for UEL/UECL, 22 Oct 2026 (GMT+2 evening).

Inputs
- output/uefa_club_2026-10-22_rank_scores.csv  (transparent Elo/market/price score, 0-100)
- output/uefa_club_2026-10-22_clubelo_official_uel.csv (ClubElo official 1X2 probabilities, UEL only)
- per-match research findings (output/uefa_club_2026-10-22_external_notes.md), encoded below as fixed deductions

Rules (fixed before looking at outcomes; observation only)
- Probability used for EV: ClubElo official probability when published (UEL); otherwise the approximated
  Elo win probability shifted by the mean (official - approximation) gap measured on the 18 UEL matches.
- Value adjustment = clip(EV_pct, -10, +10) * 0.5  (range -5..+5) at the user's platform price.
- Risk deductions: >=4 listed absentees -6; 2-3 absentees -2; >=3 losses in last five -5;
  long away winless run -5; domestic match within 3 days -2; adverse market move -3;
  not individually researched -3.
- Formal status is always 0 CNY: European club competitions have no frozen validated model, the score is not
  historically validated, and the user's hard requirement (score >= 84) is not met by any match.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RANK = ROOT / "output" / "uefa_club_2026-10-22_rank_scores.csv"
OFFICIAL = ROOT / "output" / "uefa_club_2026-10-22_clubelo_official_uel.csv"
OUT_CSV = ROOT / "output" / "uefa_club_2026-10-22_ranked_observations.csv"
OUT_JSON = ROOT / "output" / "uefa_club_2026-10-22_ranked_observations_summary.json"

USER_MIN_SCORE = 84.0
USER_MIN_ODDS = 1.50

# research-based deductions and price notes, keyed by home team in the score file
RESEARCH = {
    "Olympiacos": dict(
        best_price=1.53, best_price_src="BetMGM 1.53（Oddspedia）；DK 1.50",
        deductions={"10/25主场Kalamata、10/28杯赛，三天后联赛": -2},
        facts="近5场全胜（4场净胜1球）；欧联2战全胜；Sparta欧联1胜1平；伤停未查到；首发未公布",
    ),
    "Pafos": dict(
        best_price=1.67, best_price_src="DK页面1.67；DK接口15:36为1.606；Legalbet均价1.65",
        deductions={"缺Goldar、Gorter、Kyriakides、Jajá、Ngamaleu（5人）": -6},
        facts="首轮1–3负Atalanta（0分）；最近联赛0–0 APOEL；Riga缺停赛Salazar；首发未公布",
    ),
    "Midtjylland": dict(
        best_price=1.714, best_price_src="美国盘最好DK 1.714（BetMGM 1.645–BetRivers 1.699）；ESPN接口无价",
        deductions={"伤病危机：Olafsson、Erlic、Gogorza、Junior Brumado、M. Jensen缺阵，Beni Junior存疑、Wätjen新伤": -6,
                    "10/25主场Lyngby，三天后联赛": -2},
        facts="首轮客1–1 Egnatia（15位）；近5场3胜2平不败；STVV首轮2–0、国内近4场3负；首发未公布",
    ),
    "Kauno Zalgiris": dict(
        best_price=1.775, best_price_src="BetRivers 1.775；DK 1.714–1.769；BetMGM/Caesars 1.667",
        deductions={"Brann缺Kasanwirjo（停赛）+Tronstad等5伤": -6, "Brann近5场3负": -5,
                    "10/25客场Lillestrøm，三天后联赛": -2},
        facts="Brann首轮2–1 Lincoln（10位）；Zalgiris首轮0–4负Brighton（36位）",
    ),
    "Braga": dict(
        best_price=2.05, best_price_src="DK开盘约1.69→接口1.909→页面2.05（主胜持续漂高）",
        deductions={"Braga三连败（1–2 Gil Vicente、0–3 København、1–3 Sporting）": -5,
                    "主胜赔率从约1.69漂至2.05，市场资金反向": -3,
                    "10/25客场Nacional，三天后联赛": -2},
        facts="Braga首轮0–3（35位0分）；Gent首轮1–0、近5场3胜1平；Braga缺Niakaté，Gent缺Ngom、Vergara",
    ),
    "Iberia 1999": dict(
        best_price=2.35, best_price_src="DK接口15:36为2.35；Legalbet 2.30；截图2.25",
        deductions={"Mjällby客场12场不胜（Scores24）": -5, "Mjällby缺Dalsgaard、Stavitski": -2,
                    "10/25客场Hammarby，三天后联赛": -2},
        facts="Mjällby首轮2–0（5位）；Iberia首轮0–2（33位）；Mjällby上轮联赛轮换0–1负",
    ),
}
UNRESEARCHED_PENALTY = -3.0


def value_adjust(ev: float) -> float:
    return float(np.clip(ev * 100, -10, 10) * 0.5)


def main() -> None:
    r = pd.read_csv(RANK)
    off = pd.read_csv(OFFICIAL)
    off_map = {}
    for o in off.to_dict("records"):
        off_map[o["home_team"]] = o

    # calibration: official ClubElo minus approximated selection probability on UEL matches
    gaps = []
    for row in r.to_dict("records"):
        o = off_map.get(row["home_team"])
        if o is None:
            continue
        p_off = (o["pH"] if row["selection_cn"] == "主胜" else o["pA"]) / 100
        gaps.append(p_off - row["elo_win_prob"])
    calib = float(np.mean(gaps))

    rows = []
    for row in r.to_dict("records"):
        if row["selection_odds"] < USER_MIN_ODDS:
            continue
        o = off_map.get(row["home_team"])
        if o is not None:
            p = (o["pH"] if row["selection_cn"] == "主胜" else o["pA"]) / 100
            p_src = "ClubElo官方赛程概率"
            p_draw = o["pD"] / 100
        else:
            p = float(np.clip(row["elo_win_prob"] + calib, 0.01, 0.98))
            p_src = f"Elo近似概率{row['elo_win_prob']:.3f}+校准{calib:+.3f}"
            p_draw = np.nan
        odds = float(row["selection_odds"])
        ev = p * odds - 1
        res = RESEARCH.get(row["home_team"])
        if res:
            ded = res["deductions"]
            ded_total = float(sum(ded.values()))
            ded_txt = "；".join(f"{k}（{v:+.0f}）" for k, v in ded.items())
            best = res["best_price"]
            best_src = res["best_price_src"]
            facts = res["facts"]
            researched = True
        else:
            ded_total = UNRESEARCHED_PENALTY
            ded_txt = f"未逐场核验伤停与近况（{UNRESEARCHED_PENALTY:+.0f}）"
            best = row["dk_selection_odds"] if pd.notna(row["dk_selection_odds"]) else odds
            best_src = "DraftKings接口"
            facts = ""
            researched = False
        ev_best = p * float(best) - 1
        va = value_adjust(ev)
        adj = row["ranking_score_100"] + ded_total + va
        rows.append({
            "competition": row["competition"], "kickoff_gmt8": row["kickoff_gmt8"], "kickoff_gmt2": row["kickoff_gmt2"],
            "match": f"{row['home_team']} vs {row['away_team']}", "selection": f"{row['selection']} {row['selection_cn']}",
            "user_platform_odds": odds, "best_verified_odds": round(float(best), 3), "best_price_source": best_src,
            "base_score_100": row["ranking_score_100"], "probability": round(p, 4), "probability_source": p_src,
            "clubelo_draw_prob": round(p_draw, 4) if pd.notna(p_draw) else None,
            "market_fair_prob": row["market_fair_prob"], "breakeven_odds": round(1 / p, 3),
            "ev_user_price": round(ev, 4), "ev_best_price": round(ev_best, 4), "value_adjust": round(va, 2),
            "risk_deductions": ded_total, "risk_detail": ded_txt, "facts": facts, "researched": researched,
            "risk_adjusted_score": round(adj, 2),
            "user_score84_pass": bool(adj >= USER_MIN_SCORE),
            "formal_stake_cny": 0,
            "formal_status": "观察：欧战无冻结验证模型；评分未经历史验证；<84分；首发未公布",
        })
    out = pd.DataFrame(rows).sort_values("risk_adjusted_score", ascending=False).reset_index(drop=True)
    out.insert(0, "risk_rank", np.arange(1, len(out) + 1))
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    # draw-bias diagnostic: ClubElo official draw vs de-vigged market draw on UEL
    d_bias = float((off["pD"] / 100 - off["mD"]).mean())
    summary = {
        "generated_at": "2026-10-22T15:40:00+02:00",
        "scope": "欧联18场+欧协联17场（用户截图），赔率>=1.50方向",
        "fixtures_scored": int(len(r)), "candidates_odds_ge_150": int(len(out)),
        "calibration_official_minus_approx_pp": round(calib * 100, 2),
        "clubelo_draw_minus_market_pp": round(d_bias * 100, 2),
        "score84_pass": int(out.user_score84_pass.sum()),
        "formal_approved": 0, "formal_stake_cny": 0,
        "top3": out.head(3)[["risk_rank", "match", "selection", "user_platform_odds", "risk_adjusted_score",
                              "ev_user_price"]].to_dict("records"),
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.set_option("display.width", 260)
    print(out[["risk_rank", "competition", "kickoff_gmt8", "match", "selection", "user_platform_odds",
               "best_verified_odds", "probability", "market_fair_prob", "breakeven_odds", "ev_user_price",
               "ev_best_price", "base_score_100", "risk_deductions", "value_adjust", "risk_adjusted_score"]]
          .to_string(index=False))
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
