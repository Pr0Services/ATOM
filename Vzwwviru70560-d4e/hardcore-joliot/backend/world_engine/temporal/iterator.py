"""
============================================================================
CHE·NU™ V69 — TEMPORAL ITERATOR
============================================================================
Version: 1.0.0
Purpose: Time management for simulations
Principle: Simulated time ≠ Real time — Support projections up to 100 years
============================================================================
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Tuple
import logging

from ..core.models import TimeUnit

logger = logging.getLogger(__name__)


# ============================================================================
# TIME CONVERSION
# ============================================================================

# Conversion factors to days
TIME_UNIT_TO_DAYS = {
    TimeUnit.TICK: 1,
    TimeUnit.HOUR: 1/24,
    TimeUnit.DAY: 1,
    TimeUnit.WEEK: 7,
    TimeUnit.MONTH: 30,
    TimeUnit.QUARTER: 90,
    TimeUnit.YEAR: 365,
}


def convert_time_units(
    value: float,
    from_unit: TimeUnit,
    to_unit: TimeUnit,
) -> float:
    """Convert between time units"""
    # Convert to days first
    days = value * TIME_UNIT_TO_DAYS[from_unit]
    # Convert to target unit
    return days / TIME_UNIT_TO_DAYS[to_unit]


# ============================================================================
# TEMPORAL ITERATOR
# ============================================================================

class TemporalIterator:
    """
    Iterator for simulation time steps.
    
    Features:
    - Configurable time unit
    - Acceleration factor
    - Long-term projections (50-100 years)
    - Real-time tracking
    
    Usage:
        iterator = TemporalIterator(
            t_start=0,
            t_end=365,
            time_unit=TimeUnit.DAY,
            start_date=datetime(2024, 1, 1),
        )
        
        for tick, sim_time, real_date in iterator:
            # tick: 0, 1, 2, ...
            # sim_time: 0.0, 1.0, 2.0, ... (in time units)
            # real_date: 2024-01-01, 2024-01-02, ...
            process_tick(tick)
    """
    
    def __init__(
        self,
        t_start: int = 0,
        t_end: int = 100,
        time_unit: TimeUnit = TimeUnit.TICK,
        start_date: Optional[datetime] = None,
        acceleration_factor: float = 1.0,
    ):
        self.t_start = t_start
        self.t_end = t_end
        self.time_unit = time_unit
        self.start_date = start_date or datetime.utcnow()
        self.acceleration_factor = acceleration_factor
        
        self._current_tick = t_start
        self._started_at: Optional[datetime] = None
    
    def __iter__(self) -> Generator[Tuple[int, float, datetime], None, None]:
        """Iterate through time steps"""
        self._started_at = datetime.utcnow()
        
        for tick in range(self.t_start, self.t_end + 1):
            self._current_tick = tick
            
            # Calculate simulated time
            sim_time = float(tick)
            
            # Calculate real date
            days_elapsed = convert_time_units(
                tick - self.t_start,
                self.time_unit,
                TimeUnit.DAY,
            )
            real_date = self.start_date + timedelta(days=days_elapsed)
            
            yield tick, sim_time, real_date
    
    @property
    def current_tick(self) -> int:
        """Current tick"""
        return self._current_tick
    
    @property
    def progress(self) -> float:
        """Progress (0-1)"""
        total = self.t_end - self.t_start
        if total == 0:
            return 1.0
        return (self._current_tick - self.t_start) / total
    
    @property
    def remaining_ticks(self) -> int:
        """Remaining ticks"""
        return self.t_end - self._current_tick
    
    def get_date_for_tick(self, tick: int) -> datetime:
        """Get real date for a specific tick"""
        days_elapsed = convert_time_units(
            tick - self.t_start,
            self.time_unit,
            TimeUnit.DAY,
        )
        return self.start_date + timedelta(days=days_elapsed)
    
    def get_tick_for_date(self, date: datetime) -> int:
        """Get tick for a specific date"""
        days_elapsed = (date - self.start_date).days
        ticks = convert_time_units(
            days_elapsed,
            TimeUnit.DAY,
            self.time_unit,
        )
        return int(self.t_start + ticks)


# ============================================================================
# TEMPORAL RANGE
# ============================================================================

class TemporalRange:
    """
    Represents a range of time in the simulation.
    
    Used for:
    - Defining simulation periods
    - Specifying intervention windows
    - Querying historical data
    """
    
    def __init__(
        self,
        t_start: int,
        t_end: int,
        time_unit: TimeUnit = TimeUnit.TICK,
    ):
        if t_end < t_start:
            raise ValueError("t_end must be >= t_start")
        
        self.t_start = t_start
        self.t_end = t_end
        self.time_unit = time_unit
    
    @property
    def duration(self) -> int:
        """Duration in time units"""
        return self.t_end - self.t_start
    
    @property
    def duration_days(self) -> float:
        """Duration in days"""
        return convert_time_units(self.duration, self.time_unit, TimeUnit.DAY)
    
    @property
    def duration_years(self) -> float:
        """Duration in years"""
        return convert_time_units(self.duration, self.time_unit, TimeUnit.YEAR)
    
    def contains(self, tick: int) -> bool:
        """Check if tick is in range"""
        return self.t_start <= tick <= self.t_end
    
    def overlaps(self, other: "TemporalRange") -> bool:
        """Check if ranges overlap"""
        return not (self.t_end < other.t_start or other.t_end < self.t_start)
    
    def intersection(self, other: "TemporalRange") -> Optional["TemporalRange"]:
        """Get intersection of two ranges"""
        if not self.overlaps(other):
            return None
        
        return TemporalRange(
            t_start=max(self.t_start, other.t_start),
            t_end=min(self.t_end, other.t_end),
            time_unit=self.time_unit,
        )
    
    def split(self, chunk_size: int) -> List["TemporalRange"]:
        """Split range into chunks"""
        chunks = []
        current = self.t_start
        
        while current < self.t_end:
            chunk_end = min(current + chunk_size - 1, self.t_end)
            chunks.append(TemporalRange(
                t_start=current,
                t_end=chunk_end,
                time_unit=self.time_unit,
            ))
            current = chunk_end + 1
        
        return chunks


# ============================================================================
# TEMPORAL SCHEDULE
# ============================================================================

class ScheduledEvent:
    """An event scheduled at a specific tick"""
    
    def __init__(
        self,
        tick: int,
        event_type: str,
        data: Dict[str, Any],
        recurring: bool = False,
        interval: int = 0,
    ):
        self.tick = tick
        self.event_type = event_type
        self.data = data
        self.recurring = recurring
        self.interval = interval
        self.executed = False


class TemporalSchedule:
    """
    Schedule of events for a simulation.
    
    Used for:
    - Scheduling interventions
    - Triggering periodic events
    - Managing external inputs
    """
    
    def __init__(self):
        self._events: List[ScheduledEvent] = []
    
    def schedule(
        self,
        tick: int,
        event_type: str,
        data: Dict[str, Any],
        recurring: bool = False,
        interval: int = 0,
    ) -> ScheduledEvent:
        """Schedule an event"""
        event = ScheduledEvent(
            tick=tick,
            event_type=event_type,
            data=data,
            recurring=recurring,
            interval=interval,
        )
        self._events.append(event)
        return event
    
    def get_events_at(self, tick: int) -> List[ScheduledEvent]:
        """Get events scheduled for a tick"""
        events = []
        
        for event in self._events:
            if event.tick == tick:
                events.append(event)
            elif event.recurring and event.interval > 0:
                if tick >= event.tick and (tick - event.tick) % event.interval == 0:
                    events.append(event)
        
        return events
    
    def get_events_in_range(self, t_start: int, t_end: int) -> List[ScheduledEvent]:
        """Get events in a range"""
        events = []
        
        for tick in range(t_start, t_end + 1):
            events.extend(self.get_events_at(tick))
        
        return events
    
    def clear(self) -> None:
        """Clear all events"""
        self._events.clear()


# ============================================================================
# LONG-TERM PROJECTIONS
# ============================================================================

class LongTermProjector:
    """
    Supports long-term projections (50-100 years).
    
    Optimizations:
    - Adaptive time steps (coarser for stable periods)
    - Checkpoint saving
    - Memory-efficient state tracking
    """
    
    def __init__(
        self,
        base_time_unit: TimeUnit = TimeUnit.MONTH,
        projection_years: int = 50,
    ):
        self.base_time_unit = base_time_unit
        self.projection_years = projection_years
        
        # Calculate total ticks
        self.total_ticks = int(convert_time_units(
            projection_years,
            TimeUnit.YEAR,
            base_time_unit,
        ))
    
    def create_iterator(
        self,
        start_date: datetime,
    ) -> TemporalIterator:
        """Create iterator for long-term projection"""
        return TemporalIterator(
            t_start=0,
            t_end=self.total_ticks,
            time_unit=self.base_time_unit,
            start_date=start_date,
        )
    
    def create_checkpoints(
        self,
        checkpoint_interval_years: int = 5,
    ) -> List[int]:
        """Create checkpoint ticks for saving state"""
        interval_ticks = int(convert_time_units(
            checkpoint_interval_years,
            TimeUnit.YEAR,
            self.base_time_unit,
        ))
        
        checkpoints = []
        tick = interval_ticks
        
        while tick <= self.total_ticks:
            checkpoints.append(tick)
            tick += interval_ticks
        
        return checkpoints
    
    def get_year_for_tick(self, tick: int) -> float:
        """Get year number for a tick"""
        return convert_time_units(tick, self.base_time_unit, TimeUnit.YEAR)
