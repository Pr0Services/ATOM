"""
LLM ROUTER
==========

Multi-provider LLM routing system for CHE·NU.
Supports 18+ LLM providers with intelligent routing, fallback, and cost tracking.

Features:
- Multi-provider support (Anthropic, OpenAI, Google, Mistral, etc.)
- Intelligent routing based on task type and requirements
- Automatic fallback on provider failure
- Token budget enforcement per identity/Thread
- Cost tracking per request and per provider
- Rate limiting per provider

R&D COMPLIANCE:
- Rule #1: LLM outputs are drafts - human gates for sensitive actions
- Rule #2: All execution in sandbox mode
- Rule #6: Complete traceability of all LLM calls

VERSION: 1.0.0
"""

from typing import Dict, Any, Optional, List, Callable, Tuple
from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from decimal import Decimal
import asyncio
import logging
import time

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS & CONSTANTS
# =============================================================================

class LLMProvider(str, Enum):
    """Supported LLM providers"""
    # Primary providers
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    MISTRAL = "mistral"
    
    # Additional providers
    COHERE = "cohere"
    REPLICATE = "replicate"
    TOGETHER = "together"
    GROQ = "groq"
    PERPLEXITY = "perplexity"
    DEEPSEEK = "deepseek"
    ANYSCALE = "anyscale"
    FIREWORKS = "fireworks"
    
    # Open source / Local
    OLLAMA = "ollama"
    VLLM = "vllm"
    LMSTUDIO = "lmstudio"
    
    # Specialized
    ELEVENLABS = "elevenlabs"  # Voice
    STABILITY = "stability"    # Image
    RUNWAY = "runway"          # Video


class TaskType(str, Enum):
    """Types of LLM tasks"""
    # Text generation
    CHAT = "chat"
    COMPLETION = "completion"
    SUMMARIZATION = "summarization"
    ANALYSIS = "analysis"
    
    # Code
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    CODE_EXPLANATION = "code_explanation"
    
    # Creative
    CREATIVE_WRITING = "creative_writing"
    BRAINSTORMING = "brainstorming"
    
    # Structured
    EXTRACTION = "extraction"
    CLASSIFICATION = "classification"
    STRUCTURED_OUTPUT = "structured_output"
    
    # Specialized
    TRANSLATION = "translation"
    REASONING = "reasoning"
    MATH = "math"
    
    # Multimodal
    VISION = "vision"
    VOICE_TO_TEXT = "voice_to_text"
    TEXT_TO_VOICE = "text_to_voice"
    IMAGE_GENERATION = "image_generation"


class RoutingStrategy(str, Enum):
    """Routing strategies"""
    COST_OPTIMIZED = "cost_optimized"       # Cheapest provider
    QUALITY_OPTIMIZED = "quality_optimized"  # Best quality
    SPEED_OPTIMIZED = "speed_optimized"      # Fastest
    BALANCED = "balanced"                    # Balance all
    SPECIFIC = "specific"                    # Use specific provider


# =============================================================================
# MODELS
# =============================================================================

@dataclass
class ProviderConfig:
    """Configuration for an LLM provider"""
    provider: LLMProvider
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    models: List[str] = field(default_factory=list)
    is_available: bool = True
    priority: int = 1  # Lower is higher priority
    max_retries: int = 3
    timeout_seconds: int = 60
    rate_limit_rpm: int = 60
    rate_limit_tpm: int = 100000
    
    # Cost per 1K tokens (in USD)
    cost_per_1k_input: Decimal = Decimal("0.0")
    cost_per_1k_output: Decimal = Decimal("0.0")
    
    # Capabilities
    supports_vision: bool = False
    supports_streaming: bool = True
    supports_function_calling: bool = False
    max_context_length: int = 4096
    
    # Health tracking
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    consecutive_failures: int = 0


@dataclass
class ModelSpec:
    """Specification for a specific model"""
    model_id: str
    provider: LLMProvider
    display_name: str
    
    # Capabilities
    max_context_length: int = 4096
    max_output_tokens: int = 4096
    supports_vision: bool = False
    supports_streaming: bool = True
    supports_function_calling: bool = False
    supports_json_mode: bool = False
    
    # Performance
    tokens_per_second: int = 50  # Estimated
    quality_score: int = 80     # 0-100
    
    # Cost per 1K tokens (USD)
    cost_per_1k_input: Decimal = Decimal("0.0")
    cost_per_1k_output: Decimal = Decimal("0.0")
    
    # Best for
    best_for: List[TaskType] = field(default_factory=list)


