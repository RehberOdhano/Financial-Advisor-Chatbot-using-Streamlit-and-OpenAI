import streamlit as st
from openai import OpenAI
import jsonify

# Set your OpenAI API key
API_KEY = "openai api key"


def get_response(user_question, chat_history):
    client = OpenAI(api_key=API_KEY)
    client.api_key = API_KEY

    try:
        prompt = open("./prompt_rules.txt", "r", encoding="UTF-8").read()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": f"Give me the output for \n {user_question, chat_history}",
                },
            ],
            temperature=0.2,
            max_tokens=1500,
        )

        res = response.choices[0].message.content

        json_res = res
        if "```" in res:
            res = res.split("```")
            json_res = res[1]

        return json_res.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    """
    Main function to create the Streamlit app for the chatbot interface.
    """

    st.set_page_config(page_title="Chatbot", page_icon="🤖")
    st.title("OpenAI Chatbot")

    # Session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        st.text(f"{message['sender']}: {message['content']}")

    # User input
    user_query = st.text_input("Type your message here...")
    if user_query:
        st.session_state.chat_history.append({"sender": "Human", "content": user_query})

        # Get response from OpenAI using custom template
        response = get_response(user_query, st.session_state.chat_history)

        # Display AI response
        st.write(f"AI: {response}")
        st.session_state.chat_history.append({"sender": "AI", "content": response})


if __name__ == "__main__":
    main()
