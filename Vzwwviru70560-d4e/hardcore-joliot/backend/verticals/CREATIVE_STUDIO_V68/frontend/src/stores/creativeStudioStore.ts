/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║              CHE·NU™ CREATIVE STUDIO — ZUSTAND STORE                         ║
 * ║                                                                              ║
 * ║  State management for Creative Studio vertical.                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface GeneratedImage {
  id: string;
  url: string;
  prompt: string;
  engine: string;
  size: string;
  style?: string;
  created_at: string;
  tokens_used: number;
  cost_usd: number;
}

export interface GeneratedAudio {
  id: string;
  url: string;
  text_preview: string;
  engine: string;
  voice_id: string;
  duration_seconds: number;
  tokens_used: number;
  cost_usd: number;
  format: string;
}

export interface ImageEngine {
  id: string;
  name: string;
  provider: string;
  cost_per_image: number;
  max_resolution: string;
  strengths: string[];
}

export interface Voice {
  id: string;
  name: string;
  voice_id: string;
}

export interface UsageStats {
  total_tokens: number;
  total_cost_usd: number;
  images: {
    total_images: number;
    total_tokens: number;
    total_cost_usd: number;
    by_engine: Record<string, { images: number; cost: number }>;
  };
  voice: {
    total_audio_seconds: number;
    total_tokens: number;
    total_cost_usd: number;
    by_engine: Record<string, { seconds: number; cost: number }>;
  };
}

export interface PromptTemplate {
  id: string;
  name: string;
  category: string;
  prompt: string;
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE INTERFACE
// ═══════════════════════════════════════════════════════════════════════════════

interface CreativeStudioState {
  // Image Generation
  imagePrompt: string;
  imageEngine: string;
  imageSize: string;
  imageStyle: string | null;
  numImages: number;
  negativePrompt: string;
  
  // Voice Generation
  voiceText: string;
  voiceEngine: string;
  voiceId: string;
  voiceStyle: string | null;
  voiceSpeed: number;
  
  // Generation State
  isGeneratingImage: boolean;
  isGeneratingVoice: boolean;
  imageError: string | null;
  voiceError: string | null;
  
  // Results
  generatedImages: GeneratedImage[];
  generatedAudios: GeneratedAudio[];
  
  // Gallery
  imageGallery: GeneratedImage[];
  voiceLibrary: GeneratedAudio[];
  
  // Config
  availableEngines: ImageEngine[];
  availableVoices: Record<string, Voice[]>;
  availableStyles: { id: string; name: string }[];
  availableSizes: { id: string; name: string; aspect: string }[];
  templates: PromptTemplate[];
  
  // Usage
  usage: UsageStats | null;
  
  // Actions - Image
  setImagePrompt: (prompt: string) => void;
  setImageEngine: (engine: string) => void;
  setImageSize: (size: string) => void;
  setImageStyle: (style: string | null) => void;
  setNumImages: (num: number) => void;
  setNegativePrompt: (prompt: string) => void;
  generateImages: () => Promise<void>;
  
  // Actions - Voice
  setVoiceText: (text: string) => void;
  setVoiceEngine: (engine: string) => void;
  setVoiceId: (id: string) => void;
  setVoiceStyle: (style: string | null) => void;
  setVoiceSpeed: (speed: number) => void;
  generateVoice: () => Promise<void>;
  
  // Actions - Data
  fetchEngines: () => Promise<void>;
  fetchVoices: () => Promise<void>;
  fetchStyles: () => Promise<void>;
  fetchSizes: () => Promise<void>;
  fetchTemplates: () => Promise<void>;
  fetchGallery: () => Promise<void>;
  fetchVoiceLibrary: () => Promise<void>;
  fetchUsage: () => Promise<void>;
  
  // Actions - Misc
  applyTemplate: (template: PromptTemplate, subject: string) => void;
  clearErrors: () => void;
  reset: () => void;
}

// ═══════════════════════════════════════════════════════════════════════════════
// API CLIENT
// ═══════════════════════════════════════════════════════════════════════════════

const API_BASE = '/api/v2/studio';

async function apiCall<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `API error: ${response.status}`);
  }
  
  return response.json();
}

// ═══════════════════════════════════════════════════════════════════════════════
// STORE
// ═══════════════════════════════════════════════════════════════════════════════

