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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
"Olib tashlangan ustunlar",
"online_order va book_table",
"rate",
"votes",
"location",
"rest_type",
"dish_liked",
"cuisines",
"approx_cost(for two people)",
"menu_item"])

with tab1:
    st.dataframe(load_data('123.csv'))

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df[['online_order', 'book_table']])
        st.write(df['online_order'].dtype)
    with col2:
        df['online_order'] = df['online_order'] == 'Yes'
        df['book_table'] = df['book_table'] == 'Yes'
        st.dataframe(df[['online_order', 'book_table']])
        st.write(df['online_order'].dtype)

with tab3:
    c = ['rate', 'votes', 'reviews_list']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.dataframe(df[c])
        st.write(df[c[0]].dtype)
        st.write('yangi: "NEW"')
        st.write('baholanmagan:', None)
    with col2:
        df[c[0]] = df[c[0]].str.replace('[/5 -]', '', regex=True)
        df[c[0]] = df[c[0]].str.replace('NEW', '-1.0')
        df[c[0]] = df[c[0]].replace('', np.nan).fillna(-2)
        df[c[0]] = df[c[0]].astype(float)
        mask = df[c[0]] < 0
        st.dataframe(df[mask][c])
        st.write(df[c[0]].dtype)
        st.write('yangi:', -1)
        st.write('baholanmagan:', -2)
    with col3:
        mask = (df[c[0]] < 0) & (df[c[2]] != '[]') & (df[c[1]] == 0)
        for i in df[mask].index.tolist():
            df.loc[i, c[0]] = float(df.loc[i, c[2]][9])
        st.dataframe(df[mask][c])
    space(5)
    st.dataframe(df[c])

with tab4:
    c = ['rate', 'votes']
    mask = (df[c[0]] > 0) & (df[c[1]] == 0)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df[mask][c])
    with col2:
        df.loc[mask, c[1]] = 1
        st.dataframe(df[mask][c])

with tab5:
    mask = df['location'].isna()
    st.dataframe(df[mask])
    st.write("location ustunidagi NaN lar soni:", df['location'].isnull().sum())
    df = pd.DataFrame(df.dropna(subset='location'))

with tab6:
    c = ['name', 'rest_type']
    mask = df[c[1]].isna()
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df[mask][c])
    with col2:
        df[c[1]] = df[c[1]].fillna('-')
        st.dataframe(df[mask][c])

with tab7:
    c = ['name', 'dish_liked']
    mask = df[c[1]].isna()
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df[mask][c])
    with col2:
        df[c[1]] = df[c[1]].fillna('-')
        st.dataframe(df[mask][c])

with tab8:
    mask = df['cuisines'].isna()
    st.dataframe(df[mask])
    df.loc[911, 'cuisines'] = '-'
    df.loc[3380, 'cuisines'] = 'Andhra, Chinese'
    df.loc[8412, 'cuisines'] = '-'
    df.loc[9424, 'cuisines'] = '-'
    st.dataframe(df[mask])

with tab9:
    c = 'approx_cost(for two people)'
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df[c])
        st.write(df[c].dtype)
    with col2:
        df[c] = df[c].str.replace(',', '', regex=True)
        df[c] = df[c].fillna(-100)
        df[c] = df[c].astype(int)
        st.dataframe(df[c])
        st.write(df[c].dtype)

with tab10:
    c = ['menu_item', 'dish_liked']
    def t10(row):
        if row[c[0]] == '[]' and row[c[1]] != '-':
            s = []
            for i in str(row[c[1]]).split(', '):
                s.append(i)
            return str(s)
        else:
            return row[c[0]]
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df[c])
    with col2:
        df[c[0]] = df.apply(t10, axis=1)
        st.dataframe(df[c])

st.markdown('---')

space(2)

st.dataframe(df)
st.write('Umumiy NaN lar soni:', df.isnull().sum().sum())