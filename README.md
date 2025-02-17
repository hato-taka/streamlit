
東中野 Mリーグ  
https://higashi-nakano-mahjong-club.streamlit.app/


dev環境
https://higashi-nakano-mahjong-club-dev.streamlit.app/

# streamlit
アプリの起動
`streamlit run app.py`

テキスト表示
```python
st.title("title") # タイトル
st.header("header") # ヘッダー
st.write("write") # 表示
st.markdown("# markdown") # マークダウンで表示
st.text("text") # テキスト表示
```

参照元: https://www.alpha.co.jp/blog/202304_02/


## 仮想環境への入り方
`source venv/bin/activate`

## パッケージの更新
`pip freeze > requirements.txt`

# テーブル設計

```mermaid
erDiagram
    mahjong {
        int id PK "Primary Key"
        varchar name "Player Name"
        int rank "Rank of the player"
        int score "Player's score"
        datetime created_at "Timestamp of game"
    }
```

# `toml`ファイルの使い方

```config.toml
# コメント行（# または // を使える）
title = "My Application" # シンプルなキーと値のペア

[database]  # セクション
host = "localhost"
port = 5432
user = "admin"
password = "password"

[api]  # 別のセクション
key = "your_api_key"
timeout = 30

[features]
enable_feature_x = true
enable_feature_y = false

# 配列
numbers = [1, 2, 3, 4, 5]
colors = ["red", "green", "blue"]

# ネストされたテーブル
[settings.logging]
level = "debug"
path = "/var/log/app.log"
```