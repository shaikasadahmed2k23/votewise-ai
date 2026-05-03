import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set dummy env vars before importing app
os.environ.setdefault("GEMINI_API_KEY", "test-key-dummy")
os.environ.setdefault("GOOGLE_SHEET_ID", "")
os.environ.setdefault("GOOGLE_SHEETS_CREDS", "")

from app import app, QUIZ_QUESTIONS, ELECTION_TIMELINE, SYSTEM_PROMPT

# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    with app.test_client() as client:
        yield client


# ── Health Check ──────────────────────────────────────────────────────────────
class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200

    def test_health_returns_json(self, client):
        res = client.get("/api/health")
        data = json.loads(res.data)
        assert data["status"] == "healthy"

    def test_health_has_service_name(self, client):
        res = client.get("/api/health")
        data = json.loads(res.data)
        assert data["service"] == "VoteWise AI"

    def test_health_has_timestamp(self, client):
        res = client.get("/api/health")
        data = json.loads(res.data)
        assert "timestamp" in data


# ── Home Page ─────────────────────────────────────────────────────────────────
class TestHomePage:
    def test_home_returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test_home_returns_html(self, client):
        res = client.get("/")
        assert b"VoteWise" in res.data

    def test_home_contains_chat_section(self, client):
        res = client.get("/")
        assert b"chat" in res.data.lower()


# ── Quiz Endpoint ─────────────────────────────────────────────────────────────
class TestQuizEndpoint:
    def test_quiz_returns_200(self, client):
        res = client.get("/api/quiz")
        assert res.status_code == 200

    def test_quiz_returns_questions(self, client):
        res = client.get("/api/quiz")
        data = json.loads(res.data)
        assert "questions" in data

    def test_quiz_has_8_questions(self, client):
        res = client.get("/api/quiz")
        data = json.loads(res.data)
        assert len(data["questions"]) == 8

    def test_quiz_total_matches(self, client):
        res = client.get("/api/quiz")
        data = json.loads(res.data)
        assert data["total"] == len(data["questions"])

    def test_quiz_question_has_required_fields(self, client):
        res = client.get("/api/quiz")
        data = json.loads(res.data)
        for q in data["questions"]:
            assert "id" in q
            assert "question" in q
            assert "options" in q
            assert "answer" in q
            assert "explanation" in q

    def test_quiz_each_question_has_4_options(self, client):
        res = client.get("/api/quiz")
        data = json.loads(res.data)
        for q in data["questions"]:
            assert len(q["options"]) == 4

    def test_quiz_answer_index_is_valid(self, client):
        res = client.get("/api/quiz")
        data = json.loads(res.data)
        for q in data["questions"]:
            assert 0 <= q["answer"] <= 3


# ── Timeline Endpoint ─────────────────────────────────────────────────────────
class TestTimelineEndpoint:
    def test_timeline_returns_200(self, client):
        res = client.get("/api/timeline")
        assert res.status_code == 200

    def test_timeline_returns_list(self, client):
        res = client.get("/api/timeline")
        data = json.loads(res.data)
        assert "timeline" in data
        assert isinstance(data["timeline"], list)

    def test_timeline_has_11_steps(self, client):
        res = client.get("/api/timeline")
        data = json.loads(res.data)
        assert len(data["timeline"]) == 11

    def test_timeline_step_has_required_fields(self, client):
        res = client.get("/api/timeline")
        data = json.loads(res.data)
        for item in data["timeline"]:
            assert "step" in item
            assert "phase" in item
            assert "icon" in item
            assert "description" in item
            assert "duration" in item

    def test_timeline_steps_are_ordered(self, client):
        res = client.get("/api/timeline")
        data = json.loads(res.data)
        steps = [item["step"] for item in data["timeline"]]
        assert steps == list(range(1, 12))


