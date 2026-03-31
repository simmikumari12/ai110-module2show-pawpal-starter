"""
PawPal+ System - Core classes for pet care task scheduling.

This module contains the backbone of the PawPal+ app:
- Task: Represents a single pet care activity
- Pet: Represents a pet and its tasks
- Owner: Represents the pet owner
- Scheduler: The scheduling logic that organizes tasks
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime, timedelta


@dataclass
class Task:
    """
    Represents a single pet care task (e.g., walk, feeding, medication).
    """
    description: str
    duration_min: int  # Duration in minutes
    priority: str  # "high", "medium", "low"
    frequency: str  # "daily", "weekly", "once"
    is_complete: bool = False
    scheduled_time: Optional[str] = None  # HH:MM format (e.g., "09:00")
    task_id: int = field(default_factory=lambda: hash(datetime.now()))  # Unique ID for tracking recurrence

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.is_complete = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_complete = False

    def __str__(self) -> str:
        """Return a readable string representation of the task."""
        status = "✓" if self.is_complete else "○"
        time_str = f" @ {self.scheduled_time}" if self.scheduled_time else ""
        return f"[{status}] {self.description} ({self.duration_min}min) - Priority: {self.priority}{time_str}"


@dataclass
class Pet:
    """
    Represents a pet owned by the owner. Stores pet details and manages tasks.
    """
    name: str
    pet_type: str  # "dog", "cat", "rabbit", etc.
    age: int
    special_needs: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def complete_task(self, task: Task) -> None:
        """Mark a specific task as complete."""
        for t in self.tasks:
            if t == task:
                t.mark_complete()
                break


@dataclass
class Owner:
    """
    Represents the pet owner. Manages pets and their tasks.
    """
    name: str
    availability_hours: float  # Hours available per day for pet care
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """
    The scheduling engine for PawPal+.
    
    Retrieves tasks from the owner's pets and organizes them into
    a daily schedule based on priority, duration, and availability constraints.
    Supports sorting, filtering, conflict detection, and recurring task management.
    """

    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner instance."""
        self.owner = owner
        self.conflicts = []  # Track detected conflicts

    def generate_schedule(self) -> List[Task]:
        """
        Generate today's optimized schedule.
        
        Returns a list of tasks organized by priority and feasibility.
        """
        all_tasks = self.owner.get_all_tasks()
        # Filter out completed tasks and organize by priority
        pending_tasks = [t for t in all_tasks if not t.is_complete]
        scheduled = self.organize_tasks_by_priority(pending_tasks)
        
        # Check for conflicts
        self.conflicts = self.detect_conflicts(scheduled)
        
        return scheduled

    def organize_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """
        Sort and organize tasks by priority level.
        
        Returns tasks in order from highest to lowest priority,
        only including tasks that fit within the owner's availability.
        """
        # Define priority order
        priority_order = {"high": 0, "medium": 1, "low": 2}
        
        # Sort by priority
        sorted_tasks = sorted(
            tasks,
            key=lambda t: priority_order.get(t.priority.lower(), 3)
        )
        
        # Filter tasks that fit within owner's availability
        total_time = 0
        available_minutes = int(self.owner.availability_hours * 60)
        feasible_tasks = []
        
        for task in sorted_tasks:
            if total_time + task.duration_min <= available_minutes:
                feasible_tasks.append(task)
                total_time += task.duration_min
        
        return feasible_tasks

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by their scheduled_time in HH:MM format.
        
        Tasks without a scheduled_time are placed at the end.
        Returns a new sorted list without modifying the original.
        """
        def parse_time(time_str: Optional[str]) -> Tuple[int, int]:
            """Parse HH:MM string to (hours, minutes) tuple for comparison."""
            if not time_str:
                return (24, 0)  # Place unscheduled tasks at the end
            try:
                h, m = map(int, time_str.split(":"))
                return (h, m)
            except (ValueError, AttributeError):
                return (24, 0)
        
        return sorted(tasks, key=lambda t: parse_time(t.scheduled_time))

    def filter_tasks(self, tasks: List[Task], pet_name: Optional[str] = None, 
                     status: Optional[str] = None) -> List[Task]:
        """
        Filter tasks by pet name and/or completion status.
        
        Args:
            tasks: List of tasks to filter.
            pet_name: Filter by pet name (None = all pets).
            status: Filter by "complete" or "incomplete" (None = all statuses).
        
        Returns:
            Filtered list of tasks.
        """
        result = tasks
        
        # Filter by status
        if status == "complete":
            result = [t for t in result if t.is_complete]
        elif status == "incomplete":
            result = [t for t in result if not t.is_complete]
        
        # Filter by pet name
        if pet_name:
            pet_tasks = []
            for pet in self.owner.get_pets():
                if pet.name == pet_name:
                    pet_tasks.extend(pet.get_tasks())
            result = [t for t in result if t in pet_tasks]
        
        return result

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """
        Detect if two tasks are scheduled at the exact same time.
        
        Returns a list of conflict warning messages.
        """
        conflict_warnings = []
        scheduled_times = {}
        
        for task in tasks:
            if task.scheduled_time:
                time = task.scheduled_time
                if time in scheduled_times:
                    msg = f"⚠️ CONFLICT: '{scheduled_times[time].description}' and '{task.description}' both at {time}"
                    conflict_warnings.append(msg)
                else:
                    scheduled_times[time] = task
        
        return conflict_warnings

    def create_recurring_task(self, original_task: Task, pet: Pet) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task.
        
        If a "daily" or "weekly" task is marked complete, generate a new task
        for the next occurrence (today+1 for daily, today+7 for weekly).
        
        Args:
            original_task: The completed task to recur.
            pet: The pet that owns the task.
        
        Returns:
            A new Task object for the next occurrence, or None if task is "once".
        """
        if original_task.frequency == "once":
            return None
        
        # Create a copy of the task
        new_task = Task(
            description=original_task.description,
            duration_min=original_task.duration_min,
            priority=original_task.priority,
            frequency=original_task.frequency,
            is_complete=False,
            scheduled_time=original_task.scheduled_time
        )
        
        return new_task

    def get_today_schedule(self) -> str:
        """
        Return a formatted string representation of today's schedule.
        """
        schedule = self.generate_schedule()
        
        if not schedule:
            return "No tasks scheduled for today."
        
        output = f"Today's Schedule for {self.owner.name}\n"
        output += "=" * 50 + "\n"
        output += f"Available time: {self.owner.availability_hours} hours\n\n"
        
        total_time = 0
        for i, task in enumerate(schedule, 1):
            output += f"{i}. {task}\n"
            total_time += task.duration_min
        
        output += "\n" + f"Total scheduled time: {total_time // 60}h {total_time % 60}m\n"
        
        # Include conflict warnings
        if self.conflicts:
            output += "\n⚠️ WARNINGS:\n"
            for warning in self.conflicts:
                output += f"  {warning}\n"
        
        return output
