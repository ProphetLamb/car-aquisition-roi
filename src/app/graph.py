import json
from dash import Dash, html, dcc, callback, clientside_callback, ClientsideFunction, Output, Input
import plotly.graph_objects as go

leasing_cost_per_month = 315
leasing_switch_cost = 500
leasing_years = 2
purchase_years = 10
purchase_new_price = 31000
purchase_used_price = 22000
purchase_used_age = 2
repair_cost_per_year = 1500
repair_free_years = 3

@callback(
    Output('graph-content', 'figure'),
    Input('slider_purchase_years', 'value'),
    Input('input_purchase_new_price', 'value'),
    Input('input_purchase_used_price', 'value'),
    Input('input_leasing_cost_per_month', 'value'),
    Input('input_leasing_switch_cost', 'value'),
    Input('slider_leasing_years', 'value'),
    Input('input_repair_cost_per_year', 'value'),
    Input('slider_repair_free_years', 'value'),
    Input('slider_purchase_used_age', 'value')
)
def update_graph(
    purchase_years,
        purchase_new_price,
        purchase_used_price,
        leasing_cost_per_month,
        leasing_switch_cost,
        leasing_years,
        repair_cost_per_year,
        repair_free_years,
        purchase_used_age
):
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
    
    
    
    return fig


def layout():
    # number input leasing_cost_per_month from 100 to 1000 in steps of 10
    input_leasing_cost_per_month = dcc.Input(
        type='number',
        min=100,
        max=5000,
        step=5,
        value=leasing_cost_per_month,
        id='input_leasing_cost_per_month'
    )
    # leasing_switch_cost from 0 to 1000 in steps of 100
    input_leasing_switch_cost = dcc.Input(
        type='number',
        min=0,
        max=10000,
        step=100,
        value=leasing_switch_cost,
        id='input_leasing_switch_cost'
    )
    # leasing_years from 1 to 4 in steps of 1
    slider_leasing_years = dcc.Slider(
        min=1,
        max=6,
        step=1,
        value=leasing_years,
        marks={i: str(i) for i in range(1, 6+1, 1)},
        id='slider_leasing_years'
    )
    # purchase_years from 5 to 20 in steps of 1
    slider_purchase_years = dcc.Slider(
        min=5,
        max=20,
        step=1,
        value=purchase_years,
        marks={i: str(i) for i in range(5, 20+1, 2)},
        id='slider_purchase_years'
    )
    # repair_cost_per_year from 0 to 5000 in steps of 100
    input_repair_cost_per_year = dcc.Input(
        type='number',
        min=0,
        max=10000,
        step=100,
        value=repair_cost_per_year,
        id='input_repair_cost_per_year'
    )
    # repair_free_years from 0 to 10 in steps of 1
    slider_repair_free_years = dcc.Slider(
        min=0,
        max=10,
        step=1,
        value=repair_free_years,
        marks={i: str(i) for i in range(0, 10+1, 1)},
        id='slider_repair_free_years'
    )
    # purchase_new_price from 10000 to 100000 in steps of 1000
    input_purchase_new_price = dcc.Input(
        type='number',
        min=10000,
        max=4000000,
        step=1000,
        value=purchase_new_price,
        id='input_purchase_new_price'
    )
    # purchase_used_price from 10000 to 100000 in steps of 1000
    input_purchase_used_price = dcc.Input(
        type='number',
        min=10000,
        max=4000000,
        step=1000,
        value=purchase_used_price,
        id='input_purchase_used_price'
    )
    # purchase_used_age from 0 to 10 in steps of 1
    slider_purchase_used_age = dcc.Slider(
        min=0,
        max=10,
        step=1,
        value=purchase_used_age,
        marks={i: str(i) for i in range(0, 10+1, 1)},
        id='slider_purchase_used_age'
    )

    def slider_wrapper(slider):
        return html.Div(slider, className='outline')

    return html.Div(
        [
            html.Header(
            html.H1(
                'Kostenvergleich zwischen Gebraucht- und Neuwagenkauf und Leasing'),
            ),
            html.Form([
                    html.H2('Leasing', ),
                html.Div([
                    html.Label([
                        'Leasingrate pro Monat',
                        input_leasing_cost_per_month
                    ],
                        htmlFor='input_leasing_cost_per_month',
                    ),
                    html.Label([
                        'Kosten für Fahrzeugwechsel',
                        input_leasing_switch_cost
                    ],
                        htmlFor='input_leasing_switch_cost',
                    ),
                    html.Label(
                        [
                            'Laufzeit in Jahren',
                            slider_wrapper(slider_leasing_years)
                        ],
                        htmlFor='slider_leasing_years',
                    ),
                ],
                    className='grid'
                ),
                    html.H2('Kauf'),
                html.Div([
                    html.Label(
                        ['Nutzungsdauer in Jahren', slider_wrapper(slider_purchase_years)],
                        htmlFor='slider_purchase_years',
                    ),
                    html.Label(
                        ['Neupreis', input_purchase_new_price],
                        htmlFor='input_purchase_new_price',
                    ),
                    html.Label(
                        ['Gebrauchtwagenpreis', input_purchase_used_price],
                        htmlFor='input_purchase_used_price',
                    ),
                    html.Label(
                        ['Gebrauchtwagens Alter in Jahren',
                            slider_wrapper(slider_purchase_used_age)],
                        htmlFor='slider_purchase_used_age',
                    ),
                ],
                    className='grid'),
                    html.H2('Instandhaltung'),
                html.Div([
                    html.Label(
                        ['Reparaturkosten pro Jahr', input_repair_cost_per_year],
                        htmlFor='input_repair_cost_per_year',
                    ),
                    html.Label(
                        ['Jahre ohne Reparatur', slider_wrapper(slider_repair_free_years)],
                        htmlFor='slider_repair_free_years',
                    ),
                ],
                    className='grid'),
            ],
            ),
            dcc.Graph(id='graph-content'),
        ],
        className='container',
    )
