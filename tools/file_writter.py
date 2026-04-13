import os

def write_file(project_name, file_name, content):
    # Full path
    file_path = os.path.join(project_name, file_name)

    # ✅ Create ALL required directories
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # ✅ Write file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Created: {file_path}")



