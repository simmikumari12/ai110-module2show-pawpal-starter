"""
Tests for PawPal+ System

Tests core functionality:
- Task completion and status tracking
- Task addition to pets
- Task retrieval from owner
- Schedule generation
- Sorting by scheduled time
- Filtering tasks by pet and status
- Conflict detection
- Recurring task creation
"""

import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTask:
    """Tests for the Task class."""
    
    def test_task_completion_marks_complete(self):
        """Verify that calling mark_complete() sets is_complete to True."""
        task = Task(
            description="Walk the dog",
            duration_min=30,
            priority="high",
            frequency="daily"
        )
        assert task.is_complete is False
        task.mark_complete()
        assert task.is_complete is True
    
    def test_task_incomplete_marks_incomplete(self):
        """Verify that calling mark_incomplete() sets is_complete to False."""
        task = Task(
            description="Feed the cat",
            duration_min=10,
            priority="high",
            frequency="daily"
        )
        task.mark_complete()
        assert task.is_complete is True
        task.mark_incomplete()
        assert task.is_complete is False
    
    def test_task_string_representation(self):
        """Verify task can be converted to readable string."""
        task = Task(
            description="Medication",
            duration_min=5,
            priority="high",
            frequency="daily"
        )
        task_str = str(task)
        assert "Medication" in task_str
        assert "5min" in task_str
        assert "high" in task_str
    
    def test_task_with_scheduled_time(self):
        """Verify task can store and display scheduled time."""
        task = Task(
            description="Morning walk",
            duration_min=30,
            priority="high",
            frequency="daily",
            scheduled_time="08:00"
        )
        assert task.scheduled_time == "08:00"
        assert "08:00" in str(task)


class TestPet:
    """Tests for the Pet class."""
    
    def test_add_task_increases_task_count(self):
        """Verify that adding a task to a pet increases the task count."""
        pet = Pet(name="Max", pet_type="dog", age=3)
        assert len(pet.get_tasks()) == 0
        
        task = Task("Walk", duration_min=30, priority="high", frequency="daily")
        pet.add_task(task)
        
        assert len(pet.get_tasks()) == 1
    
    def test_add_multiple_tasks(self):
        """Verify that multiple tasks can be added to a pet."""
        pet = Pet(name="Fluffy", pet_type="cat", age=5)
        
        task1 = Task("Feed", duration_min=10, priority="high", frequency="daily")
        task2 = Task("Play", duration_min=15, priority="medium", frequency="daily")
        task3 = Task("Groom", duration_min=20, priority="low", frequency="weekly")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        assert len(pet.get_tasks()) == 3
    
    def test_complete_task(self):
        """Verify that completing a pet's task works correctly."""
        pet = Pet(name="Buddy", pet_type="dog", age=2)
        task = Task("Walk", duration_min=30, priority="high", frequency="daily")
        pet.add_task(task)
        
        assert task.is_complete is False
        pet.complete_task(task)
        assert task.is_complete is True


class TestOwner:
    """Tests for the Owner class."""
    
    def test_add_pet_increases_pet_count(self):
        """Verify that adding a pet to owner increases pet count."""
        owner = Owner(name="John", availability_hours=2.0)
        assert len(owner.get_pets()) == 0
        
        pet = Pet(name="Max", pet_type="dog", age=3)
        owner.add_pet(pet)
        
        assert len(owner.get_pets()) == 1
    
    def test_get_all_tasks_from_owner(self):
        """Verify that owner can retrieve all tasks from all pets."""
        owner = Owner(name="Sarah", availability_hours=3.0)
        
        dog = Pet(name="Max", pet_type="dog", age=3)
        cat = Pet(name="Whiskers", pet_type="cat", age=5)
        
        dog_task = Task("Walk", duration_min=30, priority="high", frequency="daily")
        cat_task = Task("Feed", duration_min=10, priority="high", frequency="daily")
        
        dog.add_task(dog_task)
        cat.add_task(cat_task)
        
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 2
        assert dog_task in all_tasks
        assert cat_task in all_tasks


