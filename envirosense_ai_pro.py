
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="EnviroSense AI Pro", layout="wide")

REPORTS_FILE = Path("reports.csv")
MARKET_FILE = Path("marketplace.csv")

def load_csv(path, columns):
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=columns)

reports_df = load_csv(REPORTS_FILE, ["Time","Issue","Location","Severity","Priority","Description","AI Insight"])
market_df = load_csv(MARKET_FILE, ["Time","Material","Quantity","Location","Price","Seller"])

def classify_priority(issue_type, severity):
    if issue_type == "Blocked Drainage" and severity == "High":
        return "Urgent"
    if severity == "Medium":
        return "Moderate"
    return "Normal"

def ai_insight(issue_type, severity, description):
    text = description.lower()
    if "plastic" in text:
        return "AI insight: Plastic accumulation suggests drainage blockage risk and recycling opportunity."
    if "metal" in text:
        return "AI insight: Metal waste may have resale value in fabrication markets."
    if issue_type == "Construction Waste":
        return "AI insight: This waste may be reusable in local fabrication or resale markets."
    if severity == "High":
        return "AI insight: Immediate intervention recommended to reduce environmental risk."
    return "AI insight: Monitor and schedule community response."

st.title("EnviroSense AI Pro: Environmental Intelligence for Safer and Cleaner Cities 🌍")
st.markdown("<p style='font-size:12px;'>Built for environmental innovation in Nigeria</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Environmental Reports", "AI Dashboard", "Waste Marketplace"])

with tab1:
    st.subheader("Submit Environmental Report")
    with st.form("report_form"):
        issue_type = st.selectbox("Issue Type", ["Blocked Drainage", "Construction Waste"])
        location = st.text_input("Location")
        severity = st.selectbox("Severity", ["Low", "Medium", "High"])
        description = st.text_area("Description")
        image = st.file_uploader("Upload image (optional)", type=["png","jpg","jpeg"])
        submitted = st.form_submit_button("Submit Report")

    if submitted:
        priority = classify_priority(issue_type, severity)
        insight = ai_insight(issue_type, severity, description)
        new_row = {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Issue": issue_type,
            "Location": location,
            "Severity": severity,
            "Priority": priority,
            "Description": description,
            "AI Insight": insight
        }
        reports_df.loc[len(reports_df)] = new_row
        reports_df.to_csv(REPORTS_FILE, index=False)
        st.success("Report submitted successfully")
        st.write(insight)
        if image:
            st.image(image, caption="Uploaded environmental image")

with tab2:
    st.subheader("Live AI Dashboard")
    if not reports_df.empty:
        st.dataframe(reports_df, use_container_width=True)
        st.bar_chart(reports_df["Priority"].value_counts())
    else:
        st.info("No reports submitted yet.")

with tab3:
    st.subheader("Waste Listing Marketplace")
    with st.form("market_form"):
        material = st.text_input("Material")
        quantity = st.text_input("Quantity")
        market_location = st.text_input("Location")
        price = st.text_input("Price")
        seller = st.text_input("Seller Contact")
        market_submit = st.form_submit_button("List Material")

    if market_submit:
        new_market = {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Material": material,
            "Quantity": quantity,
            "Location": market_location,
            "Price": price,
            "Seller": seller
        }
        market_df.loc[len(market_df)] = new_market
        market_df.to_csv(MARKET_FILE, index=False)
        st.success("Material listed successfully")

    if not market_df.empty:
        st.dataframe(market_df, use_container_width=True)
    else:
        st.info("No waste materials listed yet.")
