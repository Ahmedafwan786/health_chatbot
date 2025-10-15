function addMessage(text, sender) {
    const chatBox = document.getElementById('chat-box');
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    // Preserve newlines
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const age = document.getElementById('age').value;
    const message = document.getElementById('message').value;
    if (!age || !message) return;
    addMessage(message, 'user');
    document.getElementById('message').value = '';
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ age: age, message: message })
        });
        const data = await res.json();
        addMessage(data.response, 'bot');
    } catch (e) {
        addMessage('Error: Could not reach server.', 'bot');
    }
}

document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('message').addEventListener('keydown', function(e){
    if (e.key === 'Enter') sendMessage();
});
