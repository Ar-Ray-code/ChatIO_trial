import openai

class ChatGPT:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_text(self, prompt, length=1000):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        return result