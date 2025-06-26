import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="SPC Dashboard", layout="centered")

st.title("📏 Machine Shop SPC Dashboard")

# Set the path for data storage
DATA_PATH = "data.csv"

# Input form
with st.form("input_form"):
    st.subheader("Enter Measurement")
    nominal = st.number_input("Nominal Dimension", step=0.01, format="%.3f")
    recorded = st.number_input("Recorded Dimension", step=0.01, format="%.3f")
    submit = st.form_submit_button("Submit")

# Load or initialise data
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=["Nominal", "Recorded"])

# Append new data
if submit:
    new_data = pd.DataFrame([[nominal, recorded]], columns=["Nominal", "Recorded"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    st.success("Measurement submitted successfully!")

# Show chart if there is data
if not df.empty:
    st.subheader("Control Chart")

    mean = df["Recorded"].mean()
    std_dev = df["Recorded"].std()
    ucl = mean + 3 * std_dev
    lcl = mean - 3 * std_dev

    fig, ax = plt.subplots()
    ax.plot(df.index, df["Recorded"], marker='o', label="Recorded Dimension")
    ax.axhline(mean, color='green', linestyle='--', label="Mean")
    ax.axhline(ucl, color='red', linestyle='--', label="UCL (+3σ)")
    ax.axhline(lcl, color='red', linestyle='--', label="LCL (-3σ)")
    ax.set_title("SPC Chart")
    ax.set_xlabel("Sample Number")
    ax.set_ylabel("Dimension")
    ax.legend()
    st.pyplot(fig)

    # Show latest measurements
    st.subheader("Latest Entries")
    st.dataframe(df.tail(10))


