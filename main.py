import streamlit as st
import pandas as pd

# --------------------------------------------------------------------

st.title("Ma'lumotlar to'plami haqida")

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data('zomato_new.csv')

st.subheader("DataFrame")
st.dataframe(df)

st.write(f"Qatorlar soni: {df.shape[0]}")
st.write(f"Ustunlar soni: {df.shape[1]}")

st.subheader("Ustunlar tipi")
st.write(df.dtypes)

st.subheader("Ustunlardagi NaN lar soni")
st.write(df.isnull().sum())
st.write('Umumiy NaN lar soni:', df.isnull().sum().sum())