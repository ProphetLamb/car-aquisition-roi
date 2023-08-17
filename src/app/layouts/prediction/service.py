from dataclasses import dataclass
import typing as t
import httpx
import base64

import cfg

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

async def get_prediction_data(params: PredictionParameters) -> PredictionResult:
    auth = httpx.BearerToken(base64.b64encode(cfg.client_id.encode("utf-8")).decode("utf-8"))
    response = await httpx.get(
        f"{cfg.api_endpoint}/prediction",
        params=params.__dict__,
        headers={"Authorization": auth}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to get prediction data: with status {response.status_code}")

    return PredictionResult(**response.json())
