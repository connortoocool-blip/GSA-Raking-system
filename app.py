import streamlit as st

st.set_page_config(page_title="GSA UTR", layout="centered")

st.title("🎾 GSA Exclusive UTR System")
st.write("Own it. Rise it. Go beyond.")
st.success("Welcome to the GSA Beyond UTR Ranking App!")
st.header("🎾 GSA Coach Match Evaluation")

with st.form("utr_input"):
    player_name = st.text_input("Player Name")
    match_result = st.radio("Did the player win?", ["Yes", "No"])
    technique = st.slider("Technique Score (1–5)", 1, 5)
    tactics = st.slider("Tactical Awareness (1–3)", 1, 3)
    effort = st.slider("Effort & Attitude (1–3)", 1, 3)
    penalty = st.selectbox("Bad Habit Penalty", ["None", "Slicing too much", "No footwork", "Lazy recovery"])

    submitted = st.form_submit_button("Submit Score")

    if submitted:
        result_points = 3 if match_result == "Yes" else 0
        penalty_points = -2 if penalty != "None" else 0
        total = result_points + technique + tactics + effort + penalty_points

        st.success(f"✅ {player_name} scored **{total} UTR+ points** for this match!")
