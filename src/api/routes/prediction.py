import logging

from starlette.requests import Request
from starlette.responses import JSONResponse

import core

async def get_prediction_data(request: Request) -> JSONResponse:
    if (not request.user.is_authenticated):
        logging.error(f"Unauthenticated user: {request.user}")
        return JSONResponse({"error": "Not authenticated"}, status_code=401, headers={"WWW-Authenticate": "Bearer"})
    # call create prediction data frame function
    # purchase_years: int,
    # purchase_new_price: int,
    # purchase_used_price: int,
    # leasing_cost_per_month: int,
    # leasing_switch_cost: int,
    # leasing_years: int,
    # repair_cost_per_year: int,
    # repair_free_years: int,
    # purchase_used_age: int
    logging.info(f"Received request")
    prediction_data = None
    try:
        prediction_data = core.create_prediction_data_frame(
            request.query_params['purchase_years'],
            request.query_params['purchase_new_price'],
            request.query_params['purchase_used_price'],
            request.query_params['leasing_cost_per_month'],
            request.query_params['leasing_switch_cost'],
            request.query_params['leasing_years'],
            request.query_params['repair_cost_per_year'],
            request.query_params['repair_free_years'],
            request.query_params['purchase_used_age']
        )
    except Exception as error:
        logging.error(f"Error while creating prediction data frame: {error}")
        return JSONResponse({"error": "Error while computing prediction data"}, status_code=500)

    if prediction_data == None:
        logging.error(f"Invalid request parameters: {request.query_params}")
        return JSONResponse({"error": "Invalid request parameters"}, status_code=400)
    
    logging.info(f"Returning prediction data len({len(prediction_data)})")
    return JSONResponse(prediction_data.to_json(orient="records"), status_code=200)
