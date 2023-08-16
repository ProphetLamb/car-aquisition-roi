import pandas as pd

def create_prediction_data_frame(
    purchase_years: int,
    purchase_new_price: int,
    purchase_used_price: int,
    leasing_cost_per_month: int,
    leasing_switch_cost: int,
    leasing_years: int,
    repair_cost_per_year: int,
    repair_free_years: int,
    purchase_used_age: int
) -> pd.DataFrame:
    """Create a data frame with the cost of a car over time.

        @param purchase_years: The number of years the car is used.
        @param purchase_new_price: The price of a new car.
        @param purchase_used_price: The price of a used car.
        @param leasing_cost_per_month: The cost of leasing a car per month.
        @param leasing_switch_cost: The cost of switching a car.
        @param leasing_years: The number of years a car is leased.
        @param repair_cost_per_year: The cost of repairing a car per year.
        @param repair_free_years: The number of years a car is free of repair.
        @param purchase_used_age: The age of a used car in years.

        @return: A data frame with the cost of a car over time.
            - year: The numeric time axis in years.
            - month: The numeric time axis in months.
            - cost_used_purchase: The absolute cost of a used car at a given time.
            - cost_new_purchase: The absolute cost of a new car at a given time.
            - cost_leasing: The absolute cost of leasing a car at a given time.
    """
    if (
        purchase_years is None or
        purchase_new_price is None or
        purchase_used_price is None or
        leasing_cost_per_month is None or
        leasing_switch_cost is None or
        leasing_years is None or
        repair_cost_per_year is None or
        repair_free_years is None or
        purchase_used_age is None
    ):
        return None

    def cost_purchase(age_month, price, initial_years):
        years = purchase_years - initial_years
        car_count = age_month // (years * 12) + 1
        car_age_months = age_month % (years * 12)

        cost_purchase = car_count * price

        car_repairfree_months = max(0, repair_free_years - initial_years) * 12
        repair_months = max(0, years * 12 - car_repairfree_months) * (car_count - 1)
        repair_months += max(0, car_age_months - car_repairfree_months)
        cost_repair  = repair_months * repair_cost_per_year / 12

        return cost_purchase + cost_repair

    def cost_leasing(age_month):
        car_count = (age_month - 1) // (leasing_years * 12) + 1
        switch_cost = car_count * leasing_switch_cost
        rate_cost = age_month * leasing_cost_per_month
        return switch_cost + rate_cost

    df = pd.DataFrame()
    df['year'] = range(1, 60)
    df['year'] = df['year'] / 2
    df['month'] = df['year'] * 12
    df['cost_used_purchase'] = df['month'].apply(
        lambda x: cost_purchase(x, purchase_used_price, purchase_used_age))
    df['cost_new_purchase'] = df['month'].apply(
        lambda x: cost_purchase(x, purchase_new_price, 0))
    df['cost_leasing'] = df['month'].apply(lambda x: cost_leasing(x))
    return df

