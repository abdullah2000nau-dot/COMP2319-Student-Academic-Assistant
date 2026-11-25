import json
from src.tools import OUTBOX_FILE, approve_email

def main():
    if not OUTBOX_FILE.exists():
        print("No approval requests found.")
        return

    try:
        records = json.loads(
            OUTBOX_FILE.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError):
        print("Could not read the approval file.")
        return

    pending = [
        item for item in records
        if item.get("status") == "PENDING"
    ]

    if not pending:
        print("There are no pending approval requests.")
        return

    print("\nSAAI - HUMAN APPROVAL SCREEN")
    print("=" * 40)

    for item in pending:
        print(f'\nApproval ID: {item["approval_id"]}')
        print(f'Recipient: {item["recipient"]}')
        print(f'Subject: {item["subject"]}')
        print("\nEmail message:")
        print(item["message"])
        print("-" * 40)

    approval_id = input(
        "\nEnter the approval ID you want to review: "
    ).strip()

    selected = next(
        (item for item in pending
         if item["approval_id"] == approval_id),
        None
    )

    if selected is None:
        print("Invalid approval ID. No action taken.")
        return

    print("\nSelected email:")
    print(f'To: {selected["recipient"]}')
    print(f'Subject: {selected["subject"]}')
    print(selected["message"])

    decision = input(
        "\nType APPROVE or REJECT (anything else cancels): "
    ).strip().upper()

    if decision == "APPROVE":
        result = approve_email(approval_id, True)
    elif decision == "REJECT":
        result = approve_email(approval_id, False)
    else:
        print("Cancelled. No action taken.")
        return

    print("\nApproval result:")
    print(result)

    if result.get("status") == "SENT_SIMULATED":
        print("\nNote: This is a simulated approval. No real email was sent.")

if __name__ == "__main__":
    main()
