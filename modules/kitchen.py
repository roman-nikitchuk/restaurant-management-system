from database.connection import get_session
from database.models import Order, OrderItem, MenuItem


def get_pending_orders():
    session = get_session()
    try:
        orders = session.query(Order).filter(
            Order.status == "pending"
        ).order_by(Order.created_at.asc()).all()
        return orders
    finally:
        session.close()


def get_in_progress_orders():
    session = get_session()
    try:
        orders = session.query(Order).filter(
            Order.status == "in_progress"
        ).order_by(Order.created_at.asc()).all()
        return orders
    finally:
        session.close()


def get_all_active_orders():
    session = get_session()
    try:
        orders = session.query(Order).filter(
            Order.status.in_(["pending", "in_progress"])
        ).order_by(Order.created_at.asc()).all()
        return orders
    finally:
        session.close()


def get_order_details(order_id):
    session = get_session()
    try:
        items = (
            session.query(OrderItem, MenuItem)
            .join(MenuItem, OrderItem.menu_item_id == MenuItem.id)
            .filter(OrderItem.order_id == order_id)
            .all()
        )
        return items
    finally:
        session.close()


def update_order_status(order_id, new_status):
    session = get_session()
    try:
        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
            print("Błąd: zamówienie nie istnieje")
            return None

        allowed_statuses = ["pending", "in_progress", "ready", "completed"]
        if new_status not in allowed_statuses:
            print(f"Błąd: nieprawidłowy status")
            return None

        order.status = new_status
        session.commit()
        session.refresh(order)
        return order
    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()