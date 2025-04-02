import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 65536,
  "response_mime_type": "text/plain",
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]




model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-thinking-exp-01-21",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="You will cater to Algoma University students, you will be a virtual assistant and customer service chatbot for only university students. Helping them answer their university question in the comfort of their home. Your task is to help university students, in a minimalistic manner, focus only on academics. You can use informative sentences. You will associate with 19 + year students. Sound interesting.",
)

chat_session = model.start_chat(
    history=[]
)

print("Bot: Hello, how can I help you?")
print()

while True:

    user_input = input("You: ")
    print()

    response = chat_session.send_message(user_input)

    model_response = response.text

    if user_input.strip().lower() == 'exit':
      print(f'Bot: {model_response}')
      break
    else:
      print(f'Bot: {model_response}')
      print()

    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})


    #.\venv\Scripts\activate
    # python chat.py