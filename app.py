from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

import streamlit as st

from converter import convert_takeout_zip_bytes, sanitize_filename_part


APP_TITLE = "Fitbit ZIP to CSV Converter"
APP_SUBTITLE = (
    "This app runs entirely on your computer. It reads a Fitbit ZIP export, "
    "processes it locally, and lets you download a CSV locally."
)


def parse_optional_date(text: str) -> Optional[date]:
    text = (text or "").strip()
    if not text:
        return None
    return date.fromisoformat(text)


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📦",
    layout="wide",
)

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

with st.expander("How to use", expanded=True):
    st.markdown(
        """
1. Upload a Fitbit ZIP export.
2. Optionally enter a start and/or end date in `YYYY-MM-DD` format.
3. Choose whether to keep only overlapping dates across all domains.
4. Click **Convert ZIP to CSV**.
5. Download the CSV.
        """
    )

uploaded_file = st.file_uploader(
    "Choose a Fitbit ZIP file",
    type=["zip"],
    accept_multiple_files=False,
)

col1, col2 = st.columns(2)
start_text = col1.text_input(
    "Optional start date (YYYY-MM-DD)",
    value="",
    placeholder="e.g. 2024-01-01",
)
end_text = col2.text_input(
    "Optional end date (YYYY-MM-DD)",
    value="",
    placeholder="e.g. 2024-12-31",
)

intersect_dates = st.checkbox(
    "Keep only dates that overlap across all activity/sleep domains",
    value=True,
    help="If checked, the app keeps only the shared date range across the parsed domains.",
)

convert_clicked = st.button("Convert ZIP to CSV", type="primary", use_container_width=True)

if convert_clicked:
    if uploaded_file is None:
        st.error("Please upload a ZIP file first.")
    else:
        try:
            user_start = parse_optional_date(start_text)
            user_end = parse_optional_date(end_text)

            if user_start and user_end and user_start > user_end:
                st.error("Start date must be on or before end date.")
            else:
                zip_bytes = uploaded_file.getvalue()
                out_bytes, activity_rows, sleep_rows, date_range = convert_takeout_zip_bytes(
                    zip_bytes=zip_bytes,
                    intersect_dates=intersect_dates,
                    user_start=user_start,
                    user_end=user_end,
                )

                stem = sanitize_filename_part(Path(uploaded_file.name).stem)
                if date_range is None:
                    suffix = "all_dates"
                else:
                    suffix = f"{date_range[0].isoformat()}_to_{date_range[1].isoformat()}"
                out_name = f"{stem}_converted_{suffix}.csv"

                st.session_state["result"] = {
                    "out_bytes": out_bytes,
                    "out_name": out_name,
                    "activity_rows": activity_rows,
                    "sleep_rows": sleep_rows,
                    "date_range": date_range,
                }
        except ValueError as exc:
            st.error(f"Invalid date or ZIP content: {exc}")
        except Exception as exc:
            st.error(f"Conversion failed: {exc}")

result = st.session_state.get("result")
if result:
    activity_rows = result["activity_rows"]
    sleep_rows = result["sleep_rows"]
    date_range = result["date_range"]

    st.success("Conversion finished.")

    m1, m2, m3 = st.columns(3)
    m1.metric("Activity rows", len(activity_rows))
    m2.metric("Sleep rows", len(sleep_rows))
    m3.metric(
        "Date range",
        "None" if date_range is None else f"{date_range[0].isoformat()} → {date_range[1].isoformat()}",
    )

    st.download_button(
        label="Download CSV",
        data=result["out_bytes"],
        file_name=result["out_name"],
        mime="text/csv",
        use_container_width=True,
    )

    tab1, tab2 = st.tabs(["Activity preview", "Sleep preview"])
    with tab1:
        if activity_rows:
            st.dataframe(activity_rows[:200], use_container_width=True)
        else:
            st.info("No activity rows were produced.")

    with tab2:
        if sleep_rows:
            st.dataframe(sleep_rows[:200], use_container_width=True)
        else:
            st.info("No sleep rows were produced.")
