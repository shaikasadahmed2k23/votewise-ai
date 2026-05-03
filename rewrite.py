import os
import re

file_path = 'templates/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS ADDITIONS
css_additions = """
        /* New Classes to replace inline styles */
        .text-saffron { color: var(--saffron); }
        .text-white { color: var(--white); }
        .text-navy { color: var(--navy); }
        .text-light { color: var(--text-light); }
        .m-0 { margin: 0; }
        .mb-1-5 { margin-bottom: 1.5rem; }
        .mb-2 { margin-bottom: 2rem; }
        .mt-0-5 { margin-top: 0.5rem; }
        .p-0 { padding: 0; }
        .text-lg { font-size: 1.2rem; }
        .text-xl { font-size: 1.5rem; }
        .w-full { width: 100%; }
        .max-w-600 { max-width: 600px; margin: 0 auto; }
        .hidden { display: none !important; }
        .flex { display: flex; }
        .justify-between { justify-content: space-between; }
        
        /* Copy Button */
        .copy-btn {
            background: transparent;
            border: none;
            cursor: pointer;
            color: var(--text-light);
            font-size: 0.85rem;
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: color 0.2s;
            padding: 4px;
        }
        .copy-btn:hover { color: var(--navy); }

        /* Quiz Explanation */
        .explanation {
            background: #f0f4f8;
            border-left: 4px solid var(--navy);
            padding: 1rem;
            margin-top: 1rem;
            border-radius: 4px;
            font-size: 0.95rem;
            display: none;
            animation: fadeInSlide 0.3s ease;
        }

        /* Character Count */
        #char-count {
            font-size: 0.8rem;
            color: var(--text-light);
            text-align: right;
            margin-top: 0.3rem;
            margin-right: 1rem;
        }

        /* App Footer */
        .app-footer {
            text-align: center;
            padding: 2rem 1rem;
            color: var(--text-light);
            font-size: 0.9rem;
            margin-top: auto;
            border-top: 1px solid var(--border-color);
        }

        /* Message header for Copy */
        .message-content { flex: 1; }
        .message-footer { display: flex; justify-content: flex-end; }
"""
html = html.replace('</style>', css_additions + '\n    </style>')

# Fade Transition
html = html.replace('animation: fadeInSlide 0.4s ease forwards;', 'animation: crossFade 0.4s ease forwards;\n        }\n\n        @keyframes crossFade {\n            from { opacity: 0; transform: translateY(5px); }\n            to { opacity: 1; transform: translateY(0); }')

# 2. INLINE STYLES -> CLASSES & ARIA LABELS in HTML
html = html.replace('<span style="color: var(--saffron);">Vote</span><span style="color: var(--white);">Wise</span>', '<span class="text-saffron">Vote</span><span class="text-white">Wise</span>')
html = html.replace('<button class="tab-btn active" onclick="switchTab(\'chat\', event)">', '<button class="tab-btn active" aria-label="Ask VoteWise Tab" onclick="switchTab(\'chat\', event)">')
html = html.replace('<button class="tab-btn" onclick="switchTab(\'timeline\', event)">', '<button class="tab-btn" aria-label="Election Timeline Tab" onclick="switchTab(\'timeline\', event)">')
html = html.replace('<button class="tab-btn" onclick="switchTab(\'quiz\', event)">', '<button class="tab-btn" aria-label="Civic Quiz Tab" onclick="switchTab(\'quiz\', event)">')
html = html.replace('<button class="tab-btn" onclick="switchTab(\'eligibility\', event)">', '<button class="tab-btn" aria-label="Check Eligibility Tab" onclick="switchTab(\'eligibility\', event)">')

html = html.replace('<div class="card" style="padding: 0;">', '<div class="card p-0">')
html = html.replace('id="chat-messages"', 'id="chat-messages" role="log" aria-live="polite"')

