from src.tools import (
    submit_email_for_approval,
    approve_email
)

print("\nTEST 1: Submit email for approval")

result = submit_email_for_approval(
    "instructor@example.edu",
    "Assignment Question",
    "Dear Instructor, I need clarification about the assignment."
)

print(result)

assert result["success"] is True
assert result["status"] == "PENDING_APPROVAL"

approval_id = result["approval_id"]

print("\nTEST 2: Reject an email")

rejection = approve_email(approval_id, False)
print(rejection)

assert rejection["success"] is True
assert rejection["status"] == "REJECTED"

print("\nTEST 3: Try to approve the rejected email again")

second_attempt = approve_email(approval_id, True)
print(second_attempt)

assert second_attempt["success"] is False

print("\nALL HUMAN APPROVAL TESTS PASSED")
