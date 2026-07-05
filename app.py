import os
import threading
import time
from flask import Flask, render_template, jsonify, request, send_from_directory
import pygame
from config import cfg

# 1. Вычисляем абсолютный путь к корню проекта (где лежит app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Собираем точные абсолютные пути к папкам html и music
HTML_DIR = os.path.join(BASE_DIR, 'html')
MUSIC_DIR = os.path.join(BASE_DIR, 'music')

# 3. Инициализируем Flask с указанием правильной корневой папки для шаблонов
app = Flask(
    __name__, 
    template_folder=HTML_DIR,  # Указываем, что корень шаблонов — это папка html
    static_folder=HTML_DIR,
    static_url_path='/html'
)

PROJECT_NAME = cfg.get("name", "open-music")
PROJECT_SHORT = cfg.get("сокращено", "OMuz")

if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)

pygame.mixer.init()
pygame.mixer.music.set_volume(cfg.get("volume_default", 0.5))

tracks = []
current_track_index = 0
is_playing = False

def update_tracks_list():
    global tracks
    if os.path.exists(MUSIC_DIR):
        tracks = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]

update_tracks_list()

def audio_loop():
    global current_track_index, is_playing
    while True:
        time.sleep(1)
        if is_playing and not pygame.mixer.music.get_busy():
            if tracks:
                current_track_index = (current_track_index + 1) % len(tracks)
                track_path = os.path.join(MUSIC_DIR, tracks[current_track_index])
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()
                print(f"[{PROJECT_SHORT}] Автопереключение на: {tracks[current_track_index]}")

threading.Thread(target=audio_loop, daemon=True).start()

# ИСПРАВЛЕННЫЙ РОУТ: Просто index.htm, без указания папки html\\
@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/api/state')
def get_state():
    update_tracks_list()
    return jsonify({
        "project_name": PROJECT_NAME,
        "tracks": tracks,
        "current_index": current_track_index,
        "is_playing": is_playing,
        "current_track": tracks[current_track_index] if tracks else "Нет треков"
    })

@app.route('/api/control', methods=['POST'])
def control():
    global current_track_index, is_playing
    data = request.json
    action = data.get('action')
    
    if not tracks:
        return jsonify({"status": "no tracks"})

    if action == 'play':
        if not is_playing:
            pygame.mixer.music.unpause()
            if not pygame.mixer.music.get_busy():
                track_path = os.path.join(MUSIC_DIR, tracks[current_track_index])
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()
            is_playing = True
            print(f"[{PROJECT_SHORT}] Играет: {tracks[current_track_index]}")
            
    elif action == 'pause':
        pygame.mixer.music.pause()
        is_playing = False
        print(f"[{PROJECT_SHORT}] Пауза")
        
    elif action == 'next':
        current_track_index = (current_track_index + 1) % len(tracks)
        track_path = os.path.join(MUSIC_DIR, tracks[current_track_index])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        is_playing = True
        print(f"[{PROJECT_SHORT}] Следующий: {tracks[current_track_index]}")
        
    elif action == 'prev':
        current_track_index = (current_track_index - 1) % len(tracks)
        track_path = os.path.join(MUSIC_DIR, tracks[current_track_index])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        is_playing = True
        print(f"[{PROJECT_SHORT}] Предыдущий: {tracks[current_track_index]}")
        
    elif action == 'select':
        current_track_index = data.get('index', 0)
        track_path = os.path.join(MUSIC_DIR, tracks[current_track_index])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        is_playing = True
        print(f"[{PROJECT_SHORT}] Выбран трек: {tracks[current_track_index]}")
        
    elif action == 'volume':
        val = float(data.get('value', 0.5))
        pygame.mixer.music.set_volume(val)

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    os.system("browser.exe http://127.0.0.1:5000/")
    print(f"[{PROJECT_SHORT}] Сервер успешно запущен!")
    app.run(debug=True, port=5000, use_reloader=False)