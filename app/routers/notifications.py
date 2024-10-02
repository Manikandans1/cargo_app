# app/notifications.py

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from .. import schemas, database, models

router = APIRouter(tags=['Notification'])
get_db = database.get_db
connected_clients = {}

@router.websocket("/ws/{customer_id}")
async def websocket_endpoint(websocket: WebSocket, customer_id: str):
    await websocket.accept()
    connected_clients[customer_id] = websocket
    try:
        while True:
            await websocket.receive_text() 
    except WebSocketDisconnect:
        del connected_clients[customer_id]

async def notify_customer(customer_id: str, message: str):
    if customer_id in connected_clients:
        await connected_clients[customer_id].send_text(message)

@router.put("/orders/liveupdate/{tracking_id}", status_code=202)
async def live_track_update(tracking_id: str, orders: schemas.LiveUpdate, db: Session = Depends(get_db)):
    live_update = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == tracking_id).first()

    if not live_update:
        raise HTTPException(status_code=404, detail=f"Tracking ID {tracking_id} not found")

    # Prepare a list to collect messages for notification
    messages = []

    # Update fields only if new values are provided and send notifications for updates
    if orders.order_confirmed is not None and orders.order_confirmed != live_update.order_confirmed:
        live_update.order_confirmed = orders.order_confirmed
        messages.append("Your order has been confirmed." if orders.order_confirmed else "Your order confirmation has been canceled.")

    if orders.package_pickup is not None and orders.package_pickup != live_update.package_pickup:
        live_update.package_pickup = orders.package_pickup
        messages.append("Your package has been picked up." if orders.package_pickup else "Your package pickup has been canceled.")

    if orders.move_to is not None and orders.move_to != live_update.move_to:
        live_update.move_to = orders.move_to
        messages.append(f"Your package is moving to {orders.move_to}.")

    if orders.clear_custom is not None and orders.clear_custom != live_update.clear_custom:
        live_update.clear_custom = orders.clear_custom
        messages.append("Your package has cleared customs." if orders.clear_custom else "Your package is held up in customs.")

    if orders.ready_to_delivery is not None and orders.ready_to_delivery != live_update.ready_to_delivery:
        live_update.ready_to_delivery = orders.ready_to_delivery
        messages.append("Your package is ready for delivery." if orders.ready_to_delivery else "Your package is not ready for delivery yet.")

    if orders.package_delivered is not None and orders.package_delivered != live_update.package_delivered:
        live_update.package_delivered = orders.package_delivered
        messages.append("Your package has been delivered." if orders.package_delivered else "Your package delivery was unsuccessful.")

    db.commit()

    db.refresh(live_update)

    # Notify customer via WebSocket with all relevant messages
    customer_id = str(tracking_id) 
    if messages:
        await notify_customer(customer_id, "\n".join(messages))

    return {"detail": "Update successful"}
