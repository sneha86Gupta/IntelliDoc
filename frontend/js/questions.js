/**
 * Questions JS
 */

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("generateBtn").addEventListener("click", handleGenerate);
});

async function handleGenerate() {
    const container = document.getElementById("questionsContainer");

    const docId = localStorage.getItem("doc_id");
    const topic = localStorage.getItem("selected_topic"); // ✅ ORIGINAL
    const topicDisplay = localStorage.getItem("selected_topic_display") || topic;

    const numQuestions = parseInt(document.getElementById("numQuestions").value);

    // ✅ dropdown single select
    const selectedType = document.getElementById("questionTypes").value;
    const questionTypes = [selectedType];

    if (!docId || !topic) {
        container.innerHTML = "<p class='text-red-400'>Missing document or topic.</p>";
        return;
    }

    container.innerHTML = `
        <p class='text-slate-400'>
            ⚡ Generating questions for 
            <span class="text-indigo-400">${topicDisplay}</span>...
        </p>
    `;

    try {
        const data = await generateQuestions({
            doc_id: docId,
            topic: topic, // ✅ ORIGINAL goes to backend
            num_questions: numQuestions,
            question_types: questionTypes
        });

        renderQuestions(data.questions);

    } catch (error) {
        console.error(error);
        container.innerHTML = "<p class='text-red-400'>Error generating questions.</p>";
    }
}

/**
 * Render Questions
 */
function renderQuestions(questions) {
    const container = document.getElementById("questionsContainer");
    container.innerHTML = "";

    if (!questions || questions.length === 0) {
        container.innerHTML = "<p class='text-slate-400'>No questions generated.</p>";
        return;
    }

    questions.forEach((q, index) => {

        const card = document.createElement("div");
        card.className = "glass p-6 rounded-2xl transition card-hover";

        const title = document.createElement("div");
        title.className = "font-semibold mb-4";
        title.innerText = `Q${index + 1} (${q.type?.toUpperCase()}): ${q.question}`;
        card.appendChild(title);

        // MCQ Options
        if (q.type === "mcq" && q.options?.length) {
            const optionsDiv = document.createElement("div");
            optionsDiv.className = "space-y-2 text-sm text-slate-300";

            q.options.forEach(opt => {
                const optItem = document.createElement("div");
                optItem.className = "px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 hover:border-indigo-500 transition cursor-pointer";
                optItem.innerText = opt;

                // UX: answer highlight
                optItem.addEventListener("click", () => {
                    optionsDiv.querySelectorAll("div").forEach(el => {
                        el.classList.remove("border-green-500", "border-red-500");
                    });

                    if (opt === q.answer) {
                        optItem.classList.add("border-green-500");
                    } else {
                        optItem.classList.add("border-red-500");
                    }
                });

                optionsDiv.appendChild(optItem);
            });

            card.appendChild(optionsDiv);
        }

        // Toggle Button
        const toggleBtn = document.createElement("button");
        toggleBtn.className = "mt-4 text-indigo-400 text-sm hover:underline";
        toggleBtn.innerText = "View Answer & Explanation ↓";

        // Accordion
        const answerDiv = document.createElement("div");
        answerDiv.className = "overflow-hidden transition-all duration-300 text-sm text-slate-300 border-t border-slate-700 mt-2";
        answerDiv.style.maxHeight = "0px";

        const inner = document.createElement("div");
        inner.className = "pt-3";

        inner.innerHTML = `
            <p><strong>Answer:</strong> ${q.answer || "N/A"}</p>
            <p class="mt-2"><strong>Explanation:</strong> ${q.explanation || "N/A"}</p>
        `;

        answerDiv.appendChild(inner);

        toggleBtn.addEventListener("click", () => {
            const isOpen = answerDiv.style.maxHeight !== "0px";

            if (isOpen) {
                answerDiv.style.maxHeight = "0px";
                toggleBtn.innerText = "View Answer & Explanation ↓";
            } else {
                answerDiv.style.maxHeight = answerDiv.scrollHeight + "px";
                toggleBtn.innerText = "Hide Answer ↑";
            }
        });

        card.appendChild(toggleBtn);
        card.appendChild(answerDiv);

        container.appendChild(card);
    });
}

/**
 * Navigation
 */
function goToTopics() {
    window.location.href = "topics.html";
}