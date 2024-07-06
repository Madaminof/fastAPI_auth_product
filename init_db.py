from database import Base, engine
from models import User, Product, Order  # import your models

Base.metadata.create_all(bind=engine)
