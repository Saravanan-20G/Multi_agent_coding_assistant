from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ✅ FIXED: Proper directory creation
def write_file(project_name, file_name, content):
    file_path = os.path.join(project_name, file_name)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Created: {file_path}")


def coder_agent(plan: dict, architecture: dict):
    project_name = plan["project_name"].lower().replace(" ", "_")
    files = architecture["files"]

    for file in files:
        print(f"⚡ Generating {file}...")

        prompt = f"""
You are a senior AI/ML Engineer.

Generate content for the given file.

RULES:

IF input_spec.format == "pdf":
- Use PyPDFLoader(file_path)
- Build RAG pipeline
- Include retriever

IF input_spec.format == "csv":
- Use pandas.read_csv()
- Perform EDA, preprocessing, training

IF input_spec.format == "image":
- Use OpenCV / PIL

ALWAYS:
- Start from input handling
- Then follow pipeline stages

Project Input:
{plan.get("input_spec")}

Project pipeline:
{plan.get("pipeline")}

File:
{file}

Return ONLY content. No markdown.
"""

        response = llm.invoke(prompt).content
        cleaned = response.replace("```", "").strip()

        write_file(project_name, file, cleaned)

    return f"🎉 Project '{project_name}' created successfully!"


