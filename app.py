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
threshold_risk = np.piecewise(dose_values, [dose_values < 10, dose_values >= 10], [0, lambda x: (x - 10) * 0.01])
hormesis_risk = np.piecewise(dose_values, [dose_values < 10, dose_values >= 10],
                             [lambda x: -0.005 * x + 0.05, lambda x: (x - 10) * 0.01])

# Layout for the app
app.layout = html.Div([
    html.H1("Understanding Radiation Exposure and Risk", style={'textAlign': 'center'}),
    html.H5("Created by Mahde Abusaleh", style={'textAlign': 'center', 'marginBottom': 20, 'color': 'gray'}),

# Navigation Bar (Updated to use html.A() for smooth scrolling)
html.Div([
    html.A('Exposure Sources | ', href='#exposure', style={'cursor': 'pointer', 'textDecoration': 'none'}),
    html.A('Dose-Response Models | ', href='#models', style={'cursor': 'pointer', 'textDecoration': 'none'}),
    html.A('Calculator | ', href='#calculator', style={'cursor': 'pointer', 'textDecoration': 'none'}),
    html.A('FAQ | ', href='#faq', style={'cursor': 'pointer', 'textDecoration': 'none'}),
    html.A('Conclusion', href='#conclusion', style={'cursor': 'pointer', 'textDecoration': 'none'})
], style={'textAlign': 'center', 'marginBottom': 20}),

# JavaScript for smooth scrolling
dcc.Markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                document.getElementById(targetId).scrollIntoView({ behavior: 'smooth' });
            });
        });
    });
    </script>
