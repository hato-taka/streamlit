import streamlit as st
import pandas as pd


### supabaseの記述
from dotenv import load_dotenv
import os
from supabase import create_client, Client

# .env ファイルの内容を環境変数にロード
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def response():
    return supabase.table("mahjong").select("*").execute()

test2 =  {
    "name": "TEST2",
    "avg_score": 2,
    "avg_rank": 3,
    "date": "2024-10-02"
}

def insert(): 
    return supabase.table("mahjong").insert(test2).execute()


st.set_page_config(
        page_title='東中野 麻雀部',
        page_icon="🀄️"                  
        )

if st.button('データ取得'):
    st.write(response().data)
    st.write(response().data[0]['name'])

if st.button('データ挿入'):
    insert()
    st.write('データ挿入完了')

st.title('東中野 Mリーグ')
st.image("top.jpg")
st.header("順位表 ")
st.write('(10月17日更新)')

data = {
    '雀士名': ['コペ', 'せいか', 'しゅん', 'ゆたか', 'あーちゃん', 'おーはし', 'ぐっさん', 'なおき', 'みぞべ', 'こじ'],
    '平均順位': [2.26, 2.45, 2.46, 2.41, 2.39, 2.52, 2.56, 3.04, 3.00, 3.25],
    '平均得点': [8.30, 4.14, 2.26, 1.74, 1.01, -1.55, -1.69, -15.03, -15.52, -30.33]
}

data2 = {

}


df = pd.DataFrame(data, index=['1位','2位','3位', '4位', '5位', '6位', '7位', '8位', '-', '-'])

st.dataframe(df)

st.image("graph.jpg")

st.title("役満達成者")



st.markdown("### 順位表の説明")
text = """
平均点による順位  
4戦以上の参加者が順位表掲載  
10戦以上の参加者がランキング対象  
三麻は対象外  
ペア打ち代打ちはどちらの参加者の実績にするか申告制  

期末に順位等による表彰予定で賞金を積み立てます。  
1局毎に1位の人から200円徴収したいと思います。（健康麻雀の場合は対象外にしますので、順位申告時に健康等のコメントをお願いします）  
また全自動雀卓利用時は購入費カンパとして200円追加徴収したいと思います。（全自動雀卓利用しない場合は対象外にしますので、順位申告時に手積み等のコメントをお願いします）  
都度の徴収は面倒なので半期の締めか退部のタイミングで一括徴収します。
"""

st.write(text)