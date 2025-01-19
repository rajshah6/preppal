from openai import OpenAI
import openai
from pydub import AudioSegment
from textblob import TextBlob
import re
import os
import tempfile
from dotenv import load_dotenv
from google.cloud import speech_v1p1beta1 as speech
import cv2

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "aksb-448207-44ea7e884b32.json"

# Initialize Google Cloud Speech client
google_speech_client = speech.SpeechClient()

# Function to convert video file (mp4) to audio file (mp3)
def convert_video_to_audio(video_path):
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio = AudioSegment.from_file(video_path, format="webm")
    audio.export(temp_audio_file.name, format="mp3")
    return temp_audio_file.name

# Function to transcribe audio using OpenAI's speech-to-text API
def transcribe_audio(audio_path):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_path, "rb")
    )
    return transcription.text

# Function to transcribe audio using Google Cloud Speech-to-Text API and get confidence scores
def transcribe_audio_with_confidence(audio_path):
    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()

    # Read the audio file
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    # Configure the audio recognition
    audio = speech.RecognitionAudio(content=content)
    config = {
        "encoding": "MP3",  # Use the actual encoding format of your audio
        "sample_rate_hertz": 44100,  # Match the audio file's sample rate
        "language_code": "en-US",
    }

    # Transcribe the audio
    response = client.recognize(config=config, audio=audio)

    # Get the confidence scores
    average_confidence = sum(result.alternatives[0].confidence for result in response.results) / len(response.results)
    return average_confidence


