"""
CHENU - Intégrations Externes
==============================
Connecteurs pour ClickUp, Google Drive, Notion, Slack, et plus.
"""

import asyncio
import aiohttp
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger("CHENU.Integrations")

# ============== BASE INTEGRATION ==============

@dataclass
class IntegrationConfig:
    """Configuration d'une intégration."""
    name: str
    api_key: str
    base_url: str
    workspace_id: Optional[str] = None
    extra: Dict[str, Any] = None

class BaseIntegration(ABC):
    """Classe de base pour toutes les intégrations."""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def connect(self):
        """Initialise la session HTTP."""
        self.session = aiohttp.ClientSession(
            headers=self._get_headers()
        )
        logger.info(f"🔗 Connected to {self.config.name}")
    
    async def disconnect(self):
        """Ferme la session."""
        if self.session:
            await self.session.close()
    
    @abstractmethod
    def _get_headers(self) -> Dict[str, str]:
        """Retourne les headers d'authentification."""
        pass
    
    async def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Effectue une requête HTTP."""
        url = f"{self.config.base_url}{endpoint}"
        async with self.session.request(method, url, json=data) as resp:
            return await resp.json()

# ============== CLICKUP INTEGRATION ==============

class ClickUpIntegration(BaseIntegration):
    """
    Intégration ClickUp pour la gestion de projets.
    """
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": self.config.api_key,
            "Content-Type": "application/json"
        }
    
    # === SPACES ===
    async def get_spaces(self) -> List[Dict]:
        """Récupère tous les espaces du workspace."""
        result = await self._request(
            "GET", 
            f"/team/{self.config.workspace_id}/space"
        )
        return result.get("spaces", [])
    
    # === FOLDERS ===
    async def get_folders(self, space_id: str) -> List[Dict]:
        """Récupère les dossiers d'un espace."""
        result = await self._request("GET", f"/space/{space_id}/folder")
        return result.get("folders", [])
    
    # === LISTS ===
    async def get_lists(self, folder_id: str) -> List[Dict]:
        """Récupère les listes d'un dossier."""
        result = await self._request("GET", f"/folder/{folder_id}/list")
        return result.get("lists", [])
    
    async def create_list(self, folder_id: str, name: str) -> Dict:
        """Crée une nouvelle liste."""
        return await self._request("POST", f"/folder/{folder_id}/list", {
            "name": name
        })
    
    # === TASKS ===
    async def get_tasks(self, list_id: str) -> List[Dict]:
        """Récupère les tâches d'une liste."""
        result = await self._request("GET", f"/list/{list_id}/task")
        return result.get("tasks", [])
    
    async def create_task(
        self, 
        list_id: str, 
        name: str, 
        description: str = "",
        priority: int = 3,
        due_date: Optional[int] = None,
        assignees: List[str] = None,
        tags: List[str] = None
    ) -> Dict:
        """Crée une nouvelle tâche."""
        payload = {
            "name": name,
            "description": description,
            "priority": priority,
        }
        if due_date:
            payload["due_date"] = due_date
        if assignees:
            payload["assignees"] = assignees
        if tags:
            payload["tags"] = tags
            
        return await self._request("POST", f"/list/{list_id}/task", payload)
    
    async def update_task(self, task_id: str, updates: Dict) -> Dict:
        """Met à jour une tâche."""
        return await self._request("PUT", f"/task/{task_id}", updates)
    
    async def add_comment(self, task_id: str, comment: str) -> Dict:
        """Ajoute un commentaire à une tâche."""
        return await self._request("POST", f"/task/{task_id}/comment", {
            "comment_text": comment
        })
    
    # === CHENU SPECIFIC ===
    async def sync_chenu_task(self, chenu_task: Dict) -> Dict:
        """Synchronise une tâche CHENU vers ClickUp."""
        return await self.create_task(
            list_id=self.config.extra.get("default_list_id"),
            name=f"[CHENU] {chenu_task['description'][:50]}",
            description=f"""
            **Tâche CHENU**
            - ID: {chenu_task['id']}
            - Agent: {chenu_task.get('assigned_to', 'N/A')}
            - Priorité: {chenu_task.get('priority', 'medium')}
            - Créée: {chenu_task.get('created_at')}
            
            {chenu_task['description']}
            """,
            priority={"low": 4, "medium": 3, "high": 2, "critical": 1}.get(
                chenu_task.get('priority', 'medium'), 3
            ),
            tags=["chenu", "ai-generated"]
        )

# ============== GOOGLE DRIVE INTEGRATION ==============

