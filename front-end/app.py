import streamlit as st
from home_page import home_page
from about_us_page import About_Page
class App:
    def __init__(self):
        about_page = About_Page()
    def main():
        col1, col2 = st.columns([1, 2])

        # Add image to the top-left corner
        with col1:
            image = st.sidebar.image("/Users/testvagrant/Baganna/hackathon-project/front-end/images/jv.jpg", use_column_width=False, width=80)

        caption_text = "Junior Vagrants"
        with col2:
            st.sidebar.markdown(f'<div style="float: left; margin-right: auto; margin-top: auto; font-size:15px;">{caption_text}</div>', unsafe_allow_html=True)

        st.sidebar.title("Navigation")
        pages = ["Home", "About Us"]
        choice = st.sidebar.selectbox("Go to", pages)

        if choice == "Home":
            home_page()
        elif choice == "About Us":
            About_Page().about_page()

if __name__ == "__main__":
     main()