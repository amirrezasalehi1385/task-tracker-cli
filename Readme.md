# Task Tracker CLI

A simple command-line interface (CLI) application to track and manage your tasks — built as part of the Task Tracker project on roadmap.sh.

Project URL: https://roadmap.sh/projects/task-tracker

This project was built to practice working with the filesystem, handling user input, and building a CLI application — without relying on any external libraries or frameworks.

## Features

- Add, update, and delete tasks
- Mark a task as `in-progress` or `done`
- List all tasks
- List tasks filtered by status (`todo`, `in-progress`, `done`)
- Tasks are persisted in a local JSON file (`tasks.json`), created automatically if it doesn't exist

## Requirements

- Python 3.10 or later (the app uses `match`/`case` statements)
- No external libraries — only Python's standard library (`sys`, `json`, `os`, `datetime`)

## Getting Started

Clone the repository and run the script directly with Python:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
python task-cli.py <command> [arguments]
```

> Replace `task-cli.py` with whatever you've named the script file.

## Usage

### Add a new task

```bash
python task-cli.py add "Buy groceries"
# Output: Task added (ID: 1)
```

If a task with the exact same description already exists, it won't be added again:

```bash
python task-cli.py add "Buy groceries"
# Output: The Task already exists
```

### Update a task

```bash
python task-cli.py update 1 "Buy groceries and cook dinner"
```

### Delete a task

```bash
python task-cli.py delete 1
```

### Mark a task as in progress or done

```bash
python task-cli.py mark-in-progress 1
python task-cli.py mark-done 1
```

### List tasks

```bash
# List all tasks
python task-cli.py list

# List tasks by status
python task-cli.py list todo
python task-cli.py list in-progress
python task-cli.py list done
```

Example output:

```
1 - Buy groceries and cook dinner (done)
2 - Finish homework (in-progress)
3 - Clean the house (todo)
```

## Task Properties

Each task stored in `tasks.json` has the following properties:

| Property     | Description                                      |
|--------------|---------------------------------------------------|
| `id`         | Unique identifier for the task                     |
| `description`| Short description of the task                      |
| `status`     | One of `todo`, `in-progress`, `done`               |
| `createdAt`  | Timestamp when the task was created                |
| `updatedAt`  | Timestamp when the task was last updated           |

## Error Handling

The CLI handles several edge cases gracefully instead of crashing:

- Missing or extra arguments (e.g. `add` with no description) → `Invalid Command`
- Non-numeric task IDs (e.g. `delete abc`) → `ID must be a number`
- Operating on a task ID that doesn't exist → `The task with id = <id> doesn't exist`
- Unknown commands → `Unknown command`
- Running with no command at all → `No command provided`

## Project Structure

```
.
├── task-cli.py     # Main application script
├── tasks.json      # Auto-generated task storage (created on first run)
└── README.md
```

## Notes & Limitations

- Task descriptions are matched exactly (case-sensitive) when checking for duplicates.
- The JSON storage file is created in the current working directory, so make sure to run the script from the same folder each time (or adjust the path in the code) to avoid losing track of your `tasks.json`.

## What I Learned

Building this project helped me practice:
- Parsing and validating command-line arguments with `sys.argv`
- Reading and writing JSON files with Python's `json` module
- Structuring a CLI app using `match`/`case` for command dispatch
- Handling errors and edge cases (invalid IDs, missing tasks, malformed input) without crashing
- Refactoring repeated logic into shared helper functions (e.g. `findTaskById`)

## License

This project is open source and available under the [MIT License](LICENSE).