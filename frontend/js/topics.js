/**
 * Topics JS
 * Handles topic fetching and rendering
 */

document.addEventListener("DOMContentLoaded", () => {
    loadTopics();
});

/**
 * Load topics
 */
async function loadTopics() {
    const container = document.getElementById("topicsList");
    container.innerHTML = "";

    const docId = localStorage.getItem("doc_id");

    if (!docId) {
        container.innerHTML = "<p class='text-slate-400'>No document selected.</p>";
        return;
    }

    try {
        const data = await getTopics(docId);
        renderTopics(data.topics);
    } catch (error) {
        console.error(error);
        container.innerHTML = "<p class='text-red-400'>Error loading topics.</p>";
    }
}

/**
 * Render topics (FINAL FIXED)
 */
function renderTopics(topics) {
    const container = document.getElementById("topicsList");
    container.innerHTML = "";

    if (!topics || topics.length === 0) {
        container.innerHTML = "<p class='text-slate-400'>No topics found.</p>";
        return;
    }

    topics.forEach(topic => {

        // ✅ CLEAN TOPIC (UI only)
        const cleanTopic = topic
            .replace(/^.*?:\s*/, "")          // removes "Cluster 1: "
            .replace(/^\d+[\).\-\s]+/, "")    // removes "1. ", "2) "
            .trim();

        // MAIN ROW
        const item = document.createElement("div");
        item.className = "glass p-4 rounded-xl flex justify-between items-center card-hover transition cursor-pointer";

        // LEFT (clean topic name)
        const name = document.createElement("div");
        name.className = "font-medium text-sm";
        name.innerText = "📌 " + cleanTopic;

        // RIGHT (action text)
        const btn = document.createElement("div");
        btn.className = "text-indigo-400 text-sm";
        btn.innerText = "Select →";

        item.appendChild(name);
        item.appendChild(btn);

        // ✅ CLICK ACTION (CRITICAL FIX)
        item.addEventListener("click", () => {
            // 🔥 Store ORIGINAL topic for backend
            localStorage.setItem("selected_topic", topic);

            // 🔥 Store CLEAN topic for UI display
            localStorage.setItem("selected_topic_display", cleanTopic);

            window.location.href = "questions.html";
        });

        container.appendChild(item);
    });
}

/**
 * Navigation
 */
function goToDashboard() {
    window.location.href = "dashboard.html";
}