class GoogleDriveIntegration(BaseIntegration):
    """
    Intégration Google Drive pour le stockage de fichiers.
    """
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
    
    async def list_files(
        self, 
        folder_id: str = "root",
        query: str = None,
        page_size: int = 100
    ) -> List[Dict]:
        """Liste les fichiers d'un dossier."""
        q = f"'{folder_id}' in parents and trashed = false"
        if query:
            q += f" and name contains '{query}'"
        
        result = await self._request(
            "GET",
            f"/files?q={q}&pageSize={page_size}&fields=files(id,name,mimeType,createdTime,modifiedTime)"
        )
        return result.get("files", [])
    
    async def create_folder(self, name: str, parent_id: str = "root") -> Dict:
        """Crée un nouveau dossier."""
        return await self._request("POST", "/files", {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        })
    
    async def upload_file(
        self, 
        name: str, 
        content: bytes, 
        mime_type: str,
        folder_id: str = "root"
    ) -> Dict:
        """Upload un fichier."""
        # Simplified - real implementation needs multipart upload
        metadata = {
            "name": name,
            "parents": [folder_id]
        }
        return await self._request("POST", "/files", metadata)
    
    async def download_file(self, file_id: str) -> bytes:
        """Télécharge un fichier."""
        async with self.session.get(
            f"{self.config.base_url}/files/{file_id}?alt=media"
        ) as resp:
            return await resp.read()
    
    async def create_google_doc(self, title: str, content: str = "") -> Dict:
        """Crée un Google Doc."""
        doc = await self._request("POST", "/files", {
            "name": title,
            "mimeType": "application/vnd.google-apps.document"
        })
        # Would need Docs API to add content
        return doc
    
    async def share_file(self, file_id: str, email: str, role: str = "reader") -> Dict:
        """Partage un fichier."""
        return await self._request("POST", f"/files/{file_id}/permissions", {
            "type": "user",
            "role": role,
            "emailAddress": email
        })
    
    # === CHENU SPECIFIC ===
    async def save_chenu_output(
        self, 
        task_id: str, 
        content: str, 
        content_type: str = "document"
    ) -> Dict:
        """Sauvegarde un output CHENU sur Drive."""
        folder_id = self.config.extra.get("chenu_folder_id", "root")
        
        if content_type == "document":
            return await self.create_google_doc(
                title=f"CHENU_Output_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                content=content
            )
        else:
            return await self.upload_file(
                name=f"chenu_output_{task_id}.txt",
                content=content.encode(),
                mime_type="text/plain",
                folder_id=folder_id
            )

# ============== NOTION INTEGRATION ==============

class NotionIntegration(BaseIntegration):
    """
    Intégration Notion pour la documentation et bases de données.
    """
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    async def search(self, query: str, filter_type: str = None) -> List[Dict]:
        """Recherche dans Notion."""
        payload = {"query": query}
        if filter_type:
            payload["filter"] = {"property": "object", "value": filter_type}
        result = await self._request("POST", "/search", payload)
        return result.get("results", [])
    
    async def get_database(self, database_id: str) -> Dict:
        """Récupère une base de données."""
        return await self._request("GET", f"/databases/{database_id}")
    
    async def query_database(
        self, 
        database_id: str, 
        filter: Dict = None,
        sorts: List[Dict] = None
    ) -> List[Dict]:
        """Query une base de données."""
        payload = {}
        if filter:
            payload["filter"] = filter
        if sorts:
            payload["sorts"] = sorts
        result = await self._request("POST", f"/databases/{database_id}/query", payload)
        return result.get("results", [])
    
    async def create_page(
        self,
        parent_id: str,
        title: str,
        properties: Dict = None,
        children: List[Dict] = None,
        is_database: bool = False
    ) -> Dict:
        """Crée une page Notion."""
        parent_type = "database_id" if is_database else "page_id"
        payload = {
            "parent": {parent_type: parent_id},
            "properties": properties or {"title": {"title": [{"text": {"content": title}}]}}
        }
        if children:
            payload["children"] = children
        return await self._request("POST", "/pages", payload)
    
    async def update_page(self, page_id: str, properties: Dict) -> Dict:
        """Met à jour une page."""
        return await self._request("PATCH", f"/pages/{page_id}", {
            "properties": properties
        })
    
    async def append_blocks(self, page_id: str, blocks: List[Dict]) -> Dict:
        """Ajoute des blocs à une page."""
        return await self._request("PATCH", f"/blocks/{page_id}/children", {
            "children": blocks
        })
    
    # === HELPER: CREATE BLOCKS ===
    @staticmethod
    def text_block(content: str, block_type: str = "paragraph") -> Dict:
        """Crée un bloc texte."""
        return {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [{"type": "text", "text": {"content": content}}]
            }
        }
    
    @staticmethod
    def heading_block(content: str, level: int = 1) -> Dict:
        """Crée un bloc heading."""
        heading_type = f"heading_{level}"
        return {
            "object": "block",
            "type": heading_type,
            heading_type: {
                "rich_text": [{"type": "text", "text": {"content": content}}]
            }
        }
    
    # === CHENU SPECIFIC ===
    async def create_chenu_task_page(self, task: Dict) -> Dict:
        """Crée une page Notion pour une tâche CHENU."""
        database_id = self.config.extra.get("tasks_database_id")
        
        return await self.create_page(
            parent_id=database_id,
            title=task["description"][:50],
            properties={
                "Name": {"title": [{"text": {"content": task["description"][:50]}}]},
                "Status": {"select": {"name": task.get("status", "pending")}},
                "Priority": {"select": {"name": task.get("priority", "medium")}},
                "Agent": {"rich_text": [{"text": {"content": task.get("assigned_to", "")}}]},
                "Task ID": {"rich_text": [{"text": {"content": task["id"]}}]}
            },
            children=[
                self.heading_block("Description", 2),
                self.text_block(task["description"]),
                self.heading_block("Contexte", 2),
                self.text_block(json.dumps(task.get("context", {}), indent=2))
            ],
            is_database=True
        )

