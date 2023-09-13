import requests
from dotenv import load_dotenv
import os
import requests
import json
from utils import MarvelConfig
import json

load_dotenv()


class Marvel:
    def make_get_request(self, character):
        # get details of the character and saves to file
        marvel_config_object = MarvelConfig()
        params = {
            "apikey": marvel_config_object.public_key,
            "ts": marvel_config_object.ts,
            "hash": marvel_config_object.hash,
            "limit": 100,
            "name": {character},
        }
        file_path = "./character_data.json"

        try:
            response = requests.get(
                marvel_config_object.base_url,
                params=params,
                headers=marvel_config_object.headers,
            )

            if response.status_code == 200:
                data = response.json()
                result = data["data"]["results"][0]

                with open(file_path, "w") as json_file:
                    json.dump({"character_data": result}, json_file)

                return result
            else:
                print(f"Request failed with status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_description(self):
        # get character "description" from the file
        with open("character_data.json", "r") as json_file:
            data = json.load(json_file)
        try:
            character_data = data["character_data"]["description"]
            return character_data
        except FileNotFoundError:
            print("Error: File not found.")
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON data from the file.")

    def get_details(self, variable):
        # get character "details": series, comics, stories, events"
        with open("character_data.json", "r") as json_file:
            data = json.load(json_file)

        try:
            character_data = data["character_data"][variable]["items"]
            text = ""
            for key in character_data:
                name = key["name"]
                text += f"{variable}: {name}, "
            return text
        except FileNotFoundError:
            print("Error: File not found.")
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON data from the file.")
