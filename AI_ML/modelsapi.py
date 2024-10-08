import joblib
import numpy as np
import pandas as pd
from collections import Counter
import joblib
import os

# Get the current file's directory
current_dir = os.path.dirname(__file__)

# Construct the full path to the model files
best_xgb_path = os.path.join(current_dir, 'models', 'best_xgb_model.pkl')
best_lgb_path = os.path.join(current_dir, 'models', 'best_lgb_model.pkl')
svm_model_path = os.path.join(current_dir, 'models', 'svm_model.pkl')
cat_model_path = os.path.join(current_dir, 'models', 'cat_model.pkl')
label_encoder_path = os.path.join(current_dir, 'models','label_encoder.joblib')

# Load the models
best_xgb = joblib.load(best_xgb_path)
best_lgb = joblib.load(best_lgb_path)
svm_model = joblib.load(svm_model_path)
cat_model = joblib.load(cat_model_path)
label_encoder = joblib.load(label_encoder_path)


symptoms_list = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing',
    'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 
    'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 
    'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 
    'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 
    'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 
    'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 
    'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 
    'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 
    'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 
    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 
    'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 
    'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 
    'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 
    'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 
    'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 
    'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 
    'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 
    'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 
    'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 
    'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 
    'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 
    'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 
    'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 
    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 
    'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 
    'altered_sensorium', 'red_spots_over_body', 'belly_pain', 
    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 
    'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 
    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 
    'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 
    'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 
    'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 
    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 
    'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 
    'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze'
]


# # List of disease classes
# classes = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 
#            'Peptic ulcer disease', 'AIDS', 'Diabetes ', 'Gastroenteritis', 'Bronchial Asthma', 
#            'Hypertension ', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 
#            'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'Hepatitis A', 
#            'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 
#            'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemorrhoids (piles)', 
#            'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 
#            'Hypoglycemia', 'Osteoarthritis', 'Arthritis', '(Vertigo) Paroxysmal Positional Vertigo', 
#            'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']


def predict_disease(symptoms_input, label_encoder =  label_encoder):
    """
    Predicts disease based on symptoms input using multiple models and selects the most frequent prediction.
    
    Args:
    symptoms_input (dict or None): Input symptoms as features. If None, it means the symptoms were insufficient.
    label_encoder (LabelEncoder): The label encoder used for encoding and decoding disease labels.
    
    Returns:
    str: The predicted disease (most frequent prediction) or an error message if symptoms are insufficient.
    """
    # Check if symptoms_input is None
    if symptoms_input is None:
        return "The symptom description is not sufficient, so no disease was predicted."

    models = [best_xgb, best_lgb, svm_model, cat_model]
    
    # Convert symptoms input to DataFrame
    symptoms_df = pd.DataFrame([symptoms_input], columns=symptoms_input.keys())
    
    model_predictions = []
    
    for model in models:
        prediction = model.predict(symptoms_df)
        if isinstance(prediction, np.ndarray):
            prediction = prediction.flatten()[0]
        model_predictions.append(int(prediction))
    
    # Find the most frequent prediction
    most_common_prediction = Counter(model_predictions).most_common(1)[0][0]
    
    # Use the label encoder to get the disease name from the predicted index
    predicted_disease = label_encoder.inverse_transform([most_common_prediction])[0]
    
    return predicted_disease
