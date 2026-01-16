/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║              CHE·NU™ CREATIVE STUDIO — MAIN PAGE                             ║
 * ║                                                                              ║
 * ║  COS: 94/100 — Adobe Creative Cloud Competitor                               ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import React, { useEffect, useState } from 'react';
import {
  useCreativeStudioStore,
  useImageGeneration,
  useVoiceGeneration,
  useCreativeStudioInit,
  GeneratedImage,
  GeneratedAudio,
} from '../../../stores/creativeStudioStore';

// ═══════════════════════════════════════════════════════════════════════════════
// TABS
// ═══════════════════════════════════════════════════════════════════════════════

type Tab = 'image' | 'voice' | 'gallery' | 'usage';

// ═══════════════════════════════════════════════════════════════════════════════
// IMAGE GENERATOR COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════

const ImageGenerator: React.FC = () => {
  const {
    prompt,
    engine,
    size,
    style,
    numImages,
    negativePrompt,
    isGenerating,
    error,
    results,
    setPrompt,
    setEngine,
    setSize,
    setStyle,
    setNumImages,
    setNegativePrompt,
    generate,
  } = useImageGeneration();
  
  const { availableEngines, availableStyles, availableSizes, templates, applyTemplate } =
    useCreativeStudioStore();
  
  const [templateSubject, setTemplateSubject] = useState('');
  const [showTemplates, setShowTemplates] = useState(false);

  return (
    <div className="space-y-6">
      {/* Prompt Input */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-300">
          Prompt
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe the image you want to create..."
          className="w-full h-32 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg 
                     text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 
                     focus:border-transparent resize-none"
        />
        
        {/* Quick Templates */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowTemplates(!showTemplates)}
            className="text-sm text-purple-400 hover:text-purple-300"
          >
            {showTemplates ? 'Hide Templates' : 'Use Template'}
          </button>
        </div>
        
        {showTemplates && (
          <div className="p-4 bg-gray-800/50 rounded-lg space-y-3">
            <input
              type="text"
              value={templateSubject}
              onChange={(e) => setTemplateSubject(e.target.value)}
              placeholder="Enter subject (e.g., 'a red sports car')"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded 
                         text-white text-sm placeholder-gray-500"
            />
            <div className="flex flex-wrap gap-2">
              {templates.map((t) => (
                <button
                  key={t.id}
                  onClick={() => {
                    applyTemplate(t, templateSubject || 'your subject');
                    setShowTemplates(false);
                  }}
                  className="px-3 py-1 text-xs bg-gray-700 hover:bg-gray-600 
                             rounded-full text-gray-300"
                >
                  {t.name}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Options Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Engine */}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-400">Engine</label>
          <select
            value={engine}
            onChange={(e) => setEngine(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                       text-white text-sm focus:ring-2 focus:ring-purple-500"
          >
            {availableEngines.map((e) => (
              <option key={e.id} value={e.id}>
                {e.name} (${e.cost_per_image})
              </option>
            ))}
          </select>
        </div>

        {/* Size */}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-400">Size</label>
          <select
            value={size}
            onChange={(e) => setSize(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                       text-white text-sm focus:ring-2 focus:ring-purple-500"
          >
            {availableSizes.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.aspect})
              </option>
            ))}
          </select>
        </div>

        {/* Style */}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-400">Style</label>
          <select
            value={style || ''}
            onChange={(e) => setStyle(e.target.value || null)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                       text-white text-sm focus:ring-2 focus:ring-purple-500"
          >
            <option value="">None</option>
            {availableStyles.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </div>

        {/* Count */}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-400">Images</label>
          <select
            value={numImages}
            onChange={(e) => setNumImages(Number(e.target.value))}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                       text-white text-sm focus:ring-2 focus:ring-purple-500"
          >
            <option value={1}>1 Image</option>
            <option value={2}>2 Images</option>
            <option value={3}>3 Images</option>
            <option value={4}>4 Images</option>
          </select>
        </div>
      </div>

      {/* Negative Prompt */}
      <div className="space-y-1">
        <label className="block text-xs font-medium text-gray-400">
          Negative Prompt (optional)
        </label>
        <input
          type="text"
          value={negativePrompt}
          onChange={(e) => setNegativePrompt(e.target.value)}
          placeholder="What to avoid..."
          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                     text-white text-sm placeholder-gray-500"
        />
      </div>

      {/* Generate Button */}
      <button
        onClick={generate}
        disabled={isGenerating || !prompt.trim()}
        className={`w-full py-3 rounded-lg font-semibold text-white transition-all
          ${isGenerating || !prompt.trim()
            ? 'bg-gray-700 cursor-not-allowed'
            : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500'
          }`}
      >
        {isGenerating ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            Generating...
          </span>
        ) : (
          `Generate ${numImages} Image${numImages > 1 ? 's' : ''}`
        )}
      </button>

      {/* Error */}
      {error && (
        <div className="p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-medium text-gray-300">Generated Images</h3>
          <div className="grid grid-cols-2 gap-4">
            {results.slice(0, 4).map((img) => (
              <ImageCard key={img.id} image={img} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// VOICE GENERATOR COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════

const VoiceGenerator: React.FC = () => {
  const {
    text,
    engine,
    voiceId,
    style,
    speed,
    isGenerating,
    error,
    results,
    setText,
    setEngine,
    setVoiceId,
    setStyle,
    setSpeed,
    generate,
  } = useVoiceGeneration();
  
  const { availableVoices } = useCreativeStudioStore();
  
  const voiceStyles = [
    { id: 'neutral', name: 'Neutral' },
    { id: 'happy', name: 'Happy' },
    { id: 'sad', name: 'Sad' },
    { id: 'excited', name: 'Excited' },
    { id: 'calm', name: 'Calm' },
    { id: 'professional', name: 'Professional' },
    { id: 'conversational', name: 'Conversational' },
    { id: 'narrative', name: 'Narrative' },
  ];

  const currentVoices = availableVoices[engine] || [];

  return (
    <div className="space-y-6">
      {/* Text Input */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-300">
          Text to Convert
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter the text you want to convert to speech..."
          className="w-full h-40 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg 
                     text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 
                     focus:border-transparent resize-none"
        />
        <div className="text-xs text-gray-500 text-right">
          {text.length} / 5000 characters
        </div>
      </div>

      {/* Options */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Engine */}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-400">Engine</label>
          <select
            value={engine}
            onChange={(e) => setEngine(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                       text-white text-sm"
          >
            <option value="openai-tts">OpenAI TTS ($0.015/1k)</option>
            <option value="elevenlabs">ElevenLabs ($0.30/1k)</option>
          </select>
        </div>

        {/* Voice */}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-400">Voice</label>
          <select
            value={voiceId}
            onChange={(e) => setVoiceId(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                       text-white text-sm"
          >
            {currentVoices.map((v) => (
              <option key={v.id} value={v.id}>
                {v.name}
              </option>
            ))}
          </select>
        </div>

        {/* Style */}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-400">Style</label>
          <select
            value={style || ''}
            onChange={(e) => setStyle(e.target.value || null)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                       text-white text-sm"
          >
            <option value="">Default</option>
            {voiceStyles.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </div>

        {/* Speed */}
        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-400">
            Speed ({speed.toFixed(1)}x)
          </label>
          <input
            type="range"
            min="0.25"
            max="4"
            step="0.25"
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
          />
        </div>
      </div>

      {/* Generate Button */}
      <button
        onClick={generate}
        disabled={isGenerating || !text.trim()}
        className={`w-full py-3 rounded-lg font-semibold text-white transition-all
          ${isGenerating || !text.trim()
            ? 'bg-gray-700 cursor-not-allowed'
            : 'bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500'
          }`}
      >
        {isGenerating ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            Generating...
          </span>
        ) : (
          'Generate Voice'
        )}
      </button>

      {/* Error */}
      {error && (
        <div className="p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-medium text-gray-300">Generated Audio</h3>
          <div className="space-y-3">
            {results.slice(0, 3).map((audio) => (
              <AudioCard key={audio.id} audio={audio} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// GALLERY COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════

const Gallery: React.FC = () => {
  const { imageGallery, voiceLibrary } = useCreativeStudioStore();
  const [activeTab, setActiveTab] = useState<'images' | 'audio'>('images');

  return (
    <div className="space-y-4">
      {/* Tabs */}
      <div className="flex gap-2">
        <button
          onClick={() => setActiveTab('images')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors
            ${activeTab === 'images'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
        >
          Images ({imageGallery.length})
        </button>
        <button
          onClick={() => setActiveTab('audio')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors
            ${activeTab === 'audio'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
        >
          Audio ({voiceLibrary.length})
        </button>
      </div>

      {/* Content */}
      {activeTab === 'images' ? (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {imageGallery.length === 0 ? (
            <div className="col-span-full text-center py-12 text-gray-500">
              No images yet. Generate some!
            </div>
          ) : (
            imageGallery.map((img) => (
              <ImageCard key={img.id} image={img} />
            ))
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {voiceLibrary.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              No audio yet. Generate some!
            </div>
          ) : (
            voiceLibrary.map((audio) => (
              <AudioCard key={audio.id} audio={audio} />
            ))
          )}
        </div>
      )}
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// USAGE COMPONENT
// ═══════════════════════════════════════════════════════════════════════════════

const UsageStats: React.FC = () => {
  const { usage } = useCreativeStudioStore();

  if (!usage) {
    return (
      <div className="text-center py-12 text-gray-500">
        Loading usage data...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="Total Tokens"
          value={usage.total_tokens.toLocaleString()}
          icon="🎯"
        />
        <StatCard
          label="Total Cost"
          value={`$${usage.total_cost_usd.toFixed(2)}`}
          icon="💰"
        />
        <StatCard
          label="Images Generated"
          value={usage.images?.total_images?.toString() || '0'}
          icon="🖼️"
        />
        <StatCard
          label="Audio Seconds"
          value={`${(usage.voice?.total_audio_seconds || 0).toFixed(1)}s`}
          icon="🎙️"
        />
      </div>

      {/* Breakdown */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Image Usage */}
        <div className="p-4 bg-gray-800/50 rounded-lg">
          <h3 className="text-sm font-semibold text-gray-300 mb-3">Image Generation</h3>
          {Object.entries(usage.images?.by_engine || {}).length === 0 ? (
            <p className="text-sm text-gray-500">No image usage yet</p>
          ) : (
            <div className="space-y-2">
              {Object.entries(usage.images?.by_engine || {}).map(([engine, data]) => (
                <div key={engine} className="flex justify-between text-sm">
                  <span className="text-gray-400">{engine}</span>
                  <span className="text-gray-300">
                    {data.images} images (${data.cost.toFixed(2)})
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Voice Usage */}
        <div className="p-4 bg-gray-800/50 rounded-lg">
          <h3 className="text-sm font-semibold text-gray-300 mb-3">Voice Synthesis</h3>
          {Object.entries(usage.voice?.by_engine || {}).length === 0 ? (
            <p className="text-sm text-gray-500">No voice usage yet</p>
          ) : (
            <div className="space-y-2">
              {Object.entries(usage.voice?.by_engine || {}).map(([engine, data]) => (
                <div key={engine} className="flex justify-between text-sm">
                  <span className="text-gray-400">{engine}</span>
                  <span className="text-gray-300">
                    {data.seconds.toFixed(1)}s (${data.cost.toFixed(2)})
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════════════════════════
// HELPER COMPONENTS
// ═══════════════════════════════════════════════════════════════════════════════

const ImageCard: React.FC<{ image: GeneratedImage }> = ({ image }) => (
  <div className="group relative rounded-lg overflow-hidden bg-gray-800">
    <img
      src={image.url}
      alt={image.prompt}
      className="w-full aspect-square object-cover"
    />
    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent 
                    opacity-0 group-hover:opacity-100 transition-opacity">
      <div className="absolute bottom-0 left-0 right-0 p-3">
        <p className="text-xs text-white line-clamp-2">{image.prompt}</p>
        <div className="flex items-center gap-2 mt-1 text-xs text-gray-400">
          <span>{image.engine}</span>
          <span>•</span>
          <span>{image.size}</span>
        </div>
      </div>
    </div>
  </div>
);

const AudioCard: React.FC<{ audio: GeneratedAudio }> = ({ audio }) => (
  <div className="p-4 bg-gray-800 rounded-lg">
    <div className="flex items-start gap-4">
      <div className="flex-shrink-0 w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center">
        <span className="text-2xl">🎙️</span>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm text-gray-300 line-clamp-2">{audio.text_preview}</p>
        <div className="flex items-center gap-2 mt-1 text-xs text-gray-500">
          <span>{audio.engine}</span>
          <span>•</span>
          <span>{audio.voice_id}</span>
          <span>•</span>
          <span>{audio.duration_seconds.toFixed(1)}s</span>
        </div>
      </div>
      <audio controls className="flex-shrink-0 h-8">
        <source src={audio.url} type={`audio/${audio.format}`} />
      </audio>
    </div>
  </div>
);

const StatCard: React.FC<{ label: string; value: string; icon: string }> = ({
  label,
  value,
  icon,
}) => (
  <div className="p-4 bg-gray-800/50 rounded-lg">
    <div className="flex items-center gap-3">
      <span className="text-2xl">{icon}</span>
      <div>
        <p className="text-xs text-gray-500">{label}</p>
        <p className="text-lg font-semibold text-white">{value}</p>
      </div>
    </div>
  </div>
);

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN PAGE
// ═══════════════════════════════════════════════════════════════════════════════

export const CreativeStudioPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('image');
  const { initialize } = useCreativeStudioInit();

  useEffect(() => {
    initialize();
  }, []);

  const tabs: { id: Tab; label: string; icon: string }[] = [
    { id: 'image', label: 'Image', icon: '🖼️' },
    { id: 'voice', label: 'Voice', icon: '🎙️' },
    { id: 'gallery', label: 'Gallery', icon: '📁' },
    { id: 'usage', label: 'Usage', icon: '📊' },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 
                             bg-clip-text text-transparent">
                Creative Studio
              </h1>
              <p className="text-sm text-gray-500 mt-1">
                Multi-engine AI creative tools • COS 94/100
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 text-xs bg-purple-600/20 text-purple-400 rounded-full">
                V68
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <nav className="border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex gap-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 text-sm font-medium transition-colors relative
                  ${activeTab === tab.id
                    ? 'text-white'
                    : 'text-gray-500 hover:text-gray-300'
                  }`}
              >
                <span className="flex items-center gap-2">
                  <span>{tab.icon}</span>
                  {tab.label}
                </span>
                {activeTab === tab.id && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-500" />
                )}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {activeTab === 'image' && <ImageGenerator />}
        {activeTab === 'voice' && <VoiceGenerator />}
        {activeTab === 'gallery' && <Gallery />}
        {activeTab === 'usage' && <UsageStats />}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 mt-auto">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          CHE·NU™ Creative Studio • Competing with Adobe Creative Cloud
        </div>
      </footer>
    </div>
  );
};

export default CreativeStudioPage;
