import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="StudentLedger AI", layout="centered")

# ------------------ CLEAN DARK UI ------------------
st.markdown("""
<style>

/* FONT */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    color: #e2e8f0;
}

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* MAIN CONTAINER */
.block-container {
    background: rgba(15, 23, 42, 0.7);
    padding: 2rem;
    border-radius: 16px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.05);
}

/* METRIC CARDS */
div[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.9);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

/* BUTTON */
.stButton>button {
    border-radius: 10px;
    background: linear-gradient(90deg, #6366f1, #4f46e5);
    color: white;
    font-weight: 600;
    border: none;
    height: 3em;
    width: 100%;
}

/* INPUTS */
.stNumberInput input {
    background: rgba(30, 41, 59, 0.95);
    color: white !important;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* SELECT */
.stSelectbox div {
    background: rgba(30, 41, 59, 0.95) !important;
    color: white !important;
}

/* HEADERS */
h1 {
    text-align: center;
    color: #ffffff;
}

h3 {
    color: #e2e8f0;
}

/* TEXT */
p {
    text-align: center;
    color: #cbd5f5;
}

/* DIVIDER */
hr {
    border: 0.5px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<h1>💰 StudentLedger AI</h1>
<p>Smart budgeting for students</p>
""", unsafe_allow_html=True)

st.markdown("### 💼 Financial Dashboard")

# ------------------ INPUTS ------------------
col1, col2 = st.columns(2)

with col1:
    income = st.number_input("💵 Income", min_value=0)
    rent = st.number_input("🏠 Rent", min_value=0)
    food = st.number_input("🍔 Food", min_value=0)

with col2:
    transport = st.number_input("🚌 Transport", min_value=0)
    other = st.number_input("🛍 Other", min_value=0)

mode = st.selectbox("🧠 Financial Personality",
                    ["Conservative", "Balanced", "Risky"])

goal = st.number_input("🎯 Savings Goal (optional)", min_value=0)

# ------------------ BUTTON ------------------
if st.button("🔍 Analyze Budget"):

    if income <= 0:
        st.error("⚠️ Enter valid income")
        st.stop()

    total = rent + food + transport + other
    savings = income - total

    st.markdown("---")

    # SCORE
    if savings < 0:
        score = 20
    elif savings < income * 0.2:
        score = 50
    else:
        score = 85

    # ------------------ RESULTS ------------------
    st.subheader("📊 Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Expenses", total)
    c2.metric("Savings", savings)
    c3.metric("Score", f"{score}/100")

    st.progress(min(max(savings / income, 0), 1))

    # ------------------ STATUS ------------------
    if savings < 0:
        st.error("⚠️ Overspending")
    elif savings < income * 0.2:
        st.warning("⚠️ Low savings")
    else:
        st.success("✅ Good financial health")

    # ------------------ PREDICTION ------------------
    st.markdown("### 📅 Survival Prediction")

    if total > 0:
        daily = total / 30
        days = int(income / daily)

        if savings < 0:
            st.error(f"⚠️ Money may run out in {days} days")
        else:
            st.success(f"✅ Sustainable for {days} days")

    # ------------------ GOAL ------------------
    if goal > 0 and savings > 0:
        months = int(goal / savings)
        st.markdown("### 🎯 Goal Tracker")
        st.info(f"Reach your goal in ~ {months} months")

    # ------------------ BREAKDOWN ------------------
    st.markdown("### 📊 Spending Breakdown")

    if total > 0:
        st.write(f"🏠 Rent: {round((rent/total)*100)}%")
        st.write(f"🍔 Food: {round((food/total)*100)}%")
        st.write(f"🚌 Transport: {round((transport/total)*100)}%")
        st.write(f"🛍 Other: {round((other/total)*100)}%")

    # ------------------ INSIGHTS ------------------
    st.markdown("### 🧠 Insights")

    if rent > income * 0.5:
        st.write("👉 Rent is too high")
    if food > income * 0.3:
        st.write("👉 Food spending is high")
    if transport > income * 0.2:
        st.write("👉 Transport cost is high")

    # ------------------ STRATEGY ------------------
    st.markdown("### 🧠 Strategy")

    if mode == "Conservative":
        st.write("👉 Save aggressively, cut costs")
    elif mode == "Balanced":
        st.write("👉 Maintain balance")
    else:
        st.write("👉 Higher spending flexibility")

    # ------------------ FINAL ------------------
    st.markdown("### 💡 Recommendations")

    if savings < 0:
        st.write("- Reduce expenses immediately")
    elif savings < income * 0.2:
        st.write("- Improve saving discipline")
    else:
        st.write("- Consider investing")

    if total == 0:
        st.info("Add expenses for better insights")

    if income > 100000:
        st.warning("Unusual income input")

    st.markdown("---")
    st.success("Analysis complete ✅")
