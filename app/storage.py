from typing import Dict, List, Optional

class TaskStorage:
    def __init__(self):
        self.tasks: Dict[int, dict] = {}
        self.next_id: int = 1

    def create(self, task_data: dict) -> dict:
        task_id = self.next_id
        self.next_id += 1
        task = {"id": task_id, **task_data}
        self.tasks[task_id] = task
        return task

    def get_by_id(self, task_id: int) -> Optional[dict]:
        return self.tasks.get(task_id)

    def get_all(self) -> List[dict]:
        return list(self.tasks.values())

    def update_status(self, task_id: int, status: str) -> Optional[dict]:
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            return self.tasks[task_id]
        return None

    def delete(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def clear(self):
        self.tasks.clear()
        self.next_id = 1

storage = TaskStorage()