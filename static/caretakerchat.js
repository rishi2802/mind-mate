document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");


    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value;
        if (message.trim() !== "") {
            displayUserMessage(message);
            userInput.value = "";
        }
    }

    function displayBotMessage(message) {
        const messageContainer = document.createElement("div");
        messageContainer.classList.add("message-container");

        const botLabel = `<h4 class="user-label">MindMate</h4>`;
        const botMessage = `<div class="bot-message">${message}</div>`;
        
        messageContainer.innerHTML = botLabel + botMessage;
        chatBox.appendChild(messageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function displayUserMessage(message) {
        const messageContainer = document.createElement("div");
        messageContainer.classList.add("message-container");

        
        const userLabel = `<h4 class="user-label">User</h4>`;
        const userMessage = `<div class="user-message">${message}</div>`;

        messageContainer.innerHTML = userLabel + userMessage;
        chatBox.appendChild(messageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
        displayBotMessage(getBotReply());
    }


    function getBotReply() {
        const randomResponses = [
            "I'm here to help.",
            "Tell me more about how you're feeling.",
            "You're not alone in this.",
            "What can I do to support you?",
            "It's okay to not be okay sometimes."
        ];
        const randomIndex = Math.floor(Math.random() * randomResponses.length);
        return randomResponses[randomIndex];
    }

    function sendMessageToBackend(message) {
        // For demonstration purposes, generate a random response
        $.ajax({
            type : "POST",
            url : '/userip',
            dataType: "json",
            data: JSON.stringify(message),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                displayBotMessage(data);
                }
            });
        

    }
});
