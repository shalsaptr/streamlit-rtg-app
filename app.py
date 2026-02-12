import streamlit as st
import pandas as pd

st.title("Gabung Data Bulanan RTG")

files = st.file_uploader(
    "Upload file bulanan",
    type=["xls","xlsx"],
    accept_multiple_files=True
)

all_df = []

if files:
    for file in files:
        df = pd.read_excel(file)
        bulan = ".".join(file.name.split(".")[:2])
        df.insert(0, "BULAN", bulan)
        all_df.append(df)

    final = pd.concat(all_df, ignore_index=True)
    st.dataframe(final)

    final.to_excel("hasil.xlsx", index=False)
    with open("hasil.xlsx","rb") as f:
        st.download_button("Download Excel", f, "hasil.xlsx")
