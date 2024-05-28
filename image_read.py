import ollama
import io
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import json
import re
load_dotenv()


SYSTEM_PROMPT = """
You are a professional timetable and schedule analyzer. 
Analyse the provided image carefully and only find out any schedule with their respective date. Make sure the the details you find make sense and are correct.
Focus only on the schedules that have a date and a title. Match the titles with their dates, if a title does not have a date or vice versa, then ignore that one.
Before outputting JSON response, carefully check everything.
Output should be a json response containing the title, its respective date with day and date, and the date converted to Datetime object with only Year-Month-Day. Three different lists named, Title, Date and Formatted_Date should be output in JSON.
Example:
{
    "Title" : [],
    "Date" : [],
    "Formatted_Date" : []
}
CONSTRAINT: Dont write anything other than JSON response. Dont put any quotes or other words in the output except the JSON. Make sure the arrays are of same length
"""

# SYSTEM_PROMPT = """You are a professional exam timetable analyzer. Analyze the provided image carefully and extract any exam titles along with their respective dates. Focus solely on identifying the exam titles and their corresponding dates. If a title does not have a date or vice versa, ignore that entry. Double-check all the information before generating the JSON response.
# The output should be a JSON response containing three lists:

# "Title" list: Exam titles
# "Date" list: Corresponding dates in the format "DD Month YYYY" (e.g., "10 May 2024")
# "Formatted_Date" list: Corresponding dates in the format "YYYY-MM-DD" (e.g., "2024-05-10")

# Match the titles and dates correctly. Before outputting, carefully verify that the lists are aligned correctly.
# Example JSON format:
# {
# "Title": ["Exam Title 1", "Exam Title 2", ...],
# "Date": ["10 May 2024", "12 June 2024", ...],
# "Formatted_Date": ["2024-05-10", "2024-06-12", ...]
# }
# CONSTRAINT: Output only the JSON response. Do not include any additional text or quotes in the output."""


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# import pprint
# for model in genai.list_models():
#     pprint.pprint(model.name)
    
def chat_with_image_gemini(image_path):
    print("Gemini-Vision Working")
    image_path = image_path.replace('\\','/')
    image = Image.open(image_path)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    image_parts = [
      {
        "mime_type": 'image/png',
        "data": image_bytes.read()  
      }
    ]
    
    model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')
    response = model.generate_content(
        [f"{SYSTEM_PROMPT}. This is an exam timetable, first the dates are written on the left and under them in the center, their respective exam title is written.", image_parts[0]]
    )
    output = response.text
    
    pattern = r'{.*}'
    match = re.search(pattern, output, re.DOTALL)
    if match:
        result = match.group(0)
        return json.loads(result)
    else:return "Nothing Could Be Extracted From Image"
    
    

def chat_with_image_llava(image_path):

    image_path = image_path.replace('\\','/')
    with open(image_path, 'rb') as image_file:
        image = io.BytesIO(image_file.read())

    message = {
        'role': 'user',
        'content': f"{SYSTEM_PROMPT}",
        'images': [image] 
    }
    
    print('Reading Image...')
    response = ollama.chat(
        model="llava:latest",  
        messages=[message]
    )
    
    return response['message']['content']

# print(chat_with_image_llava(r'./output_image.jpg'))
# print(chat_with_image_gemini(r'./output_image.jpg'))