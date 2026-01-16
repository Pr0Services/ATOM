"""
============================================================================
CHE·NU™ V69 — WORKER MANAGER
============================================================================
Version: 1.0.0
Purpose: Manage simulation workers and task execution
Principle: Isolated, deterministic, parallel execution
============================================================================
"""

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, Future
import logging
import threading
import uuid

from ..core.models import (
    WorkerTask,
    WorkerStatus,
    SimulationArtifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# WORKER
# ============================================================================

class Worker:
    """
    Simulation worker for executing tasks.
    
    Each worker:
    - Runs in isolation
    - Processes one task at a time
    - Reports progress
    - Handles errors gracefully
    """
    
    def __init__(self, worker_id: Optional[str] = None):
        self.worker_id = worker_id or str(uuid.uuid4())
        self.status = WorkerStatus.IDLE
        self.current_task: Optional[WorkerTask] = None
        self._lock = threading.Lock()
    
    def execute(
        self,
        task: WorkerTask,
        executor: Callable[[WorkerTask], SimulationArtifact],
    ) -> SimulationArtifact:
        """
        Execute a task.
        
        Args:
            task: Task to execute
            executor: Function that runs the task
            
        Returns:
            SimulationArtifact result
        """
        with self._lock:
            if self.status == WorkerStatus.RUNNING:
                raise RuntimeError(f"Worker {self.worker_id} is already running")
            
            self.status = WorkerStatus.RUNNING
            self.current_task = task
            task.worker_id = self.worker_id
            task.status = WorkerStatus.RUNNING
            task.started_at = datetime.utcnow()
        
        try:
            result = executor(task)
            
            with self._lock:
                self.status = WorkerStatus.COMPLETED
                task.status = WorkerStatus.COMPLETED
                task.completed_at = datetime.utcnow()
                task.result_artifact_id = result.artifact_id
                self.current_task = None
            
            logger.info(f"Worker {self.worker_id} completed task {task.task_id}")
            
            return result
            
        except Exception as e:
            with self._lock:
                self.status = WorkerStatus.FAILED
                task.status = WorkerStatus.FAILED
                task.error_message = str(e)
                task.completed_at = datetime.utcnow()
                self.current_task = None
            
            logger.error(f"Worker {self.worker_id} failed task {task.task_id}: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if worker is available"""
        with self._lock:
            return self.status in [WorkerStatus.IDLE, WorkerStatus.COMPLETED]


# ============================================================================
# WORKER POOL
# ============================================================================

class WorkerPool:
    """
    Pool of workers for parallel task execution.
    
    Manages a fixed number of workers and distributes tasks.
    """
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.workers: List[Worker] = [
            Worker(worker_id=f"worker-{i}")
            for i in range(num_workers)
        ]
        self._executor = ThreadPoolExecutor(max_workers=num_workers)
        self._pending_futures: Dict[str, Future] = {}
    
    def submit_task(
        self,
        task: WorkerTask,
        executor: Callable[[WorkerTask], SimulationArtifact],
    ) -> str:
        """
        Submit a task for execution.
        
        Args:
            task: Task to execute
            executor: Function that runs the task
            
        Returns:
            Task ID
        """
        # Find available worker
        worker = self._get_available_worker()
        if worker is None:
            raise RuntimeError("No workers available")
        
        # Submit to thread pool
        future = self._executor.submit(worker.execute, task, executor)
        self._pending_futures[task.task_id] = future
        
        logger.info(f"Submitted task {task.task_id} to worker {worker.worker_id}")
        
        return task.task_id
    
    def wait_for_task(self, task_id: str, timeout: Optional[float] = None) -> Optional[SimulationArtifact]:
        """
        Wait for a task to complete.
        
        Args:
            task_id: Task ID
            timeout: Timeout in seconds
            
        Returns:
            SimulationArtifact or None if timeout
        """
        future = self._pending_futures.get(task_id)
        if future is None:
            return None
        
        try:
            result = future.result(timeout=timeout)
            del self._pending_futures[task_id]
            return result
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            return None
    
    def wait_all(self, timeout: Optional[float] = None) -> Dict[str, Optional[SimulationArtifact]]:
        """
        Wait for all pending tasks.
        
        Returns:
            Dict of task_id -> result
        """
        results = {}
        
        for task_id in list(self._pending_futures.keys()):
            results[task_id] = self.wait_for_task(task_id, timeout)
        
        return results
    
    def _get_available_worker(self) -> Optional[Worker]:
        """Get an available worker"""
        for worker in self.workers:
            if worker.is_available():
                return worker
        return None
    
    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the pool"""
        self._executor.shutdown(wait=wait)
    
    @property
    def available_workers(self) -> int:
        """Number of available workers"""
        return sum(1 for w in self.workers if w.is_available())
    
    @property
    def pending_tasks(self) -> int:
        """Number of pending tasks"""
        return len(self._pending_futures)


# ============================================================================
# WORKER MANAGER
# ============================================================================

class WorkerManager:
    """
    High-level manager for worker operations.
    
    Provides:
    - Task scheduling
    - Progress tracking
    - Result collection
    - Error handling
    """
    
    def __init__(self, num_workers: int = 4):
        self.pool = WorkerPool(num_workers)
        self._tasks: Dict[str, WorkerTask] = {}
        self._results: Dict[str, SimulationArtifact] = {}
    
    def create_task(
        self,
        simulation_id: str,
        scenario_id: str,
        t_start: int = 0,
        t_end: int = 100,
        task_type: str = "simulate",
    ) -> WorkerTask:
        """Create a new task"""
        task = WorkerTask(
            simulation_id=simulation_id,
            scenario_id=scenario_id,
            t_start=t_start,
            t_end=t_end,
            task_type=task_type,
        )
        
        self._tasks[task.task_id] = task
        
        return task
    
    def submit(
        self,
        task: WorkerTask,
        executor: Callable[[WorkerTask], SimulationArtifact],
    ) -> str:
        """Submit a task"""
        return self.pool.submit_task(task, executor)
    
    def get_task(self, task_id: str) -> Optional[WorkerTask]:
        """Get task by ID"""
        return self._tasks.get(task_id)
    
    def get_result(self, task_id: str) -> Optional[SimulationArtifact]:
        """Get result for a task"""
        return self._results.get(task_id)
    
    def collect_result(self, task_id: str, timeout: Optional[float] = None) -> Optional[SimulationArtifact]:
        """Wait for and collect a task result"""
        result = self.pool.wait_for_task(task_id, timeout)
        if result:
            self._results[task_id] = result
        return result
    
    def collect_all(self, timeout: Optional[float] = None) -> Dict[str, Optional[SimulationArtifact]]:
        """Collect all pending results"""
        results = self.pool.wait_all(timeout)
        self._results.update({k: v for k, v in results.items() if v is not None})
        return results
    
    def shutdown(self) -> None:
        """Shutdown manager"""
        self.pool.shutdown()
