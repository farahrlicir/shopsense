# ShopSense — Online Purchase Intention Prediction

ShopSense is a machine learning project that predicts whether an online shopping session will result in a purchase. It explores how session behavior and visitor characteristics can support purchase-intention analysis.

**Project status:** Model trained and evaluated; production-readiness work remains.

## Business Problem

E-commerce businesses want to better understand which browsing sessions are associated with purchases. A purchase-intention model can help investigate visitor behavior and inform future marketing and personalization strategies.

ShopSense frames this as a **binary classification problem**.

## Dataset

- **Dataset:** UCI Online Shoppers Purchasing Intention
- **Target:** `Revenue`
- **Task:** Predict whether a session results in a purchase.
- **Data unit:** Individual browsing sessions.

The dataset contains behavioral, temporal, and visitor-related features. Feature availability at the intended prediction time still requires verification.

## Machine Learning Workflow

The project covers:

- Data understanding and validation
- Stratified train, validation, and test splitting
- Preprocessing with a scikit-learn pipeline
- Logistic Regression baseline experimentation
- Random Forest model tuning
- Validation-based decision-threshold selection
- Held-out test evaluation
- Model serialization and basic prediction tests

## Final Model

The selected candidate is a Random Forest classifier with preprocessing bundled into a scikit-learn pipeline.

- Trees: 500
- Maximum depth: 30
- Minimum samples per leaf: 8
- Maximum features: 0.5
- Decision threshold: 0.37

The decision threshold was selected using validation data.

## Held-Out Test Results

| Metric | Score |
|---|---:|
| ROC-AUC | 0.9324 |
| PR-AUC | 0.7538 |
| Precision | 0.6501 |
| Recall | 0.7199 |
| F1-score | 0.6832 |

At the selected threshold, the model identifies approximately 72% of the actual purchase sessions in the test set. Precision is approximately 65%, so some sessions predicted to result in purchases do not end in a purchase.

These are offline test results, not evidence of business impact in production.

## Repository Contents

- `notebooks/` — analysis, modeling, and evaluation notebooks
- `shopsense_pipeline.joblib` — serialized fitted pipeline
- `shopsense_experiment.json` — experiment configuration, test metrics, and limitations
- `requirements.txt` — Python dependencies

## Limitations and Next Steps

- Verify that every feature is available at the intended prediction time and investigate potential target leakage, particularly for `PageValues`.
- The current dataset supports a session-level benchmark; it does not establish that the model can make reliable predictions partway through an active session.
- Pin tested dependency versions and add a formal automated test suite.
- Build and test an inference API before considering deployment.
- Evaluate operational performance and business impact before using predictions to drive marketing decisions.

## Reproducibility

The fitted pipeline is saved as `shopsense_pipeline.joblib`, and experiment details are recorded in `shopsense_experiment.json`. The pipeline can be loaded with joblib in a compatible Python environment.

**Note:** Only load serialized model files from trusted sources.

## Technologies

Python · pandas · NumPy · scikit-learn · joblib · Jupyter / Kaggle
