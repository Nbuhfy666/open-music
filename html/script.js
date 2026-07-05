let isPlaying = false;

async function sendAction(action, extraData = {}) {
    await fetch('/api/control', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ action: action, ...extraData })
    });
    updateState();
}

function togglePlay() {
    sendAction(isPlaying ? 'pause' : 'play');
}

function changeVolume(val) {
    sendAction('volume', { value: val });
}

async function updateState() {
    const res = await fetch('/api/state');
    const data = await res.json();
    
    isPlaying = data.is_playing;
    document.getElementById('play-btn').innerText = isPlaying ? '⏸ Пауза' : '▶ Старт';
    document.getElementById('track-name').innerText = data.current_track.replace('.mp3', '');
    
    // Автоматически ставим имя проекта из Python-конфига
    document.querySelector('h3').innerText = data.project_name;
    
    const listDiv = document.getElementById('list');
    listDiv.innerHTML = '';
    
    data.tracks.forEach((track, idx) => {
        const item = document.createElement('div');
        item.className = `track-item ${idx === data.current_index ? 'active' : ''}`;
        item.innerText = track.replace('.mp3', '');
        item.onclick = () => sendAction('select', { index: idx });
        listDiv.appendChild(item);
    });
}

// Каждую секунду синхронизируем пульт с сервером Python
setInterval(updateState, 1000);
updateState();
