from database.connection import get_session
from database.models import Category, MenuItem


def get_all_categories():
    session = get_session()
    try:
        categories = session.query(Category).all()
        return categories
    finally:
        session.close()


def get_menu_by_category(category_id):
    session = get_session()
    try:
        items = session.query(MenuItem).filter(
            MenuItem.category_id == category_id,
            MenuItem.is_available == True
        ).all()
        return items
    finally:
        session.close()


def get_all_menu_items():
    session = get_session()
    try:
        items = session.query(MenuItem).filter(
            MenuItem.is_available == True
        ).all()
        return items
    finally:
        session.close()


def search_menu_items(query):
    session = get_session()
    try:
        items = session.query(MenuItem).filter(
            MenuItem.name.ilike(f"%{query}%"),
            MenuItem.is_available == True
        ).all()
        return items
    finally:
        session.close()


def toggle_item_availability(item_id):
    session = get_session()
    try:
        item = session.query(MenuItem).filter(MenuItem.id == item_id).first()
        if item:
            item.is_available = not item.is_available
            session.commit()
            return item
    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()