document.addEventListener('DOMContentLoaded', function() {
    const talkBotButton = document.getElementById('talk-bot');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotCloseButton = document.getElementById('chatbot-close');
    const chatbotSendButton = document.getElementById('chatbot-send');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotMessages = document.getElementById('chatbot-messages');
    
    talkBotButton.addEventListener('click', function() {
    chatbotContainer.style.display = 'flex'; // Show the chat container
    talkBotButton.style.display = 'none'; // Hide the chat icon
    });
    
    chatbotCloseButton.addEventListener('click', function() {
    chatbotContainer.style.display = 'none'; // Hide the chat container
    talkBotButton.style.display = 'block'; // Show the chat icon
    });
    
    chatbotSendButton.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
    sendMessage();
    }
    });
    
    function sendMessage() {
    const userMessage = chatbotInput.value.trim();
    if (userMessage === '') return;
    
    displayMessage(userMessage, 'user');
    chatbotInput.value = '';
    
    // Simulate a response from the bot
    setTimeout(() => {
    const botResponse = getBotResponse(userMessage);
    displayMessage(botResponse, 'bot');
    }, 1000);
    }
    
    function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    chatbotMessages.appendChild(messageElement);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
    
    function getBotResponse(message) {
    message = message.toLowerCase();
    if (message.includes('hello') || message.includes('hi')) {
    return 'Hi there! How can I help you today?';
    } else if (message.includes('how are you')) {
    return 'I\'m just a bot, but I\'m doing great! How about you?';
    } else if (message.includes('website')) {
    return 'This website allows you to view bus routes, schedules, and make payments for bus tickets. How can I assist you further?';
    } else if (message.includes('pay') || message.includes('payment')) {
    return 'You can make a payment by clicking the "Pay" link next to your desired bus route.';
    } else if (message.includes('schedule') || message.includes('departure')) {
    return 'You can view the schedules and departure times for each bus route on the main page.';
    } else {
    return 'I\'m sorry, I don\'t understand that yet. Can you please ask something else?';
    }
    }
    });