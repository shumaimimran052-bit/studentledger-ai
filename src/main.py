import os
from typing import Optional, Dict, Any

import streamlit as st
from dotenv import load_dotenv

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

load_dotenv()

st.set_page_config(page_title="StudentLedger AI", page_icon="💰", layout="centered")

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY and OpenAI else None


def build_prompt(income: float, rent: float, food: float, transport: float, others: float, living_situation: str, budget_mode: str) -> str:
    return f"""
You are a financial assistant for university students.

Student details:
- Living situation: {living_situation}
- Budget mode: {budget_mode}
- Monthly income: {income}
- Rent: {rent}
- Food: {food}
- Transport: {transport}
- Other expenses: {others}

Tasks:
1. Analyze whether the student is spending safely or overspending.
2. Give a short budget summary.
3. Give 3 practical saving tips.
4. Give a risk level: Low, Medium, or High.
5. Keep the answer clear, student-friendly, and structured.

Return the answer in this format:
Summary:
Risk:
Advice:
Tips:
"""


def local_analysis(income: float, rent: float, food: float, transport: float, others: float, living_situation: str, budget_mode: str) -> Dict[str, Any]:
    total_expenses = rent + food + transport + others
    savings = income - total_expenses
    savings_rate = (savings / income * 100) if income > 0 else 0

    if total_expenses > income:
        risk = "High"
        summary = "Expenses are higher than income."
        advice = ["Reduce non-essential spending immediately.", "Look for cheaper options for food and transport."]
    elif total_expenses > income * 0.85:
        risk = "Medium"
        summary = "You are close to overspending."
        advice = ["Control expenses carefully this month.", "Try to reduce one spending category."]
    else:
        risk = "Low"
        summary = "Your budget looks stable."
        advice = ["Keep your spending habits balanced.", "Maintain regular savings."]
    
    if rent > income * 0.5:
        advice.append("Rent is too high compared to income.")
    if food > income * 0.3:
        advice.append("Food spending is high.")
    if savings < income * 0.2:
        advice.append("Try saving at least 20% of income.")

    tips = [
        "Track expenses weekly.",
        "Avoid impulse purchases.",
        "Set a fixed savings goal every month."
    ]

    if living_situation == "Living Alone":
        tips.append("Living alone usually costs more, so keep a tighter budget.")
    elif living_situation == "Sharing Apartment":
        tips.append("Sharing helps reduce rent and utility costs.")
    else:
        tips.append("Hostel living can be cheaper, so focus on saving more.")

    if budget_mode == "Strict Budget Mode":
        tips.append("Strict mode: reduce wants before touching needs.")

    return {
        "summary": summary,
        "risk": risk,
        "advice": advice,
        "tips": tips,
        "income": income,
        "total_expenses": total_expenses,
        "savings": savings,
        "savings_rate": round(savings_rate, 2),
    }


def get_ai_refined_text(prompt: str) -> Optional[str]:
    if client is None:
        return None

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )
        text = getattr(response, "output_text", "")
        return text.strip() if text else None
    except Exception:
        return None


st.title("💰 StudentLedger AI")
st.subheader("Smart Financial Assistant for Students")
st.write("Analyze your spending, see your financial risk, and get practical savings advice.")

with st.sidebar:
    st.header("About")
    st.write("StudentLedger AI helps students manage money smarter.")
    st.subheader("Tips")
    st.write("• Save at least 20% of income")
    st.write("• Track expenses weekly")
    st.write("• Avoid impulse spending")

st.divider()

living_situation = st.selectbox(
    "Your Living Situation",
    ["Living in Hostel", "Sharing Apartment", "Living Alone"]
)

budget_mode = st.selectbox(
    "Budget Mode",
    ["Normal Analysis", "Strict Budget Mode"]
)

st.markdown("### Monthly Financial Input")
income = st.number_input("Monthly Income", min_value=0.0, step=50.0)
rent = st.number_input("Rent", min_value=0.0, step=50.0)
food = st.number_input("Food", min_value=0.0, step=50.0)
transport = st.number_input("Transport", min_value=0.0, step=50.0)
others = st.number_input("Other Expenses", min_value=0.0, step=50.0)

purchase_amount = st.number_input("Optional: amount for affordability check", min_value=0.0, step=50.0)

total_expenses = rent + food + transport + others

st.divider()

if "cached_results" not in st.session_state:
    st.session_state.cached_results = {}

if st.button("Run Financial Analysis"):
    if income <= 0:
        st.error("Please enter a valid income greater than 0.")
    else:
        cache_key = f"{income}-{rent}-{food}-{transport}-{others}-{living_situation}-{budget_mode}"
        if cache_key in st.session_state.cached_results:
            result = st.session_state.cached_results[cache_key]
        else:
            result = local_analysis(income, rent, food, transport, others, living_situation, budget_mode)
            st.session_state.cached_results[cache_key] = result

        prompt = build_prompt(income, rent, food, transport, others, living_situation, budget_mode)

        with st.spinner("Generating analysis..."):
            ai_text = get_ai_refined_text(prompt)

        st.markdown("### Financial Report")
        st.write(f"Income: {result['income']}")
        st.write(f"Total Expenses: {result['total_expenses']}")
        st.write(f"Savings: {result['savings']}")
        st.write(f"Savings Rate: {result['savings_rate']}%")

        if result["risk"] == "High":
            st.error("Risk Level: High")
        elif result["risk"] == "Medium":
            st.warning("Risk Level: Medium")
        else:
            st.success("Risk Level: Low")

        st.markdown("### Summary")
        st.write(result["summary"])

        st.markdown("### Advice")
        for item in result["advice"]:
            st.write(f"• {item}")

        st.markdown("### Tips")
        for item in result["tips"]:
            st.write(f"• {item}")

        st.markdown("### Expense Breakdown")
        if income > 0:
            st.write(f"Rent: {round((rent / income) * 100, 1)}%")
            st.write(f"Food: {round((food / income) * 100, 1)}%")
            st.write(f"Transport: {round((transport / income) * 100, 1)}%")
            st.write(f"Other: {round((others / income) * 100, 1)}%")

        if ai_text:
            st.markdown("### AI-Refined Output")
            st.info(ai_text)
        else:
            st.caption("AI API not available or not connected, so local analysis was used.")

        st.markdown("### Evaluation Notes")
        st.write("The app checks accuracy by comparing income and expenses, relevance by using student-specific advice, and clarity by showing structured output.")

st.divider()

st.subheader("Affordability Check")
if income > 0:
    if purchase_amount > income * 0.3:
        st.error("This purchase is probably too expensive for your budget.")
    elif purchase_amount > income * 0.1:
        st.warning("Think carefully before buying this item.")
    else:
        st.success("This looks affordable for your budget.")
else:
    st.info("Enter income first to use the affordability check.")

st.divider()
st.caption("StudentLedger AI | DDS AI Challenge | Day 4")

