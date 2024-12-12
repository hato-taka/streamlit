import streamlit as st
import pandas as pd
import pytz
from dateutil.parser import isoparse

### supabaseの記述
from supabase import create_client, Client

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
    updated_time = response.data[0]["created_at"]
    # ISO形式の日時文字列
    utc_updated_time = isoparse(updated_time)
    # UTCからJSTに変換
    jst_timezone = pytz.timezone("Asia/Tokyo")
    jst_updated_time = utc_updated_time.astimezone(jst_timezone)
    # JSTのdatetimeオブジェクトを日本の形式で文字列に変換
    jst_time_str = jst_updated_time.strftime("%Y年%m月%d日 %H時")
    
    return jst_time_str

def show_table():
    # データフレームに変換
    row_data = get_all_data().data
    df_row_data = pd.DataFrame(row_data)
    formatted_data = df_row_data.drop(columns=["id"])
    # カラム順を入れ替える
    desired_order = ["name", "rank", "score", "created_at"]  # 任意の順番を指定
    df = formatted_data[desired_order]  # 指定した順番に並べ替える
    st.dataframe(df)  # Streamlitのデータフレーム表示

# 平均スコアを計算して表示する関数
def show_average_scores():

    # データを取得
    response = get_all_data()
    row_data = response.data
    
    # DataFrameに変換
    df = pd.DataFrame(row_data)

    # Nameごとに平均スコアと合計スコアを算出    
    scores_summary = df.groupby("name").agg(
        平均点=("score", "mean"),
        合計点=("score", "sum")
    ).reset_index()

    # Streamlitで表示
    st.dataframe(scores_summary)

# 累計得点

# 平均順位

# 参加回数

# 1位の回数

# データの追加
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