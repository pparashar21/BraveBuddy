import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar
import time
import streamlit as st
from PIL import Image


# Initialize session state for page navigation, user info, and tasks
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'first_name' not in st.session_state:
    st.session_state.first_name = ""
if 'age' not in st.session_state:
    st.session_state.age = 0
if 'language' not in st.session_state:
    st.session_state.language = ""
if 'gender' not in st.session_state:
    st.session_state.gender = ""
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = pd.DataFrame(columns=["Task", "Frequency", "Next Reminder", "Actual Date", "Start Time", "End Time", "All Day"])

# Function to set the background color
def set_background_color(color):
    st.markdown(f"<style>body {{background-color: {color};}}</style>", unsafe_allow_html=True)


# Function to set the background color
def set_background_color(color):
    st.markdown(f"<style>body {{background-color: {color};}}</style>", unsafe_allow_html=True)

# Function for login page
def login_page():
    set_background_color("#f0f2f5")  # Light gray background
    st.title("Login Page", anchor="login")

    # Create two columns for layout
    col1, col2 = st.columns([1, 1])  # Adjust width ratio if needed

    # Place the image in the first column
    with col1:
        img = Image.open("file.png")
        # Define a scale factor, e.g., 0.5 to reduce the image size by half
        scale_factor = 0.5
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))

        # Resize the image
        scaled_img = img.resize(new_size)

        # Display the scaled image
        st.image(scaled_img, use_column_width=True)  # `use_column_width=True` fits it to the column width

    # Place the login form in the second column
    with col2:
        # Create a form for better layout
        with st.form("login_form"):
            first_name = st.text_input("Enter your first name", placeholder="John")
            age = st.number_input("Enter your age", min_value=2, max_value=10, step=1, value=5)
            language = st.selectbox("Select your language", options=["English", "Spanish", "French", "German", "Other"])
            gender = st.radio("Select your gender", options=["Male", "Female"])
            password = st.text_input("Enter your password", type="password")  # Password field

            # Login button
            submitted = st.form_submit_button("Login")
            if submitted:
                if first_name and age and language and gender and password:
                    # Consolidate information into a single dictionary, including password
                    user_info = {
                        "first_name": first_name,
                        "age": age,
                        "language": language,
                        "gender": gender,
                        "password": password  # Add password to user info
                    }
                    # Store user information in session state
                    st.session_state.update(user_info)
                    st.session_state.is_logged_in = True
                    st.success("Successfully logged in!")  # Confirmation message
                else:
                    st.error("Please enter all fields: first name, age, language, gender, and password.")


# Function to calculate next reminder date based on frequency
def calculate_next_reminder(frequency):
    if frequency == "Daily":
        return datetime.now() + timedelta(days=1)
    elif frequency == "Weekly":
        return datetime.now() + timedelta(weeks=1)
    elif frequency == "Monthly":
        return datetime.now() + timedelta(days=30)
    elif frequency == "Yearly":
        return datetime.now() + timedelta(days=365)
    else:
        return None

def format_time(hour, minute, period):
    return f"{hour}:{minute:02} {period}"

