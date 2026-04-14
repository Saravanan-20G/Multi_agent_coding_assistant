import re
import json
from langchain_groq import ChatGroq


def extract_json(text: str):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"error": "No JSON found"}
    except Exception as e:
        return {"error": f"Parsing failed: {str(e)}"}


def planner_agent(task: str, api_key: str):
    prompt = f"""
You are a software planning assistant.

Design a REAL system.

STEP 1: Identify project type:
- rag_pipeline → requires PDF input
- ml_pipeline → requires CSV dataset
- nlp_pipeline → text input
- cv_pipeline → image input

STEP 2: Define INPUT SPEC clearly
STEP 3: Build MULTI-STAGE pipeline

IMPORTANT RULES:

IF rag_pipeline:
- input must be PDF
- use PyPDFLoader, TextSplitter, Embeddings, FAISS

IF ml_pipeline:
- input must be CSV
- include preprocessing, EDA, feature engineering, train/test split, model training, evaluation

RETURN ONLY JSON:

{{
  "project_name": "string",
  "project_type": "...",
  "input_spec": {{
    "type": "file",
    "format": "pdf | csv | image | text",
    "description": "what user must provide"
  }},
  "pipeline": [
    {{
      "stage": "name",
      "purpose": "what it does",
      "tools": ["library"]
    }}
  ]
}}

Task:
{task}
"""

    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    response = llm.invoke(prompt)
    return extract_json(response.content)



