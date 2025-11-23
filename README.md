
# TherapyX-Next-Gen-AI-Mental-Health-Assistant (Demo)

**TherapyX** is an AI-driven mental-health companion designed to demonstrate how to build a **tool-using LLM agent** capable of therapeutic-style conversation, safety intervention, and real-world integrations.
It includes:

* 🌱 **Empathetic, therapy-style conversation** powered by a MedGemma-based LLM via Groq
* 🚨 **Crisis detection & emergency call tool** (Twilio Voice)
* 📍 **Location-aware therapist finder** using Google Maps
* 💬 **Two chat interfaces:** Streamlit web client + Twilio WhatsApp chatbot
* 🧩 A LangGraph REAct-style AI agent with structured tool-use

> **⚠️ Important:** SafeSpace is strictly a **technical demonstration** and **not a clinical tool**.
> It is *not* a substitute for professional mental healthcare or emergency services.

---

# 📁 Project Structure

```
safespace-ai-therapist/
├── backend/
│   ├── ai_agent.py              # LangGraph-based AI agent + tools
│   ├── config.py                # API key container (created by user)
│   ├── main.py                  # FastAPI backend + Twilio webhook
│   ├── tools.py                 # LLM, Google Maps, Twilio integrations
│   └── test_location_tool.py    # Example/test for location tool
├── frontend.py                  # Streamlit chat UI
├── pyproject.toml               # Dependencies (managed by uv)
└── README.md
```

---

# 🔧 Key Components

### **1. `frontend.py` – Streamlit UI**

* Simple chat interface using `st.chat_input` and `st.chat_message`
* Sends user messages to `POST /ask` on the backend
* Displays AI response + tool used

### **2. `backend/main.py` – FastAPI Server**

* `POST /ask` — JSON endpoint for web chat
* `POST /whatsapp_ask` — Twilio WhatsApp webhook (form-encoded)
* Returns TwiML responses for WhatsApp users

### **3. `backend/ai_agent.py` – LangGraph REAct Agent**

Tools available to the agent:

| Tool                                           | Description                            |
| ---------------------------------------------- | -------------------------------------- |
| `ask_mental_health_specialist(query)`          | Therapeutic response using MedGemma    |
| `emergency_call_tool()`                        | Triggers a Twilio emergency voice call |
| `find_nearby_therapists_by_location(location)` | Google Maps geocoding + Places API     |

* Uses Groq LLM (`openai/gpt-oss-120b`)
* Custom system prompt for safety + tool selection
* `parse_response()` extracts the final message and any tool invocation from streaming output

### **4. `backend/tools.py`**

Implements:

* MedGemma query wrapper
* Twilio voice call starter
* Google Maps therapist search

---

# 🧰 Tech Stack

**Language:** Python 3.11+
**Dependency Manager:** `uv`
**Backend:** FastAPI + Uvicorn
**Frontend:** Streamlit
**LLM/Agent:** LangChain, LangGraph, Groq’s ChatGroq
**Integrations:**

* Twilio (WhatsApp + Voice)
* Google Maps (Places & Geocoding)
* Geopy, Requests

Dependencies include:
`fastapi`, `googlemaps`, `langchain`, `langgraph`, `langchain-groq`,
`python-multipart`, `twilio`, `streamlit`, `uvicorn`, etc.

---

# 🚀 Getting Started

## 1. Install & Create Environment

```bash
git clone https://github.com/AIwithhassan/safespace-ai-therapist.git
cd safespace-ai-therapist
uv sync
source .venv/bin/activate   # macOS/Linux
```

---

## 2. Configure API Keys (`backend/config.py`)

```python
GROQ_API_KEY = "your_groq_key"
GOOGLE_MAPS_API_KEY = "your_google_key"

TWILIO_ACCOUNT_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_FROM_NUMBER = "+1234567890"
TWILIO_EMERGENCY_TO_NUMBER = "+1987654321"
```

> Do **NOT** commit real keys. Use `.env` or environment variables in production.

---

# 🖥️ Running the Backend (FastAPI)

From project root:

```bash
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Endpoints

| Endpoint             | Purpose                       |
| -------------------- | ----------------------------- |
| `POST /ask`          | JSON API for web client       |
| `POST /whatsapp_ask` | Twilio webhook (form-encoded) |

Example:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"message":"I feel overwhelmed"}'
```

---

# 💬 Running the Streamlit Frontend

```bash
uv run streamlit run frontend.py
```

Opens at: **[http://localhost:8501](http://localhost:8501)**

---

# 📲 WhatsApp Integration (Twilio)

### 1. Create a public URL

```bash
ngrok http 8000
```

### 2. Configure Twilio WhatsApp Sandbox

Set the incoming message webhook to:

```
https://your-ngrok-url/whatsapp_ask
```

### 3. Test locally

```bash
curl -X POST http://localhost:8000/whatsapp_ask \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=Hello"
```

Common Issues:

* **422 error** → missing `Body` field or wrong content type
* Twilio can't reach local server → ngrok not running

---

# 📍 Therapist Finder (Google Maps)

`find_nearby_therapists_by_location(location)`:

1. Geocodes user location → lat/lng
2. Searches for *psychotherapists* within 5 km
3. Retrieves name, address, phone
4. Returns a formatted list

Used when user asks for help near a city/place.

---

# 🚨 Emergency Call Tool

`emergency_call_tool()` triggers `call_emergency()`, which:

* Initiates a voice call via Twilio
* Intended only for demo purposes
* Must follow legal and ethical guidelines if adapted for real use

---

# 🧪 Testing

Run tests:

```bash
uv run pytest
```

The sample test file covers therapist finder logic.

---

# 🛠️ Future Enhancements

* Add Twilio signature validation
* More robust error handling
* Session and rate-limit mechanisms
* Expanded automated tests
* UI section for safety limitations

---

# ⚠️ Disclaimer

SafeSpace is a **technical demo**, not a clinical tool.
It **cannot** diagnose, treat, or replace mental health professionals.
If someone is in immediate danger, always contact local emergency services.

---
