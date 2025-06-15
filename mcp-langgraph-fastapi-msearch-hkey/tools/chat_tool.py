from openai import OpenAI

# import os
# from dotenv import load_dotenv
# load_dotenv(dotenv_path="../.env")

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_completion(content: str, api_key: str) -> str:
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.9,
        messages=[{"role": "user", "content": content}])
    return response.choices[0].message.content.strip()


# print(chat_completion("넌 누구야?"))

# print(chat_completion("대한민국의 21대 대통령 이름?"))