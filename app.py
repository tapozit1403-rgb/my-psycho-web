import streamlit as st
import random
import os

st.set_page_config(page_title="פסיכומטרי Master", page_icon="🚀")

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

if not vocabulary:
    st.error("לא נמצאו מילים ב-words.txt")
else:
    if 'target' not in st.session_state:
        st.session_state.target = random.choice(list(vocabulary.keys()))
        st.session_state.score = 0

    st.title("🚀 פסיכומטרי Master")
    
    target = st.session_state.target
    correct = vocabulary[target]
    
    st.subheader(f"מה הפירוש של: {target}?")
    
    other_defs = [v for k, v in vocabulary.items() if v != correct]
    options = random.sample(other_defs, min(3, len(other_defs))) + [correct]
    random.shuffle(options)

    for opt in options:
        if st.button(opt, use_container_width=True):
            if opt == correct:
                st.balloons()
                st.success("נכון!")
                st.session_state.score += 1
            else:
                st.error(f"טעות... הפירוש הוא {correct}")
            
            if st.button("למילה הבאה"):
                st.session_state.target = random.choice(list(vocabulary.keys()))
                st.rerun()

    st.sidebar.write(f"ניקוד: {st.session_state.score}")
