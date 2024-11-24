import streamlit as st
import pandas as pd
from streamlit_carousel import carousel
from streamlit_javascript import st_javascript
from datetime import datetime
import pytz

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

# def insert(): 
#     return supabase.table("mahjong").insert(test2).execute()


st.set_page_config(
        page_title='東中野 麻雀部',
        page_icon="🀄️"                  
        )

if st.button('データ取得'):
    st.write(get_all_data().data)

# if st.button('データ挿入'):
#     insert()
#     st.write('データ挿入完了')

# 入力フォーム
with st.form(key="input_form"):
    name = st.text_input("名前を入力してください")
    rank = st.number_input("順位を入力してください", min_value=1, max_value=4, step=1)
    score = st.number_input("スコアを入力してください", min_value=0, step=1)
    submit_button = st.form_submit_button(label="送信")
    
# データをSupabaseに挿入
if submit_button:
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

# データフレームに変換
row_data = get_all_data().data
df_row_data = pd.DataFrame(row_data)
formatted_data = df_row_data.drop(columns=["id"])
df = pd.DataFrame(formatted_data)
st.dataframe(df)  # Streamlitのデータフレーム表示

# ISO形式の日時文字列
utc_time_str = get_last_date()

# ISO形式の文字列をUTCのdatetimeオブジェクトに変換
utc_time = datetime.fromisoformat(utc_time_str)

# UTCからJSTに変換
jst_timezone = pytz.timezone("Asia/Tokyo")
jst_time = utc_time.astimezone(jst_timezone)

# JSTのdatetimeオブジェクトを日本の形式で文字列に変換
jst_time_str = jst_time.strftime("%Y年%m月%d日 %H時")

st.title('東中野 Mリーグ')
st.image("top.jpg", use_container_width=True)
st.header("順位表 ")

# データの最新更新日を取得する

st.write(f"({jst_time_str}　更新)")

data = {
    '雀士名': ['コペ', 'せいか', 'しゅん', 'ゆたか', 'あーちゃん', 'おーはし', 'ぐっさん', 'なおき', 'みぞべ', 'こじ'],
    '平均順位': [2.26, 2.45, 2.46, 2.41, 2.39, 2.52, 2.56, 3.04, 3.00, 3.25],
    '平均得点': [8.30, 4.14, 2.26, 1.74, 1.01, -1.55, -1.69, -15.03, -15.52, -30.33]
}

df = pd.DataFrame(data, index=['1位','2位','3位', '4位', '5位', '6位', '7位', '8位', '-', '-'])

# テスト用
import numpy as np
import plotly.graph_objects as go
import time

st.title("Plotlyで折れ線グラフのアニメーション")

# ボタンを作成
start_animation = st.button("アニメーションを開始")

# ボタンが押された場合の処理
if start_animation:
    # 初期データ
    x_data = []
    y1_data = []
    y2_data = []

    # PlotlyのFigureを作成
    fig = go.Figure()

    # Sin(x)とCos(x)のトレースを追加
    fig.add_trace(go.Scatter(x=x_data, y=y1_data, mode='lines', name='sin(x)'))
    fig.add_trace(go.Scatter(x=x_data, y=y2_data, mode='lines', name='cos(x)'))
    # 凡例の位置を変更
    fig.update_layout(
        legend=dict(
            x=0.5,  # 横方向の位置 (0: 左端, 1: 右端)
            y=-0.3,    # 縦方向の位置 (0: 下端, 1: 上端)
            xanchor='center',  # 横方向のアンカー (center, left, right)
            yanchor='top'      # 縦方向のアンカー (top, middle, bottom)
        )
    )

    # グラフ用のコンテナ
    chart_placeholder = st.plotly_chart(fig, use_container_width=True)

    # アニメーションループ
    for i in range(1, 101):
        # 新しいデータポイントを計算
        new_x = i / 10
        x_data.append(new_x)
        y1_data.append(np.sin(new_x))
        y2_data.append(np.cos(new_x))
        
        # データを更新
        fig.data[0].x = x_data
        fig.data[0].y = y1_data
        fig.data[1].x = x_data
        fig.data[1].y = y2_data

        # グラフを更新
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # アニメーション速度を調整
        time.sleep(0.1)


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