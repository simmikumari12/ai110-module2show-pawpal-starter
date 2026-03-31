# PawPal+ Project Reflection

## 1. System Design

**a. Core User Actions**

The app enables three primary user interactions:

1. **Add and manage pet & owner information** — Users can enter and store basic details about themselves (availability, preferences) and their pet (name, type, age, special needs), which inform the daily schedule.

2. **Create and edit pet care tasks** — Users can add tasks (e.g., feeding, walks, medication, enrichment) with properties like duration and priority level so the scheduler understands what needs to happen and how urgent each task is.

3. **View today's scheduled plan** — The app generates and displays an optimized daily schedule that fits all tasks into the owner's available time, prioritizes based on importance, and explains why tasks were scheduled in that order.

**b. Initial design**

The initial UML design includes four core classes:

1. **Task** — Represents a single pet care activity with attributes (description, duration_min, priority, frequency, is_complete) and methods to mark tasks complete/incomplete. This keeps task state isolated and simple.

2. **Pet** — Represents a single pet, storing pet details (name, type, age, special_needs) and managing a list of tasks. Methods include add_task(), get_tasks(), and complete_task() to manage the pet's care schedule.

3. **Owner** — Represents the pet owner with attributes for name, availability_hours (how much time they have per day), preferences, and a list of pets. Methods include add_pet(), get_pets(), and get_all_tasks() to provide access to all pet information.

4. **Scheduler** — The core orchestration engine that receives an Owner instance and generates optimized daily schedules. Key methods include generate_schedule() (which retrieves all tasks and prioritizes them) and organize_tasks_by_priority() (which sorts tasks by urgency).

The relationships are: Owner has multiple Pets, each Pet contains multiple Tasks, and the Scheduler manages access to an Owner's data to produce a feasible daily plan.

Responsibilities: Task handles its own state (complete/incomplete), Pet manages its tasks, Owner aggregates pets, and Scheduler orchestrates the planning logic.

**c. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
