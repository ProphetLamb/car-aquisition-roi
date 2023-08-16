from dash import Dash, html, dcc, callback, clientside_callback, ClientsideFunction, Output, Input
import dash_mantine_components as dmc

import pathlib
import logging
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv('CAR_CLIENT_ID')
assert client_id, "A shared client id between the server and client is required"
debug = os.getenv('DEBUG', False)
origin = os.getenv('ORIGIN', 'http://127.0.0.1:3000')
host = origin.split('//')[1]
host, port = host.split(':')
port = int(port) if port else None
assert port, "A port must be specified in the ORIGIN environment variable"

def external_stylesheets():
    return [
        {
            'rel': 'stylesheet',
            'href': 'https://cdn.jsdelivr.net/npm/@picocss/pico@1.5.10/css/pico.min.css',
        }
    ]


def external_scripts():
    return [
        {
            'src': 'https://cdn.jsdelivr.net/npm/@picocss/pico@1.5.10/css/postcss.config.min.js'
        }
    ]

app = Dash(
    __name__,
    external_scripts=external_scripts(),
    external_stylesheets=external_stylesheets(),
)

clientside_callback(
    ClientsideFunction(namespace='handleData', function_name='getTimezone'),
    Output("timezone", "data"),
    Input("timezone", "id")
)

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark", "fontFamily": "'segoe ui', 'Inter', sans-serif"},
    children=[
        layout(),
        dcc.Store(id="timezone", storage_type="memory"),
        dcc.Store(id="pipe", storage_type="memory", data=origin),
    ]
)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug, dev_tools_ui=debug, dev_tools_props_check=debug)
