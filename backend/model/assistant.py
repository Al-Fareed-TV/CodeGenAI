from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os,sys
import time
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)
assistants_id = os.getenv("assistant_id")
sys.path.append("/Users/testvagrant/Documents/junior-vagrants/backend/")
from scrapper.HTMLScraper import HTMLScraper
# --------------------------------------------------------------
# Get the code
# --------------------------------------------------------------
code = "<!DOCTYPE html>\n<html>\n<head>\n  <title>\n    LoginPage Practise | Rahul Shetty Academy\n  </title>\n  <link href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css\" id=\"bootstrap-css\" rel=\"stylesheet\"/>\n</head>\n<body>\n  <a class=\"blinkingText\" href=\"https://rahulshettyacademy.com/documents-request\" target=\"_blank\">\n    Free Access to InterviewQues/ResumeAssistance/Material\n  </a>\n  <div id=\"login\">\n    <h3 class=\"text-center pt-5\">\n      <span class=\"icon-circled\">\n        <svg class=\"bi bi-lock\" fill=\"currentColor\" height=\"2em\" viewbox=\"0 0 16 16\" width=\"2em\" xmlns=\"http://www.w3.org/2000/svg\">\n          <path d=\"M11.5 8h-7a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h7a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1zm-7-1a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h7a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7zm0-3a3.5 3.5 0 1 1 7 0v3h-1V4a2.5 2.5 0 0 0-5 0v3h-1V4z\" fill-rule=\"evenodd\">\n          </path>\n        </svg>\n      </span>\n    </h3>\n    <br/>\n    <div class=\"container\">\n      <div class=\"row justify-content-center align-items-center\" id=\"login-row\">\n        <div class=\"col-md-6\" id=\"login-column\">\n          <div class=\"col-md-12\" id=\"login-box\">\n            <form action=\"\" class=\"form\" id=\"login-form\" method=\"post\" name=\"loginForm\">\n              <div class=\"alert alert-danger col-md-12\" style=\"display: none\">\n                <strong>\n                  Incorrect\n                </strong>\n                username/password.\n              </div>\n              <div class=\"form-group\">\n                <label class=\"text-white\" for=\"username\">\n                  Username:\n                </label>\n                <br/>\n                <input class=\"form-control\" id=\"username\" name=\"username\" type=\"text\"/>\n              </div>\n              <div class=\"form-group\">\n                <label class=\"text-white\" for=\"password\">\n                  Password:\n                </label>\n                <br/>\n                <input class=\"form-control\" id=\"password\" name=\"password\" type=\"password\"/>\n              </div>\n              <div class=\"form-group\">\n                <div class=\"form-check-inline\">\n                  <label class=\"customradio\">\n                    <span class=\"radiotextsty\">\n                      Admin\n                    </span>\n                    <input checked=\"checked\" id=\"usertype\" name=\"radio\" type=\"radio\" value=\"admin\"/>\n                    <span class=\"checkmark\">\n                    </span>\n                  </label>\n                  <label class=\"customradio\">\n                    <span class=\"radiotextsty\">\n                      User\n                    </span>\n                    <input id=\"usertype\" name=\"radio\" type=\"radio\" value=\"user\"/>\n                    <span class=\"checkmark\">\n                    </span>\n                  </label>\n                </div>\n              </div>\n              <div class=\"form-group\">\n                <select class=\"form-control\" data-style=\"btn-info\">\n                  <option value=\"stud\">\n                    Student\n                  </option>\n                  <option value=\"teach\">\n                    Teacher\n                  </option>\n                  <option value=\"consult\">\n                    Consultant\n                  </option>\n                </select>\n              </div>\n              <div class=\"form-group\">\n                <label class=\"text-info\" for=\"terms\">\n                  <span>\n                    <input id=\"terms\" name=\"terms\" type=\"checkbox\">\n                    </input>\n                  </span>\n                  <span class=\"text-white termsText\">\n                    I Agree to the\n                    <a href=\"#\">\n                      terms and conditions\n                    </a>\n                  </span>\n                </label>\n                <br/>\n                <input class=\"btn btn-info btn-md\" id=\"signInBtn\" name=\"signin\" type=\"submit\" value=\"Sign In\"/>\n              </div>\n              <div class=\"form-group\">\n                <p class=\"text-center text-white\">\n                  (username is\n                  <b>\n                    <i>\n                      rahulshettyaca"

# --------------------------------------------------------------
# Create assistant
# --------------------------------------------------------------
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

assistant = create_assistant()


# --------------------------------------------------------------
# Thread management
# --------------------------------------------------------------
def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)


def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id


# --------------------------------------------------------------
# Generate response
# --------------------------------------------------------------
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
        new_message = run_assistant(thread)
        print(f"To:", new_message)
        return new_message


# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(thread):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(assistants_id)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistants_id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    print(f"Generated message: {new_message}")
    return new_message


# --------------------------------------------------------------
# Test assistant
# --------------------------------------------------------------

new_message = generate_response(code, assistants_id, "Junior Vagrants")
print(new_message)