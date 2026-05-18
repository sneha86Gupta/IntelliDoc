/**
 * API Utility
 * Handles all backend API calls
 */

const API_BASE_URL = "http://localhost:8000"; // Update if deployed

/**
 * Upload file
 */
async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("Upload failed");
    }

    return response.json();
}

/**
 * Get topics for a document
 */
async function getTopics(docId) {
    const response = await fetch(`${API_BASE_URL}/topics/${docId}`);

    if (!response.ok) {
        throw new Error("Failed to fetch topics");
    }

    return response.json();
}

/**
 * Generate questions
 */
async function generateQuestions(data) {
    const response = await fetch(`${API_BASE_URL}/questions/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error("Failed to generate questions");
    }

    return response.json();
}

/**
 * Export PDF
 */
async function exportPDF(data) {
    const response = await fetch(`${API_BASE_URL}/export/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error("Failed to export PDF");
    }

    return response.blob();
}