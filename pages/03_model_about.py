import streamlit as st

def model_about():
    st.title("About the Models")
    st.write("""
    This app uses four models: XGBoost, LightGBM, SVM, and CatBoost for disease prediction.
    The app combines their predictions to give the best possible result.
    """)
    if st.button("🔙 Back to Homepage"):
        st.session_state.page = 'homepage'

model_about()
