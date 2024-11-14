import os
import json
import streamlit as st
from datetime import datetime, timedelta

# Set up page configuration and title
st.set_page_config(page_title="IIIT Sonepat Examination Management System", layout="wide")
st.title("IIIT Sonepat Examination Management System")
st.write("Design and Developed by Dr. Mukesh Mann")

# Directory setup for uploads and academic calendar
upload_dir = "D:/Exam_management_iiit/uploads"
calendar_dir = "D:/Exam_management_iiit/academiccalendar"
os.makedirs(upload_dir, exist_ok=True)
os.makedirs(calendar_dir, exist_ok=True)

# Path for academic calendar JSON file
calendar_file_path = os.path.join(calendar_dir, "academic_calendar.json")

# Load academic calendar from JSON file
def load_calendar_from_file():
    if os.path.exists(calendar_file_path):
        with open(calendar_file_path, "r") as file:
            return json.load(file)
    return []

# Save academic calendar to JSON file
def save_calendar_to_file(calendar):
    with open(calendar_file_path, "w") as file:
        json.dump(calendar, file, indent=4)

# Initialize session state for admin login, academic calendar, and notification dismissal
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False
if "academic_calendar" not in st.session_state:
    st.session_state["academic_calendar"] = load_calendar_from_file()
if "notification_dismissed" not in st.session_state:
    st.session_state["notification_dismissed"] = False  # Track if user has dismissed notifications

