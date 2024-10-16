from data.menu_db import MenuDatabase

def populate_menu():
    db = MenuDatabase()
    
    # Add some sample menu items
    db.add_item("Cheeseburger", "Classic beef patty with cheese", 5.99, "Main")
    db.add_item("Fries", "Crispy golden fries", 2.99, "Side")
    db.add_item("Soda", "Refreshing carbonated drink", 1.99, "Drink")
    db.add_item("Chicken Sandwich", "Grilled chicken breast with lettuce and mayo", 6.99, "Main")
    db.add_item("Salad", "Fresh mixed greens with choice of dressing", 4.99, "Side")
    
    print("Database populated with sample menu items.")

if __name__ == "__main__":
    populate_menu()

