from database.connection import get_session
from database.models import Order, OrderItem, MenuItem, RestaurantTable


def get_available_tables():
    session = get_session()
    try:
        tables = session.query(RestaurantTable).filter(
            RestaurantTable.status == "free"
        ).all()
        return tables
    finally:
        session.close()


def create_order(table_id, employee_id, guest_count, notes=""):
    session = get_session()
    try:
        table = session.query(RestaurantTable).filter(
            RestaurantTable.id == table_id
        ).first()
        if not table:
            print("Błąd: stolik nie istnieje")
            return None

        table.status = "occupied"

        order = Order(
            table_id=table_id,
            employee_id=employee_id,
            guest_count=guest_count,
            notes=notes,
            status="pending"
        )
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()


def add_item_to_order(order_id, menu_item_id, quantity):
    session = get_session()
    try:
        if quantity <= 0:
            print("Błąd: ilość musi być większa od 0")
            return None

        menu_item = session.query(MenuItem).filter(
            MenuItem.id == menu_item_id
        ).first()
        if not menu_item:
            print("Błąd: pozycja menu nie istnieje")
            return None

        order_item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            unit_price=menu_item.price
        )
        session.add(order_item)
        session.commit()
        return order_item
    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()


def get_order_items(order_id):
    session = get_session()
    try:
        items = session.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()
        return items
    finally:
        session.close()


def cancel_order(order_id):
    session = get_session()
    try:
        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
            print("Błąd: zamówienie nie istnieje")
            return None

        table = session.query(RestaurantTable).filter(
            RestaurantTable.id == order.table_id
        ).first()
        if table:
            table.status = "free"

        order.status = "cancelled"
        session.commit()
        return order
    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()


def get_active_orders():
    session = get_session()
    try:
        orders = session.query(Order).filter(
            Order.status.in_(["pending", "in_progress"])
        ).all()
        return orders
    finally:
        session.close()