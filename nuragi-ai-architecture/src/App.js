import React from 'react';
import { Slack, MessageSquare, Bot, Mail, Clock, Brain, UserCog, PenTool, ClipboardCheck, Mic, Video, Settings, Cloud, Server, ArrowDown, ArrowUp, Repeat } from 'lucide-react';

// Main App Component
const App = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white font-inter p-4 sm:p-8 flex items-center justify-center">
      <div className="w-full max-w-6xl bg-gray-900 border border-gray-700 rounded-xl shadow-2xl overflow-hidden">
        {/* Diagram Title */}
        <div className="p-6 sm:p-8 border-b border-gray-700 text-center">
          <h1 className="text-3xl sm:text-4xl font-bold text-blue-400 mb-2">Agentic AI Orchestration Platform</h1>
          <p className="text-gray-400 text-lg">High-Level Architecture Diagram</p>
        </div>

        {/* Diagram Body - Layers */}
        <div className="p-6 sm:p-8 space-y-10">

          {/* Client Layer */}
          <div className="relative bg-gray-800 border border-gray-700 rounded-lg p-6 flex flex-col items-center shadow-lg">
            <h2 className="text-xl sm:text-2xl font-semibold text-green-400 mb-4">Client Layer</h2>
            <div className="flex flex-wrap justify-center gap-6 sm:gap-8">
              <IconCard icon={<Slack size={36} />} label="Slack" />
              <IconCard icon={<MessageSquare size={36} />} label="MS Teams" />
              <IconCard icon={<Bot size={36} />} label="Chatbot" />
              <IconCard icon={<Mail size={36} />} label="Email" />
              <IconCard icon={<Clock size={36} />} label="Cron Jobs" />
            </div>
            {/* Downward arrows indicating triggers */}
            <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 flex flex-col items-center">
              <ArrowDown size={32} className="text-blue-500 animate-pulse-flow" />
              <div className="w-0.5 h-8 bg-blue-500 animate-flow-line"></div>
            </div>
          </div>

          {/* Spacer with animated arrow */}
          <div className="relative h-16 flex items-center justify-center">
            <div className="w-0.5 h-full bg-gradient-to-b from-blue-500 to-purple-500 animate-flow-line-vertical"></div>
            <ArrowDown size={32} className="absolute text-purple-500 animate-pulse-flow" style={{ animationDelay: '0.5s' }} />
          </div>

          {/* Control Plane / Orchestration Layer */}
          <div className="relative bg-gray-800 border border-gray-700 rounded-lg p-6 flex flex-col items-center shadow-lg">
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-400 mb-4">Control Plane / Orchestration Layer</h2>
            <div className="flex flex-col items-center space-y-6">
              {/* LLM Brain */}
              <div className="bg-purple-600 p-4 rounded-full shadow-xl animate-glow">
                <Brain size={48} className="text-white" />
              </div>
              <p className="text-lg font-medium text-gray-300">LLM Core</p>

              {/* AI Agent Modules */}
              <div className="flex flex-wrap justify-center gap-6 sm:gap-10 mt-4">
                <AgentModule icon={<UserCog size={30} />} label="Agent 1" />
                <AgentModule icon={<UserCog size={30} />} label="Agent 2" />
                <AgentModule icon={<UserCog size={30} />} label="Agent N" />
              </div>
            </div>
            {/* Downward arrows to Tool & Data Layer */}
            <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 flex flex-col items-center">
              <ArrowDown size={32} className="text-purple-500 animate-pulse-flow" />
              <div className="w-0.5 h-8 bg-purple-500 animate-flow-line"></div>
            </div>
          </div>

          {/* Spacer with animated arrow */}
          <div className="relative h-16 flex items-center justify-center">
            <div className="w-0.5 h-full bg-gradient-to-b from-purple-500 to-teal-500 animate-flow-line-vertical" style={{ animationDelay: '1s' }}></div>
            <ArrowDown size={32} className="absolute text-teal-500 animate-pulse-flow" style={{ animationDelay: '1.5s' }} />
          </div>

          {/* Tool & Data Layer */}
          <div className="relative bg-gray-800 border border-gray-700 rounded-lg p-6 flex flex-col items-center shadow-lg">
            <h2 className="text-xl sm:text-2xl font-semibold text-teal-400 mb-4">Tool & Data Layer</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 sm:gap-8">
              <ToolCard icon={<PenTool size={32} />} label="Content Creation (Jasper AI)" />
              <ToolCard icon={<ClipboardCheck size={32} />} label="Plagiarism Detection (Originality.ai)" />
              <ToolCard icon={<Mic size={32} />} label="Meeting Assistance (Otter.ai)" />
              <ToolCard icon={<Video size={32} />} label="Video/Speech AI" />
              <ToolCard icon={<Settings size={32} />} label="Custom Enterprise Tools" />
              <ToolCard icon={<Cloud size={32} />} label="Multi-Model Access (Together.ai)" />
            </div>
            {/* Upward arrows for Outcome & Feedback */}
            <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 flex flex-col items-center">
              <div className="w-0.5 h-8 bg-green-500 animate-flow-line-reverse"></div>
              <ArrowUp size={32} className="text-green-500 animate-pulse-flow-reverse" />
            </div>
          </div>

          {/* Spacer with animated arrow for Infrastructure */}
          <div className="relative h-16 flex items-center justify-center">
            <div className="w-0.5 h-full bg-gradient-to-b from-teal-500 to-gray-600 animate-flow-line-vertical" style={{ animationDelay: '2s' }}></div>
            <ArrowDown size={32} className="absolute text-gray-600 animate-pulse-flow" style={{ animationDelay: '2.5s' }} />
          </div>

          {/* Infrastructure Layer */}
          <div className="relative bg-gray-800 border border-gray-700 rounded-lg p-6 flex flex-col items-center shadow-lg">
            <h2 className="text-xl sm:text-2xl font-semibold text-yellow-400 mb-4">Infrastructure Layer</h2>
            <div className="flex flex-wrap justify-center gap-6 sm:gap-8">
              <IconCard icon={<Server size={36} />} label="Server Racks" />
              <IconCard icon={<Cloud size={36} />} label="Cloud Providers (Coreweave)" />
            </div>
          </div>

        </div>

        {/* Dynamic Styles for Animations */}
        <style jsx>{`
          @keyframes pulse-flow {
            0%, 100% { opacity: 0.2; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1); }
          }
          @keyframes pulse-flow-reverse {
            0%, 100% { opacity: 0.2; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1); }
          }
          @keyframes flow-line {
            0% { transform: scaleY(0); transform-origin: top; }
            100% { transform: scaleY(1); transform-origin: top; }
          }
          @keyframes flow-line-reverse {
            0% { transform: scaleY(0); transform-origin: bottom; }
            100% { transform: scaleY(1); transform-origin: bottom; }
          }
          @keyframes flow-line-vertical {
            0% { background-position: 0% 0%; }
            100% { background-position: 0% 100%; }
          }
          @keyframes glow {
            0%, 100% { box-shadow: 0 0 5px rgba(168, 85, 247, 0.5), 0 0 10px rgba(168, 85, 247, 0.3); }
            50% { box-shadow: 0 0 15px rgba(168, 85, 247, 0.8), 0 0 30px rgba(168, 85, 247, 0.6); }
          }

          .animate-pulse-flow { animation: pulse-flow 2s infinite ease-in-out; }
          .animate-pulse-flow-reverse { animation: pulse-flow-reverse 2s infinite ease-in-out; }
          .animate-flow-line { animation: flow-line 1.5s infinite linear; }
          .animate-flow-line-reverse { animation: flow-line-reverse 1.5s infinite linear; }
          .animate-flow-line-vertical {
            animation: flow-line-vertical 2s infinite linear;
            background-size: 100% 200%; /* Ensures the gradient moves */
          }
          .animate-glow { animation: glow 3s infinite ease-in-out; }
        `}</style>
      </div>
    </div>
  );
};

