import streamlit as st

def main():
    
    # Set up the page title and subtitle
    st.markdown("""
    <div style='text-align: center;'>
        <h1>🌟 Welcome to the Disease Prediction App</h1>
        <p>Our app uses advanced machine learning models to predict diseases based on your symptoms. 
        Enter your symptoms, and we'll provide you with the most accurate prediction using four powerful models: XGBoost, LightGBM, SVM, and CatBoost.</p>
    </div>
        """, unsafe_allow_html=True)

    st.sidebar.title("Welcome")
    st.sidebar.info("🗺️ Navigate your way! Select a page above to continue.")

    # Add a description and images/icons for each section
    st.write("### Explore the App")

    # Use a 2-column layout for a more engaging homepage
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://img.freepik.com/premium-photo/doctor-using-technology-provide-healthcare_14117-1060619.jpg?w=900", use_column_width=True)
        st.subheader("🔍 Predict Disease")
        st.write("""
        Enter your symptoms in the "Predict Disease" section to get predictions from our advanced models. 
        Experience how our ensemble of machine learning models can provide insights into potential health issues based on your symptoms.
        """)
        st.write("👈🏻 **Check the sidebar to start predicting!**")

    with col2:
        st.image("https://imageio.forbes.com/specials-images/imageserve/64d24936a0c9451a52034c63/Training-machine-learning-model-concept/960x0.jpg?format=jpg&width=1440", use_column_width=True)
        st.subheader("📖 About Models")
        st.write("""
        Discover more about the powerful models that drive our predictions. 
        Learn about XGBoost, LightGBM, SVM, and CatBoost, and understand how they work together to provide accurate disease predictions.
        """)
        st.write("👈🏻 **Check the sidebar for more information!**")

    # Add a creative section for user engagement
    st.write("### 💡 Empowering Your Health Journey")
    st.write("""
    We believe in empowering you with the knowledge to make informed health decisions. 
    Our app is designed to be user-friendly and informative, helping you navigate your health journey with confidence. 
    Feel free to explore and utilize the tools we provide for better health insights!
    """)

if __name__ == "__main__":
    main()