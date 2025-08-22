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
import pandas as pd
from datetime import datetime
import os

# File path to save data
csv_file = "scores.csv"

# Save data if form was submitted
if submitted:
    # Create a new row of data
    new_row = {
        ""Date": st.date_input("Match Date", datetime.today()).strftime("%Y-%m-%d"),
        "Player": player_name,
        "Win": match_result,
        "Technique": technique,
        "Tactics": tactics,
        "Effort": effort,
        "Penalty": penalty,
        "Total": total
    }

    # Check if CSV exists — if not, create one
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    # Save to CSV
    df.to_csv(csv_file, index=False)
    st.success("🎉 Score saved to leaderboard!")

# Load scores if file exists
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)

    st.subheader("📊 GSA UTR+ Leaderboard")
    leaderboard = df.groupby("Player")["Total"].sum().sort_values(ascending=False).reset_index()
    st.dataframe(leaderboard)

    st.subheader("📈 Weekly Progress by Player")
    player_to_plot = st.selectbox("Choose a player", df["Player"].unique())

    # Filter for selected player
    player_data = df[df["Player"] == player_to_plot]

    # Group by date and sum score
    weekly_progress = player_data.groupby("Date")["Total"].sum().reset_index()

    st.line_chart(weekly_progress.set_index("Date"))
