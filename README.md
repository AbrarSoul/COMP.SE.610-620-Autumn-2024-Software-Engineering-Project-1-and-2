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

# Relevance Scoring Guide

This project evaluates the relevance of LLM-generated content to the course material using three metrics: **Semantic Similarity**, **Keyword Overlap**, and **LLM Feedback Score**. Below is the interpretation of each score:

## 1. Semantic Similarity

Semantic similarity measures the closeness between the embeddings of the course material and the generated content. Scores range from 0 to 1, where higher scores indicate greater relevance.

| Score Range | Interpretation   | Quality   |
|-------------|------------------|-----------|
| 0.85 - 1.00 | Highly relevant  | Excellent |
| 0.70 - 0.84 | Relevant         | Good      |
| 0.50 - 0.69 | Somewhat relevant| Average   |
| 0.30 - 0.49 | Weak relevance   | Poor      |
| 0.00 - 0.29 | Not relevant     | Very Bad  |

### What it does

Measures the overall similarity between the course material and the generated content based on their meanings, not just word matching.

### How it works

- Both the course material and generated content are converted into vector embeddings using a pre-trained model like OpenAI’s text-embedding-ada-002.
- The similarity is calculated using cosine similarity, which measures the angle between the two vectors.
- A score closer to 1 indicates high relevance, while a score closer to 0 indicates low relevance.

### Why it’s important

Captures the conceptual closeness between the source material and the output, ensuring the generated content aligns semantically.

## 2. Keyword Overlap

Keyword overlap calculates the percentage of keywords in the course material that also appear in the generated content. A higher percentage indicates better alignment.

| Overlap Range | Interpretation   | Quality   |
|---------------|------------------|-----------|
| 75% - 100%    | Highly relevant  | Excellent |
| 50% - 74%     | Relevant         | Good      |
| 30% - 49%     | Somewhat relevant| Average   |
| 10% - 29%     | Weak relevance   | Poor      |
| 0% - 9%       | Not relevant     | Very Bad  |

### What it does

Compares the keywords in the course material with those in the generated content to find overlapping terms.

### How it works

- Extracts keywords from both the course material and the generated content using Natural Language Processing (NLP) techniques like spaCy.
- Calculates the percentage of overlapping keywords relative to the total number of keywords in the course material.
- A higher percentage indicates better relevance, as it shows the generated content uses terms related to the source material.

### Why it’s important

Ensures the generated content covers key topics and terms from the original material, which is critical for accurate representation.

## 3. LLM Feedback Score

The LLM feedback score is based on the LLM’s evaluation of the relevance of the generated content to the course material. Scores range from 0 to 10.

| Score Range | Interpretation   | Quality   |
|-------------|------------------|-----------|
| 9 - 10      | Highly relevant  | Excellent |
| 7 - 8       | Relevant         | Good      |
| 5 - 6       | Somewhat relevant| Average   |
| 3 - 4       | Weak relevance   | Poor      |
| 0 - 2       | Not relevant     | Very Bad  |

### What it does

Uses the same LLM to evaluate the relevance of its generated content against the course material.

### How it works

- A specially designed prompt is sent to the LLM, asking it to compare the course material with the generated content.
- The LLM provides a numerical score (0-10) and a short explanation of how relevant the generated content is.
- A higher score reflects better relevance based on the LLM’s internal understanding of the context.

### Why it’s important

Provides an additional layer of evaluation by leveraging the LLM’s reasoning ability to judge the quality of its own output.

###Live Demo
[Click here to view the live demo](https://comp-se-610-620-autumn-2024-software.onrender.com/)