from __future__ import annotations

import json
from datetime import date
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


SCENARIOS = ("Low", "Base", "High")
CONFIDENCE_SCORES = {
    "Confirmed": 1.0,
    "Public indirect": 0.7,
    "Analyst assumption": 0.45,
    "Speculative": 0.2,
}


def default_events() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Event": "Crescendo",
                "Date": "1993-09-21",
                "Deal value ($m)": 94.5,
                "Low ownership %": 3.0,
                "Base ownership %": 6.0,
                "High ownership %": 10.0,
                "Low keep %": 40.0,
                "Base keep %": 50.0,
                "High keep %": 60.0,
                "Low return multiple": 29.4,
                "Base return multiple": 49.6,
                "High return multiple": 85.3,
                "Confidence": "Analyst assumption",
                "Source ID": "S1/S2",
                "Notes": "Founder/VP engineering allocation estimate.",
            },
            {
                "Event": "Andiamo",
                "Date": "2004-02-20",
                "Deal value ($m)": 750.0,
                "Low ownership %": 2.0,
                "Base ownership %": 4.0,
                "High ownership %": 7.0,
                "Low keep %": 40.0,
                "Base keep %": 50.0,
                "High keep %": 60.0,
                "Low return multiple": 9.8,
                "Base return multiple": 13.6,
                "High return multiple": 13.1,
                "Confidence": "Public indirect",
                "Source ID": "S3/S4",
                "Notes": "Spin-in proceeds estimated from public deal value.",
            },
            {
                "Event": "Nuova",
                "Date": "2008-05-22",
                "Deal value ($m)": 678.0,
                "Low ownership %": 2.0,
                "Base ownership %": 4.0,
                "High ownership %": 7.0,
                "Low keep %": 40.0,
                "Base keep %": 50.0,
                "High keep %": 60.0,
                "Low return multiple": 7.5,
                "Base return multiple": 10.5,
                "High return multiple": 14.1,
                "Confidence": "Public indirect",
                "Source ID": "S5",
                "Notes": "Maximum success-based payout used as deal value.",
            },
            {
                "Event": "Insieme",
                "Date": "2013-11-06",
                "Deal value ($m)": 863.0,
                "Low ownership %": 2.0,
                "Base ownership %": 4.0,
                "High ownership %": 7.0,
                "Low keep %": 40.0,
                "Base keep %": 50.0,
                "High keep %": 60.0,
                "Low return multiple": 5.2,
                "Base return multiple": 7.1,
                "High return multiple": 7.8,
                "Confidence": "Public indirect",
                "Source ID": "S6/S7",
                "Notes": "Maximum potential payout used as deal value.",
            },
            {
                "Event": "Pensando",
                "Date": "2022-05-26",
                "Deal value ($m)": 1655.0,
                "Low ownership %": 2.0,
                "Base ownership %": 4.0,
                "High ownership %": 7.0,
                "Low keep %": 40.0,
                "Base keep %": 50.0,
                "High keep %": 60.0,
                "Low return multiple": 2.0,
                "Base return multiple": 2.8,
                "High return multiple": 3.9,
                "Confidence": "Public indirect",
                "Source ID": "S8/S9",
                "Notes": "Uses recorded consideration net of deferred comp.",
            },
        ]
    )


def default_comp_streams() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Stream": "Cisco senior technical leadership comp/equity",
                "Start year": 1994,
                "End year": 2016,
                "Low annual gross ($m)": 1.0,
                "Base annual gross ($m)": 2.5,
                "High annual gross ($m)": 5.0,
                "Low investable %": 30.0,
                "Base investable %": 40.0,
                "High investable %": 50.0,
                "Low CAGR %": 8.1,
                "Base CAGR %": 10.3,
                "High CAGR %": 12.8,
                "Confidence": "Analyst assumption",
                "Source ID": "S10",
                "Notes": "Ongoing cash/equity comp saved and invested.",
            },
            {
                "Stream": "AMD/Pensando retention and acquisition-related comp",
                "Start year": 2023,
                "End year": 2023,
                "Low annual gross ($m)": 5.0,
                "Base annual gross ($m)": 20.0,
                "High annual gross ($m)": 60.0,
                "Low investable %": 40.0,
                "Base investable %": 50.0,
                "High investable %": 55.0,
                "Low CAGR %": 20.2,
                "Base CAGR %": 34.2,
                "High CAGR %": 34.2,
                "Confidence": "Public indirect",
                "Source ID": "S9",
                "Notes": "Retention pool exists, individual allocation unknown.",
            },
        ]
    )


