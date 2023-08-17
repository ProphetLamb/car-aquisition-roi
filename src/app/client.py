#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dash import Dash, html, dcc, callback, clientside_callback, ClientsideFunction, Output, Input
import dash_mantine_components as dmc
import cfg
import layouter

cfg.load()

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
        *layouter.app_layouts,
        dcc.Store(id="timezone", storage_type="memory"),
        dcc.Store(id="pipe", storage_type="memory", data=cfg.origin),
    ]
)

if __name__ == '__main__':
    app.run(host=cfg.host, port=cfg.port, debug=cfg.debug, dev_tools_ui=cfg.debug)
