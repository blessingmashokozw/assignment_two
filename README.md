# DevOps AI Troubleshooting Crew

This project demonstrates how to use [CrewAI](https://github.com/joaomdmoura/crewai) with multiple agents to troubleshoot **CI/CD pipeline failures** and **Kubernetes pod issues**.  
The crew consists of four specialized agents:
- **Planner** – creates a step-by-step troubleshooting plan
- **Inspector** – inspects logs or pod status and classifies failure reasons
- **Self-Reflector** – validates and critiques the reasoning
- **Advisor** – provides actionable fixes

---

## 🚀 Features
- Dynamic task creation for CI/CD and Kubernetes troubleshooting
- Multi-agent workflow with dependencies (`Planner → Inspector → Reflector → Advisor`)
- Supports multiple LLM providers (OpenAI, Anthropic, Google, Ollama/local models)

---

## 📦 Requirements
- Python 3.12+
- Virtual environment (`venv`)
- CrewAI with provider extras (e.g., Anthropic)

##  API Keys
You must set your API key as an environment variable before running:

## Anthropic (Claude)
bash
export ANTHROPIC_API_KEY="your_anthropic_api_key"
OpenAI (GPT models)
bash
export OPENAI_API_KEY="your_openai_api_key"

## Usage
Activate your virtual environment:

bash
source venv/bin/activate

## Run the script:
bash
python agent.py
