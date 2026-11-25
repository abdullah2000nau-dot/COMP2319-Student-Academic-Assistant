from pathlib import Path
import json

from src.memory import search_documents

ROOT = Path(__file__).resolve().parent.parent
OUTBOX_FILE = ROOT / "data" / "outbox.json"

ASSIGNMENTS = [
    {
        "title": "AI Assistant Development Project",
        "course": "COMP2319",
        "deadline": "2026-12-03 11:59 PM Central",
        "status": "In progress"
    }
]

def search_course_materials(question):
    """Search academic documents and return source citations."""

    if not isinstance(question, str) or not question.strip():
        return {
            "success": False,
            "error": "A non-empty question is required."
        }

    result = search_documents(question)

    if not result["success"]:
        return result

    citations = []

    for item in result["results"]:
        citations.append({
            "source": item["source"],
            "chunk": item["chunk"],
            "text": item["text"],
            "similarity": round(item["similarity"], 3)
        })

    return {
        "success": True,
        "citations": citations
    }

def list_assignments():
    """Return available sample assignment information."""

    return {
        "success": True,
        "assignments": ASSIGNMENTS
    }

def draft_email(recipient, subject, message):
    """Create an email draft without sending it."""

    if not all(
        isinstance(value, str) and value.strip()
        for value in [recipient, subject, message]
    ):
        return {
            "success": False,
            "error": "Recipient, subject, and message are required."
        }

    return {
        "success": True,
        "status": "DRAFT_ONLY",
        "recipient": recipient,
        "subject": subject,
        "message": message,
        "notice": "This email has NOT been sent."
    }

def submit_email_for_approval(recipient, subject, message):
    """Save an email as pending human approval."""

    draft = draft_email(recipient, subject, message)

    if not draft["success"]:
        return draft

    OUTBOX_FILE.parent.mkdir(parents=True, exist_ok=True)

    records = []

    if OUTBOX_FILE.exists():
        records = json.loads(
            OUTBOX_FILE.read_text(encoding="utf-8")
        )

    import uuid

    approval_id = str(uuid.uuid4())[:8]

    records.append({
        "approval_id": approval_id,
        "recipient": recipient,
        "subject": subject,
        "message": message,
        "status": "PENDING"
    })

    OUTBOX_FILE.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8"
    )

    return {
        "success": True,
        "status": "PENDING_APPROVAL",
        "approval_id": approval_id,
        "notice": "Human approval is required before sending."
    }

def approve_email(approval_id, approved):
    """Approve or reject a pending email for local simulation."""

    if not isinstance(approved, bool):
        return {
            "success": False,
            "error": "Approval must be True or False."
        }

    if not OUTBOX_FILE.exists():
        return {
            "success": False,
            "error": "No pending emails exist."
        }

    records = json.loads(
        OUTBOX_FILE.read_text(encoding="utf-8")
    )

    for record in records:
        if record["approval_id"] == approval_id:

            if record["status"] != "PENDING":
                return {
                    "success": False,
                    "error": "This approval has already been processed."
                }

            if approved:
                record["status"] = "SENT_SIMULATED"
                message = "Email approved and saved in the simulated outbox."
            else:
                record["status"] = "REJECTED"
                message = "Email rejected. Nothing was sent."

            OUTBOX_FILE.write_text(
                json.dumps(records, indent=2),
                encoding="utf-8"
            )

            return {
                "success": True,
                "status": record["status"],
                "message": message
            }

    return {
        "success": False,
        "error": "Approval ID not found."
    }

TOOL_SPECS = [
    {
        "name": "search_course_materials",
        "description": "Search course documents and return citations.",
        "parameters": {
            "question": "string"
        }
    },
    {
        "name": "list_assignments",
        "description": "List available sample assignments and deadlines.",
        "parameters": {}
    },
    {
        "name": "draft_email",
        "description": "Prepare an email without sending it.",
        "parameters": {
            "recipient": "string",
            "subject": "string",
            "message": "string"
        }
    }
]
