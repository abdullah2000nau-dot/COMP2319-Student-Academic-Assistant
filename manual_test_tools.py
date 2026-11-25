from src.tools import (
    search_course_materials,
    list_assignments,
    draft_email
)

print("\nTEST 1: Search course materials")
result = search_course_materials(
    "What are the required project components?"
)
print(result)

assert result["success"] is True
assert len(result["citations"]) > 0

print("\nTEST 2: List assignments")
result = list_assignments()
print(result)

assert result["success"] is True
assert len(result["assignments"]) > 0

print("\nTEST 3: Draft an email")
result = draft_email(
    "instructor@example.edu",
    "Question about assignment",
    "Dear Instructor, I have a question about the assignment."
)
print(result)

assert result["success"] is True
assert result["status"] == "DRAFT_ONLY"

print("\nALL THREE TOOL TESTS PASSED")
