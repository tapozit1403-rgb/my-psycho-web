import streamlit as st
import random
import os

# הגדרות דף ועיצוב
st.set_page_config(page_title="פסיכומטרי Master 🚀", page_icon="🚀", layout="centered")

# פונקציה לטעינת מילים מתוך words.txt
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

# אתחול משתני המערכת (Session State)
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'wrong_count' not in st.session_state:
    st.session_state.wrong_count = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'target' not in st.session_state:
    st.session_state.target = random.choice(list(vocabulary.keys())) if vocabulary else ""

# פונקציה למעבר למילה הבאה
def next_word():
    if vocabulary:
        st.session_state.target = random.choice(list(vocabulary.keys()))
    st.session_state.answered = False

# --- תצוגת צד (Sidebar) לניקוד ---
st.sidebar.title("📊 לוח תוצאות")
st.sidebar.divider()
st.sidebar.metric("✅ תשובות נכונות", st.session_state.correct_count)
st.sidebar.metric("❌ טעויות", st.session_state.wrong_count)

total = st.session_state.correct_count + st.session_state.wrong_count
if total > 0:
    accuracy = (st.session_state.correct_count / total) * 100
    st.sidebar.write(f"דיוק: {accuracy:.1f}%")

if st.sidebar.button("אפס נתונים"):
    st.session_state.correct_count = 0
    st.session_state.wrong_count = 0
    st.rerun()

# --- גוף האתר ---
st.title("🚀 פסיכומטרי Master")

if not vocabulary:
    st.error("לא נמצאו מילים בקובץ words.txt. וודא שהקובץ קיים ב-GitHub.")
else:
    target = st.session_state.target
    correct_def = vocabulary[target]

    st.subheader(f"איך אומרים בעברית: **{target}**?")

    # יצירת אפשרויות (מסיחים)
    all_defs = list(set(vocabulary.values()))
    if correct_def in all_defs: all_defs.remove(correct_def)
    distractors = random.sample(all_defs, min(3, len(all_defs)))
    options = distractors + [correct_def]
    random.shuffle(options)

    # כפתורי תשובה
    for opt in options:
        # הכפתורים ננעלים אחרי לחיצה כדי שלא ילחצו פעמיים
        if st.button(opt, use_container_width=True, key=opt, disabled=st.session_state.answered):
            st.session_state.answered = True
            if opt == correct_def:
                st.balloons() # הבלונים מופיעים כאן!
                st.session_state.correct_count += 1
                st.success(f"נכון מאוד! {target} זה {correct_def}")
            else:
                st.session_state.wrong_count += 1
                st.error(f"טעות... {target} פירושו: {correct_def}")
            
            st.rerun() # מרענן כדי לעדכן את הניקוד בצד מיד

    # כפתור מעבר למילה הבאה (מופיע רק אחרי שענו)
    if st.session_state.answered:
        st.button("המילה הבאה ➡️", on_click=next_word, type="primary", use_container_width=True)
