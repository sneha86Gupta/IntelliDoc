/**
 * Upload JS
 * Handles file upload UI and interactions
 */

document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileInput");
    const statusText = document.getElementById("status");

    uploadBtn.addEventListener("click", async () => {
        const file = fileInput.files[0];

        if (!file) {
            statusText.innerText = "Please select a file.";
            return;
        }

        statusText.innerText = "Uploading and processing...";

        try {
            const result = await uploadFile(file);

            // Save doc_id to localStorage
            localStorage.setItem("doc_id", result.doc_id);
            localStorage.setItem("doc_name", file.name);
            statusText.innerText = "Upload successful! Redirecting...";

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1500);

        } catch (error) {
            console.error(error);
            statusText.innerText = "Upload failed. Try again.";
        }
    });
});

/**
 * Navigation
 */
function goToDashboard() {
    window.location.href = "dashboard.html";
}