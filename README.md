# ShopSense — Online Purchase Intention Prediction

ShopSense is an end-to-end machine learning project that predicts whether an online shopping session will result in a purchase. It combines model development, evaluation, API development, and cloud deployment into a single application.

**Project status:** Model trained and evaluated; API and interactive UI deployed. Further production-readiness work remains.

**Live demo:** [Open ShopSense](https://shopsensegit-cvlacf6nua5tkzonzzaie5.streamlit.app/)

**Prediction API:** [ShopSense API](https://shopsense-api-94dm.onrender.com)

## Business Problem

E-commerce businesses want to understand which browsing sessions are associated with purchases. A purchase-intention model can support exploratory analysis of visitor behavior and inform future marketing and personalization experiments.

ShopSense frames this as a **binary classification problem**, using session-level features to estimate the probability that a session results in a purchase.

The current model is a research and portfolio benchmark, not a validated business decision system.

## Dataset

- **Dataset:** UCI Online Shoppers Purchasing Intention
- **Target:** `Revenue`
- **Task:** Binary classification
- **Data unit:** Individual browsing sessions
- **Target classes:** Purchase and no purchase

The dataset includes browsing behavior, page counts and durations, visitor characteristics, and temporal features.

Feature availability at the intended prediction time remains an important limitation. In particular, `PageValues` requires further investigation for potential leakage or dependence on information unavailable when a prediction would be made.

## Machine Learning Workflow

The project covers the following stages:

1. Business problem formulation
2. Data understanding and validation
3. Duplicate handling and stratified train/validation/test splitting
4. Preprocessing with a scikit-learn `ColumnTransformer` and `Pipeline`
5. Baseline experimentation with Logistic Regression
6. Random Forest hyperparameter tuning
7. Decision-threshold selection using validation data
8. Final evaluation on a held-out test set
9. Model serialization and experiment documentation
10. API development and automated tests
11. Interactive UI development
12. Cloud deployment

## Model and Evaluation

The selected model is a Random Forest classifier with preprocessing bundled into a scikit-learn pipeline.

| Configuration | Value |
|---|---|
| Number of trees | 500 |
| Maximum depth | 30 |
| Minimum samples per leaf | 8 |
| Maximum features | 0.5 |
| Decision threshold | 0.37 |

The decision threshold was selected using validation data before final evaluation on the held-out test set.

### Held-out test results

| Metric | Score |
|---|---:|
| ROC-AUC | 0.9324 |
| PR-AUC | 0.7538 |
| Precision | 0.6501 |
| Recall | 0.7199 |
| F1-score | 0.6832 |

At the selected threshold, the model identifies approximately 72% of actual purchase sessions in the test set. Its precision is approximately 65%, meaning some sessions predicted as purchases do not result in purchases.

These metrics describe offline test performance. They do not establish business impact, calibration quality, or performance on live traffic.

## Application Architecture

The application has three main components:

- **Streamlit UI:** Collects session features and displays prediction results.
- **FastAPI service:** Validates incoming requests, loads the fitted pipeline, and returns purchase probabilities and threshold-based decisions.
- **Serialized model:** Contains the fitted preprocessing and Random Forest pipeline.

The UI sends session features to the API, which returns the estimated purchase probability, predicted class, and decision threshold.

### Deployed services

- **Interactive application:** [Streamlit Community Cloud](https://shopsensegit-cvlacf6nua5tkzonzzaie5.streamlit.app/)
- **API service:** [Render](https://shopsense-api-94dm.onrender.com)
- **API health endpoint:** [/health](https://shopsense-api-94dm.onrender.com/health)
- **Interactive API documentation:** [/docs](https://shopsense-api-94dm.onrender.com/docs)

The API provides a `POST /predict` endpoint for predictions and a `GET /health` endpoint for basic service health checks.

Free hosting may introduce cold-start delays. The UI allows a longer request timeout, but this does not guarantee that every request will succeed.

## Repository Structure

- `app.py` — Streamlit user interface
- `src/api.py` — FastAPI application and prediction endpoint
- `tests/test_api.py` — automated API tests
- `notebooks/` — exploratory analysis, modeling, and evaluation
- `shopsense_pipeline.joblib` — serialized fitted pipeline
- `shopsense_experiment.json` — experiment configuration, test metrics, and limitations
- `requirements.txt` — Python dependencies

## Run Locally

Python 3.11 is the tested Python version for the current deployment setup.

### 1. Install dependencies

Clone the repository, navigate to its root directory, and create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

### 2. Start the API

From the repository root:

```bash
uvicorn src.api:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 3. Start the UI

In a separate terminal, activate the same virtual environment and run:

```bash
streamlit run app.py
```

When running locally, the UI uses `http://127.0.0.1:8000` as its default API URL. A configured `API_URL` secret or environment variable can override this value.

## Run Tests

Run the automated API tests from the repository root:

```bash
pytest -q
```

The current API test suite contains five tests. These verify selected API behaviors; they do not replace comprehensive load, security, or production integration testing.

## Reproducibility

The fitted pipeline is saved in `shopsense_pipeline.joblib`, while `shopsense_experiment.json` records the model configuration, decision threshold, test metrics, and known limitations.

The saved pipeline should be loaded in a compatible environment. The tested scikit-learn version is pinned in `requirements.txt` because serialized scikit-learn objects may not be compatible across versions.

Only load serialized model files from trusted sources.

## Limitations and Future Work

- Verify feature availability at the intended prediction time, especially for `PageValues`, `BounceRates`, and `ExitRates`.
- The dataset supports a session-level benchmark; it does not establish reliable prediction partway through an active session.
- Improve cold-start handling and API error reporting.
- Strengthen input validation and automated integration tests.
- Add structured logging and operational monitoring.
- Evaluate probability calibration and performance across relevant visitor segments.
- Measure business impact through controlled experiments before using predictions to drive marketing decisions.

## Technologies

Python · pandas · NumPy · scikit-learn · joblib · FastAPI · Pydantic · Streamlit · pytest · GitHub · Render · Streamlit Community Cloud

---

**Disclaimer:** ShopSense is an educational and portfolio project. Predictions are estimates based on a historical dataset and should not be interpreted as guarantees of future purchases.