# ============== SLACK INTEGRATION ==============

class SlackIntegration(BaseIntegration):
    """Intégration Slack pour les notifications."""
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
    
    async def post_message(
        self,
        channel: str,
        text: str,
        blocks: List[Dict] = None,
        thread_ts: str = None
    ) -> Dict:
        """Envoie un message."""
        payload = {"channel": channel, "text": text}
        if blocks:
            payload["blocks"] = blocks
        if thread_ts:
            payload["thread_ts"] = thread_ts
        return await self._request("POST", "/chat.postMessage", payload)
    
    async def notify_task_complete(self, task: Dict, channel: str) -> Dict:
        """Notifie la complétion d'une tâche CHENU."""
        return await self.post_message(
            channel=channel,
            text=f"✅ Tâche CHENU terminée: {task['description'][:50]}",
            blocks=[
                {"type": "header", "text": {"type": "plain_text", "text": "✅ Tâche terminée"}},
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*{task['description']}*"}},
                {"type": "context", "elements": [
                    {"type": "mrkdwn", "text": f"Agent: {task.get('assigned_to', 'N/A')}"},
                    {"type": "mrkdwn", "text": f"ID: `{task['id']}`"}
                ]}
            ]
        )

# ============== INTEGRATION MANAGER ==============

class IntegrationManager:
    """Gestionnaire central des intégrations."""
    
    def __init__(self):
        self.integrations: Dict[str, BaseIntegration] = {}
    
    def register(self, name: str, integration: BaseIntegration):
        self.integrations[name] = integration
        logger.info(f"📦 Integration registered: {name}")
    
    async def connect_all(self):
        for name, integration in self.integrations.items():
            await integration.connect()
    
    async def disconnect_all(self):
        for integration in self.integrations.values():
            await integration.disconnect()
    
    def get(self, name: str) -> Optional[BaseIntegration]:
        return self.integrations.get(name)

# ============== USAGE EXAMPLE ==============

async def main():
    # Configuration
    manager = IntegrationManager()
    
    # ClickUp
    manager.register("clickup", ClickUpIntegration(IntegrationConfig(
        name="ClickUp",
        api_key="pk_xxx",
        base_url="https://api.clickup.com/api/v2",
        workspace_id="team_id",
        extra={"default_list_id": "list_id"}
    )))
    
    # Google Drive
    manager.register("drive", GoogleDriveIntegration(IntegrationConfig(
        name="Google Drive",
        api_key="access_token",
        base_url="https://www.googleapis.com/drive/v3",
        extra={"chenu_folder_id": "folder_id"}
    )))
    
    # Notion
    manager.register("notion", NotionIntegration(IntegrationConfig(
        name="Notion",
        api_key="secret_xxx",
        base_url="https://api.notion.com/v1",
        extra={"tasks_database_id": "db_id"}
    )))
    
    # Connect all
    await manager.connect_all()
    
    # Use integrations
    clickup = manager.get("clickup")
    spaces = await clickup.get_spaces()
    print(f"Found {len(spaces)} ClickUp spaces")
    
    await manager.disconnect_all()

if __name__ == "__main__":
    asyncio.run(main())
