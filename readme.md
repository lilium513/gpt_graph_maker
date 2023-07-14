# 各コードの役割について
## streamlit_app.py
- 画面を構成するファイル
- 中に入っている「parse_analysis_str_and_to_graph」関数
  - GPTの結果を辞書にしたものを使ってグラフの描画を行う関数
 
## try_function_calling.py
- auto_data_analysis関数
  - 分析対象のデータの一部を`data`として受け取ることで、分析案や可視化案を作成する関数
  - こちらに関しては [fucntion_calling](https://platform.openai.com/docs/guides/gpt/function-calling) を使用している

# 実行方法について
- 環境変数`open_api_key`にAPIkeyをセット
- `streamlit run streamlit_app.py`でアプリケーションを起動
