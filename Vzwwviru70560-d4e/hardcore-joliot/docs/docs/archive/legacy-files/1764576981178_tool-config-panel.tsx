import React, { useState } from 'react';

const toolsData = {
  "Communication": [
    { id: "email_sender", name: "Email Sender", icon: "📧", cost: 50, params: ["smtp_server", "port", "auth_method", "timeout"] },
    { id: "slack_poster", name: "Slack Poster", icon: "💬", cost: 30, params: ["workspace", "default_channel", "bot_token", "rate_limit"] },
    { id: "sms_sender", name: "SMS Sender", icon: "📱", cost: 100, params: ["provider", "api_key", "sender_id", "country_code"] },
    { id: "webhook_caller", name: "Webhook Caller", icon: "🔗", cost: 20, params: ["timeout", "retry_count", "headers", "auth_type"] },
  ],
  "Data Processing": [
    { id: "csv_parser", name: "CSV Parser", icon: "📊", cost: 30, params: ["delimiter", "encoding", "header_row", "max_rows"] },
    { id: "json_transformer", name: "JSON Transformer", icon: "🔄", cost: 25, params: ["schema_validation", "null_handling", "nested_depth"] },
    { id: "pdf_extractor", name: "PDF Extractor", icon: "📄", cost: 150, params: ["ocr_enabled", "language", "page_range", "output_format"] },
    { id: "image_processor", name: "Image Processor", icon: "🖼️", cost: 200, params: ["max_size", "formats", "compression", "resize_mode"] },
  ],
  "AI & ML": [
    { id: "sentiment_analyzer", name: "Sentiment Analyzer", icon: "😊", cost: 100, params: ["model", "language", "confidence_threshold", "batch_size"] },
    { id: "entity_extractor", name: "Entity Extractor", icon: "🏷️", cost: 150, params: ["entity_types", "model", "context_window"] },
    { id: "text_classifier", name: "Text Classifier", icon: "🗂️", cost: 100, params: ["categories", "model", "threshold"] },
    { id: "chatbot_engine", name: "Chatbot Engine", icon: "🤖", cost: 300, params: ["llm_model", "temperature", "max_tokens", "system_prompt"] },
  ],
  "Marketing": [
    { id: "social_poster", name: "Social Poster", icon: "📱", cost: 100, params: ["platforms", "schedule_mode", "hashtag_limit", "media_types"] },
    { id: "email_campaign", name: "Email Campaign", icon: "📧", cost: 250, params: ["template_engine", "personalization", "tracking", "unsubscribe"] },
    { id: "ab_tester", name: "A/B Tester", icon: "🔬", cost: 300, params: ["variants", "traffic_split", "metric", "duration"] },
  ]
};

const defaultValues = {
  smtp_server: "smtp.gmail.com", port: "587", auth_method: "OAuth2", timeout: "30",
  workspace: "chenu-team", default_channel: "#general", bot_token: "xoxb-***", rate_limit: "50",
  provider: "Twilio", api_key: "sk-***", sender_id: "CHENU", country_code: "+1",
  delimiter: ",", encoding: "UTF-8", header_row: "true", max_rows: "10000",
  schema_validation: "strict", null_handling: "ignore", nested_depth: "5",
  ocr_enabled: "true", language: "fr", page_range: "all", output_format: "markdown",
  max_size: "10MB", formats: "jpg,png,webp", compression: "85", resize_mode: "fit",
  model: "claude-sonnet", confidence_threshold: "0.8", batch_size: "10",
  entity_types: "person,org,location", context_window: "512",
  categories: "positive,negative,neutral", threshold: "0.7",
  llm_model: "claude-opus", temperature: "0.7", max_tokens: "4096", system_prompt: "",
  platforms: "twitter,linkedin,instagram", schedule_mode: "queue", hashtag_limit: "5", media_types: "image,video",
  template_engine: "handlebars", personalization: "true", tracking: "true", unsubscribe: "true",
  variants: "2", traffic_split: "50/50", metric: "conversion", duration: "7d"
};

export default function ToolConfigPanel() {
  const [selectedCategory, setSelectedCategory] = useState("Communication");
  const [selectedTool, setSelectedTool] = useState(null);
  const [configs, setConfigs] = useState({});
  const [savedTools, setSavedTools] = useState([]);

  const handleConfigChange = (toolId, param, value) => {
    setConfigs(prev => ({
      ...prev,
      [toolId]: { ...prev[toolId], [param]: value }
    }));
  };

  const saveTool = (tool) => {
    if (!savedTools.includes(tool.id)) {
      setSavedTools([...savedTools, tool.id]);
    }
  };

  const getConfigValue = (toolId, param) => {
    return configs[toolId]?.[param] ?? defaultValues[param] ?? "";
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <span className="text-3xl">🔌</span>
          <h1 className="text-2xl font-bold">Tool Configuration Panel</h1>
          <span className="ml-auto bg-green-600 px-3 py-1 rounded-full text-sm">
            {savedTools.length} configuré(s)
          </span>
        </div>

        <div className="grid grid-cols-4 gap-4">
          {/* Categories */}
          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3 text-purple-400">📁 Catégories</h2>
            {Object.keys(toolsData).map(cat => (
              <button
                key={cat}
                onClick={() => { setSelectedCategory(cat); setSelectedTool(null); }}
                className={`w-full text-left p-2 rounded mb-1 transition ${
                  selectedCategory === cat ? 'bg-purple-600' : 'hover:bg-gray-700'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Tools List */}
          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3 text-blue-400">🔧 Outils</h2>
            {toolsData[selectedCategory]?.map(tool => (
              <button
                key={tool.id}
                onClick={() => setSelectedTool(tool)}
                className={`w-full text-left p-2 rounded mb-1 flex items-center gap-2 transition ${
                  selectedTool?.id === tool.id ? 'bg-blue-600' : 'hover:bg-gray-700'
                }`}
              >
                <span>{tool.icon}</span>
                <span className="flex-1">{tool.name}</span>
                {savedTools.includes(tool.id) && <span className="text-green-400">✓</span>}
              </button>
            ))}
          </div>

          {/* Configuration */}
          <div className="col-span-2 bg-gray-800 rounded-lg p-4">
            {selectedTool ? (
              <>
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-3xl">{selectedTool.icon}</span>
                  <div>
                    <h2 className="text-xl font-bold">{selectedTool.name}</h2>
                    <span className="text-yellow-400 text-sm">⚡ {selectedTool.cost} tokens</span>
                  </div>
                </div>

                <div className="space-y-3">
                  {selectedTool.params.map(param => (
                    <div key={param}>
                      <label className="block text-sm text-gray-400 mb-1">{param}</label>
                      <input
                        type="text"
                        value={getConfigValue(selectedTool.id, param)}
                        onChange={(e) => handleConfigChange(selectedTool.id, param, e.target.value)}
                        className="w-full bg-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                        placeholder={defaultValues[param]}
                      />
                    </div>
                  ))}
                </div>

                <div className="flex gap-2 mt-4">
                  <button
                    onClick={() => saveTool(selectedTool)}
                    className="flex-1 bg-green-600 hover:bg-green-700 py-2 rounded font-semibold transition"
                  >
                    💾 Sauvegarder
                  </button>
                  <button
                    onClick={() => setConfigs(prev => ({ ...prev, [selectedTool.id]: {} }))}
                    className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded transition"
                  >
                    🔄 Reset
                  </button>
                </div>
              </>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500">
                <p>← Sélectionne un outil pour le configurer</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
