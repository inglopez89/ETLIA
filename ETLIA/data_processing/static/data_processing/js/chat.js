function handleFileSelect(event) {
    const files = Array.from(event.target.files);
    
    const infoDiv = document.getElementById('selectedFilesInfo');
    const chatInput = document.getElementById('chatInput');
    
    if (files.length > 0) {
        if (files.length > 4) {
            infoDiv.textContent = '⚠️ Maximum 4 files allowed. Please select fewer files.';
            infoDiv.style.display = 'block';
            infoDiv.style.color = '#c53030';
            chatInput.value = '';
        } else {
            const fileNames = files.map(f => f.name).join(', ');
            infoDiv.textContent = `✓ ${files.length} file(s) selected: ${fileNames}`;
            infoDiv.style.display = 'block';
            infoDiv.style.color = '#4a5568';
            chatInput.value = `${files.length} file(s) ready to upload`;
            
            // Brief delay to show selection feedback before auto-submitting
            setTimeout(() => {
                document.getElementById('uploadForm').submit();
            }, 500);
        }
    } else {
        infoDiv.style.display = 'none';
        chatInput.value = '';
    }
}

function deleteFile(fileId) {
    if (!confirm('Are you sure you want to delete this file?')) {
        return;
    }

    const card = document.getElementById(`file-card-${fileId}`);
    card.style.opacity = '0.5';
    card.style.pointerEvents = 'none';

    fetch(`/data/files/delete/${fileId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove the card from DOM
            card.remove();
            
            // Update file count
            const filesGrid = document.querySelector('.files-grid');
            const heading = document.querySelector('.files-section h2');
            const remainingFiles = filesGrid ? filesGrid.children.length : 0;
            
            if (heading) {
                heading.textContent = `Uploaded Files (${remainingFiles})`;
            }
            
            // Show "no files" message if all files deleted
            if (remainingFiles === 0 && filesGrid) {
                filesGrid.parentElement.innerHTML = '<div class="no-files">No files uploaded yet. Click the + button above to upload your first file!</div>';
            }
        } else {
            card.style.opacity = '1';
            card.style.pointerEvents = 'auto';
            alert('Failed to delete file. Please refresh the page and try again.');
        }
    })
    .catch(error => {
        card.style.opacity = '1';
        card.style.pointerEvents = 'auto';
        alert('Network error while deleting file. Please check your connection and try again.');
    });
}

async function handleChatInput(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const chatInput = document.getElementById('chatInput');
        const message = chatInput.value.trim();

        if (message) {
            const chatMessages = document.getElementById('chatMessages');

            // Add user message to chat
            const messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message user';
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);

            // Clear input and scroll
            chatInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // Add loading indicator
            const systemDiv = document.createElement('div');
            systemDiv.className = 'chat-message system';
            systemDiv.textContent = 'Procesando...';
            chatMessages.appendChild(systemDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch(`/data/ai_interaction/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });
                const data = await response.json();

                if (data.error) {
                    systemDiv.textContent = `Error: ${data.error}`;
                } else {
                    let displayText = data.interpretation || '';
                    if (data.action) {
                        displayText += `\n\nAcción ejecutada: ${data.action}`;
                    }
                    if (data.rows_file1 !== undefined && data.rows_file2 !== undefined) {
                        displayText += `\nResultado: ${data.rows_file1} filas en el archivo 1, ${data.rows_file2} filas en el archivo 2, ${data.columns_file1?.length} columnas en el archivo 1, ${data.columns_file2?.length} columnas en el archivo 2.`;
                    }
                    systemDiv.style.whiteSpace = 'pre-wrap';
                    systemDiv.textContent = displayText || JSON.stringify(data);
                }
            } catch (error) {
                systemDiv.textContent = 'Error al procesar tu solicitud.';
            }

            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Scroll chat to bottom on load
window.onload = function() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
};
