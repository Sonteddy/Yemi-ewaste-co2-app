
import streamlit as st
import pandas as pd
import os

# CO2 saved per item type
CO2_VALUES = {
    "Mobile Phone": 4.2,
    "Laptop": 12.5,
    "Charger": 0.5,
    "Keyboard": 1.1,
    "Headphone": 0.7
}

# File to store data
DATA_FILE = "ewaste_data.csv"

# Load existing data or initialize empty dataframe
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Item", "Quantity", "CO2_Saved"])

# Streamlit UI
st.title("🌍 Smart E-Waste Hero - CO₂ Calculator")
st.markdown("Calculate and track how much CO₂ you're saving by recycling e-waste.")

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

# Display total CO2 saved
total_saved = df["CO2_Saved"].sum()
st.metric("🌱 Total CO₂ Saved", f"{total_saved:.2f} kg")

# Show data table
st.subheader("📊 Saved Entries")
st.dataframe(df)

# Charts
st.subheader("📈 CO₂ Saved by Item Type")
if not df.empty:
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
    st.info("No data yet. Enter some above to begin tracking.")
