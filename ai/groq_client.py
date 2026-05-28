import os

def fallback_summary(context):
    return (
        "Forecast commentary: GTN movement appears primarily influenced by rebate behavior, payer mix exposure, "
        "and channel dynamics. Review high-WMAPE components and scenario sensitivity to identify areas requiring Finance review."
    )

def generate_ai_summary(context):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return fallback_summary(context)
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        prompt = f"""
You are a pharma Finance GTN forecasting assistant.
Summarize the forecast in concise, executive-friendly language.
Use only the context provided.

Context:
{context}
"""
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You explain pharma GTN forecasts clearly and concisely."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=350,
        )
        return response.choices[0].message.content
    except Exception:
        return fallback_summary(context)
