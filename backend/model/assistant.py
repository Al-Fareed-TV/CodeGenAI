from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time
import sys
sys.path.append("/Users/testvagrant/Documents/junior-vagrants/backend/")
from scrapper.HTMLScraper import HTMLScraper

class Assistant:
    def __init__(self):
        load_dotenv()
        self.OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
        self.client = OpenAI(api_key=self.OPEN_AI_API_KEY)
        self.assistant = None


    def create_assistant(self, language, tool):
        self.assistant = self.client.beta.assistants.create(
            name="Automation code Generator",
            instructions=f"""Generate Automation code in ``` {language} language in {tool} tool ```. Cover all edge cases by assertion and checking for the presence of all elements.
            Assume the user has already created the WebDriver.
            Generate test cases only, focusing on assertions and element presence also performing actions following the Page Object Model.
            Provide code only, no import statements, no beforeClass or afterClass methods.
            Generate responses in code, not scenarios. ```Segregate different test cases into separate methods as different responses```.
            Provide responses in JSON format as mentioned below. 
            ```All the test cases must be segregated into '''one array of json objects, each objects containing description and testCase in format''':
            {{
                "description": "Description of the test case",
                "tesCase": "Test cases that are generated"
            }} and so on```
            """,
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview",
        )
        return self.assistant


    def check_if_thread_exists(self, wa_id):
        with shelve.open("threads_db") as threads_shelf:
            return threads_shelf.get(wa_id, None)

    def store_thread(self, wa_id, thread_id):
        with shelve.open("threads_db", writeback=True) as threads_shelf:
            threads_shelf[wa_id] = thread_id

    
    def generate_response(self,url):
        scrapper = HTMLScraper()
        htmlCode = scrapper.remove_css_js_and_save_html(url)
        # If a thread doesn't exist, create one and store it
        print(f"Creating new thread")
        thread = self.client.beta.threads.create()
        thread_id = thread.id

        # Add message to thread
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=htmlCode,
        )

        # Run the assistant and get the new message
        new_message = self.run_assistant(thread)
        return new_message

    def run_assistant(self, thread):
        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
        )

        # Wait for completion
        while run.status != "completed":
            # Be nice to the API
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Retrieve the Messages
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        new_message = messages.data[0].content[0].text.value
        return new_message

# https://rahulshettyacademy.com/loginpagePractise/