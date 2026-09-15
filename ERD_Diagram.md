# Entity Relationship Diagram (ERD)
## Vendor Invoice Intelligence System
---

## Database Schema Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     INVOICE INTELLIGENCE SYSTEM DATABASE                     │
│                              (inventory.db)                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Core Entities

#### 1. **PURCHASES** (Transactional Records)
```
┌────────────────────────────────────────┐
│            PURCHASES                   │
├────────────────────────────────────────┤
│ PK  InventoryId         VARCHAR(50)    │
│ FK  VendorNumber        INT            │───┐
│ FK  Brand              INT             │   │
│     Description        VARCHAR(255)    │   │
│     Size               VARCHAR(10)     │   │
│     PONumber           INT             │───┼─┐
│     PODate             DATE            │   │ │
│     ReceivingDate      DATE            │   │ │
│     InvoiceDate        DATE            │   │ │
│     PayDate            DATE            │   │ │
│     PurchasePrice      DECIMAL(10,2)   │   │ │
│     Quantity           INT             │   │ │
│     Dollars            DECIMAL(12,2)   │   │ │
│     Classification     INT (0/1)       │   │ │
└────────────────────────────────────────┘   │ │
                                             │ │
                                             │ │
┌────────────────────────────────────────┐   │ │
│        VENDOR_INVOICE (Aggregated)     │   │ │
├────────────────────────────────────────┤   │ │
│ FK  VendorNumber       INT             │◄──┘ │
│ FK  PONumber           INT             │◄────┘
│     VendorName         VARCHAR(255)    │
│     InvoiceDate        DATE            │
│     PODate             DATE            │
│     PayDate            DATE            │
│     Quantity           INT             │
│     Dollars            DECIMAL(12,2)   │
│     Freight            DECIMAL(10,2)   │ ◄── [ML TARGET: Freight Cost Prediction]
│     Approval           VARCHAR(50)     │
└────────────────────────────────────────┘


┌────────────────────────────────────────┐
│        PURCHASE_PRICES (Reference)     │
├────────────────────────────────────────┤
│ PK  Brand              INT             │
│     Description        VARCHAR(255)    │
│     Price              DECIMAL(10,2)   │
│     Size               VARCHAR(10)     │
│     Volume             INT             │
│     Classification     INT (0/1)       │
│ FK  VendorNumber       INT             │
│     VendorName         VARCHAR(255)    │
└────────────────────────────────────────┘
        ▲
        │ Brand, VendorNumber
        │
        └─── PURCHASES
```

#### 2. **Inventory Tracking** (Historical Records)
```
┌────────────────────────────────────────┐
│       BEGIN_INVENTORY (Period Start)   │
├────────────────────────────────────────┤
│ PK  InventoryId        VARCHAR(50)     │
│     Store              INT             │
│     City               VARCHAR(50)     │
│ FK  Brand              INT             │
│     Description        VARCHAR(255)    │
│     Size               VARCHAR(10)     │
│     onHand             INT             │
│     Price              DECIMAL(10,2)   │
│     startDate          DATE            │
└────────────────────────────────────────┘
         ▲
         │ InventoryId, Brand
         │
         ├─── Common Reference Data
         │
         ▼
┌────────────────────────────────────────┐
│        END_INVENTORY (Period End)      │
├────────────────────────────────────────┤
│ PK  InventoryId        VARCHAR(50)     │
│     Store              INT             │
│     City               VARCHAR(50)     │
│ FK  Brand              INT             │
│     Description        VARCHAR(255)    │
│     Size               VARCHAR(10)     │
│     onHand             INT             │
│     Price              DECIMAL(10,2)   │
│     endDate            DATE            │
└────────────────────────────────────────┘
```

---

## Data Flow & Relationships

### Primary Keys (PK)
- **PURCHASES**: `InventoryId` (Unique identifier for each item purchase)
- **VENDOR_INVOICE**: Implicit (one row per invoice, aggregated by PONumber)
- **PURCHASE_PRICES**: `Brand` (Product catalog reference)
- **BEGIN_INVENTORY / END_INVENTORY**: `InventoryId`

