# 3. Data Understanding

## Objective

The objective of this phase is to understand the structure, content, distributions, and initial relationships within the dataset before making modeling decisions.

The goal is not to build a model yet, but to answer:

- What does one observation represent?
- What is the prediction target?
- What types of features are available?
- How are the classes distributed?
- Which features appear potentially informative?
- Are there characteristics of the data that may affect preprocessing, modeling, or evaluation?

---

## 3.1 Dataset Overview

The dataset contains **12,330 observations and 18 columns**.

Each observation represents one **website session** from an online shopping website.

The target variable is:

`Revenue`

where:

- `False` → the session did not result in a purchase
- `True` → the session resulted in a purchase

The dataset therefore represents a **binary classification problem** at the session level.

---

## 3.2 Feature Types

The dataset contains numerical, categorical, and boolean features.

### Numerical features

- `Administrative`
- `Administrative_Duration`
- `Informational`
- `Informational_Duration`
- `ProductRelated`
- `ProductRelated_Duration`
- `BounceRates`
- `ExitRates`
- `PageValues`
- `SpecialDay`

### Categorical features

- `Month`
- `OperatingSystems`
- `Browser`
- `Region`
- `TrafficType`
- `VisitorType`

Although `OperatingSystems`, `Browser`, `Region`, and `TrafficType` are stored as integers, their values represent **categories/codes rather than continuous numerical quantities**.

For example, Browser `13` is not inherently greater than Browser `2`.

###
