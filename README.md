# 🗳️ VoteWise AI — Election Education Assistant

> An AI-powered interactive assistant that helps citizens understand the election process, voter rights, timelines, and civic duties.

[![Google Cloud Run](https://img.shields.io/badge/Deployed%20on-Cloud%20Run-4285F4?logo=google-cloud)](https://cloud.google.com/run)
[![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-orange)](https://ai.google.dev)

---

## 🎯 Chosen Vertical

**Election Process Education** — Making the election process accessible, understandable, and engaging for every citizen through an interactive AI assistant.

---

## 💡 Approach & Logic

VoteWise AI combines **Google Gemini's language capabilities** with structured civic education content to create a multi-feature educational platform:

### 1. 💬 AI Chatbot (Ask VoteWise)
- Powered by **Gemini 1.5 Flash** with a detailed election-education system prompt
- Maintains conversation history for contextual follow-up questions
- Covers: voter registration, EVM usage, MCC, NOTA, constituency boundaries, results, government formation

### 2. 📅 Election Timeline
- Visual step-by-step breakdown of the Indian General Election process
- 11 stages: Announcement → MCC → Nomination → Scrutiny → Campaign → Silence Period → Polling → Counting → Results → Government Formation

### 3. 🧠 Civic Quiz
- 8 carefully crafted questions on Indian election fundamentals
- Instant feedback with explanations after each answer
- Score tracking and performance evaluation

### 4. ✅ Voter Eligibility Checker
- User inputs age and country
- Gemini API generates country-specific eligibility information
- Covers required documents, registration steps, and deadlines

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| AI | Google Gemini 1.5 Flash API |
| Google Service | Google Sheets API (interaction logging) |
| Deployment | Google Cloud Run |
| Container | Docker |
| Frontend | HTML5 + CSS3 + Vanilla JS |

---

## 🚀 How It Works

```
User → Frontend UI → Flask API → Gemini 1.5 Flash → Response
                              ↓
                    Google Sheets (logs Q&A)
```

1. User interacts via one of 4 modules (Chat, Timeline, Quiz, Eligibility)
2. Chat queries are sent to the Flask backend
3. Backend forwards chat prompts to Gemini API with an election-education system prompt
4. Response is returned and displayed in real-time
5. Timeline, Quiz, and basic Eligibility checks run client-side for a seamless, instant UI experience
6. Interactions are optionally logged to Google Sheets for analytics

---

## 📦 Project Structure

```
votewise-ai/
├── app.py              # Flask backend with Gemini + Sheets integration
├── test_app.py         # Unit tests using Pytest
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container config for Cloud Run
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore file
├── templates/
│   └── index.html      # Full frontend (single-file, no framework)
└── README.md
```

---

## ⚙️ Environment Variables

```bash
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_SHEET_ID=optional_sheet_id_for_logging
GOOGLE_SHEETS_CREDS=optional_service_account_json
PORT=8080
```

---

## 📸 Screenshots

<table>
  <tr>
    <td align="center" width="50%">
      <img src="screenshots/ask_votewise.png" alt="Ask VoteWise AI Chatbot" width="100%"/>
      <br/>
      <b>💬 Ask VoteWise</b>
      <br/>
      <sub>AI-powered chatbot for all election queries</sub>
    </td>
    <td align="center" width="50%">
      <img src="screenshots/election_timeline.png" alt="Election Timeline" width="100%"/>
      <br/>
      <b>📅 Election Timeline</b>
      <br/>
      <sub>11-step visual guide to the Indian election process</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="screenshots/civic_quiz.png" alt="Civic Quiz" width="100%"/>
      <br/>
      <b>🧠 Civic Quiz</b>
      <br/>
      <sub>8-question interactive quiz with live scoring</sub>
    </td>
    <td align="center" width="50%">
      <img src="screenshots/am_i_eligible.png" alt="Voter Eligibility Checker" width="100%"/>
      <br/>
      <b>✅ Am I Eligible?</b>
      <br/>
      <sub>Instant voter eligibility checker by age & country</sub>
    </td>
  </tr>
</table>

---

## 🏃 Running Locally

```bash
# Clone the repo
git clone https://github.com/shaikasadahmed2k23/votewise-ai.git
cd votewise-ai

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_key_here

# Run
python app.py
# Visit: http://localhost:8080
```

---

## ☁️ Deploying to Cloud Run

```bash
# Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/votewise-ai

# Deploy to Cloud Run
gcloud run deploy votewise-ai \
  --image gcr.io/YOUR_PROJECT_ID/votewise-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key
```

---

## 📋 Assumptions

- Default election context is **India (ECI system)** unless user specifies another country
- The chatbot is educational only — it remains politically neutral at all times
- Google Sheets logging is optional; the app works fully without it
- Quiz questions are focused on Indian elections but the chatbot covers global election systems

---

## ♿ Accessibility

- ARIA labels on all interactive elements
- Keyboard navigation support (Enter to send messages)
- Screen reader-friendly live regions for chat and eligibility results
- High contrast civic color scheme (saffron, blue, green — Indian flag inspired)
- Responsive design for mobile and desktop

---

## 🔐 Security

- API keys stored as environment variables, never in code
- Input validation on all API endpoints
- CORS configured properly
- No sensitive data stored client-side

---

## 🧪 Testing

```bash
# Run unit tests locally with pytest
pytest test_app.py

# Alternatively, run tests using Python directly
python test_app.py

# Test health endpoint on Cloud Run
curl https://YOUR_CLOUD_RUN_URL/api/health

# Test chat endpoint
curl -X POST https://YOUR_CLOUD_RUN_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I register to vote in India?", "history": []}'

# Test eligibility endpoint
curl -X POST https://YOUR_CLOUD_RUN_URL/api/eligibility \
  -H "Content-Type: application/json" \
  -d '{"age": 20, "country": "India"}'
```

---

## 👨‍💻 Author

**Shaik Asad Ahmed**  
B.Tech Computer Science (AI) | 4th Year  
GitHub: [@shaikasadahmed2k23](https://github.com/shaikasadahmed2k23)

---

*Built with ❤️ for Prompt Wars Hackathon — Google Developer Groups*
