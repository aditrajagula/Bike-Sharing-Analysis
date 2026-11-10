# Bike Sharing Analysis & Dashboard

A data analysis and interactive Streamlit dashboard analyzing the **Capital Bikeshare** dataset (Washington, D.C., 2011–2012). Built as the final project for Dicoding's **"Belajar Analisis Data dengan Python"** course.

🔗 **Live Demo:** [bikeshare-analysis.streamlit.app](https://bikeshare-analysis.streamlit.app/)

---

## Project Structure

```text
Bike-Sharing-Analysis/
├── dashboard/
│   ├── dashboard.py         # Streamlit dashboard application
│   ├── day_clean.csv        # Cleaned daily dataset
│   └── main_data.csv       # Cleaned hourly dataset
├── data/
│   ├── day.csv              # Raw daily data
│   └── hour.csv             # Raw hourly data
├── notebook.ipynb           # Data wrangling, EDA & visualization
├── requirements.txt         # Dependencies
├── url.txt                  # Deployment link
└── README.md
```

---

## How to Run Locally

### 1. Set Up Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit Dashboard

```bash
streamlit run dashboard/dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## Key Insights

* **Season & Weather:** Peak rental activity occurs in **Fall** (~5,644 rentals/day) and under **Clear** weather (~4,877 rentals/day). Adverse rain/snow reduces rentals to ~1,803 units/day.
* **Hourly Patterns:**
  * **Working Days:** Pronounced rush-hour peaks at **08:00 AM** and **05:00–06:00 PM**, dominated by registered commuters (>85%).
  * **Weekends/Holidays:** Recreational demand peaks in the afternoon (**12:00–04:00 PM**) with higher casual rider volume.
* **Recommendations:** Schedule fleet maintenance during low-demand winter/rainy periods, rebalance station bikes before commute peaks, and target casual riders with membership promotions on weekends.

---