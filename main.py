import google.generativeai as genai
import discord
from discord.ext import commands
import yaml
import json
import os

#tải lịch sử chat
def load_history():
    if os.path.exists("history.json"):
        with open("history.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return {}
#lưu lịch sử chat
def save_history(history):
    with open("history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
#load con phíc
with open('ChatbotConfig.yml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
################################################################
TOKEN = config['Token']
Gemini_Api_Key = config['Gemini_api_key']
# nếu không muốn load config và token trong file riêng thì
# Token = "nhập token bot"
# Gemini_Api_Key = "nhập api"
# xoá cái load config đi là xong
intents = discord.Intents.all()
app = commands.Bot(command_prefix='@', intents=intents)
chat_history = load_history()


@app.event
async def on_ready():
    print('Bot đã chạy')


@app.event
async def on_message(message):
    if message.author == app.user:
        return
    content = message.content
    print(f'User Name: {message.author.name}, User ID: {message.author.id}, Message: {message.content}')

    if f'<@{app.user.id}>' in content:
        api_key = Gemini_Api_Key
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        with open('system_instruction.yml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        system_instruction = data['Data']['system_instruction']

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
            system_instruction=system_instruction,
        )

        question = content.replace(f'<@{app.user.id}>', '').strip()
        user_id = str(message.author.id)

        history = chat_history.get(user_id, [])
        chat_session = model.start_chat(history=history)

        response = chat_session.send_message(f"Người hỏi -> {message.author.name} | Câu hỏi ->  *{question}*")
        model_response = response.text

        if len(model_response) > 2000:
            parts = [model_response[i:i + 2000] for i in range(0, len(model_response), 2000)]
            for part in parts:
                await message.channel.send(f"{part}")
        else:
            await message.channel.send(f"<@{message.author.id}> {model_response}") # send tin nhan


        history.append({"role": "user", "parts": [question]})
        history.append({"role": "model", "parts": [model_response]})
        chat_history[user_id] = history
        save_history(chat_history)

    await app.process_commands(message)


app.run(TOKEN)
#code by kenftr
