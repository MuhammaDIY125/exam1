import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------------------------

st.set_page_config(
    page_title="Zomato Bangalore Restaurants"
)

def space(num_lines=1):
    """qancha joy tashlash"""
    for _ in range(num_lines):
        st.write("")

@st.cache_data
def load_data(url):
    df = pd.read_csv(url).drop('Unnamed: 0', axis=1)
    return df

df = load_data('zomato_new.csv')

# --------------------------------------------------------------------

st.header("Ma'lumotlar to'plami haqida", divider=True)

st.subheader("DataFrame")
st.dataframe(df)

st.write("Qatorlar soni:", df.shape[0])
st.write("Ustunlar soni:", df.shape[1])

space(2)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ustunlar tipi")
    st.dataframe(df.dtypes)

with col2:
    st.subheader("Ustunlardagi NaN lar soni")
    st.write(df.isnull().sum())
    st.write('Umumiy NaN lar soni:', df.isnull().sum().sum())

space(2)

# --------------------------------------------------------------------

st.header("Tozalash", divider=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Olib tashlangan ustunlar",
                                  "online_order va book_table",
                                  "rate",
                                  "location",
                                  "cuisines"])

with tab1:
    st.dataframe(load_data('123.csv'))

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.write(df['online_order'].dtype)
        st.dataframe(df[['online_order', 'book_table']])
    with col2:
        df['online_order'] = df['online_order'] == 'Yes'
        df['book_table'] = df['book_table'] == 'Yes'
        st.write(df['online_order'].dtype)
        st.dataframe(df[['online_order', 'book_table']])

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.write(df['rate'].dtype)
        st.dataframe(df['rate'])
        st.write('NEW - yangi')
        st.write(None, '- baholanmagan')
    with col2:
        df['rate'] = df['rate'].str.replace('[/5 -]', '', regex=True)
        df['rate'] = df['rate'].str.replace('NEW', '-1.0')
        df['rate'] = df['rate'].replace('', np.nan).fillna(-2)
        df['rate'] = df['rate'].astype(float)
        st.write(df['rate'].dtype)
        mask = (df['rate'] < 0) & (df['reviews_list'] != '[]') & (df['votes'] == 0)
        st.dataframe(df[mask])
        st.dataframe(df['rate'])
        st.write(-1, '- yangi')
        st.write(-2, '- baholanmagan')

with tab4:
    mask = df['location'].isna()
    st.dataframe(df[mask])
    st.write("location ustunidagi NaN lar soni:", df['location'].isnull().sum())
    df = pd.DataFrame(df.dropna(subset='location'))

with tab5:
    mask = df['cuisines'].isna()
    st.dataframe(df[mask])
    df.loc[911, 'cuisines'] = '-'
    df.loc[3380, 'cuisines'] = 'Andhra, Chinese'
    df.loc[8412, 'cuisines'] = '-'
    df.loc[9424, 'cuisines'] = '-'
    st.dataframe(df[mask])
    # st.write("location ustunidagi NaN lar soni:", df['location'].isnull().sum())
    # df = pd.DataFrame(df.dropna(subset='location'))

space(30)

st.dataframe(df)