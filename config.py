from pydantic import BaseModel
from typing import Dict, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()


class AgentConfig(BaseModel):
    id: str
    name: str
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    system_prompt: Optional[str] = None


class BindingConfig(BaseModel):
    agent_id: str
    channel: str
    account_pattern: str = "*"
    peer: Optional[Dict[str, str]] = None


class Config(BaseModel):
    agents: Dict[str, AgentConfig]
    bindings: list[BindingConfig]
    default_agent_id: str
    gateway_port: int = 8000

    @classmethod
    def load(cls) -> "Config":
        return cls(
            agents={
                "default": AgentConfig(
                    id="default",
                    name="Default Agent",
                    provider=os.getenv("DEFAULT_PROVIDER", "openai"),
                    model=os.getenv("DEFAULT_MODEL", "gpt-4o-mini"),
                    system_prompt="You are a helpful assistant.",
                )
            },
            bindings=[
                BindingConfig(
                    agent_id="default",
                    channel="*",
                    account_pattern="*",
                )
            ],
            default_agent_id="default",
            gateway_port=int(os.getenv("GATEWAY_PORT", "8000")),
        )


config = Config.load()
