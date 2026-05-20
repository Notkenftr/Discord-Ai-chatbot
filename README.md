#### B1 Create a Bot

* Visit: [Discord Developer Portal](https://discord.com/developers/applications?utm_source=chatgpt.com)
* Click the **New Application** button in the top-right corner
* Enter any name you want

#### B2 Get the Bot Token

* Go to the **Bot** section (left sidebar)
* Click **Reset Token**
* Enter your password
* Copy the token
* Open `./configs/main.yml`
* Paste the token there

#### B3 Create an API Key for the AI Model

* If you use Gemini:

  * Visit: [Google AI Studio](https://aistudio.google.com/prompts/new_chat?utm_source=chatgpt.com)
  * In the left sidebar, click **Get API key**
  * Create a new API key and copy it
  * Open the `Chatbotconfig.yml` file
  * Paste the API key into:

```yaml
gemini:
  model: "gemini-3.5-flash"
  api_key:
    - "YOUR_API_KEY"
  enable: true
```

* If you use Groq:

  * Visit: [Groq Console](https://console.groq.com/keys?utm_source=chatgpt.com)
  * Create an API key and paste it into:

```yaml
groq:
  model: "openai/gpt-oss-120b"
  api_key:
    - "YOUR_API_KEY"
  enable: true
```

* If you use OpenAI:

  * Visit: [OpenAI Platform](https://platform.openai.com/api-keys?utm_source=chatgpt.com)
  * Create an API key and paste it into:

```yaml
openai:
  model: "gpt-5.5"
  api_key:
    - "YOUR_API_KEY"
  enable: true
```

* If you use Mistral:

  * Visit: [Mistral Console](https://console.mistral.ai/api-keys?utm_source=chatgpt.com)
  * Create an API key and paste it into:

```yaml
mistral:
  model: "mistral-medium-3-5"
  api_key:
    - "YOUR_API_KEY"
  enable: true
```

#### B4 Edit the System Prompt

The system prompt controls how the bot responds.

Open:

```text
./configs/system_prompt.yml
```

There, you can customize it however you want. Example:

```text
You are a Discord bot that communicates in Vietnamese. Your task is to answer users' questions.
```

#### B5 Install and Run the Bot

The bot is designed to automatically install the required libraries.
You only need to run the `start.py` file.

However, if the dependencies are not installed automatically, you can run:

```bash
pip install -r requirements.txt
```