### Foreign Keys (FK)
| Source Table | FK Column | Target Table | Target Column | Relationship |
|---|---|---|---|---|
| PURCHASES | VendorNumber | PURCHASE_PRICES | VendorNumber | N:1 (Many purchases from one vendor) |
| PURCHASES | PONumber | VENDOR_INVOICE | PONumber | N:1 (Many items per PO) |
| VENDOR_INVOICE | VendorNumber | PURCHASE_PRICES | VendorNumber | N:1 |
| PURCHASES / INVENTORY | Brand | PURCHASE_PRICES | Brand | N:1 (Brand reference) |

---

## Project 1: Freight Cost Prediction Pipeline

```
┌─────────────────────────────────┐
│    VENDOR_INVOICE Table         │
│   (Load Data)                   │
│                                 │
│  Features:                      │
│  • Dollars (Invoice Amount)     │
│  • Quantity                     │
│  • VendorNumber                 │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Feature Engineering            │
│  & Data Preprocessing           │
│                                 │
│  X = ["Dollars"]                │
│  y = ["Freight"]                │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Train-Test Split               │
│  80% Training / 20% Testing     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Model Training                 │
│  • Linear Regression            │
│  • Decision Tree Regressor      │
│  • Random Forest Regressor      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Model Evaluation               │
│  Metrics:                       │
│  • MAE (Mean Absolute Error)    │
│  • MSE (Mean Squared Error)     │
│  • R² Score                     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Best Model Selection           │
│  (Lowest MAE)                   │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ MODEL OUTPUT                    │
│ predict_freight_model.pkl       │
│                                 │
│ Purpose: Predict Freight        │
│ given Invoice Dollars           │
└─────────────────────────────────┘
```

---

## Project 2: Invoice Flagging System Pipeline

```
┌─────────────────────────────────────────────────┐
│         VENDOR_INVOICE + PURCHASES              │
│      (SQL JOIN via PONumber)                    │
│                                                 │
│  vendor_invoice (vi)                            │
│      LEFT JOIN                                  │
│  purchases_aggregated (pa)                      │
│      ON vi.PONumber = pa.PONumber               │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Feature Engineering                            │
│  ───────────────────────────────────────────   │
│  From VENDOR_INVOICE (vi):                      │
│  • invoice_quantity (Quantity)                  │
│  • invoice_dollars (Dollars)                    │
│  • Freight (Actual Freight Cost)                │
│  • days_po_to_invoice (InvoiceDate - PODate)   │
│  • days_to_pay (PayDate - InvoiceDate)          │
│                                                 │
│  From PURCHASES Aggregates (pa):                │
│  • total_brands (COUNT DISTINCT Brand)          │
│  • total_item_quantity (SUM Quantity)           │
│  • total_item_dollars (SUM Dollars)             │
│  • avg_receiving_delay (AVG(ReceivingDate      │
│                          - PODate))             │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Risk-Based Labeling (Rule Engine)              │
│  ───────────────────────────────────────────   │
│  Flag = 1 if:                                   │
│  • Invoice $ ≠ Item Total $ (diff > $5)   OR   │
│  • Avg Receiving Delay > 10 days                │
│                                                 │
│  Flag = 0 otherwise (Normal invoice)            │
│                                                 │
│  Target: flag_invoice (Binary: 0/1)             │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Data Scaling (Normalization)                   │
│  StandardScaler Applied                         │
│  (Mean=0, Std=1)                                │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Model Training & Hyperparameter Tuning         │
│  ───────────────────────────────────────────   │
│  RandomForestClassifier + GridSearchCV          │
│  • 5-Fold Cross-Validation                      │
│  • Scoring: F1-Score (balanced)                 │
│  • Best hyperparameters selected                │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Model Evaluation                               │
│  Metrics:                                       │
│  • Accuracy                                     │
│  • Precision (True Positives / Predicted +)     │
│  • Recall (True Positives / Actual +)           │
│  • F1-Score (Harmonic mean of P & R)            │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│ MODEL OUTPUTS                                   │
│ ───────────────────────────────────────────    │
│ 1. predict_flag_invoice.pkl                     │
│    → Predicts if invoice is risky (0/1)         │
│                                                 │
│ 2. scaler.pkl                                   │
│    → StandardScaler for feature normalization   │
│                                                 │
│ Purpose: Automate manual invoice approval       │
│ by flagging suspicious invoices for review      │
└─────────────────────────────────────────────────┘
```

