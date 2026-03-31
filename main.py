"""
PawPal+ Demo Script

This script demonstrates the core PawPal+ functionality:
- Creating an owner and pets
- Adding tasks with different priorities
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
    
    # Create tasks for the dog
    dog_walk = Task(
        description="Morning walk",
        duration_min=30,
        priority="high",
        frequency="daily"
    )
    dog_feeding = Task(
        description="Feed Max",
        duration_min=10,
        priority="high",
        frequency="daily"
    )
    dog_playtime = Task(
        description="Playtime with Max",
        duration_min=20,
        priority="medium",
        frequency="daily"
    )
    
    # Create tasks for the cat
    cat_feeding = Task(
        description="Feed Whiskers",
        duration_min=10,
        priority="high",
        frequency="daily"
    )
    cat_litter = Task(
        description="Clean litter box",
        duration_min=15,
        priority="medium",
        frequency="daily"
    )
    cat_grooming = Task(
        description="Brush Whiskers",
        duration_min=20,
        priority="low",
        frequency="weekly"
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
    
    # Display today's schedule
    print(scheduler.get_today_schedule())
    
    # Demonstrate task completion
    print("\n" + "=" * 50)
    print("Marking tasks as complete...\n")
    dog_walk.mark_complete()
    dog_feeding.mark_complete()
    
    print(scheduler.get_today_schedule())
    
    # Display all pets and their task counts
    print("\n" + "=" * 50)
    print("Pet Information:\n")
    for pet in owner.get_pets():
        print(f"{pet.name} ({pet.pet_type}):")
        print(f"  - Age: {pet.age} years old")
        print(f"  - Special needs: {pet.special_needs}")
        print(f"  - Number of tasks: {len(pet.get_tasks())}")
        print()


if __name__ == "__main__":
    main()