class LLMRequest(BaseModel):
    """Request to LLM Router"""
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    
    # Content
    messages: List[Dict[str, Any]]
    system_prompt: Optional[str] = None
    
    # Task info
    task_type: TaskType = TaskType.CHAT
    
    # Routing preferences
    strategy: RoutingStrategy = RoutingStrategy.BALANCED
    preferred_provider: Optional[LLMProvider] = None
    preferred_model: Optional[str] = None
    
    # Requirements
    max_tokens: int = 1024
    temperature: float = 0.7
    requires_vision: bool = False
    requires_function_calling: bool = False
    requires_json_output: bool = False
    
    # Budget
    max_cost_usd: Optional[Decimal] = None
    
    # Identity for budget tracking
    identity_id: str
    thread_id: Optional[str] = None
    sphere_id: Optional[str] = None
    
    # Streaming
    stream: bool = False
    
    class Config:
        arbitrary_types_allowed = True


@dataclass
class LLMResponse:
    """Response from LLM Router"""
    request_id: str
    
    # Content
    content: str
    finish_reason: str
    
    # Provider info
    provider: LLMProvider
    model: str
    
    # Usage
    input_tokens: int
    output_tokens: int
    total_tokens: int
    
    # Cost
    cost_usd: Decimal
    
    # Performance
    latency_ms: int
    tokens_per_second: float
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # Raw response for debugging
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TokenBudget:
    """Token budget for an identity/Thread"""
    identity_id: str
    thread_id: Optional[str] = None
    
    # Limits
    daily_limit: int = 100000
    monthly_limit: int = 1000000
    
    # Usage
    daily_used: int = 0
    monthly_used: int = 0
    
    # Cost
    daily_cost_limit: Decimal = Decimal("10.0")
    monthly_cost_limit: Decimal = Decimal("100.0")
    daily_cost_used: Decimal = Decimal("0.0")
    monthly_cost_used: Decimal = Decimal("0.0")
    
    # Period tracking
    daily_reset_at: datetime = field(default_factory=datetime.utcnow)
    monthly_reset_at: datetime = field(default_factory=datetime.utcnow)


# =============================================================================
# MODEL REGISTRY
# =============================================================================

