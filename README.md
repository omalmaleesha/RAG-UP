# 🚀 RAG-UP: Transforming a Traditional RAG Chatbot into an Agentic AI System with LangGraph

**From Traditional RAG → Agentic RAG**

RAG-UP is an evolution of my original [HelpDesk RAG Chatbot](https://github.com/omalmaleesha/HelpDesk-RAG-Chatbot), redesigned from a traditional Retrieval-Augmented Generation (RAG) pipeline into an **agentic AI system** powered by LangGraph.
The original project followed a relatively straightforward RAG workflow:

```
User Question → Retrieval → Context → LLM → Answer
```

RAG-UP introduces an intelligent orchestration layer that allows the system to decide:

- When to retrieve information
- When to use tools
- When existing information is sufficient
- When to reuse cached answers
- When an answer should be evaluated before being stored for future use

---

## 🎯 Goal and Problem

My original HelpDesk RAG Chatbot used a traditional RAG pipeline where most questions followed the same **retrieve → send to LLM → generate** flow.

While it worked, I realized the system was too dependent on the LLM and could perform unnecessary retrievals and LLM calls, increasing latency, token usage, and cost.
Instead of leaving the project as it was, I challenged my own implementation and rebuilt it as **RAG-UP**, an agentic RAG system using LangGraph.

The goal is simple:

> **Don't use AI for everything. Use AI where it adds value, and use good software engineering everywhere else.**

I continuously improve my own projects by identifying bottlenecks, learning new technologies, measuring performance, and redesigning systems to deliver a faster, smarter, and more efficient experience for the end user.

---

## 🛠️ Why These Technologies?

### 🧠 LangChain & LangGraph

- LangChain provides the building blocks for RAG, prompts, retrievers, and LLM integration.
- LangGraph allows me to move beyond a fixed RAG pipeline and build a **stateful, decision-driven agent workflow**.
- Makes it easier to separate responsibilities into independent nodes such as planning, retrieval, generation, reflection, and caching.
- The modular architecture makes the system easier to debug, extend, and optimize.

### ⚡ FastAPI

- Lightweight and high-performance Python framework for exposing the AI agent as REST APIs.
- Provides a clean separation between the AI backend and frontend.
- Built-in request validation and automatic API documentation make development and testing easier.
- Easy to extend when adding authentication, streaming responses, or additional AI tools.

### 🚀 Groq

- Chosen primarily for **very fast LLM inference**, which is important for an interactive AI application.
- Provides access to capable open models with a developer-friendly API.
- The availability of free/low-cost usage during development made it practical for experimentation and continuous optimization.
- Fast inference helps reduce the perceived response time for end users.

---

## 🎯 Overall Technology Strategy

I chose these technologies based on the requirements of the system rather than simply following trends:

**LangGraph for orchestration → FastAPI for backend APIs → Groq for fast LLM inference**

### Architecture Diagram

![RAG-UP Architecture Diagram](https://drive.google.com/file/d/1ygrwyNLfEe8DEXNxah683_hUkgDuhNTH/view?usp=sharing)

---

## 🚀 Run the Project

Using [`uv`](https://github.com/astral-sh/uv) for fast and reproducible Python dependency management:

```bash
uv sync
uv run main.py
```

Once the server starts, open:

- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

FastAPI provides interactive Swagger documentation, so you can test the endpoints directly from your browser without needing additional tools.

---

## License
This project is open source. Feel free to explore, learn from, and build upon it.
