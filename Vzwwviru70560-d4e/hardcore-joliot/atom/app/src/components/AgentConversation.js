/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       █████╗  ██████╗ ███████╗███╗   ██╗████████╗     ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ███████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
 *      ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
 *      ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║       ██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝███████╗███████║   ██║   ██║██║   ██║██╔██╗ ██║
 *      ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║       ██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
 *      ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║███████║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
 *      ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
 *
 *                              💬 INTERFACE DE CONVERSATION AVEC AGENTS 💬
 *                         Chat immersif avec Nova, Aria et les 287 agents
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { getOrchestrator, CORE_AGENTS } from '../lib/AgentOrchestrationSystem';

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: AVATAR AGENT
// ═══════════════════════════════════════════════════════════════════════════════

const AgentAvatar = ({ agent, size = 'md', isTyping = false, isSpeaking = false }) => {
  const sizeClasses = {
    sm: 'w-8 h-8 text-sm',
    md: 'w-12 h-12 text-xl',
    lg: 'w-16 h-16 text-2xl',
    xl: 'w-24 h-24 text-4xl'
  };

  return (
    <div className="relative">
      <div
        className={`${sizeClasses[size]} rounded-full flex items-center justify-center
          transition-all duration-300 ${isSpeaking ? 'animate-pulse' : ''}`}
        style={{
          backgroundColor: `${agent.color}20`,
          border: `2px solid ${agent.color}`,
          boxShadow: isSpeaking ? `0 0 20px ${agent.color}50` : 'none'
        }}
      >
        <span>{agent.icon}</span>
      </div>

      {/* Status indicator */}
      <div
        className={`absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-gray-900
          ${isTyping ? 'bg-yellow-500 animate-pulse' : agent.status === 'active' ? 'bg-green-500' : 'bg-gray-500'}`}
      />

      {/* Typing indicator */}
      {isTyping && (
        <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2">
          <div className="flex gap-1">
            <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: MESSAGE DE CHAT
// ═══════════════════════════════════════════════════════════════════════════════

const ChatMessage = ({ message, agent }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
      {!isUser && agent && (
        <AgentAvatar agent={agent} size="sm" />
      )}

      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-yellow-600 text-black rounded-br-none'
            : 'bg-gray-800 text-white rounded-bl-none'
        }`}
      >
        {!isUser && agent && (
          <div className="text-xs opacity-60 mb-1" style={{ color: agent.color }}>
            {agent.name} • {agent.level}
          </div>
        )}
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        <div className={`text-xs mt-1 ${isUser ? 'text-black/50' : 'text-gray-500'}`}>
          {new Date(message.timestamp).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SÉLECTEUR D'AGENT
// ═══════════════════════════════════════════════════════════════════════════════

const AgentSelector = ({ agents, selectedAgentId, onSelect, isOpen, onToggle }) => {
  const coreAgents = Object.values(CORE_AGENTS).filter(a => a.level === 'L0' || a.level === 'L1');

  return (
    <div className="relative">
      {/* Bouton de sélection */}
      <button
        onClick={onToggle}
        className="flex items-center gap-2 px-3 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
      >
        {selectedAgentId && agents.get(selectedAgentId) ? (
          <>
            <AgentAvatar agent={agents.get(selectedAgentId)} size="sm" />
            <span className="text-sm text-white">{agents.get(selectedAgentId).name}</span>
          </>
        ) : (
          <span className="text-sm text-gray-400">Choisir un agent</span>
        )}
        <svg
          className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown */}
      {isOpen && (
        <>
          <div className="fixed inset-0 z-40" onClick={onToggle} />
          <div className="absolute bottom-full left-0 mb-2 w-72 bg-gray-900 border border-gray-700 rounded-xl
            shadow-xl z-50 overflow-hidden">
            <div className="p-2 border-b border-gray-800">
              <h4 className="text-xs text-gray-500 uppercase tracking-wider px-2">Agents Principaux</h4>
            </div>
            <div className="max-h-64 overflow-y-auto p-2 space-y-1">
              {coreAgents.map(agent => (
                <button
                  key={agent.id}
                  onClick={() => { onSelect(agent.id); onToggle(); }}
                  className={`w-full flex items-center gap-3 p-2 rounded-lg transition-colors ${
                    selectedAgentId === agent.id
                      ? 'bg-yellow-500/20 border border-yellow-500/30'
                      : 'hover:bg-gray-800'
                  }`}
                >
                  <AgentAvatar agent={agent} size="sm" />
                  <div className="flex-1 text-left">
                    <div className="text-sm text-white">{agent.name}</div>
                    <div className="text-xs text-gray-500">{agent.specialty}</div>
                  </div>
                  <span
                    className="px-1.5 py-0.5 rounded text-xs"
                    style={{ backgroundColor: `${agent.color}20`, color: agent.color }}
                  >
                    {agent.level}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: CONTRÔLES VOCAUX
// ═══════════════════════════════════════════════════════════════════════════════

const VoiceControls = ({ onStartListening, onStopListening, isListening, onSpeak, isSpeaking }) => {
  return (
    <div className="flex items-center gap-2">
      {/* Bouton microphone */}
      <button
        onClick={isListening ? onStopListening : onStartListening}
        className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
          isListening
            ? 'bg-red-500 text-white animate-pulse'
            : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
        }`}
        title={isListening ? 'Arrêter l\'écoute' : 'Parler'}
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <path d="M8 1a2 2 0 0 0-2 2v4a2 2 0 1 0 4 0V3a2 2 0 0 0-2-2z" />
          <path d="M4.5 7a.5.5 0 0 0-1 0v.5A4.5 4.5 0 0 0 8 12a4.5 4.5 0 0 0 4.5-4.5V7a.5.5 0 0 0-1 0v.5a3.5 3.5 0 1 1-7 0V7z" />
          <path d="M8 14a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-1 0v2a.5.5 0 0 0 .5.5z" />
        </svg>
      </button>

      {/* Bouton haut-parleur */}
      <button
        onClick={onSpeak}
        className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
          isSpeaking
            ? 'bg-green-500 text-white animate-pulse'
            : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
        }`}
        title={isSpeaking ? 'Arrêter la lecture' : 'Lire le dernier message'}
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <path d="M9 2v12l-4-4H2V6h3l4-4z" />
          <path d="M11.5 4.5a4.5 4.5 0 0 1 0 7M13 3a6.5 6.5 0 0 1 0 10" fill="none" stroke="currentColor" strokeWidth="1.5" />
        </svg>
      </button>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT: SUGGESTIONS DE PROMPTS
// ═══════════════════════════════════════════════════════════════════════════════

const PromptSuggestions = ({ agent, onSelect }) => {
  const getSuggestions = (agentId) => {
    const suggestions = {
      nova: [
        'Analyse mon activité récente',
        'Génère un environnement de travail',
        'Optimise mes paramètres système'
      ],
      aria: [
        'Aide-moi à brainstormer des idées',
        'Crée une ambiance créative',
        'Inspire-moi pour mon projet'
      ],
      orion: [
        'Vérifie la sécurité de mon compte',
        'Analyse les menaces potentielles',
        'Recommande des mesures de protection'
      ],
      default: [
        'Comment puis-tu m\'aider ?',
        'Quelles sont tes capacités ?',
        'Parle-moi de toi'
      ]
    };

    return suggestions[agentId] || suggestions.default;
  };

  if (!agent) return null;

  const suggestions = getSuggestions(agent.id);

  return (
    <div className="flex flex-wrap gap-2 mb-4">
      {suggestions.map((suggestion, index) => (
        <button
          key={index}
          onClick={() => onSelect(suggestion)}
          className="px-3 py-1.5 bg-gray-800/50 border border-gray-700 rounded-full text-xs text-gray-300
            hover:bg-gray-700 hover:border-gray-600 transition-colors"
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// COMPOSANT PRINCIPAL: CONVERSATION AGENT
// ═══════════════════════════════════════════════════════════════════════════════

const AgentConversation = ({ initialAgentId = 'nova', onClose }) => {
  const [orchestrator, setOrchestrator] = useState(null);
  const [agents, setAgents] = useState(new Map());
  const [selectedAgentId, setSelectedAgentId] = useState(initialAgentId);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isAgentTyping, setIsAgentTyping] = useState(false);
  const [showAgentSelector, setShowAgentSelector] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [conversationId, setConversationId] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Initialisation
  useEffect(() => {
    const init = async () => {
      const orch = getOrchestrator();
      await orch.initialize();
      setOrchestrator(orch);
      setAgents(orch.agents);

      // Activer l'agent initial
      await orch.activateAgent(initialAgentId);

      // Message de bienvenue
      const agent = orch.getAgent(initialAgentId);
      if (agent) {
        setMessages([{
          id: 'welcome',
          role: 'assistant',
          agentId: agent.id,
          agentName: agent.name,
          content: `Bonjour ! Je suis ${agent.name}, ${agent.specialty}. Comment puis-je vous aider aujourd'hui ?`,
          timestamp: new Date().toISOString()
        }]);
      }
    };

    init();
  }, [initialAgentId]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Envoyer un message
  const sendMessage = useCallback(async (text = inputValue) => {
    if (!text.trim() || !orchestrator || !selectedAgentId) return;

    const userMessage = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: text.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsAgentTyping(true);

    try {
      const result = await orchestrator.sendMessage(selectedAgentId, text.trim(), 'user', conversationId);

      if (!conversationId) {
        setConversationId(result.conversationId);
      }

      const agentMessage = {
        id: `agent_${Date.now()}`,
        role: 'assistant',
        agentId: result.agent.id,
        agentName: result.agent.name,
        content: result.response,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: 'Désolé, une erreur s\'est produite. Veuillez réessayer.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsAgentTyping(false);
    }
  }, [inputValue, orchestrator, selectedAgentId, conversationId]);

  // Changer d'agent
  const handleAgentChange = useCallback(async (agentId) => {
    if (orchestrator && agentId !== selectedAgentId) {
      // Désactiver l'ancien agent
      orchestrator.deactivateAgent(selectedAgentId);

      // Activer le nouvel agent
      await orchestrator.activateAgent(agentId);
      setSelectedAgentId(agentId);

      // Message de transition
      const agent = orchestrator.getAgent(agentId);
      if (agent) {
        setMessages(prev => [...prev, {
          id: `switch_${Date.now()}`,
          role: 'assistant',
          agentId: agent.id,
          agentName: agent.name,
          content: `${agent.name} prend le relais. ${agent.specialty}. Comment puis-je vous assister ?`,
          timestamp: new Date().toISOString()
        }]);
      }
    }
  }, [orchestrator, selectedAgentId]);

  // Lecture vocale
  const handleSpeak = useCallback(async () => {
    if (!orchestrator || isSpeaking) return;

    const lastAgentMessage = [...messages].reverse().find(m => m.role === 'assistant');
    if (lastAgentMessage) {
      setIsSpeaking(true);
      try {
        await orchestrator.speakAs(selectedAgentId, lastAgentMessage.content);
      } catch (error) {
        console.error('Speech error:', error);
      } finally {
        setIsSpeaking(false);
      }
    }
  }, [orchestrator, messages, selectedAgentId, isSpeaking]);

  const selectedAgent = agents.get(selectedAgentId);

  return (
    <div className="flex flex-col h-full bg-gray-950">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-black border-b border-gray-800">
        <div className="flex items-center gap-3">
          {selectedAgent && (
            <>
              <AgentAvatar agent={selectedAgent} size="md" isSpeaking={isSpeaking} />
              <div>
                <h2 className="text-sm font-medium text-white">{selectedAgent.name}</h2>
                <p className="text-xs text-gray-500">{selectedAgent.specialty}</p>
              </div>
            </>
          )}
        </div>

        <div className="flex items-center gap-2">
          <span
            className="px-2 py-1 rounded text-xs"
            style={{
              backgroundColor: selectedAgent ? `${selectedAgent.color}20` : '#6B728020',
              color: selectedAgent?.color || '#6B7280'
            }}
          >
            {selectedAgent?.frequency} Hz
          </span>

          {onClose && (
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-white"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M4 4l8 8M12 4l-8 8" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(message => (
          <ChatMessage
            key={message.id}
            message={message}
            agent={message.agentId ? agents.get(message.agentId) : null}
          />
        ))}

        {isAgentTyping && selectedAgent && (
          <div className="flex gap-3">
            <AgentAvatar agent={selectedAgent} size="sm" isTyping={true} />
            <div className="bg-gray-800 rounded-2xl rounded-bl-none px-4 py-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      {messages.length <= 1 && selectedAgent && (
        <div className="px-4">
          <PromptSuggestions agent={selectedAgent} onSelect={sendMessage} />
        </div>
      )}

      {/* Input Area */}
      <div className="p-4 bg-black border-t border-gray-800">
        <div className="flex items-end gap-3">
          <AgentSelector
            agents={agents}
            selectedAgentId={selectedAgentId}
            onSelect={handleAgentChange}
            isOpen={showAgentSelector}
            onToggle={() => setShowAgentSelector(!showAgentSelector)}
          />

          <div className="flex-1 flex items-end gap-2 bg-gray-900 rounded-2xl border border-gray-700 p-2">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
              }}
              placeholder={`Message à ${selectedAgent?.name || 'l\'agent'}...`}
              className="flex-1 bg-transparent text-white text-sm resize-none outline-none max-h-32
                placeholder-gray-500 py-1 px-2"
              rows={1}
            />

            <VoiceControls
              onStartListening={() => setIsListening(true)}
              onStopListening={() => setIsListening(false)}
              isListening={isListening}
              onSpeak={handleSpeak}
              isSpeaking={isSpeaking}
            />

            <button
              onClick={() => sendMessage()}
              disabled={!inputValue.trim() || isLoading}
              className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                inputValue.trim()
                  ? 'bg-yellow-600 text-black hover:bg-yellow-500'
                  : 'bg-gray-800 text-gray-600 cursor-not-allowed'
              }`}
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M15 8L1 14l3-6-3-6z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentConversation;