# Pre-configured models with their specs
MODEL_REGISTRY: Dict[str, ModelSpec] = {
    # Anthropic Claude
    "claude-3-5-sonnet-20241022": ModelSpec(
        model_id="claude-3-5-sonnet-20241022",
        provider=LLMProvider.ANTHROPIC,
        display_name="Claude 3.5 Sonnet",
        max_context_length=200000,
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=80,
        quality_score=95,
        cost_per_1k_input=Decimal("0.003"),
        cost_per_1k_output=Decimal("0.015"),
        best_for=[TaskType.ANALYSIS, TaskType.CODE_GENERATION, TaskType.REASONING]
    ),
    "claude-3-5-haiku-20241022": ModelSpec(
        model_id="claude-3-5-haiku-20241022",
        provider=LLMProvider.ANTHROPIC,
        display_name="Claude 3.5 Haiku",
        max_context_length=200000,
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=150,
        quality_score=85,
        cost_per_1k_input=Decimal("0.00025"),
        cost_per_1k_output=Decimal("0.00125"),
        best_for=[TaskType.CHAT, TaskType.SUMMARIZATION, TaskType.EXTRACTION]
    ),
    
    # OpenAI GPT
    "gpt-4o": ModelSpec(
        model_id="gpt-4o",
        provider=LLMProvider.OPENAI,
        display_name="GPT-4o",
        max_context_length=128000,
        max_output_tokens=16384,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=70,
        quality_score=93,
        cost_per_1k_input=Decimal("0.0025"),
        cost_per_1k_output=Decimal("0.01"),
        best_for=[TaskType.ANALYSIS, TaskType.VISION, TaskType.STRUCTURED_OUTPUT]
    ),
    "gpt-4o-mini": ModelSpec(
        model_id="gpt-4o-mini",
        provider=LLMProvider.OPENAI,
        display_name="GPT-4o Mini",
        max_context_length=128000,
        max_output_tokens=16384,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=120,
        quality_score=85,
        cost_per_1k_input=Decimal("0.00015"),
        cost_per_1k_output=Decimal("0.0006"),
        best_for=[TaskType.CHAT, TaskType.CLASSIFICATION, TaskType.EXTRACTION]
    ),
    "o1": ModelSpec(
        model_id="o1",
        provider=LLMProvider.OPENAI,
        display_name="o1 (Reasoning)",
        max_context_length=200000,
        max_output_tokens=100000,
        supports_vision=True,
        supports_function_calling=False,
        supports_json_mode=False,
        tokens_per_second=30,
        quality_score=98,
        cost_per_1k_input=Decimal("0.015"),
        cost_per_1k_output=Decimal("0.06"),
        best_for=[TaskType.REASONING, TaskType.MATH, TaskType.CODE_GENERATION]
    ),
    
    # Google Gemini
    "gemini-2.0-flash-exp": ModelSpec(
        model_id="gemini-2.0-flash-exp",
        provider=LLMProvider.GOOGLE,
        display_name="Gemini 2.0 Flash",
        max_context_length=1000000,
        max_output_tokens=8192,
        supports_vision=True,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=200,
        quality_score=90,
        cost_per_1k_input=Decimal("0.0"),
        cost_per_1k_output=Decimal("0.0"),
        best_for=[TaskType.CHAT, TaskType.VISION, TaskType.SUMMARIZATION]
    ),
    
    # Mistral
    "mistral-large-latest": ModelSpec(
        model_id="mistral-large-latest",
        provider=LLMProvider.MISTRAL,
        display_name="Mistral Large",
        max_context_length=128000,
        max_output_tokens=8192,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=80,
        quality_score=88,
        cost_per_1k_input=Decimal("0.002"),
        cost_per_1k_output=Decimal("0.006"),
        best_for=[TaskType.CODE_GENERATION, TaskType.ANALYSIS]
    ),
    "codestral-latest": ModelSpec(
        model_id="codestral-latest",
        provider=LLMProvider.MISTRAL,
        display_name="Codestral",
        max_context_length=32000,
        max_output_tokens=8192,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=100,
        quality_score=92,
        cost_per_1k_input=Decimal("0.001"),
        cost_per_1k_output=Decimal("0.003"),
        best_for=[TaskType.CODE_GENERATION, TaskType.CODE_REVIEW, TaskType.CODE_EXPLANATION]
    ),
    
    # Groq (fast inference)
    "llama-3.3-70b-versatile": ModelSpec(
        model_id="llama-3.3-70b-versatile",
        provider=LLMProvider.GROQ,
        display_name="Llama 3.3 70B (Groq)",
        max_context_length=128000,
        max_output_tokens=8192,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=500,  # Groq is very fast
        quality_score=88,
        cost_per_1k_input=Decimal("0.00059"),
        cost_per_1k_output=Decimal("0.00079"),
        best_for=[TaskType.CHAT, TaskType.SUMMARIZATION]
    ),
    
    # DeepSeek
    "deepseek-chat": ModelSpec(
        model_id="deepseek-chat",
        provider=LLMProvider.DEEPSEEK,
        display_name="DeepSeek V3",
        max_context_length=64000,
        max_output_tokens=8192,
        supports_vision=False,
        supports_function_calling=True,
        supports_json_mode=True,
        tokens_per_second=60,
        quality_score=90,
        cost_per_1k_input=Decimal("0.00027"),
        cost_per_1k_output=Decimal("0.0011"),
        best_for=[TaskType.CODE_GENERATION, TaskType.REASONING, TaskType.MATH]
    ),
    
    # Perplexity (search-augmented)
    "sonar-pro": ModelSpec(
        model_id="sonar-pro",
        provider=LLMProvider.PERPLEXITY,
        display_name="Sonar Pro",
        max_context_length=200000,
        max_output_tokens=8192,
        supports_vision=False,
        supports_function_calling=False,
        supports_json_mode=False,
        tokens_per_second=50,
        quality_score=85,
        cost_per_1k_input=Decimal("0.003"),
        cost_per_1k_output=Decimal("0.015"),
        best_for=[TaskType.ANALYSIS]  # Good for research with web search
    ),
    
    # Local (Ollama)
    "llama3.2:latest": ModelSpec(
        model_id="llama3.2:latest",
        provider=LLMProvider.OLLAMA,
        display_name="Llama 3.2 (Local)",
        max_context_length=128000,
        max_output_tokens=4096,
        supports_vision=True,
        supports_function_calling=False,
        supports_json_mode=True,
        tokens_per_second=20,  # Depends on hardware
        quality_score=82,
        cost_per_1k_input=Decimal("0.0"),  # Free (local)
        cost_per_1k_output=Decimal("0.0"),
        best_for=[TaskType.CHAT]
    ),
}


