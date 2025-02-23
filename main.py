from openai import OpenAI
import streamlit as st
import itertools
import os
from utils import check_password
import random

st.set_page_config(
    page_title="Weaver - Edu AI",
    page_icon="🖍️",
    layout="wide",
)

st.title("🧠 + 🖍️ Weaver")
st.markdown("""
Fined tuned on publicly available online lesson plan data
*Created by Bradford Gill*
""")

if not check_password():  
    st.stop()
    
st.warning(
    """
    **Disclaimer:** This application is an AI prototype and is for demonstration purposes only.
    Results are likely to be inaccurate or incomplete. Use at your own discretion.
    """
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def lesson_gen():
    st.header("Lesson Generator")
    standards = []
    
    students = st.session_state.get("students", [])

    selected_student = st.selectbox(
        "Select Student", 
        options=students, 
        format_func=lambda s: s['name'],
        help="Select the student for whom you want to create a problem set."
    )
    
    # Text inputs and number input for the additional fields
    learning_standards = st.text_area(
        "Learning Standards (one per line)", 
        value='Solve word problems involving multiplication and division within 100.',
        help="Enter the learning standards for the lesson plan. Put each standard on a new line.",
        height=100
    )

    problem_type = st.text_input(
        "Activity type", 
        help="Specify the type of problem (e.g., multiple-choice, essay, etc.)."
    )
    number_of_problems = st.number_input(
        "Number of problems", 
        min_value=3, 
        max_value=15,
        value=8, 
        step=1, 
        help="Enter the number of problems to generate."
    )


    submitted = st.button("Submit")
        
    if submitted:
        standards_str = '\n'.join(standards)
        messages = [
            {
                'role': 'system',
                'content': '''
                You are an assistant used by teachers to create problem sets. Please create a problem set of work problems based on the bellow critera. 
                
                Incorperate the students interests into the problems to make it more engaging.

                At the top of each plan please have a line to put name and date, as a childs homework might look like.

                At the bottom, please have directions for solving including step by step instructions that are appropraite by grade level. 
                ''',
            },
            {
                'role': 'user',
                'content': f'''

                Student: {selected_student}

                Learning Standards: {learning_standards}
                Problem Type: {problem_type}
                Number of Problems: {number_of_problems}

                {standards_str}
                ''',
            },
            
        ]
        
        stream = client.chat.completions.create(
                model='gpt-4-turbo',
                messages=messages,
                stream=True,
            )
        
        response = st.write_stream(stream)

        st.download_button(
            label="Download lesson plan as a .txt",
            data=response,              # The string content you want to download
            file_name="response.txt",   # The name of the file being downloaded
            mime="text/plain"           # The MIME type of the file
        )

def student_profile():
    st.header("Student Profile Management")

    # Initialize session state for student profiles if not exists
    if "students" not in st.session_state:
        st.session_state["students"] = [
            {
                "name": "Bradford",
                "learning_attributes": "Has trouble focusing when not intreguied, interested in skiing, trail running, mountian biking. Bad at spelling.",
                "favorite_topics": "math",
                "grade_level": "3",
            },
            {
                "name": "Tobias",
                "learning_attributes": "Deep thinker, likes skiing and being in the out doors",
                "favorite_topics": "Science",
                "grade_level": "2",
            },
            {
                "name": "Jupiter",
                "learning_attributes": "Big dreamer, Thinks outside the box. Likes snowboarding.",
                "favorite_topics": "Science",
                "grade_level": "1",
            },
        ]
    
    operation = st.radio("Select Operation", ["View Student", "Add New Student", "Edit Student"])

    if operation == "Add New Student":
        with st.form("add_student_form"):
            student_name = st.text_input("Student Name")
            learning_attributes_str = st.text_input("List of Learner Attributes (comma separated)")
            favorite_topics_str = st.text_input("Interests (comma separated)")
            grade_level = st.selectbox("Grade Level", ["K", "1", "2", "3", "4", "5", "6", "7", "8"])
            submitted = st.form_submit_button("Add Student")
            if submitted:
                learning_attributes = [attr.strip() for attr in learning_attributes_str.split(",") if attr.strip()]
                favorite_topics = [topic.strip() for topic in favorite_topics_str.split(",") if topic.strip()]
                new_student = {
                    "name": student_name,
                    "learning_attributes": learning_attributes,
                    "favorite_topics": favorite_topics,
                    "grade_level": grade_level,
                }
                st.session_state.students.append(new_student)
                st.success(f"Student '{student_name}' added successfully.")

    elif operation == "Edit Student":
        if st.session_state.students:
            student_names = [student["name"] for student in st.session_state.students]
            selected_student = st.selectbox("Select Student to Edit", student_names)
            student_index = student_names.index(selected_student)
            student = st.session_state.students[student_index]
            
            with st.form("edit_student_form"):
                new_name = st.text_input("Student Name", value=student["name"])
                new_learning_attributes_str = st.text_input("List of Learner Attributes (comma separated)", student["learning_attributes"])
                new_favorite_topics_str = st.text_input("Interests (comma separated)", student["favorite_topics"])
                new_grade_level = st.selectbox("Grade Level", ["K", "1", "2", "3", "4", "5", "6", "7", "8"], index=["K", "1", "2", "3", "4", "5", "6", "7", "8"].index(student["grade_level"]))
                submitted_edit = st.form_submit_button("Save Changes")

                if submitted_edit:
                    st.session_state.students[student_index] = {
                        "name": new_name,
                        "learning_attributes": new_learning_attributes_str,
                        "favorite_topics": new_favorite_topics_str,
                        "grade_level": new_grade_level,
                    }
                    st.success(f"Student '{new_name}' updated successfully.")
        else:
            st.info("No students available to edit. Please add a student first.")
    
    elif operation == "View Student":
        if st.session_state.students:
            student_names = [student["name"] for student in st.session_state.students]
            selected_student = st.selectbox("Select Student to View", student_names)
            student_index = student_names.index(selected_student)
            student = st.session_state.students[student_index]

            st.subheader(f"Student: {student['name']}")
            st.markdown("**Learner Attributes:**")
            st.write(student['learning_attributes'])
            st.markdown("**Interests:**")
            st.write(student['favorite_topics'])
            st.markdown("**Grade Level:**")
            st.write(student['grade_level'])
        else:
            st.info("No students found. Please add a student first.")
    

def main():
    left, right = st.columns(2)

    with left:
        student_profile()

    with right:
        lesson_gen()





if __name__ == "__main__":
    main()


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


    
    

