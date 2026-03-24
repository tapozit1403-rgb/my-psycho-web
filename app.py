if st.button(opt, use_container_width=True, key=opt):
            if opt == correct:
                st.balloons()  # האנימציה
                st.success(f"💥 בול! {target} זה {correct}")
                st.session_state.score += 1
                # הוספת כפתור למעבר מילה שמופיע רק אחרי הצלחה
                if st.button("מעולה, למילה הבאה! ➡️"):
                    st.session_state.target = random.choice(list(vocabulary.keys()))
                    st.rerun()
            else:
                st.error(f"לא מדויק... {target} פירושו: {correct}")
                if st.button("ננסה מילה אחרת? 🔄"):
                    st.session_state.target = random.choice(list(vocabulary.keys()))
                    st.rerun()
