import openai
import json
import os

# supply your API key however you choose
openai.api_key = os.environ["open_api_key"]


def auto_data_analysis(data):
    messages = [{"role": "system",
                 "content": "あなたは優秀なデータ分析者です。与えられたデータに対して分析を行ってください。"},
                {"role": "user",
                 "content": """データの分析を行ってください。groupbyで集約を行い、それに対する可視化が行える分析が良いです。
        どのカラムで集約するかなどを分析内容に基づいて考えてください。
        今回のデータは以下です
    \n\n""" + data,
                 },
                ]
    functions = [
        {
            "name": "auto_data_analysis",
            "description": "読み込んだデータをもとにデータ分析の例を作成する関数。結果は日本語で返す。結果はpandasとplotlyで可視化する。",
            "parameters": {
                "type": "object",
                "required": [
                    "analysis_title",
                    "analysis_description",
                    "agg_by",
                    "agg_num",
                    "agg_type",
                    "graph_type",
                    "x_column",
                    "y_column",
                    "insight_hint",
                ],
                "properties": {
                    "analysis_title": {
                        "type": "string",
                        "description": "分析のタイトル。可視化の際に用いる値なども加味して決定してください。",
                    },
                    "analysis_description": {
                        "type": "string",
                        "description": "分析の説明。詳しく。",
                    },
                    "insight_hint": {
                        "type": "string",
                        "description": "どのような観点でデータを見ると示唆が得られそうかの助言。",
                    },
                    "graph_type": {
                        "type": "string",
                        "description": "可視化の際に用いるグラフのタイプ。棒グラフならbar、折れ線グラフならlineと返す",
                        "enum": ["bar", "line"],
                    },
                    "x_column": {
                        "type": "string",
                        "description": "可視化の際に用いるグラフのx軸の値。元データにある値でお願いします。",
                    },
                    "y_column": {
                        "type": "string",
                        "description": "可視化の際に用いるグラフのy軸の値。元データにある値でお願いします。",
                    },
                    "detail": {
                        "type": "string",
                        "description": "可視化の際に更に細分化するときに使用。もし使わない場合には空白を返してください",
                    },
                    "agg_type": {
                        "type": "string",
                        "description": "可視化の際に用いる集約の方法。例 : mean、sum",
                        "enum": ["mean", "sum", "max", "min"],
                    },
                    "agg_num": {
                        "type": "string",
                        "description": "可視化の際に用いる集約する値。groupby(agg_by)[agg_num]となるイメージです。",
                    },
                    "agg_by": {
                        "type": "string",
                        "description": "可視化の際に用いる集約の単位。複数の値で集約する場合にはカンマ区切りで返してください。groupby(agg_by)[agg_num]となるイメージです",
                    },
                },
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=1.5,
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )

    response_message = response["choices"][0]["message"]
    print("res_message ==== ")
    print(response_message)
    print("res_message =====")

    if response_message.get("function_call"):
        function_args = json.loads(
            response_message["function_call"]["arguments"])
        return function_args
    else:
        return "error"
