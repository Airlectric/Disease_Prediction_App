import streamlit as st

def model_about():
    st.title("About the Models")
    st.write("""
    This app uses four models: XGBoost, LightGBM, SVM, and CatBoost for disease prediction.
    These models have been trained to predict diseases based on user symptoms.
    The app combines their predictions and uses the most common result as the final output.
    """)
    st.write("""
    - **XGBoost**: An efficient gradient boosting model that is optimized for both speed and accuracy.
    - **LightGBM**: A gradient boosting model that is optimized for speed and memory usage.
    - **SVM**: A Support Vector Machine model that works well with high-dimensional data.
    - **CatBoost**: A gradient boosting model designed to handle categorical data efficiently.
    """)
    if st.button("🔙 Back to Homepage"):
        st.session_state.page = 'homepage'
