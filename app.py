import os
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LifeLine AI",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f5f8fc;
    }

    /* Main content width */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hero section */
    .hero-box {
        background: linear-gradient(
            135deg,
            #0759a5,
            #1687d4
        );
        padding: 35px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0, 80, 150, 0.18);
    }

    .hero-title {
        color: white;
        font-size: 42px;
        font-weight: 800;
        margin: 0;
    }

    .hero-subtitle {
        color: #eaf6ff;
        font-size: 18px;
        margin-top: 8px;
    }

    /* Section headings */
    h2, h3 {
        color: #123b5d;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #8493a1;
        font-size: 13px;
        padding-top: 25px;
        margin-top: 40px;
        border-top: 1px solid #dce5ed;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">LifeLine AI</div>
        <div class="hero-subtitle">
            AI-Powered Emergency Triage & Hospital Load Balancing
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.write(
    "Enter the patient's vital signs and clinical symptoms "
    "to obtain an AI-based emergency triage prediction "
    "and hospital recommendation."
)


# ============================================================
# PATIENT ASSESSMENT
# ============================================================

st.header("Patient Assessment")

st.write(
    "Provide the patient's current vital signs and clinical symptoms."
)


# ============================================================
# INPUT COLUMNS
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# VITAL SIGNS
# ============================================================

with col1:

    with st.container(border=True):

        st.subheader("🫀 Vital Signs")

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=45
        )

        heart_rate = st.number_input(
            "Heart Rate (bpm)",
            min_value=0,
            value=110
        )

        systolic_bp = st.number_input(
            "Systolic BP (mmHg)",
            min_value=0,
            value=90
        )

        diastolic_bp = st.number_input(
            "Diastolic BP (mmHg)",
            min_value=0,
            value=60
        )

        spo2 = st.number_input(
            "SpO₂ (%)",
            min_value=0.0,
            max_value=100.0,
            value=92.0
        )


# ============================================================
# CLINICAL SYMPTOMS
# ============================================================

with col2:

    with st.container(border=True):

        st.subheader("🩺 Clinical Symptoms")

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=25.0,
            max_value=45.0,
            value=38.5
        )

        respiratory_rate = st.number_input(
            "Respiratory Rate (/min)",
            min_value=0,
            value=24
        )

        chest_pain = st.selectbox(
            "Chest Pain",
            ["No", "Yes"]
        )

        breathing_difficulty = st.selectbox(
            "Breathing Difficulty",
            ["No", "Yes"]
        )

        consciousness = st.selectbox(
            "Consciousness",
            ["Unconscious", "Conscious"]
        )


# ============================================================
# IBM WATSONX CONFIGURATION
# ============================================================

API_KEY = os.getenv("IBM_API_KEY")

DEPLOYMENT_URL = (
    "https://eu-gb.ml.cloud.ibm.com/"
    "ml/v4/deployments/lifeline_ai_triage/"
    "predictions?version=2021-05-01"
)


# ============================================================
# GET IBM IAM TOKEN
# ============================================================

def get_iam_token():

    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": API_KEY,
            "grant_type":
                "urn:ibm:params:oauth:grant-type:apikey"
        }
    )

    response.raise_for_status()

    return response.json()["access_token"]


# ============================================================
# IBM TRIAGE PREDICTION
# ============================================================

