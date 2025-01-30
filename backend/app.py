import logging
from flask import Flask, request, jsonify, send_from_directory
from cohere_api import generate_questions, extract_text_from_pdf
from flask_cors import CORS
from sqlalchemy import create_engine
from models import InterviewSession, Question, User, Response, EvaluationMetrics
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from werkzeug.utils import secure_filename  # Secure file handling
from audio_transcription import process_user_video


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
CORS(app, resources={"/*": {"origins": "*"}})  # Allow requests from React dev server

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATABASE_URL = "sqlite:///ai_interview_bot.db"
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the PrepPal!"}), 200

# Endpoint to process form data and generate questions
@app.route('/api/process-form', methods=['POST'])
def process_form():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        occupation = request.form.get('occupation')
        num_questions = request.form.get('num_questions')

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if not occupation or not num_questions:
            return jsonify({"error": "Missing occupation or number of questions"}), 400

        try:
            num_questions = int(num_questions)
            if not (1 <= num_questions <= 5):
                return jsonify({"error": "Number of questions must be between 1 and 5"}), 400
        except ValueError:
            return jsonify({"error": "Invalid number for questions"}), 400

        # Securely save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(file_path)

       # Create database session
        session = Session()

        try:
            # Create or get user (for demo, create a default user)
            user = session.query(User).first()
            if not user:
                user = User(name="Default User", email="default@example.com")
                session.add(user)
                session.flush()

            # Create interview session
            interview_session = InterviewSession(
                user_id=user.user_id,
                desired_occupation=occupation,
                num_questions=num_questions
            )
            session.add(interview_session)
            session.flush()

            # Generate questions
            resume_text = extract_text_from_pdf(file_path)
            generated_questions = generate_questions(resume_text, occupation, num_questions)

            # Save questions
            for i, q_text in enumerate(generated_questions):
                question = Question(
                    session_id=interview_session.session_id,
                    question_text=q_text,
                    order=i
                )
                session.add(question)

            session.commit()
            return jsonify({"questions": generated_questions}), 200

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error in /api/process-form: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Endpoint to submit answer and process it
@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    try:
        session = Session()
        try:
            # Retrieve form data
            questions = request.form.getlist('questions[]')
            question = request.form.get('question')
            video_answer = request.files.get('answer')

            if not question:
                return jsonify({"error": "Missing question"}), 400

            if not video_answer:
                return jsonify({"error": "No video uploaded"}), 400

            # Save video file
            video_answer_path = os.path.join(UPLOAD_FOLDER, secure_filename(video_answer.filename))
            video_answer.save(video_answer_path)

            # Get question from database
            db_question = session.query(Question).filter_by(question_text=question).first()
            if not db_question:
                return jsonify({"error": "Question not found"}), 404

            # Process video and get results
            results = process_user_video(questions=questions, video_path=video_answer_path)

            # Create Response record
            response = Response(
                question_id=db_question.question_id,
                video_path=video_answer_path,
                transcript=results.get('transcript')
            )
            session.add(response)
            session.flush()  # Get response_id

            # Create EvaluationMetrics record
            metrics = EvaluationMetrics(
                response_id=response.response_id,
                wpm=float(results.get('audio_duration', 0)),
                eye_contact=float(results.get('eye_contact_percentage', 0)),
                filler_words_count=sum(results.get('filler_counts', {}).values()),
                avg_sentence_length=float(results.get('avg_sentence_length', 0)),
                duration=float(results.get('audio_duration', 0))
            )
            session.add(metrics)
            session.commit()

            return jsonify({"feedback": results}), 200

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error in /api/submit-answer: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()