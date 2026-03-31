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

During implementation, the design evolved significantly from Phase 1 to Phase 6:

**Added in Phase 4:**
- **scheduled_time attribute**: Added HH:MM format time field to Task for chronological scheduling and conflict detection
- **task_id field**: Added unique identifier for tracking recurring task instances
- **New Scheduler methods**: sort_by_time(), filter_tasks(), detect_conflicts(), create_recurring_task()
- **Scheduler.conflicts list**: Track detected scheduling issues

**Rationale for changes:**
- The scheduled_time field enables more intelligent scheduling (time-based sorting, conflict detection) without requiring complex datetime objects
- The task_id field supports recurring task management and tracking
- New methods keep the Scheduler focused as the single "smart" component; all business logic centralized there
- The design remained faithful to the 4-class architecture from Phase 1, confirming the initial UML was well-thought-out

**Key design principle:** Each class has a single responsibility (Task manages its state, Pet manages its tasks, Owner aggregates pets, Scheduler handles all scheduling intelligence). This follows SRP (Single Responsibility Principle) and makes the code maintainable.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two primary mandatory constraints:

1. **Time availability** — Tasks are only scheduled if they fit within the owner's availability_hours. Total scheduled duration cannot exceed available time in minutes. This is non-negotiable; it respects the owner's real-world time limits.

2. **Task priority** — Tasks are ranked as "high", "medium", or "low" and scheduled in that order (high first, then medium, then low). This ensures critical care tasks (medication, feeding) take precedence over optional ones (enrichment, grooming).

Optional constraints (stored but not yet integrated into scheduling):
- **scheduled_time**: Allows checking for time conflicts and potential future time-slot-based scheduling
- **Owner preferences**: Could factor in time-of-day preferences ("morning preferred") into scheduling order

The scheduler processes all pending (incomplete) tasks, sorts them by priority, greedily includes tasks that fit within the time constraint, and checks for conflicts.

**b. Tradeoffs and design decisions**

**Tradeoff 1: Greedy Scheduling vs. Optimization**
- **Current:** Greedy (take highest priority tasks first; include if they fit)
  - ✓ Simple, predictable, fast (O(n))
  - ✗ May skip lower-priority tasks that would fit
- **Alternative:** Bin-packing optimization
  - ✓ Fits more tasks
  - ✗ Complex, unpredictable why tasks chosen
- **Decision:** Greedy better for PawPal+ — predictability matters more than task packing

**Tradeoff 2: Exact Time Matching vs. Duration Overlap Detection**
- **Current:** Exact time matching (warn if same scheduled_time)
  - ✓ Simple, fast warnings to users
  - ✗ Doesn't catch overlapping tasks
- **Alternative:** Interval overlap checking
  - ✓ Catches all real conflicts
  - ✗ More complex logic
- **Decision:** Exact matching sufficient for Phase 2; documented as future improvement

**Tradeoff 3: Recurring Task Instance vs. Template Pattern**
- **Current:** Instance-based (create new Task objects)
  - ✓ Each task is independent, simple to understand
  - ✗ More memory usage
- **Alternative:** Template pattern
  - ✓ Memory efficient
  - ✗ More complex code
- **Decision:** Instance-based better; works well with Streamlit session_state

---

## 3. Algorithmic Implementation (Phase 4)

**a. Core algorithms implemented**

1. **sort_by_time()** — Sorts tasks chronologically by scheduled_time (HH:MM format)
   - Uses lambda key function to parse HH:MM to (h, m) tuples
   - Unscheduled tasks placed at end (treated as 24:00)
   - Complexity: O(n log n)

2. **filter_tasks()** — Filters task list by pet name and/or completion status
   - Supports filtering by status ("complete", "incomplete") or by pet name
   - Uses list comprehensions for readability
   - Complexity: O(n)

3. **detect_conflicts()** — Scans tasks for duplicate scheduled_time values
   - Uses dictionary for O(1) lookups; returns warning messages for collisions
   - Unscheduled tasks don't trigger conflicts
   - Complexity: O(n)

4. **create_recurring_task()** — Generates next occurrence of daily/weekly tasks
   - Copies task attributes; creates fresh Task with is_complete=False
   - One-time tasks return None (no recurrence)
   - Complexity: O(1) per task

**b. Why these algorithms**

- **Sorting by time** improves UX by showing schedule in chronological order
- **Filtering** helps users focus on specific pets or task statuses
- **Conflict detection** prevents scheduling errors; warnings help users resolve conflicts
- **Recurring automation** reduces repetitive data entry for daily/weekly tasks

---

## 4. AI Collaboration (Phases 1-6)

**a. How you used AI at each phase**

1. **Phase 1 - Design:** Asked AI to identify core objects/responsibilities. AI suggested Task/Pet/Owner/Scheduler. ✓ Accepted
2. **Phase 2 - Skeleton:** Asked AI to create dataclass structures. AI suggested dataclasses with default_factory. ✓ Accepted
3. **Phase 3 - UI Integration:** Asked about st.session_state. AI recommended storing Owner directly. ✓ Accepted
4. **Phase 4 - Algorithms:** 
   - Sorting: AI suggested lambda key function for tuples ✓ Accepted
   - Conflict detection: AI suggested dictionary lookup ✓ Accepted
   - Filtering: AI suggested list comprehensions ✓ Accepted
