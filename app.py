# Field to put my JD
# Upload PDF

from dotenv import load_dotenv

# Load the environment variables from the .env file into the program

load_dotenv()

import streamlit as st
import os # Import the os module for interacting with the operating system
import google.generativeai as genai
import PyPDF2 as pdf
import json



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')  # Create an instance of the Gemini generative model
    response=model.generate_content(input)   # Generate content using the model with the input, PDF content, and a prompt
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

# Function to parse and aggregate responses
def aggregate_responses(response):
    try:
        result = json.loads(response)
        return {
            "JD Match": f"{result['JD Match']}%",
            "MissingKeywords": result.get("MissingKeywords", []),
            "Profile Summary": result.get("Profile Summary", "")
        }
    except Exception as e:
        return {"Error": str(e)}

## prompt template

# Generalized prompt template for the generative model
input_prompt_template = """
Hey, act like a skilled and very experienced ATS (Applicant Tracking System) with a deep understanding of various job roles across different industries. Your task is to evaluate the resume based on the given job description. 
You must consider that the job market is very competitive and you should provide the best assistance for improving the resumes. Assign the percentage matching based on the job description and the missing keywords with high accuracy.

Ensure the output is consistent and in the exact format specified below every time you generate it. Minimize randomness in your evaluation and focus on accuracy.

resume: {resume_text}
description: {job_description}

I want the response in one single string having the structure:
{{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}
"""


## Streamlit App
# Initialize session state
session_state = st.session_state.setdefault("response", {})

st.title("Resume Tracking System")
st.text("Improve Your Resume")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt_template.format(resume_text=resume_text, job_description=jd)
        
        # Check if response is already stored in session state
        if 'response' not in session_state or session_state.response == "":
            # Generate response and store it in session state
            session_state.response = get_gemini_response(input_prompt)
            session_state.aggregated_response = aggregate_responses(session_state.response)
            
        # Display the stored response
        st.subheader("Response")
        st.write(session_state.aggregated_response)

    else:
        st.write("Please upload a PDF file")