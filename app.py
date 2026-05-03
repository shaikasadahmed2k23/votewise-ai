import os
import json
import logging
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL = "gemini-2.0-flash"

SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "")
SHEETS_CREDS_JSON = os.environ.get("GOOGLE_SHEETS_CREDS", "")

SYSTEM_PROMPT = """
You are VoteWise AI — a friendly, clear, and knowledgeable Election Education Assistant.
Your job is to help users understand election processes, timelines, voter rights, and civic duties.
You cover topics like voter registration, types of elections, how voting works, election timelines,
role of Election Commission, voter rights, how results are declared, electoral systems, and
India-specific election process (ECI, EVMs, Model Code of Conduct, etc.).
Rules:
- Always be factual, neutral, and educational
- Use simple language with bullet points and emojis
- Default context is India unless user specifies otherwise
- Never give political opinions or support any party/candidate
- Suggest official sources like eci.gov.in when unsure
"""

QUIZ_QUESTIONS = [
    {"id": 1, "question": "What is the minimum age to vote in Indian General Elections?",
     "options": ["16 years", "18 years", "21 years", "25 years"], "answer": 1,
     "explanation": "In India, citizens who are 18 years or older are eligible to vote as per Article 326 of the Constitution."},
    {"id": 2, "question": "What does EVM stand for?",
     "options": ["Electronic Voting Machine", "Election Verification Method", "Electronic Vote Monitor", "Electoral Voting Mechanism"], "answer": 0,
     "explanation": "EVM stands for Electronic Voting Machine. India adopted EVMs to make voting faster, more accurate, and tamper-resistant."},
    {"id": 3, "question": "Which body conducts General Elections in India?",
     "options": ["Supreme Court", "Parliament", "Election Commission of India", "President of India"], "answer": 2,
     "explanation": "The Election Commission of India (ECI) is an autonomous constitutional authority responsible for administering election processes in India."},
    {"id": 4, "question": "What is the Model Code of Conduct?",
     "options": ["A code for elected officials after winning", "Guidelines for voter behavior on election day", "A set of guidelines for political parties during elections", "Rules for counting votes"], "answer": 2,
     "explanation": "The Model Code of Conduct is a set of guidelines issued by the ECI for political parties and candidates during elections to ensure free and fair elections."},
    {"id": 5, "question": "What is NOTA in Indian elections?",
     "options": ["Name of the Actual candidate", "None Of The Above", "National Online Tracking Application", "New Order of Territorial Administration"], "answer": 1,
     "explanation": "NOTA (None Of The Above) allows voters to reject all candidates on the ballot. It was introduced in India in 2013 following a Supreme Court order."},
    {"id": 6, "question": "How often are Lok Sabha elections held in India?",
     "options": ["Every 3 years", "Every 4 years", "Every 5 years", "Every 6 years"], "answer": 2,
     "explanation": "Lok Sabha elections are held every 5 years unless the house is dissolved earlier."},
    {"id": 7, "question": "What is a constituency?",
     "options": ["A political party", "A geographic area represented by one elected official", "The election commission office", "A type of ballot paper"], "answer": 1,
     "explanation": "A constituency is a geographic division of voters who elect a representative. India has 543 Lok Sabha constituencies."},
    {"id": 8, "question": "What document is primarily used as voter ID in India?",
     "options": ["Aadhar Card", "PAN Card", "EPIC (Voter ID Card)", "Passport"], "answer": 2,
     "explanation": "EPIC (Electors Photo Identity Card), commonly called the Voter ID card, is the primary document for voter identification in India."}
]

