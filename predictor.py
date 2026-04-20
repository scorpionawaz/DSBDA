import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class InventoryPredictor:
    """
    Processing Tier: Handles Data Scrubbing, Exploring, and Modeling.
    """
    def __init__(self):
        self.model = LinearRegression()
        self.le = LabelEncoder()
        self.is_trained = False

    def scrub_data(self, df):
        """
        Assignment 4 & 5: Data Scrubbing (Cleaning, Encoding, Outlier focus).
        """
        # Handling missing values (if any)
        df = df.dropna()
        
        # Encoding categorical variables
        df['Product_Category_Encoded'] = self.le.fit_transform(df['Product_Category'])
        
        return df

    def train(self, df):
        """
        Assignment 10: Model Building.
        """
        df = self.scrub_data(df)
        
        X = df[['Product_Category_Encoded', 'Previous_Stock', 'Units_Sold_Last_Week', 'Promotion_Active']]
        y = df['Target_Demand']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Calculate accuracy for internal tracking
        score = self.model.score(X_test, y_test)
        print(f"Model trained with R^2 Score: {score:.4f}")
        
        return score

    def predict(self, category, stock, sales, promo):
        """
        Predict demand based on input.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction.")
        
        cat_enc = self.le.transform([category])[0]
        promo_val = 1 if promo else 0
        
        prediction = self.model.predict([[cat_enc, stock, sales, promo_val]])
        return int(prediction[0])

if __name__ == "__main__":
    # Test internal logic
    from data_manager import WarehouseDataManager
    import os
    
    if not os.path.exists('warehouse_data.csv'):
        from data_generator import generate_warehouse_data
        generate_warehouse_data()
        
    manager = WarehouseDataManager().connect()
    data = manager.get_raw_data()
    
    predictor = InventoryPredictor()
    predictor.train(data)
    
    res = predictor.predict('Electronics', 500, 200, True)
    print(f"Test Prediction: {res}")
