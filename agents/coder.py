import os
from langchain_groq import ChatGroq


def write_file(project_name, file_name, content):
    file_path = os.path.join(project_name, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created: {file_path}")


def coder_agent(plan: dict, architecture: dict, api_key: str):
    project_name = plan["project_name"].lower().replace(" ", "_")
    files = architecture["files"]

    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    for file in files:
        prompt = f"""
        You are a professional software developer.


        Generate complete code for the file: {file}


        Project details:
        {plan}


        Rules:
        - Return ONLY code
        - No explanations
        - No markdown (no ```)


        """
        response = llm.invoke(prompt).content
        cleaned = response.replace("```", "").strip()
        write_file(project_name, file, cleaned)

    return f"Project '{project_name}' created successfully!"
