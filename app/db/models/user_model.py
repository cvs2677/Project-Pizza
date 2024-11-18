import enum
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum, Float, Table
from sqlalchemy.orm import relationship
from app.db.base import Base



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

    order = relationship("Order", back_populates="user")

    tokens = relationship("Token", back_populates="user")


# Token Models
class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    access_token = Column(String, unique=True, index=True, nullable=False)
    refresh_token = Column(String, unique=True, index=True, nullable=False)


    user = relationship("User", back_populates="tokens")

# Pizza Models

order_pizza_association = Table(
    "order_pizza_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("order.id"), primary_key=True),
    Column("pizza_id", Integer, ForeignKey("pizzas.id"), primary_key=True),
    Column("quantity", Integer, nullable=False)
)

class PizzaSize(enum.Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra-large"



class Pizza(Base):
    __tablename__ = 'pizzas'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    size = Column(Enum(PizzaSize), default=PizzaSize.SMALL)

    order = relationship(
        'Order',
        secondary=order_pizza_association,
        back_populates='pizzas')

# Order Models

class OrderStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('user.id'))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_price = Column(Float, default=0.0)

    user = relationship('User', back_populates='order')

    pizzas = relationship(
            'Pizza',
            secondary=order_pizza_association,
            back_populates='order'
        )











