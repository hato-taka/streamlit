import streamlit as st
import pandas as pd
from streamlit_carousel import carousel
from streamlit_javascript import st_javascript

from utils import *

# タイトルとファビコンの設定
st.set_page_config(
        page_title='東中野 麻雀部',
        page_icon="🀄️"                  
        )

# タイトル部分
st.title('東中野 Mリーグ')
st.image("top.jpg", use_container_width=True)

# 点数計算のフォーム
st.title("麻雀スコア計算フォーム")

# 説明文
st.markdown("25000点持ち、30000点返しです。半角数字で入力してください。")

# 順位ごとのスコア入力
st.subheader("スコア入力")


rank_1_name = st.selectbox('1位の名前', get_names(), index=0)

# st.text_input("1位：自動で計算されます", key="rank_1", value="自動で計算されます", disabled=True)
rank_1 = st.number_input("1位：", min_value=0, max_value=100000, step=1000, key="rank_1", value=30000)

rank_2_name = st.selectbox('2位の名前',get_names(), index=0)
rank_2 = st.number_input("2位：", min_value=0, max_value=100000, step=1000, key="rank_2", value=20000)

rank_3_name = st.selectbox('3位の名前',get_names(), index=0)
rank_3 = st.number_input("3位：", min_value=0, max_value=100000, step=1000, key="rank_3", value=10000)

rank_4_name = st.selectbox('4位の名前',get_names(), index=0)
rank_4 = st.number_input("4位：", min_value=-100000, max_value=100000, step=1000, key="rank_4", value=0)

# # レート選択
st.subheader("レート")
rate_options = ["50円（テンゴ）", "100円（テンピン）", "1円(テンイチ)"]
rate = st.selectbox("レートを選択してください", options=rate_options, key="rate")

# Session State の初期化
if "calc_button" not in st.session_state:
    st.session_state.calc_button = False
    
if "submit_button" not in st.session_state:
    st.session_state.submit_button = False

# 計算ボタン
if st.button("計算する"):
    st.session_state.calc_button = True
    
if st.session_state.calc_button:
    # データをまとめる
    ranks = ['1位', '2位', '3位', '4位']
    names = [rank_1_name, rank_2_name, rank_3_name, rank_4_name]
    scores = [rank_1, rank_2, rank_3, rank_4]
    # データフレームの作成
    df = pd.DataFrame({'雀士名': names, '得点': scores}, index=ranks)
    # 確認用テーブルの表示
    st.write("以下の点数で間違いないですか？")
    st.table(df)
    submit_button = st.button("送信する")
    if submit_button:
        st.session_state.submit_button = True
        
if st.session_state.submit_button:
    submit_data = [
        {"name": rank_1_name, "rank": 1, "score": rank_1},
        {"name": rank_2_name, "rank": 2, "score": rank_2},
        {"name": rank_3_name, "rank": 3, "score": rank_3},
        {"name": rank_4_name, "rank": 4, "score": rank_4},
        ]
    response = supabase.table("mahjong").insert(submit_data).execute()
    if response: 
        st.success("データが正常に追加されました！")
        show_table()
    else:
        st.error(f"データの追加に失敗しました: {response.json()}")
        
# Session State の初期化
if "first_button_clicked" not in st.session_state:
    st.session_state.first_button_clicked = False

if "second_button_clicked" not in st.session_state:
    st.session_state.second_button_clicked = False

st.header("順位表")

st.write("サンプル用の表")
show_average_scores()

# データの最新更新日を取得する
st.write(f"({get_last_date()}　更新)")

st.image("rank.jpg")

st.image("graph.jpg")

# テーブル一覧を表示する
st.header("成績表一覧")

show_table()

st.title("役満達成者")

# 役満達成者の画像のリスト
images = [
    dict(
        title="",
        text="",
        img="yakuman01.jpg"
    ),
    dict(
        title="",
        text="",
        img="yakuman02.jpg"
    ),
    dict(
        title="",
        text="",
        img="yakuman03.jpg"
    ),
]

# JavaScriptを使って画面幅を取得
screen_width = st_javascript("window.outerWidth")

# 画面幅が取得できなかった場合のデフォルト値
if screen_width is None:
    screen_width = 1024  # PC表示のデフォルト

# デバイスに基づく表示切り替え
if screen_width > 768:  # 幅が768pxより大きければPCと判断
    # カルーセルを表示
    selected_item = carousel(items=images, container_height=500)
else:  # 幅が768px以下ならSPと判断
    # SP用
    st.image("yakuman01.jpg")
    st.image("yakuman02.jpg")
    st.image("yakuman03.jpg")


st.markdown("### 順位表の説明")

html ="""
<details>

<summary>順位表の詳細ルール</summary>
<ul>
<li>平均点による順位</li>
<li>4戦以上の参加者が順位表掲載</li>  
<li>10戦以上の参加者がランキング対象</li>  
<li>三麻は対象外</li>
<li>ペア打ち代打ちはどちらの参加者の実績にするか申告制</li>
</ul>

<br>
期末に順位等による表彰予定で賞金を積み立てます。<br>  
1局毎に1位の人から200円徴収したいと思います。（健康麻雀の場合は対象外にしますので、順位申告時に健康等のコメントをお願いします）<br>
また全自動雀卓利用時は購入費カンパとして200円追加徴収したいと思います。（全自動雀卓利用しない場合は対象外にしますので、順位申告時に手積み等のコメントをお願いします）<br>
都度の徴収は面倒なので半期の締めか退部のタイミングで一括徴収します。
</details>
"""

st.html(html)

import matplotlib.pyplot as plt
# japanize_matplotlib は非推奨扱い
# import japanize_matplotlib
import matplotlib_fontja

# 仮のデータ
data = {
    "日付": [
        "7/7", "7/14", "7/21", "7/28", "8/4", "8/11", "8/18", "8/25", "9/1", "9/8", 
        "9/15", "9/22", "9/29", "10/6", "10/13", "10/20", "10/27", "11/3", "11/10", 
        "11/17", "11/24", "12/1", "12/8", "12/15", "12/22", "12/29"
    ],
    "おーはし": [0, -2, -3, -5, -7, -10, -12, -12, -10, -8, -5, -3, -2, 0, 2, 3, 5, 7, 8, 9, 10, 10, 10, 10, 10, 10],
    "ゆたかさん": [20, 18, 16, 15, 12, 10, 8, 6, 5, 3, 2, 0, -1, -2, -3, -5, -7, -8, -9, -10, -10, -10, -10, -10, -10, -10],
    "ぐっさん": [5, 4, 6, 8, 10, 12, 12, 12, 11, 10, 9, 7, 5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    # 他のデータをここに追加
}

# データをデータフレームに変換
df = pd.DataFrame(data)

# Streamlitで表示
st.title("平均点推移グラフ(途中)")

# 折れ線グラフをプロット
fig, ax = plt.subplots()
for column in df.columns[1:]:
    ax.plot(df["日付"], df[column], 'o-', label=column)

ax.set_title("平均点推移")
ax.set_xlabel("日付")
ax.set_ylabel("点数")
ax.legend()
ax.grid()

# 日付ラベルの間隔を調整
tick_interval = 3  # 表示する間隔（3つおきに表示）
ax.set_xticks(df["日付"][::tick_interval])  # 間引いて表示

st.pyplot(fig)