def welcome_page():
    st.empty()
    set_background_color("#f0f2f5")  # Light gray background
    st.title("Welcome Page", anchor="welcome")
    st.write(f"**Welcome, {st.session_state.first_name}!**")
    st.write(f"You are **{st.session_state.age} years old.**")
    st.write(f"**Language:** {st.session_state.language}")
    st.write(f"**Gender:** {st.session_state.gender}")

    # Real-time clock display
    st.subheader("Current Time")
    clock_placeholder = st.empty()  # Placeholder for the clock

    # Reminder app functionality
    st.subheader("Task Reminder App")

    # Task creation section
    task_name = st.text_input("Task Name", "")
    frequency = st.selectbox("Set Reminder Frequency", ["None", "Daily", "Weekly", "Monthly", "Yearly"])
    actual_date = st.date_input("Select Actual Date", value=datetime.today())

    # Start time input
    start_hour, start_minute, start_period = st.columns(3)
    with start_hour:
        start_hour_value = st.selectbox("Start Hour", list(range(1, 13)), key="start_hour")
    with start_minute:
        start_minute_value = st.selectbox("Start Minute", list(range(0, 60)), key="start_minute")
    with start_period:
        start_period_value = st.selectbox("AM/PM", ["AM", "PM"], key="start_period")

    # End time input
    end_hour, end_minute, end_period = st.columns(3)
    with end_hour:
        end_hour_value = st.selectbox("End Hour", list(range(1, 13)), key="end_hour")
    with end_minute:
        end_minute_value = st.selectbox("End Minute", list(range(0, 60)), key="end_minute")
    with end_period:
        end_period_value = st.selectbox("AM/PM", ["AM", "PM"], key="end_period")

    all_day = st.checkbox("All Day Event")

    # Add Task button
    if st.button("Add Task"):
        if task_name:
            if all_day:
                start_datetime = pd.to_datetime(actual_date)  # Set start time as the date
                end_datetime = pd.to_datetime(actual_date) + timedelta(days=1)  # End time for "All Day" event is the next day
            else:
                # Convert to 24-hour format
                start_time_str = f"{start_hour_value} {start_period_value}"
                end_time_str = f"{end_hour_value} {end_period_value}"

                # Create datetime objects
                start_datetime = pd.to_datetime(f"{actual_date} {start_time_str}")
                end_datetime = pd.to_datetime(f"{actual_date} {end_time_str}")

            if frequency != "None":
                next_reminder = calculate_next_reminder(frequency)
            else:
                next_reminder = start_datetime  # Use start time as the reminder if no frequency

            new_task = pd.DataFrame({
                "Task": [task_name],
                "Frequency": [frequency if frequency != "None" else "One-Time"],  # Label as "One-Time"
                "Next Reminder": [pd.to_datetime(next_reminder)],  # Ensure this is a datetime object
                "Actual Date": [pd.to_datetime(actual_date)],  # Ensure this is a datetime object
                "Start Time": [format_time(start_hour_value, start_minute_value, start_period_value)],
                "End Time": [format_time(end_hour_value, end_minute_value, end_period_value)],
                "All Day": [all_day]  # Store whether it's an all-day event
            })
            st.session_state['tasks'] = pd.concat([st.session_state['tasks'], new_task], ignore_index=True)
            st.success("Task added successfully!")
        else:
            st.error("Please enter a task name.")

    # Display upcoming reminders
    st.subheader("Upcoming Reminders")
    today = pd.to_datetime(datetime.now().date())  # Ensure today is in datetime format

    # Convert 'Next Reminder' to datetime to ensure proper filtering
    st.session_state['tasks']['Next Reminder'] = pd.to_datetime(st.session_state['tasks']['Next Reminder'], errors='coerce')
    upcoming_reminders = st.session_state['tasks'][st.session_state['tasks']['Next Reminder'] >= today]  # Ensure comparison is valid

    # Drop NaN values in 'Next Reminder'
    upcoming_reminders = upcoming_reminders.dropna(subset=['Next Reminder'])

    # Add a calendar
    st.subheader("Task Calendar")
    calendar_date = st.date_input("Select Date to View Tasks", value=today)

    # Create a list to hold task details for the selected date
    tasks_for_selected_date = upcoming_reminders[upcoming_reminders['Next Reminder'].dt.date == calendar_date]

    # Display calendar with dots for tasks
    month_days = calendar.monthcalendar(calendar_date.year, calendar_date.month)

    for week in month_days:
        cols = st.columns(7)  # Create 7 columns for the days of the week
        for day in week:
            if day == 0:
                cols[week.index(day)].write("")  # Empty day
            else:
                current_day = datetime(calendar_date.year, calendar_date.month, day)
                tasks_on_day = upcoming_reminders[upcoming_reminders['Next Reminder'].dt.date == current_day.date()]
                if not tasks_on_day.empty:
                    cols[week.index(day)].markdown(f"<span style='color:red;'>•</span> **{day}**", unsafe_allow_html=True)  # Dot for task
                else:
                    cols[week.index(day)].write(f"{day}")  # Just the day number

    # Show tasks for the selected date
    if not tasks_for_selected_date.empty:
        st.subheader(f"Tasks on {calendar_date}")
        for index, task in tasks_for_selected_date.iterrows():
            st.write(f"- **{task['Task']}**: {task['Start Time']} to {task['End Time']}")
    else:
        st.write("No tasks scheduled for this day.")

    # Check if tasks are available
    if 'tasks' in st.session_state and not st.session_state['tasks'].empty:
    # Initialize task_to_delete with None
      task_to_delete = None

    task_options = st.session_state['tasks']['Task'].tolist()
    task_to_delete = st.selectbox("Select a task to delete", options=task_options)
    
    if task_to_delete is not None:
      if st.button("Delete Task"):
          # Delete the selected task
          st.session_state['tasks'] = st.session_state['tasks'][st.session_state['tasks']['Task'] != task_to_delete].reset_index(drop=True)
          st.success(f"Task '{task_to_delete}' deleted successfully!")
    else:
      st.warning("No tasks available to delete.")



    # Real-time clock update
    while True:
        clock_placeholder.text(datetime.now().strftime("%H:%M:%S"))
        time.sleep(1)


# Page navigation
# login_page()
if st.session_state.is_logged_in:
  welcome_page()
else:
  login_page()

