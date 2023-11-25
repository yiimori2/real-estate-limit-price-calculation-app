import streamlit as st
from limit_price_calculator import LimitPriceCalculator

st.title("不動産指値計算アプリ")

st.number_input("売出価格（万円）", min_value=0, key="sale_price")
st.number_input("借入金額（万円）", min_value=0, key="loan_amount")
st.number_input("家賃収入（万円／年）", min_value=0, key="annual_rental_income")

sale_price = st.session_state.sale_price
loan_amount = st.session_state.loan_amount
annual_rental_income = st.session_state.annual_rental_income

PAYMENT_RATIOS: list[float] = [0.4, 0.45, 0.5]  # 返済比率

for payment_ratio in PAYMENT_RATIOS:
    if st.checkbox(f"返済比率{int(payment_ratio * 100)}%"):
        c = LimitPriceCalculator(
            payment_ratio=payment_ratio,
            sale_price=sale_price,
            loan_amount=loan_amount,
            annual_rental_income=annual_rental_income,
        )
        df = c.create_df()
        st.write(df)
