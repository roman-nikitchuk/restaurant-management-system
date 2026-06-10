from database.connection import get_session
from database.models import Bill, Order, OrderItem, RestaurantTable


def calculate_total(order_id):
    session = get_session()
    try:
        items = session.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()
        total = sum(item.unit_price * item.quantity for item in items)
        return total
    finally:
        session.close()


def create_bill(order_id, pay_method):
    session = get_session()
    try:
        existing = session.query(Bill).filter(
            Bill.order_id == order_id
        ).first()
        if existing:
            print("Błąd: rachunek już istnieje")
            return None

        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
            print("Błąd: zamówienie nie istnieje")
            return None

        total = calculate_total(order_id)

        bill = Bill(
            order_id=order_id,
            total_amount=total,
            pay_method=pay_method,
            pay_status="unpaid"
        )
        session.add(bill)
        session.commit()
        session.refresh(bill)
        return bill
    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()


def pay_bill(bill_id):
    session = get_session()
    try:
        bill = session.query(Bill).filter(Bill.id == bill_id).first()
        if not bill:
            print("Błąd: rachunek nie istnieje")
            return None

        if bill.pay_status == "paid":
            print("Błąd: rachunek już opłacony")
            return None

        bill.pay_status = "paid"

        order = session.query(Order).filter(
            Order.id == bill.order_id
        ).first()
        if order:
            order.status = "completed"
            table = session.query(RestaurantTable).filter(
                RestaurantTable.id == order.table_id
            ).first()
            if table:
                table.status = "free"

        session.commit()
        session.refresh(bill)
        return bill
    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()


def get_bill_by_order(order_id):
    session = get_session()
    try:
        bill = session.query(Bill).filter(
            Bill.order_id == order_id
        ).first()
        return bill
    finally:
        session.close()