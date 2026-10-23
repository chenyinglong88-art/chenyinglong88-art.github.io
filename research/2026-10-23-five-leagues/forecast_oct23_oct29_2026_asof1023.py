#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from download_match_xg import canonical, decode_response, parse_season
from dynamic_poisson_bayes import BayesParams, run_filter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
FROZEN = OUT / "dynamic_bayes_frozen_predictions.csv.gz"
START = pd.Timestamp("2026-10-23")
END = pd.Timestamp("2026-10-29")
AS_OF = pd.Timestamp("2026-10-23")
ALPHA = 0.14
BASE_RATE = 0.012
LEAGUES = {
    "EPL": ("E0", "英超"),
    "Bundesliga": ("D1", "德甲"),
    "Serie_A": ("I1", "意甲"),
    "La_liga": ("SP1", "西甲"),
    "Ligue_1": ("F1", "法甲"),
}
SELECTIONS = ("H", "D", "A")
FIXTURE_OVERRIDES: list[dict] = [
]


def fetch_live(league: str) -> dict:
    url = f"https://understat.com/getLeagueData/{league}/2026"
    headers = {
        "User-Agent": "Mozilla/5.0 research-execution-audit",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://understat.com/league/{league}/2026",
        "Accept": "application/json,text/javascript,*/*;q=0.01",
    }
    response = requests.get(url, headers=headers, timeout=45)
    response.raise_for_status()
    payload = json.loads(decode_response(response.content).decode("utf-8"))
    dest = ROOT / "xg_data" / "raw" / f"{league}_2026_live_asof_2026-10-23.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


def probabilities(lam_home: float, lam_away: float, max_goals: int = 10) -> dict[str, float]:
    ks = np.arange(max_goals + 1)
    ph = np.empty(max_goals + 1)
    pa = np.empty(max_goals + 1)
    ph[0], pa[0] = math.exp(-lam_home), math.exp(-lam_away)
    for k in range(1, max_goals + 1):
        ph[k] = ph[k - 1] * lam_home / k
        pa[k] = pa[k - 1] * lam_away / k
    ph[-1] += max(0.0, 1.0 - ph.sum())
    pa[-1] += max(0.0, 1.0 - pa.sum())
    mat = np.outer(ph, pa)
    hg, ag = ks[:, None], ks[None, :]
    return {
        "H": float(mat[hg > ag].sum()),
        "D": float(mat[hg == ag].sum()),
        "A": float(mat[hg < ag].sum()),
    }


def lookup_from(frame: pd.DataFrame) -> dict[str, str]:
    values = pd.concat([frame["home_team"], frame["away_team"]]).dropna().astype(str).unique()
    return {canonical(value): value for value in values}


