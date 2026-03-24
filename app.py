import streamlit as st
import random
import os

st.set_page_config(page_title="פסיכומטרי Master", page_icon="🚀")

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

# אתחול משתנים ב-Session
if 'target' not in st.session_state:
    st.session_state.target = random.choice(list(vocabulary.keys()))
    st.session_state.score = 0
    st.session_state.show_balloons = False

st.title("🚀 פסיכומטרי Master")

target = st.session_state.target
correct = vocabulary[target]

# הצגת הבלונים בראש הדף אם המשתמש צדק
if st.session_state.show_balloons:
    st.balloons()

st.subheader(f"מה הפירוש של: **{target}**?")

other_defs = [v for k, v in vocabulary.items() if v != correct]
options = random.sample(other_defs, min(3, len(other_defs))) + [correct]
random.shuffle(options)

# יצירת כפתורים לתשובות
for opt in options:
    if st.button(opt, use_container_width=True, key=f"btn_{opt}"):
        if opt == correct:
            st.session_state.show_balloons = True
            st.session_state.score += 1
            st.rerun() # מרענן כדי להציג את הבלונים למעלה
        else:
            st.session_state.show_balloons = False
            st.error(f"לא נכון... {target} זה {correct}")

st.divider()

# כפתור למעבר מילה - רק הוא מאפס את הבלונים
if st.button("למילה הבאה ➡️", type="primary"):
    st.session_state.target = random.choice(list(vocabulary.keys()))
    st.session_state.show_balloons = False
    st.rerun()

st.sidebar.metric("מילים שזכרת", st.session_state.score)
