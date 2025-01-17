from openai import OpenAI
import streamlit as st
import itertools
import os
from utils import check_password

st.set_page_config(
    page_title="Weaver - Edu AI",
    page_icon="🖍️",
    layout="centered"
)

st.title("🧠 + 🖍️ Weaver")
st.markdown("""
Fined tuned on publicly available online lesson plan data
*Created by Bradford Gill*
""")

if not check_password():  
    st.stop()
    
st.warning(
    """
    **Disclaimer:** This application is an AI prototype and is for demonstration purposes only.
    Results are likely to be inaccurate or incomplete. Use at your own discretion.
    """
)


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

num_standards = 6
standards = []

with st.form("input form"):
    # child interest 
    child_interest = st.text_input("What topic would engage this child?")
    
    cols = itertools.cycle(st.columns(2))
    for i_standard in range(num_standards):
        standards.append(next(cols).text_input(f'Standard # {i_standard + 1}'))
        
    num_problems = st.number_input("Number of problems in set", 1, 30, value=15, step=1)

    submitted = st.form_submit_button("Submit")
    
if submitted:
    standards_str = '\n'.join(standards)
    messages = [
        {
            'role': 'system',
            'content': '''
            You are an assistant used by teachers to create problem sets.
            ''',
        },
        {
            'role': 'user',
            'content': f'''
            My student is interested in {child_interest}.
            
            The standards needed in this problem set are: {standards_str}
            
            Please create a problem set work sheet with {num_problems} problems.
            ''',
        },
        
    ]
    
    stream = client.chat.completions.create(
            model='gpt-4',
            messages=messages,
            stream=True,
        )
    
    response = st.write_stream(stream)
    st.download_button(
        label="Download lesson plan as a .txt",
        data=response,              # The string content you want to download
        file_name="response.txt",   # The name of the file being downloaded
        mime="text/plain"           # The MIME type of the file
    )
    
    

