# LifeLine AI

## AI-Powered Emergency Triage & Hospital Load Balancing

LifeLine AI is an AI-assisted emergency decision-support system designed to help assess patient severity and recommend a suitable hospital based on emergency requirements and available hospital capacity.

The system collects patient vital signs and clinical symptoms, uses an IBM AutoAI machine learning model to predict the patient's triage level, and then provides a hospital recommendation based on the predicted severity and hospital capabilities.

## Live Demo

[Open LifeLine AI](https://lifeline-ai-gyyxvd5spk7durvw8nss9q.streamlit.app/)

## Project Workflow

Patient Information
        ↓
Vital Signs & Clinical Symptoms
        ↓
IBM AutoAI Triage Model
        ↓
Triage Level Prediction
        ↓
Prediction Confidence
        ↓
Hospital Suitability Analysis
        ↓
Hospital Recommendation
        ↓
Hospital Load Balancing

## Features

- Patient emergency assessment interface
- Vital sign input
- Clinical symptom input
- AI-based triage classification
- Prediction confidence display
- Hospital recommendation
- Emergency and ICU capability checking
- Hospital available-bed comparison
- Hospital load-balancing view
- Interactive Streamlit interface
- IBM AutoAI model integration
- Cloud deployment

## Triage Classification

The AI model predicts one of the following triage levels:

- HIGH
- MEDIUM
- LOW

The predicted triage level is used to determine which hospitals are suitable for the patient.

## Hospital Recommendation

The hospital recommendation considers:

- Predicted triage level
- Emergency care availability
- ICU availability
- Available beds
- Distance

For example, HIGH-level cases require hospitals with emergency services and ICU availability.

> Note: The hospital information used in this prototype is demonstration data and does not represent live hospital capacity or real-time hospital availability.

## Machine Learning

The triage prediction model was developed using IBM watsonx.ai AutoAI.

The selected AutoAI pipeline uses a tree-based classification approach for predicting the patient's triage level.

### Input Features

The model uses the following patient features:

- Age
- Heart rate
- Systolic blood pressure
- Diastolic blood pressure
- SpO₂
- Temperature
- Respiratory rate
- Chest pain
- Breathing difficulty
- Consciousness

### Target

`triage_level`

## Technology Stack

### Frontend
- Streamlit

### Backend / Programming
- Python
- Requests

### Machine Learning
- IBM watsonx.ai
- IBM AutoAI
- Machine Learning Classification

### Deployment
- Streamlit Community Cloud
- IBM Cloud / watsonx.ai

### Version Control
- Git
- GitHub

## Project Structure

```text
LifeLine-AI/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md

Disclaimer
LifeLine AI is an educational and research prototype intended to demonstrate AI-assisted emergency triage and hospital recommendation.
It is not a medical diagnosis system and should not be used as a substitute for qualified medical professionals or real emergency services.
Hospital capacity and availability shown in the prototype are demonstration data and are not real-time information.

Future Improvements
- Integration with real-time hospital bed availability
- Real geographic distance and routing
- Real-time emergency department capacity
- Ambulance integration
- Explainable AI for triage predictions
- Patient history integration
- Real-time hospital load monitoring
- Secure healthcare data integration
- Improved model validation using larger clinical datasets

Author
Spandana Basava Kulal
B.Tech – Computer Science and Engineering (AI & ML)
License

This project is intended for educational and research purposes.
