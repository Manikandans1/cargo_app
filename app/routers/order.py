from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..respository import order


router = APIRouter(
    tags=['Orders']
)
get_db = database.get_db



@router.get('/orders/', response_model=List[schemas.Show_Create_Order])
def view_all_orders(db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.get_all(db)


#NEW ORDER CREATE
@router.post('/orders/', status_code=status.HTTP_201_CREATED)
def create_orders(orders: schemas.Create_Order, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.create_orders(orders, db)
 

#DELETE
@router.delete('/orders/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.destroy(id,db)


#UPDATE
@router.put('/orders/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int, orders: schemas.Create_Order, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.update(id,orders,db)




#ORDER UNIQUE ID TO GET DEATILS
@router.get('/orders/{id}',status_code=200,response_model=schemas.Show_Create_Order)
def track_id(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.track_id(id,db)


#----------NOTIFICATION-----------
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# A manager to handle active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)



@app.post("/order/book")
async def book_order(order_data: dict):
    # Your logic for booking an order
    # Notify the client
    await manager.send_message("New order booked successfully.")
    return {"message": "Order booked."}

@app.post("/payment/confirm")
async def confirm_payment(payment_data: dict):
    # Your logic for confirming payment
    # Notify the client
    await manager.send_message("Payment confirmed.")
    return {"message": "Payment confirmed."}