def mapped(name: str, lookup: dict[str, str]) -> str:
    return lookup.get(canonical(name), str(name))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    hist = pd.read_csv(FROZEN, low_memory=False)
    hist.columns = [c.lstrip("\ufeff") for c in hist.columns]
    hist["date"] = pd.to_datetime(hist["date"], errors="coerce")
    hist["home_xg"] = pd.to_numeric(hist["obs_home"], errors="coerce")
    hist["away_xg"] = pd.to_numeric(hist["obs_away"], errors="coerce")
    hist["home_npxg"] = hist["home_xg"]
    hist["away_npxg"] = hist["away_xg"]
    hist = hist.dropna(subset=["date", "home_xg", "away_xg"])
    hist = hist[hist["date"] < AS_OF].copy()

    payloads = {league: fetch_live(league) for league in LEAGUES}
    append_rows: list[dict] = []
    fixture_rows: list[dict] = []
    fresh_counts: dict[str, int] = {}

    for league, (division, league_cn) in LEAGUES.items():
        div_hist = hist[hist["division"].eq(division)].copy()
        lookup = lookup_from(div_hist)
        parsed = pd.DataFrame(parse_season(league, 2026, payloads[league]))
        if not parsed.empty:
            parsed["date"] = pd.to_datetime(parsed["date"], errors="coerce")
            parsed = parsed[parsed["date"] < AS_OF].copy()
            parsed["home_team"] = parsed["home_team_xg"].map(lambda value: mapped(value, lookup))
            parsed["away_team"] = parsed["away_team_xg"].map(lambda value: mapped(value, lookup))
            parsed["division"] = division
            existing = {
                (pd.Timestamp(row.date).normalize(), canonical(row.home_team), canonical(row.away_team))
                for row in div_hist.itertuples(index=False)
            }
            added = []
            for row in parsed.itertuples(index=False):
                key = (pd.Timestamp(row.date).normalize(), canonical(row.home_team), canonical(row.away_team))
                if key in existing:
                    continue
                hg = float(row.home_goals_xg)
                ag = float(row.away_goals_xg)
                result = "H" if hg > ag else ("A" if hg < ag else "D")
                added.append({
                    "date": pd.Timestamp(row.date),
                    "division": division,
                    "season": "2627",
                    "match_key": f"{pd.Timestamp(row.date).date()}|{division}|{row.home_team}|{row.away_team}",
                    "home_team": row.home_team,
                    "away_team": row.away_team,
                    "home_goals": hg,
                    "away_goals": ag,
                    "result": result,
                    "AvgH": np.nan,
                    "AvgD": np.nan,
                    "AvgA": np.nan,
                    "AvgCH": np.nan,
                    "AvgCD": np.nan,
                    "AvgCA": np.nan,
                    "home_xg": float(row.home_xg),
                    "away_xg": float(row.away_xg),
                    "home_npxg": float(row.home_npxg) if pd.notna(row.home_npxg) else float(row.home_xg),
                    "away_npxg": float(row.away_npxg) if pd.notna(row.away_npxg) else float(row.away_xg),
                    "obs_home": float(row.home_xg),
                    "obs_away": float(row.away_xg),
                })
            append_rows.extend(added)
            fresh_counts[division] = len(added)
        else:
            fresh_counts[division] = 0

        for match in payloads[league].get("dates", []):
            dt = pd.to_datetime(match.get("datetime"), errors="coerce")
            if pd.isna(dt) or dt.normalize() < START or dt.normalize() > END or bool(match.get("isResult")):
                continue
            fixture_rows.append({
                "date": dt.normalize(),
                "kickoff_utc": dt,
                "understat_id": str(match["id"]),
                "division": division,
                "league": league_cn,
                "home_team": mapped(match["h"]["title"], lookup),
                "away_team": mapped(match["a"]["title"], lookup),
            })

    existing_fixture_keys = {
        (str(row["division"]), canonical(str(row["home_team"])), canonical(str(row["away_team"])))
        for row in fixture_rows
    }
    for override in FIXTURE_OVERRIDES:
        key = (
            str(override["division"]),
            canonical(str(override["home_team"])),
            canonical(str(override["away_team"])),
        )
        if key not in existing_fixture_keys:
            fixture_rows.append(dict(override))
            existing_fixture_keys.add(key)

    if append_rows:
        history = pd.concat([hist, pd.DataFrame(append_rows)], ignore_index=True, sort=False)
    else:
        history = hist.copy()
    history = history.sort_values(["date", "division", "home_team", "away_team"]).reset_index(drop=True)
    fixtures = pd.DataFrame(fixture_rows)
    if fixtures.empty:
        raise RuntimeError("No uncompleted five-league fixtures found in Oct 9-11 horizon")
    fixtures = fixtures.sort_values(["kickoff_utc", "division", "home_team"]).reset_index(drop=True)

    b_rows: list[dict] = []
    for division, league_hist in history.groupby("division", sort=True):
        state: dict[str, dict[str, float]] = {}
        base_h, base_a = 1.45, 1.15
        for _, day in league_hist.groupby("date", sort=True):
            day = day.sort_values(["home_team", "away_team"])
            for row in day.itertuples(index=False):
                state.setdefault(str(row.home_team), {"hs": base_h, "hc": base_a, "as": base_a, "ac": base_h})
                state.setdefault(str(row.away_team), {"hs": base_h, "hc": base_a, "as": base_a, "ac": base_h})
            for row in day.itertuples(index=False):
                home, away = str(row.home_team), str(row.away_team)
                obs_h, obs_a = float(row.home_xg), float(row.away_xg)
                base_h = (1 - BASE_RATE) * base_h + BASE_RATE * obs_h
                base_a = (1 - BASE_RATE) * base_a + BASE_RATE * obs_a
                state[home]["hs"] = (1 - ALPHA) * state[home]["hs"] + ALPHA * obs_h
                state[home]["hc"] = (1 - ALPHA) * state[home]["hc"] + ALPHA * obs_a
                state[away]["as"] = (1 - ALPHA) * state[away]["as"] + ALPHA * obs_a
                state[away]["ac"] = (1 - ALPHA) * state[away]["ac"] + ALPHA * obs_h
        for fixture in fixtures[fixtures["division"].eq(division)].to_dict("records"):
            home, away = fixture["home_team"], fixture["away_team"]
            state.setdefault(home, {"hs": base_h, "hc": base_a, "as": base_a, "ac": base_h})
            state.setdefault(away, {"hs": base_h, "hc": base_a, "as": base_a, "ac": base_h})
            sh, sa = state[home], state[away]
            lam_h = float(np.clip(sh["hs"] * sa["ac"] / max(base_h, 0.30), 0.12, 5.50))
            lam_a = float(np.clip(sa["as"] * sh["hc"] / max(base_a, 0.25), 0.08, 5.00))
            probs = probabilities(lam_h, lam_a)
            record = dict(fixture)
            record.update({
                "b_lambda_home": lam_h,
                "b_lambda_away": lam_a,
                "p_B_H": probs["H"],
                "p_B_D": probs["D"],
                "p_B_A": probs["A"],
            })
            b_rows.append(record)

    b = pd.DataFrame(b_rows)
    future_rows = []
    for row in fixtures.itertuples(index=False):
        future_rows.append({
            "date": AS_OF,
            "division": row.division,
            "season": "2627",
            "match_key": f"{pd.Timestamp(row.date).date()}|{row.division}|{row.home_team}|{row.away_team}",
            "home_team": row.home_team,
            "away_team": row.away_team,
            "home_goals": 0.0,
            "away_goals": 0.0,
            "result": "D",
            "AvgH": np.nan,
            "AvgD": np.nan,
            "AvgA": np.nan,
            "AvgCH": np.nan,
            "AvgCD": np.nan,
            "AvgCA": np.nan,
            "home_xg": 0.0,
            "away_xg": 0.0,
            "home_npxg": 0.0,
            "away_npxg": 0.0,
        })
    bayes_input = pd.concat([history, pd.DataFrame(future_rows)], ignore_index=True, sort=False)
    params = BayesParams(**json.loads((ROOT / "dynamic_bayes_frozen_params.json").read_text(encoding="utf-8")))
    bayes_predictions = run_filter(bayes_input, params, quadrature=True, save_states=False)
    bp = bayes_predictions[bayes_predictions["date"].eq(AS_OF)].copy()
    bp = bp[[
        "division", "home_team", "away_team", "p_bayes_H", "p_bayes_D", "p_bayes_A",
        "sd_bayes_H", "sd_bayes_D", "sd_bayes_A", "lambda_home", "lambda_away",
    ]].rename(columns={"lambda_home": "bayes_lambda_home", "lambda_away": "bayes_lambda_away"})

    out = b.merge(bp, on=["division", "home_team", "away_team"], how="left", validate="one_to_one")
    if out["p_bayes_H"].isna().any():
        raise RuntimeError("Missing Bayesian predictions after merge")
    b_array = out[["p_B_H", "p_B_D", "p_B_A"]].to_numpy(float)
    b_index = b_array.argmax(axis=1)
    out["b_top_selection"] = [SELECTIONS[index] for index in b_index]
    out["b_top_probability"] = b_array[np.arange(len(out)), b_index]
    out["b_min_odds_ev1pct"] = 1.01 / out["b_top_probability"]
    bayes_array = out[["p_bayes_H", "p_bayes_D", "p_bayes_A"]].to_numpy(float)
    bayes_index = bayes_array.argmax(axis=1)
    out["bayes_top_selection"] = [SELECTIONS[index] for index in bayes_index]
    out["bayes_top_probability"] = bayes_array[np.arange(len(out)), bayes_index]
    out["bayes_mean_sd"] = out[["sd_bayes_H", "sd_bayes_D", "sd_bayes_A"]].mean(axis=1)
    out["model_direction_agreement"] = out["b_top_selection"].eq(out["bayes_top_selection"])
    out = out.sort_values(["kickoff_utc", "division", "home_team"])
    output_path = OUT / "oct23_oct29_2026_asof1023_frozen_models.csv"
    out.to_csv(output_path, index=False, encoding="utf-8-sig")
    metadata = {
        "target_start": START.date().isoformat(),
        "target_end": END.date().isoformat(),
        "as_of_date": AS_OF.date().isoformat(),
        "forecast_policy": "All horizon fixtures use states frozen before AS_OF and are predicted in one batch; refresh each matchday before approval",
        "fixture_count": int(len(out)),
        "historical_source": str(FROZEN),
        "understat_fresh_completed_added": fresh_counts,
        "b_model": {"alpha": ALPHA, "base_rate": BASE_RATE, "same_day_policy": "update after date batch"},
        "bayes_params": asdict(params),
        "output": str(output_path),
    }
    (OUT / "oct23_oct29_2026_asof1023_frozen_models_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(out[[
        "date", "kickoff_utc", "league", "home_team", "away_team", "b_top_selection",
        "b_top_probability", "b_min_odds_ev1pct", "bayes_top_selection",
        "bayes_top_probability", "bayes_mean_sd", "model_direction_agreement",
    ]].to_string(index=False))
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
