
---

# ESG Portfolio Analytics Dashboard

## Overview

The ESG Portfolio Analytics Dashboard is a data-driven application that evaluates and ranks companies based on Environmental, Social, and Governance (ESG) metrics. It processes structured datasets, computes weighted ESG scores, and provides interactive insights to support investment decision-making.

---

## Features

* Multi-factor ESG scoring model (Environmental, Social, Governance)
* Data normalization using Scikit-learn (MinMaxScaler)
* Company ranking based on ESG scores
* Risk classification (Low, Medium, High)
* Interactive dashboard built with Streamlit
* CSV upload support for dynamic datasets
* Filtering based on ESG score thresholds
* Summary insights including best, worst, and average ESG performance
* Visualizations for comparative analysis

---

## Tech Stack

* Python
* Pandas
* Scikit-learn
* Streamlit
* Plotly

---

## Project Structure

```
esg-engine/
│── data/
│   └── esg_data.csv
│── src/
│   ├── data_loader.py
│   ├── scoring.py
│   └── ranking.py
│── streamlit_app.py
│── requirements.txt
│── README.md
```

---

## Methodology

### 1. Data Processing

* Input dataset contains ESG-related features such as emissions, energy usage, employee satisfaction, and governance indicators.
* Data is normalized using MinMaxScaler to ensure comparability across features.

### 2. ESG Score Calculation

* Environmental Score (E): Based on emissions and energy usage (lower is better)
* Social Score (S): Based on employee satisfaction and diversity
* Governance Score (G): Based on board independence and ethics

Final ESG Score:

```
ESG = (E + S + G) / 3
```

### 3. Ranking

* Companies are sorted in descending order of ESG score
* Ranking is assigned dynamically

### 4. Risk Classification

* ESG ≥ 75 → Low Risk
* ESG 50–74 → Medium Risk
* ESG < 50 → High Risk

---

## How to Run

### 1. Clone the Repository

```
git clone <your-repo-link>
cd esg-engine
```

### 2. Install Dependencies

```
python -m pip install -r requirements.txt
```

### 3. Run the Application

```
python -m streamlit run streamlit_app.py
```

### 4. Open in Browser

```
http://localhost:8501
```

---

## Input Data Format

The dataset should follow this structure:

```
company,carbon_emissions,energy_usage,employee_satisfaction,diversity_score,board_independence,ethics_score
```

---

## Example Use Cases

* ESG-based investment analysis
* Portfolio risk assessment
* Sustainability benchmarking
* Data-driven corporate evaluation

---

## Limitations

* Uses synthetic or simplified ESG data for demonstration
* Scoring model uses fixed weights (can be enhanced with ML models)
* Does not include real-time financial or ESG APIs

---

## Future Enhancements

* Integration with real-world ESG datasets (e.g., Kaggle, financial APIs)
* SQL database integration for persistent storage
* Advanced analytics and clustering for ESG risk segmentation
* Deployment on cloud platforms (Streamlit Cloud, AWS, etc.)
* Automated data ingestion pipelines

---

## Conclusion

This project demonstrates the application of data analytics and machine learning techniques to evaluate ESG performance. It combines data processing, scoring logic, and visualization into an interactive tool suitable for real-world decision support scenarios.

---


