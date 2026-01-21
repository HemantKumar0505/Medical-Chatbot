import streamlit as st
import time

from utils.helpers import build_structured, needs_clarification, get_next_question
from utils.retriever import retrieve_conditions
from utils.triage import triage
from utils.prompts import build_medical_prompt
from utils.safety import add_medical_safety
from models.gemini_client import generate_medical_response


# ---------------- CSS ----------------

CUSTOM_CSS = """
<style>
body { background-color: #0e1117 !important; }

.card {
    background: #1c1f26;
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 10px;
    border: 1px solid #2c303a;
}

.section-title {
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 6px;
}

.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    color: white;
    margin-bottom: 6px;
}

.badge-low { background: #3a8458; }
.badge-moderate { background: #d4a017; }
.badge-high { background: #b73939; }

.symptom-chip {
    display: inline-block;
    background: #232832;
    padding: 4px 10px;
    border-radius: 12px;
    margin-right: 6px;
    margin-bottom: 4px;
    font-size: 12px;
    border: 1px solid #3b4252;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="Medical Symptom Assistant",
    page_icon="🧑‍⚕️",
    layout="wide"
)


# ---------------- SESSION STATE ----------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_struct" not in st.session_state:
    st.session_state.pending_struct = None

if "thinking" not in st.session_state:
    st.session_state.thinking = False


# ---------------- RENDER HELPERS ----------------

def add_message(role, content, meta=None):
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "meta": meta or {}
    })


def render_message(role, content, meta=None):
    avatar = "🙂" if role == "user" else "🧑‍⚕️"

    with st.chat_message(role, avatar=avatar):
        if role == "assistant" and meta and meta.get("structured"):
            render_structured(content, meta)
        else:
            st.markdown(content)


def render_structured(content, meta):
    struct = meta["struct"]
    risk = meta["risk"]

    # risk badge
    risk_class = "badge-low" if risk == "LOW RISK" else "badge-moderate" if risk == "MODERATE RISK" else "badge-high"
    st.markdown(f"<span class='badge {risk_class}'>{risk}</span>", unsafe_allow_html=True)

    # symptom chips
    if struct.get("symptoms"):
        chips = " ".join([f"<span class='symptom-chip'>{s}</span>" for s in struct["symptoms"]])
        st.markdown(chips, unsafe_allow_html=True)

    # clinical card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🧾 Clinical Summary")

    st.write(f"• Duration: **{struct.get('duration')} days**" if struct.get("duration") else "")
    st.write(f"• Severity: **{struct.get('severity')}**" if struct.get("severity") else "")

    st.markdown("### 🧠 Possible Causes\n" + content.get("causes", ""))

    st.markdown("### 🚨 Watch For\n" + content.get("red_flags", ""))

    st.markdown("### 👨‍⚕️ When to Get Checked\n" + content.get("doctor", ""))

    st.markdown("### 🏠 Helpful at Home\n" + content.get("self_care", ""))

    st.markdown("### ⚠️ Disclaimer\n" + content.get("disclaimer", "Not medical advice. For informational purposes only."))

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
# 🧑‍⚕️ Medical Symptom Assistant  
Professional, structured, and safety-aware symptom guide  
""")


# ---------------- CHAT DISPLAY ----------------

for msg in st.session_state.chat_history:
    render_message(msg["role"], msg["content"], msg["meta"])


# ---------------- USER INPUT ----------------

disabled = st.session_state.thinking
user_query = st.chat_input("Describe your symptoms...", disabled=disabled)


# ---------------- MAIN CHAT LOGIC ----------------

if user_query and not disabled:

    add_message("user", user_query)
    st.session_state.thinking = True

    struct = build_structured(user_query)

    if st.session_state.pending_struct:
        for k, v in struct.items():
            if v:
                st.session_state.pending_struct[k] = v
        struct = st.session_state.pending_struct

    if needs_clarification(struct):
        question = get_next_question(struct)
        st.session_state.pending_struct = struct
        add_message("assistant", question)
        st.session_state.thinking = False
        st.rerun()

    st.session_state.pending_struct = None

    risk = triage(struct["symptoms"], struct["severity"], struct["duration"])
    rag = retrieve_conditions(" ".join(struct["symptoms"]))
    prompt = build_medical_prompt(user_query, rag, risk)
    llm_output = generate_medical_response(prompt)
    final = add_medical_safety(llm_output, risk)

    add_message(
    "assistant",
    final,
    meta={"structured": True, "risk": risk, "struct": struct}
)

    st.session_state.thinking = False
    st.rerun()

