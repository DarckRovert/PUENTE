const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const modelSelect = document.getElementById('model-select');
const btnFindWindow = document.getElementById('btn-find-window');
const windowSearchInput = document.getElementById('window-search');
const windowStatus = document.getElementById('window-status');
const streamImg = document.getElementById('stream-img');
const btnToggleStream = document.getElementById('toggle-stream');
const thoughtLog = document.getElementById('thought-log');
const panicBtn = document.getElementById('panic-btn');

let isStreaming = false;

// --- DYNAMIC LOGS (SUSURROS DEL VACIO) ---
function addThought(text) {
    const entry = document.createElement('div');
    entry.classList.add('thought-entry');
    entry.innerText = `> ${new Date().toLocaleTimeString()} || ${text}`;
    thoughtLog.prepend(entry);
    if (thoughtLog.childNodes.length > 50) thoughtLog.removeChild(thoughtLog.lastChild);
}

// --- STREAM LOGIC ---
function toggleStream() {
    isStreaming = !isStreaming;
    if (isStreaming) {
        streamImg.src = 'http://localhost:5000/stream';
        streamImg.style.display = 'block';
        btnToggleStream.classList.add('active');
        addThought('Conectando visión con el Ojo del Vacío...');
    } else {
        streamImg.src = '';
        streamImg.style.display = 'none';
        btnToggleStream.classList.remove('active');
        addThought('Cerrando portal de visión.');
    }
}

btnToggleStream.addEventListener('click', toggleStream);
toggleStream(); // Iniciar por defecto

// --- CHAT & COMMAND LOGIC ---
async function appendMessage(role, content) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', role);
    msgDiv.innerHTML = `<p>${content}</p>`;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msgDiv;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    
    userInput.value = '';
    await appendMessage('user', text);
    addThought(`Comando recibido: "${text}"`);

    // Lógica para enviar ordenes al backend de IA
    const botMsgDiv = await appendMessage('bot', 'Canalizando energía...');
    const botTextP = botMsgDiv.querySelector('p');

    try {
        const response = await fetch('http://localhost:5000/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'think', text: text, model: modelSelect.value })
        });
        const data = await response.json();
        botTextP.innerText = data.output || data.error || 'Silencio en el vacío.';
    } catch (e) {
        botTextP.innerText = 'Error de conexión con el núcleo.';
    }
}

sendBtn.addEventListener('click', sendMessage);

const startAgentBtn = document.getElementById('start-agent-btn');

// --- START AGENT ---
startAgentBtn.addEventListener('click', async () => {
    addThought('Iniciando ritual de liberación...');
    startAgentBtn.innerText = 'ENVIANDO ORDEN...';
    
    try {
        const response = await fetch('http://localhost:5000/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'start_agent' })
        });
        const data = await response.json();
        if (data.success) {
            startAgentBtn.innerText = 'ESBIRRO LIBERADO';
            startAgentBtn.classList.add('active');
            addThought('¡El Esbirro del Terror está activo!');
        } else {
            addThought(`Error: ${data.message}`);
            startAgentBtn.innerText = 'LIBERAR ESBIRRO';
        }
    } catch (e) {
        addThought('Fallo de conexión en el ritual.');
    }
});

// --- PANIC PROTOCOL ---
panicBtn.addEventListener('click', async () => {
    addThought('¡PROTOCOLO DE PÁNICO ACTIVADO!');
    panicBtn.style.background = '#ef4444';
    panicBtn.innerText = 'SISTEMA BLOQUEADO';
    startAgentBtn.innerText = 'LIBERAR ESBIRRO';
    startAgentBtn.classList.remove('active');
    
    try {
        const response = await fetch('http://localhost:5000/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'panic' })
        });
        const data = await response.json();
        if (data.success) {
            appendMessage('system', '!!! AGENTE DESACTIVADO POR SEGURIDAD !!!');
        }
    } catch (e) {
        console.error('Fallo al enviar señal de pánico total.');
    }
});

// --- WINDOW BINDING ---
btnFindWindow.addEventListener('click', async () => {
    const title = windowSearchInput.value;
    addThought(`Vinculando esencia con: ${title}`);
});

// --- TELEMETRY POLLING (LATENCY & THOUGHTS) ---
setInterval(async () => {
    try {
        const latencyBadge = document.getElementById('latency-ms');
        const response = await fetch('http://localhost:5000/get_log');
        const data = await response.json();
        
        if (data.latency !== undefined) {
            latencyBadge.innerText = `LATENCY: ${Math.round(data.latency * 1000)}ms`;
            // Cambiar color según latencia
            if (data.latency < 1.0) latencyBadge.style.color = '#39ff14';
            else if (data.latency < 3.0) latencyBadge.style.color = '#facc15';
            else latencyBadge.style.color = '#ef4444';
        }
        
        if (data.thought && data.thought !== "En espera...") {
            // Solo añadir si es un pensamiento nuevo o relevante
            // addThought(data.thought); // Desactivado para no saturar, ya se ve en el log
        }
    } catch (e) {
        // Silencio en la telemetría
    }
}, 1000);
