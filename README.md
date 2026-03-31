# PawPal+ (Module 2 Project)

**PawPal+** is an intelligent pet care planning assistant built with Python and Streamlit. It helps busy pet owners prioritize and organize daily care tasks for their pets.

## 🎯 Features

### Core Functionality
- **Owner & Pet Management**: Create and manage multiple pet profiles with special care needs
- **Task Tracking**: Add tasks with duration, priority level (high/medium/low), and frequency (daily/weekly/once)
- **Priority-Based Scheduling**: Generates daily schedules that prioritize high-urgency tasks first
- **Time Constraints**: Respects owner's available time per day; only includes tasks that fit

### Algorithmic Features (Phase 4)
- **Chronological Sorting**: Sort tasks by scheduled time (HH:MM format)
- **Flexible Filtering**: Filter tasks by pet name, completion status, or custom criteria
- **Conflict Detection**: Identifies when multiple tasks are scheduled at the same time (warning system)
- **Recurring Tasks**: Automatically creates next occurrences of daily/weekly tasks marked as complete

### Testing & Verification
- **24 Comprehensive Tests**: Unit tests covering all core behaviors, edge cases, and new algorithms
- **Confidence Level**: ⭐⭐⭐⭐⭐ (High) — All tests passing; system verified for core use cases

## 📋 Architecture

### Classes (pawpal_system.py)
- **Task**: Represents a single pet care activity with attributes (description, duration, priority, frequency, scheduled_time)
- **Pet**: Stores pet information and manages a list of tasks
- **Owner**: Manages multiple pets and provides task aggregation
- **Scheduler**: The intelligence layer — generates optimized schedules with prioritization and conflict detection

### System Diagram
```
Owner (1) --has--> Pet (*)
  |
  +--manages--> Scheduler
  
Pet (1) --contains--> Task (*)
```

## 🚀 Getting Started

### Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
# Start Streamlit UI
streamlit run app.py

# Run demo script (CLI)
python main.py

# Run tests
python -m pytest tests/test_pawpal.py -v
```

## 🏗️ Implementation Timeline

### Phase 1: System Design ✓
- Brainstormed 4-class architecture (Task, Pet, Owner, Scheduler)
- Created UML class diagram with relationships
- Built dataclass skeletons with method stubs
- Documented initial design in reflection.md

### Phase 2: Core Implementation ✓
- Implemented all class methods (add_pet, add_task, mark_complete, etc.)
- Built priority-based scheduling with time constraints
- Created main.py demo script
- Added 12 unit tests (all passing)

### Phase 3: UI and Backend Integration ✓
- Imported classes into app.py
- Implemented st.session_state for data persistence
- Wired UI buttons to class methods
- Built interactive owner/pet/task management interface

### Phase 4: Algorithmic Layer ✓
- Added scheduled_time (HH:MM) attribute to Task
- Implemented sort_by_time() for chronological ordering
- Implemented filter_tasks() for flexible filtering
- Implemented detect_conflicts() for scheduling collision detection
- Implemented create_recurring_task() for daily/weekly task automation
- Expanded main.py demo with 6 feature demonstrations

### Phase 5: Testing and Verification ✓
- Expanded test suite from 12 to 24 tests
- Added TestSortingAndFiltering (4 tests)
- Added TestConflictDetection (3 tests)
- Added TestRecurringTasks (4 tests)
- All tests passing with 100% success rate

### Phase 6: UI Polish and Documentation ✓
- Enhanced Streamlit UI with scheduled time management
- Added sorting/filtering views in schedule display
- Added conflict warning display
- Added recurring task creation button
- Updated README with features and test results
- Completed reflection.md with design decisions and tradeoffs

## 📊 Testing PawPal+

### Run All Tests
```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage
- **Task Management**: Completion tracking, state transitions, string representation
- **Pet Operations**: Task addition, multi-task handling, completion
- **Owner Aggregation**: Pet management, cross-pet task retrieval
- **Scheduler Core**: Schedule generation, priority ordering, availability constraints
- **Sorting**: Chronological ordering, unscheduled task handling
- **Filtering**: By pet name, by completion status, filter combinations
- **Conflict Detection**: Same-time detection, different-time validation, unscheduled tasks
- **Recurring Tasks**: Daily/weekly creation, one-time validation, attribute preservation

### Confidence Level: ⭐⭐⭐⭐⭐

**Why high confidence:**
- ✓ All 24 tests passing
- ✓ Edge cases covered (empty lists, unscheduled tasks, conflicts)
- ✓ Demo script runs without errors
- ✓ UI integration tested with multiple scenarios
- ✓ Scheduling logic verified through multiple code paths

**Future test areas:**
- Overlapping duration detection (not just exact time matches)
- Recurring task date calculations with timedelta
- JSON persistence for data saving
- Owner preference integration with scheduling

## 🎨 UI Features

### Main Sections
1. **Owner Profile**: Set name and daily availability
2. **Pet Management**: Add/view pets with special needs tracking
3. **Task Management**: Add tasks with priority and scheduled time; mark complete/recur
4. **Schedule View**: Generate and view schedules by priority, time, or pet

### Smart Features
- ✓ Persistent session state across page refreshes
- ✓ Real-time task updates
- ✓ Conflict warnings when tasks overlap
- ⏳ Scheduling time validation
- 🔄 One-click recurring task creation

## 📝 Project Reflection

### Key Design Decisions

1. **Greedy Scheduling Algorithm**: Prioritizes high→medium→low, includes tasks that fit. Trade-off: simple and predictable, but may not pack every task.

2. **Task Uniqueness**: Uses object equality rather than task IDs for simplicity, trades some flexibility for clean code.

3. **Scheduled Time as String**: HH:MM format allows for sorting/display without complex datetime objects until persistence needed.

### AI Collaboration

- Used AI for UML brainstorming, class skeleton generation, and algorithm implementation
- Verified critical components (greedy scheduler) through testing before acceptance
- Maintained human oversight on design decisions (tradeoffs, complexity)

### Lessons Learned

1. **Design-First Wins**: Investing in clear UML before coding saved significant debugging time
2. **Test-Driven Confidence**: Writing tests immediately after implementation ensured correctness
3. **Incremental Integration**: Separating CLI testing (main.py) from UI testing (app.py) caught integration issues early
4. **Clear Tradeoffs**: Documenting why simpler solutions were chosen over complex ones aids future maintenance

## 🔄 Workflow

The project follows a structured 6-phase workflow:

1. **Design** (UML)
2. **Core Implementation** (Classes & Logic)
3. **UI Integration** (Streamlit)
4. **Algorithms** (Filtering, Sorting, Conflicts)
5. **Testing** (Unit & Integration)
6. **Polish** (UI Refinement & Documentation)

This systematic approach ensures that business logic is solid before UI work, and all components are verified through testing before deployment.

---

**Built with:** Python 3.11 · Streamlit · pytest · Dataclasses

**Author:** Simmi Kumari

