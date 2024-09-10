import streamlit as st

def homepage():
    st.title("🌟 Welcome to the Disease Prediction App")
    st.write("""
    Our app uses advanced machine learning models to predict diseases based on your symptoms. 
    Enter your symptoms, and we’ll provide you with the most accurate prediction using four powerful models: 
    XGBoost, LightGBM, SVM, and CatBoost.
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Predict Disease"):
            st.session_state.page = 'predict_disease'

    with col2:
        if st.button("📖 Learn More About the Models"):
            st.session_state.page = 'model_about'

    # Daily health tips
    st.write("### 🏥 Daily Health Tip")
    daily_health_tips()