ELECTION_TIMELINE = [
    {"step": 1, "phase": "Announcement", "icon": "📢", "description": "Election Commission announces election dates and schedule", "duration": "Day 1"},
    {"step": 2, "phase": "Model Code of Conduct", "icon": "📋", "description": "MCC comes into effect — parties must follow guidelines", "duration": "Immediately after announcement"},
    {"step": 3, "phase": "Nomination Filing", "icon": "📝", "description": "Candidates file nomination papers with the returning officer", "duration": "~7 days"},
    {"step": 4, "phase": "Scrutiny", "icon": "🔍", "description": "Nominations are scrutinized for validity and eligibility", "duration": "1 day after last nomination"},
    {"step": 5, "phase": "Withdrawal of Candidature", "icon": "↩️", "description": "Last date for candidates to withdraw from the election", "duration": "2 days after scrutiny"},
    {"step": 6, "phase": "Campaign Period", "icon": "🗣️", "description": "Parties and candidates campaign, hold rallies, and outreach voters", "duration": "~14 days"},
    {"step": 7, "phase": "Campaign Silence", "icon": "🤫", "description": "No campaigning allowed 48 hours before polling", "duration": "48 hours before polling"},
    {"step": 8, "phase": "Polling Day", "icon": "🗳️", "description": "Voters cast their votes at designated polling booths", "duration": "Single day (7 AM – 6 PM)"},
    {"step": 9, "phase": "Vote Counting", "icon": "🔢", "description": "Votes are counted under strict supervision", "duration": "Counting day (set by ECI)"},
    {"step": 10, "phase": "Results & Declaration", "icon": "🏆", "description": "Winners declared, results published on ECI website", "duration": "Same day as counting"},
    {"step": 11, "phase": "Government Formation", "icon": "🏛️", "description": "Winning party/coalition forms government, oath-taking ceremony", "duration": "Within 2–4 weeks"}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Message is required"}), 400
        user_message = data.get("message", "").strip()
        chat_history = data.get("history", [])
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        conversation = SYSTEM_PROMPT + "\n\n"
        for msg in chat_history[-10:]:
            role_label = "User" if msg["role"] == "user" else "VoteWise AI"
            conversation += f"{role_label}: {msg['content']}\n"
        conversation += f"User: {user_message}\nVoteWise AI:"
        response = client.models.generate_content(model=MODEL, contents=conversation)
        reply = response.text
        if SHEET_ID and SHEETS_CREDS_JSON:
            try:
                log_to_sheets(user_message, reply)
            except Exception as e:
                logger.warning(f"Sheets logging failed: {e}")
        return jsonify({"reply": reply, "status": "success"})
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": "Something went wrong. Please try again.", "status": "error"}), 500

@app.route("/api/quiz", methods=["GET"])
def get_quiz():
    return jsonify({"questions": QUIZ_QUESTIONS, "total": len(QUIZ_QUESTIONS)})

@app.route("/api/timeline", methods=["GET"])
def get_timeline():
    return jsonify({"timeline": ELECTION_TIMELINE})

@app.route("/api/eligibility", methods=["POST"])
def check_eligibility():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400
        age = int(data.get("age", 0))
        country = data.get("country", "India").strip()
        if age < 1 or age > 120:
            return jsonify({"error": "Invalid age"}), 400
        prompt = f"{SYSTEM_PROMPT}\n\nA user wants to know about voter eligibility.\nAge: {age} years old\nCountry: {country}\nTell them: 1. Whether they are eligible 2. What documents they need 3. How to register 4. Important deadlines. Be specific to {country}. Use bullet points."
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return jsonify({"result": response.text, "age": age, "country": country})
    except Exception as e:
        logger.error(f"Eligibility error: {e}")
        return jsonify({"error": "Could not check eligibility."}), 500

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "VoteWise AI", "timestamp": datetime.now().isoformat()})

def log_to_sheets(question: str, answer: str):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds_dict = json.loads(SHEETS_CREDS_JSON)
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=creds)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = [[timestamp, question[:500], answer[:500]]]
    service.spreadsheets().values().append(spreadsheetId=SHEET_ID, range="Sheet1!A:C", valueInputOption="RAW", body={"values": values}).execute()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)