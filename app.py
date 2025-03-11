import streamlit as st
import sqlite3

# Database setup
def create_connection():
    conn = sqlite3.connect("bns_lawbot.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bns_laws (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        offense TEXT UNIQUE,
                        section TEXT,
                        punishment TEXT
                    )''')
    conn.commit()
    conn.close()

def insert_data():
    conn = create_connection()
    cursor = conn.cursor()
    sample_data = [
        ("theft", "Section 303", "Imprisonment of up to 3 years, or a fine, or both."),
        ("murder", "Section 302", "Life imprisonment or the death penalty, along with a fine."),
        ("assault", "Section 351", "Imprisonment of up to 1 year, or a fine, or both."),
        ("fraud", "Section 420", "Imprisonment of up to 7 years, and a fine."),
        ("hit and run", "Section 279 & 304A", "Imprisonment of up to 2 years, or a fine, or both."),
        ("rash driving", "Section 279", "Imprisonment of up to 6 months, or a fine, or both."),
        ("drunk driving", "Section 185 of Motor Vehicles Act", "Fine up to ₹10,000 or imprisonment of up to 6 months."),
        ("domestic violence", "Section 498A", "Imprisonment of up to 3 years, and a fine."),
        ("cyber fraud", "Section 66D of IT Act", "Imprisonment of up to 3 years and a fine.")
    ]
    cursor.executemany('''INSERT OR IGNORE INTO bns_laws (offense, section, punishment) VALUES (?, ?, ?)''', sample_data)
    conn.commit()
    conn.close()

def query_bns(query):
    conn = create_connection()
    cursor = conn.cursor()
    
    # Mapping keywords to legal cases
    keywords = {
        "hit my car": "hit and run",
        "accident and ran": "hit and run",
        "punched me": "assault",
        "slapped me": "assault",
        "scammed": "fraud",
        "stole from me": "theft",
        "drunk and driving": "drunk driving",
        "husband beat me": "domestic violence",
        "cheated online": "cyber fraud"
    }
    
    for key, offense in keywords.items():
        if key in query.lower():
            cursor.execute("SELECT section, punishment FROM bns_laws WHERE offense LIKE ?", (f"%{offense}%",))
            result = cursor.fetchone()
            conn.close()
            return f"This falls under '{offense.capitalize()}'. Relevant Section: {result[0]} - {result[1]}" if result else "⚠️ No specific criminal law provision found for your query."
    
    conn.close()
    return "⚠️ No specific criminal law provision found for your query."

# Initialize database
db_conn = create_connection()
create_table()
insert_data()
db_conn.close()

# Streamlit UI
st.title("🧑‍⚖️ LawBot - Criminal Law Assistant for BNS")
st.write("Ask me anything about criminal offenses under Bharatiya Nyaya Sanhita (BNS)!")

# User input
user_query = st.text_input("Enter your legal query:")
if user_query:
    response = query_bns(user_query.lower())
    st.subheader("Relevant Legal Sections:")
    st.write(response)