5. **Phase 5 - Tests:** AI drafted test structure and edge cases. ✓ Accepted structure
6. **Phase 6 - Documentation:** AI helped structure README and consolidation. ✓ Accepted framework

**Most helpful prompts:**
- "How should Scheduler retrieve and organize tasks without tight coupling?"
- "What's the Pythonic way to sort by HH:MM format?"
- "What edge cases need testing for a pet scheduler?"
- "How should I structure system documentation?"

**b. Judgment and verification**

**Instance 1: Greedy Scheduling (Phase 2)**
- AI suggested: Greedy approach
- My verification: Wrote tests for priority ordering, constraints, edge cases
- Result: ✓ Tests passed; confirmed correctness

**Instance 2: Session State (Phase 3)**
- AI suggested: Store Owner object directly in st.session_state
- My verification: Manual testing with owner creation, pet addition, page refresh
- Result: ✓ Verified; data persisted correctly

**Instance 3: Recurring Task Creation (Phase 4)**
- AI suggested: Create new Task instances preserving attributes
- My verification: Wrote tests for attribute preservation and is_complete=False
- Result: ✓ Tests passed; logic confirmed

**When I modified AI suggestions:**
1. **filter_tasks()**: Changed from set-based to list-based (Task objects aren't hashable)
2. **Conflict detection scope**: Chose exact time matching over complex overlap detection (sufficient for current phase)

**Summary:** AI excellent for architecture/algorithms; human verification through testing adds confidence before committing.

---

## 5. Testing and Verification (Phase 5)

**a. Test Coverage Expansion**

**Initial (Phase 2):** 12 tests
- Task management (4)
- Pet operations (3)
- Owner aggregation (2)
- Scheduler core (3)

**Expanded (Phase 5):** 24 tests (+12 new)
- TestSortingAndFiltering (4): chronological sorting, pet filtering, status filtering
- TestConflictDetection (3): same-time conflicts, different times, unscheduled tasks
- TestRecurringTasks (4): daily/weekly creation, one-time validation, attribute preservation
- Task scheduled_time (1): time storage and display

**All 24 tests passing** ✓

**b. Confidence Level: ⭐⭐⭐⭐⭐ (Very High - 95%)**

System correctly:
- ✓ Manages task state transitions
- ✓ Aggregates data across pets/owners
- ✓ Generates schedules respecting constraints
- ✓ Prioritizes tasks correctly (high→medium→low)
- ✓ Filters completed tasks
- ✓ Sorts chronologically
- ✓ Detects conflicts
- ✓ Creates recurring instances
- ✓ Handles edge cases (empty lists, unscheduled tasks)
- ✓ UI integrates correctly

**Why very high (not perfect):**
- All base functionality covered
- CLI demo runs with 6 feature demonstrations
- UI tested through Streamlit
- Main use cases verified end-to-end

**Future gaps:**
- Overlapping duration detection
- Recurring task date calculations
- JSON persistence
- Large-scale performance
- Concurrent access testing

---

## 6. Final Reflection (Phases 1-6)

**a. What went really well**

1. **UML-first approach (Phase 1)** — Clear design saved ~50% of coding time. Skeleton mapped 1:1 to implementation. No rework needed.

2. **Incremental integration** — Separating CLI (main.py) → UI (app.py) → Algorithms caught issues early. Each phase independently testable.

3. **Test-driven confidence** — 24-test suite gave genuine confidence, not hope. All tests passing before committing code.

4. **Clear responsibilities** — Each class has ONE job (Task: state, Pet: tasks, Owner: aggregation, Scheduler: intelligence). Maintainable and extensible.

5. **Documentation discipline** — Updated README/reflection as I built (not after). Kept context fresh.

**b. What would improve with more time**

1. **JSON persistence (Challenge 2)** — Save/load owner/pet/task data between sessions
2. **Advanced scheduling** — Duration overlap detection, timedelta for recurring dates
3. **UI polish** — Emojis, color coding, drag-to-reorder
4. **Extended filtering** — Time ranges, duration filters, completion stats
5. **Performance** — Indexing for O(1) lookups, lazy loading, schedule caching
6. **External integration** — Google Calendar sync, mobile app, Slack notifications

**c. Key Takeaways**

1. **Design-first beats code-first by 10x.** UML upfront saved massive debugging later.

2. **Testing is the only confidence mechanism.** Tests ARE evidence the system works.

3. **Verify AI suggestions; verify before accepting.** AI excellent for architecture; humans verify through testing.

4. **Incremental integration beats big-bang.** CLI demo (main.py) before UI (app.py) caught problems early.

5. **Document decisions, not just code.** "Why greedy scheduling?" explained matters more than code itself.

6. **Ship working prototypes; refine iteratively.** PawPal+ went from zero → functionality in 6 phases, each delivering real value.

---

**Project Status:** Phase 6 Complete ✓ | All 24 tests passing | UI + CLI demo working | Documentation complete | Ready for user testing
