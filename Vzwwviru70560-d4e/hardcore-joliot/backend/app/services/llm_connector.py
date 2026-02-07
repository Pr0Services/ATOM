"""
═══════════════════════════════════════════════════════════════════════════════
AT·OM LLM CONNECTOR — Real Provider Integration
═══════════════════════════════════════════════════════════════════════════════

Connects the LLM Router to actual API providers:
- Anthropic (Claude)
- OpenAI (GPT)
- Google (Gemini)
- Groq (Llama)
- DeepSeek
- Mistral

This module replaces the mock implementation with real API calls.

R&D COMPLIANCE:
- Rule #1: LLM outputs are drafts only - requires human gates
- Rule #6: All API calls are logged for traceability
- Rule #7: Respects token budgets

VERSION: 1.0.0
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import asyncio
import logging
import time
from typing import Dict, Any, Optional, List, AsyncIterator
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from enum import Enum

import httpx

logger = logging.getLogger("atom.llm_connector")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class APIConfig:
    """Configuration for an API provider."""
    name: str
    base_url: str
    api_key_env: str
    default_model: str
    timeout: int = 60
    max_retries: int = 3


# Provider configurations
PROVIDER_CONFIGS: Dict[str, APIConfig] = {
    "anthropic": APIConfig(
        name="Anthropic",
        base_url="https://api.anthropic.com/v1",
        api_key_env="ANTHROPIC_API_KEY",
        default_model="claude-3-5-sonnet-20241022",
        timeout=120,
    ),
    "openai": APIConfig(
        name="OpenAI",
        base_url="https://api.openai.com/v1",
        api_key_env="OPENAI_API_KEY",
        default_model="gpt-4o",
        timeout=60,
    ),
    "google": APIConfig(
        name="Google",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_key_env="GOOGLE_API_KEY",
        default_model="gemini-2.0-flash-exp",
        timeout=60,
    ),
    "groq": APIConfig(
        name="Groq",
        base_url="https://api.groq.com/openai/v1",
        api_key_env="GROQ_API_KEY",
        default_model="llama-3.3-70b-versatile",
        timeout=30,
    ),
    "deepseek": APIConfig(
        name="DeepSeek",
        base_url="https://api.deepseek.com/v1",
        api_key_env="DEEPSEEK_API_KEY",
        default_model="deepseek-chat",
        timeout=60,
    ),
    "mistral": APIConfig(
        name="Mistral",
        base_url="https://api.mistral.ai/v1",
        api_key_env="MISTRAL_API_KEY",
        default_model="mistral-large-latest",
        timeout=60,
    ),
    "openrouter": APIConfig(
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        api_key_env="OPENROUTER_API_KEY",
        default_model="anthropic/claude-3-5-sonnet",
        timeout=120,
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# LLM CONNECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class LLMConnector:
    """
    Real LLM connector that calls actual provider APIs.

    Supports:
    - Anthropic Claude
    - OpenAI GPT
    - Google Gemini
    - Groq
    - DeepSeek
    - Mistral
    - OpenRouter (unified gateway)
    """

    def __init__(self):
        self._clients: Dict[str, httpx.AsyncClient] = {}
        self._api_keys: Dict[str, str] = {}
        self._stats = {
            "total_calls": 0,
            "total_tokens": 0,
            "total_cost": Decimal("0.0"),
            "errors": 0,
        }

        # Load API keys from environment
        self._load_api_keys()

        logger.info(f"LLMConnector initialized with {len(self._api_keys)} providers")

    def _load_api_keys(self):
        """Load API keys from environment variables."""
        for provider, config in PROVIDER_CONFIGS.items():
            api_key = os.getenv(config.api_key_env)
            if api_key:
                self._api_keys[provider] = api_key
                logger.info(f"✓ Loaded API key for {config.name}")
            else:
                logger.warning(f"✗ No API key for {config.name} ({config.api_key_env})")

    def get_available_providers(self) -> List[str]:
        """Get list of providers with valid API keys."""
        return list(self._api_keys.keys())

    async def _get_client(self, provider: str) -> httpx.AsyncClient:
        """Get or create HTTP client for provider."""
        if provider not in self._clients:
            config = PROVIDER_CONFIGS.get(provider)
            if not config:
                raise ValueError(f"Unknown provider: {provider}")

            self._clients[provider] = httpx.AsyncClient(
                base_url=config.base_url,
                timeout=httpx.Timeout(config.timeout),
                headers=self._get_headers(provider),
            )

        return self._clients[provider]

    def _get_headers(self, provider: str) -> Dict[str, str]:
        """Get headers for a provider."""
        api_key = self._api_keys.get(provider)
        if not api_key:
            raise ValueError(f"No API key for provider: {provider}")

        headers = {
            "Content-Type": "application/json",
        }

        if provider == "anthropic":
            headers["x-api-key"] = api_key
            headers["anthropic-version"] = "2023-06-01"
        elif provider == "openrouter":
            headers["Authorization"] = f"Bearer {api_key}"
            headers["HTTP-Referer"] = "https://atom.chenutechnologies.com"
            headers["X-Title"] = "AT·OM Multidimensional OS"
        else:
            # OpenAI-compatible APIs (OpenAI, Groq, DeepSeek, Mistral)
            headers["Authorization"] = f"Bearer {api_key}"

        return headers

    # ═══════════════════════════════════════════════════════════════════════════
    # COMPLETION METHODS
    # ═══════════════════════════════════════════════════════════════════════════

    async def complete(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute completion with a specific provider.

        Args:
            provider: Provider name (anthropic, openai, etc.)
            model: Model ID
            messages: List of message dicts
            system_prompt: Optional system message
            max_tokens: Max output tokens
            temperature: Sampling temperature
            stream: Whether to stream response

        Returns:
            Dict with content, tokens, cost, etc.
        """
        start_time = time.time()

        try:
            if provider == "anthropic":
                result = await self._complete_anthropic(
                    model, messages, system_prompt, max_tokens, temperature
                )
            elif provider == "google":
                result = await self._complete_google(
                    model, messages, system_prompt, max_tokens, temperature
                )
            else:
                # OpenAI-compatible providers
                result = await self._complete_openai_compatible(
                    provider, model, messages, system_prompt, max_tokens, temperature
                )

            # Add timing
            result["latency_ms"] = int((time.time() - start_time) * 1000)
            result["provider"] = provider
            result["model"] = model

            # Update stats
            self._stats["total_calls"] += 1
            self._stats["total_tokens"] += result.get("total_tokens", 0)
            self._stats["total_cost"] += Decimal(str(result.get("cost", 0)))

            logger.info(
                f"LLM Complete: provider={provider} model={model} "
                f"tokens={result.get('total_tokens', 0)} "
                f"latency={result['latency_ms']}ms"
            )

            return result

        except Exception as e:
            self._stats["errors"] += 1
            logger.error(f"LLM Error: provider={provider} error={e}")
            raise

    async def _complete_anthropic(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> Dict[str, Any]:
        """Complete with Anthropic Claude API."""
        client = await self._get_client("anthropic")

        # Build request body
        body = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
        }

        if system_prompt:
            body["system"] = system_prompt

        if temperature is not None:
            body["temperature"] = temperature

        # Make request
        response = await client.post("/messages", json=body)
        response.raise_for_status()

        data = response.json()

        # Extract content
        content = ""
        if data.get("content"):
            for block in data["content"]:
                if block.get("type") == "text":
                    content += block.get("text", "")

        # Calculate cost (Claude 3.5 Sonnet pricing)
        input_tokens = data.get("usage", {}).get("input_tokens", 0)
        output_tokens = data.get("usage", {}).get("output_tokens", 0)

        # Cost per 1M tokens: input $3, output $15
        cost = (input_tokens * 0.000003) + (output_tokens * 0.000015)

        return {
            "content": content,
            "finish_reason": data.get("stop_reason", "end_turn"),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": cost,
            "raw_response": data,
        }

    async def _complete_openai_compatible(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> Dict[str, Any]:
        """Complete with OpenAI-compatible API (OpenAI, Groq, DeepSeek, Mistral)."""
        client = await self._get_client(provider)

        # Add system message to messages
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        # Build request body
        body = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
        }

        if temperature is not None:
            body["temperature"] = temperature

        # Make request
        response = await client.post("/chat/completions", json=body)
        response.raise_for_status()

        data = response.json()

        # Extract content
        content = ""
        if data.get("choices"):
            content = data["choices"][0].get("message", {}).get("content", "")

        # Extract usage
        usage = data.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        # Estimate cost based on provider
        cost = self._estimate_cost(provider, model, input_tokens, output_tokens)

        return {
            "content": content,
            "finish_reason": data.get("choices", [{}])[0].get("finish_reason", "stop"),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": cost,
            "raw_response": data,
        }

    async def _complete_google(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> Dict[str, Any]:
        """Complete with Google Gemini API."""
        api_key = self._api_keys.get("google")
        if not api_key:
            raise ValueError("No Google API key")

        # Google uses a different API structure
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            role = "user" if msg.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.get("content", "")}]
            })

        body = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            }
        }

        if system_prompt:
            body["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=body,
                params={"key": api_key},
                timeout=60,
            )
            response.raise_for_status()

        data = response.json()

        # Extract content
        content = ""
        if data.get("candidates"):
            parts = data["candidates"][0].get("content", {}).get("parts", [])
            for part in parts:
                content += part.get("text", "")

        # Google usage metadata
        usage = data.get("usageMetadata", {})
        input_tokens = usage.get("promptTokenCount", 0)
        output_tokens = usage.get("candidatesTokenCount", 0)

        return {
            "content": content,
            "finish_reason": "stop",
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": 0.0,  # Gemini Flash is free
            "raw_response": data,
        }

    def _estimate_cost(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """Estimate cost based on provider and model."""
        # Pricing per 1M tokens
        pricing = {
            "openai": {
                "gpt-4o": (2.5, 10),       # $2.50 input, $10 output
                "gpt-4o-mini": (0.15, 0.6), # $0.15 input, $0.60 output
                "o1": (15, 60),             # $15 input, $60 output
            },
            "anthropic": {
                "claude-3-5-sonnet-20241022": (3, 15),
                "claude-3-5-haiku-20241022": (0.25, 1.25),
            },
            "groq": {
                "llama-3.3-70b-versatile": (0.59, 0.79),
            },
            "deepseek": {
                "deepseek-chat": (0.27, 1.1),
            },
            "mistral": {
                "mistral-large-latest": (2, 6),
                "codestral-latest": (1, 3),
            },
        }

        provider_pricing = pricing.get(provider, {})
        model_pricing = provider_pricing.get(model, (1, 3))  # Default

        input_cost = (input_tokens / 1_000_000) * model_pricing[0]
        output_cost = (output_tokens / 1_000_000) * model_pricing[1]

        return input_cost + output_cost

    # ═══════════════════════════════════════════════════════════════════════════
    # STREAMING
    # ═══════════════════════════════════════════════════════════════════════════

    async def stream(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        """
        Stream completion from a provider.

        Yields content chunks as they arrive.
        """
        if provider == "anthropic":
            async for chunk in self._stream_anthropic(
                model, messages, system_prompt, max_tokens, temperature
            ):
                yield chunk
        else:
            async for chunk in self._stream_openai_compatible(
                provider, model, messages, system_prompt, max_tokens, temperature
            ):
                yield chunk

    async def _stream_anthropic(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> AsyncIterator[str]:
        """Stream from Anthropic Claude."""
        client = await self._get_client("anthropic")

        body = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
            "stream": True,
        }

        if system_prompt:
            body["system"] = system_prompt
        if temperature is not None:
            body["temperature"] = temperature

        async with client.stream("POST", "/messages", json=body) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        import json
                        event = json.loads(data)
                        if event.get("type") == "content_block_delta":
                            delta = event.get("delta", {})
                            if delta.get("type") == "text_delta":
                                yield delta.get("text", "")
                    except:
                        pass

    async def _stream_openai_compatible(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> AsyncIterator[str]:
        """Stream from OpenAI-compatible API."""
        client = await self._get_client(provider)

        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        body = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": True,
        }

        if temperature is not None:
            body["temperature"] = temperature

        async with client.stream("POST", "/chat/completions", json=body) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        import json
                        event = json.loads(data)
                        content = event.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if content:
                            yield content
                    except:
                        pass

    # ═══════════════════════════════════════════════════════════════════════════
    # CLEANUP
    # ═══════════════════════════════════════════════════════════════════════════

    async def close(self):
        """Close all HTTP clients."""
        for client in self._clients.values():
            await client.aclose()
        self._clients.clear()
        logger.info("LLMConnector closed")

    def get_stats(self) -> Dict[str, Any]:
        """Get connector statistics."""
        return {
            **self._stats,
            "available_providers": self.get_available_providers(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_connector: Optional[LLMConnector] = None


def get_llm_connector() -> LLMConnector:
    """Get or create the LLM connector singleton."""
    global _connector
    if _connector is None:
        _connector = LLMConnector()
    return _connector


async def close_llm_connector():
    """Close the LLM connector."""
    global _connector
    if _connector:
        await _connector.close()
        _connector = None


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "LLMConnector",
    "get_llm_connector",
    "close_llm_connector",
    "PROVIDER_CONFIGS",
    "APIConfig",
]
