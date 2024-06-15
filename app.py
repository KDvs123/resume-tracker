# Field to put my JD
# Upload PDF
# Convert the PDF To image ---> processing ----> google gemini pro
# Prompts Template [Multiple prompts]


from dotenv import load_dotenv

# Load the environment variables from the .env file into the program

load_dotenv()
import base64
import io
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
    if uploaded_file is not None:
    # Convert the PDF into images, one per page
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes

        img_byte_arr=io.BytesIO() # Create a BytesIO object to hold the image bytes
        first_page.save(img_byte_arr,format='JPEG') # Save the image as a JPEG into the BytesIO object
        img_byte_arr=img_byte_arr.getvalue() # Get the byte value of the image

        pdf_parts =[
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode() # Encode the image bytes to base64 and decode to a string
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("JoB Description: ",key="input")
uploaded_file = st.file_uploader("Upload your Resume PDF", type=["pdf"], key="file_up")

if uploaded_file is not None:
    st.write("PDF Uploaded succeesfully")

submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced HR With Tech Experience in the field of any one job role from Data Science or Full stack , Web Development , Big Data Enginnering, Software Enginnering Intern, DEVOPS,Data Analyst, CyberSecurity your task is to review the provided resume against the job description for these profiles. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""


input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role Data Science,Full stack, Web Development , Big Data Enginnering, Software Enginnering Intern, DEVOPS,Data Analyst, CyberSecurity and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload a pdf File")

elif submit3:
     if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
     else:
        st.write("Please Upload a pdf File")
