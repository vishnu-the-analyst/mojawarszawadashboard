import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# MySQL database connection details
endpoint = 'sql7.freesqldatabase.com'
username = 'sql7714154'
password = 'UE9b4TPXsp'
database_name = 'sql7714154'

# Function to fetch leaderboard data from MySQL
def fetch_leaderboard():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host=endpoint,
            user=username,
            password=password,
            database=database_name
        )

        if conn.is_connected():
            # Prepare SQL query to fetch leaderboard data
            query = """
                SELECT user_id, SUM(score) AS Total_Score
                FROM leaderboard
                GROUP BY user_id
                ORDER BY Total_Score DESC
            """

            # Execute the query
            cursor = conn.cursor()
            cursor.execute(query)

            # Fetch all rows from the result set
            results = cursor.fetchall()

            # Close cursor and connection
            cursor.close()
            conn.close()

            return results

    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

# Function to apply rewards based on leaderboard rank
def apply_rewards(leaderboard_data):
    # Display leaderboard in Streamlit
    st.subheader("🏆 Contributors Leaderboard and Rewards 🏆")
    if leaderboard_data:
        # Prepare data for table display
        df = pd.DataFrame(leaderboard_data, columns=['User ID', 'Total Score'])
        df['Rank'] = range(1, len(df) + 1)

        # Apply rewards based on rank
        rewards = {
            1: "🥇 10% tax cut",
            2: "🥈 5% tax cut",
            3: "🥉 3% tax cut"
        }

        df['Reward'] = df['Rank'].apply(lambda rank: rewards.get(rank, "Free 1-month ZTM pass"))

        # Display leaderboard in table format
        st.dataframe(df[['Rank', 'User ID', 'Total Score', 'Reward']].style
                     .highlight_max(subset=['Total Score'], color='skyblue')
                     .set_properties(**{'text-align': 'center'}))

    else:
        st.warning("No data found.")

# Function to explain how to win attractive prizes
def explain_prizes():
    st.subheader("🌟 How to Win Attractive Prizes 🌟")
    st.markdown("""
        Contributing more to the society of Warsaw through various initiatives not only helps in
        improving the community but also rewards you with attractive prizes! Here's how you can
        maximize your impact and rewards:
        - **Top Contributors**: Top 3 contributors receive tax cuts in their income tax.
        - **Rank 4 to 10**: Receive a free one-month ZTM public transport pass.
        - **Community Engagement**: Engage with @mojawarszawabot on Telegram to participate
          in community-driven activities and initiatives.
    """)

# Main function to run the Streamlit app
def main():
    # Title and introduction
    st.title('🌍 Warsaw Community Contributions Dashboard 🌍')
    st.write("""
        Welcome to the Warsaw Community Contributions Dashboard! This dashboard showcases the
        top contributors and rewards for their valuable contributions to the society of Warsaw.
        Explore the leaderboard, learn about rewards, and engage with community initiatives
        through @mojawarszawabot on Telegram.
    """)

    # Fetch leaderboard data from MySQL
    leaderboard_data = fetch_leaderboard()

    # Apply rewards based on leaderboard rank
    apply_rewards(leaderboard_data)

    # Explain how to win attractive prizes
    explain_prizes()

if __name__ == "__main__":
    main()
