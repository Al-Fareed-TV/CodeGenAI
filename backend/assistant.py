from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)
assistant_id = os.getenv("assistant_id")
assistant = None
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
            rahulshettyacademy
           </i>
          </b>
          and Password is
          <b>
           <i>
            learning
           </i>
          </b>
          )
         </p>
        </div>
       </form>
      </div>
     </div>
    </div>
   </div>
  </div>
  <div class="modal fade" id="myModal">
   <div class="modal-dialog modal-confirm">
    <div class="modal-content">
     <div class="modal-body">
      <p>
       You will be limited to only fewer functionalities of the app. Proceed?
      </p>
     </div>
     <div class="modal-footer justify-content-center">
      <button class="btn btn-secondary" data-dismiss="modal" id="cancelBtn" type="button">
       Cancel
      </button>
      <button autofocus="" class="btn btn-success" id="okayBtn" type="button">
       Okay
      </button>
     </div>
    </div>
   </div>
  </div>
 </body>
</html>
"""

# --------------------------------------------------------------
# Create assistant
# --------------------------------------------------------------
def create_assistant():
    global assistant  # Make the assistant variable global
    assistant = client.beta.assistants.create(
        name="Automation code Generator",
        instructions="You're an Automation expert who knows to write automation script in different languages and tools.\
            Help me to write Automation code in Java using Selenium tool.Remember to cover all the edge cases. \
            Assume that user has created webdriver and wants only test cases that covers all the edge cases,  \
            also look for assertions if possible like assertion on page title placeholder of the input element or label.\
            Also look for every element in provided whether they are present or not. html code is provided below.\
             Generate test case on this. Also generate code which is reusable following Page object model and reusability. \
             Generate only test cases not other than that. if you are generating response with full context it will be rejected and not accepted. \
            Provide only test cases with no import statement and no beforeClass and afterClass method. \
            While generating test cases segregate different test cases don't give in one single response. Create '''different responses'''    \
        ",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview",
    )
    return assistant

assistant = create_assistant()


# --------------------------------------------------------------
# Thread management
# --------------------------------------------------------------


# --------------------------------------------------------------
# Generate response
# --------------------------------------------------------------
def generate_response(message_body, name):
    # If a thread doesn't exist, create one and store it
    print(f"Creating new thread for {name} with wa_id")
    thread = client.beta.threads.create()
    thread_id = thread.id

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread)
    return new_message


# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(thread):
    # Retrieve the Assistant

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        print(run.status)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    print(f"Generated message: {new_message}")
    return new_message


# --------------------------------------------------------------
# Test assistant
# --------------------------------------------------------------

new_message = generate_response(code,"Junior Vagrants")
print(new_message)