# Task to provider recommendations
TASK_PROVIDER_RECOMMENDATIONS: Dict[TaskType, List[str]] = {
    TaskType.CHAT: ["claude-3-5-haiku-20241022", "gpt-4o-mini", "llama-3.3-70b-versatile"],
    TaskType.ANALYSIS: ["claude-3-5-sonnet-20241022", "gpt-4o", "gemini-2.0-flash-exp"],
    TaskType.CODE_GENERATION: ["claude-3-5-sonnet-20241022", "codestral-latest", "deepseek-chat"],
    TaskType.CODE_REVIEW: ["claude-3-5-sonnet-20241022", "codestral-latest"],
    TaskType.REASONING: ["o1", "claude-3-5-sonnet-20241022", "deepseek-chat"],
    TaskType.MATH: ["o1", "deepseek-chat", "claude-3-5-sonnet-20241022"],
    TaskType.VISION: ["gpt-4o", "claude-3-5-sonnet-20241022", "gemini-2.0-flash-exp"],
    TaskType.SUMMARIZATION: ["claude-3-5-haiku-20241022", "gemini-2.0-flash-exp", "llama-3.3-70b-versatile"],
    TaskType.EXTRACTION: ["gpt-4o-mini", "claude-3-5-haiku-20241022"],
    TaskType.STRUCTURED_OUTPUT: ["gpt-4o", "claude-3-5-sonnet-20241022"],
    TaskType.CREATIVE_WRITING: ["claude-3-5-sonnet-20241022", "gpt-4o"],
}


# =============================================================================
# LLM ROUTER SERVICE
# =============================================================================

