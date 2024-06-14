// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded!');
    // Add any custom JS here
});

    const groupID = "{{ group.id }}";
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + groupID + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const message = data.message;
        const username = data.username;
        const messageType = data.message_type;

        const chatLog = document.getElementById('chat-log');
        const messageElement = document.createElement('div');
        
        if (messageType === 'text') {
            messageElement.innerHTML = `<strong>${username}:</strong> ${message}`;
        } else if (messageType === 'image') {
            messageElement.innerHTML = `<strong>${username}:</strong> <img src="${message}" alt="Image" width="200">`;
        } else if (messageType === 'audio') {
            messageElement.innerHTML = `<strong>${username}:</strong> <audio controls><source src="${message}" type="audio/mpeg">Your browser does not support the audio element.</audio>`;
        }

        chatLog.appendChild(messageElement);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.getElementById('chat-message-form').onsubmit = function(e) {
        e.preventDefault();
        const messageInput = document.getElementById('chat-message-input');
        const fileInput = document.getElementById('chat-file-input');
        const message = messageInput.value;
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const dataURL = e.target.result;
                if (file.type.startsWith('image/')) {
                    chatSocket.send(JSON.stringify({
                        'image': dataURL,
                        'username': "{{ request.user.username }}"
                    }));
                } else if (file.type.startsWith('audio/')) {
                    chatSocket.send(JSON.stringify({
                        'audio': dataURL,
                        'username': "{{ request.user.username }}"
                    }));
                }
            };
            reader.readAsDataURL(file);
        } else {
            chatSocket.send(JSON.stringify({
                'message': message,
                'username': "{{ request.user.username }}"
            }));
        }

        messageInput.value = '';
        fileInput.value = '';
    };
