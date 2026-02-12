import streamlit as st
import pandas as pd

st.title("Gabung Data Bulanan RTG")

files = st.file_uploader(
    "Upload file bulanan",
    type=["xls","xlsx","html"],
    accept_multiple_files=True
)

all_df = []

def read_any_excel(file):
    try:
        # coba excel normal dulu
        return pd.read_excel(file, engine="openpyxl")
    except:
        try:
            file.seek(0)
            return pd.read_excel(file, engine="xlrd")
        except:
            # fallback: kemungkinan html disguised as xls
            file.seek(0)
            tables = pd.read_html(file)
            return tables[0]

if files:
    for file in files:
        try:
            df = read_any_excel(file)

            bulan = ".".join(file.name.split(".")[:2])
            df.insert(0, "BULAN", bulan)

            all_df.append(df)

        except Exception as e:
            st.error(f"Gagal baca file {file.name}: {e}")

    if all_df:
        final = pd.concat(all_df, ignore_index=True)

        st.success("Data berhasil digabung")
        st.dataframe(final)

        final.to_excel("hasil.xlsx", index=False)

        with open("hasil.xlsx","rb") as f:
            st.download_button("Download Excel", f, "hasil.xlsx")