# Function to display refined academic calendar with countdown and organization
def display_academic_calendar():
    today = datetime.now().date()
    
    # Split activities into categories based on date
    upcoming_activities = []
    ongoing_activities = []
    past_activities = []
    
    for event in sorted(st.session_state["academic_calendar"], key=lambda x: x["start_date"]):
        activity = event["activity"]
        start_date = datetime.strptime(event["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(event["end_date"], "%Y-%m-%d").date() if event["end_date"] else None
        days_remaining = (start_date - today).days
        
        if end_date and end_date < today:
            past_activities.append((activity, start_date, end_date, "Ended"))
        elif start_date <= today <= (end_date or today):
            ongoing_activities.append((activity, start_date, end_date, "Ongoing"))
        else:
            countdown_text = f"{days_remaining} days remaining" if days_remaining > 0 else "Today!"
            upcoming_activities.append((activity, start_date, end_date, countdown_text))

    # Function to format activity details with color coding
    def format_activity(activity, start_date, end_date, countdown_text, color):
        start_display = start_date.strftime("%d-%m-%Y")
        end_display = end_date.strftime("%d-%m-%Y") if end_date else "N/A"
        return f"<span style='color:{color}'>{activity}: {start_display} to {end_display} - {countdown_text}</span>"

    # Display activities with refined layout
    st.subheader("Academic Calendar Activities")

    if upcoming_activities:
        st.markdown("### Upcoming Activities")
        for activity, start_date, end_date, countdown_text in upcoming_activities:
            color = "blue" if "days remaining" in countdown_text else "orange"
            st.markdown(format_activity(activity, start_date, end_date, countdown_text, color), unsafe_allow_html=True)

    if ongoing_activities:
        st.markdown("### Ongoing Activities")
        for activity, start_date, end_date, countdown_text in ongoing_activities:
            st.markdown(format_activity(activity, start_date, end_date, countdown_text, "green"), unsafe_allow_html=True)

    if past_activities:
        st.markdown("### Past Activities")
        for activity, start_date, end_date, countdown_text in past_activities:
            st.markdown(format_activity(activity, start_date, end_date, countdown_text, "red"), unsafe_allow_html=True)

# Popup notification for upcoming activity if notification has not been dismissed
def show_upcoming_activity_notification():
    today = datetime.now().date()
    upcoming_activities = [
        event for event in st.session_state["academic_calendar"]
        if 0 < (datetime.strptime(event["start_date"], "%Y-%m-%d").date() - today).days <= 10
    ]

    if upcoming_activities:
        st.sidebar.info("**Upcoming Activities**")
        for event in upcoming_activities:
            days_left = (datetime.strptime(event["start_date"], "%Y-%m-%d").date() - today).days
            st.sidebar.write(f"Activity: {event['activity']} - {days_left} days remaining")

        # Button to dismiss notification
        if st.sidebar.button("Dismiss Notifications"):
            st.session_state["notification_dismissed"] = True

# Admin login section
if not st.session_state["is_admin"]:
    st.sidebar.subheader("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login as Admin"):
        if username == "admin" and password == "admin123":
            st.session_state["is_admin"] = True
            st.sidebar.success("Logged in as Admin")
            st.session_state["notification_dismissed"] = False  # Reset notification dismissal on login
        else:
            st.sidebar.error("Incorrect username or password")
else:
    # Logout button for admin
    if st.sidebar.button("Logout"):
        st.session_state["is_admin"] = False  # Set to logged-out state
        st.session_state["notification_dismissed"] = False  # Reset notification dismissal on logout

# Calendar and Activity input for Admin to add new calendar events
if st.session_state["is_admin"]:
    st.subheader("Add Academic Calendar Activity")

    # Select a date
    selected_date = st.date_input("Select a Date to Add Activity")

    # Input fields for activity name and end date
    activity_name = st.text_input("Activity Name")
    end_date = st.date_input("End Date (optional)", value=selected_date)

    # Button to add the activity
    if st.button("Add Activity"):
        if activity_name and selected_date:
            new_activity = {
                "activity": activity_name,
                "start_date": selected_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d") if end_date else None
            }
            st.session_state["academic_calendar"].append(new_activity)
            save_calendar_to_file(st.session_state["academic_calendar"])
            st.success("Activity added successfully!")
        else:
            st.error("Please enter both an activity name and a start date.")

# Display the academic calendar on the main page after logout
if not st.session_state["is_admin"] and st.session_state["academic_calendar"]:
    display_academic_calendar()

# Show notification if user has not dismissed it
if not st.session_state["notification_dismissed"]:
    show_upcoming_activity_notification()

# Define document structure and tabs for other documents
tab = st.sidebar.selectbox("Choose an Examination Session", 
                           ["Mid Semester -1", "Mid Semester -2", "End Term Examination Theory", 
                            "End Term Practical Examination", "General Documents"])

documents = {
    "Mid Semester -1": ["Mid Semester-1 Date Sheet", "Gmail Language for Mid Term-1", "List of Faculty Members"],
    "Mid Semester -2": ["Mid Semester-2 Date Sheet", "Gmail Language for Mid Term-2", "List of Faculty Members"],
    "End Term Examination Theory": ["End Semester Date Sheet", "End Term General Notice", 
                                    "Gmail Language for End Term", "List of Faculty Members"],
    "End Term Practical Examination": ["End Semester Practical Date Sheet", "End Term Practical General Notice", 
                                       "Gmail Language for Practical", "List of Faculty Members"],
    "General Documents": ["Seating Plan", "Attendance Sheets", "Duty Chart", "Date Sheet", "UFM Form", 
                          "Individual Result Sheet Format", "Consolidated Result Sheet Format", 
                          "Display Result Format", "Bundle Slip", "Leave/Substitution Format", "Students Cut List", 
                          "Student Re-Appear Form", "Provisional Degree", "Migration", "Character Certificate", 
                          "Bonafide Certificate", "Transcript", "Mid Semester Question Paper Format", 
                          "End Semester Question Paper Format", "Service/Rate Chart"]
}

# MIME types for supported file extensions
mime_types = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

# Document management view
if tab in documents:
    st.header(f"{tab} Documents")

    # Display each document in a row
    for idx, doc_name in enumerate(documents[tab], start=1):
        file_exists = False
        file_path = ""
        mime_type = ""
        available_files = [f for f in os.listdir(upload_dir) if f.startswith(doc_name)]

        # Check if the file exists
        if available_files:
            file_name = available_files[0]  # Get the first match for the document
            file_extension = os.path.splitext(file_name)[1]
            mime_type = mime_types.get(file_extension, "application/octet-stream")
            file_path = os.path.join(upload_dir, file_name)
            file_exists = True

        # Display document details
        col1, col2, col3 = st.columns([1, 4, 2])
        col1.write(f"{idx}.")
        col2.write(doc_name)

        # Admin Mode: Show Upload and Delete options
        if st.session_state["is_admin"]:
            if file_exists:
                # Display delete button for existing files
                if col3.button("Delete", key=f"delete_{file_name}"):
                    os.remove(file_path)
            else:
                # Display upload option if file does not exist
                uploaded_file = col3.file_uploader(f"Upload {doc_name}", type=['pdf', 'docx', 'txt', 'xlsx'], key=f"upload_{doc_name}")
                if uploaded_file:
                    # Save the uploaded file with the document name
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                    standardized_name = f"{doc_name}{file_extension}"  # Standardize the file name with the correct extension
                    file_path = os.path.join(upload_dir, standardized_name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

        # User Mode: Show Download button only if the file exists
        elif file_exists:
            with open(file_path, "rb") as f:
                file_data = f.read()
            col3.download_button(label="Download", data=file_data, file_name=file_name, mime=mime_type)
