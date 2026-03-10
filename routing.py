from typing import Optional
from config import Config, BindingConfig


class RoutePeer:
    def __init__(self, kind: str, id: str):
        self.kind = kind
        self.id = id


class ResolvedRoute:
    def __init__(
        self,
        agent_id: str,
        channel: str,
        account_id: str,
        session_key: str,
        matched_by: str,
    ):
        self.agent_id = agent_id
        self.channel = channel
        self.account_id = account_id
        self.session_key = session_key
        self.matched_by = matched_by


def resolve_agent_route(
    cfg: Config,
    channel: str,
    account_id: Optional[str] = None,
    peer: Optional[RoutePeer] = None,
) -> ResolvedRoute:
    account_id = account_id or "default"

    for binding in cfg.bindings:
        if _matches_binding(binding, channel, account_id, peer):
            session_key = _build_session_key(
                binding.agent_id, channel, account_id, peer
            )
            return ResolvedRoute(
                agent_id=binding.agent_id,
                channel=channel,
                account_id=account_id,
                session_key=session_key,
                matched_by="binding",
            )

    session_key = _build_session_key(
        cfg.default_agent_id, channel, account_id, peer
    )
    return ResolvedRoute(
        agent_id=cfg.default_agent_id,
        channel=channel,
        account_id=account_id,
        session_key=session_key,
        matched_by="default",
    )


def _matches_binding(
    binding: BindingConfig,
    channel: str,
    account_id: str,
    peer: Optional[RoutePeer],
) -> bool:
    if binding.channel != "*" and binding.channel != channel:
        return False

    if binding.account_pattern != "*" and binding.account_pattern != account_id:
        return False

    if binding.peer:
        if not peer:
            return False
        if binding.peer.get("kind") != peer.kind:
            return False
        if binding.peer.get("id") != peer.id:
            return False

    return True


def _build_session_key(
    agent_id: str,
    channel: str,
    account_id: str,
    peer: Optional[RoutePeer],
) -> str:
    parts = [agent_id, channel, account_id]
    if peer:
        parts.extend([peer.kind, peer.id])
    return ":".join(parts).lower()
