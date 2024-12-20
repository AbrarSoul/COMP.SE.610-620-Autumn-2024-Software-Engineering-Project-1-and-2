# LLM-Powered Online Teaching Assistant for Requirements Engineering (RE) Course (APUOPE-RE)

## Live Project Link
[https://comp-se-610-620-autumn-2024-software.onrender.com/](https://comp-se-610-620-autumn-2024-software.onrender.com/)

## User Acceptance Testing (UAT) Process

### Step-1: Register as a Teacher and Login as a Teacher

1. **Register and Login**
   - Register with any email and set a password.
   - Choose 'teacher' from the role panel.
   - Login after completing the registration.

2. **Dashboard**
   - Navigate to the Dashboard to see an overview of the course with progress.
   - Note: This page is structured with dummy data and is not integrated with live data as it was not required by the customer. Further development is planned.

3. **Materials**
   - If any material is listed, delete them for a fresh start.
   - Add your own materials. Materials can be any PDF file on your PC.

4. **Studying Lectures**
   - View uploaded materials in the list panel.
   - Choose any material from the list and use the following buttons:
     - "Generate Conceptual Example"
     - "Generate Summary"
     - "Find Contents"
   - These buttons will generate conceptual examples, summaries, and contents based on the selected material.
   - After generating the response, check the relevance of the content using the "Check Relevance" button (this button appears after generating a response).
   - Write prompts in the text field below for further analysis on the material.

5. **Quiz**
   - No information will be displayed initially as no student has taken any quiz yet.

6. **Assignment**
   - No information will be displayed initially as no student has submitted any assignment yet.

7. **Feedback**
   - No information will be displayed initially as no student has submitted any feedback yet.

### Step-2: Register as a Student and Login as a Student

1. **Register and Login**
   - Register with another email and set a password.
   - Choose 'student' from the role panel.
   - Provide any ID as the student ID.
   - Login after completing the registration.

2. **Dashboard**
   - Navigate to the Dashboard to see an overview of the course with progress.
   - Note: This page is structured with dummy data and is not integrated with live data as it was not required by the customer. Further development is planned.

3. **Materials**
   - View materials uploaded by the teacher.
   - As a student, you can only view materials uploaded by the teacher. You cannot upload or delete any material.

4. **Studying Lectures**
   - View uploaded materials in the list panel.
   - Choose any material from the list and use the following buttons:
     - "Generate Conceptual Example"
     - "Generate Summary"
     - "Find Contents"
   - These buttons will generate conceptual examples, summaries, and contents based on the selected material.
   - After generating the response, check the relevance of the content using the "Check Relevance" button (this button appears after generating a response).
   - Write prompts in the text field below for further analysis on the material.

5. **Quiz**
   - Choose any material from the dropdown list.
   - Select a difficulty level and press "Generate Quiz" to take the quiz.
   - After answering the quiz questions, your score will be displayed.

6. **Assignment**
   - Choose any material from the dropdown list.
   - Press "Generate Conceptual Assignment" to generate an assignment with instructions.
   - The generated assignment will also be available as a PDF.
   - Download the PDF by pressing "Download Generated Assignment (PDF)".
   - Upload your completed assignment below with your name.

7. **Feedback**
   - Submit your feedback anonymously as a student.

### Step-3: Login Again as a Teacher

1. **Quiz**
   - View the quiz responses submitted when logged in as a student.

2. **Assignment**
   - View the assignments submitted when logged in as a student.

3. **Feedback**
   - View the feedback submitted when logged in as a student.
