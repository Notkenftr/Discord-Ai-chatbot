import json
import random
import aiohttp
from src.config import MainConfig

model_config = (MainConfig().get_config_data()
                    .get("Models", {})
                    .get("model_config",{}))

async def gemini(system_prompt_content,
                        prompt):
    from google import genai
    from google.genai import types

    this_model_config = (MainConfig().get_config_data()
                        .get("Models",{})
                        .get("service",{})
                        .get("gemini",{}))

    client = genai.Client(
        api_key=random.choice(
            this_model_config.get("api_key",[])
        )
    )

    config = types.GenerateContentConfig(
        system_instruction=system_prompt_content,
        temperature=model_config.get("temperature",0.7),
        top_k=model_config.get("top_k",40),
        top_p=model_config.get("top_p",0.95),
        max_output_tokens=model_config.get("max_output_tokens",8192),

    )

    response = client.models.generate_content(
        model=this_model_config["model"],
        contents=prompt,
        config=config
    )

    return response.text.__str__()

async def groq(system_prompt_content, prompt):
    from groq import AsyncGroq

    this_model_config = (MainConfig().get_config_data()
                        .get("Models", {})
                        .get("service", {})
                        .get("groq", {}))

    client = AsyncGroq(
        api_key=random.choice(
            this_model_config.get("api_key", [])
        )
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt_content
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = await client.chat.completions.create(
        model=this_model_config["model"],
        messages=messages,
        temperature=model_config.get("temperature", 0.7),
        top_p=model_config.get("top_p", 0.95),
        max_tokens=model_config.get("max_output_tokens", 8192),
    )

    return response.choices[0].message.content.__str__()

async def openai(system_prompt_content, prompt):
    from openai import AsyncOpenAI

    this_model_config = (MainConfig().get_config_data()
                        .get("Models", {})
                        .get("service", {})
                        .get("openai", {}))

    client = AsyncOpenAI(
        api_key=random.choice(
            this_model_config.get("api_key", [])
        )
    )

    messages = [
        {"role": "system", "content": system_prompt_content},
        {"role": "user", "content": prompt}
    ]

    response = await client.chat.completions.create(
        model=this_model_config["model"],
        messages=messages,
        temperature=model_config.get("temperature", 0.7),
        top_p=model_config.get("top_p", 0.95),
        max_tokens=model_config.get("max_output_tokens", 1024*2),
    )

    return response.choices[0].message.content.__str__()

async def mistral(system_prompt_content, prompt):
    from mistralai.client import Mistral
    this_model_config = (MainConfig().get_config_data()
                        .get("Models", {})
                        .get("service", {})
                        .get("mistral", {}))
    client = Mistral(
        api_key=random.choice(
            this_model_config.get("api_key", [])
        )
    )

    messages = [
        {"role": "system", "content": system_prompt_content},
        {"role": "user", "content": prompt}
    ]

    response = await client.chat.complete_async(
        model=this_model_config["model"],
        messages=messages,
        temperature=model_config.get("temperature", 0.7),
        top_p=model_config.get("top_p", 0.95),
        max_tokens=model_config.get("max_output_tokens", 8192),
    )

    return response.choices[0].message.content.__str__()


async def localhost(system_prompt_content, prompt, previous_bot_response=""):
    def format_payload(payload_template, mapping):

        if isinstance(payload_template, dict):
            return {k: format_payload(v, mapping) for k, v in payload_template.items()}
        elif isinstance(payload_template, list):
            return [format_payload(v, mapping) for v in payload_template]
        elif isinstance(payload_template, str):
            return payload_template.format(**mapping)
        return payload_template


    this_model_config = (MainConfig().get_config_data()
                         .get("Models", {})
                         .get("service", {})
                         .get("localhost", {}))

    if not this_model_config.get("enable", False):
        raise RuntimeError("Localhost service is disabled.")

    selected_model = random.choice(this_model_config.get("model", ["llama3"]))
    api_url = this_model_config.get("api", "").format(model=selected_model)

    mapping_data = {
        "model": selected_model,
        "system_prompt": system_prompt_content,
        "user_prompt": prompt,
        "previous_bot_response": previous_bot_response,
        "top_p": str(model_config.get("top_p", 0.9)),
        "top_k": str(model_config.get("top_k", 50)),
        "temperature": str(model_config.get("temperature", 0.5))
    }

    requests_template = this_model_config.get("requests")

    if not requests_template:
        raise ValueError("Missing 'requests' template configuration for localhost.")

    if isinstance(requests_template, str):
        requests_template = json.loads(requests_template)

    payload = format_payload(requests_template, mapping_data)

    timeout = aiohttp.ClientTimeout(total=60.0)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(api_url, json=payload) as response:
            response.raise_for_status()

            result = await response.json()
            return str(result["choices"][0]["message"]["content"])