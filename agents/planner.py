
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os, json

# load_dotenv()


def get_llm():
    import os
    import streamlit as st
    from langchain_openai import ChatOpenAI

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            raise ValueError("GROQ_API_KEY not found in environment or Streamlit secrets")

    return ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
        model="llama3-70b-8192",
        temperature=0
    )

def planner_agent(task: str):
        prompt = f"""
    You are a senior AI/ML Architect.

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
        llm = get_llm()
        try:
            response = llm.invoke(prompt)
            print("FULL RESPONSE:", response)
            res = response.content
        except Exception as e:
            import traceback
            print("ERROR:", str(e))
            print(traceback.format_exc())
            raise

        data = extract_json(res)

        return data

import re
import json

def extract_json(text: str):
    try:
        # Extract first JSON object
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group()
            return json.loads(json_str)
        else:
            return {"error": "No JSON found"}
    except Exception as e:
        return {"error": f"Parsing failed: {str(e)}"}




