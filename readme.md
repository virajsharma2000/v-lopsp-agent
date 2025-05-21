# 🤖 LOPSP - LLM-Orchestrated Prompt Scheduling Protocol

This project is a prototype for a new paradigm: **LLMs that control the scheduling of their next invocation** — not humans or static schedules.

Instead of polling or cron jobs, we use a pattern where:

> 🧠 The **LLM response itself determines when and under what condition it should be prompted next.**

---

## 💡 What is LOPSP?

**LOPSP** stands for **LLM-Orchestrated Prompt Scheduling Protocol**.  
It’s a protocol where the **LLM decides when to prompt again** and optionally sets a **condition** (e.g., a file appearing, time delay, or a signal) that, when met, triggers the next prompt.

This enables **autonomous agents** with long-running goals — **LLMs in control of their execution timeline**.

---

## 🔧 Components

### 1. `lops_scheduler.py` — Joke Agent (Fun Demo)

This agent:
- Tells a joke
- Asks the LLM when it should ask again
- Waits for:
  - A number of seconds suggested by the LLM
  - Or a file (`tell_joke.txt`) to appear
- Loops with a new joke

### 2. `poem_scheduler.py` — Poem Agent (Creative Scheduler)

This agent:
- Asks the LLM to write a poem on a random topic
- Also asks **when the next poem should be written**
- Stores the poem with timestamps
- Runs perpetually, controlled by the LLM

---

## 📦 Requirements

- Python 3.8+
- [Ollama](https://ollama.com) with a local LLM running (like `llama3` or `mistral`)
  ```bash
  ollama run llama3
