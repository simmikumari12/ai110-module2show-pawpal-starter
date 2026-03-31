"""
PawPal+ Demo Script

This script demonstrates the core PawPal+ functionality:
- Creating an owner and pets
- Adding tasks with different priorities and scheduled times
- Sorting and filtering tasks
- Detecting scheduling conflicts
- Handling recurring tasks
- Generating and displaying a daily schedule
"""

from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    """Run a demo of the PawPal+ system."""
    
    # Create an owner
    owner = Owner(
        name="Alex",
        availability_hours=3.0,  # 3 hours available for pet care today
        preferences={"morning_preferred": True}
    )
    
    # Create two pets
    dog = Pet(name="Max", pet_type="dog", age=3, special_needs="Needs daily walks")
    cat = Pet(name="Whiskers", pet_type="cat", age=5, special_needs="Prefers quiet mornings")
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Create tasks for the dog with scheduled times
    dog_walk = Task(
        description="Morning walk",
        duration_min=30,
        priority="high",
        frequency="daily",
        scheduled_time="08:00"
    )
    dog_feeding = Task(
        description="Feed Max",
        duration_min=10,
        priority="high",
        frequency="daily",
        scheduled_time="07:00"
    )
    dog_playtime = Task(
        description="Playtime with Max",
        duration_min=20,
        priority="medium",
        frequency="daily",
        scheduled_time="14:00"
    )
    
    # Create tasks for the cat
    cat_feeding = Task(
        description="Feed Whiskers",
        duration_min=10,
        priority="high",
        frequency="daily",
        scheduled_time="07:30"
    )
    cat_litter = Task(
        description="Clean litter box",
        duration_min=15,
        priority="medium",
        frequency="daily",
        scheduled_time="09:00"
    )
    cat_grooming = Task(
        description="Brush Whiskers",
        duration_min=20,
        priority="low",
        frequency="weekly",
        scheduled_time="10:00"
    )
    
    # Add tasks to pets
    dog.add_task(dog_walk)
    dog.add_task(dog_feeding)
    dog.add_task(dog_playtime)
    
    cat.add_task(cat_feeding)
    cat.add_task(cat_litter)
    cat.add_task(cat_grooming)
    
    # Create scheduler
    scheduler = Scheduler(owner)
    
    # ========================================================================
    # DEMO 1: Display today's schedule
    # ========================================================================
    print("\n" + "=" * 70)
    print("DEMO 1: Today's Schedule")
    print("=" * 70)
    print(scheduler.get_today_schedule())
    
    # ========================================================================
    # DEMO 2: Sort tasks by scheduled time
    # ========================================================================
    print("\n" + "=" * 70)
    print("DEMO 2: Tasks sorted by scheduled time")
    print("=" * 70)
    all_tasks = owner.get_all_tasks()
    sorted_by_time = scheduler.sort_by_time(all_tasks)
    print(f"\nAll tasks sorted by time ({len(sorted_by_time)} total):")
    for task in sorted_by_time:
        print(f"  {task}")
    
    # ========================================================================
    # DEMO 3: Filter tasks by pet and status
    # ========================================================================
    print("\n" + "=" * 70)
    print("DEMO 3: Filtering tasks")
    print("=" * 70)
    
    # Filter tasks for Max only
    max_tasks = scheduler.filter_tasks(all_tasks, pet_name="Max")
    print(f"\nTasks for Max ({len(max_tasks)} tasks):")
    for task in max_tasks:
        print(f"  {task}")
    
    # Filter incomplete tasks only
    incomplete_tasks = scheduler.filter_tasks(all_tasks, status="incomplete")
    print(f"\nIncomplete tasks ({len(incomplete_tasks)} tasks):")
    for task in incomplete_tasks:
        print(f"  {task}")
    
    # ========================================================================
    # DEMO 4: Conflict detection
    # ========================================================================
    print("\n" + "=" * 70)
    print("DEMO 4: Conflict detection")
    print("=" * 70)
    
    # Create two tasks at the same time to demonstrate conflict detection
    conflict_task1 = Task("Task A", 15, "high", "once", scheduled_time="09:00")
    conflict_task2 = Task("Task B", 15, "high", "once", scheduled_time="09:00")
    conflict_task3 = Task("Task C", 15, "low", "once", scheduled_time="10:00")
    
    test_tasks = [conflict_task1, conflict_task2, conflict_task3]
    conflicts = scheduler.detect_conflicts(test_tasks)
    
    if conflicts:
        print("\n⚠️ Conflicts detected:")
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("\n✓ No conflicts detected.")
    
    # ========================================================================
    # DEMO 5: Task completion and recurrence
    # ========================================================================
    print("\n" + "=" * 70)
    print("DEMO 5: Task completion and recurrence")
    print("=" * 70)
    
    print("\nMarking tasks as complete...")
    dog_walk.mark_complete()
    dog_feeding.mark_complete()
    
    # Create new recurring tasks
    print("\nCreating recurring tasks for completed daily tasks...")
    if dog_walk.frequency in ["daily", "weekly"]:
        new_walk = scheduler.create_recurring_task(dog_walk, dog)
        if new_walk:
            print(f"  ✓ Created new task: {new_walk.description} (tomorrow)")
            dog.add_task(new_walk)
    
    if dog_feeding.frequency in ["daily", "weekly"]:
        new_feeding = scheduler.create_recurring_task(dog_feeding, dog)
        if new_feeding:
            print(f"  ✓ Created new task: {new_feeding.description} (tomorrow)")
            dog.add_task(new_feeding)
    
    # Display updated schedule
    print("\nUpdated schedule after task completion:")
    print(scheduler.get_today_schedule())
    
    # ========================================================================
    # DEMO 6: Pet and task summary
    # ========================================================================
    print("\n" + "=" * 70)
    print("DEMO 6: Pet Information Summary")
    print("=" * 70)
    for pet in owner.get_pets():
        complete_count = sum(1 for t in pet.get_tasks() if t.is_complete)
        total_count = len(pet.get_tasks())
        print(f"\n🐾 {pet.name} ({pet.pet_type}):")
        print(f"   Age: {pet.age} years old")
        print(f"   Special needs: {pet.special_needs}")
        print(f"   Tasks: {complete_count} complete, {total_count - complete_count} remaining (total: {total_count})")


if __name__ == "__main__":
    main()

