# AI-Assisted GTN Forecasting MVP

Enterprise-style Gross-to-Net forecasting MVP for Pharma Finance teams.

## Workflow

Login → Workspace → Data Intake → Forecast Engine → Outputs → Scenario Simulator → AI Copilot → Model Zoo

## Capabilities

- 48-month synthetic GTN demo dataset
- CSV templates and upload validation
- Multi-model forecasting framework
- Champion model selection by WMAPE
- GTN, Net Sales, and GTN % forecast outputs
- Scenario simulator
- AI commentary via Groq, with fallback commentary if no key is provided
- Render deployment ready

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Render settings

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Optional environment variable:

```text
GROQ_API_KEY=your_key_here
```

## Demo credentials

```text
admin@gtnforecast.com
password123
```
