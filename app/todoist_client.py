import logging
from typing import Any
import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TodoistTask(BaseModel):
    id: str
    content: str
    description: str | None = None
    is_completed: bool = False
    project_id: str | None = None
    priority: int = 1
    due: dict | None = None
    labels: list[str] = []


class TodoistClient:
    def __init__(self, api_token: str | None = None, mock: bool = False):
        self.api_token = api_token
        self.mock = mock or not api_token
        self.base_url = "https://api.todoist.com/rest/v2"
        self._client: httpx.AsyncClient | None = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json",
                },
                base_url=self.base_url,
                timeout=30.0,
            )
        return self._client
    
    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def get_tasks(self, project_id: str | None = None) -> list[TodoistTask]:
        if self.mock:
            return []
        
        client = await self._get_client()
        
        params = {}
        if project_id:
            params["project_id"] = project_id
        
        response = await client.get("/tasks", params=params)
        response.raise_for_status()
        
        tasks = []
        for task_data in response.json():
            tasks.append(TodoistTask(
                id=task_data["id"],
                content=task_data["content"],
                description=task_data.get("description"),
                is_completed=task_data.get("is_completed", False),
                project_id=task_data.get("project_id"),
                priority=task_data.get("priority", 1),
                due=task_data.get("due"),
                labels=task_data.get("labels", []),
            ))
        
        return tasks
    
    async def create_task(
        self,
        content: str,
        project_id: str | None = None,
        due_string: str | None = None,
        priority: int = 1,
    ) -> TodoistTask:
        if self.mock:
            return TodoistTask(id="mock-123", content=content)
        
        client = await self._get_client()
        
        data: dict[str, Any] = {
            "content": content,
            "priority": priority,
        }
        
        if project_id:
            data["project_id"] = project_id
        
        if due_string:
            data["due_string"] = due_string
        
        response = await client.post("/tasks", json=data)
        response.raise_for_status()
        
        task_data = response.json()
        return TodoistTask(
            id=task_data["id"],
            content=task_data["content"],
            description=task_data.get("description"),
            is_completed=task_data.get("is_completed", False),
            project_id=task_data.get("project_id"),
            priority=task_data.get("priority", 1),
            due=task_data.get("due"),
            labels=task_data.get("labels", []),
        )
    
    async def complete_task(self, task_id: str) -> bool:
        if self.mock:
            return True
        
        client = await self._get_client()
        
        response = await client.post(f"/tasks/{task_id}/close")
        response.raise_for_status()
        
        return True
    
    async def update_task(
        self,
        task_id: str,
        content: str | None = None,
        priority: int | None = None,
        labels: list[str] | None = None,
        due_string: str | None = None,
    ) -> TodoistTask:
        if self.mock:
            return TodoistTask(id=task_id, content=content or "mock")
        
        client = await self._get_client()
        
        data: dict[str, Any] = {}
        if content is not None:
            data["content"] = content
        if priority is not None:
            data["priority"] = priority
        if labels is not None:
            data["labels"] = labels
        if due_string is not None:
            data["due_string"] = due_string
        
        response = await client.post(f"/tasks/{task_id}", json=data)
        response.raise_for_status()
        
        task_data = response.json()
        return TodoistTask(
            id=task_data["id"],
            content=task_data["content"],
            description=task_data.get("description"),
            is_completed=task_data.get("is_completed", False),
            project_id=task_data.get("project_id"),
            priority=task_data.get("priority", 1),
            due=task_data.get("due"),
            labels=task_data.get("labels", []),
        )
    
    async def move_task(self, task_id: str, project_id: str) -> bool:
        if self.mock:
            return True
        
        client = await self._get_client()
        
        response = await client.post(
            f"/tasks/{task_id}/move",
            json={"project_id": project_id},
        )
        response.raise_for_status()
        
        return True
    
    async def delete_task(self, task_id: str) -> bool:
        if self.mock:
            return True
        
        client = await self._get_client()
        
        response = await client.delete(f"/tasks/{task_id}")
        response.raise_for_status()
        
        return True