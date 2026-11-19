# 🛡️ Cybersecurity Intrusion Data Warehouse and Attack Analysis Using Data Mining

An intelligent cybersecurity intrusion detection system that combines **Data Warehousing, OLAP Analysis, Machine Learning, Feature Selection, and Explainable AI (XAI)** to classify network traffic as **Attack or Normal**.

The project uses the **NSL-KDD dataset** to analyze network traffic, compare machine learning algorithms, identify important features, and provide interactive predictions through a Streamlit web application.

---

## 📌 Project Overview

Cyberattacks such as Denial of Service (DoS), Probe, Remote to Local (R2L), and User to Root (U2R) can affect the availability, confidentiality, and integrity of computer networks.

This project develops a data-driven intrusion detection prototype using data mining and machine learning techniques.

The system performs the following operations:

- Collects and preprocesses NSL-KDD network traffic data.
- Constructs a data warehouse using fact and dimension tables.
- Performs OLAP operations for analytical exploration.
- Compares five machine learning classification algorithms.
- Selects important features using Mutual Information.
- Trains a Random Forest classification model.
- Uses SHAP for explainable AI.
- Provides an interactive Streamlit web application.

## 🎯 Objectives

- Analyze network intrusion data using data mining techniques.
- Design a structured cybersecurity data warehouse.
- Perform Roll-Up, Drill-Down, Slice, and Dice operations.
- Compare different machine learning algorithms.
- Identify important network traffic features.
- Improve classification performance through feature selection.
- Explain model predictions using SHAP.
- Develop an interactive web-based intrusion detection application.

## 🏗️ System Architecture

```text
             NSL-KDD Dataset
                    |
                    v
             Data Preprocessing
                    |
                    v
          Data Warehouse Construction
                    |
                    v
              OLAP Analysis
                    |
                    v
             Feature Selection
             (Mutual Information)
                    |
                    v
            Machine Learning Models
                    |
                    v
             Model Evaluation
                    |
                    v
       Random Forest - Top 5 Features
                    |
                    v
             SHAP Explainability
                    |
                    v
          Model Serialization
                    |
                    v
             Streamlit Web App
                    |
                    v
          Attack / Normal Prediction
```

## 📊 Dataset Information

**Dataset:** NSL-KDD

The NSL-KDD dataset is a benchmark dataset used for network intrusion detection research. It contains network connection records with traffic characteristics and corresponding labels.

| Dataset | Records | Features/Columns |
|---|---:|---:|
| Training Dataset | 125,973 | 43 |
| Testing Dataset | 22,543 | 43 |

### Training Dataset Distribution

| Category | Number of Records |
|---|---:|
| Normal | 67,343 |
| Attack | 58,630 |
| DoS | 45,927 |
| Probe | 11,656 |
| R2L | 995 |
| U2R | 52 |

The application performs binary classification:

- **Attack**
- **Normal**

Dataset source: [NSL-KDD Dataset – Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/nsl.html)

## 🗄️ Data Warehouse Design

The project implements a data warehouse using fact and dimension tables.

| Table | Rows | Columns |
|---|---:|---:|
| DIM_ATTACK | 23 | 3 |
| DIM_PROTOCOL | 3 | 2 |
| DIM_NETWORK | 334 | 3 |
| DIM_TIME | 125,973 | 5 |
| FACT_INTRUSION | 125,973 | 10 |

### OLAP Operations

The following OLAP operations are implemented:

1. **Roll-Up:** Summarizes detailed attack records into higher-level categories.
2. **Drill-Down:** Explores summarized information at a more detailed level.
3. **Slice:** Filters records based on a selected dimension.
4. **Dice:** Filters records using multiple conditions.

These operations support analytical exploration of network intrusion records.

*Note: The time dimension uses generated analytical time values and does not represent actual network event timestamps.*

## 🤖 Machine Learning Algorithms

Five classification algorithms are evaluated:

1. Decision Tree
2. Random Forest
3. Support Vector Machine (Linear SVM)
4. Logistic Regression
5. Naive Bayes

### Algorithm Comparison

| Algorithm | Accuracy | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|
| Decision Tree | 80.55% | 84.79% | 80.55% | 80.48% |
| Random Forest | 79.51% | 84.59% | 79.51% | 79.36% |
| Linear SVM | 74.36% | 80.81% | 74.36% | 73.95% |
| Logistic Regression | 72.92% | 79.92% | 72.92% | 72.39% |
| Naive Bayes | 45.03% | 72.34% | 45.03% | 30.30% |

*The above values are from the initial comparison using the selected 16-feature configuration.*

## 🔍 Feature Selection

Mutual Information is used to identify the most informative features for intrusion classification.

### Selected Top 5 Features

| Feature | Description |
|---|---|
| `src_bytes` | Bytes sent from source to destination |
| `service` | Network service used by the connection |
| `dst_bytes` | Bytes sent from destination to source |
| `same_srv_rate` | Rate of connections to the same service |
| `diff_srv_rate` | Rate of connections to different services |

