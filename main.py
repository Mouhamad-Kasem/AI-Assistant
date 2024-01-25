from openai import OpenAI
import os
from time import sleep

client = OpenAI(api_key=os.environ['secret'])

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions=
    "You are a personal math tutor. Write and run code to answer math questions.",
    model="gpt-3.5-turbo-1106",
    tools=[{
        "type": "retrieval"
    }])

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?")

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

# Check if the Run requires action (function call)
while True:
  run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                 run_id=run.id)
  print(f"Run status: {run_status.status}")
  if run_status.status == 'completed':
    break
  sleep(1)  # Wait for a second before checking again

messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)

