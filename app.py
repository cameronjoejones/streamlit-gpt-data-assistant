import streamlit as st
import pandas as pd
from api import OpenAI_API, open_ai_response
from question_bank import question_bank


st.set_page_config(page_title="ChatGPT Data Assistant", page_icon=":lemon:", layout="centered")

hide_menu_style = "<style> footer {visibility: hidden;} </style>"
st.markdown(hide_menu_style, unsafe_allow_html=True)


def run_app():
    api_key = st.secrets["api_key"]['open_ai']
    if api_key is None:
        st.error('API key not found. Please set the api_key in the .streamlit/secrets.toml file.')
    else:
        with OpenAI_API(api_key):
            st.title('📊 ChatGPT Data Assistant')
            upload_file = st.file_uploader("Upload your data file", type=['csv'])
            prompt_selected = st.selectbox('Select a prompt', list(question_bank.keys()))
            prompt = question_bank[prompt_selected]['question']
            st.write(prompt)


            submit = st.button('Generate response')
            
            if submit:
                with st.spinner('Generating response...'):            
                    if upload_file is not None:
                        df = pd.read_csv(upload_file)
                        prompt = question_bank[prompt_selected]['question']
                        answer = open_ai_response(prompt, df)
                        st.markdown('### Ouput:')
                        st.write(answer)
                        print(answer)
                    else:
                        st.error('Please upload a data file')
                        st.stop()


def sidebar():
    st.sidebar.title('About')
    st.sidebar.info('''
        This app uses the [OpenAI API](https://beta.openai.com/) to generate responses to questions about data files.
        ''')
    st.sidebar.title('Guide')
    st.sidebar.info('''
        1. Upload a data file in CSV format.
        2. Select a prompt from the dropdown menu.
        3. Click the "Generate response" button.
        ''')
    st.sidebar.title('Credits')
    st.sidebar.info('''
        This app was built by [Cameron Jones](https://www.cameronjones.co.uk/)
        ''')


if __name__ == '__main__':
    run_app()
    sidebar()