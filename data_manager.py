import pandas as pd
import os

class WarehouseDataManager:
    """
    Simulates a Data Tier using a Hive-like interface. 
    In a real scenario, this would use PyHive to connect to a Hadoop/Hive cluster.
    """
    def __init__(self, data_path='warehouse_data.csv'):
        self.data_path = data_path
        self.df = None

    def connect(self):
        """Simulates connection to a Hive warehouse."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data source {self.data_path} not found. please run data logic first.")
        print("Connected to Hive simulation (Local CSV).")
        self.df = pd.read_csv(self.data_path)
        return self

    def execute_query(self, query):
        """
        Simulates HiveQL query execution.
        Example: 'SELECT * FROM inventory_logs'
        """
        if self.df is None:
            self.connect()
        
        # In this simulation, we just return the full dataframe or filter if query contains WHERE
        # For academic purposes, we keep it simple but modular.
        print(f"Executing simulated HiveQL: {query}")
        return self.df

    def get_raw_data(self):
        if self.df is None:
            self.connect()
        return self.df

if __name__ == "__main__":
    manager = WarehouseDataManager()
    manager.connect()
    data = manager.execute_query("SELECT * FROM warehouse_inventory")
    print(data.head())
