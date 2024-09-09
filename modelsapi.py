import joblib
import numpy as np
import pandas as pd
from collections import Counter

# Load models
best_xgb = joblib.load('models/best_xgb_model.pkl')
best_lgb = joblib.load('models/best_lgb_model.pkl')
svm_model = joblib.load('models/svm_model.pkl')
cat_model = joblib.load('models/cat_model.pkl')

# List of disease classes
classes = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 
           'Peptic ulcer disease', 'AIDS', 'Diabetes ', 'Gastroenteritis', 'Bronchial Asthma', 
           'Hypertension ', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 
           'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'Hepatitis A', 
           'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 
           'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemorrhoids (piles)', 
           'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 
           'Hypoglycemia', 'Osteoarthritis', 'Arthritis', '(Vertigo) Paroxysmal Positional Vertigo', 
           'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']

def predict_disease(symptoms_input):
    """
    Predicts disease based on symptoms input using multiple models and selects the most frequent prediction.
    
    Args:
    symptoms_input (dict): Input symptoms as features.
    
    Returns:
    str: The predicted disease (most frequent prediction).
    """
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
    
    # Ensure the predicted index is valid
    if most_common_prediction >= len(classes):
        return 'Invalid index'
    return classes[most_common_prediction]
