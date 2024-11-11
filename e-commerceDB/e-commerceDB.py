from sqlalchemy import (
    create_engine, Column, Integer, String, Float, ForeignKey, DateTime,
    func, desc
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.sql import and_, or_
from datetime import datetime

# Define the database and base class
engine = create_engine("sqlite:///:memory:")
Base = declarative_base()

# Models

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="user")
    
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category(name={self.name})>"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    
    def __repr__(self):
        return f"<Order(user_id={self.user_id}, created_at={self.created_at})>"

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"

# Create all tables
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# Add sample data
category1 = Category(name="Electronics")
category2 = Category(name="Books")

product1 = Product(name="Laptop", price=1200.0, category=category1)
product2 = Product(name="Headphones", price=200.0, category=category1)
product3 = Product(name="Novel", price=20.0, category=category2)

user1 = User(name="Alice", email="alice@example.com")
user2 = User(name="Bob", email="bob@example.com")

order1 = Order(user=user1)
order2 = Order(user=user1)
order3 = Order(user=user2)

order_item1 = OrderItem(order=order1, product=product1, quantity=1)
order_item2 = OrderItem(order=order1, product=product2, quantity=2)
order_item3 = OrderItem(order=order2, product=product3, quantity=1)
order_item4 = OrderItem(order=order3, product=product2, quantity=1)

session.add_all([category1, category2, product1, product2, product3, user1, user2, order1, order2, order3, order_item1, order_item2, order_item3, order_item4])
session.commit()

# Queries
print("Created Tables, Schema, And added sample data!")

print("-"*60)
print("1. Join and filter: List all orders with user names and product details")
for order in session.query(Order).join(User).join(OrderItem).join(Product).all():
    print(f"Order ID: {order.id}, User: {order.user.name}, Items: {[item.product.name for item in order.order_items]}")

print("-"*60)
print("2. Sorting: Get all products sorted by price descending")
for product in session.query(Product).order_by(desc(Product.price)).all():
    print(product)

print("-"*60)
print("3. Aggregate functions: Find max, min, average price of products")
max_price = session.query(func.max(Product.price)).scalar()
min_price = session.query(func.min(Product.price)).scalar()
avg_price = session.query(func.avg(Product.price)).scalar()
print(f"Max Price: {max_price}, Min Price: {min_price}, Average Price: {avg_price}")

print("-"*60)
print("4. Grouping with HAVING: Find categories with more than one product")
for category in session.query(Category).join(Product).group_by(Category.id).having(func.count(Product.id) > 1).all():
    print(f"Category: {category.name}, Product Count: {len(category.products)}")

print("-"*60)
print("5. Complex filtering: Find orders placed by Alice with more than one item")
for order in session.query(Order).join(User).filter(User.name == "Alice").join(OrderItem).group_by(Order.id).having(func.count(OrderItem.id) > 1).all():
    print(f"Order ID: {order.id}, User: {order.user.name}")

print("-"*60)
print("6. Multi-table query: Total quantity of each product ordered")
for product, total_quantity in session.query(Product, func.sum(OrderItem.quantity)).join(OrderItem).group_by(Product.id).all():
    print(f"Product: {product.name}, Total Quantity Ordered: {total_quantity}")

print("-"*60)
print('7. Filtering with OR conditions: Find users who placed orders in the last day or have an email starting with "bob"')
yesterday = datetime.now()
recent_or_bob = session.query(User).join(Order, isouter=True).filter(or_(User.email.like("bob%"), Order.created_at >= yesterday)).all()
print(recent_or_bob)
