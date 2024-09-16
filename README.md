# Disease Prediction Application

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Application Flow](#application-flow)
  - [Background Setup](#background-setup)
  - [Symptom Input Options](#symptom-input-options)
    - [Manual Symptom Input](#manual-symptom-input)
    - [Text Description Input](#text-description-input)
    - [Voice Input](#voice-input)
  - [Disease Prediction](#disease-prediction)
    - [Machine Learning Model Prediction](#machine-learning-model-prediction)
- [Pages and Functionality](#pages-and-functionality)
  - [Welcome Page](#welcome-page)
  - [Predict Disease Page](#predict-disease-page)
  - [Exploratory Analysis Page](#exploratory-analysis-page)
  - [About Page](#about-page)
- [Models and External Libraries](#models-and-external-libraries)
- [Dependencies](#dependencies)
- [License](#license)

---

## Overview
The **Disease Prediction Application** is a web-based tool that uses machine learning models to predict potential diseases based on user input. Users can input symptoms in three ways: manually selecting symptoms, entering a text description, or using voice input. The app then leverages various machine learning models to make predictions and provides disease descriptions, along with general advice.

---

## Features
- **Three Input Modes:**
  - **Manual Symptom Selection:** Choose symptoms from a predefined list.
  - **Text Description Input:** Enter a plain text description of symptoms.
  - **Voice Input:** Record voice for symptom input, automatically transcribed to text.
- **Multiple Model Predictions:** The app uses an ensemble of machine learning models (XGBoost, LightGBM, SVM, and CatBoost) to ensure accurate predictions.
- **AI-Powered Descriptions:** After disease prediction, AI generates a user-friendly description of the disease and provides general advice.
- **Responsive UI:** The app is designed with a clean and adaptable interface for both desktop and mobile devices.

---

## Technologies Used
- **Python**: Backend logic and machine learning model integration.
- **Streamlit**: Frontend for creating the web-based user interface.
- **Scikit-learn**: For machine learning model development and evaluation.
- **LightGBM**: A gradient boosting framework used in disease prediction.
- **XGBoost**: Another gradient boosting library for performance in predictions.
- **SVM**: Support vector machine model for classification tasks.
- **CatBoost**: A high-performance boosting algorithm used for disease prediction.
- **LangChain**: Used for natural language processing with AI models (Groq API) for extracting symptoms from user descriptions.
- **faster-whisper**: Transcription of voice inputs into text.
- **Pydub**: Audio processing and segmentation for voice inputs.
- **Joblib**: Model serialization and deserialization for fast loading.

---

## Application Flow

### Background Setup
The app allows you to customize its background with an image, which can be modified through the `set_background()` function in the codebase.

### Symptom Input Options
The application provides three different methods for inputting symptoms:

#### Manual Symptom Input
- Go to the "Manual Symptom Input" tab.
- A dropdown of predefined symptoms allows users to select "Yes" or "No."
- Users must choose at least **10 symptoms** to initiate disease prediction.

#### Text Description Input
- Go to the "Text Description Input" tab.
- Enter a description of your symptoms (minimum 5 words).
- The description will be parsed by AI to extract relevant symptoms.

#### Voice Input
- Go to the "Voice Input" tab.
- Record a voice description of symptoms. The AI will transcribe and extract symptoms from your voice recording.

---

### Disease Prediction

Once symptoms are provided, the machine learning models use the data to predict the most likely disease based on the symptom set.

#### Machine Learning Model Prediction
The application utilizes an ensemble of four machine learning models:
1. **XGBoost (best_xgb_model)**: A decision-tree-based ensemble model.
2. **LightGBM (best_lgb_model)**: A gradient-boosting framework designed for large datasets.
3. **Support Vector Machine (svm_model)**: A supervised learning model for classification.
4. **CatBoost (cat_model)**: An algorithm that handles categorical features well.

Each model predicts the disease, and the most frequent prediction among the models is returned as the final output. The models work with encoded symptoms, where each symptom is represented as a 1 (present) or 0 (absent) in the input.

**Prediction Workflow Example**:
1. Symptoms are processed into a format readable by the models.
2. All models (XGBoost, LightGBM, SVM, and CatBoost) predict the disease based on input.
3. The most frequent disease predicted by the models is selected as the final output.
4. The predicted disease is passed to an AI model (Groq API), which generates a description of the disease and offers general advice.

---

## Pages and Functionality


## Welcome Page

The welcome page provides an introduction to the disease prediction app and guides users on how to interact with the various features.

![Welcome Page](images/welcome.jpeg)

---

## Predict Disease Page

This is the core functionality of the app. Users can predict diseases based on symptoms they input through three methods:

### 1. **Manual Symptom Input**

Users can manually select symptoms from a predefined list to make predictions.

![Manual Input](images/manualInput.jpeg)

### 2. **Text Input Symptom Description**

Users can enter a free-text description of their symptoms, which is analyzed using the NLP model to extract relevant symptoms.

![Text Input](images/textInput.jpeg)

### 3. **Voice Input Symptom Description**

Users can use voice input to describe their symptoms, and the system will automatically convert speech to text and make a prediction.

![Voice Input](images/voiceInput.jpeg)

---

### 4. **Disease Prediction and AI Explanation**

Once the prediction is made, the model provides the predicted disease, and the AI explains the disease in a user-friendly way. This includes a simple description of the disease and advice to seek medical attention.

![Model Prediction with AI Explanation](images/predictedMalaria.jpeg)

---

## Exploratory Data Analysis Page

This page provides insights into the dataset used to train the machine learning models. Users can explore various statistics, charts, and visualizations.

![EDA Page](images/eda.jpeg)

---

## About Page

The About Page explains the purpose of the app, its underlying technology stack, and offers additional details about the dataset and models used.

![About Page](images/about.jpeg)


---

## Models and External Libraries
- **WhisperModel (faster-whisper)**: Converts voice input into text for symptom extraction.
- **LangChain**: AI-based language processing to identify symptoms from textual descriptions.
- **Pydub**: Used for audio file processing.
- **XGBoost, LightGBM, SVM, CatBoost**: Machine learning models used to predict diseases.

---

## Dependencies
The application requires several Python libraries for its functionality, including:
- **Streamlit**
- **faster-whisper**
- **pydub**
- **joblib**
- **XGBoost**
- **LightGBM**
- **Scikit-learn**
- **LangChain**
  
Refer to `requirements.txt` for the full list of dependencies.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
