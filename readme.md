# 🧑‍⚕️ Medical Symptom Assistant (AI + RAG + Triage)

A medical information assistant that helps users describe symptoms, answers clarification questions, performs risk triage, retrieves medical context using RAG, and generates structured clinical-style output using Google Gemini models.

> ⚠️ Not a diagnostic tool. Educational purposes only.

---

## 🚀 Features

### **Symptom Handling**
✓ Multi-turn conversation  
✓ Extracts symptoms, duration, severity  
✓ Hinglish friendly (“3 din”, “kal se”, etc.)  

### **Medical Triage**
✓ Classifies as **LOW / MODERATE / HIGH** risk  
✓ Uses red-flag symptom logic  
✓ Shows severity + duration summary  
✓ Color-coded triage badges  

### **RAG (Retrieval Augmented Generation)**
✓ Retrieves possible causes from disease dataset  
✓ Embeddings generated locally  
✓ Supports future medical dataset expansion  

### **LLM Integration**
✓ Uses Gemini 2.x (Flash / Pro)  
✓ Structured medical sections:
- Clinical Summary
- Possible Causes
- Watch For (Red Flags)
- When to Get Checked
- Helpful at Home
- Sources
- Medical Disclaimer

### **UI (Premium Chat)**
✓ Streamlit chat interface  
✓ Avatars (user + clinician style)  
✓ Chips for symptoms  
✓ Card layout for clinical output  
✓ Safe consumer-oriented design  
✓ Dark theme optimized  

---

## 🧠 Architecture Overview

```
User → NLP Extraction → Clarification → Triage → RAG Context → Prompt → Gemini → Safety → UI
```

### Components:
- `helpers.py` → NLP extraction
- `triage.py` → red-flag risk scoring
- `retriever.py` → embeddings + DB lookup
- `prompts.py` → clinical structured prompt
- `gemini_client.py` → LLM API client
- `safety.py` → disclaimers + safety guardrail
- `app.py` → Streamlit frontend

---

## 📦 Folder Structure

```
medical_chatbot/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── rag/
│   ├── dataset/
│   │   └── diseases.json
│   ├── embeddings/
│   └── build_embeddings.py
│
├── utils/
│   ├── helpers.py
│   ├── safety.py
│   ├── triage.py
│   ├── retriever.py
│   ├── prompts.py
│   └── nlp/
│
├── models/
│   └── gemini_client.py
│
├── docs/
│   ├── architecture.md
│   ├── dataset_sources.md
│   └── future_work.md
│
└── tests/
    └── test_cases.md
```

---

## 🔧 Installation

```bash
git clone <your-repo-url>
cd medical_chatbot
python -m venv venv
source venv/bin/activate       # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create `.env`:

```
GEMINI_API_KEY=your_key
```

---

## 📍 Running Embeddings

```bash
python rag/build_embeddings.py
```

---

## ▶️ Run App

```bash
streamlit run app.py
```

---

## 📚 Dataset Source (RAG)

Current dataset (example):

- WHO
- CDC
- Mayo Clinic
- NHS
- Buoy Health & Ada style structures

Easily extendable.

---

## ❗ Medical Disclaimer

This project is **not a diagnostic medical device** and is intended only for educational purposes. Always consult a qualified healthcare provider for medical advice.

---

## 🧩 Future Work (Planned)

- Symptom → differential mapping
- Telemedicine handoff
- Voice input + TTS
- Hindi/Hinglish expansion
- ICD-10 / SNOMED mapping
- Deployment (Cloud/Edge)
- Benchmarking dataset

---

## ⭐ Tech Used

- Python 3.10+
- Streamlit 1.53+
- Gemini 2.x API
- LangChain (RAG + embeddings)
- ChromaDB
- Custom NLP heuristics

---

## 👨‍💼 Ideal Use Cases

- AI Health Assistants
- Prototype symptom checker
- RAG-based chatbots
- Clinical UX demos
- Portfolio & interview projects

---

# License
MIT
