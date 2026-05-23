from database.connection import get_session
from database.models import Role, Employee, Category, MenuItem, RestaurantTable


def seed_data():
    session = get_session()

    try:
        waiter = Role(name="Kelner")
        cook = Role(name="Kucharz")
        manager = Role(name="Menedżer")
        session.add_all([waiter, cook, manager])
        session.flush()

        session.add_all([
            Employee(name="Roman", role_id=waiter.id),
            Employee(name="Natalia", role_id=waiter.id),
            Employee(name="Jan", role_id=cook.id),
            Employee(name="Anna", role_id=manager.id),
        ])

        starters = Category(name="Przystawki")
        soups = Category(name="Zupy")
        mains = Category(name="Dania główne")
        desserts = Category(name="Desery")
        drinks = Category(name="Napoje")
        session.add_all([starters, soups, mains, desserts, drinks])
        session.flush()

        session.add_all([
            MenuItem(name="Bruschetta", category_id=starters.id, price=89.00, description="Z pomidorami i bazylią"),
            MenuItem(name="Sałatka Cezar", category_id=starters.id, price=129.00, description="Z kurczakiem i parmezanem"),
            MenuItem(name="Barszcz", category_id=soups.id, price=95.00, description="Tradycyjny barszcz ukraiński"),
            MenuItem(name="Zupa krem z grzybów", category_id=soups.id, price=110.00, description="Ze śmietaną"),
            MenuItem(name="Stek", category_id=mains.id, price=350.00, description="Wołowina średnio wysmażona"),
            MenuItem(name="Makaron Carbonara", category_id=mains.id, price=185.00, description="Z boczkiem i parmezanem"),
            MenuItem(name="Tiramisu", category_id=desserts.id, price=95.00, description="Klasyczny włoski deser"),
            MenuItem(name="Sernik", category_id=desserts.id, price=89.00, description="Z sosem jagodowym"),
            MenuItem(name="Americano", category_id=drinks.id, price=55.00, description="Podwójne espresso"),
            MenuItem(name="Świeżo wyciskany sok", category_id=drinks.id, price=75.00, description="Pomarańczowy lub jabłkowy"),
        ])

        session.add_all([
            RestaurantTable(number=1, capacity=2, status="free"),
            RestaurantTable(number=2, capacity=4, status="free"),
            RestaurantTable(number=3, capacity=4, status="free"),
            RestaurantTable(number=4, capacity=6, status="free"),
            RestaurantTable(number=5, capacity=8, status="free"),
        ])

        session.commit()
        print("Dane testowe dodane pomyślnie!")

    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()