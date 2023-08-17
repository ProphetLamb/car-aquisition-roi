from dataclasses import dataclass
import pandas as pd
import typing as t

@dataclass
class PredictionParameters:
    """Parameters for the prediction of the cost of a car over time.

    @param purchase_years: The number of years the car is used.
    @param purchase_new_price: The price of a new car.
    @param purchase_used_price: The price of a used car.
    @param leasing_cost_per_month: The cost of leasing a car per month.
    @param leasing_switch_cost: The cost of switching a car.
    @param leasing_years: The number of years a car is leased.
    @param repair_cost_per_year: The cost of repairing a car per year.
    @param repair_free_years: The number of years a car is free of repair.
    @param purchase_used_age: The age of a used car in years.
    """
    purchase_years: int
    purchase_new_price: int
    purchase_used_price: int
    purchase_used_age: int
    leasing_cost_per_month: int
    leasing_switch_cost: int
    leasing_years: int
    repair_cost_per_year: int
    repair_free_years: int

    def ensure_valid(self):
        self.purchase_years = int(self.purchase_years)
        self.purchase_new_price = int(self.purchase_new_price)
        self.purchase_used_price = int(self.purchase_used_price)
        self.purchase_used_age = int(self.purchase_used_age)
        self.leasing_cost_per_month = int(self.leasing_cost_per_month)
        self.leasing_switch_cost = int(self.leasing_switch_cost)
        self.leasing_years = int(self.leasing_years)
        self.repair_cost_per_year = int(self.repair_cost_per_year)
        self.repair_free_years = int(self.repair_free_years)
        assert self.purchase_years > 0, "purchase_years must be greater than 0"
        assert self.purchase_new_price > 0, "purchase_new_price must be greater than 0"
        assert self.purchase_used_price > 0, "purchase_used_price must be greater than 0"
        assert self.purchase_used_age >= 0, "purchase_used_age must be greater than or equal to 0"
        assert self.leasing_cost_per_month > 0, "leasing_cost_per_month must be greater than 0"
        assert self.leasing_switch_cost > 0, "leasing_switch_cost must be greater than 0"
        assert self.leasing_years > 0, "leasing_years must be greater than 0"
        assert self.repair_cost_per_year >= 0, "repair_cost_per_year must be greater than or equal to 0"
        assert self.repair_free_years >= 0, "repair_free_years must be greater than or equal to 0"

@dataclass
class PredictionResult:
    """A data frame with the cost of a car over time.
        - year: The numeric time axis in years.
        - month: The numeric time axis in months.
        - cost_used_purchase: The absolute cost of a used car at a given time.
        - cost_new_purchase: The absolute cost of a new car at a given time.
        - cost_leasing: The absolute cost of leasing a car at a given time.
    """
    year: t.List[float]
    month: t.List[int]
    cost_used_purchase: t.List[float]
    cost_new_purchase: t.List[float]
    cost_leasing: t.List[float]


def create_prediction_data_frame(params: PredictionParameters) -> PredictionResult:
    """Create a data frame with the cost of a car over time.

        @return: A data frame with the cost of a car over time.
            - year: The numeric time axis in years.
            - month: The numeric time axis in months.
            - cost_used_purchase: The absolute cost of a used car at a given time.
            - cost_new_purchase: The absolute cost of a new car at a given time.
            - cost_leasing: The absolute cost of leasing a car at a given time.
    """
    params.ensure_valid()

    def cost_purchase(age_month, price, initial_years):
        years = params.purchase_years - initial_years
        car_count = age_month // (years * 12) + 1
        car_age_months = age_month % (years * 12)

        cost_purchase = car_count * price

        car_repairfree_months = max(0, params.repair_free_years - initial_years) * 12
        repair_months = max(0, years * 12 - car_repairfree_months) * (car_count - 1)
        repair_months += max(0, car_age_months - car_repairfree_months)
        cost_repair  = repair_months * params.repair_cost_per_year / 12

        return cost_purchase + cost_repair

    def cost_leasing(age_month):
        car_count = (age_month - 1) // (params.leasing_years * 12) + 1
        switch_cost = car_count * params.leasing_switch_cost
        rate_cost = age_month * params.leasing_cost_per_month
        return switch_cost + rate_cost

    df = pd.DataFrame()
    df['year'] = range(1, 60)
    df['year'] = df['year'] / 2
    df['month'] = df['year'] * 12
    df['cost_used_purchase'] = df['month'].apply(
        lambda x: cost_purchase(x, params.purchase_used_price, params.purchase_used_age))
    df['cost_new_purchase'] = df['month'].apply(
        lambda x: cost_purchase(x, params.purchase_new_price, 0))
    df['cost_leasing'] = df['month'].apply(lambda x: cost_leasing(x))
    return PredictionResult(
        df['year'].tolist(),
        df['month'].tolist(),
        df['cost_used_purchase'].tolist(),
        df['cost_new_purchase'].tolist(),
        df['cost_leasing'].tolist()
    )
