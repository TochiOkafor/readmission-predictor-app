# Model Card: Hospital Readmission Risk Predictor

## Model Details

- **Model Name:** Hospital Readmission Risk Predictor v1.0
- **Model Type:** Binary Classification (XGBoost)
- **Developer:** Tochukwu Okafor
- **Date:** 2025
- **Version:** 1.0
- **License:** MIT
- **Repository:** https://github.com/TochiOkafor/readmission-predictor-app

## Intended Use

### Primary Intended Use
Educational demonstration of clinical AI deployment methodology, illustrating:
- End-to-end ML pipeline development
- Model serialisation and web deployment
- Responsible AI documentation practices

### Intended Users
- Prospective employers evaluating portfolio work
- ML/AI engineers learning about model deployment
- Students studying responsible AI documentation

### Out-of-Scope Uses
This model must NOT be used for:
- Actual clinical decisions
- Patient care in any healthcare setting
- Regulatory submission or medical device claims
- Insurance or reimbursement decisions
- Any decision affecting real patient outcomes

## Factors

### Relevant Factors
- **Demographics:** Age, gender, race
- **Clinical:** Diabetes-related measurements, medications, procedures
- **Utilisation:** Prior emergency, outpatient, and inpatient visits

### Evaluation Factors
Performance was evaluated across the following subgroups:
- Race (6 categories)
- Gender (2 categories)
- Age (10 decade groups)

## Metrics

- **Primary Metric:** AUC-ROC = 0.6752
- **Accuracy:** 0.89
- **Precision (readmission class):** 0.49
- **Recall (readmission class):** 0.02
- **F1 (readmission class):** 0.04

### Decision Threshold
Default: 0.5 probability threshold. Alternative thresholds should be considered based on the operational trade-off between false positives (unnecessary interventions) and false negatives (missed at-risk patients).

## Training Data

- **Source:** UCI Machine Learning Repository — Diabetes 130-US Hospitals for years 1999-2008
- **Size:** 101,766 patient encounters
- **Timeframe:** 1999-2008
- **Population:** Diabetic patients across 130 US hospitals
- **Class balance:** 11% readmitted within 30 days, 89% not readmitted
- **License:** CC BY 4.0

## Evaluation Data

Held-out 20% test set from the same distribution, stratified by outcome.

## Ethical Considerations

### Fairness Assessment
A separate fairness audit ([Healthcare Fairness Audit repository](https://github.com/TochiOkafor/healthcare-fairness-audit)) revealed:
- **Age disparity:** Equalised Odds Difference of 0.21 — clinically significant
- **Race disparity:** Four of six racial groups received zero positive predictions
- **Gender:** Minimal disparity

These findings indicate the model performs unequally across demographic groups and would not be appropriate for real-world deployment without significant mitigation.

### Data Provenance Concerns
- Training data is from 1999-2008, potentially reflecting outdated clinical practices
- US healthcare system context may not generalise to UK NHS populations
- Original dataset does not capture social determinants of health

### Broader Impact
Deployment of imperfect readmission models in real healthcare settings could:
- Divert resources away from patients incorrectly flagged as low-risk
- Reinforce existing healthcare disparities if fairness issues are not addressed
- Undermine clinician trust if false alerts fatigue teams

## Caveats and Recommendations

### Known Limitations
- Low recall on readmitted class (2%) — misses most actual readmissions
- Trained on data over 15 years old
- Uses only US healthcare system patient data
- Does not include social determinants of health
- No calibration adjustment applied to output probabilities

### Recommendations for Real-World Use
Before any real deployment, this model would need:
1. Retraining on modern EHR data with appropriate privacy protections
2. Post-hoc calibration to align probabilities with true risk
3. Fairness constraints applied during training to reduce demographic disparity
4. Prospective clinical validation study
5. Regulatory review (MHRA in UK, FDA in US)
6. Clinician-in-the-loop workflow design
7. Ongoing monitoring for model drift

## Contact
For questions about this model or its documentation, contact via:
- LinkedIn: https://linkedin.com/in/contacttochukwuedith
- GitHub: https://github.com/TochiOkafor

---

*This Model Card follows the framework introduced by Mitchell et al. (2019) — "Model Cards for Model Reporting" (FAccT '19).*