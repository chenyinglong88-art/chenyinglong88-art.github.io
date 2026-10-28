#!/usr/bin/env python3
"""Risk-adjusted observation ranking for five-league fixtures 2026-10-29..11-02 (as of 2026-10-28 23:05 CET).

Transparent observation score (0-100), NOT historically validated and NOT the user's v3.6 score.
It never creates formal approval: formal stake stays 0 CNY unless the locked B-model rules pass AND
a reproducible 84 (EPL 88) score exists. No such scorer exists.

Base score (DraftKings price from ESPN, same source for every match) - unchanged from the Oct 23 version:
- B model edge          30 * clip(EV_B / 0.20, 0, 1)
- Bayes agreement       25 * clip(1 + EV_Bayes / 0.20, 0, 1)
- Market support        15 * clip((p_mkt_fair - 1/3) / (0.72 - 1/3), 0, 1)
- Model consistency     15 * clip(1 - |pB - pBayes| / 25pp, 0, 1)
- Price band            15 if 1.50-2.00, 10 if 2.00-2.50, 5 if 2.50-3.00, else 0
Fixed research adjustments (written before kickoff; only the 5 matches researched get them):
- home side >=4 confirmed absentees -6; 2-3 -2; away side >=4 confirmed absentees +3 (doubts not counted)
- home side played a European OR cup match within 3 days before kickoff -3; away side did +2
  (Oct 23 rule covered European matches only; extended to cups this week before any of these matches started,
   because three of the five candidates played League Cup / DFB-Pokal / Copa del Rey midweek)
- home side <=1 win in last five competitive matches -5
- home price lengthened >=0.05 from DraftKings open -3
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
APPROVAL = OUT / "oct29_nov02_2026_asof1029_approval.csv"
MODELS = OUT / "oct29_nov02_2026_asof1029_models_with_lines.csv"
OUT_CSV = OUT / "oct29_nov02_2026_asof1029_risk_ranking.csv"
OUT_JSON = OUT / "oct29_nov02_2026_asof1029_risk_ranking_summary.json"

# research (workflow 5343af6a2337, 2026-10-28 ~22:00-23:00 CET); see output/oct29_2026_external_notes.md
RESEARCH = {
    ("Leverkusen", "VfB Stuttgart"): dict(
        best=1.85, best_src="1xBet/888Starz 1.85（SportyTrader）；BetMGM/Fanatics 1.80；DK 1.769；bet365 1.746–1.75；FanDuel 1.69",
        home_out=5, away_out=2, home_midweek_3d=True, away_midweek_3d=True, home_wins_last5=4,
        notes="勒沃库森周三德国杯5–2胜纽伦堡；缺Diaby、Kofane、Terrier、Ben Seghir、Doué（进攻线大面积缺阵），Eichhorn、Culbreath存疑；"
              "上轮联赛0–3负霍芬海姆；第4（13分）。斯图加特周三杯赛1–0胜帕德博恩，缺Vagnoman、Nartey，Zagadou、Diehl、Tiago Tomás存疑；"
              "第15（6分），下周二客战加拉塔萨雷"),
    ("Bournemouth", "Leeds"): dict(
        best=2.15, best_src="DK/BetMGM 2.15（Oddschecker US）；英国最佳23/20=2.15；FanDuel/Fanatics 2.10；bet365 2.05",
        home_out=3, away_out=1, home_midweek_3d=True, away_midweek_3d=False, home_wins_last5=5,
        notes="伯恩茅斯5连胜（含周三联赛杯3–0胜维拉、欧联3–0胜米兰），但10月第7场、休息3天；缺Scott、Araujo、Toth；"
              "利兹第7（11分）近期多平局，缺Joseph，Rodon、James、Elvedi存疑，无周中比赛"),
    ("Hull", "Ipswich"): dict(
        best=2.65, best_src="DK 2.65；Caesars 2.63；FanDuel/BetRivers/Fanatics 2.60；bet365 2.58；BetMGM 2.55",
        home_out=4, away_out=0, home_midweek_3d=False, away_midweek_3d=False, home_wins_last5=0,
        notes="赫尔近5场0胜（3平2负）；缺Gyabi、Hughes、Cho、Gourna-Douath，Butland、Mendy存疑；伊普斯维奇仅Lukić存疑；两队同为10分"),
    ("Athletic Club", "Sociedad"): dict(
        best=2.16, best_src="Pinnacle 2.16；FanDuel 2.15；DK/BetMGM/Fanatics 2.10；bet365 2.05",
        home_out=3, away_out=2, home_midweek_3d=True, away_midweek_3d=False, home_wins_last5=1,
        notes="毕尔巴鄂周四国王杯客战AE Prat（距德比约3天）；缺Ruiz de Galarreta、Guruzeta、Egiluz，Sancet存疑；近5场1胜；"
              "皇家社会联赛4连胜、第5（19分），缺Beitia、Odriozola；DK主胜由1.952漂至2.10"),
    ("Man City", "Brighton"): dict(
        best=1.69, best_src="BetMGM/Fanatics 1.69；DK/BetRivers 1.667；bet365 1.649；FanDuel 1.61–1.625",
        home_out=1, away_out=5, home_midweek_3d=True, away_midweek_3d=True, home_wins_last5=2,
        notes="两队周三联赛杯刚踢过2–2（曼城点球晋级）；曼城第1（21分），缺Semenyo，Nunes存疑，下周三客战莱比锡；"
              "布莱顿第3（16分，净胜+16），缺三笘薰、Azeez、Struijk、Ferguson、Tzimas"),
}


def clip01(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))


def price_points(o: float) -> float:
    if o < 1.50:
        return 0.0
    if o <= 2.00:
        return 15.0
    if o <= 2.50:
        return 10.0
    if o <= 3.00:
        return 5.0
    return 0.0


def beijing(ts) -> str:
    return pd.Timestamp(ts).tz_localize("UTC").tz_convert("Asia/Shanghai").strftime("%m-%d %H:%M")


def local_eu(ts) -> str:
    return pd.Timestamp(ts).tz_localize("UTC").tz_convert("Europe/Paris").strftime("%m-%d %H:%M")


def main() -> None:
    a = pd.read_csv(APPROVAL)
    m = pd.read_csv(MODELS)
    m.columns = [c.lstrip("\ufeff") for c in m.columns]
    cand = a[(a["selection_cn"] == "主胜") & (a["odds"] >= 1.50)].copy()
    rows = []
    for _, r in cand.iterrows():
        mm = m[(m.home_team == r.home_team) & (m.away_team == r.away_team)].iloc[0]
        res = RESEARCH.get((r.home_team, r.away_team))
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
        adj: dict[str, int] = {}
        opened = float(mm.home_open_dec) if pd.notna(mm.home_open_dec) else o
        if res:
            if res["home_out"] >= 4:
                adj["主队确认缺阵≥4人"] = -6
            elif res["home_out"] >= 2:
                adj["主队确认缺阵2–3人"] = -2
            if res["away_out"] >= 4:
                adj["客队确认缺阵≥4人"] = +3
            if res["home_midweek_3d"]:
                adj["主队3天内踢杯赛/欧战"] = -3
            if res["away_midweek_3d"]:
                adj["客队3天内踢杯赛/欧战"] = +2
            if res["home_wins_last5"] <= 1:
                adj["主队近5场≤1胜"] = -5
            if o - opened >= 0.05 - 1e-9:
                adj[f"主胜由{opened:.3f}漂至{o:.3f}"] = -3
        total = base + sum(adj.values())
        best = res["best"] if res else np.nan
        rows.append({
            "kickoff_beijing": beijing(mm.kickoff_utc), "kickoff_cet": local_eu(mm.kickoff_utc),
            "league": r.league, "match": f"{r.home_team} vs {r.away_team}", "selection": "主胜",
            "dk_odds": round(o, 3), "dk_open": round(opened, 3), "best_odds": best,
            "best_src": res["best_src"] if res else "未逐场核验",
            "p_b": round(r.p_b, 4), "p_bayes": round(r.p_bayes_same, 4), "p_mkt_fair": round(r.p_mkt_fair, 4),
            "ev_b": round(ev_b, 4), "ev_bayes": round(ev_z, 4),
            "ev_b_best": round(r.p_b * best - 1, 4) if res else np.nan,
            "ev_bayes_best": round(r.p_bayes_same * best - 1, 4) if res else np.nan,
            "model_gap_pp": round(gap, 2), "edge_vs_market_pp": round((r.p_b - r.p_mkt_fair) * 100, 2),
            "b_min_odds_ev1": round(1.01 / r.p_b, 3), "both_min_odds_ev1": round(1.01 / min(r.p_b, r.p_bayes_same), 3),
            **{k: round(v, 2) for k, v in comp.items()}, "base_score": round(base, 2),
            "researched": bool(res), "adjustments": "；".join(f"{k}{v:+d}" for k, v in adj.items()),
            "adjust_total": sum(adj.values()), "risk_score": round(total, 2),
            "reaches_84": bool(res and total >= 84), "required_score": 88 if mm.division == "E0" else 84,
            "formal_gate_reason": r.reason, "formal_stake_cny": 0,
            "notes": res["notes"] if res else "", "odds_url": r.odds_url,
        })
    out = pd.DataFrame(rows)
    out["sort_key"] = np.where(out["researched"], out["risk_score"], out["base_score"] - 1000)
    out = out.sort_values("sort_key", ascending=False).drop(columns="sort_key").reset_index(drop=True)
    out.insert(0, "risk_rank", np.where(out["researched"], np.arange(1, len(out) + 1), 0))
    out.loc[~out["researched"], "risk_rank"] = 0
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    top = out[out["researched"]]
    summary = {
        "as_of": "2026-10-28 23:05 CET (Beijing 2026-10-29 06:05)",
        "fixtures_modelled": int(len(a)), "fixtures_priced": int(a.odds.notna().sum()),
        "home_candidates_ge_1_50": int(len(out)), "researched": int(len(top)),
        "conditional_watch_formal_gates": 0, "formal_approved": 0, "formal_stake_cny": 0,
        "max_risk_score": float(top["risk_score"].max()), "any_reaches_84": bool(top["reaches_84"].any()),
        "top": top[["risk_rank", "kickoff_beijing", "league", "match", "dk_odds", "best_odds", "ev_b", "ev_bayes",
                    "ev_b_best", "ev_bayes_best", "base_score", "adjust_total", "risk_score", "formal_gate_reason"]]
        .to_dict("records"),
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    pd.set_option("display.width", 280)
    print(top[["risk_rank", "kickoff_beijing", "league", "match", "dk_odds", "dk_open", "best_odds", "p_b", "p_bayes",
               "p_mkt_fair", "ev_b", "ev_bayes", "ev_b_best", "ev_bayes_best", "model_gap_pp", "base_score",
               "adjust_total", "risk_score"]].to_string(index=False))
    for _, r in top.iterrows():
        print(r.risk_rank, r.match, "|", r.adjustments, "|", r.formal_gate_reason)
    print(out[~out.researched][["league", "match", "dk_odds", "ev_b", "ev_bayes", "base_score"]].head(6).to_string(index=False))


if __name__ == "__main__":
    main()
