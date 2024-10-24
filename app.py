# Import necessary libraries
from transformers import pipeline
import streamlit as st

# Load a text generation model (which can be used for generating health suggestions)
suggestion_model = pipeline("text-generation", model="gpt2", max_length=50)

# A simple function to suggest reasons for common health queries
def get_health_reason(query):
    # Predefined responses for specific common symptoms (rule-based approach)
    predefined_responses = {
        "headache": "A headache can be caused by stress, dehydration, eye strain, or lack of sleep. It may also indicate migraines or sinus infections.",
        "fever": "Fever is often a sign of infections such as the flu or a cold. It may also indicate inflammation or other health issues.",
        "stomach pain": "Stomach pain can be caused by indigestion, gas, infections, or ulcers. Persistent pain should be checked by a doctor.",
        "fatigue": "Fatigue may result from lack of sleep, poor nutrition, or dehydration, and can also indicate conditions like anemia or thyroid issues."
    }
    
    # Normalize the query to improve matching
    query_normalized = query.lower().strip()
    
    # Check if the query matches a predefined illness
    if query_normalized in predefined_responses:
        return predefined_responses[query_normalized]
    
    # Use regex to check for common typos and return corrected query
    corrected_query = correct_typos(query_normalized)
    if corrected_query in predefined_responses:
        return predefined_responses[corrected_query]
    
    # Generate a response for less common queries
    else:
        generated_text = suggestion_model(f"Possible causes of {query_normalized}:")[0]["generated_text"]
        return generated_text.strip()

def correct_typos(query):
    # Simple typo correction logic for common queries
    corrections = {
        "fiver": "fever",
        "hedache": "headache",
        "stomack pain": "stomach pain",
        "fatique": "fatigue"
    }
    return corrections.get(query, query)

# Create the Streamlit app layout
st.title("Health Query Suggestion App")

# Input box for health query
query = st.text_input("Health Query:")

# Button to submit the query
if st.button("Submit"):
    if query:
        response = get_health_reason(query)  # Get the response
        st.text_area("Suggested Reason:", response)  # Display the response
    else:
        st.warning("Please enter a health query.")