---

## Cardinality & Relationships

```
PURCHASE_PRICES
      ▲
      │ 1
      │
      └─ N ─ PURCHASES
             │
             │ N (via PONumber)
             │
             ▼
      VENDOR_INVOICE
      
      
BEGIN_INVENTORY ─── 1 ──┐
                         │ (Same InventoryId & Brand)
END_INVENTORY ───── 1 ──┤
                         │
                         └─ 1 ── PURCHASES (Historical reference)
```

---

## Data Dictionary Summary

| Table | Rows | Purpose | Key Columns |
|---|---|---|---|
| **PURCHASES** | ~5,543 | Line-item purchase records | InventoryId, PONumber, VendorNumber, Quantity, Dollars |
| **VENDOR_INVOICE** | ~5,543 | Aggregated invoices by PO | PONumber, VendorNumber, Freight, Dollars |
| **PURCHASE_PRICES** | ~500+ | Product catalog & pricing | Brand, Description, Price, VendorNumber |
| **BEGIN_INVENTORY** | ~1,000+ | Starting inventory snapshot | InventoryId, Store, Brand, onHand |
| **END_INVENTORY** | ~1,000+ | Ending inventory snapshot | InventoryId, Store, Brand, onHand |

---

## ML Model Integration

### Model 1: Freight Cost Prediction
```
Input:   invoice_dollars (feature)
│
├─ Train: 80% (4,434 records)
├─ Test:  20% (1,109 records)
│
Output:  predicted_freight (regression)
```

### Model 2: Invoice Flagging System
```
Inputs:  7 features
│        • invoice_quantity
│        • invoice_dollars
│        • Freight
│        • days_po_to_invoice
│        • days_to_pay
│        • total_brands
│        • total_item_quantity
│        • total_item_dollars
│        • avg_receiving_delay
│
├─ Rule-based labeling (binary: 0/1)
├─ StandardScaler normalization
├─ Cross-validation: 5-Fold
│
Output:  flag_invoice (binary classification)
         • 0 = Safe (Auto-approve)
         • 1 = Risky (Manual review required)
```

---

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| **Database** | SQLite3 | Persistent data storage |
| **Data Processing** | Pandas | Data manipulation & aggregation |
| **Model Building** | Scikit-learn | ML algorithms & cross-validation |
| **Model Serialization** | Joblib | Save/load trained models |
| **Notebooks** | Jupyter | Development & analysis |

---

## File Structure & Artifacts

```
machinelearningproject/
│
├── freight_cost_prediction/
│   ├── data_preprocessing.py      (Load, preprocess VENDOR_INVOICE data)
│   ├── model_evaluation.py        (Train 3 regression models, evaluate)
│   └── train.py                   (End-to-end pipeline)
│
├── invoice_flagging/
│   ├── data_preprocessing.py      (SQL join, feature engineering, labeling)
│   ├── model_evaluation.py        (RF classifier + GridSearchCV tuning)
│   └── train.py                   (End-to-end pipeline)
│
├── data/
│   └── inventory.db               (SQLite database)
│
├── models/
│   ├── predict_freight_model.pkl  (Best regression model)
│   ├── predict_flag_invoice.pkl   (Best classification model)
│   └── scaler.pkl                 (StandardScaler for normalization)
│
└── notebooks/
    ├── Predicting Freight Cost.ipynb
    └── flagginginvoice.ipynb
```

---

## Key Insights from ERD

1. **Data Integrity**: Referential integrity maintained through VendorNumber and PONumber
2. **Denormalization**: VENDOR_INVOICE aggregates line-item data for efficiency
3. **Feature Richness**: Temporal features (PODate, InvoiceDate, PayDate) enable pattern detection
4. **Risk Detection**: Multiple data points (freight, receiving delays, pricing) support fraud detection
5. **Scalability**: SQLite structure supports large transaction volumes (5,000+ invoices)

---

**Created for**: Fahad Ahmad Khan | BCA (AI & Data Analytics) | Teerthanker Mahaveer University