class LLMRouter:
    """
    Multi-provider LLM router with intelligent routing and fallback.
    
    Features:
    - Route requests to best provider based on task type
    - Automatic fallback on failure
    - Token budget enforcement
    - Cost tracking
    - Rate limiting
    """
    
    def __init__(self):
        # Provider configurations
        self._providers: Dict[LLMProvider, ProviderConfig] = {}
        
        # Token budgets per identity
        self._budgets: Dict[str, TokenBudget] = {}
        
        # Request history for analytics
        self._request_history: List[Dict[str, Any]] = []
        
        # Stats
        self._stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost_usd": Decimal("0.0"),
            "requests_per_provider": {},
            "failures_per_provider": {},
        }
        
        # Rate limiting trackers
        self._rate_limiters: Dict[LLMProvider, Dict[str, Any]] = {}
        
        logger.info("LLMRouter initialized")
    
    # -------------------------------------------------------------------------
    # CONFIGURATION
    # -------------------------------------------------------------------------
    
    def register_provider(self, config: ProviderConfig):
        """Register a provider configuration"""
        self._providers[config.provider] = config
        self._rate_limiters[config.provider] = {
            "requests_this_minute": 0,
            "tokens_this_minute": 0,
            "minute_start": time.time()
        }
        logger.info(f"Registered provider: {config.provider.value}")
    
    def get_available_providers(self) -> List[LLMProvider]:
        """Get list of available providers"""
        return [p for p, c in self._providers.items() if c.is_available]
    
    def get_provider_config(self, provider: LLMProvider) -> Optional[ProviderConfig]:
        """Get provider configuration"""
        return self._providers.get(provider)
    
    # -------------------------------------------------------------------------
    # ROUTING
    # -------------------------------------------------------------------------
    
    def select_model(self, request: LLMRequest) -> Tuple[str, LLMProvider]:
        """
        Select the best model for a request.
        
        Returns:
            Tuple of (model_id, provider)
        """
        # If specific model requested, use it
        if request.preferred_model and request.preferred_model in MODEL_REGISTRY:
            model = MODEL_REGISTRY[request.preferred_model]
            if self._is_provider_available(model.provider):
                return model.model_id, model.provider
        
        # If specific provider requested, find best model from that provider
        if request.preferred_provider:
            model_id = self._find_best_model_for_provider(
                request.preferred_provider,
                request
            )
            if model_id:
                return model_id, request.preferred_provider
        
        # Route based on strategy
        if request.strategy == RoutingStrategy.COST_OPTIMIZED:
            return self._select_cheapest_model(request)
        elif request.strategy == RoutingStrategy.QUALITY_OPTIMIZED:
            return self._select_best_quality_model(request)
        elif request.strategy == RoutingStrategy.SPEED_OPTIMIZED:
            return self._select_fastest_model(request)
        else:  # BALANCED
            return self._select_balanced_model(request)
    
    def _select_cheapest_model(self, request: LLMRequest) -> Tuple[str, LLMProvider]:
        """Select cheapest model meeting requirements"""
        candidates = self._get_candidate_models(request)
        
        if not candidates:
            # Fallback to default
            return "claude-3-5-haiku-20241022", LLMProvider.ANTHROPIC
        
        # Sort by cost
        candidates.sort(
            key=lambda m: float(m.cost_per_1k_input + m.cost_per_1k_output)
        )
        
        return candidates[0].model_id, candidates[0].provider
    
    def _select_best_quality_model(self, request: LLMRequest) -> Tuple[str, LLMProvider]:
        """Select highest quality model"""
        candidates = self._get_candidate_models(request)
        
        if not candidates:
            return "claude-3-5-sonnet-20241022", LLMProvider.ANTHROPIC
        
        # Sort by quality
        candidates.sort(key=lambda m: m.quality_score, reverse=True)
        
        return candidates[0].model_id, candidates[0].provider
    
    def _select_fastest_model(self, request: LLMRequest) -> Tuple[str, LLMProvider]:
        """Select fastest model"""
        candidates = self._get_candidate_models(request)
        
        if not candidates:
            return "llama-3.3-70b-versatile", LLMProvider.GROQ
        
        # Sort by speed
        candidates.sort(key=lambda m: m.tokens_per_second, reverse=True)
        
        return candidates[0].model_id, candidates[0].provider
    
    def _select_balanced_model(self, request: LLMRequest) -> Tuple[str, LLMProvider]:
        """Select balanced model considering quality, cost, and speed"""
        candidates = self._get_candidate_models(request)
        
        if not candidates:
            return "claude-3-5-sonnet-20241022", LLMProvider.ANTHROPIC
        
        # Score each model (normalized)
        max_quality = max(m.quality_score for m in candidates)
        max_speed = max(m.tokens_per_second for m in candidates)
        min_cost = min(float(m.cost_per_1k_input + m.cost_per_1k_output) for m in candidates)
        
        def score_model(m: ModelSpec) -> float:
            quality_score = m.quality_score / max_quality if max_quality > 0 else 0
            speed_score = m.tokens_per_second / max_speed if max_speed > 0 else 0
            cost = float(m.cost_per_1k_input + m.cost_per_1k_output)
            cost_score = min_cost / cost if cost > 0 else 1.0
            
            # Weights: 40% quality, 30% speed, 30% cost
            return 0.4 * quality_score + 0.3 * speed_score + 0.3 * cost_score
        
        candidates.sort(key=score_model, reverse=True)
        
        return candidates[0].model_id, candidates[0].provider
    
    def _get_candidate_models(self, request: LLMRequest) -> List[ModelSpec]:
        """Get models that meet request requirements"""
        candidates = []
        
        # Start with task recommendations
        task_models = TASK_PROVIDER_RECOMMENDATIONS.get(request.task_type, [])
        
        for model_id in task_models:
            if model_id not in MODEL_REGISTRY:
                continue
                
            model = MODEL_REGISTRY[model_id]
            
            # Check if provider is available
            if not self._is_provider_available(model.provider):
                continue
            
            # Check requirements
            if request.requires_vision and not model.supports_vision:
                continue
            if request.requires_function_calling and not model.supports_function_calling:
                continue
            if request.requires_json_output and not model.supports_json_mode:
                continue
            if request.max_tokens > model.max_output_tokens:
                continue
            
            # Check cost budget
            if request.max_cost_usd:
                estimated_cost = self._estimate_cost(
                    model,
                    input_tokens=1000,  # Rough estimate
                    output_tokens=request.max_tokens
                )
                if estimated_cost > request.max_cost_usd:
                    continue
            
            candidates.append(model)
        
        # If no task recommendations match, try all models
        if not candidates:
            for model in MODEL_REGISTRY.values():
                if not self._is_provider_available(model.provider):
                    continue
                if request.requires_vision and not model.supports_vision:
                    continue
                if request.requires_function_calling and not model.supports_function_calling:
                    continue
                candidates.append(model)
        
        return candidates
    
    def _find_best_model_for_provider(
        self, 
        provider: LLMProvider, 
        request: LLMRequest
    ) -> Optional[str]:
        """Find best model for a specific provider"""
        provider_models = [
            m for m in MODEL_REGISTRY.values() 
            if m.provider == provider
        ]
        
        # Filter by requirements
        valid_models = []
        for model in provider_models:
            if request.requires_vision and not model.supports_vision:
                continue
            if request.requires_function_calling and not model.supports_function_calling:
                continue
            valid_models.append(model)
        
        if not valid_models:
            return None
        
        # Return best quality
        valid_models.sort(key=lambda m: m.quality_score, reverse=True)
        return valid_models[0].model_id
    
    def _is_provider_available(self, provider: LLMProvider) -> bool:
        """Check if provider is available"""
        config = self._providers.get(provider)
        if not config:
            return False
        
        if not config.is_available:
            return False
        
        # Check consecutive failures
        if config.consecutive_failures >= config.max_retries:
            # Check if enough time has passed to retry
            if config.last_failure:
                cooldown = config.consecutive_failures * 60  # Progressive cooldown
                if (datetime.utcnow() - config.last_failure).seconds < cooldown:
                    return False
        
        return True
    
    # -------------------------------------------------------------------------
    # EXECUTION
    # -------------------------------------------------------------------------
    
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """
        Execute an LLM completion request.
        
        Handles routing, fallback, budget, and cost tracking.
        """
        start_time = time.time()
        
        # Check budget
        if not self._check_budget(request.identity_id, request.thread_id):
            raise BudgetExceededError(
                f"Token budget exceeded for identity {request.identity_id}"
            )
        
        # Select model
        model_id, provider = self.select_model(request)
        
        # Get model spec
        model_spec = MODEL_REGISTRY.get(model_id)
        if not model_spec:
            raise ModelNotFoundError(f"Model not found: {model_id}")
        
        # Check rate limit
        if not self._check_rate_limit(provider):
            # Try fallback provider
            fallback = self._get_fallback_provider(request, exclude=[provider])
            if fallback:
                model_id, provider = fallback
            else:
                raise RateLimitExceededError(f"Rate limit exceeded for {provider.value}")
        
        # Execute with retry and fallback
        last_error = None
        attempted_providers = set()
        
        while len(attempted_providers) < len(self._providers):
            attempted_providers.add(provider)
            
            try:
                response = await self._execute_completion(
                    request=request,
                    model_id=model_id,
                    provider=provider,
                    model_spec=model_spec
                )
                
                # Success - update stats and return
                self._record_success(provider, response)
                self._update_budget(
                    request.identity_id,
                    request.thread_id,
                    response.total_tokens,
                    response.cost_usd
                )
                
                # Track request
                self._stats["total_requests"] += 1
                self._stats["total_tokens"] += response.total_tokens
                self._stats["total_cost_usd"] += response.cost_usd
                
                response.latency_ms = int((time.time() - start_time) * 1000)
                
                return response
                
            except Exception as e:
                logger.warning(f"Provider {provider.value} failed: {e}")
                self._record_failure(provider)
                last_error = e
                
                # Try fallback
                fallback = self._get_fallback_provider(request, exclude=attempted_providers)
                if fallback:
                    model_id, provider = fallback
                    model_spec = MODEL_REGISTRY.get(model_id)
                else:
                    break
        
        # All providers failed
        raise LLMRouterError(f"All providers failed. Last error: {last_error}")
    
    async def _execute_completion(
        self,
        request: LLMRequest,
        model_id: str,
        provider: LLMProvider,
        model_spec: ModelSpec
    ) -> LLMResponse:
        """
        Execute completion with a specific provider.
        
        This is a mock implementation. In production, this would
        call the actual provider APIs.
        """
        # Mock implementation
        # In production, this would use httpx to call provider APIs
        
        # Simulate some processing time
        await asyncio.sleep(0.1)
        
        # Mock response
        input_tokens = sum(len(m.get("content", "").split()) * 1.3 for m in request.messages)
        output_tokens = min(request.max_tokens, 500)  # Mock output
        
        cost = self._estimate_cost(model_spec, int(input_tokens), output_tokens)
        
        return LLMResponse(
            request_id=request.request_id,
            content=f"[Mock response from {model_id}] This is a simulated response.",
            finish_reason="stop",
            provider=provider,
            model=model_id,
            input_tokens=int(input_tokens),
            output_tokens=output_tokens,
            total_tokens=int(input_tokens) + output_tokens,
            cost_usd=cost,
            latency_ms=100,
            tokens_per_second=model_spec.tokens_per_second
        )
    
    def _get_fallback_provider(
        self, 
        request: LLMRequest,
        exclude: set
    ) -> Optional[Tuple[str, LLMProvider]]:
        """Get a fallback provider that wasn't tried yet"""
        candidates = self._get_candidate_models(request)
        
        for model in candidates:
            if model.provider not in exclude and self._is_provider_available(model.provider):
                return model.model_id, model.provider
        
        return None
    
    # -------------------------------------------------------------------------
    # BUDGET MANAGEMENT
    # -------------------------------------------------------------------------
    
    def _check_budget(
        self, 
        identity_id: str, 
        thread_id: Optional[str]
    ) -> bool:
        """Check if identity has available budget"""
        budget = self._budgets.get(identity_id)
        
        if not budget:
            # Create default budget
            budget = TokenBudget(identity_id=identity_id, thread_id=thread_id)
            self._budgets[identity_id] = budget
        
        # Check if we need to reset
        now = datetime.utcnow()
        if (now - budget.daily_reset_at).days >= 1:
            budget.daily_used = 0
            budget.daily_cost_used = Decimal("0.0")
            budget.daily_reset_at = now
        
        if (now - budget.monthly_reset_at).days >= 30:
            budget.monthly_used = 0
            budget.monthly_cost_used = Decimal("0.0")
            budget.monthly_reset_at = now
        
        # Check limits
        if budget.daily_used >= budget.daily_limit:
            return False
        if budget.monthly_used >= budget.monthly_limit:
            return False
        if budget.daily_cost_used >= budget.daily_cost_limit:
            return False
        if budget.monthly_cost_used >= budget.monthly_cost_limit:
            return False
        
        return True
    
    def _update_budget(
        self,
        identity_id: str,
        thread_id: Optional[str],
        tokens: int,
        cost: Decimal
    ):
        """Update budget usage"""
        budget = self._budgets.get(identity_id)
        if budget:
            budget.daily_used += tokens
            budget.monthly_used += tokens
            budget.daily_cost_used += cost
            budget.monthly_cost_used += cost
    
    def get_budget(self, identity_id: str) -> Optional[TokenBudget]:
        """Get budget for an identity"""
        return self._budgets.get(identity_id)
    
    def set_budget_limits(
        self,
        identity_id: str,
        daily_limit: Optional[int] = None,
        monthly_limit: Optional[int] = None,
        daily_cost_limit: Optional[Decimal] = None,
        monthly_cost_limit: Optional[Decimal] = None
    ):
        """Set budget limits for an identity"""
        budget = self._budgets.get(identity_id)
        if not budget:
            budget = TokenBudget(identity_id=identity_id)
            self._budgets[identity_id] = budget
        
        if daily_limit is not None:
            budget.daily_limit = daily_limit
        if monthly_limit is not None:
            budget.monthly_limit = monthly_limit
        if daily_cost_limit is not None:
            budget.daily_cost_limit = daily_cost_limit
        if monthly_cost_limit is not None:
            budget.monthly_cost_limit = monthly_cost_limit
    
    # -------------------------------------------------------------------------
    # RATE LIMITING
    # -------------------------------------------------------------------------
    
    def _check_rate_limit(self, provider: LLMProvider) -> bool:
        """Check if provider is within rate limits"""
        limiter = self._rate_limiters.get(provider)
        if not limiter:
            return True
        
        config = self._providers.get(provider)
        if not config:
            return True
        
        now = time.time()
        
        # Reset if minute has passed
        if now - limiter["minute_start"] >= 60:
            limiter["requests_this_minute"] = 0
            limiter["tokens_this_minute"] = 0
            limiter["minute_start"] = now
        
        # Check limits
        if limiter["requests_this_minute"] >= config.rate_limit_rpm:
            return False
        if limiter["tokens_this_minute"] >= config.rate_limit_tpm:
            return False
        
        # Increment
        limiter["requests_this_minute"] += 1
        
        return True
    
    # -------------------------------------------------------------------------
    # HEALTH & STATS
    # -------------------------------------------------------------------------
    
    def _record_success(self, provider: LLMProvider, response: LLMResponse):
        """Record successful request"""
        config = self._providers.get(provider)
        if config:
            config.last_success = datetime.utcnow()
            config.consecutive_failures = 0
        
        # Update stats
        provider_key = provider.value
        if provider_key not in self._stats["requests_per_provider"]:
            self._stats["requests_per_provider"][provider_key] = 0
        self._stats["requests_per_provider"][provider_key] += 1
    
    def _record_failure(self, provider: LLMProvider):
        """Record failed request"""
        config = self._providers.get(provider)
        if config:
            config.last_failure = datetime.utcnow()
            config.consecutive_failures += 1
        
        # Update stats
        provider_key = provider.value
        if provider_key not in self._stats["failures_per_provider"]:
            self._stats["failures_per_provider"][provider_key] = 0
        self._stats["failures_per_provider"][provider_key] += 1
    
    def _estimate_cost(
        self, 
        model: ModelSpec, 
        input_tokens: int, 
        output_tokens: int
    ) -> Decimal:
        """Estimate cost for a request"""
        input_cost = (Decimal(input_tokens) / 1000) * model.cost_per_1k_input
        output_cost = (Decimal(output_tokens) / 1000) * model.cost_per_1k_output
        return input_cost + output_cost
    
    def get_stats(self) -> Dict[str, Any]:
        """Get router statistics"""
        return {
            **self._stats,
            "available_providers": [p.value for p in self.get_available_providers()],
            "total_budgets_tracked": len(self._budgets)
        }
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model"""
        model = MODEL_REGISTRY.get(model_id)
        if not model:
            return None
        
        return {
            "model_id": model.model_id,
            "provider": model.provider.value,
            "display_name": model.display_name,
            "max_context_length": model.max_context_length,
            "max_output_tokens": model.max_output_tokens,
            "supports_vision": model.supports_vision,
            "supports_function_calling": model.supports_function_calling,
            "supports_json_mode": model.supports_json_mode,
            "quality_score": model.quality_score,
            "cost_per_1k_input": str(model.cost_per_1k_input),
            "cost_per_1k_output": str(model.cost_per_1k_output),
            "best_for": [t.value for t in model.best_for]
        }
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models"""
        return [
            self.get_model_info(model_id)
            for model_id in MODEL_REGISTRY.keys()
        ]


