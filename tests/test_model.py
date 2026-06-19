import json
import math
import unittest
from datetime import date

import pandas as pd

import app


class AssumptionLedgerTests(unittest.TestCase):
    def test_blank_model_has_required_columns(self):
        drivers = app.combine_drivers(
            app.blank_events(),
            app.blank_comp_streams(),
            app.blank_assets(),
            valuation_year=2026,
        )
        self.assertIn("Sensitivity spread ($m)", drivers.columns)
        self.assertIn("Base current ($m)", drivers.columns)

        summary = app.summarize(
            drivers, {"Low": 20.0, "Base": 10.0, "High": 5.0}
        )
        self.assertEqual(summary["Estimated net worth ($m)"].tolist(), [0.0, 0.0, 0.0])
        self.assertTrue(app.top_sensitivity_rows(drivers).empty)

    def test_comp_stream_ignores_future_years(self):
        row = pd.Series(
            {
                "Start year": 2026,
                "End year": 2030,
                "Base annual gross ($m)": 10.0,
                "Base investable %": 50.0,
                "Base CAGR %": 10.0,
            }
        )
        self.assertEqual(app.compound_stream(row, "Base", valuation_year=2026), 5.0)

        future_row = row.copy()
        future_row["Start year"] = 2027
        self.assertEqual(
            app.compound_stream(future_row, "Base", valuation_year=2026), 0.0
        )

    def test_download_json_is_strict_and_reproducible(self):
        events = app.default_events()
        events.loc[0, "Notes"] = math.nan
        drivers = app.combine_drivers(
            events,
            app.default_comp_streams(),
            app.default_assets(),
            valuation_year=2026,
        )
        summary = app.summarize(
            drivers, {"Low": 20.0, "Base": 10.0, "High": 5.0}
        )

        exported = app.dataframe_for_download(
            summary,
            drivers,
            events,
            app.default_comp_streams(),
            app.default_assets(),
            app.default_sources(),
            valuation_date=date(2026, 6, 18),
            threshold=1000.0,
            haircuts={"Low": 20.0, "Base": 10.0, "High": 5.0},
        )
        payload = json.loads(exported)

        self.assertEqual(payload["metadata"]["valuation_date"], "2026-06-18")
        self.assertEqual(payload["metadata"]["threshold_m"], 1000.0)
        self.assertIsNone(payload["events"][0]["Notes"])
        self.assertNotIn("NaN", exported)

    def test_sensitivity_sorting_uses_spread(self):
        drivers = pd.DataFrame(
            [
                {
                    "Driver": "Huge base",
                    "Type": "Liquidity event",
                    "Low current ($m)": 990.0,
                    "Base current ($m)": 1000.0,
                    "High current ($m)": 1010.0,
                    "Confidence": "Confirmed",
                    "Source ID": "S1",
                    "Notes": "",
                },
                {
                    "Driver": "Small base, high spread",
                    "Type": "Liquidity event",
                    "Low current ($m)": 0.0,
                    "Base current ($m)": 1.0,
                    "High current ($m)": 500.0,
                    "Confidence": "Speculative",
                    "Source ID": "S2",
                    "Notes": "",
                },
            ]
        )
        drivers["Confidence score"] = drivers["Confidence"].map(app.confidence_score)
        drivers["Sensitivity spread ($m)"] = (
            drivers["High current ($m)"] - drivers["Low current ($m)"]
        )

        top = app.top_sensitivity_rows(drivers, limit=1)
        self.assertEqual(top.iloc[0]["Driver"], "Small base, high spread")


if __name__ == "__main__":
    unittest.main()