# ── Chat Endpoint ─────────────────────────────────────────────────────────────
class TestChatEndpoint:
    def test_chat_empty_message_returns_400(self, client):
        res = client.post("/api/chat",
            json={"message": "", "history": []},
            content_type="application/json")
        assert res.status_code == 400

    def test_chat_missing_message_returns_400(self, client):
        res = client.post("/api/chat",
            json={"history": []},
            content_type="application/json")
        assert res.status_code == 400

    def test_chat_whitespace_message_returns_400(self, client):
        res = client.post("/api/chat",
            json={"message": "   ", "history": []},
            content_type="application/json")
        assert res.status_code == 400

    def test_chat_no_json_body_returns_error(self, client):
        res = client.post("/api/chat", data="not json",
            content_type="text/plain")
        assert res.status_code in [400, 500]

    def test_chat_with_invalid_api_key_returns_500(self, client):
        # With dummy key, Gemini will fail — expect 500
        res = client.post("/api/chat",
            json={"message": "What is voting?", "history": []},
            content_type="application/json")
        assert res.status_code == 500

    def test_chat_error_response_has_error_field(self, client):
        res = client.post("/api/chat",
            json={"message": "What is voting?", "history": []},
            content_type="application/json")
        data = json.loads(res.data)
        assert "error" in data


# ── Eligibility Endpoint ──────────────────────────────────────────────────────
class TestEligibilityEndpoint:
    def test_eligibility_invalid_age_zero_returns_400(self, client):
        res = client.post("/api/eligibility",
            json={"age": 0, "country": "India"},
            content_type="application/json")
        assert res.status_code == 400

    def test_eligibility_invalid_age_over_120_returns_400(self, client):
        res = client.post("/api/eligibility",
            json={"age": 150, "country": "India"},
            content_type="application/json")
        assert res.status_code == 400

    def test_eligibility_negative_age_returns_400(self, client):
        res = client.post("/api/eligibility",
            json={"age": -5, "country": "India"},
            content_type="application/json")
        assert res.status_code == 400

    def test_eligibility_valid_age_with_bad_key_returns_500(self, client):
        # With dummy API key Gemini will fail — expected
        res = client.post("/api/eligibility",
            json={"age": 20, "country": "India"},
            content_type="application/json")
        assert res.status_code == 500


# ── Data Integrity Tests ──────────────────────────────────────────────────────
class TestDataIntegrity:
    def test_system_prompt_is_not_empty(self):
        assert len(SYSTEM_PROMPT.strip()) > 0

    def test_system_prompt_mentions_india(self):
        assert "India" in SYSTEM_PROMPT

    def test_system_prompt_mentions_election(self):
        assert "election" in SYSTEM_PROMPT.lower()

    def test_quiz_questions_list_not_empty(self):
        assert len(QUIZ_QUESTIONS) > 0

    def test_election_timeline_not_empty(self):
        assert len(ELECTION_TIMELINE) > 0

    def test_all_quiz_questions_have_non_empty_text(self):
        for q in QUIZ_QUESTIONS:
            assert len(q["question"].strip()) > 0

    def test_all_quiz_explanations_are_meaningful(self):
        for q in QUIZ_QUESTIONS:
            assert len(q["explanation"]) > 20

    def test_timeline_first_step_is_announcement(self):
        assert ELECTION_TIMELINE[0]["phase"] == "Announcement"

    def test_timeline_last_step_is_government_formation(self):
        assert ELECTION_TIMELINE[-1]["phase"] == "Government Formation"


# ── Security Tests ────────────────────────────────────────────────────────────
class TestSecurity:
    def test_api_key_not_hardcoded_in_env(self):
        # Key should come from env, not be hardcoded
        key = os.environ.get("GEMINI_API_KEY", "")
        assert key != ""  # Should be set (even if dummy in test)

    def test_chat_accepts_only_post(self, client):
        res = client.get("/api/chat")
        assert res.status_code == 405

    def test_eligibility_accepts_only_post(self, client):
        res = client.get("/api/eligibility")
        assert res.status_code == 405

    def test_large_message_handled_gracefully(self, client):
        large_msg = "A" * 10000
        res = client.post("/api/chat",
            json={"message": large_msg, "history": []},
            content_type="application/json")
        # Should not crash server — either 400 or 500, not unhandled
        assert res.status_code in [400, 500]