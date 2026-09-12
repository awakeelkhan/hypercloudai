import logging
from task import Task

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def add_task(tasks: list[Task]) -> None:
    title = input("Enter task: ").strip()
    if not title:
        print("Task cannot be empty.")
        return
    tasks.append(Task(title))
    logger.info("Task added.")

def list_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks yet.")
        return
    for number, task in enumerate(tasks, start=1):
        status = "✓" if task.completed else " "
        print(f"{number}. [{status}] {task.title}")

def complete_task(tasks: list[Task]) -> None:
    list_tasks(tasks)
    if not tasks:
        return
    try:
        number = int(input("Enter task number: "))
        tasks[number - 1].complete()
        logger.info("Task completed.")
    except (ValueError, IndexError):
        print("Invalid task number.")

def delete_task(tasks: list[Task]) -> None:
    list_tasks(tasks)
    if not tasks:
        return
    try:
        number = int(input("Enter task number: "))
        tasks.pop(number - 1)
        logger.info("Task deleted.")
    except (ValueError, IndexError):
        print("Invalid task number.")

def main() -> None:
    tasks: list[Task] = []

    while True:
        print("\nHyperCloudAI Task Manager")
        print("1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()