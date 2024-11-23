import streamlit as st
import pandas as pd
from streamlit_carousel import carousel

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
# def response():
#     return supabase.table("mahjong").select("*").execute()

# def insert(): 
#     return supabase.table("mahjong").insert(test2).execute()


st.set_page_config(
        page_title='東中野 麻雀部',
        page_icon="🀄️"                  
        )

# if st.button('データ取得'):
#     st.write(response().data)
#     st.write(response().data[0]['name'])

# if st.button('データ挿入'):
#     insert()
#     st.write('データ挿入完了')

st.title('東中野 Mリーグ')
st.image("top.jpg")
st.header("順位表 ")

# データの最新更新日を取得する
st.write('(11月17日更新)')

data = {
    '雀士名': ['コペ', 'せいか', 'しゅん', 'ゆたか', 'あーちゃん', 'おーはし', 'ぐっさん', 'なおき', 'みぞべ', 'こじ'],
    '平均順位': [2.26, 2.45, 2.46, 2.41, 2.39, 2.52, 2.56, 3.04, 3.00, 3.25],
    '平均得点': [8.30, 4.14, 2.26, 1.74, 1.01, -1.55, -1.69, -15.03, -15.52, -30.33]
}


df = pd.DataFrame(data, index=['1位','2位','3位', '4位', '5位', '6位', '7位', '8位', '-', '-'])

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

# カルーセルを表示
selected_item = carousel(items=images, container_height=500)


# st.image("yakuman01.jpg")

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