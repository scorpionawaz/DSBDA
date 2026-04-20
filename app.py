import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_manager import WarehouseDataManager
from predictor import InventoryPredictor
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="InvenSense | Predictive Warehouse Management",
    page_icon="📦",
    layout="wide",
)

# --- PREMIUM STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    /* Glassmorphic Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 600;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.4);
    }
    
    .metric-val {
        font-size: 2.5rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA AND TRAIN MODEL ---
@st.cache_resource
def initialize_system():
    # Ensure data exists
    if not os.path.exists('warehouse_data.csv'):
        from data_generator import generate_warehouse_data
        generate_warehouse_data()
    
    # Tier 1: Data Manager
    manager = WarehouseDataManager().connect()
    data = manager.get_raw_data()
    
    # Tier 2: Predictor
    predictor = InventoryPredictor()
    predictor.train(data)
    
    return manager, predictor, data

try:
    manager, predictor, data = initialize_system()
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/000000/warehouse.png", width=100)
    st.title("InvenSense AI")
    st.markdown("### Model Control Panel")
    
    category = st.selectbox("Product Category", data['Product_Category'].unique())
    stock = st.slider("Current Stock Level", 0, 1500, 500)
    sales = st.number_input("Units Sold (Last Week)", min_value=0, max_value=1000, value=200)
    promo = st.checkbox("Promotion Campaign Active", value=False)
    
    predict_btn = st.button("Generate Forecast", use_container_width=True)

# --- MAIN DASHBOARD ---
st.title("📦 Warehouse Inventory Analytics")
st.markdown("#### Predictive Forecasting & Demand Trends")

# Top Row Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.metric("Total Skus", len(data))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    avg_sales = int(data['Units_Sold_Last_Week'].mean())
    st.metric("Avg. Weekly Sales", avg_sales)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    total_cost = f"${data['Inventory_Cost'].sum():,.0f}"
    st.metric("Total Inventory Value", total_cost)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.metric("Promo Penetration", f"{data['Promotion_Active'].mean()*100:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# Middle Row: Prediction Result & Charts
row2_col1, row2_col2 = st.columns([1, 2])

with row2_col1:
    st.markdown("### 🎯 Smart Forecast")
    if predict_btn:
        prediction = predictor.predict(category, stock, sales, promo)
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <p style="font-size: 1.1rem; margin-bottom: 0;">Predicted Demand</p>
            <h2 class="metric-val">{prediction} Units</h2>
            <p style="font-size: 0.9rem; color: #94a3b8;">Next 7 Days Forecast</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendation
        if prediction > stock:
            st.warning(f"⚠️ **Stockout Risk:** Current stock ({stock}) is below forecast ({prediction}). Recommend ordering {prediction - stock} units.")
        else:
            st.success(f"✅ **Stock Healthy:** Current stock ({stock}) covers forecast demand.")
    else:
        st.info("Adjust the parameters in the sidebar and click **Generate Forecast** to see AI predictions.")

with row2_col2:
    st.markdown("### 📈 Category-wise Demand")
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    sns.barplot(data=data, x='Product_Category', y='Target_Demand', palette='Blues_d', ax=ax)
    ax.tick_params(colors='#f1f5f9')
    ax.spines['bottom'].set_color('#f1f5f9')
    ax.spines['left'].set_color('#f1f5f9')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel("Category", color='#f1f5f9')
    ax.set_ylabel("Total Demand", color='#f1f5f9')
    
    st.pyplot(fig)

# Bottom Row: Data Exploration
st.markdown("### 🔍 Historical Inventory Log (Simulated Hive View)")
st.dataframe(data.head(10).style.background_gradient(subset=['Target_Demand'], cmap='Blues'), use_container_width=True)

st.markdown("""
---
<p style="text-align: center; color: #64748b; font-size: 0.8rem;">
    InvenSense Predictive Engine v1.0 | Built with Python, Scikit-Learn & Streamlit
</p>
""", unsafe_allow_html=True)
