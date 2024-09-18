import streamlit as st
from toolhouse import Toolhouse
from anthropic import Anthropic

anthropic_key = st.secrets["ANTHROPIC_KEY"]

th = Toolhouse(provider="anthropic", access_token="0482bdd8-c424-47a3-92fa-01ef24772616")
client = Anthropic(api_key=anthropic_key)

def llm_call(messages: list[dict]):
  return client.messages.create(
    model="claude-3-5-sonnet-20240620",
    system="You are the worlds leading authority on Events in New York City. List your findings in a table format and populate the following columns if the information exists on the page for each event: Event Title, Event Date, Event Time, Event Location, Event Link. List the events in the chronological order found on the page contents. Respond with only the data requested, do not preface or end your responses with any added verbiage.",
    max_tokens=500,
    messages=messages,
    tools=th.get_tools(),
  )

messages = [
  {"role": "user", "content": "Get the events for the next 30 days from the content of https://lu.ma/nyc. List all the upcoming events and the content for those events in a table. Don't add anything."},
]

response = llm_call(messages)
messages += th.run_tools(response, append=True)
final_response = llm_call(messages)
st.write(final_response.content[0].text)



