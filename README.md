# Unix Shell Emulator (VFS)

## Описание

Эмулятор командной строки UNIX-подобной ОС на Python с GUI на Tkinter.
Поддерживает виртуальную файловую систему (VFS) из ZIP-архива в памяти.

Этапы 1–5 выполнены.

## Функции и настройки

| Команда | Что делает                        |
|---------|-----------------------------------|
| `ls`    | список файлов                     |
| `cd`    | сменить директорию                |
| `head`  | первые 10 строк файла             |
| `tac`   | строки в обратном порядке         |
| `wc`    | строки, слова, байты              |
| `cp`    | копировать файл (в памяти)        |
| `exit`  | выйти                             |

Параметры: `--vfs` (путь к ZIP), `--script` (стартовый скрипт),
`--no-gui` (без окна). Переменные окружения раскрываются через
`os.path.expandvars`.

## Сборка и тесты

Нужен Python 3.10+.

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pytest
python -m pytest
```

Запуск: `run.bat` или `python -m src.main`.

## Примеры

```cmd
run.bat
python -m src.main --vfs scripts\vfs\deep.zip --script scripts\start_deep.emu
```

Тестовые архивы: `python scripts\make_vfs.py`.