def default_assets() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Item": "Board/advisory/private-investment current value",
                "Low value ($m)": 0.0,
                "Base value ($m)": 5.0,
                "High value ($m)": 25.0,
                "Confidence": "Analyst assumption",
                "Source ID": "S10",
                "Notes": "Enter negative rows here for liabilities.",
            }
        ]
    )


def default_sources() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Source ID": "S1",
                "Source": "Cisco acquisition list",
                "URL": "https://www.cisco.com/site/us/en/about/corporate-development/acquisitions/acquisitions-list-years/index.html",
                "Claim": "Crescendo agreement date.",
                "Confidence": "Confirmed",
            },
            {
                "Source ID": "S2",
                "Source": "Business Insider",
                "URL": "https://www.businessinsider.com/why-cisco-showered-three-men-with-billions-2014-9",
                "Claim": "Cisco spin-in deal values and caveat that direct personal payouts are not public.",
                "Confidence": "Public indirect",
            },
            {
                "Source ID": "S3",
                "Source": "Cisco Andiamo completion",
                "URL": "https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2004/m02/cisco-systems-completes-acquisition-of-andiamo-systems-inc.html",
                "Claim": "Andiamo purchase price.",
                "Confidence": "Confirmed",
            },
            {
                "Source ID": "S4",
                "Source": "Business Insider",
                "URL": "https://www.businessinsider.com/why-cisco-showered-three-men-with-billions-2014-9",
                "Claim": "Mazzola 2004 option cashout anchor.",
                "Confidence": "Public indirect",
            },
            {
                "Source ID": "S5",
                "Source": "Cisco Nuova completion",
                "URL": "https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2008/m05/cisco-completes-acquisition-of-nuova-systems.html",
                "Claim": "Nuova maximum success-based payout.",
                "Confidence": "Confirmed",
            },
            {
                "Source ID": "S6",
                "Source": "Cisco ACI/Insieme announcement",
                "URL": "https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2013/m11/cisco-pioneers-real-time-application-delivery-in-global-data-centers-and-clouds-to-enable-greater-business-agility.html",
                "Claim": "Insieme maximum potential payout.",
                "Confidence": "Confirmed",
            },
            {
                "Source ID": "S7",
                "Source": "Cisco Insieme completion",
                "URL": "https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2013/m12/cisco-completes-acquisition-of-insieme-networks.html",
                "Claim": "Insieme completion date.",
                "Confidence": "Confirmed",
            },
            {
                "Source ID": "S8",
                "Source": "AMD Pensando completion",
                "URL": "https://ir.amd.com/news-events/press-releases/detail/1071/amd-expands-data-center-solutions-capabilities-with-acquisition-of-pensando",
                "Claim": "Pensando transaction value and completion date.",
                "Confidence": "Confirmed",
            },
            {
                "Source ID": "S9",
                "Source": "AMD 2024 10-K",
                "URL": "https://www.sec.gov/Archives/edgar/data/2488/000000248825000012/amd-20241228.htm",
                "Claim": "Recorded Pensando consideration and acquisition-related compensation context.",
                "Confidence": "Confirmed",
            },
            {
                "Source ID": "S10",
                "Source": "Skorpios director bio",
                "URL": "https://www.skorpiosinc.com/about-us/board-of-directors/",
                "Claim": "Career summary and director role.",
                "Confidence": "Public indirect",
            },
        ]
    )


def blank_events() -> pd.DataFrame:
    template = default_events().iloc[:0].copy()
    return template


def blank_comp_streams() -> pd.DataFrame:
    template = default_comp_streams().iloc[:0].copy()
    return template


