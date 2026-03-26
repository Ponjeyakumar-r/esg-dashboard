
---

# ESG Portfolio Analytics Dashboard

## Overview

The ESG Portfolio Analytics Dashboard is an end-to-end data analytics application that evaluates and ranks companies based on Environmental, Social, and Governance (ESG) metrics. It integrates data processing, scoring, database storage, and interactive visualization into a unified system for sustainability analysis.

---

## Live Demo

Access the deployed application:
**[Live App](https://esg-dashboard-01.streamlit.app/)**

---

## Features

* Multi-factor ESG scoring model (Environmental, Social, Governance)
* Data normalization using Scikit-learn (MinMaxScaler)
* Company ranking based on ESG scores
* Risk classification (Low, Medium, High)
* K-Means clustering for company segmentation
* Interactive dashboard built with Streamlit
* CSV upload support for dynamic datasets
* Filtering by ESG score and risk level
* SQL-based insights using SQLite
* Export results as CSV (full and filtered)
* Real-time visualizations:
  * ESG score distribution (bar chart)
  * Risk level distribution (pie chart)
  * E/S/G score breakdown (bar chart)
  * Top 5 companies comparison (radar chart)
  * Industry comparison
  * Score correlation heatmap
* Company clustering visualization

---

## Tech Stack

* Python
* Pandas
* Scikit-learn
* Streamlit
* SQLite
* Plotly

---

## Project Structure

```id="7opbbq"
esg-engine/
│── data/
│   └── esg_data.csv
│── src/
│   ├── data_loader.py
│   ├── scoring.py
│   ├── ranking.py
│   ├── database.py
│   └── __init__.py
│── streamlit_app.py
│── requirements.txt
│── README.md
```

---

## System Architecture

The application follows a layered architecture:

1. Data Layer

   * Loads ESG datasets (default or user-uploaded)
   * Stores processed data in SQLite database

2. Processing Layer

   * Normalizes features using MinMaxScaler
   * Computes Environmental, Social, and Governance scores
   * Aggregates into a final ESG score

3. Storage Layer

   * Saves processed data into SQLite (`esg.db`)
   * Enables persistent storage and querying

4. Query Layer

   * Executes SQL queries to retrieve top companies and aggregate metrics

5. Presentation Layer

   * Displays results using Streamlit dashboard
   * Provides filters, insights, and visualizations

---

## Methodology

### ESG Score Calculation

* Environmental Score (E): Carbon emissions (60%) + Energy usage (40%) - lower is better
* Social Score (S): Employee satisfaction (60%) + Diversity score (40%)
* Governance Score (G): Board independence (50%) + Ethics score (50%)

Final ESG Score:

```
ESG = (E + S + G) / 3
```

All scores are normalized to 0-100 scale using MinMaxScaler.

---

### Risk Classification

* ESG ≥ 75 → Low Risk
* ESG 50–74 → Medium Risk
* ESG < 50 → High Risk

### Clustering

K-Means clustering is applied to segment companies into performance groups based on E/S/G scores.

---

## SQL Integration

* Implemented SQLite for persistent data storage
* Stored processed ESG data into relational tables
* Executed SQL queries to:

  * Retrieve top-performing companies
  * Calculate average ESG score
* Enabled separation between analytics and data retrieval layers

---

## How to Run Locally

### 1. Clone the Repository

```id="x12tt5"
git clone https://github.com/Ponjeyakumar-r/esg-dashboard.git
cd esg-dashboard
```

### 2. Install Dependencies

```id="5kvq3u"
python -m pip install -r requirements.txt
```

### 3. Run the Application

```id="0gcm9c"
python -m streamlit run streamlit_app.py
```

---

## Input Data Format

The dataset should follow this structure:

```id="3ff63l"
company,carbon_emissions,energy_usage,employee_satisfaction,diversity_score,board_independence,ethics_score
```

---

## Example Use Cases

* ESG-based investment analysis
* Portfolio risk assessment
* Corporate sustainability benchmarking
* Data-driven decision support

---

## Limitations

* Uses synthetic or simplified ESG data for demonstration
* Fixed weighting scheme for ESG scoring
* Does not integrate real-time ESG APIs

---

## Future Enhancements

* Integration with real-world ESG datasets (financial APIs, Kaggle)
* Advanced ML models for ESG prediction and clustering
* Cloud database integration (PostgreSQL, AWS RDS)
* User authentication and role-based access
* Automated data pipelines

---

## Conclusion

This project demonstrates the application of data analytics, machine learning preprocessing, database management, and interactive visualization to solve a real-world sustainability problem. It provides a scalable foundation for ESG-based decision support systems.

---

