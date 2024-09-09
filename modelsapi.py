import joblib
import numpy as np
from scipy import stats
import pandas as pd

import xgboost as xgb
import lightgbm as lgb
from sklearn import svm
from catboost import CatBoostClassifier
from collections import Counter
from sklearn.preprocessing import LabelEncoder


best_xgb = joblib.load('models/best_xgb_model.pkl')
best_lgb = joblib.load('models/best_lgb_model.pkl')
svm_model = joblib.load('models/svm_model.pkl')
cat_model = joblib.load('models/cat_model.pkl')
label_encoder = LabelEncoder()


classes = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis',
           'Drug Reaction', 'Peptic ulcer disease', 'AIDS', 'Diabetes ',
           'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine',
           'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice',
           'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'Hepatitis A',
           'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
           'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
           'Dimorphic hemorrhoids (piles)', 'Heart attack', 'Varicose veins',
           'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
           'Osteoarthritis', 'Arthritis',
           '(Vertigo) Paroxysmal Positional Vertigo', 'Acne',
           'Urinary tract infection', 'Psoriasis', 'Impetigo']

# Function to make predictions based on symptoms
def predict_disease(symptoms_input, models, classes):
    """
    Predicts disease based on symptoms input using multiple models and selects the most frequent prediction.
    
    Args:
    symptoms_input (array-like): Input symptoms as features (must match the feature columns used in training).
    models (list): List of trained models.
    label_encoder (LabelEncoder): The label encoder used for encoding and decoding disease labels.
    
    Returns:
    str: The predicted disease (most frequent prediction).
    """
    
    # Convert symptoms input to DataFrame
    symptoms_df = pd.DataFrame([symptoms_input], columns=columns)
    
    model_predictions = []
    
    for model in models:
        # Make prediction
        prediction = model.predict(symptoms_df)
        
        # Flatten the prediction if it's an array
        if isinstance(prediction, np.ndarray):
            prediction = prediction.flatten()
        
        # Append the first element if prediction is an array
        if len(prediction) > 1:
            prediction = prediction[0]
        
        model_predictions.append(prediction)
    
    # Ensure all predictions are integers (if they are not already)
    model_predictions = [int(pred) for pred in model_predictions]
#     print(f"Model Predictions: {model_predictions}")

    # Find the most frequent prediction (mode)
    most_common_prediction = Counter(model_predictions).most_common(1)[0][0]  
    
        # Validate the index
    if most_common_prediction >= len(classes):
        predicted_disease = 'Invalid index'
    else:
        predicted_disease = classes[most_common_prediction]
    
    return predicted_disease

# Example usage:
if __name__ == "__main__":
   

    symptoms_input = {
        'itching': 0,
        'skin_rash': 0,
        'nodal_skin_eruptions': 1,
        'continuous_sneezing': 0,
        'shivering': 0,
        'chills': 0,
        'joint_pain': 1,
        'stomach_pain': 0,
        'acidity': 0,
        'ulcers_on_tongue': 0,
        'muscle_wasting': 0,
        'vomiting': 0,
        'burning_micturition': 0,
        'spotting_ urination': 0,
        'fatigue': 1,
        'weight_gain': 0,
        'anxiety': 0,
        'cold_hands_and_feets': 0,
        'mood_swings': 0,
        'weight_loss': 0,
        'restlessness': 0,
        'lethargy': 1,
        'patches_in_throat': 0,
        'irregular_sugar_level': 0,
        'cough': 0,
        'high_fever': 0,
        'sunken_eyes': 0,
        'breathlessness': 0,
        'sweating': 0,
        'dehydration': 0,
        'indigestion': 0,
        'headache': 0,
        'yellowish_skin': 0,
        'dark_urine': 0,
        'nausea': 0,
        'loss_of_appetite': 0,
        'pain_behind_the_eyes': 0,
        'back_pain': 0,
        'constipation': 0,
        'abdominal_pain': 0,
        'diarrhoea': 0,
        'mild_fever': 0,
        'yellow_urine': 0,
        'yellowing_of_eyes': 0,
        'acute_liver_failure': 0,
        'fluid_overload': 0,
        'swelling_of_stomach': 0,
        'swelled_lymph_nodes': 0,
        'malaise': 0,
        'blurred_and_distorted_vision': 0,
        'phlegm': 0,
        'throat_irritation': 0,
        'redness_of_eyes': 0,
        'sinus_pressure': 0,
        'runny_nose': 0,
        'congestion': 0,
        'chest_pain': 0,
        'weakness_in_limbs': 0,
        'fast_heart_rate': 0,
        'pain_during_bowel_movements': 0,
        'pain_in_anal_region': 0,
        'bloody_stool': 0,
        'irritation_in_anus': 0,
        'neck_pain': 0,
        'dizziness': 0,
        'cramps': 0,
        'bruising': 0,
        'obesity': 0,
        'swollen_legs': 0,
        'swollen_blood_vessels': 0,
        'puffy_face_and_eyes': 0,
        'enlarged_thyroid': 0,
        'brittle_nails': 0,
        'swollen_extremeties': 0,
        'excessive_hunger': 0,
        'extra_marital_contacts': 0,
        'drying_and_tingling_lips': 0,
        'slurred_speech': 0,
        'knee_pain': 0,
        'hip_joint_pain': 0,
        'muscle_weakness': 0,
        'stiff_neck': 0,
        'swelling_joints': 0,
        'movement_stiffness': 0,
        'spinning_movements': 0,
        'loss_of_balance': 0,
        'unsteadiness': 0,
        'weakness_of_one_body_side': 0,
        'loss_of_smell': 0,
        'bladder_discomfort': 0,
        'foul_smell_of urine': 0,
        'continuous_feel_of_urine': 0,
        'passage_of_gases': 0,
        'internal_itching': 0,
        'toxic_look_(typhos)': 0,
        'depression': 0,
        'irritability': 0,
        'muscle_pain': 0,
        'altered_sensorium': 0,
        'red_spots_over_body': 0,
        'belly_pain': 0,
        'abnormal_menstruation': 0,
        'dischromic _patches': 0,
        'watering_from_eyes': 0,
        'increased_appetite': 0,
        'polyuria': 0,
        'family_history': 0,
        'mucoid_sputum': 0,
        'rusty_sputum': 0,
        'lack_of_concentration': 0,
        'visual_disturbances': 0,
        'receiving_blood_transfusion': 0,
        'receiving_unsterile_injections': 0,
        'coma': 0,
        'stomach_bleeding': 0,
        'distention_of_abdomen': 0,
        'history_of_alcohol_consumption': 0,
        'fluid_overload.1': 0,
        'blood_in_sputum': 0,
        'prominent_veins_on_calf': 0,
        'palpitations': 0,
        'painful_walking': 0,
        'pus_filled_pimples': 0,
        'blackheads': 0,
        'scurring': 0,
        'skin_peeling': 0,
        'silver_like_dusting': 0,
        'small_dents_in_nails': 0,
        'inflammatory_nails': 0,
        'blister': 0,
        'red_sore_around_nose': 0,
        'yellow_crust_ooze': 0
    }

    columns = list(symptoms_input.keys())

    # Predict disease using the function
    predicted_disease = predict_disease(symptoms_input, [best_xgb, best_lgb, svm_model, cat_model], classes)
    print(f"Predicted Disease: {predicted_disease}")
