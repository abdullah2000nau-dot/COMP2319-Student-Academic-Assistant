from src.memory import search_documents

question = "What are the required components of the AI assistant project?"

result = search_documents(question)

if result["success"]:
    print("\nSEARCH RESULTS\n")

    for item in result["results"]:
        print("Source:", item["source"])
        print("Similarity:", round(item["similarity"], 3))
        print("Text:", item["text"])
        print("-" * 60)
else:
    print("Search failed:", result["error"])