html = html.replace('class="chip" onclick="', 'class="chip" role="button" aria-label="Quick Question" tabindex="0" onclick="')
html = html.replace('id="chat-input" placeholder="Type your question here..."\n                            onkeypress="handleEnter(event)">', 'id="chat-input" placeholder="Type your question here..."\n                            aria-label="Chat Input" maxlength="500" oninput="updateCharCount()" onkeypress="handleEnter(event)">')
html = html.replace('<button onclick="sendMessage()">', '<button id="send-btn" onclick="sendMessage()" aria-label="Send Message">')
html = html.replace('</div>\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <!-- 2. Timeline Tab -->', '    <div id="char-count">0/500</div>\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <!-- 2. Timeline Tab -->')

html = html.replace('<p style="margin-bottom: 2rem; color: var(--text-light);">A step-by-step guide', '<p class="mb-2 text-light">A step-by-step guide')
html = html.replace('<h2 style="margin: 0;">Civic Knowledge Quiz</h2>', '<h2 class="m-0">Civic Knowledge Quiz</h2>')
html = html.replace('<p style="font-size: 1.2rem; margin-bottom: 1.5rem;">Your Score: <strong id="score"\n                            style="color: var(--navy); font-size: 1.5rem;">0 / 8</strong></p>', '<p class="text-lg mb-1-5">Your Score: <strong id="score" class="text-navy text-xl">0 / 8</strong></p>')
html = html.replace('style="margin-bottom: 2rem; color: var(--text-light);"', 'class="mb-2 text-light"')

html = html.replace('<div class="card" style="max-width: 600px; margin: 0 auto;">', '<div class="card max-w-600">')
html = html.replace('<p style="margin-bottom: 1.5rem; color: var(--text-light);">Find out if you meet', '<p class="mb-1-5 text-light">Find out if you meet')
html = html.replace('style="width: 100%; margin-top: 0.5rem;"', 'class="w-full mt-0-5"')

html = html.replace('<label for="country">', '<span id="country-desc" class="hidden">Select your country of citizenship.</span>\n                    <label for="country">')
html = html.replace('<select id="country">', '<select id="country" aria-describedby="country-desc">')
html = html.replace('<label for="age">', '<span id="age-desc" class="hidden">Enter your age in years.</span>\n                    <label for="age">')
html = html.replace('<input type="number" id="age" min="1" max="120" placeholder="e.g. 21">', '<input type="number" id="age" min="1" max="120" placeholder="e.g. 21" aria-describedby="age-desc">')

# Add explanation div to quiz
html = html.replace('<div class="options" id="options">\n                        <!-- Options injected by JS -->\n                    </div>', '<div class="options" id="options">\n                        <!-- Options injected by JS -->\n                    </div>\n                    <div id="quiz-explanation" class="explanation"></div>')

# Footer
html = html.replace('</main>', '    </main>\n    <footer class="app-footer">\n        Built with ❤️ for Prompt Wars by GDG | Powered by Gemini AI\n    </footer>')

