import streamlit as st
from homepage import homepage
from model_about import model_about
from predict_disease import predict_disease_page
from health_data import historical_health_data_page

def switch_page(page_name):
    st.session_state.page = page_name

if 'page' not in st.session_state:
    st.session_state.page = 'homepage'

def main():
    # Load and apply styles from styles.css
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page_selection = st.sidebar.radio(
        "Go to",
        ["Homepage", "Model About", "Predict Disease", "Health Data"]
    )

    # Update session state based on sidebar choice
    selected_page = page_selection.lower().replace(" ", "_")
    switch_page(selected_page)

    # Check which page is active and display content accordingly
    if st.session_state.page == 'homepage':
        homepage()
    elif st.session_state.page == 'model_about':
        model_about()
    elif st.session_state.page == 'predict_disease':
        predict_disease_page()
    elif st.session_state.page == 'health_data':
        historical_health_data_page()

if __name__ == '__main__':
    main()
