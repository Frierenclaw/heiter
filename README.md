# 🦋 Heiter (The Inference Server)

> *"The wise memory keeper. A repository of knowledge and character."*

**Heiter** is the intelligence layer and the "brain" of the Frieren AI Ecosystem. It acts as a high-throughput, asynchronous inference server that provides OpenAI-compatible streaming endpoints for the pipeline.

## 🔮 Responsibilities

* **The Grimoire (LLM Layer):** Exposes a fully OpenAI-compatible API (`/v1/chat/completions`) to serve the underlying language model text generation seamlessly.
* **The Voice (Edge TTS):** Provides lightweight, natural, and low-latency Text-to-Speech generation powered by Edge TTS, keeping the server independent from heavy paid API dependencies.
* **The Overseer (Async & Workers):** Built on native `asyncio` and optimized with background workers to handle multiple concurrent sessions without blocking text/audio generation.

## 📐 Architecture Integration

## 🔮 Core Specifications

| Component / Layer | Magic Spell (Tech Stack) | Responsibility & Integration |
| :--- | :--- | :--- |
| **The Grimoire (LLM Layer)** | FastAPI + OpenAI API | Exposes a fully OpenAI-compatible API (/v1/chat/completions) to serve the underlying language model text generation seamlessly. |
| **The Voice (TTS)** | edge-tts | Provides lightweight, natural, and low-latency Text-to-Speech generation, keeping the server independent from heavy paid cloud APIs. |
| **The Overseer (Async Core)** | Python 3.14 + asyncio | Powered by native asyncio and optimized background workers to handle multiple concurrent sessions without blocking text/audio generation. |

## 🛠 Tech Stack & Spells

* **Core Server:** Python 3.14 (Driven by `asyncio` & `Uvicorn`)
* **API Framework:** `FastAPI`
* **Speech Synthesis:** `edge-tts`
* **HTTP Client:** `httpx`

## 🚀 Quick Start

1. **Clone the grimoire:**
```
   git clone https://github.com/Frierenclaw/heiter.git
   cd heiter
```

2. **Prepare the ingredients:**
    Install docker

3. **Configure your secrets:**
   Create a `.env` 

4. **Cast the spell:**
```
   docker compose up --build
```

---
*Part of the [Frieren AI Ecosystem](https://github.com/Frierenclaw).*
