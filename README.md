# Marketing Mix Modeling (MMM) Studio

A production-ready Marketing Mix Modeling (MMM) engine and interactive "Data Science Studio" dashboard built with Python, `scikit-learn`, and `NiceGUI`. Designed to help executive teams and data scientists perform quantitative econometric time-series analysis (using Ridge Regression, Adstock transformations, and Hill saturation curves) to evaluate paid media effectiveness and optimize multi-channel budget allocations.

---

## Features

- **Econometric Modeling Engine (`model.py`)**:
  - **Adstock Transformation**: Simulates advertising carryover/lingering effects over time using geometric decay.
  - **Hill Saturation Curves**: Models diminishing returns on marketing spend[cite: 1].
  - **Ridge Regression**: Regularized regression pipeline using `scikit-learn` to estimate stable media contribution weights and baseline revenue[cite: 1].
- **Data Science Studio UI (`ui.py`)**:[cite: 1]
  - Dark-themed, modern slate aesthetic with crisp teal and amber accents[cite: 1].
  - Interactive budget-allocation simulation sliders that instantly recalculate predicted revenues[cite: 1].
  - Dynamic KPI cards and coefficients weights evaluation table[cite: 1].
- **Cloud-Ready**: Fully containerized with Docker and configured for automated deployment via Render Blueprint (`render.yaml`)[cite: 1].

---

## Tech Stack

- **Backend & Modeling**: Python, NumPy, Pandas, Scikit-Learn[cite: 1]
- **UI Framework**: NiceGUI (FastAPI / Vue 3 reactive foundation)[cite: 1]
- **Deployment & Hosting**: Docker, Gunicorn, Uvicorn, Render[cite: 1]

---

## Local Development & Installation

1. **Clone the repository**:[cite: 1]
   ```bash
   git clone [https://github.com/YOUR_USERNAME/marketing-mix-modeling-studio.git](https://github.com/YOUR_USERNAME/marketing-mix-modeling-studio.git)
   cd marketing-mix-modeling-studio