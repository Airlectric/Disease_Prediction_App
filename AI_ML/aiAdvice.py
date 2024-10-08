from langchain_groq import ChatGroq
from langchain.agents import Tool
from langchain.tools.base import BaseTool
from langgraph.graph import Graph
import streamlit as st
from .modelsapi import symptoms_list, predict_disease

# Initialize AI model (Groq)
groq_api_key = st.secrets["general"]["GROQ_API_KEY"]

model = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    groq_api_key=groq_api_key,
)

import re

import re
from langchain_groq import ChatGroq

# Initialize AI model (Groq)
groq_api_key = st.secrets["general"]["GROQ_API_KEY"]

model = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    groq_api_key=groq_api_key,
)

def extract_symptoms_from_description(state):
    """
    This function processes a user's text description of symptoms. The AI parses 
    the description to identify which predefined symptoms are mentioned. It then 
    updates and organizes a dictionary (`symptoms_dict`) where each symptom from 
    the predefined list is set to either:
        - 1: if the symptom is present (i.e., mentioned in the user input),
        - 0: if the symptom is absent (i.e., not mentioned).

    The dictionary structure will match the format used in manual input processing,
    where each symptom is a key, and its value is either 0 or 1.

    Args:
    state (dict): A dictionary containing user input including the description of symptoms.
                  Expected format: {'symptoms_input': 'user provided text'}

    Returns:
    dict or None: A dictionary where keys are symptoms and values are 0 or 1, reflecting 
                  whether the symptom was mentioned in the user's description.
                  Returns None if no symptoms are matched or less than 10 are present.
    """
    # Get the symptoms description from the input state
    description = state['symptoms_input']

    # Initialize the symptoms dictionary with all symptoms set to 0 by default
    symptoms_dict = {symptom: 0 for symptom in symptoms_list}

    # Convert the user description to lowercase to ensure case-insensitive matching
    description = description.lower()

    # Use AI model to assist in extracting symptoms from the description
    ai_query = f"Identify symptoms from the following description: '{description}'. List the symptoms using words from the predefined list {symptoms_list}. If the description is gibberish or not sufficient send none null response."
    response = model.invoke(ai_query)
    
    # Extract symptom list from AI response and clean it
    ai_extracted_symptoms = response.content.split("*")  # Split by '*' since the output uses this for symptoms
    ai_extracted_symptoms = [symptom.strip().lower() for symptom in ai_extracted_symptoms if symptom.strip()]  # Clean the symptom strings

    print("\n[DEBUG] AI output:", ai_extracted_symptoms)  # Debugging output

    # Improve matching between the AI extracted symptoms and the predefined list
    for symptom in symptoms_list:
        symptom_clean = symptom.replace('_', ' ').lower()  # Handle underscores in the symptom names
        if symptom_clean in description or any(symptom_clean in ai_symptom for ai_symptom in ai_extracted_symptoms):
            symptoms_dict[symptom] = 1  # Mark the symptom as present in the dictionary

    # Count the number of symptoms marked as 1
    matched_symptoms_count = sum(symptoms_dict.values())

    # Debugging statement: print the dictionary to see what was updated
    # print("\n[DEBUG] Symptoms Dictionary after extraction:", symptoms_dict)
    # print(f"\n[DEBUG] Number of matched symptoms: {matched_symptoms_count}")

    # If no symptoms are matched or fewer than 10 symptoms are marked as 1, return None
    if matched_symptoms_count < 5:
        return None

    return symptoms_dict



# Step 3: AI describes disease and gives general advice
def describe_disease(predicted_disease):
    state = {'predicted_disease': predicted_disease, 'messages': []}

    # AI will describe the disease and give advice
    advice_query = f"""
    The user gave some symptoms to a machine learning model, and it predicted a disease.
    The predicted disease is: {state['predicted_disease']}.
    
    Please provide a description of this disease in a simple, user-friendly manner.
    Also, offer general advice to the user to seek medical help or go to a hospital for further diagnosis. Avoid giving specific medical treatment instructions. 
    """
    
    # Invoke the AI to generate a response
    response = model.invoke(advice_query)
    state['messages'].append(response.content)
    
    # Return the disease description and advice as a dictionary
    disease_description = {
        "predicted_disease": state['predicted_disease'],
        "description": response.content,
        "advice": "If you are experiencing symptoms related to this disease, please seek medical attention immediately. It's important to consult a healthcare professional for a proper diagnosis and treatment plan.",
        "note": "This information is generated by an AI model and should not replace professional medical advice."
    }
    
    return disease_description



# Langraph initialization
workflow = Graph()

# Add nodes for workflow
# workflow.add_node('symptoms_input', lambda state: state.update({'symptoms': symptoms}))
workflow.add_node('user_symptoms_input',extract_symptoms_from_description)
workflow.add_node('predict_disease', predict_disease)
workflow.add_node('describe_disease', describe_disease)

workflow.add_edge('user_symptoms_input', 'predict_disease')
workflow.add_edge('predict_disease', 'describe_disease')

workflow.set_entry_point('user_symptoms_input')
workflow.set_finish_point('describe_disease')

# Compile the workflow
predictDiseaseWorkflow = workflow.compile()

# Define the entry point function
def entry_point(input_type, input_value):
    if input_type == 'predicted_disease':
        # Skip the input functions and directly call describe_disease
        # state = {'predicted_disease': input_value, 'messages': []}  # Initialize state with predicted disease
        return describe_disease(input_value)
    elif input_type == 'userinput':
        # Extract symptoms from the entry
        # symptoms = extract_symptoms_from_description(input_value)
        
        # # Initialize state with extracted symptoms
        state = {'symptoms_input': input_value, 'messages': []}
        
        # Execute the workflow and get the final state
        final_state = predictDiseaseWorkflow.invoke(state)
        
        # Return the predicted disease from the final state
        return final_state