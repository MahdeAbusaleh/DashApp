import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Radiation exposure data (in millisieverts, mSv)
radiation_sources = {
    "Background Radiation (Annual Avg)": 3.0,
    "Chest X-ray": 0.1,
    "Dental X-ray": 0.005,
    "Mammogram": 0.4,
    "CT Scan (Abdomen)": 8.0,
    "Flight (NYC to LA)": 0.04,
    "Smoking (1 pack/day, Annual)": 70.0,
    "Fukushima Evacuation Zone (Annual)": 12.0,
}

df = pd.DataFrame(list(radiation_sources.items()), columns=["Source", "Dose (mSv)"])

# LNT vs. Threshold vs. Hormesis Models
dose_values = np.linspace(0, 100, 100)
lnt_risk = dose_values * 0.01
threshold_risk = np.piecewise(dose_values, [dose_values < 10, dose_values >= 10], [0, lambda x: (x-10)*0.01])
hormesis_risk = np.piecewise(dose_values, [dose_values < 10, dose_values >= 10], [lambda x: -0.005*x+0.05, lambda x: (x-10)*0.01])

# Layout for the app
app.layout = html.Div([
    html.H1("Understanding Radiation Exposure and Risk", style={'textAlign': 'center'}),

    html.H3("Radiation Exposure from Common Sources"),
    html.P("This chart shows the radiation dose from various common activities and sources."),
    dcc.Graph(
        figure={
            "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker_color='blue')],
            "layout": go.Layout(title="Radiation Dose Comparison (mSv)", xaxis_title="Source", yaxis_title="Dose (mSv)")
        }
    ),

    html.H3("Dose-Response Models: LNT vs. Threshold vs. Hormesis"),
    html.P("The following graph compares three models of radiation risk assessment: \n            Linear No-Threshold (LNT), which assumes all radiation is harmful; \n            the Threshold model, which assumes there is a safe level of exposure below which no harm occurs; \n            and the Hormesis model, which suggests low doses may be beneficial."),
    dcc.Graph(
        figure={
            "data": [
                go.Scatter(x=dose_values, y=lnt_risk, mode='lines', name='Linear No-Threshold (LNT)', line=dict(color='red')),
                go.Scatter(x=dose_values, y=threshold_risk, mode='lines', name='Threshold Model', line=dict(color='blue', dash='dash')),
                go.Scatter(x=dose_values, y=hormesis_risk, mode='lines', name='Hormesis Model', line=dict(color='green', dash='dot')),
            ],
            "layout": go.Layout(title="Radiation Dose-Response Models", xaxis_title="Radiation Dose (mSv)", yaxis_title="Relative Risk")
        }
    ),

    html.H3("Personal Radiation Exposure Calculator"),
    html.Label("Number of flights per year (NYC to LA equivalent):"),
    dcc.Slider(0, 50, 1, value=5, marks={i: str(i) for i in range(0, 51, 10)}, id='flight-slider', tooltip={"placement": "bottom", "always_visible": True}),
    html.Label("Number of chest X-rays per year:"),
    dcc.Slider(0, 10, 1, value=1, marks={i: str(i) for i in range(0, 11)}, id='xray-slider', tooltip={"placement": "bottom", "always_visible": True}),
    html.Div(id='total-dose-output', style={'fontSize': 20, 'marginTop': 20}),

    html.H3("Key Takeaways and References"),
    html.Ul([
        html.Li("Most people receive around 3 mSv of background radiation annually."),
        html.Li("The LNT model assumes all radiation is harmful, but other models suggest low doses may be harmless or beneficial."),
        html.Li("Understanding radiation exposure helps dispel myths and unnecessary fear."),
    ]),
    html.P("References: "),
    html.Ul([
        html.Li("BEIR VII Report"),
        html.Li("NCRP Publications"),
        html.Li("ICRP Reports"),
    ]),
    html.Footer("Created by Mahde Abusaleh. Data sourced from NCRP and ICRP publications.", style={"textAlign": "center", "marginTop": 40})
])

@app.callback(
    dash.Output("total-dose-output", "children"),
    [dash.Input("flight-slider", "value"), dash.Input("xray-slider", "value")]
)
def update_dose(flights, xrays):
    total_dose = (flights * 0.04) + (xrays * 0.1)
    return f"Your estimated annual radiation dose from selected activities: {total_dose:.2f} mSv"

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8080)


