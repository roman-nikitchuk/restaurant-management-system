from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    Numeric, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    employees = relationship("Employee", back_populates="role")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="employees")
    orders = relationship("Order", back_populates="employee")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    menu_items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)

    category = relationship("Category", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String(20), default="free")

    orders = relationship("Order", back_populates="table")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey("restaurant_tables.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    guest_count = Column(Integer)
    notes = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    table = relationship("RestaurantTable", back_populates="orders")
    employee = relationship("Employee", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    bill = relationship("Bill", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    pay_method = Column(String(20))
    pay_status = Column(String(20), default="unpaid")
    created_at = Column(DateTime, default=func.now())

    order = relationship("Order", back_populates="bill")