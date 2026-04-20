# InvenSense: Predictive Warehouse Inventory Management

InvenSense is a predictive analytics system designed for warehouse inventory optimization. It utilizes historical data to forecast future product demand, helping warehouse managers minimize overstocking costs and prevent stock-outs.

The project is built using a **Tiered Architecture** and follows the **Data Science Project Life Cycle** (Obtain, Scrub, Explore, Model, Interpret), aligning with DSBDA lab requirements.

## 🚀 Key Features
- **Predictive Forecasting**: High-accuracy Linear Regression model (R² ~ 0.97).
- **Interactive Dashboard**: Premium glassmorphic UI built with Streamlit.
- **Hive Simulation**: Data Tier structured to simulate HiveQL managed logs.
- **Smart Alerts**: Actionable inventory recommendations based on AI forecasts.
- **Modular Design**: Decoupled Data, Processing, and Presentation layers.

## 🏗️ Technical Architecture
1.  **Data Tier (`data_manager.py`)**: Connects to the warehouse logs. Currently simulates an Apache Hive connection via local storage but is fully modular for Hadoop integration.
2.  **Processing Tier (`predictor.py`)**: Handles data cleaning (scrubbing), label encoding, and regression model training.
3.  **Presentation Tier (`app.py`)**: Provides a real-time web interface for demand visualization and metric tracking.

## 🛠️ Technology Stack
- **Language**: Python 3.14
- **Data Handling**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (Linear Regression)
- **UI/UX**: Streamlit
- **Visualization**: Seaborn, Matplotlib

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   cd "DSBDA Project"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate synthetic data**:
   ```bash
   python data_generator.py
   ```

4. **Launch the dashboard**:
   ```bash
   python -m streamlit run app.py
   ```

## 📚 Lab Assignment Mapping
This project demonstrates compliance with the following academic concepts:
- **Assignment 4 & 5**: Data Scrubbing and Preprocessing (Cleaning & Encoding).
- **Assignment 8**: Data Visualization (Seaborn Dashboard).
- **Assignment 10**: Model Building (Predictive Regression).

---
*Built with ❤️ for the DSBDA Academics project.*
