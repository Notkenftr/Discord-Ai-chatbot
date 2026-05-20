import re
import os.path
import asyncio
from src.config import MainConfig
from src.handler import model_response

class ResponseHandler:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.config = MainConfig().get_config_data()
        self.unfilter_response = None
        self.filter_response = None

    def _filter_response(self,response):
        filter_config = (MainConfig().get_config_data()
                         .get("filter", {}))

        if filter_config.get("enable") is False:
            return response
        response_filter = response
        if filter_config.get("mention_blacklist", {}).get("user"):
            mention_pattern = r"<@!?\d+>"
            response_filter = re.sub(mention_pattern, "``@user_mention``", response_filter)

        if filter_config.get("mention_blacklist", {}).get("role"):
            role_pattern = r"<@&\d+>"
            response_filter = re.sub(role_pattern, "``@role_mention``", response_filter)

        if filter_config.get("mention_blacklist", {}).get("everyone"):
            response_filter = re.sub(r"@everyone", "``@everyone``", response_filter)

        if filter_config.get("mention_blacklist", {}).get("here"):
            response_filter = re.sub(r"@here", "``@here``", response_filter)

        blacklist_words = filter_config.get("content_blacklist", [])

        if blacklist_words:
            blacklist_words = sorted(blacklist_words, key=len, reverse=True)

            pattern = r"\b(" + "|".join(re.escape(word) for word in blacklist_words) + r")\b"

            response_filter = re.sub(pattern, "``***``", response_filter, flags=re.IGNORECASE)

        return response_filter

    async def handler(self):

        services_dict = self.config.get("Models", {}).get("service", {})

        enabled_models = [
            model_name
            for model_name, model_info in services_dict.items()
            if model_info.get("enable") is True
        ]
        if enabled_models == None:
            raise ValueError("No model enabled")

        use_model = enabled_models[0]

        with open(os.path.join(MainConfig().get_root(),"configs","system_prompt.txt"), 'r', encoding='utf-8') as f:

            system_prompt_content = f.read()

        model_func = getattr(model_response, use_model)
        self.unfilter_response = await model_func(system_prompt_content,self.prompt)
        self.filter_response = self._filter_response(self.unfilter_response)

    def get_response(self, filter=True):
        if filter:
            return self.filter_response
        else:
            return self.unfilter_response

