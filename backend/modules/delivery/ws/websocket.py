from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

active_connections: Dict[str, list] = {}

async def websocket_endpoint(websocket: WebSocket, uuid: str):
    await websocket.accept()
    if uuid not in active_connections:
        active_connections[uuid] = []
    active_connections[uuid].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            for conn in active_connections[uuid]:
                if conn != websocket:
                    await conn.send_json(data)
    except WebSocketDisconnect:
        active_connections[uuid].remove(websocket)