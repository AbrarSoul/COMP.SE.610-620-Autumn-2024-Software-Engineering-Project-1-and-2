# LLM-powered Teaching Assistant for Requirements Engineering (RE) Students

The AI-Driven Teaching Assistant (TA) is designed to enhance learning in Requirements Engineering (RE) by offering interactive content, adaptive quizzing, in-depth explanations, personalized support, and engagement tools. This assistant tailors content to each student’s needs, ensuring an engaging, efficient, and comprehensive learning experience.

## Our recommended key requirements so far

### 1. Interactive Content Generation
- **Lecture Summaries**: Automatically summarize lecture content or textbook chapters into concise notes, emphasizing core concepts.
- **Contextual Examples**: Generate context-rich examples specific to RE topics (e.g., requirements elicitation, analysis, validation) to aid understanding.
- **Real-World Scenarios**: Create real-world case studies based on RE concepts to demonstrate practical applications.
- **Comparison Insights**: Offer comparisons between similar concepts (e.g., MoSCoW analysis vs. Kano model) to clarify differences.

### 2. Adaptive Quizzing and Practice
- **Personalized Question Generation**: Generate questions based on each student’s learning history, focusing on areas needing improvement.
- **Dynamic Difficulty Adjustment**: Adjust the difficulty of quizzes based on students' quiz performance, providing additional challenges or support where needed.
- **Concept Reinforcement Mode**: Offer targeted practice on weak areas if students struggle with specific quiz topics, reinforcing learning.

### 3. In-Depth Explanations and Guidance
- **Detailed Step-by-Step Solutions**: Provide detailed explanations for each quiz question, showing correct and incorrect answers with reasoning.
- **Interactive Q&A Support**: Allow students to ask questions on specific RE concepts and get instant, contextual responses.
- **Guided Exercises**: Walk students through complex RE processes (e.g., developing use cases, creating requirements documents) step-by-step, allowing them to work independently with LLM guidance.

### 4. Feedback and Insight Tools
- **Real-Time Feedback Collection**: After each quiz or session, ask students to rate the content's helpfulness and suggest improvements, feeding this into a continuous refinement loop.
- **Student Progress Tracking**: Monitor students’ progress, highlighting improvement areas and suggesting personalized study plans.
- **Misconception Analysis**: Identify and flag common misconceptions or misunderstandings for targeted correction.

### 5. Customization and Personalization
- **Preferred Learning Style Customization**: Adjust responses based on each student's preferred learning style, whether they prefer definitions, analogies, or visual aids.
- **Personalized Study Reminders and Tips**: Send reminders for study sessions or tips based on students' progress, helping them stay engaged and focused.
- **Adaptive Goal Setting**: Enable students to set personal goals (e.g., mastering a specific RE technique) and receive targeted content to reach them.

### 6. Enhanced Engagement Features
- **Gamified Learning**: Introduce point systems or badges for completing quizzes, improving retention, or mastering new topics.
- **Scenario-Based Learning Paths**: Offer scenario-based learning paths where students can “role-play” as RE professionals and make decisions based on simulated project requirements.
- **Peer Interaction Modules**: Enable virtual peer review sessions, allowing students to review and critique each other’s answers or case studies.

### 7. Deployment and Monitoring Tools
- **Integration with Learning Management Systems (LMS)**: Integrate with platforms like Moodle or Blackboard for seamless access to quizzes and content.
- **Analytics Dashboard for Educators**: Provide teachers with analytics on student engagement, performance, and areas where students need additional support.
- **Scalability and Reliability**: Ensure the system can handle varying loads with robust error handling, ensuring a reliable experience for all students.

## How to Run the Project

1. **Clone the Repository**:
    ```bash
    git clone -b user_authentication_authorization_ozayer https://github.com/AbrarSoul/COMP.SE.610-620-Autumn-2024-Software-Engineering-Project-1-and-2.git
    cd <project-directory>
    ```
2. **Ensure Permissions**: If the run.sh script does not have execution permissions, grant them:
    ```bash
    chmod +x run.sh
    ```
3. **Run the Setup and Application**: Execute the script to set up and run the project:
    ```bash
    ./run.sh
    ```

## What the Script Does

1. **Checks for a Virtual Environment**: Creates a new venv directory if it doesn't exist.
2. **Activates the Virtual Environment**: Ensures all commands run in an isolated Python environment.
3. **Installs Dependencies**: Installs all required Python libraries listed in requirements.txt.
4. **Initializes the Database**: Sets up the SQLite database and ensures required tables are created.
5. **Runs the Application**: Launches the Streamlit app.

## Debugging Tips
If you encounter:
    ```bash
    ./run.sh: bad interpreter: /bin/bash^M: no such file or directory
    ```
Reason: Line endings are in Windows format (CRLF) instead of Unix (LF).
Fix:
Open the script in VS Code.
Click the CRLF button at the bottom right corner.
Select LF and save the file.