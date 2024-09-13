import streamlit as st
import numpy as np
import pandas as pd
from AI_ML import entry_point, predict_disease, symptoms_list
import streamlit.components.v1 as com
from streamlit_mic_recorder import mic_recorder
from faster_whisper import WhisperModel
import os
from pydub import AudioSegment
import concurrent.futures
import re

# Function to set the background image
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://img.freepik.com/free-photo/top-view-tensiometer-checking-blood-pressure_23-2150456081.jpg?t=st=1726198628~exp=1726202228~hmac=2fbc29e3cdc86ca113989382de63ca38d314cc290b2a9a7b8e4b6559e16614a5&w=740");
            background-size: cover; 
            background-repeat: no-repeat; 
            background-attachment: fixed; 
            background-position: center;
        }

        /* Styling for the text boxes with background */
        .styled-box {
            background-color: rgba(255, 255, 255, 0.85); /* Light background with opacity */
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            color: black;
        }
        
        /* Adjust for dark mode */
        @media (prefers-color-scheme: dark) {
            .styled-box {
                background-color: rgba(0, 0, 0, 0.75); /* Darker background with opacity for dark mode */
                color: white;
            }
        }

        /* Ensure headings and paragraph text are always white */
        h1, h2, h3, h4, h5, h6, p {
            color: white !important; /* Force white text for headings and paragraphs */
        }

        /* Optional: add shadow to improve readability */
        h1, h2, h3, h4, h5, h6, p {
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.75); /* Add subtle shadow for better readability */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Initialize Whisper model (only executed once!)
@st.cache_resource()
def load_whisper_model():
    return WhisperModel("small")

whisper_model = load_whisper_model()

def split_audio_file(audio_file, segment_length_ms=60000):
    """Split audio file into segments of specified length."""
    audio = AudioSegment.from_file(audio_file)
    segments = []
    for i in range(0, len(audio), segment_length_ms):
        segment = audio[i:i + segment_length_ms]
        segment_file = f"segment_{i // segment_length_ms}.wav"
        segment.export(segment_file, format="wav")
        segments.append(segment_file)
    return segments

def transcribe_segment(segment):
    segment_transcription = whisper_model.transcribe(segment, language="en")
    transcription_text = " ".join([s.text for s in segment_transcription[0]])
    os.remove(segment)
    return transcription_text

def process_audio_file(audio_file):
    segments = split_audio_file(audio_file)
    full_transcription = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(transcribe_segment, segment): segment for segment in segments}

        for future in concurrent.futures.as_completed(futures):
            transcription_text = future.result()
            full_transcription.append(transcription_text)

    os.remove(audio_file)
    return " ".join(full_transcription)

def validate_description(description):
    """
    Validate the input description to ensure it meets criteria for processing.
    Args:
    description (str): The text description of symptoms.

    Returns:
    bool: True if the description is valid, False otherwise.
    str: Feedback message if the description is invalid.
    """
    if not description.strip():
        return False, "⚠️ The description is empty. Please provide more information about your symptoms."

    if len(description.split()) < 5:  # Example: require at least 5 words
        return False, "⚠️ The description is too short. Please provide a more detailed description of your symptoms."

    if re.search(r'\b(?:\d{1,3}(?:,\d{3})*|(?:[1-9]\d*))\b', description):
        return False, "⚠️ The description seems to contain numeric values. Please provide a clear description of your symptoms."

    return True, ""

