import streamlit as st
import random
import os

# הגדרות עיצוב דף
st.set_page_config(page_title="סוכן פסיכומטרי AI", page_icon="🎓")


# פונקציה לקריאת המילים מהקובץ words.txt
def load_words():
    vocab = {}
    if os.path.exists("words.txt"):
        with open("words.txt", "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    word, definition = line.strip().split(":", 1)
                    vocab[word.strip()] = definition.strip()
    return vocab


# טעינת נתונים
vocabulary = load_words()

if not vocabulary:
    st.error("לא נמצאו מילים בקובץ words.txt. וודא שהקובץ קיים ומכיל מילים בפורמט - מילה: פירוש")
else:
    words_list = list(vocabulary.keys())

    st.title("🎓 סוכן ה-AI שלך לפסיכומטרי")

    # ניהול מצב המערכת (Session State)
    if 'target_word' not in st.session_state:
        st.session_state.target_word = random.choice(words_list)
        st.session_state.score = 0
        st.session_state.total = 0


    def next_question():
        st.session_state.target_word = random.choice(words_list)


    # יצירת השאלה הנוכחית
    target = st.session_state.target_word
    correct = vocabulary[target]

    # יצירת מסיחים (תשובות לא נכונות)
    other_defs = [v for k, v in vocabulary.items() if k != target]
    if len(other_defs) >= 3:
        options = random.sample(other_defs, 3) + [correct]
    else:
        options = other_defs + [correct]
    random.shuffle(options)

    st.write(f"### מה הפירוש של המילה: **{target}**?")

    # יצירת כפתורי תשובה
    for option in options:
        if st.button(option, use_container_width=True):
            st.session_state.total += 1
            if option == correct:
                st.success("✅ כל הכבוד! תשובה נכונה.")
                st.session_state.score += 1
            else:
                st.error(f"❌ טעות. הפירוש הנכון הוא: {correct}")

            st.button("לשאלה הבאה ➡️", on_click=next_question)

    # הצגת ניקוד בצד
    st.sidebar.metric("הניקוד שלך", f"{st.session_state.score}/{st.session_state.total}")
    if st.sidebar.button("אפס ניקוד"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.rerun()