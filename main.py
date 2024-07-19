import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------------------------

st.title("Ma'lumotlar to'plami haqida")

@st.cache_data
def load_data(url):
    df = pd.read_csv(url).drop('Unnamed: 0', axis=1)
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

# --------------------------------------------------------------------

st.title("Tozalash")
df2 = load_data('123.csv')
st.dataframe(df2)
st.write('Olib tashlangan ustunlar: url, address va phone')

st.subheader("Yes/No to True/False")
df['online_order'] = df['online_order'] == 'Yes'
df['book_table'] = df['book_table'] == 'Yes'
st.dataframe(df[['online_order', 'book_table']])
st.write(df['book_table'].dtype)

st.subheader("Clear 'rate'")
df['rate'] = df['rate'].str.replace('/5', '').str.replace('[/5 -]', '', regex=True)
df['rate'] = df['rate'].str.replace('NEW', '-1.0')
df['rate'] = df['rate'].replace('', np.nan)
df['rate'] = df['rate'].fillna(-2)
df['rate'] = df['rate'].astype(float)
st.dataframe(df)
st.write('-1 - yangi')
st.write('-2 - baholanmagan')
st.write(df['rate'].dtype)

st.subheader("Ustunlar tipi")
st.write(df.dtypes)