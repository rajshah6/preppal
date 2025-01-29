import React, { useState, useRef, useEffect, createContext, useContext } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import { useNavigate, useLocation } from 'react-router-dom';
import LoadingSpinner from './LoadingSpinner'; // Import LoadingSpinner

const PracticeQuestion = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { questions } = location.state || {};
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(questions ? questions[0] : 'Tell me about a time when you faced a challenging technical problem while working with SQL to design or optimize a database. How did you approach solving it, and what was the outcome?');
  const videoRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
    previewStream,
  } = useReactMediaRecorder({ audio: true, video: true });

  useEffect(() => {
    if (videoRef.current && previewStream) {
      videoRef.current.srcObject = previewStream;
    }
  }, [previewStream]);

  useEffect(() => {
    if (status === 'stopped' && videoRef.current) {
      const stream = videoRef.current.srcObject;
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
        videoRef.current.srcObject = null;
      }
    }
  }, [status]);

  const handleSubmit = async () => {
    if (mediaBlobUrl && currentQuestion) {
      setIsLoading(true); // Show loading spinner
      try {
        const blob = await fetch(mediaBlobUrl).then(r => r.blob());
        const answer = new File([blob], 'answer.webm', { type: 'video/webm' });
        const formData = new FormData();
        formData.append('answer', answer);
        formData.append('question', currentQuestion);
        formData.append('questions[]', JSON.stringify(questions));

        const response = await fetch('/api/submit-answer', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error('Error submitting response:', errorData.error || 'An error occurred.');
          setIsLoading(false); // Hide loading spinner
          return;
        }

        const data = await response.json();
        console.log('Response submitted:', data);
        navigate('/feedback', { state: { feedback: data.feedback } });
      } catch (error) {
        console.error('Error submitting response:', error);
      } finally {
        setIsLoading(false); // Hide loading spinner
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-purple-900 to-gray-900 text-white flex items-center justify-center">
      {isLoading && <LoadingSpinner />}
      <div className="relative bg-gray-900 p-10 rounded-3xl shadow-2xl max-w-xl w-full">
        <div className="absolute inset-0 opacity-60 blur-lg rounded-3xl"></div>
        <div className="relative z-10">
          <h1 className="text-4xl font-extrabold text-center mb-8 text-indigo-400">Practice Question</h1>

          <div className="bg-gray-800 p-6 rounded-xl mb-8">
            <p className="text-xl text-gray-300">{currentQuestion}</p>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-300 mb-4">Your Answer</h2>
            {status === 'recording' && (
              <video ref={videoRef} className="w-full mb-4 rounded-xl" autoPlay muted />
            )}
            {status === 'stopped' && mediaBlobUrl && (
              <div className="mb-4">
                <h3 className="text-lg text-gray-300 mb-2">Playback</h3>
                <video src={mediaBlobUrl} className="w-full rounded-xl" controls />
              </div>
            )}
          </div>

          <div className="space-y-3">
            {status !== 'recording' ? (
              <button
                onClick={startRecording}
                className="w-full py-3 bg-violet-400 hover:from-indigo-400 hover:to-purple-500 text-white font-bold text-lg rounded-lg shadow-lg focus:outline-none focus:ring-4 focus:ring-purple-450 transition-all duration-300"
              >
                Start Recording
              </button>
            ) : (
              <button
                onClick={stopRecording}
                className="w-full py-3 bg-gradient-to-r from-red-500 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold text-lg rounded-lg shadow-lg focus:outline-none focus:ring-4 focus:ring-red-400 transition-all duration-300"
              >
                Stop Recording
              </button>
            )}
            {status === 'stopped' && mediaBlobUrl && (
              <button
                onClick={handleSubmit}
                className="w-full py-3 bg-indigo-800 hover:from-indigo-400 hover:to-purple-500 text-white font-bold text-lg rounded-lg shadow-lg focus:outline-none focus:ring-4 focus:ring-purple-450 transition-all duration-300"
              >
                Submit Answer
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PracticeQuestion;