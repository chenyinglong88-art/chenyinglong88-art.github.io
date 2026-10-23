#!/usr/bin/env python3
"""Approval and ranking for five-league fixtures 2026-10-23..29 (as of 2026-10-23 GMT+2).

Rules (locked, unchanged):
- Formal core: five leagues, 90-minute 1X2 home win, odds <= 1.50, B EV >= 1%.
- Locked extension: EPL / LaLiga home win, odds 1.25-2.00, B EV >= 1%.
- User floor: odds >= 1.50. Bayes is risk prompt only; direction must agree.
- Required reproducible score: 84 (EPL 88). No reproducible scorer exists -> formal approval impossible.
- Away / draw / other leagues' high odds are not authorised; listed only as price checks.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
SRC = OUT / "oct23_oct29_2026_asof1023_models_with_lines.csv"
AS_OF = "2026-10-23 06:52 GMT+2"
BANKROLL = 10836.26
OPEN_EXPOSURE = 0.0
USER_MIN_ODDS = 1.50
CORE_MAX_ODDS = 1.50
EXT_MIN, EXT_MAX = 1.25, 2.00
NORMAL_CAP = 0.05
DAILY_CAP = 0.12

# Cross-checked prices / injury notes are filled after research (see output/oct23_2026_external_notes.md).
BEST_PRICE: dict = {}
SEL_COL = {"H": "home_dec", "D": "draw_dec", "A": "away_dec"}
SEL_CN = {"H": "主胜", "D": "平局", "A": "客胜"}


def classify(r: pd.Series) -> tuple[str, str, int]:
    """Return status, reason and number of gates passed (for ranking)."""
    sel, div, odds, ev = r["b_top_selection"], r["division"], r["odds"], r["ev_b"]
    gates = 0
    if pd.isna(odds):
        return "无报价", "ESPN/DraftKings尚未开盘", 0
    if sel != "H":
        return "拒绝", f"B版方向为{SEL_CN[sel]}；客胜/平局无正式授权", 0
    gates += 1
    in_core = odds <= CORE_MAX_ODDS + 1e-9
    in_ext = div in {"E0", "SP1"} and EXT_MIN <= odds <= EXT_MAX
    if odds < USER_MIN_ODDS - 1e-9:
        return "拒绝", "低于用户1.50最低赔率", gates
    gates += 1
    if not (in_core or in_ext):
        if div in {"E0", "SP1"}:
            return "拒绝", "高于锁定扩展2.00上限", gates
        return "拒绝", "非英超/西甲且赔率高于核心1.50上限", gates
    gates += 1
    if ev < 0.01:
        return "拒绝", "B版EV低于1%", gates
    gates += 1
    if not bool(r["model_direction_agreement"]):
        return "拒绝", "B版与动态贝叶斯方向不一致", gates
    gates += 1
    return "条件观察，未批准", "价格与模型门槛通过，但可复现总分（英超88/其他84）与正式首发未通过", gates


def main() -> None:
    df = pd.read_csv(SRC)
    df.columns = [c.lstrip("\ufeff") for c in df.columns]
    df["odds"] = df.apply(lambda r: r[SEL_COL[r["b_top_selection"]]], axis=1)
    df["p_b"] = df["b_top_probability"]
    df["p_bayes_same"] = df.apply(lambda r: r[f"p_bayes_{r['b_top_selection']}"], axis=1)
    df["p_mkt_fair"] = df.apply(lambda r: r[f"fair_mkt_{r['b_top_selection']}"], axis=1)
    df["ev_b"] = df["p_b"] * df["odds"] - 1
    df["ev_bayes"] = df["p_bayes_same"] * df["odds"] - 1
    df["edge_vs_market_pp"] = (df["p_b"] - df["p_mkt_fair"]) * 100
    df["model_gap_pp"] = (df["p_b"] - df["p_bayes_same"]).abs() * 100
    df["raw_kelly"] = (df["ev_b"] / (df["odds"] - 1)).clip(lower=0)
    df["min_odds_ev1pct"] = 1.01 / df["p_b"]
    res = df.apply(classify, axis=1, result_type="expand")
    df["status"], df["reason"], df["gates_passed"] = res[0], res[1], res[2]
    df["required_score"] = df["division"].map(lambda d: 88 if d == "E0" else 84)
    df["score_available"] = False
    df["formal_approved"] = False
    df["formal_stake_cny"] = 0.0
    df["selection_cn"] = df["b_top_selection"].map(SEL_CN)
    df["best_uk_odds"] = df.apply(lambda r: BEST_PRICE.get((r["home_team"], r["away_team"]), {}).get("best_odds"), axis=1)
    df["injury_note"] = df.apply(lambda r: BEST_PRICE.get((r["home_team"], r["away_team"]), {}).get("injury_note", ""), axis=1)

    df["rank_key"] = df["gates_passed"] * 100 + df["ev_b"].fillna(-1) * 10
    df = df.sort_values(["rank_key"], ascending=False)
    df["rank"] = range(1, len(df) + 1)
    cols = ["rank", "kickoff_gmt2", "league", "home_team", "away_team", "selection_cn", "odds", "best_uk_odds",
            "p_b", "p_bayes_same", "p_mkt_fair", "ev_b", "ev_bayes", "edge_vs_market_pp", "model_gap_pp",
            "min_odds_ev1pct", "raw_kelly", "model_direction_agreement", "home_spread_line", "home_spread_dec",
            "gates_passed", "required_score", "score_available", "formal_approved", "formal_stake_cny",
            "status", "reason", "injury_note", "odds_url"]
    out = df[cols]
    # observation ranking across ALL 1X2 directions (H/D/A) priced >= 1.50: conservative EV = min(B EV, Bayes EV)
    obs = []
    for _, r in df.iterrows():
        for k in ("H", "D", "A"):
            o = r[SEL_COL[k]]
            if pd.isna(o) or o < USER_MIN_ODDS:
                continue
            pb, pz, pm = r[f"p_B_{k}"], r[f"p_bayes_{k}"], r[f"fair_mkt_{k}"]
            obs.append({"kickoff_gmt2": r["kickoff_gmt2"], "league": r["league"], "division": r["division"],
                        "home_team": r["home_team"], "away_team": r["away_team"], "selection": k,
                        "selection_cn": SEL_CN[k], "odds": o, "p_b": pb, "p_bayes": pz, "p_mkt_fair": pm,
                        "ev_b": pb * o - 1, "ev_bayes": pz * o - 1, "ev_conservative": min(pb, pz) * o - 1,
                        "model_gap_pp": abs(pb - pz) * 100, "min_odds_both_ev1pct": 1.01 / min(pb, pz),
                        "formal_path": bool(k == "H" and ((o <= CORE_MAX_ODDS + 1e-9) or (r["division"] in {"E0", "SP1"} and EXT_MIN <= o <= EXT_MAX))),
                        "odds_url": r["odds_url"]})
    obs = pd.DataFrame(obs).sort_values("ev_conservative", ascending=False)
    obs.insert(0, "obs_rank", range(1, len(obs) + 1))
    obs.to_csv(OUT / "oct23_oct29_2026_asof1023_conservative_ev_ranking.csv", index=False, encoding="utf-8-sig")
    print(obs.head(15).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    out.to_csv(OUT / "oct23_oct29_2026_asof1023_approval.csv", index=False, encoding="utf-8-sig")

    watch = out[out["status"].eq("条件观察，未批准")]
    price_checks = out[(out["status"] == "拒绝") & (out["ev_b"] > 0.15)].head(8)
    summary = {
        "as_of": AS_OF,
        "bankroll_cny": BANKROLL,
        "open_exposure_cny": OPEN_EXPOSURE,
        "normal_cap_cny": round(BANKROLL * NORMAL_CAP, 2),
        "daily_cap_cny": round(BANKROLL * DAILY_CAP, 2),
        "matches_modelled": int(len(out)),
        "matches_priced": int(out["odds"].notna().sum()),
        "formal_approved_count": 0,
        "formal_stake_cny": 0.0,
        "score_available": False,
        "asian_minus_1_25_available": bool((out["home_spread_line"].astype(str) == "-1.25").any()),
        "conditional_watchlist": watch[["rank", "kickoff_gmt2", "league", "home_team", "away_team", "selection_cn",
                                        "odds", "best_uk_odds", "p_b", "p_bayes_same", "ev_b", "ev_bayes",
                                        "min_odds_ev1pct", "reason"]].to_dict("records"),
        "high_ev_not_authorised": price_checks[["kickoff_gmt2", "league", "home_team", "away_team", "selection_cn",
                                                "odds", "ev_b", "ev_bayes", "reason"]].to_dict("records"),
        "status_counts": out["status"].value_counts().to_dict(),
    }
    (OUT / "oct23_oct29_2026_asof1023_approval_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    pd.set_option("display.width", 250)
    print(out[["rank", "kickoff_gmt2", "league", "home_team", "away_team", "selection_cn", "odds", "p_b",
               "p_bayes_same", "ev_b", "ev_bayes", "model_gap_pp", "gates_passed", "status", "reason"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("conditional_watchlist", "high_ev_not_authorised")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
