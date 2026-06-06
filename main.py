import requests

while True:
    question = input("你：")

    if question.lower() == "exit":
        print("已退出")
        break

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1:14b",
            "prompt": question,
            "stream": False
        }
    )

    result = response.json()

    print("\nAI：")
    print(result["response"])
    print()