def predict_disease_page():
    set_background()

    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            com.iframe("https://lottie.host/embed/e977d988-97a3-401f-aa70-b5909e09b94e/y6WCoJ6vXt.json")

        with col2:
            st.title('Disease Prediction')

    tabs = st.tabs(["🌡️ Manual Symptom Input", "📝 Text Description Input", "🎤 Voice Input"])

    # --- Manual Symptom Input Tab ---
    with tabs[0]:
        st.header("🩹 Select Symptoms")
        st.write("Please select the symptoms you're experiencing:")

        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = False

        with st.form(key='symptom_form', clear_on_submit=True):
            symptoms_input = {}
            columns = st.columns(3)

            for idx, symptom in enumerate(symptoms_list):
                col = columns[idx % 3]
                user_input = col.selectbox(f"{symptom.replace('_', ' ').capitalize()}", ("No", "Yes"))
                symptoms_input[symptom] = 1 if user_input == "Yes" else 0

            submit_button = st.form_submit_button(label='🔍 Predict Disease')
            predicted_disease = None

            if submit_button:
                selected_symptoms_count = sum(symptoms_input.values())

                if selected_symptoms_count == 0:
                    st.warning("⚠️ Please select more than one symptom to proceed.")
                elif selected_symptoms_count < 10:
                    st.warning("⚠️ Please select at least 10 symptoms for a more accurate prediction.")
                else:
                    predicted_disease = predict_disease(symptoms_input)
                    st.session_state.show_popup = True

            if st.session_state.show_popup:
                with st.expander("🧠 See Predicted Disease", expanded=True):
                    Disease_prediction1 = entry_point('predicted_disease', predicted_disease)
                    st.markdown(f"""
                        <div class='styled-box'>
                            <h4>🩺 Predicted Disease: {Disease_prediction1['predicted_disease']}</h4>
                            <p>📜 Description: {Disease_prediction1['description']}</p>
                            <p>🚑 Advice: {Disease_prediction1['advice']}</p>
                            <p>🔍 Important Note: {Disease_prediction1['note']}</p>
                        </div>
                    """, unsafe_allow_html=True)

    # --- Text Description Input Tab ---
    with tabs[1]:
        st.header("📝 Provide a Symptom Description")
        st.write("Please provide a text description of your symptoms:")

        with st.form(key='description_form', clear_on_submit=True):
            symptom_description = st.text_area("Describe your symptoms", placeholder="Describe your symptoms...")

            # Button to predict disease based on text input
            submit_description = st.form_submit_button(label="🔍 Predict from Description")

            if submit_description:
                is_valid, feedback_message = validate_description(symptom_description)
                if not is_valid:
                    st.warning(feedback_message)
                else:
                    Disease_prediction2 = entry_point('userinput', symptom_description)
                    st.markdown(f"""
                        <div class='styled-box'>
                            <h4>🩺 Predicted Disease: {Disease_prediction2['predicted_disease']}</h4>
                            <p>📜 Description: {Disease_prediction2['description']}</p>
                            <p>🚑 Advice: {Disease_prediction2['advice']}</p>
                            <p>🔍 Important Note: {Disease_prediction2['note']}</p>
                        </div>
                    """, unsafe_allow_html=True)

    # --- Voice Input Tab ---
    with tabs[2]:
        st.header("🎤 Voice Input")
        st.write("Record your symptoms and we will transcribe them for you:")

        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:  
            audio_data = mic_recorder(
                start_prompt="🎙️ Start Recording",
                stop_prompt="⏹️ Stop Recording",
                key="mic_recorder",
                use_container_width=True 
            )

        transcription = ""
        if audio_data:
            st.success("Recording finished! Processing audio...")
            audio_file = "output.wav"
            with open(audio_file, "wb") as f:
                f.write(audio_data['bytes'])

            transcription = process_audio_file(audio_file)

            if transcription.strip():
                st.write("🎧 Transcription complete!")
            else:
                st.warning("⚠️ Transcription failed or result is empty. Please try again.")

        with st.form(key='voice_form', clear_on_submit=True):
            symptom_description = st.text_area("Transcription of your symptoms", value=transcription)

            submit_voice_description = st.form_submit_button(label="🔍 Predict from Voice Input")

            if submit_voice_description:
                is_valid, feedback_message = validate_description(symptom_description)
                if not is_valid:
                    st.warning(feedback_message)
                else:
                    Disease_prediction3 = entry_point('userinput', symptom_description)
                    st.markdown(f"""
                        <div class='styled-box'>
                            <h4>🩺 Predicted Disease: {Disease_prediction3['predicted_disease']}</h4>
                            <p>📜 Description: {Disease_prediction3['description']}</p>
                            <p>🚑 Advice: {Disease_prediction3['advice']}</p>
                            <p>🔍 Important Note: {Disease_prediction3['note']}</p>
                        </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    predict_disease_page()
