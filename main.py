from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def index():
    return {'data':{'name':'Mani'}}

@app.get('/orders/{id}')
def orders(id: int):
    return {'data': id}

class Create_Order(BaseModel):
    coustmer_name: str
    pickup_location: str
    delivery_location: str
   # description: str | None = None
   # price: float
   # tax: float | None = None





@app.post('/orders/')
def create_orders(orders: Create_Order):
    return orders
    #return {'data':'New Coustemer'}