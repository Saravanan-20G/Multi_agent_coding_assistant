from agents.planner import planner_agent
from agents.architect import architect_agent
from agents.coder import coder_agent
import json
import os

def run_multi_agent_system(user_input):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment")

    print("\nStep 1: Planning...")
    plan = planner_agent(user_input, api_key)
    print(json.dumps(plan, indent=4))

    print("\nStep 2: Designing Architecture...")
    architecture = architect_agent(plan)
    print(json.dumps(architecture, indent=4))

    print("\nStep 3: Generating Code...")
    result = coder_agent(plan, architecture, api_key)

    print("\nFINAL RESULT:")
    print(result)

if __name__ == "__main__":
    user_input = input("Enter your project idea: ")
    run_multi_agent_system(user_input)



# from agents.planner import planner_agent
# from agents.architect import architect_agent
# from agents.coder import coder_agent
# import json

# def run_multi_agent_system(user_input):
#     print("\n Step 1: Planning...")
#     plan = planner_agent(user_input)
#     print(json.dumps(plan, indent=4))


#     print("\n Step 2: Designing Architecture...")
#     architecture = architect_agent(plan)
#     print(json.dumps(architecture, indent=4))

#     print("\n Step 3: Generating Code...")
#     result = coder_agent(plan, architecture)

#     print("\n FINAL RESULT:")
#     print(result)

# #  Run System
# if __name__ == "__main__":
#     user_input = input(" Enter your project idea: ")

#     run_multi_agent_system(user_input)
