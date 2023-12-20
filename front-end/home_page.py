import streamlit as st
import time
import sys
import ast 
sys.path.append("/Users/testvagrant/Desktop/junior-vagrants/backend/")
from model.assistant import Assistant

class Home_Page:
    def __init__(self):
        pass
    def home_page(self):
        # Input textbox with styling
        st.markdown("""
        <style>
            div.Widget.row-widget.stTextInput > div {
                width: 300px;
            }
        </style>
    """, unsafe_allow_html=True)
        input_text = st.text_input("Enter URL:", "")

        # Dropdown with styling
        st.markdown("""
        <style>
            div.Widget.row-widget.stSelectbox >div{
                width: 300px;
            }
        </style>
    """, unsafe_allow_html=True)
        tools = ["Select","Selenium", "PlayWright", "WebDriverIO"]
        selected_tool = st.selectbox("Select an tool:", tools)
        if selected_tool == "Selenium":
            languages = ["Select","Java", "JavaScript", "Python", "Ruby","CSharp","Kotlin"]
            selected_language = st.selectbox("Select an Language:", languages)
        elif selected_tool == "PlayWright":
            languages = ["Select","Java", "JavaScript", "Python", ".NET"]
            selected_language = st.selectbox("Select an Language:", languages)
        else:
            languages = ["Select", "JavaScript"]
            selected_language = st.selectbox("Select an Language:", languages)
        # Submit button with styling
        st.markdown("""
        <style>
            div.Widget.stButton > button {
                width: 150px;
                height: 40px;
                background-color: #4CAF51;
                color: white;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)
        if st.button("Generate Testcase"):
            if not input_text:
                st.warning("Please enter URL.")
            elif selected_tool == "Select":
                st.warning("Please select tool.")
            elif selected_language == "Select":
                st.warning("Please select language.")
            else:
                success_message = st.success("Wait for response")
                time.sleep(1)
                success_message.empty()

                #create assistant object
                assistant = Assistant()
                assistant.create_assistant(selected_language, selected_tool)
                response = assistant.generate_response(input_text)
                # Check if response is a list
                if isinstance(response, str):
                    json_string = response.replace("```json", "").replace("```", "")
                    json_list = ast.literal_eval(json_string)
                    
                    if isinstance(json_list, list):
                        for res in json_list:
                            st.write(res.get('description', ''))
                            st.code(res.get('testCase', ''))
                    else:
                        st.warning("Unexpected response format.")
                else:
                    st.warning("Unexpected response format.")