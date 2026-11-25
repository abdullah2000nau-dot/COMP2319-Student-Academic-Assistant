import json
from pathlib import Path

from openai import OpenAI

from src.tools import (
    search_course_materials,
    list_assignments,
    draft_email,
    submit_email_for_approval,
    approve_email
)

from src.guardrails import check_input, check_output

ROOT = Path(__file__).resolve().parent.parent

MODEL = "qwen2.5:7b"
MAX_TURNS = 5
MAX_CONTEXT_MESSAGES = 10
MAX_MESSAGE_CHARS = 3000
MAX_CONTEXT_TOKENS = 6000


def estimate_tokens(messages):
    """Estimate tokens using approximately 4 characters per token."""
    total_chars = sum(
        len(str(message.get('content', '')))
        for message in messages
    )
    return total_chars // 4


def trim_context(messages):
    """Keep system instructions and recent messages within the token budget."""
    system_message = messages[0]
    recent_messages = messages[1:]

    while recent_messages and estimate_tokens(
        [system_message] + recent_messages
    ) > MAX_CONTEXT_TOKENS:
        recent_messages.pop(0)

    return [system_message] + recent_messages

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

SOUL_FILE = ROOT / "SOUL.md"
SYSTEM_PROMPT = SOUL_FILE.read_text(encoding="utf-8")

conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


def get_tool_result(name, arguments):
    """Run an approved tool and report errors safely."""

    try:
        if name == "search_course_materials":
            return search_course_materials(
                arguments.get("question", "")
            )

        if name == "list_assignments":
            return list_assignments()

        if name == "draft_email":
            return draft_email(
                arguments.get("recipient", ""),
                arguments.get("subject", ""),
                arguments.get("message", "")
            )

        if name == "submit_email_for_approval":
            return submit_email_for_approval(
                arguments.get("recipient", ""),
                arguments.get("subject", ""),
                arguments.get("message", "")
            )

        return {
            "success": False,
            "error": "Unknown tool requested."
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Tool failed: {type(error).__name__}"
        }


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_course_materials",
            "description": "Search academic documents and return citations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"}
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_assignments",
            "description": "List available assignments and deadlines.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "draft_email",
            "description": "Draft an email without sending it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "subject": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["recipient", "subject", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "submit_email_for_approval",
            "description": "Submit an email for human approval. Does not send it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "subject": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["recipient", "subject", "message"]
            }
        }
    }
]


def ask_agent(user_message):
    """Run one bounded agent turn with input and output safety checks."""

    global conversation

    allowed, reason = check_input(user_message)

    if not allowed:
        return "SAFETY BLOCK: " + reason

    if len(user_message) > MAX_MESSAGE_CHARS:
        return "Your message is too long. Please shorten it."

    conversation.append({
        "role": "user",
        "content": user_message
    })

    conversation = (
        [conversation[0]]
        + conversation[-MAX_CONTEXT_MESSAGES:]
    )
    conversation = trim_context(conversation)

    try:
        for turn in range(MAX_TURNS):

            response = client.chat.completions.create(
                model=MODEL,
                messages=conversation,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0
            )

            message = response.choices[0].message

            if message.tool_calls:
                conversation.append(message)

                for tool_call in message.tool_calls:
                    name = tool_call.function.name

                    try:
                        arguments = json.loads(
                            tool_call.function.arguments
                        )
                    except (ValueError, TypeError):
                        arguments = {}

                    result = get_tool_result(name, arguments)

                    if name == "submit_email_for_approval":
                        if result.get("success"):
                            print(
                                "\nHUMAN APPROVAL REQUIRED"
                                "\nApproval ID:",
                                result["approval_id"]
                            )
                            print(
                                "The email is pending. "
                                "It has NOT been sent."
                            )

                    conversation.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })

                continue

            answer = message.content or "I could not generate an answer."

            safe, checked_answer = check_output(answer)

            if not safe:
                return "SAFETY BLOCK: " + checked_answer

            conversation.append({
                "role": "assistant",
                "content": checked_answer
            })

            return checked_answer

        return "Maximum agent turns reached. Please try a simpler question."

    except Exception as error:
        return (
            "The assistant encountered an error: "
            + type(error).__name__
        )


def main():
    print("\nSAAI - Student Academic Assistant AI")
    print("Local model:", MODEL)
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("SAAI: Goodbye!")
            break

        print("\nSAAI:", ask_agent(question), "\n")


if __name__ == "__main__":
    main()
