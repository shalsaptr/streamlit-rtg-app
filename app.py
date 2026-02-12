import streamlit as st
import pandas as pd

st.title("Gabung Data Bulanan RTG")

files = st.file_uploader(
    "Upload file bulanan",
    type=["xls","xlsx"],
    accept_multiple_files=True
)

all_df = []

def read_excel_safe(file):
    name = file.name.lower()
    if name.endswith(".xlsx"):
        return pd.read_excel(file, engine="openpyxl")
    elif name.endswith(".xls"):
        return pd.read_excel(file, engine="xlrd")
    else:
        return pd.read_excel(file)

if files:
    for file in files:
        try:
            df = read_excel_safe(file)

            bulan = ".".join(file.name.split(".")[:2])
            df.insert(0, "BULAN", bulan)

            all_df.append(df)

        except Exception as e:
            st.error(f"Gagal baca file {file.name}: {e}")

    if all_df:
        final = pd.concat(all_df, ignore_index=True)
        st.dataframe(final)

        final.to_excel("hasil.xlsx", index=False)
        with open("hasil.xlsx","rb") as f:
            st.download_button("Download Excel", f, "hasil.xlsx")
