<div align="center">

# PrepPal

</div>

PrepPal is your ultimate AI-powered interview preparation assistant. Whether you're gearing up for technical, behavioral, or industry-specific interviews, PrepPal provides personalized and interactive mock interviews to help you ace the big day.

## Features

- **Interactive Mock Interviews**: Simulates real interview scenarios with dynamic question-and-answer sessions.
- **AI Feedback**: Receive detailed feedback on your responses, including strengths and areas for improvement.
- **Customizable Question Sets**: Focus on technical, behavioural, or domain-specific questions.
- **Progress Tracking**: Monitor your improvement over time with insightful analytics.
- **24/7 Accessibility**: Practice interviews anytime, anywhere.


## Installation

To run PrepPal locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Ajith-Bondili/ai_interview_bot
   ```

2. Navigate to the project directory:
   ```bash
   cd ai_interview_bot
   cd frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open your browser and go to `http://localhost:5173` to use the frontend of PrepPal.

6. Create a flask virtual environment (follow installations in ```requirements.txt```) to run the backend of PrepPal.

7. After installing all modules, run ```python3 app.py``` to initialize the backend and use the app.

## Technologies Used

- **Frontend**: React.js, Tailwind CSS
- **Backend**: Flask, Python
- **Generative AI**: OpenAI API, GCP, Cohere API, OpenCV
- **Database**: SQLite, SQLAlchemy
- **Deployment**: _Coming Soon..._

## Live Demo
This is the Live Demo of our [submission](https://dorahacks.io/buidl/21711) to UofTHacks 12:
armaan add link to full video

## Project Structure

```plaintext
preppal/
├── public/         # Static files
├── src/            # Source code
│   ├── components/ # Reusable UI components
│   ├── pages/      # Application pages
│   ├── utils/      # Utility functions
├── server/         # Backend server code
├── .env.example    # Environment variable template
├── package.json    # Node.js dependencies
└── README.md       # Project documentation
```

## Environment Variables

To run PrepPal, you need to configure the following environment variables in a `.env` file:

```env
OPENAI_API_KEY="your openai_api key"
COHERE_API_KEY="your cohere-api key"
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your forked repository:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

Give PrepPal a try and take your interview preparation to the next level!
