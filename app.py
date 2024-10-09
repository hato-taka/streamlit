import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib
import matplotlib.dates as mdates


st.title('東中野 Mリーグ')
st.image("top.jpg")
st.write('東中野麻雀部の結果発表')

st.header("順位表 (10月7日更新)")

data = {
    '雀士名': ['コペ', 'せいか', 'ゆたか', 'しゅん', 'ぐっさん', 'あーちゃん', 'おーはし', 'なおき', 'こじ'],
    '平均順位': [2.29, 2.48, 2.39, 2.53, 2.53, 2.45, 2.49, 2.81, 3.25],
    '平均得点': [6.94, 4.24, 2.71, -0.01, -0.71, -0.77, -1.40, -9.39, -30.33]
}

df = pd.DataFrame(data, index=['1位','2位','3位', '4位', '5位', '6位', '7位', '8位', '-'])

st.dataframe(df)

st.image("graph.jpg")