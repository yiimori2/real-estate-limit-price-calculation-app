import numpy_financial as npf
import pandas as pd

INTEREST_RATES: list[float] = [0.02, 0.025, 0.03]  # 金利
REPAYMENT_PERIODS: list[int] = [10, 15, 20, 25]  # 返済期間(年）


class LimitPriceCalculator:
    def __init__(
        self,
        payment_ratio: float,
        sale_price: int,
        loan_amount: int,
        annual_rental_income: int,
    ):
        self.payment_ratio = payment_ratio
        self.sale_price = sale_price
        self.loan_amount = loan_amount
        self.annual_rental_income = annual_rental_income

    def create_df(self) -> pd.DataFrame:
        data = []
        for interest_rate in INTEREST_RATES:
            for repayment_period in REPAYMENT_PERIODS:
                required_yield = self._calc_required_yield(
                    interest_rate=interest_rate, repayment_period=repayment_period
                )
                limit_price = self._calc_limit_price(required_yield)
                d = {
                    "金利": interest_rate * 100,
                    "返済期間": repayment_period,
                    "必要利回り": required_yield * 100,
                    "指値": limit_price,
                }
                data.append(d)
        df = pd.DataFrame(data)
        return df

    def _calc_limit_price(self, required_yield: float) -> float:
        """
        指値を計算する
        指値 = 年間家賃収入 / 必要利回り
        """
        limit_price = self.annual_rental_income / required_yield
        return limit_price

    def _calc_required_yield(self, interest_rate: float, repayment_period: int) -> float:
        """
        必要利回りを計算する
        必要利回り = 年間返済額 / 返済比率 / 売出価格
        """
        annual_repayment_amount = self._calc_annual_repayment_amount(interest_rate, repayment_period)
        required_yield = annual_repayment_amount / self.payment_ratio / self.sale_price
        return round(required_yield, 3)

    def _calc_annual_repayment_amount(self, interest_rate: float, repayment_period: int) -> float:
        """年間返済額を計算する"""
        rate = interest_rate / 12  # 月利
        nper = repayment_period * 12  # 月数
        pv = self.loan_amount * 10000  # 残金
        pmt: float = -npf.pmt(rate, nper, pv)  # 毎月の返済金額
        return pmt * 12 / 10000