const initialState = {
  // Image Generation
  imagePrompt: '',
  imageEngine: 'dalle-3',
  imageSize: '1024x1024',
  imageStyle: null,
  numImages: 1,
  negativePrompt: '',
  
  // Voice Generation
  voiceText: '',
  voiceEngine: 'openai-tts',
  voiceId: 'alloy',
  voiceStyle: null,
  voiceSpeed: 1.0,
  
  // Generation State
  isGeneratingImage: false,
  isGeneratingVoice: false,
  imageError: null,
  voiceError: null,
  
  // Results
  generatedImages: [],
  generatedAudios: [],
  
  // Gallery
  imageGallery: [],
  voiceLibrary: [],
  
  // Config
  availableEngines: [],
  availableVoices: {},
  availableStyles: [],
  availableSizes: [],
  templates: [],
  
  // Usage
  usage: null,
};

export const useCreativeStudioStore = create<CreativeStudioState>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,
        
        // ═══════════════════════════════════════════════════════════════════════
        // IMAGE ACTIONS
        // ═══════════════════════════════════════════════════════════════════════
        
        setImagePrompt: (prompt) => set({ imagePrompt: prompt }),
        setImageEngine: (engine) => set({ imageEngine: engine }),
        setImageSize: (size) => set({ imageSize: size }),
        setImageStyle: (style) => set({ imageStyle: style }),
        setNumImages: (num) => set({ numImages: Math.min(4, Math.max(1, num)) }),
        setNegativePrompt: (prompt) => set({ negativePrompt: prompt }),
        
        generateImages: async () => {
          const state = get();
          
          if (!state.imagePrompt.trim()) {
            set({ imageError: 'Please enter a prompt' });
            return;
          }
          
          set({ isGeneratingImage: true, imageError: null });
          
          try {
            const response = await apiCall<{
              success: boolean;
              images: GeneratedImage[];
              total_tokens: number;
              total_cost: number;
            }>('/generate/image?user_id=current', {
              method: 'POST',
              body: JSON.stringify({
                prompt: state.imagePrompt,
                engine: state.imageEngine,
                size: state.imageSize,
                style: state.imageStyle,
                num_images: state.numImages,
                negative_prompt: state.negativePrompt || null,
              }),
            });
            
            if (response.success) {
              set({
                generatedImages: [...response.images, ...state.generatedImages],
                isGeneratingImage: false,
              });
              
              // Refresh gallery
              get().fetchGallery();
              get().fetchUsage();
            }
          } catch (error) {
            set({
              imageError: error instanceof Error ? error.message : 'Generation failed',
              isGeneratingImage: false,
            });
          }
        },
        
        // ═══════════════════════════════════════════════════════════════════════
        // VOICE ACTIONS
        // ═══════════════════════════════════════════════════════════════════════
        
        setVoiceText: (text) => set({ voiceText: text }),
        setVoiceEngine: (engine) => set({ voiceEngine: engine }),
        setVoiceId: (id) => set({ voiceId: id }),
        setVoiceStyle: (style) => set({ voiceStyle: style }),
        setVoiceSpeed: (speed) => set({ voiceSpeed: Math.min(4, Math.max(0.25, speed)) }),
        
        generateVoice: async () => {
          const state = get();
          
          if (!state.voiceText.trim()) {
            set({ voiceError: 'Please enter text to convert' });
            return;
          }
          
          set({ isGeneratingVoice: true, voiceError: null });
          
          try {
            const response = await apiCall<GeneratedAudio & { success: boolean }>(
              '/generate/voice?user_id=current',
              {
                method: 'POST',
                body: JSON.stringify({
                  text: state.voiceText,
                  engine: state.voiceEngine,
                  voice_id: state.voiceId,
                  style: state.voiceStyle,
                  speed: state.voiceSpeed,
                }),
              }
            );
            
            if (response.success) {
              set({
                generatedAudios: [response, ...state.generatedAudios],
                isGeneratingVoice: false,
              });
              
              get().fetchVoiceLibrary();
              get().fetchUsage();
            }
          } catch (error) {
            set({
              voiceError: error instanceof Error ? error.message : 'Generation failed',
              isGeneratingVoice: false,
            });
          }
        },
        
        // ═══════════════════════════════════════════════════════════════════════
        // DATA FETCHING
        // ═══════════════════════════════════════════════════════════════════════
        
        fetchEngines: async () => {
          try {
            const engines = await apiCall<ImageEngine[]>('/image/engines');
            set({ availableEngines: engines });
          } catch (error) {
            console.error('Failed to fetch engines:', error);
          }
        },
        
        fetchVoices: async () => {
          try {
            const voices = await apiCall<Record<string, Voice[]>>('/voice/voices');
            set({ availableVoices: voices });
          } catch (error) {
            console.error('Failed to fetch voices:', error);
          }
        },
        
        fetchStyles: async () => {
          try {
            const styles = await apiCall<{ id: string; name: string }[]>('/image/styles');
            set({ availableStyles: styles });
          } catch (error) {
            console.error('Failed to fetch styles:', error);
          }
        },
        
        fetchSizes: async () => {
          try {
            const sizes = await apiCall<{ id: string; name: string; aspect: string }[]>('/image/sizes');
            set({ availableSizes: sizes });
          } catch (error) {
            console.error('Failed to fetch sizes:', error);
          }
        },
        
        fetchTemplates: async () => {
          try {
            const templates = await apiCall<PromptTemplate[]>('/templates');
            set({ templates });
          } catch (error) {
            console.error('Failed to fetch templates:', error);
          }
        },
        
        fetchGallery: async () => {
          try {
            const response = await apiCall<{ items: GeneratedImage[] }>(
              '/image/gallery?user_id=current&limit=50'
            );
            set({ imageGallery: response.items });
          } catch (error) {
            console.error('Failed to fetch gallery:', error);
          }
        },
        
        fetchVoiceLibrary: async () => {
          try {
            const response = await apiCall<{ items: GeneratedAudio[] }>(
              '/voice/library?user_id=current&limit=50'
            );
            set({ voiceLibrary: response.items });
          } catch (error) {
            console.error('Failed to fetch voice library:', error);
          }
        },
        
        fetchUsage: async () => {
          try {
            const usage = await apiCall<UsageStats>('/usage?user_id=current');
            set({ usage });
          } catch (error) {
            console.error('Failed to fetch usage:', error);
          }
        },
        
        // ═══════════════════════════════════════════════════════════════════════
        // MISC ACTIONS
        // ═══════════════════════════════════════════════════════════════════════
        
        applyTemplate: (template, subject) => {
          const prompt = template.prompt.replace('{subject}', subject);
          set({ imagePrompt: prompt });
        },
        
        clearErrors: () => set({ imageError: null, voiceError: null }),
        
        reset: () => set(initialState),
      }),
      {
        name: 'chenu-creative-studio',
        partialize: (state) => ({
          imageEngine: state.imageEngine,
          imageSize: state.imageSize,
          voiceEngine: state.voiceEngine,
          voiceId: state.voiceId,
          voiceSpeed: state.voiceSpeed,
        }),
      }
    ),
    { name: 'CreativeStudioStore' }
  )
);

