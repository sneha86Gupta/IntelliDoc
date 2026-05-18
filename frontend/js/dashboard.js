/**
 * Dashboard JS
 * Handles document listing and navigation
 */

document.addEventListener("DOMContentLoaded", () => {
    loadDocuments();
});

/**
 * Load documents from localStorage
 * (Simple MVP: single doc support, extendable later)
 */
function loadDocuments() {
    const container = document.getElementById("documentsList");
    container.innerHTML = "";

    const docId = localStorage.getItem("doc_id");

    if (!docId) {
        container.innerHTML = "<p>No documents uploaded yet.</p>";
        return;
    }

    const docName = localStorage.getItem("doc_name") || "Untitled Document";

    const docItem = document.createElement("div");
    docItem.className = "glass p-4 rounded-xl flex justify-between items-center card-hover transition cursor-pointer";

    // LEFT (ONLY NAME NOW)
    const name = document.createElement("div");
    name.className = "font-medium text-sm";
    name.innerText = "📄 " + docName;

    // RIGHT
    const btn = document.createElement("div");
    btn.className = "text-indigo-400 text-sm";
    btn.innerText = "Open →";

    docItem.appendChild(name);
    docItem.appendChild(btn);

    // CLICK (still uses docId internally)
    docItem.addEventListener("click", () => {
        goToTopics(docId);
    });

    container.appendChild(docItem);
}

/**
 * Navigation
 */
function goToTopics(docId) {
    localStorage.setItem("doc_id", docId);
    window.location.href = "topics.html";
}

function goToUpload() {
    window.location.href = "index.html";
}