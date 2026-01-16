"""
============================================================================
CHE·NU™ V69 — REPLAY CHUNKER
============================================================================
Version: 1.0.0
Purpose: Split replay frames into CDN-friendly chunks
Principle: Progressive loading for smooth XR experience
============================================================================
"""

from typing import Any, Dict, List, Optional
import logging
import math

from ..models.artifacts import (
    ReplayFrame,
    ReplayChunk,
    ChunkReference,
    ReplayIndexV1,
    ReplayMode,
)

logger = logging.getLogger(__name__)


# ============================================================================
# REPLAY CHUNKER
# ============================================================================

class ReplayChunker:
    """
    Splits replay frames into CDN-friendly chunks.
    
    Why chunking?
    - Loading 50k frames in WebXR = death
    - Chunking = smooth UX + CDN caching
    - Progressive loading = instant start
    
    Usage:
        chunker = ReplayChunker(chunk_size=250)
        
        # Add frames
        for step, state in enumerate(simulation_states):
            chunker.add_frame(ReplayFrame(
                step=step,
                slots=state["slots"],
                events=state.get("events", []),
            ))
        
        # Generate chunks
        index, chunks = chunker.build()
    """
    
    def __init__(self, chunk_size: int = 250):
        self.chunk_size = chunk_size
        self.frames: List[ReplayFrame] = []
    
    def add_frame(self, frame: ReplayFrame) -> None:
        """Add a frame to the replay"""
        self.frames.append(frame)
    
    def add_frames(self, frames: List[ReplayFrame]) -> None:
        """Add multiple frames"""
        self.frames.extend(frames)
    
    def build(self) -> tuple[ReplayIndexV1, List[ReplayChunk]]:
        """
        Build replay index and chunks.
        
        Returns:
            Tuple of (ReplayIndexV1, list of ReplayChunk)
        """
        if not self.frames:
            return self._build_empty()
        
        # Sort frames by step
        sorted_frames = sorted(self.frames, key=lambda f: f.step)
        
        # Calculate number of chunks
        num_chunks = math.ceil(len(sorted_frames) / self.chunk_size)
        
        # Create index
        index = ReplayIndexV1(
            mode=ReplayMode.CHUNKED,
            chunk_size=self.chunk_size,
            total_steps=len(sorted_frames),
            total_chunks=num_chunks,
        )
        
        # Create chunks
        chunks: List[ReplayChunk] = []
        
        for chunk_id in range(num_chunks):
            start_idx = chunk_id * self.chunk_size
            end_idx = min(start_idx + self.chunk_size, len(sorted_frames))
            
            chunk_frames = sorted_frames[start_idx:end_idx]
            
            if not chunk_frames:
                continue
            
            chunk = ReplayChunk(
                chunk_id=chunk_id,
                from_step=chunk_frames[0].step,
                to_step=chunk_frames[-1].step,
                frames=chunk_frames,
            )
            
            chunks.append(chunk)
            index.add_chunk(chunk)
        
        logger.info(
            f"Built {len(chunks)} replay chunks "
            f"({len(sorted_frames)} frames, chunk_size={self.chunk_size})"
        )
        
        return index, chunks
    
    def _build_empty(self) -> tuple[ReplayIndexV1, List[ReplayChunk]]:
        """Build empty replay"""
        return ReplayIndexV1(
            mode=ReplayMode.CHUNKED,
            chunk_size=self.chunk_size,
            total_steps=0,
            total_chunks=0,
        ), []
    
    @classmethod
    def from_simulation_states(
        cls,
        states: List[Dict[str, Any]],
        chunk_size: int = 250,
    ) -> tuple[ReplayIndexV1, List[ReplayChunk]]:
        """
        Create chunks from simulation state history.
        
        Args:
            states: List of {"step": int, "slots": {}, "events": []}
            chunk_size: Frames per chunk
        """
        chunker = cls(chunk_size)
        
        for state in states:
            frame = ReplayFrame(
                step=state.get("step", 0),
                timestamp_sim=state.get("timestamp", 0),
                slots=state.get("slots", {}),
                events=state.get("events", []),
                camera_focus=state.get("camera_focus"),
                highlights=state.get("highlights", []),
            )
            chunker.add_frame(frame)
        
        return chunker.build()


# ============================================================================
# CHUNK FILE GENERATOR
# ============================================================================

class ChunkFileGenerator:
    """
    Generates chunk file paths and content.
    
    File naming convention:
    - replay/index.v1.json
    - replay/chunk_0000.v1.json
    - replay/chunk_0001.v1.json
    - ...
    """
    
    @staticmethod
    def get_index_filename() -> str:
        """Get index filename"""
        return "replay/index.v1.json"
    
    @staticmethod
    def get_chunk_filename(chunk_id: int) -> str:
        """Get chunk filename"""
        return f"replay/chunk_{chunk_id:04d}.v1.json"
    
    @staticmethod
    def generate_files(
        index: ReplayIndexV1,
        chunks: List[ReplayChunk],
    ) -> Dict[str, str]:
        """
        Generate all replay files as JSON strings.
        
        Returns:
            Dict of {filename: json_content}
        """
        files = {}
        
        # Index file
        files[ChunkFileGenerator.get_index_filename()] = index.model_dump_json(indent=2)
        
        # Chunk files
        for chunk in chunks:
            filename = ChunkFileGenerator.get_chunk_filename(chunk.chunk_id)
            files[filename] = chunk.model_dump_json(indent=2)
        
        return files


# ============================================================================
# CHUNK LOADER (for XR client simulation)
# ============================================================================

class ChunkLoader:
    """
    Simulates chunk loading for testing.
    
    In production, this would be replaced by XR client fetch logic.
    """
    
    def __init__(self, chunks: List[ReplayChunk]):
        self._chunks = {c.chunk_id: c for c in chunks}
    
    def get_chunk(self, chunk_id: int) -> Optional[ReplayChunk]:
        """Get chunk by ID"""
        return self._chunks.get(chunk_id)
    
    def get_chunk_for_step(self, step: int, index: ReplayIndexV1) -> Optional[ReplayChunk]:
        """Get chunk containing a specific step"""
        for ref in index.chunks:
            if ref.from_step <= step <= ref.to_step:
                return self._chunks.get(ref.id)
        return None
    
    def get_frame(self, step: int, index: ReplayIndexV1) -> Optional[ReplayFrame]:
        """Get specific frame by step"""
        chunk = self.get_chunk_for_step(step, index)
        if chunk is None:
            return None
        
        for frame in chunk.frames:
            if frame.step == step:
                return frame
        
        return None