// ═══════════════════════════════════════════════════════════════════════════════
// HOOKS
// ═══════════════════════════════════════════════════════════════════════════════

export function useImageGeneration() {
  return useCreativeStudioStore((state) => ({
    prompt: state.imagePrompt,
    engine: state.imageEngine,
    size: state.imageSize,
    style: state.imageStyle,
    numImages: state.numImages,
    negativePrompt: state.negativePrompt,
    isGenerating: state.isGeneratingImage,
    error: state.imageError,
    results: state.generatedImages,
    setPrompt: state.setImagePrompt,
    setEngine: state.setImageEngine,
    setSize: state.setImageSize,
    setStyle: state.setImageStyle,
    setNumImages: state.setNumImages,
    setNegativePrompt: state.setNegativePrompt,
    generate: state.generateImages,
  }));
}

export function useVoiceGeneration() {
  return useCreativeStudioStore((state) => ({
    text: state.voiceText,
    engine: state.voiceEngine,
    voiceId: state.voiceId,
    style: state.voiceStyle,
    speed: state.voiceSpeed,
    isGenerating: state.isGeneratingVoice,
    error: state.voiceError,
    results: state.generatedAudios,
    setText: state.setVoiceText,
    setEngine: state.setVoiceEngine,
    setVoiceId: state.setVoiceId,
    setStyle: state.setVoiceStyle,
    setSpeed: state.setVoiceSpeed,
    generate: state.generateVoice,
  }));
}

export function useCreativeStudioInit() {
  const store = useCreativeStudioStore();
  
  const initialize = async () => {
    await Promise.all([
      store.fetchEngines(),
      store.fetchVoices(),
      store.fetchStyles(),
      store.fetchSizes(),
      store.fetchTemplates(),
      store.fetchGallery(),
      store.fetchVoiceLibrary(),
      store.fetchUsage(),
    ]);
  };
  
  return { initialize };
}
