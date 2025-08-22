import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="GSA UTR+", layout="centered")
st.title("🎾 GSA Beyond UTR+ System")
st.caption("Own it. Rise it. Go beyond.")

csv_file = "scores.csv"

# ------------------ FORM: Coach Input ------------------ #
st.header("📋 Coach Evaluation Form")

with st.form("utr_input"):
    player_name = st.text_input("Player Name")
    match_date = st.date_input("Match Date", datetime.today()).strftime("%Y-%m-%d")
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

        new_row = {
            "Date": match_date,
            "Player": player_name,
            "Win": match_result,
            "Technique": technique,
            "Tactics": tactics,
            "Effort": effort,
            "Penalty": penalty,
            "Total": total
        }

        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])

        df.to_csv(csv_file, index=False)
        st.success(f"✅ {player_name} scored {total} UTR+ points. Saved to leaderboard!")

# ------------------ DELETE PLAYER SECTION ------------------ #
st.header("🗑️ Delete Player Scores")

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)

    all_players = df["Player"].unique()
    player_to_delete = st.selectbox("Select a player to delete all scores for:", all_players)

    if st.button("Delete Player Data"):
        df = df[df["Player"] != player_to_delete]
        df.to_csv(csv_file, index=False)
        st.warning(f"⚠️ All data for {player_to_delete} has been deleted.")
        st.experimental_rerun()

# ------------------ LEADERBOARD ------------------ #
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)

    st.header("🏆 UTR+ Leaderboard")
    leaderboard = df.groupby("Player")["Total"].sum().sort_values(ascending=False).reset_index()
    st.dataframe(leaderboard)

    # ------------------ Weekly Progress ------------------ #
    st.header("📈 Weekly Progress Chart")
    player_to_plot = st.selectbox("Choose a player to view progress:", df["Player"].unique())

    player_data = df[df["Player"] == player_to_plot]
    weekly_progress = player_data.groupby("Date")["Total"].sum().reset_index()
    st.line_chart(weekly_progress.set_index("Date"))
