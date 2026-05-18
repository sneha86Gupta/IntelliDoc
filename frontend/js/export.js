/**
 * Export JS
 * Handles exporting generated questions to PDF
 */

document.addEventListener("DOMContentLoaded", () => {
    const exportBtn = document.getElementById("exportBtn");

    if (exportBtn) {
        exportBtn.addEventListener("click", handleExport);
    }
});

/**
 * Export PDF
 */
async function handleExport() {
    const docId = localStorage.getItem("doc_id");
    const topic = localStorage.getItem("selected_topic");

    const numQuestions = parseInt(document.getElementById("numQuestions").value);
    const questionTypes = Array.from(
        document.getElementById("questionTypes").selectedOptions
    ).map(opt => opt.value);

    if (!docId || !topic) {
        alert("Missing document or topic.");
        return;
    }

    try {
        const blob = await exportPDF({
            doc_id: docId,
            topic: topic,
            num_questions: numQuestions,
            question_types: questionTypes
        });

        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "questions.pdf";

        document.body.appendChild(a);
        a.click();

        // Cleanup
        a.remove();
        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error(error);
        alert("Failed to export PDF.");
    }
}