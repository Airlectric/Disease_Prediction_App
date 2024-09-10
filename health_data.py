import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def historical_health_data_page():
    st.title("Historical Health Data")
    st.write("Visualizing your health data over time.")

    # Example health data visualization
    dates = pd.date_range(start="2023-01-01", periods=30, freq='D')
    values = np.random.randint(1, 100, size=30)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o')
    plt.title('Health Metrics Over Time')
    plt.xlabel('Date')
    plt.ylabel('Health Metric')
    plt.grid()
    st.pyplot(plt)
