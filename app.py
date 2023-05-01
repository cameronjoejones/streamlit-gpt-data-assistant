import streamlit as st
import pandas as pd
from api import OpenAI_API, open_ai_response
from question_bank import question_bank

def page_config():
    st.set_page_config(page_title="ChatGPT Data Assistant", page_icon="📊", layout="centered")
    hide_menu_style = "<style> footer {visibility: hidden;} </style>"
    st.markdown(hide_menu_style, unsafe_allow_html=True)


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
    st.text(" ")
    st.sidebar.markdown(
    """
    <a href="https://twitter.com/cameronjoejones" target="_blank" style="text-decoration: none;">
        <div style="display: flex; align-items: center;">
            <img src="https://abs.twimg.com/icons/apple-touch-icon-192x192.png" width="30" height="30">
            <span style="font-size: 16px; margin-left: 5px;">Follow me on Twitter</span>
        </div>
    </a>
    """, unsafe_allow_html=True
    )
    


def run_app():
    api_key = st.secrets["api_key"]['open_ai']
    if api_key is None:
        st.error('API key not found. Please set the api_key in the .streamlit/secrets.toml file.')
    else:
        with OpenAI_API(api_key):
            st.title('🤵🏻‍♂️ ChatGPT Data Assistant')

            example_data = st.checkbox('Use example data', value=False)

            if example_data == True:
                upload_file = r'input/example_data.csv'
                st.write(pd.read_csv(upload_file))

            elif example_data == False:
                upload_file = st.file_uploader("Upload your data file", type='csv')

            prompt_selected = st.selectbox('Select a prompt', list(question_bank.keys()))
            prompt = question_bank[prompt_selected]['question']
            st.write(prompt)
            submit = st.button('Generate response')

            
            if submit:
                with st.spinner('Generating response...'):            
                    if upload_file is not None:
                        if example_data == False:
                            if upload_file.name.endswith('.csv'):
                                df = pd.read_csv(upload_file)
                            elif upload_file.name.endswith('.xlsx') or upload_file.name.endswith('.xls'):
                                df = pd.read_excel(upload_file)
                        elif example_data == True:
                            df = pd.read_csv(upload_file)
                        
                        prompt = question_bank[prompt_selected]['question']
                        answer = open_ai_response(prompt, df)
                        st.markdown('### Ouput:')
                        st.write(answer)
                        # st.text_area(label='', value=answer, height=200)

                        print(answer)
                    else:
                        st.error('Please upload a data file')
                        st.stop()
                    return df
    

if __name__ == '__main__':
    page_config()
    run_app()
    sidebar()
