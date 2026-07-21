import sqlite3
from sklearn.model_selection import train_test_split
import pandas as pd

def load_vendor_invoice_data(db_path: str):
    "load data of the invoices from the sql database"
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM vendor_invoice"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def prepare_features(df: pd.DataFrame):
    "Select features and target values"
    X = df[["Dollars"]]
    y = df[["Freight"]]
    return X,y

def split_data(X,y,test_size=0.2,random_state=42):
    "split dataset into train and test data"
    return train_test_split(X, y, random_state=random_state, test_size=test_size)
    

