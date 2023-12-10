from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time
load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)
assistants_id = os.getenv("assistant_id")

# --------------------------------------------------------------
# Get the code
# --------------------------------------------------------------
code = """
<!DOCTYPE html>
<html>
<head>
  <title>
    LoginPage Practise | Rahul Shetty Academy
  </title>
  <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" id="bootstrap-css" rel="stylesheet"/>
</head>
<body>
  <a class="blinkingText" href="https://rahulshettyacademy.com/documents-request" target="_blank">
    Free Access to InterviewQues/ResumeAssistance/Material
  </a>
  <div id="login">
    <h3 class="text-center pt-5">
      <span class="icon-circled">
        <svg class="bi bi-lock" fill="currentColor" height="2em" viewbox="0 0 16 16" width="2em" xmlns="http://www.w3.org/2000/svg">
          <path d="M11.5 8h-7a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h7a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1zm-7-1a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h7a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7zm0-3a3.5 3.5 0 1 1 7 0v3h-1V4a2.5 2.5 0 0 0-5 0v3h-1V4z" fill-rule="evenodd">
          </path>
        </svg>
      </span>
    </h3>
    <br/>
    <div class="container">
      <div class="row justify-content-center align-items-center" id="login-row">
        <div class="col-md-6" id="login-column">
          <div class="col-md-12" id="login-box">
            <form action="" class="form" id="login-form" method="post" name="loginForm">
              <div class="alert alert-danger col-md-12" style="display: none">
                <strong>
                  Incorrect
                </strong>
                username/password.
              </div>
              <div class="form-group">
                <label class="text-white" for="username">
                  Username:
                </label>
                <br/>
                <input class="form-control" id="username" name="username" type="text"/>
              </div>
              <div class="form-group">
                <label class="text-white" for="password">
                  Password:
                </label>
                <br/>
                <input class="form-control" id="password" name="password" type="password"/>
              </div>
              <div class="form-group">
                <div class="form-check-inline">
                  <label class="customradio">
                    <span class="radiotextsty">
                      Admin
                    </span>
                    <input checked="checked" id="usertype" name="radio" type="radio" value="admin"/>
                    <span class="checkmark">
                    </span>
                  </label>
                  <label class="customradio">
                    <span class="radiotextsty">
                      User
                    </span>
                    <input id="usertype" name="radio" type="radio" value="user"/>
                    <span class="checkmark">
                    </span>
                  </label>
                </div>
              </div>
              <div class="form-group">
                <select class="form-control" data-style="btn-info">
                  <option value="stud">
                    Student
                  </option>
                  <option value="teach">
                    Teacher
                  </option>
                  <option value="consult">
                    Consultant
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label class="text-info" for="terms">
                  <span>
                    <input id="terms" name="terms" type="checkbox">
                    </input>
                  </span>
                  <span class="text-white termsText">
                    I Agree to the
                    <a href="#">
                      terms and conditions
                    </a>
                  </span>
                </label>
                <br/>
                <input class="btn btn-info btn-md" id="signInBtn" name="signin" type="submit" value="Sign In"/>
              </div>
              <div class="form-group">
                <p class="text-center text-white">
                  (username is
                  <b>
                    <i>
                      rahulshettyaca
"""

# --------------------------------------------------------------
# Create or Retrieve assistant
# --------------------------------------------------------------
def create_or_retrieve_assistant():
    assistant = None
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
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )
        print(f"Created new assistant with id: {assistant.id}")
    return assistant

assistant = create_or_retrieve_assistant()

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
def generate_response(message_body, wa_id, name):
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        print(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread
