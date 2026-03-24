import streamlit as st
import random
import os

# הגדרות דף
st.set_page_config(page_title="פסיכומטרי Master 🚀", page_icon="🚀")

# טעינת מילים
def load_words():
    vocab = {}
    if os.path.exists("words.txt"):
        with open("words.txt", "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    word, definition = line.strip().split(":", 1)
                    vocab[word.strip()] = definition.strip()
    return vocab

vocabulary = load_words()

# ניהול מצב (Session State)
if 'correct' not in st.session_state: st.session_state.correct = 0
if 'wrong' not in st.session_state: st.session_state.wrong = 0
if 'show_party' not in st.session_state: st.session_state.show_party = False
if 'target' not in st.session_state: 
    st.session_state.target = random.choice(list(vocabulary.keys())) if vocabulary else ""

def next_question():
    st.session_state.target = random.choice(list(vocabulary.keys()))
    st.session_state.show_party = False

# --- חגיגה! (מופיע בראש הדף אם צדקת) ---
if st.session_state.show_party:
    st.balloons() # בלונים
    st.snow()     # שלג ליתר ביטחון

# --- תצוגת צד ---
st.sidebar.title("📊 ניקוד")
st.sidebar.metric("✅ הצלחות", st.session_state.correct)
st.sidebar.metric("❌ טעויות", st.session_state.wrong)
if st.sidebar.button("איפוס"):
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.rerun()

# --- גוף האתר ---
st.title("🚀 פסיכומטרי Master")

if vocabulary:
    target = st.session_state.target
    answer = vocabulary[target]

    st.subheader(f"מה זה: **{target}**?")

    # יצירת תשובות
    if 'options' not in st.session_state or not st.session_state.show_party:
        others = list(set(vocabulary.values()))
        if answer in others: others.remove(answer)
        st.session_state.options = random.sample(others, min(3, len(others))) + [answer]
        random.shuffle(st.session_state.options)

    # הצגת כפתורים
    for opt in st.session_state.options:
        if st.button(opt, use_container_width=True, disabled=st.session_state.show_party):
            if opt == answer:
                st.session_state.correct += 1
                st.session_state.show_party = True # מדליק את החגיגה
                st.rerun()
            else:
                st.session_state.wrong += 1
                st.error(f"טעות! {target} = {answer}")

    # כפתור מעבר מילה
    if st.session_state.show_party:
        st.success(f"בול! {target} זה {answer}")
        st.button("למילה הבאה ➡️", on_click=next_question, type="primary", use_container_width=True)
