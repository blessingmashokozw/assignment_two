import os
import google.generativeai as genai
from crewai import Agent, Task, Crew, LLM

# --- Configure Gemini SDK ---
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# --- Dynamically pick a Gemini model ---
def get_default_gemini_model():
    # List all models
    models = list(genai.list_models())
    # Filter only those that support generateContent
    content_models = [m for m in models if "generateContent" in m.supported_generation_methods]
    # Prefer pro, fallback to flash
    for m in content_models:
        if "gemini-1.5-pro" in m.name:
            return m.name
    for m in content_models:
        if "gemini-1.5-flash" in m.name:
            return m.name
    # Fallback: just return the first available
    return content_models[0].name if content_models else None

model_name = get_default_gemini_model()
print(f"Using Gemini model: {model_name}")

# --- Define the LLM using CrewAI's wrapper ---
llm = LLM(provider="google", model=model_name, temperature=0)

# --- Shared Agents ---
planning_agent = Agent(
    role="Planner",
    goal="Create a step-by-step plan for DevOps troubleshooting.",
    backstory="Expert in CI/CD and Kubernetes planning.",
    llm=llm
)

tool_agent = Agent(
    role="Inspector",
    goal="Inspect logs or pod status and classify failure reasons.",
    backstory="Knows how to detect CI/CD errors and Kubernetes pod issues.",
    llm=llm
)

reflection_agent = Agent(
    role="Self-Reflector",
    goal="Evaluate reasoning and ensure correctness.",
    backstory="Critical thinker that validates DevOps troubleshooting steps.",
    llm=llm
)

final_agent = Agent(
    role="Advisor",
    goal="Provide actionable fixes for DevOps issues.",
    backstory="DevOps expert who gives practical CI/CD and Kubernetes solutions.",
    llm=llm
)

# --- Define Tasks Dynamically ---
def build_tasks(task_type: str, input_data: str):
    if task_type == "cicd":
        planning_task = Task(
            description="Plan how to troubleshoot CI/CD pipeline failures.",
            agent=planning_agent,
            expected_output="A clear troubleshooting plan with ordered steps."
        )
        tool_task = Task(
            description=f"Inspect CI/CD logs: {input_data}",
            agent=tool_agent,
            expected_output="Classification of failure reasons from the logs.",
            depends_on=[planning_task]
        )
        reflection_task = Task(
            description="Reflect on the CI/CD log analysis.",
            agent=reflection_agent,
            expected_output="Validation and critique of the inspection reasoning.",
            depends_on=[tool_task]
        )
        final_task = Task(
            description="Provide final actionable fixes for the CI/CD failure.",
            agent=final_agent,
            expected_output="Concrete fixes and commands to resolve the CI/CD issue.",
            depends_on=[reflection_task]
        )
    elif task_type == "k8s":
        planning_task = Task(
            description="Plan how to troubleshoot Kubernetes CrashLoopBackOff.",
            agent=planning_agent,
            expected_output="A clear troubleshooting plan with ordered steps."
        )
        tool_task = Task(
            description=f"Inspect Kubernetes pod status: {input_data}",
            agent=tool_agent,
            expected_output="Classification of failure reasons from pod status.",
            depends_on=[planning_task]
        )
        reflection_task = Task(
            description="Reflect on the Kubernetes pod analysis.",
            agent=reflection_agent,
            expected_output="Validation and critique of the inspection reasoning.",
            depends_on=[tool_task]
        )
        final_task = Task(
            description="Provide final actionable fixes for the pod issue.",
            agent=final_agent,
            expected_output="Concrete fixes and commands to resolve the Kubernetes issue.",
            depends_on=[reflection_task]
        )
    else:
        raise ValueError("Unsupported task type. Use 'cicd' or 'k8s'.")

    return [planning_task, tool_task, reflection_task, final_task]

# --- Run Crew ---
def run_devops_agent(task_type: str, input_data: str):
    tasks = build_tasks(task_type, input_data)
    crew = Crew(
        agents=[planning_agent, tool_agent, reflection_agent, final_agent],
        tasks=tasks,
        verbose=True
    )
    results = crew.kickoff()
    print("=== DevOps AI Agent Output ===")
    print(results)

# --- Example Runs ---
if __name__ == "__main__":
    run_devops_agent("cicd", "ERROR: ModuleNotFoundError: No module named 'requests'")
    run_devops_agent("k8s", "status=CrashLoopBackOff, reason=OOMKilled")
