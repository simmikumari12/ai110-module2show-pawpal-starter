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

During implementation, the design remained very close to the initial UML, which validated the planning phase. However, one minor refinement was made:

- **Task storage simplification**: Instead of using task IDs for tracking completion, we store Task objects directly and use object equality for comparisons. This simplified the code and reduced the chance of ID-mapping bugs, while still maintaining full functionality for marking tasks complete/incomplete.

The decision to use Python dataclasses for Task and Pet proved excellent for keeping the code clean and maintainable. The Scheduler's constraint checking (respecting owner's availability_hours) became the critical logic hub, successfully filtering tasks that fit within available time.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two primary constraints:

1. **Time availability** — Tasks are only scheduled if they fit within the owner's availability_hours. Total scheduled duration cannot exceed available time in minutes.
2. **Task priority** — Tasks are ranked as "high", "medium", or "low" and scheduled in that order (high first, then medium, then low).

The scheduler processes all pending (incomplete) tasks, sorts them by priority level, and greedily includes tasks that fit within the time constraint. This ensures important tasks get scheduled first.

**b. Tradeoffs**

One key tradeoff in the scheduler is **greedy scheduling vs. optimization**. The current scheduler uses a greedy approach (take best priority task first, if it fits), which is simple and predictable. However, it may occasionally skip low-priority tasks that would fit if high-priority tasks were reordered. A more complex optimization algorithm could pack more tasks but would be harder to understand and explain to the user. For PawPal+'s use case (a busy pet owner wanting clarity), the greedy approach is reasonable because predictability and explainability are more important than squeezing in every possible task.

---

## 3. AI Collaboration

**a. How you used AI**

The AI tool was used throughout the project to:

1. **Design brainstorming** — Identified the four core classes (Task, Pet, Owner, Scheduler) and their responsibilities using the project requirements.
2. **UML visualization** — Generated a Mermaid class diagram to document relationships and confirm that the design made sense before coding.
3. **Code skeleton generation** — Created the initial method stubs using Python dataclasses, establishing a clear contract for implementation.
4. **Implementation** — Implemented full class logic, including the critical scheduling algorithm that respects time constraints and task priorities.
5. **Test generation** — Created 12 comprehensive test cases covering task completion, pet management, owner aggregation, and scheduler constraints.

**Most helpful prompts**: "Based on the UML, what methods should each class have?" and "How should the Scheduler retrieve and organize tasks?"

**b. Judgment and verification**

One instance where independent verification was essential: the scheduler's greedy algorithm. The AI suggested a greedy approach (sort by priority and include tasks in order), but I verified this would work correctly by:
1. Running the demo script (main.py) with multiple tasks and observing the output.
2. Writing tests for edge cases: tasks exceeding availability, priority ordering, completed task exclusion.
3. Confirming all 12 tests passed before committing.

This gave confidence that the scheduling logic was sound before moving forward.

---

## 4. Testing and Verification

**a. What you tested**

12 test cases were created covering:

1. **Task completion** (3 tests) — Ensuring mark_complete(), mark_incomplete(), and string representation work correctly.
2. **Pet management** (3 tests) — Verifying add_task(), multiple task handling, and task completion on pets.
3. **Owner aggregation** (2 tests) — Confirming pets can be added and all tasks retrieved from all pets.
4. **Scheduler logic** (4 tests) — Testing schedule generation, availability constraints, priority ordering, and completed task exclusion.

These tests were important because they verify the core invariants: tasks track state correctly, pets aggregate tasks, and the scheduler makes intelligent decisions about which tasks fit.

**b. Confidence**

Confidence level: **High** (90%)

The system correctly:
- Manages task state transitions (complete/incomplete)
- Aggregates data across pets and owners
- Generates schedules that respect time constraints
- Prioritizes tasks by level
- Filters completed tasks from schedules

**Edge cases to test with more time**:
- Recurring tasks (frequency="daily" vs "weekly") — currently not used in scheduling
- Tie-breaking when multiple tasks have the same priority and duration
- Very tight time constraints (e.g., 5 min availability with 10 min tasks)
- Empty task lists and owner with no pets
- Float precision issues with availability_hours calculations

---

## 5. Reflection

**a. What went well**

The **UML-first approach** was the most satisfying part. By investing time in clear design before coding, the implementation was straightforward. The dataclass-based skeleton was easy to fill in with logic. The Scheduler's constraint-checking algorithm is clean and understandable, making it easy to verify correctness through tests.

**b. What you would improve**

1. **Recurring task logic**: The frequency field is stored but not used in scheduling. A real system would need to handle "daily" vs "weekly" tasks differently.
2. **Task descriptions in schedule**: The output could include reasoning (e.g., "High priority - medication") to help users understand why tasks were scheduled in that order.
3. **Owner preferences**: The Owner stores a preferences dict but it's not used by the scheduler. Time-of-day preferences ("morning preferred") could be factored into the schedule.

**c. Key takeaway**

**Design before coding beats coding without a plan.** The UML diagram caught potential confusion about relationships (e.g., how Scheduler accesses tasks) before writing a single line of code. This saved debugging time later. Pair this with **test-driven verification** — writing tests as soon as implementation is done ensured confidence in the system's behavior, not just its structure. For future projects, the combination of clear design + immediate testing is a powerful workflow.
