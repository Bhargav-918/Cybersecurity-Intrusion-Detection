
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="CyberShield | Intrusion Detection",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------
# LOAD SAVED MODEL ARTIFACTS
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "intrusion_model"

@st.cache_resource
def load_artifacts():
    model = joblib.load(
        MODEL_DIR / "random_forest_model.pkl"
    )
    features = joblib.load(
        MODEL_DIR / "selected_features.pkl"
    )
    encoders = joblib.load(
        MODEL_DIR / "categorical_encoders.pkl"
    )
    target_encoder = joblib.load(
        MODEL_DIR / "target_encoder.pkl"
    )
    explainer = shap.TreeExplainer(model)

    return model, features, encoders, target_encoder, explainer

try:
    model, features, encoders, target_encoder, explainer = load_artifacts()
except Exception as exc:
    st.error(
        "Could not load the saved model files. "
        "Check that all four .pkl files exist in the "
        "intrusion_model folder and that package versions "
        "are compatible."
    )
    st.exception(exc)
    st.stop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🛡️ CyberShield")
st.subheader("Cybersecurity Intrusion Detection System")
st.write(
    "Analyze selected network traffic characteristics "
    "using a machine-learning model trained on NSL-KDD."
)

st.info(
    "This is a research demonstration using five selected "
    "features. It is not a live network monitor and should "
    "not be used as the sole basis for security decisions."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("About the Model")
st.sidebar.write("**Algorithm:** Random Forest")
st.sidebar.write("**Dataset:** NSL-KDD")
st.sidebar.write("**Selected features:** 5")
st.sidebar.write("**Test accuracy:** 82.05%")
st.sidebar.write("**Weighted F1 score:** 0.8203")
st.sidebar.caption(
    "Metrics are from the existing notebook evaluation; "
    "they are not a guarantee for new traffic."
)

# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------
st.header("Network Traffic Input")
st.write("Enter the characteristics of one network connection.")

service_names = list(encoders["service"].classes_)

with st.form("traffic_form"):
    col1, col2 = st.columns(2)

    with col1:
        src_bytes = st.number_input(
            "Source bytes",
            min_value=0,
            value=0,
            step=1,
            help="Number of data bytes sent from the source."
        )

        service = st.selectbox(
            "Network service",
            options=service_names,
            index=(
                service_names.index("http")
                if "http" in service_names else 0
            )
        )

        dst_bytes = st.number_input(
            "Destination bytes",
            min_value=0,
            value=0,
            step=1,
            help="Number of data bytes sent to the destination."
        )

    with col2:
        same_srv_rate = st.number_input(
            "Same-service rate",
            min_value=0.0,
            max_value=1.0,
            value=0.50,
            step=0.01,
            format="%.2f",
            help="Rate of connections to the same service."
        )

        diff_srv_rate = st.number_input(
            "Different-service rate",
            min_value=0.0,
            max_value=1.0,
            value=0.10,
            step=0.01,
            format="%.2f",
            help="Rate of connections to different services."
        )

    submitted = st.form_submit_button(
        "Analyze Traffic",
        type="primary",
        use_container_width=True
    )

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if submitted:
    try:
        service_encoder = encoders["service"]

        if service not in service_encoder.classes_:
            st.error("The selected service is not supported.")
            st.stop()

        service_encoded = int(
            service_encoder.transform([service])[0]
        )

        # Keep column names and order identical to training.
        input_values = {
            "src_bytes": int(src_bytes),
            "service": service_encoded,
            "dst_bytes": int(dst_bytes),
            "same_srv_rate": float(same_srv_rate),
            "diff_srv_rate": float(diff_srv_rate)
        }

        input_df = pd.DataFrame(
            [[input_values[f] for f in features]],
            columns=features
        )

        predicted_encoded = int(model.predict(input_df)[0])
        predicted_label = str(
            target_encoder.inverse_transform(
                np.array([predicted_encoded])
            )[0]
        )

        st.divider()
        st.header("Prediction Result")

        result_col, details_col = st.columns([1, 1])

        with result_col:
            if predicted_label == "Attack":
                st.error("⚠️ Prediction: Attack")
                st.write(
                    "The model classified this input as attack traffic."
                )
            else:
                st.success("✅ Prediction: Normal")
                st.write(
                    "The model classified this input as normal traffic."
                )

        with details_col:
            probabilities = model.predict_proba(input_df)[0]
            class_probabilities = {}

            for encoded_class, probability in zip(
                model.classes_, probabilities
            ):
                label = target_encoder.inverse_transform(
                    np.array([int(encoded_class)])
                )[0]
                class_probabilities[str(label)] = float(probability)

            st.write("**Model probability scores**")
            for label in ["Attack", "Normal"]:
                if label in class_probabilities:
                    st.write(
                        f"{label}: "
                        f"{class_probabilities[label] * 100:.2f}%"
                    )
                    st.progress(class_probabilities[label])

        st.caption(
            "These are model probability scores, not necessarily "
            "calibrated real-world probabilities."
        )

        # --------------------------------------------------
        # SHOW INPUT
        # --------------------------------------------------
        with st.expander("View encoded model input"):
            st.dataframe(input_df, use_container_width=True)

        # --------------------------------------------------
        # SHAP EXPLANATION
        # --------------------------------------------------
        st.divider()
        st.header("Explainable AI — SHAP")
        st.write(
            "This chart shows how the selected features influenced "
            "the model output for this individual prediction. "
            "Positive and negative values indicate direction relative "
            "to the explainer's output baseline."
        )

        shap_result = explainer.shap_values(input_df)
        predicted_class_index = list(model.classes_).index(
            predicted_encoded
        )

        if isinstance(shap_result, list):
            row_shap = np.asarray(
                shap_result[predicted_class_index]
            )[0]
        else:
            shap_array = np.asarray(shap_result)

            if shap_array.ndim == 3:
                # Typical shape: samples x features x classes
                row_shap = shap_array[
                    0, :, predicted_class_index
                ]
            elif shap_array.ndim == 2:
                row_shap = shap_array[0]
            else:
                raise ValueError(
                    f"Unexpected SHAP output shape: {shap_array.shape}"
                )

        explanation_df = pd.DataFrame({
            "Feature": features,
            "Input value": [
                input_values[f] for f in features
            ],
            "SHAP value": row_shap
        })

        explanation_df["Absolute impact"] = (
            explanation_df["SHAP value"].abs()
        )
        explanation_df = explanation_df.sort_values(
            "Absolute impact", ascending=True
        )

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.barh(
            explanation_df["Feature"],
            explanation_df["SHAP value"]
        )
        ax.axvline(0, linewidth=1)
        ax.set_xlabel("SHAP value")
        ax.set_title(
            f"Feature contributions for predicted class: "
            f"{predicted_label}"
        )
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.write("**Feature contribution details**")
        st.dataframe(
            explanation_df[
                ["Feature", "Input value", "SHAP value"]
            ].sort_values(
                "SHAP value",
                key=lambda series: series.abs(),
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "SHAP explains model behavior, not the true cause of "
            "a network event. Encoded service values are categorical "
            "labels, not numerical rankings."
        )

    except Exception as exc:
        st.error(
            "Prediction or explanation failed. Check the input, "
            "saved model artifacts, and package compatibility."
        )
        st.exception(exc)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption(
    "Academic project: Cybersecurity Intrusion Data Warehouse "
    "and Attack Analysis Using Data Mining | Dataset: NSL-KDD"
)