class TestScheduler:
    """Tests for the Scheduler class and its methods."""
    
    def test_scheduler_generates_schedule(self):
        """Verify that scheduler can generate a schedule from owner's tasks."""
        owner = Owner(name="Alex", availability_hours=2.0)
        pet = Pet(name="Max", pet_type="dog", age=3)
        
        task1 = Task("Walk", duration_min=30, priority="high", frequency="daily")
        task2 = Task("Play", duration_min=20, priority="medium", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()
        
        assert len(schedule) == 2
        assert task1 in schedule
        assert task2 in schedule
    
    def test_scheduler_respects_availability_constraint(self):
        """Verify that scheduler only includes tasks that fit in available time."""
        owner = Owner(name="Bob", availability_hours=0.5)  # 30 minutes
        pet = Pet(name="Spot", pet_type="dog", age=4)
        
        # Add tasks totaling 90 minutes
        task1 = Task("Walk", duration_min=30, priority="high", frequency="daily")
        task2 = Task("Play", duration_min=30, priority="medium", frequency="daily")
        task3 = Task("Feed", duration_min=30, priority="high", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()
        
        # Should only schedule one task (30 min high priority)
        assert len(schedule) == 1
        assert schedule[0].priority == "high"
    
    def test_scheduler_prioritizes_high_priority_tasks(self):
        """Verify that scheduler prioritizes high priority tasks first."""
        owner = Owner(name="Carol", availability_hours=1.0)
        pet = Pet(name="Rex", pet_type="dog", age=2)
        
        high = Task("Medication", duration_min=10, priority="high", frequency="daily")
        medium = Task("Play", duration_min=15, priority="medium", frequency="daily")
        low = Task("Groom", duration_min=20, priority="low", frequency="weekly")
        
        # Add in random order
        pet.add_task(low)
        pet.add_task(high)
        pet.add_task(medium)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()
        
        # High priority should be first
        assert schedule[0] == high
        assert schedule[1] == medium
    
    def test_scheduler_excludes_completed_tasks(self):
        """Verify that scheduler does not include completed tasks in schedule."""
        owner = Owner(name="Diana", availability_hours=2.0)
        pet = Pet(name="Daisy", pet_type="dog", age=1)
        
        task1 = Task("Walk", duration_min=30, priority="high", frequency="daily")
        task2 = Task("Feed", duration_min=10, priority="high", frequency="daily")
        
        task1.mark_complete()  # Mark first task as complete
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()
        
        # Only incomplete task should be in schedule
        assert len(schedule) == 1
        assert schedule[0] == task2


class TestSortingAndFiltering:
    """Tests for sorting and filtering functionality."""
    
    def test_sort_by_time_chronological_order(self):
        """Verify tasks are sorted by scheduled_time in chronological order."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        
        task1 = Task("Morning walk", duration_min=30, priority="high", frequency="daily", scheduled_time="09:00")
        task2 = Task("Feed", duration_min=10, priority="high", frequency="daily", scheduled_time="07:00")
        task3 = Task("Playtime", duration_min=20, priority="medium", frequency="daily", scheduled_time="14:00")
        
        tasks = [task1, task2, task3]
        sorted_tasks = scheduler.sort_by_time(tasks)
        
        assert sorted_tasks[0] == task2  # 07:00
        assert sorted_tasks[1] == task1  # 09:00
        assert sorted_tasks[2] == task3  # 14:00
    
    def test_sort_by_time_handles_unscheduled_tasks(self):
        """Verify unscheduled tasks appear at the end when sorting by time."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        
        task1 = Task("Morning walk", duration_min=30, priority="high", frequency="daily", scheduled_time="09:00")
        task2 = Task("Feed", duration_min=10, priority="high", frequency="daily")  # No scheduled time
        
        tasks = [task2, task1]
        sorted_tasks = scheduler.sort_by_time(tasks)
        
        assert sorted_tasks[0] == task1  # Scheduled task first
        assert sorted_tasks[1] == task2  # Unscheduled task last
    
    def test_filter_tasks_by_pet_name(self):
        """Verify tasks can be filtered by pet name."""
        owner = Owner(name="Test", availability_hours=3.0)
        dog = Pet(name="Max", pet_type="dog", age=3)
        cat = Pet(name="Whiskers", pet_type="cat", age=5)
        
        dog_task = Task("Walk", duration_min=30, priority="high", frequency="daily")
        cat_task = Task("Feed", duration_min=10, priority="high", frequency="daily")
        
        dog.add_task(dog_task)
        cat.add_task(cat_task)
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()
        
        dog_tasks = scheduler.filter_tasks(all_tasks, pet_name="Max")
        assert len(dog_tasks) == 1
        assert dog_task in dog_tasks
        assert cat_task not in dog_tasks
    
    def test_filter_tasks_by_status(self):
        """Verify tasks can be filtered by completion status."""
        owner = Owner(name="Test", availability_hours=3.0)
        pet = Pet(name="Max", pet_type="dog", age=3)
        
        task1 = Task("Walk", duration_min=30, priority="high", frequency="daily")
        task2 = Task("Feed", duration_min=10, priority="high", frequency="daily")
        
        task1.mark_complete()  # Mark first as complete
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()
        
        complete_tasks = scheduler.filter_tasks(all_tasks, status="complete")
        incomplete_tasks = scheduler.filter_tasks(all_tasks, status="incomplete")
        
        assert len(complete_tasks) == 1
        assert task1 in complete_tasks
        assert len(incomplete_tasks) == 1
        assert task2 in incomplete_tasks


class TestConflictDetection:
    """Tests for conflict detection functionality."""
    
    def test_detect_conflicts_same_time(self):
        """Verify scheduler detects tasks scheduled at the exact same time."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        
        task1 = Task("Task A", duration_min=15, priority="high", frequency="once", scheduled_time="09:00")
        task2 = Task("Task B", duration_min=15, priority="high", frequency="once", scheduled_time="09:00")
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        assert len(conflicts) == 1
        assert "CONFLICT" in conflicts[0]
        assert "Task A" in conflicts[0]
        assert "Task B" in conflicts[0]
    
    def test_detect_conflicts_different_times(self):
        """Verify scheduler does not flag conflicts for tasks at different times."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        
        task1 = Task("Task A", duration_min=15, priority="high", frequency="once", scheduled_time="09:00")
        task2 = Task("Task B", duration_min=15, priority="high", frequency="once", scheduled_time="10:00")
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        assert len(conflicts) == 0
    
    def test_detect_conflicts_no_scheduled_time(self):
        """Verify unscheduled tasks don't trigger conflicts."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        
        task1 = Task("Task A", duration_min=15, priority="high", frequency="once")  # No time
        task2 = Task("Task B", duration_min=15, priority="high", frequency="once")  # No time
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        assert len(conflicts) == 0


class TestRecurringTasks:
    """Tests for recurring task functionality."""
    
    def test_create_recurring_task_daily(self):
        """Verify daily tasks create a new occurrence when marked complete."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        pet = Pet(name="Max", pet_type="dog", age=3)
        
        task = Task("Walk", duration_min=30, priority="high", frequency="daily")
        new_task = scheduler.create_recurring_task(task, pet)
        
        assert new_task is not None
        assert new_task.description == "Walk"
        assert new_task.frequency == "daily"
        assert new_task.is_complete is False
    
    def test_create_recurring_task_weekly(self):
        """Verify weekly tasks create a new occurrence when marked complete."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        pet = Pet(name="Max", pet_type="dog", age=3)
        
        task = Task("Grooming", duration_min=60, priority="medium", frequency="weekly")
        new_task = scheduler.create_recurring_task(task, pet)
        
        assert new_task is not None
        assert new_task.description == "Grooming"
        assert new_task.frequency == "weekly"
        assert new_task.is_complete is False
    
    def test_create_recurring_task_once_returns_none(self):
        """Verify one-time tasks don't create new occurrences."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        pet = Pet(name="Max", pet_type="dog", age=3)
        
        task = Task("Vet appointment", duration_min=45, priority="high", frequency="once")
        new_task = scheduler.create_recurring_task(task, pet)
        
        assert new_task is None
    
    def test_recurring_task_preserves_attributes(self):
        """Verify new recurring tasks preserve important attributes from original."""
        scheduler = Scheduler(Owner(name="Test", availability_hours=3.0))
        pet = Pet(name="Max", pet_type="dog", age=3)
        
        task = Task(
            "Walk",
            duration_min=30,
            priority="high",
            frequency="daily",
            scheduled_time="08:00"
        )
        new_task = scheduler.create_recurring_task(task, pet)
        
        assert new_task.duration_min == task.duration_min
        assert new_task.priority == task.priority
        assert new_task.scheduled_time == task.scheduled_time