### Random Forest Feature Comparison

| Configuration | Accuracy | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|
| All 16 Features | 79.51% | 84.59% | 79.51% | 79.36% |
| Top 5 Features | **82.05%** | **85.59%** | **82.05%** | **82.03%** |

<details>
<summary><b>View best model classification report</b></summary>

| Class | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| Attack | 0.96 | 0.71 | 0.82 | 12,833 |
| Normal | 0.72 | 0.96 | 0.82 | 9,710 |
| Accuracy | — | — | 0.82 | 22,543 |
| Macro Average | 0.84 | 0.84 | 0.82 | 22,543 |
| Weighted Average | 0.86 | 0.82 | 0.82 | 22,543 |

Confusion Matrix:

```text
                 Predicted
               Attack  Normal

Actual Attack   9164    3669
Actual Normal    378    9332
```

</details>

## 🧠 Explainable AI Using SHAP

SHAP (SHapley Additive exPlanations) is used to interpret the predictions of the trained Random Forest model.

It helps explain how individual input features contribute to the model's output.

The application displays feature-contribution visualizations to improve the interpretability of Attack and Normal predictions.

## 💻 Streamlit Web Application

The project includes an interactive web application developed using Streamlit.

### Application Features

- Interactive network traffic input form.
- Service selection dropdown.
- Source and destination byte inputs.
- Same-service and different-service rate inputs.
- Random Forest-based Attack/Normal prediction.
- Prediction probability display.
- SHAP feature explanation chart.
- Model information and performance metrics.

### Input Features

| Input | Type |
|---|---|
| Source Bytes | Numerical |
| Service | Categorical |
| Destination Bytes | Numerical |
| Same Service Rate | Numerical |
| Different Service Rate | Numerical |

### Example Workflow

1. Open the Streamlit application.
2. Enter the network traffic characteristics.
3. Select the required network service.
4. Submit the input.
5. View the predicted class.
6. Examine the SHAP explanation chart.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and evaluation |
| Matplotlib | Data visualization |
| SHAP | Model explainability |
| Streamlit | Web application development |
| Joblib | Model serialization |
| Google Colab | Model development and experimentation |
| Git | Version control |
| GitHub | Source code hosting |
| Streamlit Community Cloud | Web application deployment |

## 📁 Project Structure

```text
Cybersecurity-Intrusion-Detection/
│
├── app.py
│
├── requirements.txt
│
├── intrusion_model/
│   ├── random_forest_model.pkl
│   ├── selected_features.pkl
│   ├── categorical_encoders.pkl
│   └── target_encoder.pkl
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Bhargav-918/Cybersecurity-Intrusion-Detection.git
```

### 2. Navigate to the Project Directory

```bash
cd Cybersecurity-Intrusion-Detection
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Streamlit Application

```bash
python -m streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 📦 Requirements

The project dependencies are listed in `requirements.txt`.

```text
streamlit
pandas
numpy
scikit-learn
joblib
shap
matplotlib
```

## ☁️ Deployment

The application can be deployed using Streamlit Community Cloud.

Deployment steps:

1. Push the project to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in using GitHub.
4. Select the project repository.
5. Select the `main` branch.
6. Set the main file path to `app.py`.
7. Click Deploy.

After successful deployment, the application becomes accessible through a Streamlit-hosted URL.

**Live Application:** Add your deployed Streamlit URL here after successful deployment.

## 🚀 Future Enhancements

- Multi-class attack classification.
- Live network traffic monitoring.
- Integration with packet-capture tools.
- Improved detection of less frequent attack categories.
- Evaluation using newer cybersecurity datasets.
- Real-time intrusion alerts.
- Interactive attack analytics dashboard.
- Downloadable intrusion analysis reports.
- Enhanced model explainability.

## ⚠️ Limitations

- The model is trained and evaluated using the NSL-KDD benchmark dataset.
- The application performs binary classification rather than identifying individual attack types.
- Users manually enter traffic features; live packet capture is not implemented.
- The model may miss some attack records, as reflected in the confusion matrix.
- SHAP explanations describe model behavior and do not prove the actual cause of an attack.
- The project is an academic demonstration and is not a replacement for production security monitoring.

## 🎓 Project Information

**Project Title:** Cybersecurity Intrusion Data Warehouse and Attack Analysis Using Data Mining

**Domain:** Cybersecurity, Data Warehousing, Data Mining, Machine Learning

**Dataset:** NSL-KDD

**Best Model:** Random Forest – Top 5 Features

**Test Accuracy:** 82.05%

**Application Framework:** Streamlit

**Repository:** [GitHub – Cybersecurity Intrusion Detection](https://github.com/Bhargav-918/Cybersecurity-Intrusion-Detection)

---

## 👨‍💻 Author

**Bhargav Reddy**

B.Tech – Computer Science and Engineering

Interested in Artificial Intelligence, Machine Learning, and Cybersecurity.

---

⭐ If you find this project useful, consider giving the repository a star!