def blank_assets() -> pd.DataFrame:
    return default_assets().iloc[:0].copy()


def blank_sources() -> pd.DataFrame:
    return default_sources().iloc[:0].copy()


def safe_number(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def confidence_score(value: Any) -> float:
    return CONFIDENCE_SCORES.get(str(value), 0.35)


def money(value: float) -> str:
    sign = "-" if value < 0 else ""
    absolute = abs(value)
    if absolute >= 1000:
        return f"{sign}${absolute / 1000:,.2f}B"
    return f"{sign}${absolute:,.1f}M"


def range_amount(low: float, high: float) -> str:
    return f"{low / 1000:,.2f}-{high / 1000:,.2f}B"


def pct(value: float) -> str:
    return f"{value:.1f}%"


def event_model(events: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in events.iterrows():
        output = {
            "Driver": str(row.get("Event", "")),
            "Type": "Liquidity event",
            "Source ID": row.get("Source ID", ""),
            "Confidence": row.get("Confidence", "Analyst assumption"),
            "Notes": row.get("Notes", ""),
        }
        deal_value = safe_number(row.get("Deal value ($m)"))
        for scenario in SCENARIOS:
            ownership = safe_number(row.get(f"{scenario} ownership %")) / 100
            keep = safe_number(row.get(f"{scenario} keep %")) / 100
            multiple = safe_number(row.get(f"{scenario} return multiple"), 1)
            gross = deal_value * ownership
            current = gross * keep * multiple
            output[f"{scenario} gross ($m)"] = gross
            output[f"{scenario} current ($m)"] = current
        rows.append(output)
    return pd.DataFrame(rows)


def compound_stream(row: pd.Series, scenario: str, valuation_year: int) -> float:
    start_year = int(safe_number(row.get("Start year"), valuation_year))
    end_year = int(safe_number(row.get("End year"), start_year))
    if end_year < start_year:
        return 0.0

    annual_gross = safe_number(row.get(f"{scenario} annual gross ($m)"))
    investable = safe_number(row.get(f"{scenario} investable %")) / 100
    cagr = safe_number(row.get(f"{scenario} CAGR %")) / 100

    total = 0.0
    for year in range(start_year, end_year + 1):
        years_compounded = max(0, valuation_year - year)
        total += annual_gross * investable * ((1 + cagr) ** years_compounded)
    return total


def comp_model(comp_streams: pd.DataFrame, valuation_year: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in comp_streams.iterrows():
        output = {
            "Driver": str(row.get("Stream", "")),
            "Type": "Comp stream",
            "Source ID": row.get("Source ID", ""),
            "Confidence": row.get("Confidence", "Analyst assumption"),
            "Notes": row.get("Notes", ""),
        }
        for scenario in SCENARIOS:
            output[f"{scenario} current ($m)"] = compound_stream(
                row, scenario, valuation_year
            )
        rows.append(output)
    return pd.DataFrame(rows)


def asset_model(assets: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in assets.iterrows():
        output = {
            "Driver": str(row.get("Item", "")),
            "Type": "Current asset / liability",
            "Source ID": row.get("Source ID", ""),
            "Confidence": row.get("Confidence", "Analyst assumption"),
            "Notes": row.get("Notes", ""),
        }
        for scenario in SCENARIOS:
            output[f"{scenario} current ($m)"] = safe_number(
                row.get(f"{scenario} value ($m)")
            )
        rows.append(output)
    return pd.DataFrame(rows)


def combine_drivers(
    events: pd.DataFrame, comp_streams: pd.DataFrame, assets: pd.DataFrame, valuation_year: int
) -> pd.DataFrame:
    frames = [
        event_model(events),
        comp_model(comp_streams, valuation_year),
        asset_model(assets),
    ]
    non_empty = [frame for frame in frames if not frame.empty]
    if not non_empty:
        return pd.DataFrame(
            columns=[
                "Driver",
                "Type",
                "Source ID",
                "Confidence",
                "Notes",
                "Low current ($m)",
                "Base current ($m)",
                "High current ($m)",
            ]
        )
    result = pd.concat(non_empty, ignore_index=True)
    result["Confidence score"] = result["Confidence"].map(confidence_score)
    result["Sensitivity spread ($m)"] = (
        result["High current ($m)"] - result["Low current ($m)"]
    )
    return result


def summarize(drivers: pd.DataFrame, haircuts: dict[str, float]) -> pd.DataFrame:
    rows = []
    for scenario in SCENARIOS:
        gross = safe_number(drivers.get(f"{scenario} current ($m)", pd.Series()).sum())
        haircut = haircuts[scenario] / 100
        net = gross * (1 - haircut)
        rows.append(
            {
                "Scenario": scenario,
                "Gross wealth ($m)": gross,
                "Global haircut %": haircuts[scenario],
                "Estimated net worth ($m)": net,
            }
        )
    return pd.DataFrame(rows)


def source_quality(drivers: pd.DataFrame) -> pd.DataFrame:
    if drivers.empty:
        return pd.DataFrame(columns=["Confidence", "Base current ($m)", "Share"])
    grouped = (
        drivers.groupby("Confidence", dropna=False)["Base current ($m)"]
        .sum()
        .reset_index()
    )
    total = grouped["Base current ($m)"].abs().sum()
    grouped["Share"] = grouped["Base current ($m)"].abs() / total if total else 0
    grouped["Score"] = grouped["Confidence"].map(confidence_score)
    return grouped.sort_values("Score", ascending=False)


def threshold_analysis(
    summary: pd.DataFrame, drivers: pd.DataFrame, threshold: float, base_haircut: float
) -> dict[str, float | str]:
    base_net = safe_number(
        summary.loc[summary["Scenario"] == "Base", "Estimated net worth ($m)"].iloc[0]
    )
    base_gross = safe_number(
        summary.loc[summary["Scenario"] == "Base", "Gross wealth ($m)"].iloc[0]
    )
    event_base = safe_number(
        drivers.loc[
            drivers["Type"] == "Liquidity event", "Base current ($m)"
        ].sum()
    )
    non_event_base = base_gross - event_base
    required_gross = threshold / max(0.0001, 1 - base_haircut / 100)
    needed_event_value = max(0, required_gross - non_event_base)
    event_scaler = needed_event_value / event_base if event_base else float("inf")

    if base_net <= 0:
        lift = float("inf")
    else:
        lift = threshold / base_net - 1

    if base_gross >= threshold:
        max_haircut = 100 * (1 - threshold / base_gross)
        haircut_text = f"{max_haircut:.1f}%"
    else:
        haircut_text = "Not enough gross wealth"

    return {
        "Base estimate": base_net,
        "Gap": threshold - base_net,
        "Required lift": lift,
        "Event scaler": event_scaler,
        "Max haircut": haircut_text,
    }


def dataframe_for_download(
    summary: pd.DataFrame,
    drivers: pd.DataFrame,
    events: pd.DataFrame,
    comp_streams: pd.DataFrame,
    assets: pd.DataFrame,
    sources: pd.DataFrame,
) -> str:
    payload = {
        "summary": summary.to_dict(orient="records"),
        "drivers": drivers.to_dict(orient="records"),
        "events": events.to_dict(orient="records"),
        "comp_streams": comp_streams.to_dict(orient="records"),
        "assets": assets.to_dict(orient="records"),
        "sources": sources.to_dict(orient="records"),
    }
    return json.dumps(payload, indent=2)


def style_app() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.3rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 0.2rem;
        }
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.045);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 0.75rem 0.9rem;
        }
        [data-testid="stMetricLabel"] {
            color: rgba(255, 255, 255, 0.72);
        }
        [data-testid="stMetricValue"] {
            color: rgba(255, 255, 255, 0.96);
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.12);
        }
        .small-note {
            color: rgba(255, 255, 255, 0.62);
            font-size: 0.9rem;
            line-height: 1.35;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def ensure_state() -> None:
    defaults = {
        "events": default_events(),
        "comp_streams": default_comp_streams(),
        "assets": default_assets(),
        "sources": default_sources(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_template(template: str) -> None:
    if template == "Blank":
        st.session_state.events = blank_events()
        st.session_state.comp_streams = blank_comp_streams()
        st.session_state.assets = blank_assets()
        st.session_state.sources = blank_sources()
    else:
        st.session_state.events = default_events()
        st.session_state.comp_streams = default_comp_streams()
        st.session_state.assets = default_assets()
        st.session_state.sources = default_sources()


def editor_config() -> dict[str, Any]:
    confidence_options = list(CONFIDENCE_SCORES)
    return {
        "Confidence": st.column_config.SelectboxColumn(
            "Confidence", options=confidence_options
        ),
        "Notes": st.column_config.TextColumn("Notes", width="large"),
        "URL": st.column_config.LinkColumn("URL", width="large"),
    }


def render_summary(
    summary: pd.DataFrame, drivers: pd.DataFrame, threshold: float, base_haircut: float
) -> None:
    low, base, high = [
        safe_number(
            summary.loc[
                summary["Scenario"] == scenario, "Estimated net worth ($m)"
            ].iloc[0]
        )
        for scenario in SCENARIOS
    ]
    spread = high - low
    threshold_stats = threshold_analysis(summary, drivers, threshold, base_haircut)

    metric_cols = st.columns([1.1, 1, 1, 1])
    metric_cols[0].metric("Base estimate", money(base))
    metric_cols[1].metric("Range", range_amount(low, high))
    metric_cols[2].metric("Scenario spread", money(spread))
    metric_cols[3].metric(
        "Threshold gap",
        money(safe_number(threshold_stats["Gap"])),
        delta=money(-safe_number(threshold_stats["Gap"])),
        delta_color="inverse",
    )

    chart_cols = st.columns([1.15, 1])
    with chart_cols[0]:
        fig = px.bar(
            summary,
            x="Scenario",
            y="Estimated net worth ($m)",
            text=summary["Estimated net worth ($m)"].map(money),
            color="Scenario",
            color_discrete_map={
                "Low": "#64748b",
                "Base": "#0f766e",
                "High": "#7c3aed",
            },
        )
        fig.add_hline(
            y=threshold,
            line_dash="dot",
            line_color="#991b1b",
            annotation_text=f"Threshold {money(threshold)}",
        )
        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            showlegend=False,
            yaxis_title="$m",
            xaxis_title=None,
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_cols[1]:
        by_type = (
            drivers.groupby("Type", dropna=False)["Base current ($m)"]
            .sum()
            .reset_index()
            .sort_values("Base current ($m)", ascending=True)
        )
        fig = px.bar(
            by_type,
            x="Base current ($m)",
            y="Type",
            orientation="h",
            text=by_type["Base current ($m)"].map(money),
            color_discrete_sequence=["#1f4e78"],
        )
        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis_title="$m",
            yaxis_title=None,
        )
        st.plotly_chart(fig, use_container_width=True)

    cols = st.columns(3)
    cols[0].metric(
        "Required lift to threshold",
        pct(100 * safe_number(threshold_stats["Required lift"])),
    )
    cols[1].metric(
        "Event-proceeds scaler",
        f"{safe_number(threshold_stats['Event scaler']):.2f}x",
    )
    cols[2].metric("Max base haircut at threshold", str(threshold_stats["Max haircut"]))


def render_driver_tables(drivers: pd.DataFrame) -> None:
    visible = drivers[
        [
            "Driver",
            "Type",
            "Low current ($m)",
            "Base current ($m)",
            "High current ($m)",
            "Sensitivity spread ($m)",
            "Confidence",
            "Source ID",
            "Notes",
        ]
    ].sort_values("Base current ($m)", ascending=False)
    st.dataframe(
        visible,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Low current ($m)": st.column_config.NumberColumn(format="$%.1f"),
            "Base current ($m)": st.column_config.NumberColumn(format="$%.1f"),
            "High current ($m)": st.column_config.NumberColumn(format="$%.1f"),
            "Sensitivity spread ($m)": st.column_config.NumberColumn(format="$%.1f"),
            "Notes": st.column_config.TextColumn(width="large"),
        },
    )

    top_sensitivity = visible.head(8).sort_values("Sensitivity spread ($m)")
    fig = go.Figure(
        go.Bar(
            x=top_sensitivity["Sensitivity spread ($m)"],
            y=top_sensitivity["Driver"],
            orientation="h",
            marker_color="#7c3aed",
            text=top_sensitivity["Sensitivity spread ($m)"].map(money),
        )
    )
    fig.update_layout(
        height=360,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title="High minus low current value ($m)",
        yaxis_title=None,
    )
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.set_page_config(
        page_title="Assumption Ledger",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    style_app()
    ensure_state()

    with st.sidebar:
        st.header("Model")
        template = st.selectbox("Template", ["Founder/executive sample", "Blank"])
        if st.button("Load template", use_container_width=True):
            load_template(template)

        valuation_date = st.date_input("Valuation date", value=date.today())
        threshold = st.number_input(
            "Threshold ($m)", min_value=0.0, value=1000.0, step=50.0
        )
        st.divider()
        st.subheader("Global Haircut")
        haircuts = {
            "Low": st.number_input("Low %", min_value=0.0, max_value=100.0, value=20.0),
            "Base": st.number_input(
                "Base %", min_value=0.0, max_value=100.0, value=10.0
            ),
            "High": st.number_input(
                "High %", min_value=0.0, max_value=100.0, value=5.0
            ),
        }
        st.caption("Post-model spending, philanthropy, errors, and unmodeled leakage.")

    st.title("Assumption Ledger")
    st.markdown(
        '<div class="small-note">Dated proceeds, compensation streams, return assumptions, leakage, and source quality.</div>',
        unsafe_allow_html=True,
    )

    valuation_year = valuation_date.year

    tabs = st.tabs(
        [
            "Workspace",
            "Liquidity events",
            "Comp streams",
            "Assets / liabilities",
            "Sources",
            "Export",
        ]
    )

    with tabs[1]:
        st.session_state.events = st.data_editor(
            st.session_state.events,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config=editor_config(),
        )

    with tabs[2]:
        st.session_state.comp_streams = st.data_editor(
            st.session_state.comp_streams,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config=editor_config(),
        )

    with tabs[3]:
        st.session_state.assets = st.data_editor(
            st.session_state.assets,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config=editor_config(),
        )

    with tabs[4]:
        st.session_state.sources = st.data_editor(
            st.session_state.sources,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config=editor_config(),
        )

    drivers = combine_drivers(
        st.session_state.events,
        st.session_state.comp_streams,
        st.session_state.assets,
        valuation_year,
    )
    summary = summarize(drivers, haircuts)
    quality = source_quality(drivers)

    with tabs[0]:
        render_summary(summary, drivers, threshold, haircuts["Base"])
        st.subheader("Drivers")
        render_driver_tables(drivers)
        cols = st.columns([1, 1])
        with cols[0]:
            st.subheader("Scenario totals")
            st.dataframe(
                summary,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Gross wealth ($m)": st.column_config.NumberColumn(format="$%.1f"),
                    "Global haircut %": st.column_config.NumberColumn(format="%.1f%%"),
                    "Estimated net worth ($m)": st.column_config.NumberColumn(
                        format="$%.1f"
                    ),
                },
            )
        with cols[1]:
            st.subheader("Evidence mix")
            st.dataframe(
                quality,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Base current ($m)": st.column_config.NumberColumn(format="$%.1f"),
                    "Share": st.column_config.ProgressColumn(
                        "Share", min_value=0, max_value=1, format="%.0f%%"
                    ),
                    "Score": st.column_config.NumberColumn(format="%.2f"),
                },
            )

    with tabs[5]:
        st.subheader("Model package")
        st.download_button(
            "Download model JSON",
            data=dataframe_for_download(
                summary,
                drivers,
                st.session_state.events,
                st.session_state.comp_streams,
                st.session_state.assets,
                st.session_state.sources,
            ),
            file_name="assumption-ledger-model.json",
            mime="application/json",
            use_container_width=True,
        )
        st.download_button(
            "Download driver table CSV",
            data=drivers.to_csv(index=False),
            file_name="drivers.csv",
            mime="text/csv",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
