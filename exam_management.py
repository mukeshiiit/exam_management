import os
import streamlit as st

# Set up page configuration and title
st.set_page_config(page_title="IIIT Sonepat Examination Management System", layout="wide")
st.title("IIIT Sonepat Examination Management System")
st.write("Design and Developed by Dr. Mukesh Mann")

# Set the directory where files will be saved
upload_dir = "D:/Exam_management_iiit/uploads"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)  # Create the directory if it doesn't exist

# Initialize session state for admin login and flags
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False
if "action_triggered" not in st.session_state:
    st.session_state["action_triggered"] = False  # Track upload/delete actions

# Admin login section
if not st.session_state["is_admin"]:
    st.sidebar.subheader("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login as Admin"):
        if username == "admin" and password == "admin123":
            st.session_state["is_admin"] = True
            st.sidebar.success("Logged in as Admin")
        else:
            st.sidebar.error("Incorrect username or password")
else:
    # Logout button for admin
    if st.sidebar.button("Logout"):
        st.session_state["is_admin"] = False
        st.session_state["action_triggered"] = True  # Set action flag to refresh view

# Display mode notification in sidebar
if st.session_state["is_admin"]:
    st.sidebar.success("Admin Mode: Upload and Delete Enabled")
else:
    st.sidebar.info("User Mode: Download Only")

# Define document structure and tabs
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

# Display documents in a table format with options based on user role
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
                    st.session_state["action_triggered"] = True  # Set action flag to refresh view
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
                    st.session_state["action_triggered"] = True  # Set action flag to refresh view

        # User Mode: Show Download button only if the file exists
        elif file_exists:
            with open(file_path, "rb") as f:
                file_data = f.read()
            col3.download_button(label="Download", data=file_data, file_name=file_name, mime=mime_type)

# Reset the action_triggered flag after rendering
if st.session_state["action_triggered"]:
    st.session_state["action_triggered"] = False  # Reset after displaying changes
