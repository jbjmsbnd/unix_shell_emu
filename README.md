# Unix Shell Emulator (VFS)

## 1. Общее описание

Эмулятор командной оболочки UNIX-подобной ОС с виртуальной файловой
системой (VFS). Реализован на Python с графическим интерфейсом на
Tkinter. Эмулятор повторяет поведение командной строки UNIX-подобных
систем: разбирает введённую строку на команду и аргументы, раскрывает
переменные окружения хоста, выполняет поддерживаемые команды и
сообщает об ошибках.

Работа выполняется поэтапно:

- [x] Этап 1. REPL — диалог с пользователем, парсер, заглушки команд.
- [x] Этап 2. Конфигурация — параметры командной строки, стартовый скрипт.
- [ ] Этап 3. VFS — загрузка виртуальной файловой системы из ZIP-архива.
- [ ] Этап 4. Основные команды — `ls`, `cd`, `head`, `tac`, `wc`.
- [ ] Этап 5. Дополнительные команды — `cp`.

## 2. Функции и настройки

### Поддерживаемые команды

| Команда | Аргументы | Описание                                       |
|---------|-----------|------------------------------------------------|
| `ls`    | до 1      | вывести список файлов (заглушка на этапе 1)    |
| `cd`    | до 1      | сменить каталог (заглушка на этапе 1)          |
| `exit`  | нет       | завершить работу эмулятора                     |

### Раскрытие переменных окружения

Команды поддерживают подстановку переменных окружения реальной ОС
через `os.path.expandvars`. Например, `$USERPROFILE` на Windows или
`$HOME` при заданной переменной.

### Параметры командной строки

| Параметр   | Описание                                        |
|------------|-------------------------------------------------|
| `--vfs`    | путь к физическому расположению VFS-архива      |
| `--script` | путь к стартовому скрипту эмулятора (`.emu`)    |
| `--no-gui` | выполнить стартовый скрипт в консоли без окна   |

При запуске эмулятор печатает отладочный вывод всех заданных
параметров:

```
[debug] vfs    = some.zip
[debug] script = scripts\start_simple.emu
[debug] no_gui = False
```
## 3. Сборка и запуск тестов

### Требования

- Python 3.10+
- Tkinter (входит в стандартную поставку Python для Windows)

### Установка окружения

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pytest
```

### Запуск эмулятора

```cmd
run.bat
```

или

```cmd
python -m src.main
```

### Запуск тестов

```cmd
python -m pytest
```

или с подробным выводом:

```cmd
python -m pytest -v
```

## 4. Примеры использования

### Успешные команды

```
$ ls
ls
$ ls /home
ls /home
$ cd
cd
$ cd /tmp
cd /tmp
```

### Обработка ошибок

```
$ ls a b
Error: ls: invalid number of arguments
$ cd a b
Error: cd: invalid number of arguments
$ echo hello
Error: unknown command: echo
```

### Раскрытие переменной окружения

```
$ ls $USERPROFILE
ls C:\Users\Admin
```

### Завершение работы

```
$ exit
```
Окно эмулятора закрывается.

### Запуск без параметров (интерактивный GUI)

```cmd
run.bat
```
или
```cmd
python -m src.main
```

### Запуск со стартовым скриптом (GUI + автопроигрывание)

```cmd
python -m src.main --vfs some.zip --script scripts\start_simple.emu
```

Окно открывается, в нём автоматически проигрывается скрипт,
после чего можно продолжать вводить команды вручную.

### Запуск стартового скрипта в консоли

```cmd
python -m src.main --script scripts\start_with_errors.emu --no-gui
```

Вывод:
```
[debug] vfs    = None
[debug] script = scripts\start_with_errors.emu
[debug] no_gui = True
$ ls
ls
$ ls one two
Error: ls: invalid number of arguments
$ echo hello
Error: unknown command: echo
$ cd a b
Error: cd: invalid number of arguments
$ unknown_command
Error: unknown command: unknown_command
$ cd /var
cd /var
$ ls
ls
$ exit
[script] total=8 executed=7 failed=4 exited=True
```

### Готовые скрипты ОС

В папке `scripts/` лежат готовые `.bat` и `.sh`:

- `run_minimal.bat` — запуск без параметров (GUI).
- `run_with_script.bat` — запуск с `--vfs` и `--script` (GUI).
- `run_console.bat` — запуск с `--no-gui` (консоль).
- `.sh`-аналоги — для Unix-подобных систем.

## 5. Структура репозитория

```
.
├── src/
│   ├── __init__.py
│   ├── emulator.py   # парсер и исполнитель команд
│   ├── runner.py     # проигрывание стартового скрипта
│   ├── gui.py        # графический интерфейс (Tkinter)
│   └── main.py       # точка входа, argparse
├── tests/
│   ├── __init__.py
│   ├── test_emulator.py
│   └── test_runner.py
├── scripts/          # стартовые скрипты и скрипты ОС
│   ├── README.md
│   ├── start_simple.emu
│   ├── start_with_errors.emu
│   ├── run_minimal.bat / .sh
│   ├── run_with_script.bat / .sh
│   └── run_console.bat / .sh
├── README.md
├── pyproject.toml
├── run.bat
└── run.sh
```

## 6. История этапов

Каждый этап оформляется отдельными коммитами с сообщениями в стиле
Conventional Commits (`feat(...)`, `docs(...)`, `chore(...)`).
