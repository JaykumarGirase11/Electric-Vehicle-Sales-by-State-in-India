import streamlit as st
import pandas as pd
import sys
import os

# --- Setup Paths ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from preprocess import preprocess_ev_data
from eda import (
    plot_yearly_sales, plot_monthly_sales, plot_top_states,
    plot_by_vehicle_category, plot_by_vehicle_type
)
from model import train_model

st.set_page_config(page_title="EV Sales Dashboard", layout="wide", page_icon="⚡")

# --- Cache the data loading ---
@st.cache_data
def load_data():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'Electric Vehicle Sales by State in India.csv'))
    return preprocess_ev_data(data_path)

df = load_data()

# --- Main Page Navigation (Centered, Not Sidebar) ---
st.markdown("""
    <style>
    .main-title { font-size: 2.8em; font-weight: 700; color: #08c0a6; margin-bottom: 5px; text-align: center; }
    .sub-title { font-size: 1.2em; color: #888; text-align: center; margin-bottom: 30px; }
    .nav-tabs { display: flex; justify-content: center; gap: 1.5rem; font-size: 1.1em; margin-bottom: 30px; }
    .nav-tabs button { background: #f0f2f6; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
    .nav-tabs button:hover { background: #08c0a633; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ Electric Vehicle Sales in India</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive Dashboard powered by Python · ML · Streamlit · Analytics</div>', unsafe_allow_html=True)

nav_selection = st.radio("", ["Home", "EDA Visuals", "Predictive Modeling", "Raw Data"], horizontal=True)

# --- Sidebar Filters ---
st.sidebar.title("⚙️ Filters")
years = ['All Years'] + sorted(df['Year'].unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", years)
selected_states = st.sidebar.multiselect("Select State(s)", sorted(df['State'].unique()))

# --- Apply Filters ---
df_filtered = df.copy()
if selected_year != 'All Years':
    df_filtered = df_filtered[df_filtered['Year'] == selected_year]
if selected_states:
    df_filtered = df_filtered[df_filtered['State'].isin(selected_states)]

# --- HOME PAGE ---
if nav_selection == "Home":
    st.image("assets/ev_banner.png", caption="Electric Future of India", use_container_width=True)
    st.markdown("""
    ### What You Can Explore:
    - ✅ EV Sales Trends (Year, State, Category, Type)
    - 🚀 Predict Future EV Sales using Machine Learning
    - 📂 Explore Cleaned Raw Data
    """)

# --- EDA PAGE ---
elif nav_selection == "EDA Visuals":
    st.header(":round_pushpin: EV Sales Trends")
    if not df_filtered.empty:
        st.pyplot(plot_yearly_sales(df_filtered))
        st.pyplot(plot_monthly_sales(df_filtered))
        st.pyplot(plot_top_states(df_filtered))
        st.pyplot(plot_by_vehicle_category(df_filtered))
        st.pyplot(plot_by_vehicle_type(df_filtered))
    else:
        st.warning("No data available for selected filters.")

# --- PREDICTIVE MODEL PAGE ---
elif nav_selection == "Predictive Modeling":
    st.header("🚀 Predictive Model: EV Sales Forecast")

    @st.cache_resource
    def get_model_results():
        return train_model(df)

    with st.spinner("Training model (only runs once)..."):
        try:
            model, X_test, y_test, y_pred = get_model_results()
            predictions_df = pd.DataFrame({"Actual": y_test, "Predicted": y_pred}).reset_index(drop=True)

            st.success("Model trained successfully!")
            st.subheader("Predictions Sample")
            st.dataframe(predictions_df.head(20))
            st.line_chart(predictions_df.head(50))
        except Exception as e:
            st.error(f"Model failed: {e}")

# --- RAW DATA PAGE ---
elif nav_selection == "Raw Data":
    st.header("📂 Cleaned Raw Dataset")
    if not df_filtered.empty:
        st.dataframe(df_filtered.head(100))
    else:
        st.warning("No raw data to show for selected filters.")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><p style='font-size: 14px;'>Created with by <b>Jaykumar Girase ❤️</b><br>Data Analytics Intern | Unified Mentor Pvt. Ltd.</p></center>",
    unsafe_allow_html=True
)