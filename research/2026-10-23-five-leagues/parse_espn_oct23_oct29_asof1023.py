#!/usr/bin/env python3
"""Parse ESPN/DraftKings scoreboard odds for Oct 23-29 2026 and join to frozen B/Bayes models."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "xg_data" / "raw" / "espn_oct2026_asof1023"
OUT = ROOT / "output"
MODELS = OUT / "oct23_oct29_2026_asof1023_frozen_models.csv"
LEAGUES = {"eng.1": "英超", "esp.1": "西甲", "ger.1": "德甲", "ita.1": "意甲", "fra.1": "法甲"}
ALIASES = {
    "manchesterunited": "manunited", "manchestercity": "mancity", "nottinghamforest": "nottmforest",
    "afcbournemouth": "bournemouth", "brightonhovealbion": "brighton", "ipswichtown": "ipswich",
    "tottenhamhotspur": "tottenham", "leedsunited": "leeds", "hullcity": "hull", "coventrycity": "coventry",
    "newcastleunited": "newcastle", "atleticomadrid": "athmadrid", "athleticclub": "athleticclub",
    "rayovallecano": "vallecano", "realsociedad": "sociedad", "deportivolacoruna": "lacoruna",
    "deportivo": "lacoruna", "realbetis": "betis", "racingsantander": "racingsantander",
    "bayernmunich": "bayernmunich", "borussiadortmund": "dortmund", "werderbremen": "werderbremen",
    "bayerleverkusen": "leverkusen", "vfbstuttgart": "vfbstuttgart", "stuttgart": "vfbstuttgart",
    "rbleipzig": "rbleipzig", "eintrachtfrankfurt": "einfrankfurt", "fckoln": "fckoln", "koln": "fckoln",
    "borussiamonchengladbach": "borussiamgladbach", "borussiamgladbach": "borussiamgladbach",
    "sc freiburg": "freiburg", "scfreiburg": "freiburg", "tsghoffenheim": "hoffenheim",
    "hamburgsv": "hamburgersv", "hamburgersv": "hamburgersv", "1fcunionberlin": "unionberlin",
    "svelversberg": "elversberg", "fsvmainz05": "mainz05", "mainz": "mainz05", "scpaderborn07": "paderborn",
    "acmilan": "milan", "internazionale": "inter", "intermilan": "inter", "parma": "parmacalcio1913",
    "parmacalcio": "parmacalcio1913", "parisstgermain": "parissg", "parissaintgermain": "parissg",
    "olympiquelyonnais": "lyon", "olympiquedemarseille": "marseille", "lehavreac": "lehavre",
    "stadebrestois29": "brest", "staderennais": "rennes", "ogcnice": "nice", "rcstrasbourg": "strasbourg",
    "rcstrasbourgalsace": "strasbourg", "lillecsc": "lille", "lille": "lille", "asmonaco": "monaco",
    "fclorient": "lorient", "estactroyesac": "troyes", "estac": "troyes", "lemansfc": "lemans",
    "ajauxerre": "auxerre", "angerssco": "angers", "rclens": "lens", "toulousefc": "toulouse",
    "celtavigo": "celtavigo", "levanteud": "levante", "malagacf": "malaga", "espanyol": "espanyol",
    "valenciacf": "valencia", "villarrealcf": "villarreal", "getafecf": "getafe", "cadosasuna": "osasuna",
    "sevillafc": "sevilla", "deportivoalaves": "alaves", "elchecf": "elche", "fcbarcelona": "barcelona",
    "atalantabc": "atalanta", "veneziafc": "venezia", "ascoma": "roma", "asroma": "roma", "ssclazio": "lazio",
    "acmonza": "monza", "uslecce": "lecce", "bolognafc1909": "bologna", "ussassuolo": "sassuolo",
    "cagliaricalcio": "cagliari", "juventusfc": "juventus", "genoacfc": "genoa", "acffiorentina": "fiorentina",
    "sscnapoli": "napoli", "frosinonecalcio": "frosinone", "torinofc": "torino", "udinesecalcio": "udinese",
    "comoc1907": "como", "como1907": "como",
    "fcaugsburg": "augsburg", "fccologne": "fckoln", "1fckoln": "fckoln",
}


def key(name: str) -> str:
    text = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9]", "", text)
    return ALIASES.get(text, text)


def american_to_decimal(value) -> float | None:
    if value in (None, "", "OFF", "EVEN"):
        return 2.0 if value == "EVEN" else None
    try:
        number = float(str(value).replace("+", ""))
    except ValueError:
        return None
    if number > 0:
        return 1 + number / 100
    return 1 + 100 / abs(number)


def main() -> None:
    rows = []
    for path in sorted(RAW.glob("*.json")):
        code = path.name.split("_")[0]
        data = json.loads(path.read_text(encoding="utf-8"))
        for event in data.get("events", []):
            comp = event["competitions"][0]
            teams = {c["homeAway"]: c["team"]["displayName"] for c in comp["competitors"]}
            odds = (comp.get("odds") or [{}])[0] or {}
            ml = odds.get("moneyline") or {}
            def side(name: str, stage: str):
                return ((ml.get(name) or {}).get(stage) or {}).get("odds")
            spread = odds.get("pointSpread") or {}
            total = odds.get("total") or {}
            status = (event.get("status") or {}).get("type", {})
            rows.append({
                "espn_id": event["id"],
                "espn_league": code,
                "league": LEAGUES[code],
                "kickoff_utc": pd.Timestamp(event["date"]).tz_convert(None),
                "kickoff_gmt2": (pd.Timestamp(event["date"]).tz_convert("Europe/Paris")).strftime("%Y-%m-%d %H:%M"),
                "home_espn": teams.get("home"),
                "away_espn": teams.get("away"),
                "status": status.get("name"),
                "provider": (odds.get("provider") or {}).get("name"),
                "home_open_us": side("home", "open"), "draw_open_us": side("draw", "open"), "away_open_us": side("away", "open"),
                "home_us": side("home", "close"), "draw_us": side("draw", "close"), "away_us": side("away", "close"),
                "home_spread_line": ((spread.get("home") or {}).get("close") or {}).get("line"),
                "home_spread_us": ((spread.get("home") or {}).get("close") or {}).get("odds"),
                "away_spread_line": ((spread.get("away") or {}).get("close") or {}).get("line"),
                "away_spread_us": ((spread.get("away") or {}).get("close") or {}).get("odds"),
                "total_line": odds.get("overUnder"),
                "over_us": ((total.get("over") or {}).get("close") or {}).get("odds"),
                "under_us": ((total.get("under") or {}).get("close") or {}).get("odds"),
                "odds_url": f"https://www.espn.com/soccer/match/_/gameId/{event['id']}",
            })
    lines = pd.DataFrame(rows).drop_duplicates("espn_id")
    for col in ("home", "draw", "away", "home_open", "draw_open", "away_open", "home_spread", "away_spread", "over", "under"):
        lines[f"{col}_dec"] = lines[f"{col}_us"].map(american_to_decimal)
    implied = 1 / lines[["home_dec", "draw_dec", "away_dec"]]
    lines["overround"] = implied.sum(axis=1)
    for s, c in (("H", "home_dec"), ("D", "draw_dec"), ("A", "away_dec")):
        lines[f"fair_mkt_{s}"] = (1 / lines[c]) / lines["overround"]
    lines["hk"] = lines["home_espn"].map(key)
    lines["ak"] = lines["away_espn"].map(key)

    models = pd.read_csv(MODELS)
    models["hk"] = models["home_team"].map(key)
    models["ak"] = models["away_team"].map(key)
    merged = models.merge(lines, on=["league", "hk", "ak"], how="outer", indicator=True, suffixes=("_understat", ""))
    unmatched = merged[merged["_merge"] != "both"][["league", "home_team", "away_team", "home_espn", "away_espn", "_merge"]]
    merged = merged[merged["_merge"] == "both"].drop(columns=["_merge"])
    merged.to_csv(OUT / "oct23_oct29_2026_asof1023_models_with_lines.csv", index=False, encoding="utf-8-sig")
    lines.to_csv(OUT / "oct23_oct29_2026_asof1023_espn_lines.csv", index=False, encoding="utf-8-sig")
    print("lines", len(lines), "models", len(models), "matched", len(merged))
    if not unmatched.empty:
        print("UNMATCHED")
        print(unmatched.to_string(index=False))
    show = merged[["kickoff_gmt2", "league", "home_team", "away_team", "home_dec", "draw_dec", "away_dec",
                   "p_B_H", "p_B_D", "p_B_A", "p_bayes_H", "p_bayes_A", "home_spread_line", "home_spread_dec"]]
    print(show.sort_values("kickoff_gmt2").to_string(index=False, float_format=lambda x: f"{x:.3f}"))


if __name__ == "__main__":
    main()
