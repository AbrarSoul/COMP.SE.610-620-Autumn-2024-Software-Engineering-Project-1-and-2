document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('pdfInput');
    const formData = new FormData();
    formData.append("pdf", fileInput.files[0]);

    const response = await fetch("/summarize", {
        method: "POST",
        body: formData
    });

    const summary = await response.text();
    document.getElementById('summary').innerText = summary;
});
