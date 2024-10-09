const ws = new WebSocket("ws://localhost:8000/ws");
const chatBox = document.getElementById("chat-box");
const inputBox = document.getElementById("input-box");

ws.onmessage = function(event) {
    const message = document.createElement("p");
    message.classList.add("bot-message");
    message.textContent = "Bot: " + event.data;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
};

inputBox.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
    const userMessage = inputBox.value;
    const messageElement = document.createElement("p");
    messageElement.classList.add("user-message");
    messageElement.textContent = "You: " + userMessage;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;

    ws.send(userMessage);
    inputBox.value = "";  // Clear input
    }
});