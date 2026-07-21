# 📦 Vendor Invoice Intelligence System

Two machine learning pipelines built on top of a vendor/inventory SQLite database:

1. **Freight Cost Prediction** — predicts freight charges from invoice data.
2. **Invoice Flagging System** — detects sketchy/suspicious invoices automatically, so they don't need manual approval.

---

## 🎯 Why This Project

Companies deal with thousands of vendor invoices. Two problems show up again and again:

- Freight costs are hard to estimate in advance.
- Every invoice needs manual checking to catch fraud or data-entry errors — slow and error-prone.

This project solves both using ML models trained on real invoice + purchase data.

---

## 🧩 Project 1: Freight Cost Prediction

**Goal:** Predict `Freight` cost from the invoice `Dollars` amount.

**Pipeline:**

| Step | What Happens |
|------|---------------|
| Load Data | Reads `vendor_invoice` table from `data/inventory.db` (SQLite) |
| Features | `Dollars` (input) → `Freight` (target) |
| Split | 80% train / 20% test |
| Models Trained | Linear Regression, Decision Tree Regressor, Random Forest Regressor |
| Evaluation | MAE, MSE, R² Score |
| Model Selection | Best model = lowest MAE |
| Output | Best model saved to `models/predict_freight_model.pkl` |

**Files:**
- `data_preprocessing.py` → loads data, splits features/target, train-test split
- `model_evaluation.py` → trains 3 regression models, evaluates each
- `train.py` → runs the full pipeline end-to-end and saves the winner

---

## 🚩 Project 2: Invoice Flagging System

**Goal:** Classify each invoice as **normal** or **flagged (risky)** — automating manual approval.

**How an invoice gets flagged:**

- 🔴 Invoice amount doesn't match the actual item-level total (difference > $5)
- 🔴 Receiving delay is abnormally high (average > 10 days)

If either is true → `flag_invoice = 1` (risky), otherwise `0` (safe).

**Pipeline:**

| Step | What Happens |
|------|---------------|
| Load Data | Joins `vendor_invoice` with an aggregated `purchases` table (per PO Number) via SQL |
| Feature Engineering | Days between PO → Invoice, Invoice → Payment, brand count, quantity, dollar totals, receiving delay |
| Labeling | Rule-based risk logic (see above) |
| Scaling | `StandardScaler` on numeric features (scaler saved for reuse) |
| Model | `RandomForestClassifier` tuned with `GridSearchCV` (5-fold CV, scored on F1) |
| Evaluation | Accuracy + full classification report |
| Output | Best model saved to `models/predict_flag_invoice.pkl`, scaler to `models/scaler.pkl` |

**Features used for prediction:**
`invoice_quantity`, `invoice_dollars`, `Freight`, `total_item_quantity`, `total_item_dollars`

**Files:**
- `data_preprocessing.py` → SQL join query, risk labeling, scaling
- `model_evaluation.py` → Random Forest + GridSearchCV hyperparameter tuning
- `train.py` → runs full pipeline and saves best model + scaler

---

## 🛠️ Tech Stack

- **Python** — core language
- **SQLite3** — database (`inventory.db`)
- **Pandas** — data loading & manipulation
- **Scikit-learn** — models, scaling, evaluation, GridSearchCV
- **Joblib** — saving trained models

---

## 📁 Project Structure

```
machinelearningproject/
│
├── freight_cost_prediction/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
│
├── invoice_flagging/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
│
├── data/
│   └── inventory.db
│
└── models/
    ├── predict_freight_model.pkl
    ├── predict_flag_invoice.pkl
    └── scaler.pkl
```

---

## ▶️ How to Run

```bash
# Freight cost prediction
python -m freight_cost_prediction.train

# Invoice flagging system
python -m invoice_flagging.train
```

Both scripts will:
1. Load data from the SQLite database
2. Train multiple models
3. Pick and print the best one
4. Save it to the `models/` folder

---

## 📊 Evaluation Metrics Used

| Project | Metrics |
|---------|---------|
| Freight Cost Prediction | MAE, MSE, R² Score |
| Invoice Flagging | Accuracy, Precision, Recall, F1-score |

---

## 🚀 Future Improvements

- Add more features to freight prediction (e.g., PO-level aggregates, brand, quantity)
- Try XGBoost/LightGBM for better accuracy
- Build a simple dashboard (Streamlit/Flask) to show flagged invoices
- Add model explainability (SHAP) so risk flags can be justified to auditors

---

## 👤 Author

**Fahad Ahmad Khan**
BCA (AI & Data Analytics) — Teerthanker Mahaveer University
