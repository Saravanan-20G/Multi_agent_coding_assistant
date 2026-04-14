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


    Return ONLY valid JSON.
    Do NOT include markdown (no ```).


    JSON format:
    {{
        "project_name": "string",
        "features": ["feature1", "feature2"],
        "tech_stack": ["tech1", "tech2"]
    }}


    Request:
    {task}
    """
    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    response = llm.invoke(prompt)
    return extract_json(response.content)



