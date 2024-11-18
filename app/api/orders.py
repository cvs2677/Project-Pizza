from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.models.user_model import Pizza, OrderStatus, Order, order_pizza_association, User
from app.db.session import get_db
from app.dependencies import get_current_user
from app.schemas.order import PizzaCreate, OrderCreate, OrderUpdate

router = APIRouter(
    prefix="/order",
    tags=["orders"]
)

# create pizza's api points
@router.post("/create_pizza")
async def create_pizza(pizza: PizzaCreate, user: Session= Depends(get_current_user), db:Session= Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_pizza = Pizza(name = pizza.name, price = pizza.price, size = pizza.size)
    db.add(new_pizza)
    db.commit()
    db.refresh(new_pizza)
    return new_pizza

@router.get("/get_pizzas")
async def get_pizzas(db: Session= Depends(get_db)):
    pizzas = db.query(Pizza).all()
    return pizzas

@router.post("/get_pizzas/{pizza_id}")
async def get_pizza_by_id(pizza_id: int, db: Session= Depends(get_db)):
    pizza =  db.query(Pizza).filter(pizza_id == Pizza.id).first()
    return pizza


# Create a Order
@router.post("/create_order")
async def create_order(order: OrderCreate, user: Session= Depends(get_current_user), db: Session= Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_order = Order(customer_id = order.customer_id, status = OrderStatus.PENDING)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    total_price = 0.0

    # adding pizzas to the order and calculate total_price

    for pizza_order in order.pizzas:
        pizza = db.query(Pizza).filter(Pizza.id == pizza_order.pizza_id).first()

        if not pizza:
            raise HTTPException(status_code=404, detail='Pizza not found.')

        total_price += pizza.price * pizza_order.quantity

        db.execute(order_pizza_association.insert().values(
            order_id = new_order.id,
            pizza_id = pizza_order.pizza_id,
            quantity = pizza_order.quantity
        ))

    new_order.total_price = total_price
    db.commit()

    return {
        'order_id': new_order.id,
        'status': new_order.status,
        'total_price': new_order.total_price,
    }


# Get Order by order_ID
@router.get("/get_order/{order_id}")
async def get_order_by_id(order_id: int, db: Session= Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found.')

    return order
    #     'order_id': order.id,
    #     'status': order.status,
    #     'total_price': order.total_price,
    #     'pizzas': [
    #         {
    #             "pizza_id": pizza.id,
    #             "name": pizza.name,
    #             "quantity": association.quantity
    #         }
    #         for pizza, association in db.execute(
    #             order_pizza_association.select().where(
    #                 order_pizza_association.c.order_id == order.id
    #             )
    #         ).join(Pizza).filter(Pizza.id == order_pizza_association.c.pizza_id)
    #     ]
    # }




# get order by user.id
@router.get("/get_orders_by_user/{user_id}")
async def get_orders_by_user_id(user_id: int, db: Session= Depends(get_db)):
    orders = db.query(Order).filter(Order.customer_id == user_id).all()
    return orders

# get order by username
@router.get("/get_orders_by_username/{username}")
async def get_orders_by_username(username: str, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found.')

    orders = db.query(Order).filter(Order.customer_id == user.id).all()
    return orders


# Update an order
@router.put('/update_order/{order_id}')
async def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    # fetching the existing user
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found.')

    if order_update.status:
       try:
           order.status = OrderStatus(order_update.status)
       except ValueError:
           raise HTTPException(status_code=400, detail='Invalid status.')

    # Update Pizza and quantity
    if order_update.pizzas:
        db.execute(order_pizza_association.delete().where(order_pizza_association.c.order_id == order.id))

        total_price = 0.0
        for pizza_order in order_update.pizzas:
            pizza =  db.query(Pizza).filter(Pizza.id == pizza_order.pizza_id).first()
            if not pizza:
                raise HTTPException(status_code=404, detail='Pizza not found.')

            total_price += pizza.price * pizza_order.quantity

            db.execute(order_pizza_association.insert().values(
                order_id = order.id,
                pizza_id = pizza_order.pizza_id,
                quantity = pizza_order.quantity
            ))

        order.total_price = total_price

    db.commit()
    db.refresh(order)
    return {
        'order_id': order.id,
       'status': order.status,
        'total_price': order.total_price,
    }

# Delete an order
@router.delete("/delete_order/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found.')

    db.delete(order)
    db.commit()
    return {'detail': 'Order deleted'}







