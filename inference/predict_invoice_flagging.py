import joblib
import pandas as pd 

MODEL_PATH = "models/predict_flag_invoice.pkl"
SCALER_PATH = "models/scaler.pkl"
FEATURES = [
    "invoice_quantity",
    "invoice_dollars",
    "Freight",
    "total_item_quantity",
    "total_item_dollars",
]

def load_model(model_path: str = MODEL_PATH):
    """
    load trained classifier model
    """
    with open(model_path, "rb") as f:
        model = joblib.load(f)
    return model


def load_scaler(scaler_path: str = SCALER_PATH):
    """
    load the scaler used during training
    """
    with open(scaler_path, "rb") as f:
        scaler = joblib.load(f)
    return scaler

def predict_invoice_flag(input_data):
    '''
    predicts freight cost for new vendor invoices.

    Parameters
    input_data : dict

    Returns
    pd.Dataframe with predict freight cost
    '''
    model = load_model()
    scaler = load_scaler()
    input_df = pd.DataFrame(input_data)
    missing_features = [feature for feature in FEATURES if feature not in input_df.columns]
    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}. Expected all of: {FEATURES}"
        )

    feature_matrix = scaler.transform(input_df[FEATURES])
    input_df['Predicted_Flag'] = model.predict(feature_matrix).round()
    return input_df

if __name__ == "__main__":
    #example inference run (local testing)
    sample_data = {
        "invoice_quantity": [10, 4, 2, 1],
        "invoice_dollars": [18500, 9000, 3000, 200],
        "Freight": [150, 90, 25, 10],
        "total_item_quantity": [10, 4, 2, 1],
        "total_item_dollars": [18450, 9050, 2990, 210],
    }
    prediction = predict_invoice_flag(sample_data)
    print(prediction)