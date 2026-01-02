# app.py - Streamlit Home Budget Tracker
import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Home Budget Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #1f77b4; text-align: center; margin-bottom: 2rem;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; color: white;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('home_budget.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        # Default data from original message
        data = [
            {'category': 'Krishna', 'amount': 7000, 'date': '2026-01-02'},
            {'category': 'SBI', 'amount': 3000, 'date': '2026-01-02'},
            {'category': 'Suman', 'amount': 2500, 'date': '2026-01-02'},
            {'category': 'Car wash', 'amount': 600, 'date': '2026-01-02'},
            {'category': 'Milk', 'amount': 4500, 'date': '2026-01-02'},
            {'category': 'Grocery', 'amount': 7000, 'date': '2026-01-02'},
            {'category': 'Vegetable', 'amount': 3500, 'date': '2026-01-02'},
            {'category': 'Fruits', 'amount': 2500, 'date': '2026-01-02'},
            {'category': 'Nonveg', 'amount': 2500, 'date': '2026-01-02'},
            {'category': 'Medicine', 'amount': 2000, 'date': '2026-01-02'},
            {'category': 'Airtel payment', 'amount': 2300, 'date': '2026-01-02'}
        ]
        return pd.DataFrame(data)

def save_data(df):
    df.to_csv('home_budget.csv', index=False)

# Header
st.markdown('<h1 class="main-header">🏠 Home Budget Tracker</h1>', unsafe_allow_html=True)

# Load data
df = load_data()

# Sidebar for adding expenses
st.sidebar.header("➕ Add New Expense")
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", 
                               ['Krishna', 'SBI', 'Suman', 'Car wash', 'Milk', 'Grocery', 
                                'Vegetable', 'Fruits', 'Nonveg', 'Medicine', 'Airtel payment', 'Other'],
                               key='add_cat')
    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.0, value=1000.0, step=100.0, key='add_amt')
    
    date_input = st.date_input("Date", value=date.today(), key='add_date')
    
    if st.button("Add Expense", type="primary"):
        new_row = pd.DataFrame({
            'category': [category if category != 'Other' else st.text_input('New Category')],
            'amount': [amount],
            'date': [date_input]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success("Expense added!")
        st.rerun()

# Metrics
col1, col2, col3, col4 = st.columns(4)
total_spent = df['amount'].sum()
current_month = df['date'].dt.to_period('M').max()
monthly_spent = df[df['date'].dt.to_period('M') == current_month]['amount'].sum()
avg_category = df.groupby('category')['amount'].mean().mean()

with col1:
    st.metric("Total Spent", f"₹{total_spent:,.0f}")
with col2:
    st.metric("This Month", f"₹{monthly_spent:,.0f}")
with col3:
    st.metric("Avg per Category", f"₹{avg_category:,.0f}")
with col4:
    st.metric("Items", len(df))

# Charts
col1, col2 = st.columns(2)

with col1:
    # Pie chart
    cat_summary = df.groupby('category')['amount'].sum().reset_index()
    fig_pie = px.pie(cat_summary, values='amount', names='category', 
                     title="Expense Breakdown", hole=0.3)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Bar chart by month
    df['month'] = df['date'].dt.to_period('M')
    monthly_summary = df.groupby('month')['amount'].sum().reset_index()
    monthly_summary['month'] = monthly_summary['month'].astype(str)
    fig_bar = px.bar(monthly_summary, x='month', y='amount', 
                     title="Monthly Spending", color='amount')
    st.plotly_chart(fig_bar, use_container_width=True)

# Data table
st.subheader("📋 All Expenses")
st.dataframe(df.sort_values('date', ascending=False), use_container_width=True)

# Download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", csv, "home_budget.csv", "text/csv")

# JSON export
json_data = df.to_dict('records')
st.json(json_data)
