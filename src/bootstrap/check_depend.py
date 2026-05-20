def check_depend():
    required = {
        "discord": "discord.py",
        "asyncio": "asyncio",
        "yaml": "PyYAML",
        "groq": "groq",
        "google": "google-genai",
        "openai": "openai",
        "mistral": "mistral",
        "mistral_lib": "mistral-lib",
    }

    missing = []

    for module, pip_name in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(pip_name)

    return len(missing) == 0,missing