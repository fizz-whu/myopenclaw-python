from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from config import config
from routing import resolve_agent_route, RoutePeer, ResolvedRoute
from agent import AgentProcessor, AgentResult
from session import SessionStore


app = FastAPI(title="MyOpenClaw Gateway", version="0.1.0")

session_store = SessionStore()
agent_processor = AgentProcessor(config, session_store)


class MessageRequest(BaseModel):
    message: str
    channel: str = "api"
    account_id: Optional[str] = None
    peer_kind: Optional[str] = None
    peer_id: Optional[str] = None
    images: Optional[List[str]] = None


class MessageResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None
    session_key: str
    agent_id: str


@app.get("/")
async def root():
    return {"status": "ok", "service": "myopenclaw-python"}


@app.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    peer = None
    if request.peer_kind and request.peer_id:
        peer = RoutePeer(kind=request.peer_kind, id=request.peer_id)

    route = resolve_agent_route(
        cfg=config,
        channel=request.channel,
        account_id=request.account_id,
        peer=peer,
    )

    result: AgentResult = agent_processor.process_message(
        route=route,
        message=request.message,
        images=request.images,
    )

    return MessageResponse(
        response=result.response,
        success=result.success,
        error=result.error,
        session_key=route.session_key,
        agent_id=route.agent_id,
    )


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/sessions")
async def list_sessions():
    return {
        "sessions": [
            {
                "key": key,
                "message_count": len(entry.messages),
                "created_at": entry.created_at,
                "updated_at": entry.updated_at,
            }
            for key, entry in session_store.sessions.items()
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=config.gateway_port)
