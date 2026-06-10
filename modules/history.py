from database.connection import get_session
from database.models import Order, OrderItem, MenuItem, Bill


def get_completed_orders():
    session = get_session()
    try:
        orders = session.query(Order).filter(
            Order.status == "completed"
        ).order_by(Order.created_at.desc()).all()
        return orders
    finally:
        session.close()


def get_order_history_details(order_id):
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


def get_daily_summary():
    session = get_session()
    try:
        from sqlalchemy import func, cast, Date
        from datetime import date

        bills = (
            session.query(Bill)
            .filter(
                Bill.pay_status == "paid",
                cast(Bill.created_at, Date) == date.today()
            )
            .all()
        )

        total_revenue = sum(bill.total_amount for bill in bills)
        total_orders = len(bills)

        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue
        }
    finally:
        session.close()


def get_revenue_by_period(date_from, date_to):
    session = get_session()
    try:
        from sqlalchemy import cast, Date

        bills = (
            session.query(Bill)
            .filter(
                Bill.pay_status == "paid",
                cast(Bill.created_at, Date) >= date_from,
                cast(Bill.created_at, Date) <= date_to
            )
            .all()
        )

        total = sum(bill.total_amount for bill in bills)
        return {
            "total_orders": len(bills),
            "total_revenue": total,
            "date_from": date_from,
            "date_to": date_to
        }
    finally:
        session.close()
