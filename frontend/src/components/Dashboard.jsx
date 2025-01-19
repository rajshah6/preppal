import React from 'react';
import Navbar from './Navbar';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import 'react-circular-progressbar/dist/styles.css';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const progress = 43; // Example overall score

  // Data for past interview scores
  const barData = [
    { name: 'Mon', score: 30 },
    { name: 'Tue', score: 45 },
    { name: 'Wed', score: 60 },
    { name: 'Thu', score: 50 },
    { name: 'Fri', score: 70 },
    { name: 'Sat', score: 80 },
    { name: 'Sun', score: 65 },
  ];

  // Data for areas of improvement (Pie Chart)
  const pieData = [
    { name: 'Eye Contact', value: 25 },
    { name: 'Confidence', value: 40 },
    { name: 'Tone', value: 20 },
    { name: 'Length', value: 15 },
  ];

  const COLORS = ['#a855f7', '#7e22ce', '#6b21a8', '#5b21b6'];

  return (
    <div className="bg-gradient-to-t from-black via-gray-900 to-purple-900 min-h-screen text-white">
      <div className="container mx-auto px-6 pt-24 pb-10">
        {/* Header Row: Welcome Message & Action Button */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
          <div className="lg:col-span-2 flex flex-col justify-center">
            <h1 className="text-8xl lg:text-7xl font-extrabold mb-3">
              Welcome Back Ajith!
            </h1>
            <p className="text-2xl lg:text-2xl text-gray-400 mb-5">
              A summary of your past interviews to see your overall feedback 
            </p>
            <div className="flex justify-start">
            <button
              onClick={() => navigate('/get-started')}
              className="w-max px-10 py-6 bg-purple-600 hover:bg-purple-700 transition text-xl text-white font-semibold rounded-md shadow-md"
            >
              New Interview
            </button>
            </div>

          </div>
          {/* Overall Score Card */}
          <div className="flex items-center justify-center">
            <div className="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-xs">
              <div className="w-28 h-28 mx-auto">
                <CircularProgressbar
                  value={progress}
                  text={`${progress}%`}
                  styles={buildStyles({
                    textColor: '#fff',
                    pathColor: '#a855f7',
                    trailColor: '#374151',
                  })}
                />
              </div>
              <h2 className="mt-4 text-center text-xl font-semibold text-purple-500">
                Average Overall Score
              </h2>
            </div>
          </div>
        </div>

        {/* Metrics Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Past Interview Scores Graph */}
          <div className="bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold mb-4 text-white">
              Past Interview Scores
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={barData}>
                <XAxis dataKey="name" stroke="#a855f7" />
                <YAxis stroke="#a855f7" />
                <Tooltip />
                <Bar dataKey="score" fill="#a855f7" barSize={30} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Areas of Improvement Pie Chart */}
          <div className="bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold mb-4 text-white">
              Areas of Improvement
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={70}
                  fill="#a855f7"
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Quick Action Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-10">
          {/* View Past Interviews */}
          <div
            onClick={() => navigate('/dashboard')}
            className="cursor-pointer bg-gray-800 rounded-lg shadow-lg p-6 hover:bg-gray-700 transition"
          >
            <h3 className="text-xl font-semibold text-white mb-2">View Past Interviews</h3>
            <p className="text-gray-400">
              Review your previous practice sessions and feedback.
            </p>
          </div>

          {/* Next Steps */}
          <div
            onClick={() => navigate('/dashboard')}
            className="cursor-pointer bg-gray-800 rounded-lg shadow-lg p-6 hover:bg-gray-700 transition"
          >
            <h3 className="text-xl font-semibold text-white mb-2">Next Steps</h3>
            <p className="text-gray-400">
              Get personalized guidance on improving your interview skills.
            </p>
          </div>
        </div>

        {/* Additional Features (Optional) */}
        <div className="mt-12 grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Achievements */}
          <div className="bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-white mb-4">Recent Achievements</h3>
            <div className="flex justify-between">
              <div className="bg-purple-600 rounded-lg shadow-inner p-4 text-center flex-1 mx-1">
                <p className="text-2xl font-bold">10</p>
                <p className="text-gray-300">Interviews Completed</p>
              </div>
              <div className="bg-purple-600 rounded-lg shadow-inner p-4 text-center flex-1 mx-1">
                <p className="text-2xl font-bold">8</p>
                <p className="text-gray-300">Target Scores Achieved</p>
              </div>
              <div className="bg-purple-600 rounded-lg shadow-inner p-4 text-center flex-1 mx-1">
                <p className="text-2xl font-bold">5</p>
                <p className="text-gray-300">Areas Improved</p>
              </div>
            </div>
          </div>

          {/* Upcoming Goals */}
          <div className="bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-semibold text-white mb-4">Upcoming Goals</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-300">
              <li>Complete 5 new interview simulations.</li>
              <li>Focus on communication skills.</li>
              <li>Refine problem-solving techniques.</li>
              <li>Set a target score of 70% in next assessments.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;