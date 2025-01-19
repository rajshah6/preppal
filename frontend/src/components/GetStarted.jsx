import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import LoadingSpinner from "./LoadingSpinner"; // Import the LoadingSpinner component

const GetStarted = () => {
  const [resume, setResume] = useState(null);
  const [occupation, setOccupation] = useState("");
  const [numQuestions, setNumQuestions] = useState(1);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      setResume(file);
      setError(""); // Clear any file-related errors
    } else {
      setError("Only PDF files are allowed.");
    }
  };

  const validateForm = () => {
    if (!resume) return "Please upload your resume.";
    if (!occupation.trim()) return "Occupation is required.";
    if (numQuestions < 1 || numQuestions > 5)
      return "Number of questions must be between 1 and 5.";
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true); // Show loading spinner

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      setIsLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", resume);
    formData.append("occupation", occupation);
    formData.append("num_questions", numQuestions);

    try {
      const response = await fetch("/api/process-form", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error || "An error occurred.");
        return;
      }

      const data = await response.json();
      navigate("/practice", { state: { questions: data.questions } });
    } catch (err) {
      console.error("Error:", err);
      setError("Failed to submit the form. Please try again.");
    } finally {
      setIsLoading(false); // Hide loading spinner
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-t from-black via-purple-900 to-gray-900 text-white flex items-center justify-center">
      {isLoading && <LoadingSpinner />} {/* Show spinner if loading */}
      <div className="relative bg-gray-900 p-10 rounded-3xl shadow-2xl max-w-lg w-full">
        {/* Glow effect */}
        <div className="absolute inset-0 xopacity-60 blur-lg rounded-3xl"></div>
        <div className="relative z-10">
          <h1 className="text-4xl font-extrabold text-center mb-8 text-indigo-400">
            Get Started
          </h1>
          {error && (
            <p className="text-red-400 text-center font-semibold mb-4">
              {error}
            </p>
          )}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Resume Upload */}
            <div>
              <label
                htmlFor="resume"
                className="block text-lg font-semibold text-gray-200 mb-2"
              >
                Upload Your Resume (PDF Only)
              </label>
              <input
                type="file"
                id="resume"
                accept=".pdf"
                onChange={handleFileChange}
                className="block w-full p-3 text-sm bg-gray-800 text-gray-200 border border-black rounded-lg focus:ring-4 focus:ring-purple-500 focus:outline-none shadow-lg transition-all duration-300"
                required
              />
              {resume && (
                <p className="mt-2 text-sm text-gray-00">
                  Selected file: {resume.name}
                </p>
              )}
            </div>

            {/* Occupation Input */}
            <div>
              <label
                htmlFor="occupation"
                className="block text-lg font-semibold text-gray-200 mb-2"
              >
                Occupation
              </label>
              <input
                type="text"
                id="occupation"
                placeholder="e.g., Software Engineer"
                value={occupation}
                onChange={(e) => setOccupation(e.target.value)}
                className="block w-full p-3 text-sm bg-gray-800 text-gray-200 border border-black rounded-lg focus:ring-4 focus:ring-purple-500 focus:outline-none shadow-lg transition-all duration-300"
                required
              />
            </div>

            {/* Number of Questions */}
            <div>
              <label
                htmlFor="numQuestions"
                className="block text-lg font-semibold text-gray-200 mb-2"
              >
                Number of Questions
              </label>
              <input
                type="number"
                id="numQuestions"
                min="1"
                max="5"
                value={numQuestions}
                onChange={(e) => setNumQuestions(Number(e.target.value))}
                className="block w-full p-3 text-sm bg-gray-800 text-gray-200 border  border-black rounded-xl focus:ring-4 focus:ring-purple-500 focus:outline-none shadow-lg transition-all duration-300"
                required
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full py-3 px-5 bg-indigo-500 hover:from-indigo-500 hover:to-black text-white font-bold text-lg rounded-lg shadow-lg focus:outline-none focus:ring-4 focus:ring-purple-400 transition-all duration-300"
              disabled={isLoading}
            >
              {isLoading ? "Submitting..." : "Submit"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default GetStarted;