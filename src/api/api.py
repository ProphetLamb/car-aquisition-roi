import routes.prediction
from starlette.routing import Mount, Route

get_prediction_data = routes.prediction.get_prediction_data

api_routes = Mount("", routes=[
    Route("/prediction", get_prediction_data, methods=["GET"])
])
