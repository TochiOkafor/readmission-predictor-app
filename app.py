import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Hospital Readmission Predictor",
    page_icon="🏥",
    layout="wide"
)

# ========== LOAD MODEL ARTEFACTS ==========
@st.cache_resource
def load_artefacts():
    model = joblib.load('models/xgboost_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    label_encoders = joblib.load('models/label_encoders.pkl')
    feature_columns = joblib.load('models/feature_columns.pkl')
    categorical_columns = joblib.load('models/categorical_columns.pkl')
    return model, scaler, label_encoders, feature_columns, categorical_columns

model, scaler, label_encoders, feature_columns, categorical_columns = load_artefacts()

# ========== HEADER ==========
st.title("🏥 Hospital Readmission Risk Predictor")
st.markdown("""
**A clinical decision support tool** — predicting 30-day readmission risk for
diabetic patients using machine learning.

⚠️ **This is a demonstration prototype for portfolio purposes. It is NOT a
medical device and must not be used to make actual clinical decisions.**
""")

st.divider()

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("📋 About This Model")
    st.markdown("""
    **Model:** XGBoost Classifier  
    **AUC-ROC:** 0.6752  
    **Training Data:** UCI Diabetes 130-US Hospitals (1999-2008)  
    **Sample Size:** 101,766 patient encounters

    ---

    **Intended Use:**  
    Educational demonstration of clinical AI deployment. Highlights how
    ML can support (not replace) clinical judgement.

    **Not Intended For:**
    - Actual patient care decisions
    - Clinical deployment
    - Regulatory submission

    ---

    📄 [View Full Model Card](https://github.com/TochiOkafor/readmission-predictor-app/blob/main/model_card.md)

    💻 [GitHub Repository](https://github.com/TochiOkafor/readmission-predictor-app)
    """)

# ========== MAIN FORM ==========
st.header("📝 Patient Information")
st.markdown("Enter patient details below to generate a readmission risk prediction.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Demographics")
    age = st.selectbox("Age Group",
                       options=['[0-10)', '[10-20)', '[20-30)', '[30-40)',
                                '[40-50)', '[50-60)', '[60-70)', '[70-80)',
                                '[80-90)', '[90-100)'])
    gender = st.selectbox("Gender", options=['Female', 'Male'])
    race = st.selectbox("Race",
                        options=['Caucasian', 'AfricanAmerican', 'Hispanic',
                                 'Asian', 'Other'])

with col2:
    st.subheader("Hospital Stay")
    time_in_hospital = st.slider("Time in Hospital (days)", 1, 14, 3)
    num_lab_procedures = st.slider("Number of Lab Procedures", 1, 100, 40)
    num_procedures = st.slider("Number of Procedures", 0, 6, 1)
    num_medications = st.slider("Number of Medications", 1, 80, 15)

with col3:
    st.subheader("Visit History")
    number_outpatient = st.slider("Outpatient Visits (past year)", 0, 40, 0)
    number_emergency = st.slider("Emergency Visits (past year)", 0, 76, 0)
    number_inpatient = st.slider("Inpatient Visits (past year)", 0, 21, 0)
    number_diagnoses = st.slider("Number of Diagnoses", 1, 16, 5)

st.divider()

col4, col5 = st.columns(2)

with col4:
    st.subheader("Clinical Details")
    max_glu_serum = st.selectbox("Max Glucose Serum",
                                 options=['None', 'Norm', '>200', '>300'])
    A1Cresult = st.selectbox("A1C Result",
                             options=['None', 'Norm', '>7', '>8'])
    change = st.selectbox("Medication Change", options=['No', 'Ch'])
    diabetesMed = st.selectbox("On Diabetes Medication", options=['No', 'Yes'])

with col5:
    st.subheader("Insulin Status")
    insulin = st.selectbox("Insulin", options=['No', 'Steady', 'Up', 'Down'])
    metformin = st.selectbox("Metformin", options=['No', 'Steady', 'Up', 'Down'])

st.divider()

# ========== PREDICT ==========
if st.button("🔮 Generate Prediction", type="primary", use_container_width=True):

    input_data = {
        'race': race,
        'gender': gender,
        'age': age,
        'time_in_hospital': time_in_hospital,
        'num_lab_procedures': num_lab_procedures,
        'num_procedures': num_procedures,
        'num_medications': num_medications,
        'number_outpatient': number_outpatient,
        'number_emergency': number_emergency,
        'number_inpatient': number_inpatient,
        'number_diagnoses': number_diagnoses,
        'max_glu_serum': max_glu_serum,
        'A1Cresult': A1Cresult,
        'change': change,
        'diabetesMed': diabetesMed,
        'insulin': insulin,
        'metformin': metformin,
    }

    input_df = pd.DataFrame(columns=feature_columns)
    for col in feature_columns:
        if col in input_data:
            input_df.loc[0, col] = input_data[col]
        else:
            input_df.loc[0, col] = 'No' if col in categorical_columns else 0

    for col in categorical_columns:
        if col in input_df.columns:
            le = label_encoders[col]
            try:
                input_df[col] = le.transform(input_df[col].astype(str))
            except ValueError:
                input_df[col] = 0

    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0, 1]

    st.divider()
    st.header("🎯 Prediction Result")

    result_col1, result_col2 = st.columns([1, 2])

    with result_col1:
        if probability >= 0.5:
            st.error(f"### ⚠️ Elevated Risk\n\n**{probability*100:.1f}%** predicted readmission risk")
        elif probability >= 0.3:
            st.warning(f"### ⚡ Moderate Risk\n\n**{probability*100:.1f}%** predicted readmission risk")
        else:
            st.success(f"### ✅ Lower Risk\n\n**{probability*100:.1f}%** predicted readmission risk")

    with result_col2:
        fig, ax = plt.subplots(figsize=(8, 2))
        colour = 'red' if probability >= 0.5 else 'orange' if probability >= 0.3 else 'green'
        ax.barh([0], [probability], color=colour)
        ax.barh([0], [1], color='lightgray', alpha=0.3, zorder=0)
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
        ax.set_title('Readmission Risk Score')
        ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='Alert threshold')
        ax.legend(loc='upper right')
        st.pyplot(fig)

    st.subheader("📖 What This Means")
    st.markdown(f"""
    The model estimates a **{probability*100:.1f}% probability** that this patient
    will be readmitted within 30 days of discharge.

    **Contextual notes:**
    - The overall readmission rate in the training data was ~11%
    - Predictions above 50% suggest higher-than-typical risk
    - This is a **screening indicator, not a diagnosis**
    - Clinical judgement should always take precedence

    **Recommended actions (illustrative only):**
    - High risk: Consider enhanced discharge planning and follow-up
    - Moderate risk: Standard follow-up with attention to patient education
    - Low risk: Standard discharge protocols
    """)

    st.warning("""
    ⚠️ **Reminder:** This tool is a demonstration prototype for portfolio purposes.
    It is not validated for clinical use and must not inform actual patient care decisions.
    """)

# ========== FOOTER ==========
st.divider()
st.caption("Model version: 1.0 | Built by [Tochukwu Okafor](https://linkedin.com/in/contacttochukwuedith)")