import pickle
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

st.title('Heart Disease Prediction')

# Load model
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = pickle.load(open(os.path.join(BASE_DIR, 'gboost_model.pkl'), 'rb'))

# Input features
Age            = st.number_input('Age',            min_value=20,  max_value=100, value=25)
RestingBP      = st.number_input('Resting BP',     min_value=0,   max_value=250, value=100)
Cholesterol    = st.number_input('Cholesterol',    min_value=0,   max_value=650, value=100)
MaxHR          = st.number_input('MaxHR',          min_value=60,  max_value=250, value=100)
Oldpeak        = st.number_input('Oldpeak',        min_value=-3,  max_value=7,   value=1)
FastingBS      = st.selectbox('FastingBS',         (1, 0))
Gender         = st.selectbox('Gender',            ('M', 'F'))
ChestPainType  = st.selectbox('ChestPainType',     ('ATP', 'NAP', 'ASY', 'TA'))
RestingECG     = st.selectbox('RestingECG',        ('Normal', 'ST', 'LVH'))
ExerciseAngina = st.selectbox('ExerciseAngina',    ('N', 'Y'))
ST_Slope       = st.selectbox('ST_Slope',          ('Up', 'Flat', 'Down'))

# Encoding — Gender
Gender_M = 1 if Gender == 'M' else 0
Gender_F = 1 if Gender == 'F' else 0

# Encoding — ChestPainType
ChestPainType_ATP = 1 if ChestPainType == 'ATP' else 0
ChestPainType_NAP = 1 if ChestPainType == 'NAP' else 0
ChestPainType_ASY = 1 if ChestPainType == 'ASY' else 0
ChestPainType_TA  = 1 if ChestPainType == 'TA'  else 0

# Encoding — RestingECG
# ❌ Remove these
Gender_M = 1 if Gender == 'M' else 0
Gender_F = 1 if Gender == 'F' else 0

# ✅ Replace with
sex = 1 if Gender == 'M' else 0   # 1 = Male, 0 = Female


# ❌ Remove these
ExerciseAngina_Y = 1 if ExerciseAngina == 'Y' else 0
ExerciseAngina_N = 1 if ExerciseAngina == 'N' else 0

# ✅ Replace with
exerciseAngina = 1 if ExerciseAngina == 'Y' else 0   # 1 = Yes, 0 = No


# ❌ Fix this name
ChestPainType_ATP = 1 if ChestPainType == 'ATP' else 0

# ✅ Replace with
ChestPainType_ATA = 1 if ChestPainType == 'ATP' else 0  # model uses ATA

# RestingECG encoding  ← ADD THIS BLOCK
RestingECG_Normal = 1 if RestingECG == 'Normal' else 0
RestingECG_ST     = 1 if RestingECG == 'ST'     else 0
RestingECG_LVH    = 1 if RestingECG == 'LVH'    else 0

# ChestPainType encoding
ChestPainType_ATA = 1 if ChestPainType == 'ATP' else 0
ChestPainType_NAP = 1 if ChestPainType == 'NAP' else 0
ChestPainType_ASY = 1 if ChestPainType == 'ASY' else 0
ChestPainType_TA  = 1 if ChestPainType == 'TA'  else 0

# ST_Slope encoding
st_Slope_dict = {'Up': 0, 'Down': 1, 'Flat': 2}
st_Slope = st_Slope_dict[ST_Slope]

# Gender
sex = 1 if Gender == 'M' else 0

# ExerciseAngina
exerciseAngina = 1 if ExerciseAngina == 'Y' else 0
# Build DataFrame  ✅ removed undefined variables
input_features = pd.DataFrame({
    'Age':               [Age],
    'RestingBP':         [RestingBP],
    'Cholesterol':       [Cholesterol],
    'FastingBS':         [FastingBS],
    'MaxHR':             [MaxHR],
    'Oldpeak':           [Oldpeak],
    'sex':               [sex],               # ✅ fixed
    'exerciseAngina':    [exerciseAngina],     # ✅ fixed
    'RestingECG_LVH':    [RestingECG_LVH],
    'RestingECG_Normal': [RestingECG_Normal],
    'RestingECG_ST':     [RestingECG_ST],
    'ChestPainType_ASY': [ChestPainType_ASY],
    'ChestPainType_ATA': [ChestPainType_ATA],  # ✅ fixed from ATP
    'ChestPainType_NAP': [ChestPainType_NAP],
    'ChestPainType_TA':  [ChestPainType_TA],
    'st_Slope':          [st_Slope]
})

# Scaling  ✅ fixed missing () and arguments
scaler = StandardScaler()
input_features[['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']] = scaler.fit_transform(
    input_features[['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']]
)

# Prediction  ✅ fixed variable name
if st.button('Predict'):
    prediction = model.predict(input_features)
    if prediction[0] == 1:
        st.error('🚨 High Risk of Heart Disease')
    else:
        st.success('✅ Low Risk of Heart Disease')