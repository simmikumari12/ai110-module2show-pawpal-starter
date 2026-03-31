import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is an intelligent pet care planning assistant. It helps you organize and prioritize care tasks for your pet(s) throughout the day.
"""
)

# Initialize session state for Owner (persists across page refreshes)
if "owner" not in st.session_state:
    st.session_state.owner = None

st.divider()

# ============================================================================
# SECTION 1: Owner Setup
# ============================================================================
st.subheader("👤 Owner Profile")

col1, col2 = st.columns(2)

with col1:
    owner_name = st.text_input(
        "Owner name",
        value="Jordan" if st.session_state.owner is None else st.session_state.owner.name,
        key="owner_name_input"
    )

with col2:
    availability = st.number_input(
        "Daily availability (hours)",
        min_value=0.5,
        max_value=24.0,
        value=3.0 if st.session_state.owner is None else st.session_state.owner.availability_hours,
        key="availability_input"
    )

if st.button("Create/Update Owner", key="create_owner_btn"):
    st.session_state.owner = Owner(name=owner_name, availability_hours=availability)
    st.success(f"✓ Owner profile created: {owner_name} ({availability}h available)")

if st.session_state.owner:
    st.info(f"Currently managing: **{st.session_state.owner.name}** | Available time: **{st.session_state.owner.availability_hours}h/day**")
else:
    st.warning("⚠️ Please create an owner profile first.")

st.divider()

# ============================================================================
# SECTION 2: Manage Pets
# ============================================================================
st.subheader("🐕 Manage Pets")

if st.session_state.owner:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
    with col2:
        pet_type = st.selectbox("Species", ["cat", "dog", "rabbit", "bird", "other"], key="pet_type_select")
    with col3:
        pet_age = st.number_input("Age (years)", min_value=0, max_value=50, value=3, key="pet_age_input")
    
    special_needs = st.text_area("Special needs (optional)", value="", key="special_needs_input", height=60)
    
    if st.button("Add Pet", key="add_pet_btn"):
        new_pet = Pet(
            name=pet_name,
            pet_type=pet_type,
            age=pet_age,
            special_needs=special_needs
        )
        st.session_state.owner.add_pet(new_pet)
        st.success(f"✓ Added {pet_name} ({pet_type}) to your pet family!")
    
    # Display current pets
    if st.session_state.owner.get_pets():
        st.write("**Current Pets:**")
        for idx, pet in enumerate(st.session_state.owner.get_pets()):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"🐾 **{pet.name}** ({pet.pet_type}, age {pet.age})")
            with col2:
                st.write(f"Tasks: {len(pet.get_tasks())}")
            with col3:
                if pet.special_needs:
                    st.caption(f"⚠️ {pet.special_needs}")
    else:
        st.info("No pets yet. Add one above!")

st.divider()

# ============================================================================
# SECTION 3: Manage Tasks
# ============================================================================
st.subheader("📋 Manage Tasks")

if st.session_state.owner and st.session_state.owner.get_pets():
    selected_pet = st.selectbox(
        "Select a pet to add tasks to",
        [pet.name for pet in st.session_state.owner.get_pets()],
        key="pet_selector"
    )
    
    pet_obj = next(p for p in st.session_state.owner.get_pets() if p.name == selected_pet)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        task_desc = st.text_input("Task description", value="Morning walk", key="task_desc_input")
    with col2:
        task_duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30, key="task_duration_input")
    with col3:
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority_select")
    with col4:
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], key="task_frequency_select")
    with col5:
        task_time = st.text_input("Scheduled time (HH:MM)", value="08:00", key="task_time_input", help="e.g., 08:00, 14:30")
    
    if st.button("Add Task", key="add_task_btn"):
        try:
            new_task = Task(
                description=task_desc,
                duration_min=task_duration,
                priority=task_priority,
                frequency=task_frequency,
                scheduled_time=task_time
            )
            pet_obj.add_task(new_task)
            st.success(f"✓ Added task to {pet_obj.name}")
        except Exception as e:
            st.error(f"Error adding task: {str(e)}")
    
    # Display tasks for selected pet
    if pet_obj.get_tasks():
        st.write(f"**Tasks for {pet_obj.name}:**")
        for idx, task in enumerate(pet_obj.get_tasks()):
            status = "✓" if task.is_complete else "○"
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"{status} {task.description} ({task.duration_min}m) - {task.priority.upper()} @ {task.scheduled_time or '—'}")
            with col2:
                if st.button("✓", key=f"complete_task_{idx}", help="Mark complete"):
                    task.mark_complete()
                    st.rerun()
            with col3:
                if st.button("↻", key=f"reset_task_{idx}", help="Mark incomplete"):
                    task.mark_incomplete()
                    st.rerun()
            with col4:
                if st.button("🔄", key=f"recur_task_{idx}", help="Create recurring"):
                    scheduler = Scheduler(st.session_state.owner)
                    new_task = scheduler.create_recurring_task(task, pet_obj)
                    if new_task:
                        pet_obj.add_task(new_task)
                        st.success(f"✓ Created next occurrence")
                        st.rerun()
                    else:
                        st.info("This is a one-time task.")
    else:
        st.info(f"No tasks for {pet_obj.name} yet.")
elif st.session_state.owner:
    st.warning("⚠️ Add a pet first to create tasks.")

st.divider()

# ============================================================================
# SECTION 4: Generate Schedule
# ============================================================================
st.subheader("📅 Today's Schedule")

if st.session_state.owner and st.session_state.owner.get_pets():
    scheduler = Scheduler(st.session_state.owner)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Generate Schedule", key="generate_schedule_btn"):
            schedule = scheduler.generate_schedule()
            st.session_state.schedule_generated = True
            st.session_state.last_schedule = schedule
    
    with col2:
        sort_option = st.selectbox("View", ["By Priority", "By Time", "Filtered", "All Tasks"], key="sort_option")
    
    with col3:
        if sort_option == "Filtered":
            filter_pet = st.selectbox("Filter by pet", [p.name for p in st.session_state.owner.get_pets()], key="filter_pet_select")
    
    # Display schedule if generated
    if hasattr(st.session_state, 'schedule_generated') and st.session_state.schedule_generated:
        schedule = st.session_state.last_schedule
        all_tasks = st.session_state.owner.get_all_tasks()
        
        # Process based on view option
        if sort_option == "By Time":
            tasks_to_show = scheduler.sort_by_time(schedule)
            st.write(f"**Schedule sorted by time ({len(tasks_to_show)} tasks):**")
        elif sort_option == "Filtered":
            tasks_to_show = scheduler.filter_tasks(schedule, pet_name=filter_pet)
            st.write(f"**Schedule filtered for {filter_pet} ({len(tasks_to_show)} tasks):**")
        elif sort_option == "All Tasks":
            tasks_to_show = all_tasks
            st.write(f"**All tasks ({len(tasks_to_show)} total):**")
        else:
            tasks_to_show = schedule
            st.write(f"**Schedule by priority ({len(tasks_to_show)} tasks fit in available time):**")
        
        if tasks_to_show:
            st.success("✓ Schedule generated!")
            
            # Display as table
            schedule_data = []
            total_time = 0
            for i, task in enumerate(tasks_to_show, 1):
                status = "✓ Complete" if task.is_complete else "⏳ Pending"
                schedule_data.append({
                    "#": i,
                    "Task": task.description,
                    "Pet": "—",  # Could be improved to show pet name
                    "Duration": f"{task.duration_min}m",
                    "Priority": task.priority.upper(),
                    "Time": task.scheduled_time or "—",
                    "Status": status
                })
                total_time += task.duration_min
            
            st.table(schedule_data)
            
            # Show time summary
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Time", f"{total_time // 60}h {total_time % 60}m")
            with col2:
                st.metric("Available", f"{st.session_state.owner.availability_hours}h")
            
            # Show conflicts if any
            if scheduler.conflicts:
                st.warning("⚠️ **Scheduling Conflicts Detected:**")
                for conflict in scheduler.conflicts:
                    st.write(f"  {conflict}")
            else:
                st.info("✓ No scheduling conflicts.")
        else:
            st.warning("⚠️ No tasks match the selected filter or fit in available time.")
    else:
        st.info("ℹ️ Click 'Generate Schedule' to see today's plan.")
else:
    st.info("ℹ️ Set up an owner and add pets with tasks to generate a schedule.")