# Function to perform sentiment analysis
def perform_sentiment_analysis(text):
    prompt = f"""
    Analyze the following response and classify its tone using only ONE word. 
    This word must be clear, concise, and match the overall tone of the response. 
    Do NOT provide any explanation, punctuation, or additional words. 
    Your response must be strictly one of the following categories: professional, casual, academic, or creative.

    Response: "{text}"

    Output the one word that best fits the tone:
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a tone classifier that responds with exactly one word."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,  # Use deterministic output
    )
    
    tone = response.choices[0].message.content.strip()      
    return tone # Fallback to casual if invalid tone
      


# Function to detect filler words
def detect_filler_words(text):
    filler_words = ["um", "uh", "like", "you know", "basically", "actually"]
    filler_counts = {word: len(re.findall(f"\\b{word}\\b", text, re.IGNORECASE)) for word in filler_words}
    return filler_counts

# Function to calculate response length in seconds
def calculate_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path, format="mp3")
    return audio.duration_seconds

# Function to calculate total words in transcript
def count_words(text):
    return len(re.findall(r'\w+', text))

# Normalize dBFS to a 0-100 scale (assuming -60 dBFS is silence and 0 dBFS is max volume)
def normalize_loudness(dBFS, min_dBFS=-60, max_dBFS=0):
    normalized_loudness = max(0, 100 * (dBFS - min_dBFS) / (max_dBFS - min_dBFS))
    return normalized_loudness

# Load pre-trained models for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


# Load pre-trained models for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def track_eye_contact(video_path):
    cap = cv2.VideoCapture(video_path)
    eye_contact_frames = 0
    total_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            # Detect eyes within the face
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) >= 2:  # Assuming eye contact when two eyes are detected
                eye_contact_frames += 1

    cap.release()
    cv2.destroyAllWindows()

    # Calculate eye contact percentage
    eye_contact_percentage = (eye_contact_frames / total_frames) if total_frames > 0 else 0
    return eye_contact_percentage

def calculate_average_sentence_length(transcript):
    # Split transcript into sentences
    sentences = re.split(r'[.!?]', transcript)
    sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty sentences and extra spaces

    # Calculate word count for each sentence
    sentence_lengths = [len(re.findall(r'\w+', sentence)) for sentence in sentences]

    # Calculate average sentence length
    if sentence_lengths:
        average_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
    else:
        average_sentence_length = 0

    return average_sentence_length


# Function to provide feedback based on filler words and response length
def provide_feedback(filler_counts, audio_duration, transcript, audio_path, video_path, eye_contact_percentage, avg_sentence_length):
    total_words = count_words(transcript)
    total_filler_words = sum(filler_counts.values())
    filler_percentage = (total_filler_words / total_words) * 100 if total_words > 0 else 0
    wpm = total_words / audio_duration if audio_duration > 0 else 0

    audio = AudioSegment.from_file(audio_path, format="mp3")
    loudness = audio.dBFS
    average_loudness = normalize_loudness(loudness)

    feedback = []

    # Filler words feedback
    if filler_percentage > 5:
        feedback.append(f"Try to reduce filler words, they comprise {filler_percentage:.2f}% of your speech. We suggest aiming for < 5%.")

    # Response length feedback
    if audio_duration < 30:
        feedback.append(f"Your answer could be more detailed, it was {audio_duration:.2f} seconds. Aim for 30-90 seconds.")
        
    if audio_duration > 90:
        feedback.append(f"Your answer may be a tad excessive, it was {audio_duration:.2f} seconds. Aim for 30-90 seconds.")

    # Word per minute feedback
    if wpm < 110:
        feedback.append(f"Your speaking rate is a bit slow, it was {wpm:.2f} words per minute (wpm). aim for around 110-150 wpm.")

    if wpm > 150:
        feedback.append(f"Your speaking rate is a bit fast, it was {wpm:.2f} words per minute (wpm). aim for around 110-150 wpm.")

    if loudness < 60:
        feedback.append(f"Your audio is a bit quiet, it was aim {average_loudness:.2f} dB on average. Aim for 60-80 dB on average.")

    if loudness > 80:
        feedback.append(f"Your audio is a bit loud, it was aim {average_loudness:.2f} dB on average. Aim for 60-80 dB on average.")

    if eye_contact_percentage < 80:
        feedback.append(f"Your eye contact could be improved, you were making eye contact {eye_contact_percentage:.2f}% of the time. Aim for 80%+.")

    if avg_sentence_length < 10:
        feedback.append(f"Your sentences are too short, they were {avg_sentence_length:.2f} words on average. Try elaborating and adding more detail.")
    
    if avg_sentence_length > 20:
        feedback.append(f"Your sentences are too long, they were {avg_sentence_length:.2f} words on average. Try breaking them up for clarity.")

    return feedback

def evaluate_response(question, transcript):
    prompt = f"""
    Here is the interview question and my response:

    **Question**: {question}
    **Response**: {transcript}

    Evaluate my response based on how well I answered the first question.
    - If I did not adequately answer the first question, provide one bullet point that explains which part of the question I addressed and how I could have elaborated to improve my response.
    - If I did adequately answer the first question, provide one bullet point that highlights a specific thing I did well in addressing the question.
    """
    
    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an evaluator that provides detailed feedback for interview responses."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the feedback using attributes
    feedback = response.choices[0].message.content
    return feedback

# Main Function
def process_user_video(questions, video_path):
    for question in questions:
        print("Converting video to audio...")
        audio_path = convert_video_to_audio(video_path)

        print("Transcribing audio using OpenAI...")
        transcript = transcribe_audio(audio_path)

        # Get average confidence score using Google Cloud Speech-to-Text
        print("Getting average confidence score from Google Cloud Speech-to-Text...")
        average_confidence = (transcribe_audio_with_confidence(audio_path))
        formatted_avg_confidence = round(average_confidence * 100, 2)

        print("Performing sentiment analysis...")
        sentiment = perform_sentiment_analysis(transcript)

        print ("Calculating average sentence length...")
        avg_sentence_length = round(calculate_average_sentence_length(transcript), 2)

        print("Detecting filler words...")
        filler_counts = detect_filler_words(transcript)

        print("Calculating response duration...")
        audio_duration = calculate_audio_duration(audio_path)

        print("Calculating eye contact percentage...")
        eye_contact_percentage = round(track_eye_contact(video_path) * 100, 2)

        print("Providing feedback...")
        feedback1 = provide_feedback(filler_counts, audio_duration, transcript, audio_path, video_path, eye_contact_percentage, avg_sentence_length)
        feedback2 = evaluate_response(question, transcript)

        prompt = f"""
                Please evaluate my response to the question and provide an overall grade based on the detailed feedback below. 
                Assign a score strictly from the range 1 to 100, where:
                - 1 is the lowest score up to 100 for highest score. 
                - The score should reflect how well the response addressed the question, the clarity, tone, and other relevant criteria.

                Feedback provided: {[feedback2] + feedback1}

                **Output only the grade** (e.g., 1, 50, 63, 90). Do not include any explanation or additional text.
                """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an evaluator that assigns a letter grade based solely on the feedback provided."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # For consistent and deterministic output
        )

        overall_score = response.choices[0].message.content.strip()
        print("overall_score:", overall_score)
        
        return {
            "transcript": transcript,
            "sentiment": sentiment,
            "filler_counts": filler_counts,
            "audio_duration": audio_duration,
            "eye_contact_percentage": eye_contact_percentage,
            "average_confidence": formatted_avg_confidence, 
            "avg_sentence_length": avg_sentence_length,
            "feedback": [feedback2],
            "overall_score": overall_score}

