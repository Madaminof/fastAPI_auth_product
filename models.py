from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users1'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(Text)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    orders = relationship("Order", back_populates='user')

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class Product(Base):
    __tablename__ = 'products1'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    price = Column(Integer)
    orders = relationship("Order", back_populates='product')

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"

class Order(Base):
    __tablename__ = 'orders1'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users1.id'))
    product_id = Column(Integer, ForeignKey('products1.id'))
    status = Column(String(20), default='PENDING')
    user = relationship("User", back_populates='orders')
    product = relationship("Product", back_populates='orders')
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Order(user_id='{self.user_id}', product_id='{self.product_id}', status='{self.status}', quantity='{self.quantity}')>"
