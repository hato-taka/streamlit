import streamlit as st
import pandas as pd
import numpy as np

st.image("top.jpg", caption="麻雀の写真")
st.title('麻雀部')
st.write('東中野麻雀部の結果発表')

print(np.random.randn(20, 3))
two_dimensional_list = [
    [1, 9, 3],
    [4, 7, 6],
    [7, 3, 9]
]
chart_data = pd.DataFrame(two_dimensional_list, columns=["a", "b", "c"])

st.line_chart(chart_data, x_label="日にち", y_label="得点")

data = {
    'name': ['Naoki', 'Ohashi', 'ゆたか'],
    'score': [100, 200,300]
}

df = pd.DataFrame(data)

st.dataframe(df)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write(uploaded_file)