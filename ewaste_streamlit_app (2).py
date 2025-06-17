import streamlit as st
import pandas as pd
import os

# Constants
CO2_VALUES = {
    "Mobile Phone": 4.2,
    "Laptop": 12.5,
    "Charger": 0.5,
    "Keyboard": 1.1,
    "Headphone": 0.7
}
DATA_FILE = "ewaste_data.csv"

# Load existing data or create new
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Item", "Quantity", "CO2_Saved"])

# Main app
st.title("🌍 Smart E-Waste Hero - CO₂ Calculator")

# Input form
with st.form("co2_form"):
    item = st.selectbox("Select E-Waste Item", list(CO2_VALUES.keys()))
    quantity = st.number_input("Enter Quantity", min_value=1, value=1)
    submitted = st.form_submit_button("Calculate and Save")

    if submitted:
        co2_saved = CO2_VALUES[item] * quantity
        new_data = pd.DataFrame([[item, quantity, co2_saved]], columns=["Item", "Quantity", "CO2_Saved"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Saved! You saved {co2_saved:.2f} kg of CO₂ by recycling {quantity} {item}(s).")

# Total CO2 saved
st.metric("🌱 Total CO₂ Saved", f"{df['CO2_Saved'].sum():.2f} kg")

# Show table
st.subheader("📊 Saved Entries")
st.dataframe(df)

# Deletion tools
st.subheader("🧹 Manage Saved Data")

if not df.empty:
    row_to_delete = st.number_input("Enter row number to delete (starting from 0)", min_value=0, max_value=len(df)-1, step=1)
    if st.button("🗑️ Delete Selected Row"):
        df = df.drop(index=row_to_delete).reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Selected row deleted. Please refresh the app to see changes.")

    if st.button("❌ Clear All Data"):
        df = pd.DataFrame(columns=["Item", "Quantity", "CO2_Saved"])
        df.to_csv(DATA_FILE, index=False)
        st.success("All data cleared. Please refresh the app.")
else:
    st.info("No data available to manage.")

# Charts
if not df.empty:
    st.subheader("📈 CO₂ Saved by Item Type")
    chart_data = df.groupby("Item")["CO2_Saved"].sum().reset_index()
    st.bar_chart(chart_data.set_index("Item"))

    st.subheader("🥧 CO₂ Contribution by Item Type")
    st.plotly_chart({
        "data": [{
            "labels": chart_data["Item"],
            "values": chart_data["CO2_Saved"],
            "type": "pie"
        }],
        "layout": {"title": "CO₂ Distribution"}
    })
else:
    st.info("No chart data available.")