import streamlit as st
import pandas as pd
from streamlit_carousel import carousel
from streamlit_javascript import st_javascript
from datetime import datetime
import pytz
from dateutil.parser import isoparse

### supabaseの記述
from dotenv import load_dotenv
import os
from supabase import create_client, Client

# .env ファイルの内容を環境変数にロード
# ローカル環境でのみ .env を読み込む
if not st.secrets:
    load_dotenv(override=True)

# url: str = os.getenv("SUPABASE_URL")
# key: str = os.getenv("SUPABASE_KEY")
url: str = st.secrets["general"]["SUPABASE_URL"]
key: str = st.secrets["general"]["SUPABASE_KEY"]
supabase: Client = create_client(url, key)
# 暫定対応
# supabase: Client = create_client("https://gljyxcfuckrjlwiwvovz.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdsanl4Y2Z1Y2tyamx3aXd2b3Z6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIzMTcwNjEsImV4cCI6MjA0Nzg5MzA2MX0.qb1gwwhaGXqwhy3kmVEwkX2p1Df1vx4b9gC1ZIlmJ3Y")


# エラー時の記述を追加する
def get_all_data():
    return supabase.table("mahjong").select("*").execute()

def get_last_date():
    response = supabase.table("mahjong").select("created_at").order("created_at", desc=True).limit(1).execute()
    return response.data[0]["created_at"]

def insert(name, score, rank): 
    if name and score and rank is not None:
        data = {"name": name, "rank": rank, "score": score}
        response = supabase.table("mahjong").insert(data).execute()

        # ステータスコードをチェック
        if response:  # 201は作成成功のステータスコード
            st.success("データが正常に追加されました！")
            st.write("追加されたデータ:")
            st.json(response.data)
        else:
            st.error(f"データの追加に失敗しました: {response.json()}")
    else:
        st.warning("全ての項目を入力してください！")

st.set_page_config(
        page_title='東中野 麻雀部',
        page_icon="🀄️"                  
        )


def show_table():
    # データフレームに変換
    row_data = get_all_data().data
    df_row_data = pd.DataFrame(row_data)
    formatted_data = df_row_data.drop(columns=["id"])
    df = pd.DataFrame(formatted_data)
    st.dataframe(df)  # Streamlitのデータフレーム表示

# ISO形式の日時文字列
utc_time = isoparse(get_last_date())

# UTCからJSTに変換
jst_timezone = pytz.timezone("Asia/Tokyo")
jst_time = utc_time.astimezone(jst_timezone)

# JSTのdatetimeオブジェクトを日本の形式で文字列に変換
jst_time_str = jst_time.strftime("%Y年%m月%d日 %H時")

# タイトル部分
st.title('東中野 Mリーグ')
st.image("top.jpg", use_container_width=True)

# 点数計算のフォーム
st.title("麻雀スコア計算フォーム")

# 説明文
st.markdown("25000点持ち、30000点返しです。半角数字で入力してください。")

# 順位ごとのスコア入力
st.subheader("スコア入力")


rank_1_name = st.text_input("1位の名前", key="rank_1_name")
# st.text_input("1位：自動で計算されます", key="rank_1", value="自動で計算されます", disabled=True)
rank_1 = st.number_input("1位：", min_value=0, max_value=100000, step=1000, key="rank_1", value=10000)

rank_2_name = st.text_input("2位の名前", key="rank_2_name")
rank_2 = st.number_input("2位：", min_value=0, max_value=100000, step=1000, key="rank_2", value=10000)

rank_3_name = st.text_input("3位の名前", key="rank_3_name")
rank_3 = st.number_input("3位：", min_value=0, max_value=100000, step=1000, key="rank_3", value=10000)

rank_4_name = st.text_input("4位の名前", key="rank_4_name")
rank_4 = st.number_input("4位：", min_value=-100000, max_value=100000, step=1000, key="rank_4", value=1000)

# # ウマ選択
# st.subheader("ウマ")
# uma_options = ["10-20（標準）", "20-40", "30-60"]
# uma = st.selectbox("ウマを選択してください", options=uma_options, key="uma")

# # レート選択
# st.subheader("レート")
# rate_options = ["50円（テンゴ）", "100円（テンピ）", "500円"]
# rate = st.selectbox("レートを選択してください", options=rate_options, key="rate")

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
        st.write("追加されたデータ:")
        st.json(response.data)
    else:
        st.error(f"データの追加に失敗しました: {response.json()}")
        
# Session State の初期化
if "first_button_clicked" not in st.session_state:
    st.session_state.first_button_clicked = False

if "second_button_clicked" not in st.session_state:
    st.session_state.second_button_clicked = False

st.header("順位表 ")

# データの最新更新日を取得する
st.write(f"({jst_time_str}　更新)")

data = {
    '雀士名': ['コペ', 'せいか', 'しゅん', 'ゆたか', 'あーちゃん', 'おーはし', 'ぐっさん', 'なおき', 'みぞべ', 'こじ'],
    '平均順位': [2.26, 2.45, 2.46, 2.41, 2.39, 2.52, 2.56, 3.04, 3.00, 3.25],
    '平均得点': [8.30, 4.14, 2.26, 1.74, 1.01, -1.55, -1.69, -15.03, -15.52, -30.33]
}

df = pd.DataFrame(data, index=['1位','2位','3位', '4位', '5位', '6位', '7位', '8位', '-', '-'])
# 小数点第2位までフォーマットを適用
styled_df = df.style.format({"平均順位": "{:.2f}", "平均得点": "{:.2f}"})
# st.table(styled_df)


# st.dataframe(df)
st.image("rank.jpg")

st.image("graph.jpg")

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