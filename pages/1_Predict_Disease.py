import streamlit as st
import numpy as np
import pandas as pd
from AI_ML import entry_point, predict_disease, symptoms_list
import streamlit.components.v1 as com

# Function to set the background image
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://img.freepik.com/free-photo/top-view-tensiometer-checking-blood-pressure_23-2150456065.jpg?t=st=1726185540~exp=1726189140~hmac=1239f086d5d0dee40a5f394a4568315b2db847f0234d9c1f503202ed000f54ac&w=740");
            background-size: cover; /* Cover the entire page */
            background-repeat: no-repeat; /* Do not repeat the image */
            background-attachment: fixed; /* Keep the image fixed while scrolling */
            background-position: center; /* Center the image */
            
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def predict_disease_page():
    set_background()  # Call the function to set the background image

    # Create a container for the UI elements
    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            com.iframe("https://lottie.host/embed/e977d988-97a3-401f-aa70-b5909e09b94e/y6WCoJ6vXt.json")

        with col2:
            st.title('Disease Prediction')

    # Create two tabs: one for manual input and another for text description input
    tabs = st.tabs(["🌡️ Manual Symptom Input", "📝 Text Description Input"])

    # --- Manual Symptom Input Tab ---
    with tabs[0]:
        st.header("🩹 Select Symptoms")
        st.write("Please select the symptoms you're experiencing:")

        # Initialize session state for pop-up visibility
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = False

        # Create a form for symptom input
        with st.form(key='symptom_form', clear_on_submit=True):
            # Create a dictionary to store symptom inputs
            symptoms_input = {}

            # Split symptoms into three columns for compact display
            columns = st.columns(3)

            # Assign each symptom input to a selectbox in three columns
            for idx, symptom in enumerate(symptoms_list):
                col = columns[idx % 3]  # Cycle through columns
                # Display "Yes" and "No" in the frontend, map to 1 and 0 in the backend
                user_input = col.selectbox(f"{symptom.replace('_', ' ').capitalize()}", ("No", "Yes"))
                # Map "Yes" to 1 and "No" to 0
                symptoms_input[symptom] = 1 if user_input == "Yes" else 0

            # Button to predict disease
            submit_button = st.form_submit_button(label='🔍 Predict Disease')
            
            # Initialize predicted_disease
            predicted_disease = None

            # Check if the submit button was pressed
            if submit_button:
                # Get the sum of all inputs (i.e., number of symptoms selected)
                selected_symptoms_count = sum(symptoms_input.values())

                if selected_symptoms_count == 0:
                    # Alert the user if no symptoms are selected
                    st.warning("⚠️ Please select more than one symptom to proceed.")
                elif selected_symptoms_count < 10:
                    # Alert the user if fewer than 10 symptoms are selected
                    st.warning("⚠️ Please select at least 10 symptoms for a more accurate prediction.")
                else:
                    # Call the prediction function (passing symptoms as values) if conditions are met
                    predicted_disease = predict_disease(symptoms_input)

                    # Set the popup visibility to True
                    st.session_state.show_popup = True

            # Display a modal-like experience using st.expander
            if st.session_state.show_popup:
                with st.expander("🧠 See Predicted Disease", expanded=True):
                    Disease_prediction1 = entry_point('predicted_disease', predicted_disease)
                    
                    # Display result creatively with emojis
                    st.markdown(f"### 🩺 **Predicted Disease**: **{Disease_prediction1['predicted_disease']}**")
                    st.markdown(f"📜 **Description**: {Disease_prediction1['description']}")
                    st.markdown(f"🚑 **Advice**: {Disease_prediction1['advice']}")
                    st.markdown(f"🔍 **Important Note**: {Disease_prediction1['note']}")

    # --- Text Description Input Tab ---
    with tabs[1]:
        st.header("📝 Provide a Symptom Description")
        st.write("Please provide a text description of your symptoms:")

        # Create a form for the text description input
        with st.form(key='description_form', clear_on_submit=True):
            # Input box for user to provide symptom description
            symptom_description = st.text_area("Enter your symptoms", placeholder="Describe your symptoms...")

            # Button to predict disease based on text input
            submit_description = st.form_submit_button(label="🔍 Predict from Description")

        # Check if the submit button was pressed
        if submit_description:
            if not symptom_description.strip():
                st.warning("⚠️ Please provide a description of your symptoms.")
            else:
                # Call the entry_point function to process the text description
                Disease_prediction2 = entry_point('userinput', symptom_description)
                
                # Display result creatively with emojis
                st.markdown(f"### 🩺 **Predicted Disease**: **{Disease_prediction2['predicted_disease']}**")
                st.markdown(f"📜 **Description**: {Disease_prediction2['description']}")
                st.markdown(f"🚑 **Advice**: {Disease_prediction2['advice']}")
                st.markdown(f"🔍 **Important Note**: {Disease_prediction2['note']}")

if __name__ == "__main__":
    predict_disease_page()