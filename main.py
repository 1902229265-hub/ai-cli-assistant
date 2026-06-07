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
        if question.lower() == "help":
            print("""
可用命令：

help              显示帮助
clear             清空聊天记录
files             查看当前目录文件
read 文件名        总结指定 txt 文件
exit              退出程序
""")
            continue

        if question.lower() == "files":
            print("\n当前目录文件：")
            for file in os.listdir():
                print("-", file)
            continue
        if question.lower().startswith("read "):
            print("DEBUG:进入read模式")
            file_name = question[5:].strip()

            if not os.path.exists(file_name):
             print("文件不存在")
             continue

            with open(file_name, "r", encoding="utf-8") as file:
             file_content = file.read()

            question = f"请总结下面这个文件的内容：\n\n{file_content}"
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
            continue


if __name__ == "__main__":
    main()