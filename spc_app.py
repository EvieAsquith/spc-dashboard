import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# File to store data
DATA_FILE = "spc_data.csv"

# Create the data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Timestamp", "Machine", "Part", "Nominal", "Measured"]).to_csv(DATA_FILE, index=False)

# Streamlit interface
st.title("🛠️ SPC Machine Entry")

# Inputs
machine = st.selectbox("Select Machine", ["Machine 1", "Machine 2", "Machine 3"])
part = st.text_input("Part Number")
nominal = st.number_input("Nominal Dimension (mm)", format="%.3f")
measured = st.number_input("Measured Dimension (mm)", format="%.3f")
submit = st.button("Submit")

# Save to CSV
if submit:
    new_row = pd.DataFrame([{
        "Timestamp": datetime.now(),
        "Machine": machine,
        "Part": part,
        "Nominal": nominal,
        "Measured": measured
    }])
    new_row.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success("✅ Measurement saved!")

# Load and show recent data
st.subheader("📋 Recent Measurements")
df = pd.read_csv(DATA_FILE)
st.dataframe(df.tail(10))

# Plot control chart
st.subheader("📈 Live SPC Chart (I-Chart)")
selected_machine = st.selectbox("Select Machine for Chart", df["Machine"].unique())

df_machine = df[df["Machine"] == selected_machine]
df_machine["Deviation"] = df_machine["Measured"] - df_machine["Nominal"]

if not df_machine.empty:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_machine["Timestamp"], df_machine["Deviation"], marker='o', label="Deviation")

    # Calculate statistics
mean = df['Recorded Dimension'].mean()
std_dev = df['Recorded Dimension'].std()
ucl = mean + 3 * std_dev
lcl = mean - 3 * std_dev

# Display calculated stats
st.write(f"Mean: {mean:.3f}")
st.write(f"Standard Deviation: {std_dev:.3f}")
st.write(f"UCL: {ucl:.3f}")
st.write(f"LCL: {lcl:.3f}")

# Plot with UCL/LCL
fig, ax = plt.subplots()
ax.plot(df['Timestamp'], df['Recorded Dimension'], marker='o', label='Recorded')
ax.axhline(mean, color='green', linestyle='--', label='Mean')
ax.axhline(ucl, color='red', linestyle='--', label='UCL (+3σ)')
ax.axhline(lcl, color='red', linestyle='--', label='LCL (-3σ)')
ax.set_xlabel("Timestamp")
ax.set_ylabel("Dimension (mm)")
ax.set_title("SPC Chart")
ax.legend()
st.pyplot(fig)

