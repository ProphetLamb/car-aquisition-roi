import logging

from starlette.requests import Request
from starlette.responses import JSONResponse

from routes.prediction.service import create_prediction_data_frame, PredictionParameters

async def get_prediction_data(request: Request) -> JSONResponse:
    logging.info(f"Received get_prediction_data request")

    if (not request.user.is_authenticated):
        logging.error(f"Unauthenticated user: {request.user}")
        return JSONResponse({"error": "Not authenticated"}, status_code=401, headers={"WWW-Authenticate": "Bearer"})

    try:
        prediction_params = PredictionParameters(**request.query_params)
        prediction_params.ensure_valid()
    except Exception as error:
        logging.error(f"Invalid request parameters: {request.query_params}")
        return JSONResponse({"error": "Invalid request parameters"}, status_code=400)

    try:
        prediction_data = create_prediction_data_frame(prediction_params)
    except Exception as error:
        logging.error(f"Error while creating prediction data frame: {error}")
        return JSONResponse({"error": "Error while computing prediction data"}, status_code=500)

    logging.info(f"Returning prediction data")
    return JSONResponse(prediction_data.__dict__, status_code=200)