def predict_triage():

    token = get_iam_token()

    fields = [
        "age",
        "heart_rate",
        "systolic_bp",
        "diastolic_bp",
        "spo2",
        "temperature",
        "respiratory_rate",
        "chest_pain",
        "breathing_difficulty",
        "consciousness"
    ]

    values = [[
        age,
        heart_rate,
        systolic_bp,
        diastolic_bp,
        spo2,
        temperature,
        respiratory_rate,
        chest_pain,
        breathing_difficulty,
        consciousness
    ]]

    payload = {
        "input_data": [
            {
                "fields": fields,
                "values": values
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.post(
        DEPLOYMENT_URL,
        json=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# DEMO HOSPITAL DATA
# ============================================================

hospitals = [

    {
        "name": "LifeLine Emergency Center",
        "level": "HIGH",
        "emergency": True,
        "icu": True,
        "available_beds": 8,
        "distance": 3.2
    },

    {
        "name": "CityCare Medical Center",
        "level": "HIGH",
        "emergency": True,
        "icu": True,
        "available_beds": 5,
        "distance": 5.1
    },

    {
        "name": "Community Health Hospital",
        "level": "MEDIUM",
        "emergency": True,
        "icu": False,
        "available_beds": 12,
        "distance": 2.4
    },

    {
        "name": "Green Valley Hospital",
        "level": "LOW",
        "emergency": False,
        "icu": False,
        "available_beds": 20,
        "distance": 4.8
    }

]


# ============================================================
# HOSPITAL RECOMMENDATION FUNCTION
# ============================================================

def recommend_hospital(triage_level):

    suitable_hospitals = []

    for hospital in hospitals:

        if triage_level == "HIGH":

            if hospital["emergency"] and hospital["icu"]:

                suitable_hospitals.append(hospital)

        elif triage_level == "MEDIUM":

            if hospital["emergency"]:

                suitable_hospitals.append(hospital)

        else:

            suitable_hospitals.append(hospital)


    if not suitable_hospitals:

        return None


    suitable_hospitals.sort(
        key=lambda x: (
            -x["available_beds"],
            x["distance"]
        )
    )

    return suitable_hospitals[0]


# ============================================================
# RUN AI ASSESSMENT BUTTON
# ============================================================

st.write("")

if st.button(
    "🚑 Run AI Emergency Assessment",
    type="primary"
):

    if not API_KEY:

        st.error(
            "IBM_API_KEY is not configured. "
            "Set your IBM Cloud API key before running the app."
        )

    else:

        try:

            # ====================================================
            # RUN IBM MODEL
            # ====================================================

            with st.spinner(
                "Analyzing patient data with LifeLine AI..."
            ):

                result = predict_triage()


            # ====================================================
            # EXTRACT PREDICTION
            # ====================================================

            prediction_data = result["predictions"][0]

            prediction_values = prediction_data["values"][0]

            prediction = prediction_values[0]

            probabilities = prediction_values[1]

            confidence = max(probabilities) * 100


            # ====================================================
            # AI ASSESSMENT RESULT
            # ====================================================

            st.divider()

            st.header("AI Assessment Result")

            st.write(
                "The deployed IBM AutoAI model has completed "
                "the emergency triage assessment."
            )


            # ====================================================
            # RESULT METRICS
            # ====================================================

            result_col1, result_col2, result_col3 = st.columns(3)


            with result_col1:

                if prediction == "HIGH":

                    st.error("🚨 HIGH RISK")

                elif prediction == "MEDIUM":

                    st.warning("⚠️ MEDIUM RISK")

                else:

                    st.success("✅ LOW RISK")


                st.caption("Triage Classification")


            with result_col2:

                st.metric(
                    "Model Confidence",
                    f"{confidence:.2f}%"
                )


            with result_col3:

                st.metric(
                    "AI Model",
                    "IBM AutoAI"
                )


            # ====================================================
            # CONFIDENCE BAR
            # ====================================================

            st.write("Confidence")

            st.progress(
                min(confidence / 100, 1.0)
            )


            # ====================================================
            # TRIAGE GUIDANCE
            # ====================================================

            if prediction == "HIGH":

                st.warning(
                    "HIGH-risk assessment: Emergency-capable care "
                    "with ICU support should be considered for this case."
                )

            elif prediction == "MEDIUM":

                st.info(
                    "MEDIUM-risk assessment: Evaluation at an "
                    "emergency-capable facility should be considered."
                )

            else:

                st.success(
                    "LOW-risk assessment: Standard medical evaluation "
                    "may be appropriate."
                )


            # ====================================================
            # HOSPITAL RECOMMENDATION
            # ====================================================

            st.divider()

            st.header("Hospital Recommendation")

            st.write(
                "Hospital selection considers triage requirements, "
                "emergency capability, ICU availability, available "
                "beds and distance."
            )


            recommended = recommend_hospital(prediction)


            if recommended:

                # ------------------------------------------------
                # RECOMMENDED HOSPITAL
                # ------------------------------------------------

                st.success(
                    f"🏥 Recommended Hospital: "
                    f"{recommended['name']}"
                )


                st.caption(
                    "Recommended facility based on the current "
                    "triage classification and available hospital capacity."
                )


                # ------------------------------------------------
                # HOSPITAL METRICS
                # ------------------------------------------------

                hospital_col1, hospital_col2 = st.columns(2)

                hospital_col3, hospital_col4 = st.columns(2)


                with hospital_col1:

                    st.metric(
                        "Available Beds",
                        recommended["available_beds"]
                    )


                with hospital_col2:

                    st.metric(
                        "Distance",
                        f"{recommended['distance']} km"
                    )


                with hospital_col3:

                    st.metric(
                        "ICU",
                        (
                            "Available"
                            if recommended["icu"]
                            else "Not Available"
                        )
                    )


                with hospital_col4:

                    st.metric(
                        "Emergency",
                        (
                            "Available"
                            if recommended["emergency"]
                            else "Not Available"
                        )
                    )


                # ------------------------------------------------
                # CAPABILITY INFORMATION
                # ------------------------------------------------

                if recommended["emergency"]:

                    st.success(
                        "✓ Emergency care capability available."
                    )


                if recommended["icu"]:

                    st.info(
                        "✓ ICU support available for the "
                        "recommended emergency facility."
                    )


                # ====================================================
                # HOSPITAL LOAD BALANCING
                # ====================================================

                st.divider()

                st.header("Hospital Load Balancing")

                st.write(
                    "Comparison of hospital capacity and "
                    "emergency-care capabilities."
                )


                hospital_table = []


                for hospital in hospitals:

                    hospital_table.append(
                        {
                            "Hospital":
                                hospital["name"],

                            "Available Beds":
                                hospital["available_beds"],

                            "Distance (km)":
                                hospital["distance"],

                            "Emergency":
                                (
                                    "Available"
                                    if hospital["emergency"]
                                    else "Not Available"
                                ),

                            "ICU":
                                (
                                    "Available"
                                    if hospital["icu"]
                                    else "Not Available"
                                ),

                            "Triage Level":
                                hospital["level"]
                        }
                    )


                st.dataframe(
                    hospital_table,
                    use_container_width=True,
                    hide_index=True
                )


                # ------------------------------------------------
                # DEMO DATA NOTE
                # ------------------------------------------------

                st.caption(
                    "Demo data: Hospital capacity, distance and "
                    "availability values are synthetic and are not "
                    "live hospital data."
                )


            else:

                st.error(
                    "No suitable hospital found in the available "
                    "hospital dataset."
                )


        except Exception as e:

            st.error(
                f"Prediction failed: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        LifeLine AI · AI-Powered Emergency Triage &
        Hospital Load Balancing
        <br><br>
        Decision-support prototype powered by IBM AutoAI.
    </div>
    """,
    unsafe_allow_html=True
)