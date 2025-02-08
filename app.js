import { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!query.trim()) return;

    const userMessage = { sender: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", { query });
      const botMessage = { sender: "bot", text: response.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
    }

    setQuery("");
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="w-1/2 bg-white p-6 rounded shadow-lg">
        <h2 className="text-xl font-bold mb-4">AI Chatbot</h2>
        <div className="h-64 overflow-y-auto border p-3 mb-4">
          {messages.map((msg, index) => (
            <div key={index} className={`p-2 my-1 ${msg.sender === "user" ? "text-right" : "text-left"}`}>
              <span className={`px-3 py-1 rounded ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-300"}`}>
                {msg.text}
              </span>
            </div>
          ))}
        </div>
        <div className="flex">
          <input
            type="text"
            className="border p-2 w-full rounded-l"
            placeholder="Ask about products or suppliers..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button className="bg-blue-500 text-white p-2 rounded-r" onClick={handleSend}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
