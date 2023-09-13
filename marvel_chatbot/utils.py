from langchain.chat_models import AzureChatOpenAI
from dotenv import load_dotenv
import os
import hashlib

load_dotenv()


class AzureModel:
    def __init__(self):
        os.environ["OPENAI_API_TYPE"] = "azure"
        os.environ["OPENAI_API_VERSION"] = "2023-03-15"
        os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

        BASE_URL = os.getenv("OPENAI_API_BASE")
        API_KEY = os.getenv("OPENAI_API_KEY")
        DEPLOYMENT_NAME = "GPT3-5"

    def get_llm_model(self):
        # gives back llm model
        BASE_URL = os.getenv("OPENAI_API_BASE")
        API_KEY = os.getenv("OPENAI_API_KEY")
        DEPLOYMENT_NAME = "GPT3-5"

        llm = AzureChatOpenAI(
            openai_api_base=BASE_URL,
            openai_api_version="2023-05-15",
            deployment_name=DEPLOYMENT_NAME,
            openai_api_key=API_KEY,
            openai_api_type="azure",
        )

        return llm


class MarvelConfig:
    def __init__(self):
        self.base_url = "http://gateway.marvel.com/v1/public/characters?"
        self.public_key = os.getenv("MARVEL_PUBLIC_KEY")
        self.private_key = os.getenv("MARVEL_PRIVATE_KEY")
        self.ts = "1690794299291"
        self.hash_value = self.create_hash()
        self.headers = {"Accept": "*/*"}

    def create_hash(self):
        input_string = f"{self.ts}{self.private_key}{self.public_key}"
        md5_hash = hashlib.md5(input_string.encode()).hexdigest()
        self.hash = md5_hash
