# # ai_model.py
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# import streamlit as st
# # Load environment variables from .env file
# load_dotenv()

# # --- Configure the Gemini API ---
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     raise ValueError("🔴 Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    
# genai.configure(api_key=api_key)

# def generate_flowchart_steps(topic: str, num_steps: int) -> str:
#     """
#     Generates flowchart steps using the Gemini model.

#     Args:
#         topic (str): The subject of the flowchart.
#         num_steps (int): The number of steps to generate.

#     Returns:
#         str: A string with each step formatted as 'Title : Description', separated by newlines.
#     """
#     # Create a Gemini model instance
#     # Note: 'gemini-2.0-flash' is not a valid model name as of late 2023. 
#     # Using 'gemini-pro' which is standard. Change if you have access to a new model.
#     # model = genai.GenerativeModel('gemini-3-flash-preview')
#     from google.generativeai.types import HarmCategory, HarmBlockThreshold

#     model = genai.GenerativeModel(
#     "gemini-3-flash-preview",
#     safety_settings={
#         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#         #HarmCategory.HARM_CATEGORY_SEXUAL_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#     }
# )

#     # --- Precise Prompt Engineering ---
#     prompt = f"""
#     You are an expert at creating clear and concise process flowcharts.
#     Your task is to generate {num_steps} steps for the topic: "{topic}".

#     **Instructions**:
#     1.  Provide exactly {num_steps} steps.
#     2.  For each step, provide a short, clear title and a brief description.
#     3.  You **MUST** follow this format for each line: `Title : Description`
#     4.  Do **NOT** add any introductory text, concluding remarks, markdown formatting (like ```), or numbered lists. Your entire output should only consist of the `Title : Description` lines.

#     **Example for topic "Making a cup of tea" with 4 steps**:
#     Boil Water : Heat water in a kettle until it reaches a rolling boil.
#     Steep Tea : Place a tea bag in a mug and pour the boiling water over it.
#     Infuse : Allow the tea to steep for 3-5 minutes to develop its flavor.
#     Serve : Remove the tea bag and add milk or sugar as desired.

#     Now, generate the steps for the topic: "{topic}".
#     """

#     try:
#         # # Generate the content
#         # response = model.generate_content(prompt)
        
#         # # Clean up the response text just in case
#         # cleaned_text = response.text.strip()
#         # return cleaned_text
        
#         response = model.generate_content(prompt)
#         if response.candidates:
#             content = response.candidates[0].content.parts
#             if content:
#                 st.write(content[0].text)
#             else:
#                 st.warning("No text returned by the model.")
#         else:
#             st.warning("Model did not return any candidates.")



#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return f"Error : Could not generate content from AI model. Details: {e}"


# ai_model.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API Key not found. Set GOOGLE_API_KEY in environment variables.")

genai.configure(api_key=api_key)

# Create model ONCE (best practice)
model = genai.GenerativeModel(
    "gemini-3-flash-preview",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)

def generate_flowchart_steps(topic: str, num_steps: int) -> str:
    """
    Generates flowchart steps using Gemini.

    Returns:
        str: Flowchart steps OR error message
    """

    prompt = f"""
You are an expert at creating clear and concise process flowcharts.

Generate exactly {num_steps} steps for the topic "{topic}".

Rules:
- Exactly {num_steps} lines
- Format strictly: Title : Description
- No numbering
- No markdown
- No extra text

Example:
Boil Water : Heat water in a kettle until boiling.
Steep Tea : Pour hot water over the tea bag.
Infuse : Let the tea rest for 3 to 5 minutes.
Serve : Remove tea bag and serve hot.
"""

    try:
        response = model.generate_content(prompt)

        output_text = ""

        if response.candidates:
            candidate = response.candidates[0]

            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, "text") and part.text:
                        output_text += part.text

        if not output_text.strip():
            return "Error: Gemini returned no text for this prompt."

        return output_text.strip()

    except Exception as e:
        return f"Error : Could not generate content from AI model. Details: {e}"
