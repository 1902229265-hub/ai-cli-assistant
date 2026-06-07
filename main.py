import requests
import json
import os

MODEL_NAME = "deepseek-r1:14b"
API_URL = "http://localhost:11434/api/chat"
HISTORY_FILE = "chat_history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=2)


def ask_ai(messages):
    response = requests.post(
        API_URL,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        }
    )

    result = response.json()
    return result["message"]["content"]


def main():
    messages = load_history()

    print("========== 本地 AI 聊天助手 2.0 ==========")
    print("输入 exit 退出")
    print("输入 clear 清空聊天记录")
    print("=========================================")

    while True:
        question = input("\n你：")

        if question.lower() == "exit":
            print("已退出")
            break

        if question.lower() == "clear":
            messages = []
            save_history(messages)
            print("聊天记录已清空")
            continue

        messages.append({
            "role": "user",
            "content": question
        })

        answer = ask_ai(messages)

        print("\nAI：")
        print(answer)

        messages.append({
            "role": "assistant",
            "content": answer
        })

        save_history(messages)


if __name__ == "__main__":
    main()