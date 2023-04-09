import openai
import pandas as pd


class OpenAI_API:
    def __init__(self, api_key):
        self.api_key = api_key

    def __enter__(self):
        openai.api_key = self.api_key

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def open_ai_response(question: str, dataframe: pd.DataFrame) -> str:
    prompt = f'''{question}
    \n
    [dataframe]
    \n{dataframe}'''
    model_engine = "text-davinci-003"

    response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1000,
    )

    answer = response.choices[0].text.strip()
    print(prompt)

    return answer
