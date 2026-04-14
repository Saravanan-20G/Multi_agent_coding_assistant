def normalize_name(name):
    return name.lower().replace(" ", "_")


def architect_agent(plan: dict):
    files = []
    pipeline = plan.get("pipeline", [])

    for stage in pipeline:
        name = normalize_name(stage["stage"])
        files.append(f"src/stages/{name}.py")

    files += [
        "src/pipeline/main_pipeline.py",
        "config/config.yaml",
        "requirements.txt",
        "README.md"
    ]

    return {"files": files}


# def architect_agent(plan: dict):
#     files = []
#     pipeline = plan.get("pipeline", [])

#     for stage in pipeline:
#         name = normalize_name(stage["stage"])
#         files.append(f"src/stages/{name}.py")

#     files += [
#         "src/pipeline/main_pipeline.py",
#         "config/config.yaml",
#         "requirements.txt",
#         "README.md"
#     ]

#     return {"files": files}

# def normalize_name(name):
#     return name.lower().replace(" ", "_")

