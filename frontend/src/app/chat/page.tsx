"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Send } from "lucide-react";

export default function ChatPage() {
  const [messages, setMessages] = useState<{role: "user" | "ai", text: string}[]>([
    { role: "ai", text: "Hello! I am MindVault. Ask me anything about your documents." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setMessages(prev => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      // In a real app, you would fetch from /api/chat
      // For now we simulate the interaction
      setTimeout(() => {
        setMessages(prev => [...prev, { role: "ai", text: "I am a simulated response. The backend AI service is being connected." }]);
        setLoading(false);
      }, 1000);
    } catch (e) {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Chat</h1>
        <p className="text-slate-500">
          Converse with your knowledge base.
        </p>
      </div>

      <Card className="flex-1 bg-white shadow-sm rounded-xl border border-slate-100 flex flex-col overflow-hidden h-[600px]">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`p-3 rounded-xl max-w-[70%] ${msg.role === "user" ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-800"}`}>
                {msg.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="p-3 rounded-xl bg-slate-100 text-slate-800 animate-pulse">
                Thinking...
              </div>
            </div>
          )}
        </div>
        <div className="p-4 border-t bg-slate-50 flex gap-2">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask a question..."
            className="flex-1 rounded-lg border-slate-200 border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-slate-900"
          />
          <button 
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="bg-slate-900 text-white px-4 py-2 rounded-lg hover:bg-slate-800 disabled:opacity-50 transition"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </Card>
    </div>
  );
}
