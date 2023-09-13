from dotenv import load_dotenv
import streamlit as st
from utils import AzureModel
from streamlit_option_menu import option_menu
import json
from backend import Marvel
from character_prompt import CharacterPrompt


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask anything")
    st.header("Ask your idols whatever you like:")
    with open("./all_characters.json", "r") as json_file:
        data = json.load(json_file)

    lt = data["character"]
    with st.sidebar:
        selected = option_menu(
            "Talk to:",
            lt,
            menu_icon="cast",
            default_index=1,
        )

    marvel_object = Marvel()
    image_url = None

    if selected:
        with st.spinner("Fetching image..."):
            response_data = marvel_object.make_get_request(selected)
            if response_data:
                image_data = response_data["thumbnail"]["path"]
                image_format = response_data["thumbnail"]["extension"]
                image_url = f"{image_data}.{image_format}"

        if image_url:
            st.image(image_url, caption=selected)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input(f"ask anything:"):
            with st.chat_message("user"):
                st.markdown(prompt)

            st.session_state.messages.append({"role": "user", "content": prompt})
            character_obj = CharacterPrompt()
            # series, comics, stories, events
            series = marvel_object.get_details("series")
            comics = marvel_object.get_details("comics")
            stories = marvel_object.get_details("stories")
            events = marvel_object.get_details("events")
            parsed_response = character_obj.get_response_from_llm(
                "marvel", selected, prompt, series, comics, stories, events
            )
            with st.chat_message("assistant"):
                st.markdown(parsed_response["answer"])

            st.session_state.messages.append(
                {"role": "assistant", "content": parsed_response["answer"]}
            )


if __name__ == "__main__":
    main()
