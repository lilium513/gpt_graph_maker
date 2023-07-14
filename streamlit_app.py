import streamlit as st
import pandas as pd
from time import time
import openai
import plotly.express as px
from try_function_calling import auto_data_analysis
import os

openai.api_key = os.environ["open_api_key"]
f = st.file_uploader("Upload a CSV", type="csv")
charset = ""
sample_size = 30


def parse_analysis_str_and_to_graph(direction_dict, df):
    print(direction_dict)
    agg = direction_dict["agg_type"]
    by = direction_dict["agg_by"].split(",")
    agg_target = direction_dict["agg_num"]
    df_grouped = df.groupby(by)[agg_target].agg(agg).reset_index()
    print(df_grouped.head())
    graph_x = direction_dict["x_column"]
    graph_y = direction_dict["y_column"]
    if direction_dict["graph_type"] == "bar":
        fig = px.histogram(df_grouped, x=graph_x, y=graph_y)
        st.plotly_chart(fig, use_container_width=True)
    if direction_dict["graph_type"] == "line":
        fig = px.line(df_grouped, x=graph_x, y=graph_y)
        st.plotly_chart(fig, use_container_width=True)


if f is not None:
    with f:
        # shift_jisを想定
        charset = "shift_jis"
        print("set : ", charset)
        df = pd.read_csv(f, encoding=charset)
        sampled_data = df.sample(sample_size, random_state=42)
        sampled_data_string = sampled_data.to_csv(index=False)
        st.subheader("↓データの一部を表示します")
        st.write(sampled_data.head(15))

    # N : 分析数を設定する
    N = 1
    if st.button(label="GPTで解析する"):
        st.session_state.analysis_candidates = []
        for i in range(N):
            with st.spinner(f"分析案を検討中です{i+1}/{N}"):
                gpt_response = auto_data_analysis(sampled_data_string)
                st.session_state.analysis_candidates.append(gpt_response)
st.session_state


buttons = []
if "analysis_candidates" in st.session_state:
    print("here")
    analysis_candidates_list = st.session_state.analysis_candidates
    st.write("以下のような分析が考えられます")

    for i, analysis_candidate in enumerate(analysis_candidates_list):
        title = analysis_candidate["analysis_title"]
        desc = analysis_candidate["insight_hint"]
        st.markdown(f"## {title}")
        st.markdown(f"- {desc}")
        if st.button(f"{i+1}番目の分析案のグラフを作成"):
            parse_analysis_str_and_to_graph(analysis_candidates_list[i], df)
