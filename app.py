# Import necessary libraries
from transformers import pipeline
from ipywidgets import widgets
from IPython.display import display

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

# Create input and output boxes using ipywidgets
input_box = widgets.Text(description="Health Query:")
output_box = widgets.Textarea(description="Suggested Reason:")

# Create a submit button
submit_button = widgets.Button(description="Submit")

# Function to handle the user's query submission
def on_submit(button):
    query = input_box.value.lower()  # Get the user's input and make it lowercase
    if query:
        try:
            # Get a predefined or generated response
            response = get_health_reason(query)
            output_box.value = response  # Display the response in the output box
        except Exception as e:
            output_box.value = f"Error: {str(e)}"  # Display any errors that occur
    else:
        output_box.value = "Please enter a health query."

# Bind the button click event to the submit function
submit_button.on_click(on_submit)

# Display the input box, submit button, and output box
display(input_box, submit_button, output_box)
