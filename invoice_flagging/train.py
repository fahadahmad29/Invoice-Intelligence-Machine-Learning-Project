try:
    from .data_preprocessing import load_invoice_data, split_data, scale_features, apply_labels
    from .model_evaluation import train_random_forest, evaluate_classifier
except ImportError:
    from invoice_flagging.data_preprocessing import load_invoice_data, split_data, scale_features, apply_labels
    from invoice_flagging.model_evaluation import train_random_forest, evaluate_classifier
import joblib

FEATURES = [
    'invoice_quantity',
    'invoice_dollars', 
    'Freight',
    'total_item_quantity',
    'total_item_dollars']

TARGET = "flag_invoice"

def main():
    #load data
    df = load_invoice_data()
    df = apply_labels(df)

    #prepare data
    X_train, X_test, y_train, y_test = split_data(df, FEATURES , TARGET)
    X_train_scaled, X_test_scaled = scale_features(
        X_train, X_test, 'models/scaler.pkl'
      )

    grid_search = train_random_forest(X_train_scaled, y_train)

    evaluate_classifier(
        grid_search.best_estimator_,
        X_test_scaled,
        y_test,
        "Random Forest Classifier"
    )

    #save the best model
    joblib.dump(grid_search.best_estimator_, 'models/predict_flag_invoice.pkl')

if __name__ == "__main__":
    main()
    






























    