# 3. JS UPDATES
js_replacements = """
        // State variables
        let isSending = false;
        let lastMessage = "";

        /**
         * Updates the character count display for the chat input
         */
        function updateCharCount() {
            const charCountEl = document.getElementById('char-count');
            const len = chatInput.value.length;
            charCountEl.textContent = `${len}/500`;
        }

        /**
         * Switches the active tab and updates UI
         * @param {string} tabId - The ID of the tab to switch to
         * @param {Event} event - The click event object
         */
        function switchTab(tabId, event) {
            // ... (keep existing body except add check for quiz caching) ...
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            if (event) event.currentTarget.classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');

            if (tabId === 'quiz' && currentQuestion === 0 && score === 0 && document.getElementById('options').innerHTML.trim() === '') {
                startQuiz();
            }
        }

        /**
         * Copies text to clipboard
         * @param {string} text - The text to copy
         */
        function copyText(button, text) {
            navigator.clipboard.writeText(text).then(() => {
                const originalText = button.innerHTML;
                button.innerHTML = '📋 Copied!';
                setTimeout(() => button.innerHTML = originalText, 2000);
            });
        }

        /**
         * Handles the enter key press on the chat input
         */
        function handleEnter(e) {
            if (e.key === 'Enter' && !isSending) {
                sendMessage();
            }
        }

        /**
         * Populates input and sends a predefined quick message
         * @param {string} text - The predefined question
         */
        function sendQuickMessage(text) {
            if (isSending) return;
            chatInput.value = text;
            updateCharCount();
            sendMessage();
        }

        /**
         * Sends the user's message to the backend API and handles the response
         * Includes debouncing to prevent double submissions
         */
        async function sendMessage(retryText = null) {
            if (isSending) return;
            
            const message = retryText || chatInput.value.trim();
            if (!message) return;

            isSending = true;
            lastMessage = message;
            
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = true;
            sendBtn.textContent = '...';

            const existingErrors = document.querySelectorAll('.message.error');
            existingErrors.forEach(err => err.remove());

            if (!retryText) {
                addMessageToChat('user', message);
            }
            
            chatInput.value = '';
            updateCharCount();

            chatMessages.appendChild(typingIndicator);
            typingIndicator.classList.add('active');
            scrollToBottom();

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });

                if (!response.ok) throw new Error('Network response was not ok');

                const data = await response.json();
                typingIndicator.classList.remove('active');
                
                const botReply = data.response || data.reply || data.answer || "I received your message but couldn't parse the response.";
                addMessageToChat('ai', botReply);

            } catch (error) {
                typingIndicator.classList.remove('active');
                addMessageToChat('error', "⚠️ Hmm, I couldn't reach the AI right now. Please check your connection and try again.");
            } finally {
                isSending = false;
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
            }
        }

        /**
         * Appends a new message bubble to the chat container
         * @param {string} role - 'user', 'ai', or 'error'
         * @param {string} text - The message content
         */
        function addMessageToChat(role, text) {
            const div = document.createElement('div');
            div.className = `message ${role}`;
            
            if (role === 'ai') {
                div.innerHTML = `<div class="message-content">${text.replace(/\\n/g, '<br>')}</div>
                                 <div class="message-footer">
                                    <button class="copy-btn" onclick="copyText(this, \`${text.replace(/`/g, '\\`')}\`)" aria-label="Copy response">📄 Copy</button>
                                 </div>`;
            } else if (role === 'error') {
                div.innerHTML = `<div>${text}</div><button class="btn-primary" style="margin-top: 10px; padding: 0.5rem 1rem;" onclick="sendMessage(lastMessage)">Retry</button>`;
            } else {
                div.textContent = text;
            }

            if (role !== 'error') {
                chatMessages.insertBefore(div, typingIndicator);
            } else {
                chatMessages.appendChild(div);
            }
            scrollToBottom();
        }
"""