# =============================================================================
# EXCEPTIONS
# =============================================================================

class LLMRouterError(Exception):
    """Base LLM Router error"""
    pass


class BudgetExceededError(LLMRouterError):
    """Token or cost budget exceeded"""
    pass


class RateLimitExceededError(LLMRouterError):
    """Provider rate limit exceeded"""
    pass


class ModelNotFoundError(LLMRouterError):
    """Model not found in registry"""
    pass


class ProviderNotAvailableError(LLMRouterError):
    """Provider not available"""
    pass


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_llm_router: Optional[LLMRouter] = None


def get_llm_router() -> LLMRouter:
    """Get or create the LLM router singleton"""
    global _llm_router
    if _llm_router is None:
        _llm_router = LLMRouter()
        
        # Register default providers (mock configs for now)
        _llm_router.register_provider(ProviderConfig(
            provider=LLMProvider.ANTHROPIC,
            models=["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"],
            priority=1,
            cost_per_1k_input=Decimal("0.003"),
            cost_per_1k_output=Decimal("0.015"),
            supports_vision=True,
            supports_function_calling=True,
            max_context_length=200000
        ))
        
        _llm_router.register_provider(ProviderConfig(
            provider=LLMProvider.OPENAI,
            models=["gpt-4o", "gpt-4o-mini", "o1"],
            priority=1,
            cost_per_1k_input=Decimal("0.0025"),
            cost_per_1k_output=Decimal("0.01"),
            supports_vision=True,
            supports_function_calling=True,
            max_context_length=128000
        ))
        
        _llm_router.register_provider(ProviderConfig(
            provider=LLMProvider.GOOGLE,
            models=["gemini-2.0-flash-exp"],
            priority=2,
            cost_per_1k_input=Decimal("0.0"),
            cost_per_1k_output=Decimal("0.0"),
            supports_vision=True,
            max_context_length=1000000
        ))
        
        _llm_router.register_provider(ProviderConfig(
            provider=LLMProvider.GROQ,
            models=["llama-3.3-70b-versatile"],
            priority=2,
            cost_per_1k_input=Decimal("0.00059"),
            cost_per_1k_output=Decimal("0.00079"),
            max_context_length=128000,
            rate_limit_rpm=30
        ))
    
    return _llm_router


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "LLMRouter",
    "LLMProvider",
    "LLMRequest",
    "LLMResponse",
    "TaskType",
    "RoutingStrategy",
    "ProviderConfig",
    "ModelSpec",
    "TokenBudget",
    "MODEL_REGISTRY",
    "get_llm_router",
    "LLMRouterError",
    "BudgetExceededError",
    "RateLimitExceededError",
    "ModelNotFoundError",
    "ProviderNotAvailableError"
]