""", dangerously_allow_html=True),

    # Radiation Exposure Section
    html.Div(id='exposure', children=[
        html.H3("Radiation Exposure from Common Sources"),
        dcc.Graph(
            figure={
                "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker_color='blue')],
                "layout": go.Layout(title="Radiation Dose Comparison (mSv)", xaxis_title="Source",
                                    yaxis_title="Dose (mSv)")
            }
        ),
        html.P("The chart above compares radiation doses from common sources, providing insight into "
               "relative exposure levels."),
    ]),

    # Dose-Response Models Section
    html.Div(id='models', children=[
        html.H3("Dose-Response Models: LNT vs. Threshold vs. Hormesis"),
        dcc.Graph(
            figure={
                "data": [
                    go.Scatter(x=dose_values, y=lnt_risk, mode='lines', name='Linear No-Threshold (LNT)',
                               line=dict(color='red')),
                    go.Scatter(x=dose_values, y=threshold_risk, mode='lines', name='Threshold Model',
                               line=dict(color='blue', dash='dash')),
                    go.Scatter(x=dose_values, y=hormesis_risk, mode='lines', name='Hormesis Model',
                               line=dict(color='green', dash='dot')),
                ],
                "layout": go.Layout(title="Radiation Dose-Response Models", xaxis_title="Radiation Dose (mSv)",
                                    yaxis_title="Relative Risk")
            }
        ),
        html.P("The Linear No-Threshold (LNT) model assumes all radiation exposure carries some risk, no matter how "
               "small, while the Threshold model assumes there is a dose below which there is no risk. "
               "The Hormesis model proposes that low levels of radiation may be beneficial."),
    ]),

    # Calculator Section
    html.Div(id='calculator', children=[
        html.H3("Personal Radiation Exposure Calculator"),
        html.Label("Number of flights per year (NYC to LA equivalent):"),
        dcc.Slider(0, 50, 1, value=5, marks={i: str(i) for i in range(0, 51, 10)}, id='flight-slider'),
        html.Label("Number of chest X-rays per year:"),
        dcc.Slider(0, 10, 1, value=1, marks={i: str(i) for i in range(0, 11)}, id='xray-slider'),
        html.Div(id='total-dose-output', style={'fontSize': 20, 'marginTop': 20}),
    ]),

  # FAQ Section
html.Div(id='faq', children=[
    html.H3("Frequently Asked Questions (FAQ)"),
    
    html.Details([
        html.Summary("What is a millisievert (mSv)?"),
        html.P("A millisievert (mSv) is a unit used to measure radiation dose and assess potential health risks from exposure.")
    ]),
    
    html.Details([
        html.Summary("Is background radiation harmful?"),
        html.P("Background radiation is naturally occurring and typically not harmful at normal exposure levels. "
               "It comes from sources like cosmic rays and the Earth's crust.")
    ]),
    
    html.Details([
        html.Summary("What is the LNT model?"),
        html.P("The Linear No-Threshold (LNT) model assumes that all radiation exposure, no matter how small, "
               "increases the risk of cancer and other health effects.")
    ]),

    html.Details([
        html.Summary("How much radiation is considered dangerous?"),
        html.P("Acute exposure above 1,000 mSv (1 Sv) can cause radiation sickness, while prolonged exposure "
               "above 100 mSv may increase cancer risk. However, small doses from medical imaging or flights "
               "are generally not dangerous.")
    ]),

    html.Details([
        html.Summary("Does flying frequently increase radiation exposure?"),
        html.P("Yes, but the exposure is minimal. A round-trip flight from NYC to LA results in about 0.08 mSv of exposure, "
               "which is much lower than an annual background dose (3 mSv).")
    ]),

    html.Details([
        html.Summary("Is radiation from medical imaging safe?"),
        html.P("Medical imaging, such as X-rays and CT scans, involves low radiation doses that are carefully controlled. "
               "The benefits usually outweigh the risks when performed by medical professionals.")
    ]),

    html.Details([
        html.Summary("What is the difference between ionizing and non-ionizing radiation?"),
        html.P("Ionizing radiation (e.g., X-rays, gamma rays) can remove electrons from atoms, potentially causing damage to cells. "
               "Non-ionizing radiation (e.g., radio waves, microwaves) does not have enough energy to ionize atoms and is generally safer.")
    ]),

    html.Details([
        html.Summary("What is radiation hormesis?"),
        html.P("Radiation hormesis is the hypothesis that low levels of radiation exposure may have beneficial effects, "
               "such as stimulating cellular repair mechanisms. This idea is debated and not widely accepted in radiation safety.")
    ]),

    html.Details([
        html.Summary("Where can I find reliable information on radiation?"),
        html.P("Reliable sources include the Health Physics Society, International Commission on Radiological Protection (ICRP), "
               "National Council on Radiation Protection and Measurements (NCRP), and BEIR VII reports.")
    ]),

    html.Details([
        html.Summary("Does radiation exposure always cause cancer?"),
        html.P("Not necessarily. While high doses of radiation can increase cancer risk, small doses from background radiation, "
               "medical imaging, or air travel are unlikely to cause harm.")
    ]),
]),

    # References Section
    html.Div(id='references', children=[
        html.H3("References"),
        html.Ul([
            html.Li("BEIR VII Report (Biological Effects of Ionizing Radiation)."),
            html.Li("National Council on Radiation Protection and Measurements (NCRP) Publications."),
            html.Li("International Commission on Radiological Protection (ICRP) Reports."),
            html.Li("Health Physics Society Fact Sheets."),
        ]),
    ]),

    # Conclusion Section
    html.Div(id='conclusion', children=[
        html.H3("Conclusion"),
        html.P("This interactive app highlights the complexity of understanding radiation exposure and risk. "
               "By comparing different models and exploring common sources of radiation, users can make informed "
               "decisions and better understand radiation safety."),
    ]),
])

# Callback for radiation dose calculator
@app.callback(
    dash.Output("total-dose-output", "children"),
    [dash.Input("flight-slider", "value"), dash.Input("xray-slider", "value")]
)
def update_dose(flights, xrays):
    total_dose = (flights * 0.04) + (xrays * 0.1)
    return f"Your estimated annual radiation dose from selected activities: {total_dose:.2f} mSv"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)




