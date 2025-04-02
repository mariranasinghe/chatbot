import json
import os
from difflib import get_close_matches
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables for Generative AI API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini AI model configuration
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp-01-21",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=(
        "You will cater to Algoma University students, you will be a virtual assistant and customer service chatbot "
        "for only university students. Helping them answer their university questions in the comfort of their home. "
        "Your task is to help university students, in a minimalistic manner, focus only on academics. You can use "
        "informative sentences. You will associate with 19+ year students. Sound interesting."
    ),
)

chat_session = model.start_chat(history=[])

# json file functions
def knowledge_base_load(file_path: str) -> dict:
    #Load knowledge base from a json file
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def knowledge_base_save(file_path: str, data: dict):
    # Save knowledge base to a JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    #Find the best match for user input in the questions list
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    #Retrieve an answer for a specific question from the knowledge base
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

# Main chatbot function
def chat_bot():
    # Load knowledge base from json file
    knowledge_base_file = 'knowledge_base.json'
    knowledge_base: dict = knowledge_base_load(knowledge_base_file)

    print("Bot: Hello, how can I help you?")
    
    while True:
        user_input: str = input('You: ').strip()

        if user_input.lower() == 'exit':
            print('Bot: Okay. Let me know if you need help with anything else AlgomaU. Have a productive day!')
            break

        # Checks the knowledge base for an answer
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            #Switch to Gemini AI if no match is found
            response = chat_session.send_message(user_input)
            model_response = response.text

            print(f'Bot: {model_response}')
            
            # Allow the user to update the json file (temporary)
            teach_bot = input("Would you like to teach me this answer? (yes/no): ").strip().lower()
            if teach_bot == 'yes':
                new_answer = input("Please provide the answer: ").strip()
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                knowledge_base_save(knowledge_base_file, knowledge_base)
                print("Bot: Thank you! I learned a new response!")

if __name__ == '__main__':
    chat_bot()
