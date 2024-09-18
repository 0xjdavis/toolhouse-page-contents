import streamlit as st
from toolhouse import Toolhouse
from anthropic import Anthropic

anthropic_key = st.secrets["ANTHROPIC_KEY"]

th = Toolhouse(provider="anthropic", access_token="0482bdd8-c424-47a3-92fa-01ef24772616")
client = Anthropic(api_key=anthropic_key)

def llm_call(messages: list[dict]):
  return client.messages.create(
    model="claude-3-5-sonnet-20240620",
    # system="You are the worlds leading authority on Events in New York City. List your findings in a table format and populate the following columns if the information exists on the page for each event: Event Title, Event Date, Event Time, Event Location, Event Link. List the events in the chronological order found on the page contents. Respond with only the data requested, do not preface or end your responses with any added verbiage.",
    system="You are the world's leading authority on events in {{City}}. You know the best event websites like {{Website}} like the back of your hand. You know where all the best parties, shows, music, art, sports and dating hotspots are. You know what is trending and you love to share recommendations to create meaningful experiences for people. Your specialty is creating great date night itineraries for new connections.",
    max_tokens=500,
    messages=messages,
    tools=th.get_tools(),
  )

messages = [
  #{"role": "user", "content": "Get the events for the next 30 days from the content of https://lu.ma/nyc. List all the upcoming events and the content for those events in a table. Don't add anything."},
  {"role": "user", "content": "Today is {{Date}}. Create a calendar of real events in New York City for the next 30 days. Be sure to list the events in chronological order. The format for the calendar should be a table with the event title, event date, event time, and event location. Do not fabricate any data."},
]

response = llm_call(messages)
messages += th.run_tools(response, append=True)
final_response = llm_call(messages)
st.write(final_response.content[0].text)



