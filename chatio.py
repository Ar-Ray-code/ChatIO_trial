import time
# from restuino import Restuino, GPIOMode
from chatgpt import ChatGPT
from speech_recognizer import SpeechRecognizer
import os

def cut_text(text, keyword_begin, keyword_end) -> str:
    # 文字列の中からキーワードを探す
    begin = text.find(keyword_begin)
    end = text.find(keyword_end)
    # キーワードの前後の文字列を切り出す
    trimed_txt = text[begin + len(keyword_begin):end]
    # split using space
    # return trimed_txt.split()
    return trimed_txt


# 音声認識器を初期化する
recognizer = SpeechRecognizer("base")

# Restuinoを初期化する
restuino = "http://192.168.0.177/gpio5"
# チャットボットを初期化する
os_env = os.environ.get("OPENAI_API_KEY")
if os_env is None:
    print("OPENAI_API_KEY is not set")
    exit(1)

chatbot = ChatGPT(os_env)
# 1st conversation from openai_text.txt
with open("openai_text.txt", "r") as f:
    prompt_base = f.read()

# response = chatbot.generate_text(prompt_base)
# print("chatbot: " + response)
print("------------------- begin -------------------")


while True:
    # 音声を認識する
    prompt = recognizer.recognize()
    print("whisper: " + prompt)
    # GPI is not found
    if prompt.find("GP") == -1:
        continue

    # チャットボットに対してテキストを生成する
    response = chatbot.generate_text(prompt_base + prompt)
    print("chatbot: " + response)
    # RestuinoのGPIO 2をHIGHに設定する
    # if not found in <text> </text> then skip
    if response.find("<text>") == -1:
        continue

    print("vvvvvvvv")
    curl_txt = cut_text(response, "<text>", "</text>")
    print ("^^^^^^^")
    print(curl_txt)
    os.system(curl_txt)
    time.sleep(1)
