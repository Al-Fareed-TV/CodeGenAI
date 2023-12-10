from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time

load_dotenv()

OPEN_AI_API_KEY = "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"
client = OpenAI(api_key=OPEN_AI_API_KEY)
assistants_id = os.getenv("assistant_id")

# ...

# Create or Retrieve assistant
def create_or_retrieve_assistant():
    global assistant
    if assistants_id:
        try:
            assistant = client.beta.assistants.retrieve(assistants_id)
            print(f"Using existing assistant with id: {assistants_id}")
        except Exception as e:
            print(f"Error retrieving existing assistant: {e}")
    if assistant is None:
        assistant = client.beta.assistants.create(
            name="Automation code Generator",
            instructions="Write Java Selenium test cases covering edge cases, assertions on page elements, and ensure reusability with the Page Object Model for provided HTML.``` Separate responses for different test cases by creating test case method without additional context, import statements, or before/after class methods. for the below html code assuming that web driver has already been created```",
            tools=[{"type": "code_interpreter"},{"type":"retrieval"}],
            model="gpt-4-1106-preview",
        )
        print(f"Created new assistant with id: {assistant.id}")
    return assistant

assistant = create_or_retrieve_assistant()

# ...

# Generate response
def generate_response(message_body, wa_id, name):
    global assistant
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        print(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread

    # ...

# Run assistant
def run_assistant(thread):
    global assistant
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(assistant)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # ...

# ...

# Test assistant
new_message = generate_response(code, assistants_id, "Junior Vagrants")
print(new_message)
