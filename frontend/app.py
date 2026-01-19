import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000/plan"

st.set_page_config(
    page_title="AI Travel Planner",
    layout="wide"
)

# ================= GLOBAL CSS =================
st.markdown("""
<style>

/* Page background */
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    font-family: 'Segoe UI', sans-serif;
}

/* Title Banner */
.title-box {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    padding: 30px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}

.title-box h1 {
    font-size: 46px;
    margin-bottom: 5px;
}

.title-box p {
    font-size: 18px;
    opacity: 0.9;
}

/* Form card */
.form-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.1);
    margin-bottom: 40px;
}

/* Plan card */
.plan-card {
    background: white;
    padding: 28px;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    margin-bottom: 30px;
}

.plan-header {
    font-size: 26px;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 10px;
}

/* Cost row */
.cost-row {
    display: flex;
    justify-content: space-between;
    font-weight: 600;
    color: #111827;
    margin-bottom: 12px;
}

/* Day card */
.day-card {
    background: #f1f5f9;
    padding: 18px;
    border-radius: 16px;
    margin-top: 14px;
}

/* Budget warning */
.warning {
    background: #fee2e2;
    color: #991b1b;
    padding: 10px;
    border-radius: 10px;
    font-weight: 600;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("""
<div class="title-box">
    <h1>🌍 AI Travel Planner</h1>
    <p>Smart • Budget-friendly • Indian Trips</p>
</div>
""", unsafe_allow_html=True)

# ================= FORM =================
st.markdown('<div class="form-card">', unsafe_allow_html=True)

with st.form("trip_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        from_city = st.text_input("🚩 From City", "Pune")
    with c2:
        to_city = st.text_input("🎯 To City", "Goa")
    with c3:
        days = st.number_input("📅 Days", 1, 10, 2)

    c4, c5 = st.columns(2)
    with c4:
        budget = st.number_input("💰 Budget (₹)", 1000, 50000, 8000, step=500)
    with c5:
        transport = st.selectbox("🚍 Transport Mode", ["train", "bus", "flight", "private"])

    submit = st.form_submit_button("✨ Generate Trip Plans")

st.markdown('</div>', unsafe_allow_html=True)

# ================= API CALL =================
if submit:
    with st.spinner("AI is planning your trip..."):
        res = requests.post(BACKEND_URL, json={
            "from_city": from_city,
            "to_city": to_city,
            "days": days,
            "budget": budget,
            "transport_mode": transport
        })

        data = res.json()
        plans = data.get("plans", [])

    st.success("✅ Trip plans generated successfully!")

    for plan in plans:
        st.markdown('<div class="plan-card">', unsafe_allow_html=True)

        st.markdown(
            f"<div class='plan-header'>Plan {plan['planId']}</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class='cost-row'>
                <span>🚍 Transport: ₹{plan['transportCost']}</span>
                <span>💰 Total: ₹{plan['totalCost']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if plan.get("budgetWarning"):
            st.markdown("<div class='warning'>⚠ Budget Exceeded</div>", unsafe_allow_html=True)

        for day in plan["days"]:
            st.markdown('<div class="day-card">', unsafe_allow_html=True)
            st.markdown(f"### Day {day['day']}")
            st.write("📍 **Spots:**", ", ".join(day["spots"]))
            st.write("🍴 **Restaurants:**", ", ".join(day["restaurants"]))
            st.write("🏨 **Stay Options:**")
            for h in day["stay"]:
                st.write("•", h)
            st.write("💵 **Day Cost:** ₹", day["dayCost"])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
