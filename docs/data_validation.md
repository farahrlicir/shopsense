# 4. Data Validation

## Objective

The objective of data validation is to determine whether the dataset is sufficiently reliable and consistent for machine learning.

At this stage, we are not trying to improve model performance. We are checking whether the data is valid, internally consistent, and safe to use.

---

## 4.1 Missing Values

We checked all 18 columns for explicit missing values.

**Result:**
- No missing values were found.
- Every column contains 12,330 non-null observations.

**Conclusion:**  
No explicit missing-value treatment is required at this stage.

However, the absence of `NaN` values does not automatically mean that the dataset is clean. Values such as `0` must be interpreted according to the meaning of each feature rather than automatically treated as missing.

---

## 4.2 Numerical Domain Validation

We checked whether numerical features contained negative values.

**Result:**
- No numerical feature contains negative values.
-
