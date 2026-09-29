# Unix Shell Emulator (VFS)

Эмулятор командной оболочки UNIX-подобной ОС с виртуальной
файловой системой. Реализован на Python с графическим
интерфейсом на Tkinter.

## Требования

- Python 3.10+
- Tkinter (входит в стандартную поставку Python для Windows)

## Установка

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pytest
```

## Запуск

```cmd
python -m src.gui
```

## Тесты

```cmd
python -m pytest
```

## Структура

```
.
├── src/            # исходный код
│   ├── __init__.py
│   ├── emulator.py # парсер и исполнитель команд
│   └── gui.py      # графический интерфейс
├── tests/          # тесты
├── scripts/        # скрипты запуска (этапы 2+)
├── README.md
├── pyproject.toml
└── run.bat
```

## Этапы

- [x] Этап 1. REPL
- [ ] Этап 2. Конфигурация
- [ ] Этап 3. VFS
- [ ] Этап 4. Основные команды
- [ ] Этап 5. Дополнительные команды