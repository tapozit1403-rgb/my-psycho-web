import streamlit as st
import random
import os

# הגדרות דף
st.set_page_config(page_title="פסיכומטרי Master 🚀", page_icon="🚀")

# פונקציה לטעינת מילים
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

# אתחול משתני מערכת (Session State)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered_correctly' not in st.session_state:
    st.session_state.answered_correctly = False
if 'target' not in st.session_state:
    st.session_state.target = random.choice(list(vocabulary.keys()))

def next_word():
    st.session_state.target = random.choice(list(vocabulary.keys()))
    st.session_state.answered_correctly = False

# עיצוב הכותרת
st.title("🚀 פסיכומטרי Master")
st.write("תרגול מילים חכם וממוקד")

target = st.session_state.target
correct = vocabulary[target]

# הצגת השאלה
st.subheader(f"מה הפירוש של: **{target}**?")

# יצירת מסיחים (תשובות לא נכונות)
all_defs = list(set(vocabulary.values()))
if correct in all_defs: all_defs.remove(correct)
distractors = random.sample(all_defs, min(3, len(all_defs)))
options = distractors + [correct]
random.shuffle(options)

# הצגת כפתורי התשובות
# אם המשתמש כבר ענה נכון, ננעל את הכפתורים כדי שלא ילחץ שוב
for opt in options:
    if st.button(opt, use_container_width=True, disabled=st.session_state.answered_correctly, key=opt):
        if opt == correct:
            st.session_state.answered_correctly = True
            st.session_state.score += 1
            st.balloons()
            st.rerun()
        else:
            st.error(f"טעות... הפירוש של {target} הוא: {correct}")

# הצגת כפתור "המילה הבאה" - מופיע רק אחרי תשובה נכונה
if st.session_state.answered_correctly:
    st.success(f"כל הכבוד! {target} = {correct}")
    st.button("המילה הבאה ➡️", on_click=next_word, type="primary", use_container_width=True)

# סטטיסטיקה בצד
st.sidebar.metric("מילים שבוצעו", st.session_state.score)
if st.sidebar.button("אפס ניקוד"):
    st.session_state.score = 0
    st.rerun()
