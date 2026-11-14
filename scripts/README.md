# Scripts

Стартовые скрипты эмулятора (`.emu`) и скрипты запуска (`.bat`, `.sh`).

## Генератор VFS

```cmd
python scripts\make_vfs.py
```

Создаёт `minimal.zip`, `several.zip`, `deep.zip` в `scripts/vfs/`
(в git не попадают).

## Стартовые скрипты

| Файл                     | Что делает                    |
|--------------------------|-------------------------------|
| `start_simple.emu`       | команды без VFS               |
| `start_with_errors.emu`  | команды с ошибками без VFS    |
| `start_minimal.emu`      | команды на `minimal.zip`      |
| `start_several.emu`      | команды на `several.zip`      |
| `start_deep.emu`         | команды на `deep.zip`         |
| `start_all_commands.emu` | все команды с ошибками        |

## Скрипты запуска

`run_vfs_*.bat` и `.sh` — запускают эмулятор с конкретным VFS
(`minimal`, `several`, `deep`, `all`). `.bat` для Windows, `.sh` для Unix.
