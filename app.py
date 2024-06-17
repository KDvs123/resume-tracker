import streamlit as st
import pandas as pd
import base64,random
import time,datetime
#libraries to parse the resume pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import pafy #for uploading youtube videos
import plotly.express as px #to create visualisations at the admin session
import nltk
nltk.download('stopwords')

def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title

def get_table_download_link(df,filename,text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in: dataframe
    out: href string
    """
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode() # some strings <-> bytes conversions necessary here
# href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'