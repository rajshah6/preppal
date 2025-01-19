import os
import requests
import cohere
from dotenv import load_dotenv
import PyPDF2

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_resume):
    resume_text = ""
    with open(pdf_resume, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            resume_text += page.extract_text()  # Extract text from each page
    return resume_text

# Load environment variables from .env file
load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
COHERE_API_URL = "https://api.cohere.ai/v1/generate"

# Initialize a Cohere client
co = cohere.Client(COHERE_API_KEY)


def generate_questions(resume_text, position, num_questions):
        prompt = (
        f"Analyze the following resume text and generate {num_questions} behavioral interview questions "
        f"for a {position} position based on the candidate's experience.\n\n{resume_text}"
        f"\n\nPlease format your response so that each question starts on a new line."
        f"\nEnsure that exactly {num_questions} questions are generated."
        f"\nDo not include any filler text other than the questions."
        )

        response = co.generate(
        model="command-r-plus-08-2024",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        k=0,
        p=1,
        stop_sequences=["--"],
        return_likelihoods='NONE'
        )

        questions = response.generations[0].text.strip().split('\n')
        # Clean and format questions
        questions = [q.strip('- ').strip() for q in questions if q.strip()]
        # Ensure the number of questions matches num_questions
        questions = questions[:num_questions]

        print(questions)
        return questions