// Reusable Icon Card Component
const IconCard = ({ icon, label }) => (
  <div className="flex flex-col items-center p-4 bg-gray-700 rounded-md border border-gray-600 shadow-md transform transition-transform hover:scale-105 duration-300">
    <div className="text-blue-300 mb-2">{icon}</div>
    <span className="text-sm text-gray-300 text-center">{label}</span>
  </div>
);

// Reusable Agent Module Component
const AgentModule = ({ icon, label }) => (
  <div className="flex flex-col items-center p-4 bg-gray-700 rounded-full border border-gray-600 shadow-md animate-pulse-glow-subtle">
    <div className="text-green-300 mb-2">{icon}</div>
    <span className="text-sm text-gray-300 text-center">{label}</span>
    <style jsx>{`
      @keyframes pulse-glow-subtle {
        0%, 100% { box-shadow: 0 0 3px rgba(52, 211, 153, 0.5); }
        50% { box-shadow: 0 0 10px rgba(52, 211, 153, 0.8); }
      }
      .animate-pulse-glow-subtle { animation: pulse-glow-subtle 2.5s infinite ease-in-out; }
    `}</style>
  </div>
);

// Reusable Tool Card Component
const ToolCard = ({ icon, label }) => (
  <div className="flex flex-col items-center p-4 bg-gray-700 rounded-md border border-gray-600 shadow-md transform transition-transform hover:scale-105 duration-300">
    <div className="text-teal-300 mb-2">{icon}</div>
    <span className="text-sm text-gray-300 text-center">{label}</span>
  </div>
);

export default App;