quiz_js_replacements = """
        const quizData = [
            { question: "What is the minimum voting age in India?", options: ["16 years", "18 years", "21 years", "25 years"], correct: 1, explanation: "Article 326 of the Constitution grants universal adult suffrage to citizens above 18 years." },
            { question: "Which body conducts elections to the Lok Sabha in India?", options: ["Supreme Court of India", "Election Commission of India", "Parliament of India", "President of India"], correct: 1, explanation: "The ECI is an autonomous constitutional authority responsible for administering election processes in India." },
            { question: "What does EVM stand for?", options: ["Electronic Voting Machine", "Electoral Verification Machine", "Election Validating Mechanism", "Electronic Voter Module"], correct: 0, explanation: "EVM stands for Electronic Voting Machine, which replaced paper ballots to speed up voting and reduce fraud." },
            { question: "What does NOTA stand for?", options: ["No Official Target Assigned", "None Of The Above", "Never Overturn The Authority", "Not On The Agenda"], correct: 1, explanation: "NOTA allows voters to officially reject all candidates contesting in their constituency." },
            { question: "How many members are there in the Lok Sabha (currently elected)?", options: ["250", "543", "545", "552"], correct: 1, explanation: "There are 543 elected constituencies in the Lok Sabha." },
            { question: "What is VVPAT?", options: ["Voter Verifiable Paper Audit Trail", "Voting Verification Protocol And Technique", "Valid Vote Paper Audit Trail", "Voter Validation Process And Trail"], correct: 0, explanation: "VVPAT provides a printed slip for 7 seconds to the voter to verify their vote." },
            { question: "Who appoints the Chief Election Commissioner of India?", options: ["Prime Minister", "Chief Justice of India", "President of India", "Parliament"], correct: 2, explanation: "The President of India appoints the Chief Election Commissioner." },
            { question: "When is National Voters' Day celebrated in India?", options: ["15th August", "26th January", "25th January", "2nd October"], correct: 2, explanation: "Celebrated on January 25th to mark the foundation day of the Election Commission of India in 1950." }
        ];

        let currentQuestion = 0;
        let score = 0;

        const questionText = document.getElementById('question-text');
        const optionsContainer = document.getElementById('options');
        const progressFill = document.getElementById('progress');
        const tracker = document.getElementById('question-tracker');
        const nextBtn = document.getElementById('next-btn');
        const quizGame = document.getElementById('quiz-game');
        const quizResultBox = document.getElementById('quiz-result');
        const explanationBox = document.getElementById('quiz-explanation');

        /**
         * Initializes and starts the civic quiz
         */
        function startQuiz() {
            currentQuestion = 0;
            score = 0;
            quizGame.style.display = 'block';
            quizResultBox.style.display = 'none';
            loadQuestion();
        }

        /**
         * Loads the current question and its options into the UI
         */
        function loadQuestion() {
            const q = quizData[currentQuestion];
            questionText.textContent = q.question;
            tracker.textContent = `Question ${currentQuestion + 1} of ${quizData.length}`;
            progressFill.style.width = `${((currentQuestion) / quizData.length) * 100}%`;
            nextBtn.style.display = 'none';
            explanationBox.style.display = 'none';

            optionsContainer.innerHTML = '';
            q.options.forEach((opt, index) => {
                const btn = document.createElement('button');
                btn.className = 'option';
                btn.textContent = opt;
                btn.setAttribute('aria-label', `Option: ${opt}`);
                btn.onclick = () => selectOption(index, btn);
                optionsContainer.appendChild(btn);
            });
        }

        /**
         * Handles option selection, highlights correct/wrong, and shows explanation
         * @param {number} selectedIndex - The index of the selected option
         * @param {HTMLElement} btnElement - The clicked button element
         */
        function selectOption(selectedIndex, btnElement) {
            const allOptions = optionsContainer.querySelectorAll('.option');
            allOptions.forEach(opt => opt.classList.add('disabled'));

            const correctIndex = quizData[currentQuestion].correct;

            if (selectedIndex === correctIndex) {
                btnElement.classList.add('correct');
                score++;
            } else {
                btnElement.classList.add('wrong');
                allOptions[correctIndex].classList.add('correct');
            }

            explanationBox.textContent = quizData[currentQuestion].explanation;
            explanationBox.style.display = 'block';

            nextBtn.style.display = 'block';
            progressFill.style.width = `${((currentQuestion + 1) / quizData.length) * 100}%`;
        }
"""

# Extract the script block
script_start = html.find('// --- Tab Switching Logic ---')
script_end = html.find('// --- Civic Quiz Logic ---')
quiz_end = html.find('// --- Eligibility Logic ---')
script_full_end = html.find('</script>', quiz_end)

new_html = html[:script_start] + js_replacements + quiz_js_replacements + html[quiz_end:script_full_end].replace('function checkEligibility()', '/**\\n         * Evaluates voter eligibility based on age and country\\n         */\\n        function checkEligibility()') + html[script_full_end:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("UI Polish complete!")
