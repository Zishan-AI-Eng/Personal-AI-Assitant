# 🤖 AI Portfolio Assistant (Multi-Agent Architecture)

An enterprise-grade, autonomous AI assistant designed to handle professional portfolio inquiries. Built with a multi-agent semantic routing architecture to ensure zero hallucinations, sub-second latency, and highly accurate responses based strictly on provided context.

## 🌟 Key Features
* **Multi-Agent Semantic Routing:** Utilizes a supervisor agent (Router) to classify user intent and route queries to specialized worker agents.
* **Zero-Hallucination Guardrails:** A dedicated `Reject Agent` blocks prompt injections, code requests, and out-of-scope queries with zero LLM inference cost.
* **Stateful Conversation Memory:** Seamlessly manages chat history using a managed cloud PostgreSQL database (Supabase), keeping context intact across sessions.
* **Ultra-Fast Inference:** Powered by Meta's `Llama-3.3-70B-Versatile` via the Groq API for rapid, intelligent query resolution.

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **LLM Orchestration:** LangChain Core & Community
* **Models:** Groq (`llama-3.3-70b-versatile`)
* **Database / Memory:** Supabase (PostgreSQL) & `psycopg2`
* **Data Validation:** Pydantic

## 📂 Project Architecture
```text
.
├── agents/
│   ├── router_agent.py      # Semantic intent classifier (Supervisor)
│   ├── portfolio_agent.py   # RAG/Context-driven response worker
│   └── reject_agent.py      # Zero-latency security guardrail
├── core/
│   ├── config.py            # Centralized environment & LLM configuration
│   └── state.py             # PostgreSQL session history manager
├── data/
│   └── profile_data.json    # Knowledge base containing skills, experience, and projects
├── main.py                  # FastAPI entry point & API routes
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables (Ignored in Git)





🚀 Setup & Installation
1. Clone the repository

Bash
git clone [https://github.com/Zishan-AI-Eng/Personal-AI-Assitant.git](https://github.com/Zishan-AI-Eng/Personal-AI-Assitant.git)
cd portfolio-ai-assistant
2. Install dependencies

Bash
pip install -r requirements.txt
3. Set up environment variables
Create a .env file in the root directory and add your credentials:

Code snippet
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://postgres:[PASSWORD]@[YOUR-SUPABASE-URL]:5432/postgres
4. Run the API Server

Bash
uvicorn main:app --reload
📡 API Usage
Endpoint: POST /chat

Request Body:

JSON
{
  "session_id": "user-unique-id-123",
  "message": "Tell me about Zeeshan's experience with Agentic AI."
}

👨‍💻 Author
Zeeshan Khan
AI Engineer & Solution Architect
Specializing in Agentic AI, Autonomous Workflows, and Applied Deep Learning.