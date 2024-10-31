const chatBox = document.getElementById("chat-box");
const sampleQuestions = document.getElementById("sample-questions");

function displayMessage(message, className) {
  const messageElement = document.createElement("div");
  messageElement.className = `message ${className}`;
  messageElement.innerHTML = message;
  chatBox.insertBefore(messageElement, chatBox.firstChild); // Display from top
  return messageElement; // Return the element to update it later
}

async function handleUserQuery() {
  const userInput = document.getElementById("user-input");
  const query = userInput.value.trim();
  if (!query) return;

  // Hide sample questions on the first message
  if (sampleQuestions) sampleQuestions.style.display = 'none';

  displayMessage(query, "user-message");
  userInput.value = ""; // Clear input box

  // Display "loading..." message
  const loadingMessage = displayMessage("Loading...", "bot-message");

  try {
    const response = await fetch("/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const data = await response.json();

    // Update the loading message with actual response
    loadingMessage.innerHTML = data.response;

  } catch (error) {
    loadingMessage.innerHTML = "Error fetching data. Please try again.";
  }
}

// Function to submit a sample question
function submitSampleQuery(query) {
  const userInput = document.getElementById("user-input");
  userInput.value = query;
  handleUserQuery();
}


// pdf upload
async function uploadPdf() {
  const fileInput = document.getElementById('pdfFile');
  const uploadMessage = document.getElementById('uploadMessage');

  // Clear any previous messages
  uploadMessage.textContent = '';

  // Validate that a file is selected and that it’s a PDF
  if (!fileInput.files.length) {
    uploadMessage.textContent = 'Please select a file to upload.';
    uploadMessage.style.color = 'red';
    return;
  }

  const file = fileInput.files[0];
  if (file.type !== 'application/pdf') {
    uploadMessage.textContent = 'Only PDF files are allowed.';
    uploadMessage.style.color = 'red';
    return;
  }

  // Prepare the form data
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/upload_pdf', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    if (response.ok) {
      uploadMessage.textContent = result.message;
      uploadMessage.style.color = 'green';
    } else {
      uploadMessage.textContent = result.message || 'Error uploading file.';
      uploadMessage.style.color = 'red';
    }
  } catch (error) {
    uploadMessage.textContent = error;
    uploadMessage.style.color = 'red';
  }
}

