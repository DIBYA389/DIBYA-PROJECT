"""Streamlit app: merge PD, LGD, EAD inputs and compute Expected Credit Loss (ECL)."""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ECL Calculator", layout="wide")
st.title("Expected Credit Loss (ECL) Calculator")
st.caption("ECL = PD x LGD x EAD, computed per account ID")

DEFAULT_PD_PATH = "data/pd_sample.csv"
DEFAULT_LGD_PATH = "data/lgd_sample.csv"
DEFAULT_EAD_PATH = "data/ead_sample.csv"


@st.cache_data
def load_default(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_input(label: str, default_path: str, value_col: str) -> pd.DataFrame:
    uploaded = st.sidebar.file_uploader(f"{label} file (ID, {value_col})", type="csv", key=label)
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        df = load_default(default_path)
    missing = {"ID", value_col} - set(df.columns)
    if missing:
        st.error(f"{label} file is missing column(s): {', '.join(sorted(missing))}")
        st.stop()
    return df[["ID", value_col]]


st.sidebar.header("Input data")
st.sidebar.caption("Upload your own CSVs, or leave blank to use the bundled sample data.")

pd_df = load_input("PD", DEFAULT_PD_PATH, "PD")
lgd_df = load_input("LGD", DEFAULT_LGD_PATH, "LGD")
ead_df = load_input("EAD", DEFAULT_EAD_PATH, "EAD")

merged = pd_df.merge(lgd_df, on="ID", how="inner").merge(ead_df, on="ID", how="inner")
merged["ECL"] = merged["PD"] * merged["LGD"] * merged["EAD"]

st.sidebar.metric("Accounts matched", len(merged))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total EAD", f"{merged['EAD'].sum():,.0f}")
col2.metric("Average PD", f"{merged['PD'].mean():.2%}")
col3.metric("Average LGD", f"{merged['LGD'].mean():.2%}")
col4.metric("Total ECL", f"{merged['ECL'].sum():,.0f}")

st.subheader("Account-level detail")
st.dataframe(
    merged.sort_values("ECL", ascending=False).style.format(
        {"PD": "{:.2%}", "LGD": "{:.2%}", "EAD": "{:,.2f}", "ECL": "{:,.2f}"}
    ),
    use_container_width=True,
)

st.subheader("ECL distribution")
st.bar_chart(merged.set_index("ID")["ECL"])

st.subheader("Top 10 exposures by ECL")
st.table(
    merged.sort_values("ECL", ascending=False)
    .head(10)
    .set_index("ID")
    .style.format({"PD": "{:.2%}", "LGD": "{:.2%}", "EAD": "{:,.2f}", "ECL": "{:,.2f}"})
)

st.download_button(
    "Download ECL results as CSV",
    data=merged.to_csv(index=False).encode("utf-8"),
    file_name="ecl_results.csv",
    mime="text/csv",
)
