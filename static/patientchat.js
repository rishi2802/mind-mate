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
            sendMessageToBackend(message); // Move this line inside if condition
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

    function sendMessage_data() {
        const message = userInput.value;
        if (message.trim() !== "") {
            displayUserMessage(message);
            userInput.value = "";
            sendMessageToBackend(message); // Move this line inside if condition
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
        sendMessageToBackend(message)
    }

    displayBotMessage("Hi, how are you doing today?");
    let questionnaireStarted = false;
    let questionnaireIndex = 1;
    let questionnaireScores = [];

    function processUserResponse(response) {
        if (response.toLowerCase().includes("sad")) {
            displayBotMessage(" Please answer the following questionnaire so that we can understand you better!!");
            displayBotMessage(`Please read each statement and circle a number 0, 1, 2, or 3 which indicates how much the statement applied to you over the past week. There are no right or wrong answers. Do not spend too much time on any statement. The rating scale is as follows: 0 --Did not apply to me at all 1 --Applied to me to some degree, or some of the time 2 --Applied to me to a considerable degree or a good part of the time 3 --Applied to me very much or most of the time`);
            questionnaireStarted = true;
            displayBotMessage(getQuestionnairePrompt(questionnaireIndex));
        }
        if (response.toLowerCase().includes("happy")) {
            displayBotMessage("Wow great ! keep up the good work");
        } else {
            // Handle other responses accordingly
        }
    }

    function sendMessage() {
        const message = userInput.value;
        if (message.trim() !== "") {
            if (!questionnaireStarted) {
                displayUserMessage(message);
                processUserResponse(message);
            } else {
                const score = parseInt(message.trim());
                if (!isNaN(score) && score >= 0 && score <= 3) {
                    questionnaireScores.push(score);
                    questionnaireIndex++;
                    if (questionnaireIndex <= 21) {
                        displayUserMessage(message);
                        displayBotMessage(getQuestionnairePrompt(questionnaireIndex));
                    } else {
                        displayUserMessage(message);
                        const totalScore = calculateTotalScore(questionnaireScores);
                        processQuestionnaireResponse(totalScore);
                    }
                } else {
                    displayBotMessage("Please enter a valid score between 0 and 3.");
                }
            }
            userInput.value = "";
        }
    }

    function getQuestionnairePrompt(index) {
        const questions = [
            " I found it hard to wind down ",
            " I was aware of dryness of my mouth ",
            " I couldn’t seem to experience any positive feeling at all ",
            " I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion) ",
            " I found it difficult to work up the initiative to do things ",
            " I tended to over-react to situations ",
            " I experienced trembling (e.g. in the hands) ",
            " I felt that I was using a lot of nervous energy ",
            " I was worried about situations in which I might panic and make a fool of myself ",
            " I felt that I had nothing to look forward to ",
            " I found myself getting agitated ",
            " I found it difficult to relax ",
            " I felt down-hearted and blue ",
            " I was intolerant of anything that kept me from getting on with what I was doing ",
            " I felt I was close to panic ",
            " I was unable to become enthusiastic about anything ",
            " I felt I wasn’t worth much as a person ",
            " I felt that I was rather touchy ",
            " I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat) ",
            " I felt scared without any good reason ",
            " I felt that life was meaningless "
        ];
        return `${index}.${questions[index - 1]}\n Enter your score (0, 1, 2, or 3):`;
    }

    function calculateTotalScore(scores) {
        return scores.reduce((total, score) => total + score, 0);
    }

    function processQuestionnaireResponse(score) {
        //add the score to backend
        sendMessage_data();
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
    console.log("hiii")
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
});


    }

    displayBotMessage("Hi, how are you doing today? Please enter your response as Happy or Sad");
    let questionnaireStarted = false;
    let questionnaireIndex = 1;
    let questionnaireScores = [];

    function processUserResponse(response) {
        if (response.toLowerCase().includes("sad")) {
            displayBotMessage(" Please answer the following questionnaire so that we can understand you better!!");
            displayBotMessage(`Please read each statement and circle a number 0, 1, 2, or 3 which indicates how much the statement applied to you over the past week. There are no right or wrong answers. Do not spend too much time on any statement. The rating scale is as follows: 0 --Did not apply to me at all 1 --Applied to me to some degree, or some of the time 2 --Applied to me to a considerable degree or a good part of the time 3 --Applied to me very much or most of the time`);
            questionnaireStarted = true;
            displayBotMessage(getQuestionnairePrompt(questionnaireIndex));
        }
        if (response.toLowerCase().includes("happy")) {
            displayBotMessage("Wow great ! keep up the good work");
        } else {
            // Handle other responses accordingly
        }
    }

    function sendMessage() {
        const message = userInput.value;
        if (message.trim() !== "") {
            if (!questionnaireStarted) {
                displayUserMessage(message);
                processUserResponse(message);
            } else {
                const score = parseInt(message.trim());
                if (!isNaN(score) && score >= 0 && score <= 3) {
                    questionnaireScores.push(score);
                    questionnaireIndex++;
                    if (questionnaireIndex <= 21) {
                        displayUserMessage(message);
                        displayBotMessage(getQuestionnairePrompt(questionnaireIndex));
                    } else {
                        displayUserMessage(message);
                        const totalScore = calculateTotalScore(questionnaireScores);
                        processQuestionnaireResponse(totalScore);
                    }
                } else {
                    displayBotMessage("Please enter a valid score between 0 and 3.");
                }
            }
            userInput.value = "";
        }
    }

    function getQuestionnairePrompt(index) {
        const questions = [
            " I found it hard to wind down ",
            " I was aware of dryness of my mouth ",
            " I couldn’t seem to experience any positive feeling at all ",
            " I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion) ",
            " I found it difficult to work up the initiative to do things ",
            " I tended to over-react to situations ",
            " I experienced trembling (e.g. in the hands) ",
            " I felt that I was using a lot of nervous energy ",
            " I was worried about situations in which I might panic and make a fool of myself ",
            " I felt that I had nothing to look forward to ",
            " I found myself getting agitated ",
            " I found it difficult to relax ",
            " I felt down-hearted and blue ",
            " I was intolerant of anything that kept me from getting on with what I was doing ",
            " I felt I was close to panic ",
            " I was unable to become enthusiastic about anything ",
            " I felt I wasn’t worth much as a person ",
            " I felt that I was rather touchy ",
            " I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat) ",
            " I felt scared without any good reason ",
            " I felt that life was meaningless "
        ];
        return `${index}.${questions[index - 1]}\n Enter your score (0, 1, 2, or 3):`;
    }

    function calculateTotalScore(scores) {
        return scores.reduce((total, score) => total + score, 0);
    }

    function processQuestionnaireResponse(score) {
        sendMessage();
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
    console.log("hiii")
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
});

