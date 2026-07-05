# config.py

cfg = {
    # Основные данные проекта
    "name": "open-music",
    "сокращено": "OMuz",
    
    # Настройки звука по умолчанию
    "volume_default": 0.5,        # Громкость при старте (от 0.0 до 1.0)
    
    # Включение/выключение дополнительных функций ("всяких штук")
    "hotkeys_enabled": True,       # Глобальные горячие клавиши в Windows 10
    "notifications_enabled": True, # Всплывающие системные уведомления Windows при смене трека
    "auto_scan_interval": 5,       # Как часто (в секундах) проверять появление новых MP3 в папке music
    
    # Комбинации клавиш (если hotkeys_enabled = True)
    # Можно будет настроить любые под себя
    "keys": {
        "play_pause": "ctrl+alt+p",
        "next_track": "ctrl+alt+right",
        "prev_track": "ctrl+alt+left"
    }
}
