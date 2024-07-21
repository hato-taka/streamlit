import streamlit as st
import pandas as pd

st.title('麻雀部')
st.write('東中野麻雀部の結果発表')

data = {
    'name': ['Naoki', 'Ohashi', 'ゆたか'],
    'score': [100, 200,300]
}

df = pd.DataFrame(data)

st.dataframe(df)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write(uploaded_file)