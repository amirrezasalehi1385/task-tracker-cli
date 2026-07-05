import sys
import json
import os
from datetime import datetime

if len(sys.argv) < 2:
    print("No command provided")
    sys.exit()
else:
    command = sys.argv[1]

now = datetime.now()
time_str = now.strftime("%Y-%m-%d %H:%M:%S")

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # File exists but content is corrupted/invalid JSON
        print("Error: tasks.json is corrupted or not valid JSON. Starting with an empty task list.")
        return []
    except OSError as e:
        print(f"Error: could not read {TASKS_FILE} ({e})")
        sys.exit(1)


def findMaxID():
    tasks = load_tasks()
    if not tasks:
        return 0
    else:
        return max(tasks, key=lambda task: task["id"])["id"]


def exists(tasks, desc):
    for task in tasks:
        if task["description"] == desc:
            return True
    return False


def findTaskById(tasks, id):
    for t in tasks:
        if t["id"] == id:
            return t
    return None


def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f, indent=4)
    except OSError as e:
        print(f"Error: could not save tasks ({e})")
        sys.exit(1)


def addTask(task):
    # Reject empty/whitespace-only descriptions
    if not task.strip():
        print("Error: task description cannot be empty")
        return

    tasks = load_tasks()
    if not exists(tasks, task):
        new_id = findMaxID() + 1
        tasks.append({
            "id": new_id,
            "description": task,
            "status": "todo",
            "createdAt": time_str,
            "updatedAt": time_str
        })
        save_tasks(tasks)
        print(f"Task added (ID: {new_id})")
    else:
        print(f"The Task already exists")


def updateTask(id, task):
    if not task.strip():
        print("Error: task description cannot be empty")
        return

    tasks = load_tasks()
    x = findTaskById(tasks, id)
    if x is None:
        print(f"The task with id = {id} doesn't exist")
        return
    x["description"] = task
    x["updatedAt"] = time_str
    save_tasks(tasks)
    print(f"Task {id} updated successfully")


def deleteTask(id):
    tasks = load_tasks()
    x = findTaskById(tasks, id)
    if x is None:
        print(f"The task with id = {id} doesn't exist")
        return
    tasks.remove(x)
    save_tasks(tasks)
    print(f"Task {id} deleted successfully")


def markInProgressTask(id):
    tasks = load_tasks()
    x = findTaskById(tasks, id)
    if x is None:
        print(f"The task with id = {id} doesn't exist")
        return
    x["status"] = "in-progress"
    x["updatedAt"] = time_str
    save_tasks(tasks)
    print(f"Task {id} marked as in-progress")


def markDoneTask(id):
    tasks = load_tasks()
    x = findTaskById(tasks, id)
    if x is None:
        print(f"The task with id = {id} doesn't exist")
        return
    x["status"] = "done"
    x["updatedAt"] = time_str
    save_tasks(tasks)
    print(f"Task {id} marked as done")


def listTask():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found")
        return
    for x in tasks:
        print(f"{x['id']} - {x['description']} ({x['status']})")


def listTodoTasks():
    tasks = load_tasks()
    for x in tasks:
        if x["status"] == "todo":
            print(f"{x['id']} - {x['description']} ({x['status']})")


def listInProgressTasks():
    tasks = load_tasks()
    for x in tasks:
        if x["status"] == "in-progress":
            print(f"{x['id']} - {x['description']} ({x['status']})")


def listDoneTasks():
    tasks = load_tasks()
    for x in tasks:
        if x["status"] == "done":
            print(f"{x['id']} - {x['description']} ({x['status']})")


match command:
    case "add":
        if len(sys.argv) == 3:
            addTask(sys.argv[2])
        else:
            print("Invalid Command")

    case "update":
        if len(sys.argv) == 4:
            try:
                updateTask(int(sys.argv[2]), sys.argv[3])
            except ValueError:
                print("ID must be a number")
        else:
            print("Invalid Command")

    case "delete":
        if len(sys.argv) == 3:
            try:
                deleteTask(int(sys.argv[2]))
            except ValueError:
                print("ID must be a number")
        else:
            print("Invalid Command")

    case "mark-in-progress":
        if len(sys.argv) == 3:
            try:
                markInProgressTask(int(sys.argv[2]))
            except ValueError:
                print("ID must be a number")
        else:
            print("Invalid Command")

    case "mark-done":
        if len(sys.argv) == 3:
            try:
                markDoneTask(int(sys.argv[2]))
            except ValueError:
                print("ID must be a number")
        else:
            print("Invalid Command")

    case "list":
        if len(sys.argv) == 2:
            listTask()
        elif len(sys.argv) == 3:
            # Reject unrecognized status filters instead of failing silently
            match sys.argv[2]:
                case "todo":
                    listTodoTasks()
                case "in-progress":
                    listInProgressTasks()
                case "done":
                    listDoneTasks()
                case _:
                    print("Invalid status filter. Use: todo, in-progress, or done")
        else:
            print("Invalid Command")

    case _:
        print("Unknown command")