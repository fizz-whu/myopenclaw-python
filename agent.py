from typing import Optional, List
from openai import OpenAI
from config import Config, AgentConfig
from session import SessionStore, SessionEntry
from routing import ResolvedRoute
import os


class AgentResult:
    def __init__(self, response: str, success: bool = True, error: Optional[str] = None):
        self.response = response
        self.success = success
        self.error = error


class AgentProcessor:
    def __init__(self, config: Config, session_store: SessionStore):
        self.config = config
        self.session_store = session_store
        self.clients: dict = {}

    def _get_client(self, provider: str) -> OpenAI:
        if provider not in self.clients:
            if provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY not set")
                self.clients[provider] = OpenAI(api_key=api_key)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        return self.clients[provider]

    def process_message(
        self,
        route: ResolvedRoute,
        message: str,
        images: Optional[List[str]] = None,
    ) -> AgentResult:
        try:
            agent_config = self.config.agents.get(route.agent_id)
            if not agent_config:
                return AgentResult(
                    response="",
                    success=False,
                    error=f"Agent {route.agent_id} not found",
                )

            session = self.session_store.get_or_create(route.session_key)

            session.add_message("user", message)

            messages = self._build_messages(session, agent_config, images)

            client = self._get_client(agent_config.provider)

            response = client.chat.completions.create(
                model=agent_config.model,
                messages=messages,
            )

            assistant_message = response.choices[0].message.content or ""

            session.add_message("assistant", assistant_message)
            self.session_store.update(route.session_key, session)

            return AgentResult(response=assistant_message, success=True)

        except Exception as e:
            return AgentResult(response="", success=False, error=str(e))

    def _build_messages(
        self,
        session: SessionEntry,
        agent_config: AgentConfig,
        images: Optional[List[str]] = None,
    ) -> List[dict]:
        messages = []

        if agent_config.system_prompt:
            messages.append({
                "role": "system",
                "content": agent_config.system_prompt,
            })

        for msg in session.messages[-20:]:
            messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        return messages
