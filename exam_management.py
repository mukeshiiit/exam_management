import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

st.set_page_config(page_title="IIIT Sonepat Examination Management System", layout="wide")
st.title("IIIT Sonepat Examination Management System")
st.write("Design and Developed by Dr. Mukesh Mann")

# Tab and document definitions
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

# Display document options and upload/download functionality
if tab in documents:
    st.header(f"{tab} Documents")
    for doc_name in documents[tab]:
        st.subheader(doc_name)
        uploaded_file = st.file_uploader(f"Upload {doc_name} Template", type=['pdf', 'docx', 'txt'], key=doc_name)
        st.download_button(label=f"Download {doc_name} Template", data="sample data", file_name=f"{doc_name}.pdf", mime="application/pdf")

# Email notification feature
def send_email(subject, body, recipient):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"

if st.button("Send Email Notification"):
    recipient_email = st.text_input("Enter Recipient Email")
    email_subject = f"Examination Notification for {tab}"
    email_body = st.text_area("Enter Email Content", "Dear Faculty, please review the attached documents.")
    if recipient_email and email_body:
        st.write(send_email(email_subject, email_body, recipient_email))
    else:
        st.write("Please enter recipient email and email content.")
