import streamlit as st

def model_about():
    st.title("🩺 Disease Prediction Models")
    st.write("""
    Welcome to the **Disease Prediction App**! This application leverages the power of **machine learning** to help predict diseases based on your symptoms.

    ### 🌟 Models Used in the App:
    We use an ensemble of four advanced machine learning models to provide you with the most accurate predictions. Here's a breakdown of the models:

    - **🌳 XGBoost**: A highly efficient implementation of gradient boosting, known for its performance in handling structured/tabular data. It's fast, accurate, and widely used in data science competitions.
    - **⚡ LightGBM**: Another powerful variant of gradient boosting, optimized for speed and large datasets. It handles categorical features and missing values better than most other models.
    - **📈 SVM (Support Vector Machine)**: A robust algorithm that excels in high-dimensional data spaces, perfect for classifying complex datasets with precision.
    - **🐱 CatBoost**: Specifically designed for datasets with categorical features, reducing the need for extensive preprocessing. It’s one of the best models for tabular data with categorical variables.

    ### 🛠️ Model Development Process:
    #### 1. **📊 Dataset Creation**:
    - A comprehensive dataset was prepared with various **symptoms** as features and corresponding **diseases** as the target label.
    - The target column (diseases) was **encoded** into numeric labels to make it suitable for machine learning.
    - Preprocessing techniques were applied to ensure the dataset was clean, consistent, and ready for training.

    #### 2. **🧠 Model Training**:
    - Each of the four models was trained on the dataset using the symptoms as features and disease labels as the target.
    - Models were trained with specific hyperparameters and evaluated to find the best configuration for prediction.

    #### 3. **🤖 Ensemble Learning**:
    - To improve the accuracy of predictions, we combine the predictions of all four models.
    - **Why ensemble?** Each model has unique strengths, and by combining their outputs, we maximize the chances of an accurate prediction. The app calculates the **mode** (most frequent prediction) from the four models as the final prediction.

    #### 4. **📈 Model Evaluation**:
    - After training, the models were rigorously evaluated using **external datasets**. 
    - Splitting the data into **training, validation, and testing sets** ensured that the models perform well on unseen data.
    - We checked the models' **accuracy, precision, and recall** to ensure robust predictions.

    #### 5. **💾 Model Saving and Deployment**:
    - Once trained, the models were saved using **Joblib** for easy reloading during deployment.
    - Models are stored in a directory and loaded at runtime when you input your symptoms.
    - This app loads the models in the backend and combines their predictions to give the final disease outcome.

    ### 🤖 Integration with Groq AI and Langgraph:
    To enhance the functionality of our app, we've integrated Groq AI using the **Langgraph** framework. Here’s how:

    - **Langgraph Framework**: We used the Langgraph framework to build a dynamic graph-based workflow for processing and interpreting the input symptoms. This allows for sophisticated processing and integration with AI models.
    - **Groq AI**: Groq AI provides advanced capabilities for generating user-friendly descriptions and advice based on the predictions made by our machine learning models. This integration helps in creating more informative and actionable outputs.
    - **Model Integration**: The Langgraph framework seamlessly integrates with the machine learning models, enabling us to manage data flow and predictions efficiently. The AI-driven advice and descriptions are dynamically generated using Groq AI, enhancing the user experience by providing personalized insights and guidance.

    ### 🚀 Model Integration with Streamlit:
    The app allows you to enter your symptoms through this user-friendly **Streamlit** interface, which then processes the input through the machine learning models. Here’s how the app works:
    
    - You input your **symptoms**.
    - The app runs the input through the models to make predictions.
    - The **combined output** of the models gives you the most accurate disease prediction.

    ### 🏅 Why this Approach?
    By using a combination of advanced machine learning models and making their predictions **collective**, we can provide **higher accuracy** and **reliability** in diagnosing potential diseases. The app not only helps predict common conditions but also includes rare and less frequent diseases.

    We hope this app can assist you in understanding potential health issues based on the symptoms you input. Always consult with a healthcare professional for a proper diagnosis! 😊
    """)

# To display the content on the Streamlit page
model_about()
