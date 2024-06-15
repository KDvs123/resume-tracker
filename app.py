# Field to put my JD
# Upload PDF
# Convert the PDF To image ---> processing ----> google gemini pro
# Prompts Template [Multiple prompts]

from dotenv import load_dotenv

# Load the environment variables from the .env file into the program

load_dotenv()

import streamlit as st
import os # Import the os module for interacting with the operating system
from PIL import Image # Import the Image class from the PIL library for image processing
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')  # Create an instance of the Gemini generative model
    response=model.generate_content(input,pdf_content[0],prompt)   # Generate content using the model with the input, PDF content, and a prompt
    return response.text

def input_pdf_setup(uploaded_file):
    # Convert the PDF into images, one per page
    images = pdf2image.convert_from_bytes(uploaded_file.read())

    first_page=images[0]
