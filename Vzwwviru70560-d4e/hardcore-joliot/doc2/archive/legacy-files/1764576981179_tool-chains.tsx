import React, { useState } from 'react';

const availableTools = [
  { id: "csv_parser", name: "CSV Parser", icon: "📊", category: "Data" },
  { id: "json_transformer", name: "JSON Transform", icon: "🔄", category: "Data" },
  { id: "sentiment_analyzer", name: "Sentiment", icon: "😊", category: "AI" },
  { id: "entity_extractor", name: "Entities", icon: "🏷️", category: "AI" },
  { id: "text_classifier", name: "Classifier", icon: "🗂️", category: "AI" },
  { id: "email_sender", name: "Email", icon: "📧", category: "Com" },
  { id: "slack_poster", name: "Slack", icon: "💬", category: "Com" },
  { id: "social_poster", name: "Social", icon: "📱", category: "Marketing" },
  { id: "pdf_extractor", name: "PDF Extract", icon: "📄", category: "Data" },
  { id: "chatbot_engine", name: "Chatbot", icon: "🤖", category: "AI" },
  { id: "webhook_caller", name: "Webhook", icon: "🔗", category: "Com" },
  { id: "ab_tester", name: "A/B Test", icon: "🔬", category: "Marketing" },
];

const presetChains = [
  {
    id: "content_analysis",
    name: "📝 Analyse de Contenu",
    description: "Extrait, analyse et classifie le contenu",
    tools: ["pdf_extractor", "entity_extractor", "sentiment_analyzer", "text_classifier"]
  },
  {
    id: "social_campaign",
    name: "📣 Campagne Social",
    description: "Crée et publie du contenu sur les réseaux",
    tools: ["chatbot_engine", "social_poster", "ab_tester", "webhook_caller"]
  },
  {
    id: "data_pipeline",
    name: "🔄 Pipeline Données",
    description: "Traite les données CSV et notifie",
    tools: ["csv_parser", "json_transformer", "email_sender"]
  },
  {
    id: "customer_feedback",
    name: "💬 Feedback Client",
    description: "Analyse les retours clients",
    tools: ["csv_parser", "sentiment_analyzer", "entity_extractor", "slack_poster"]
  }
];

export default function ToolChains() {
  const [activeChain, setActiveChain] = useState([]);
  const [chainName, setChainName] = useState("");
  const [savedChains, setSavedChains] = useState(presetChains);
  const [draggedTool, setDraggedTool] = useState(null);

  const addTool = (tool) => {
    if (activeChain.length < 8) {
      setActiveChain([...activeChain, { ...tool, stepId: Date.now() }]);
    }
  };

  const removeTool = (stepId) => {
    setActiveChain(activeChain.filter(t => t.stepId !== stepId));
  };

  const loadPreset = (preset) => {
    const tools = preset.tools.map((toolId, idx) => ({
      ...availableTools.find(t => t.id === toolId),
      stepId: Date.now() + idx
    }));
    setActiveChain(tools);
    setChainName(preset.name);
  };

  const saveChain = () => {
    if (chainName && activeChain.length > 0) {
      const newChain = {
        id: `custom_${Date.now()}`,
        name: chainName,
        description: `Chain personnalisée avec ${activeChain.length} outils`,
        tools: activeChain.map(t => t.id)
      };
      setSavedChains([...savedChains, newChain]);
      setChainName("");
      setActiveChain([]);
    }
  };

  const getTool = (toolId) => availableTools.find(t => t.id === toolId);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <span className="text-3xl">🔗</span>
          <h1 className="text-2xl font-bold">Tool Chains Builder</h1>
        </div>

        <div className="grid grid-cols-3 gap-4">
          {/* Available Tools */}
          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3 text-purple-400">🧰 Outils Disponibles</h2>
            <div className="grid grid-cols-2 gap-2">
              {availableTools.map(tool => (
                <button
                  key={tool.id}
                  onClick={() => addTool(tool)}
                  className="bg-gray-700 hover:bg-gray-600 p-2 rounded text-sm flex items-center gap-2 transition"
                >
                  <span>{tool.icon}</span>
                  <span className="truncate">{tool.name}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Chain Builder */}
          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3 text-blue-400">⛓️ Chaîne Active</h2>
            
            <input
              type="text"
              value={chainName}
              onChange={(e) => setChainName(e.target.value)}
              placeholder="Nom de la chaîne..."
              className="w-full bg-gray-700 rounded px-3 py-2 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            <div className="space-y-2 min-h-64">
              {activeChain.length === 0 ? (
                <div className="text-gray-500 text-center py-8">
                  Clique sur les outils à gauche pour construire ta chaîne
                </div>
              ) : (
                activeChain.map((tool, idx) => (
                  <div key={tool.stepId} className="flex items-center gap-2">
                    <span className="text-gray-500 w-6">{idx + 1}.</span>
                    <div className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 p-2 rounded flex items-center gap-2">
                      <span>{tool.icon}</span>
                      <span>{tool.name}</span>
                    </div>
                    <button
                      onClick={() => removeTool(tool.stepId)}
                      className="text-red-400 hover:text-red-300 px-2"
                    >
                      ✕
                    </button>
                    {idx < activeChain.length - 1 && (
                      <div className="absolute left-8 mt-8 text-gray-500">↓</div>
                    )}
                  </div>
                ))
              )}
            </div>

            <div className="flex gap-2 mt-4">
              <button
                onClick={saveChain}
                disabled={!chainName || activeChain.length === 0}
                className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 py-2 rounded font-semibold transition"
              >
                💾 Sauvegarder
              </button>
              <button
                onClick={() => { setActiveChain([]); setChainName(""); }}
                className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded transition"
              >
                🗑️
              </button>
            </div>
          </div>

          {/* Saved Chains */}
          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3 text-green-400">📦 Chaînes Sauvegardées</h2>
            <div className="space-y-3">
              {savedChains.map(chain => (
                <div
                  key={chain.id}
                  className="bg-gray-700 rounded-lg p-3 hover:bg-gray-650 cursor-pointer"
                  onClick={() => loadPreset(chain)}
                >
                  <div className="font-semibold mb-1">{chain.name}</div>
                  <div className="text-gray-400 text-xs mb-2">{chain.description}</div>
                  <div className="flex gap-1 flex-wrap">
                    {chain.tools.map((toolId, idx) => {
                      const tool = getTool(toolId);
                      return tool ? (
                        <span key={idx} className="text-lg" title={tool.name}>
                          {tool.icon}
                        </span>
                      ) : null;
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Execution Preview */}
        {activeChain.length > 0 && (
          <div className="mt-4 bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-3 text-yellow-400">⚡ Aperçu d'exécution</h2>
            <div className="flex items-center gap-2 overflow-x-auto pb-2">
              {activeChain.map((tool, idx) => (
                <React.Fragment key={tool.stepId}>
                  <div className="bg-gradient-to-br from-purple-600 to-blue-600 p-3 rounded-lg text-center min-w-20">
                    <div className="text-2xl mb-1">{tool.icon}</div>
                    <div className="text-xs">{tool.name}</div>
                  </div>
                  {idx < activeChain.length - 1 && (
                    <div className="text-2xl text-gray-500">→</div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
