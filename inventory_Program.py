print("Assignment: HW9")

import sqlite3
from enum import Enum

class Inv_Col(Enum):
    INVENTORY_ID = 0
    PART_ID = 1

class Part_Col(Enum):
    PART_ID = 0
    PART_NAME = 1


class DBbase:
    _conn = None
    _cursor = None

    def __init__(self, db_name):
        self._db_name = db_name
        self.connect()

    def connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()

    def execute_script(self, sql_string):
        self._cursor.executescript(sql_string)

    @property
    def get_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn

    def close_db(self):
        self._conn.close()

    def reset_database(self):
        raise NotImplementedError()

class Parts(DBbase):

    def __init__(self):
        super().__init__("inventoryDB.sqlite")

    def update(self, part_id, name):
        try:
            super().connect()
            super().get_cursor.execute("""update Parts set name = ? where id = ?;""", (name, part_id,))
            super().get_connection.commit()
            super().close_db()
            print("updated part successfully.")
        except Exception as e:
            print("An error occurred.", e)

    def add(self, name):
        try:
            super().connect()
            super().get_cursor.execute("""insert or ignore into Parts (name) values (?);""", (name,))
            super().get_connection.commit()
            super().close_db()
            print("added part successfully")
        except Exception as e:
            print("An error occurred.", e)

    def delete(self, part_id):
        # delete from Parts where id = 3
        try:
            super().connect()
            super().get_cursor.execute("""delete from Parts where id = ?;""", (part_id,))
            super().get_connection.commit()
            super().close_db()
            print("deleted part successfully.")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False


    def fetch(self, id=None, part_name=None):
        # if id is null or None, then get everything, else get by id.
        try:
            super().connect()
            if id is not None:
                return super().get_cursor.execute("""SELECT * FROM Parts WHERE id = ?;""", (id,)).fetchone()
            elif part_name is not None:
                return super().get_cursor.execute("""SELECT * FROM Parts WHERE name = ?;""", (part_name,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Parts;""").fetchall()
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def reset_database(self):
        sql = """
              DROP TABLE IF EXISTS Parts:
                  Create TABLE Parts (
                      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                      name TEXT UNIQUE
                      );
              """
        super().execute_script(sql)
#
# parts = Parts()
# results = parts.fetch()
# print(results)


class Inventory(Parts):

    def add(self, name, qty, current_price):
        try:
            super().add(name)
        except Exception as e:
            print("An error occurred in the parts class.", e)
        else:
            try:
                # get part Id from parts table
                p_id = super().fetch(part_name=name)
                if p_id is not None:
                    super().connect()
                    super().get_cursor.execute(
                        """insert into Inventory (part_id, quantity, current_price)
                    values (?,?,?);""", (p_id[Part_Col.PART_ID.value], qty, current_price))
                    super().get_connection.commit()
                    super().close_db()
                    print("added inventory successfully.")
                else:
                    raise Exception("An id of the part name was not found")
            except Exception as e:
                print("An error occurred in the inventory class.", e)

    def update(self, id, qty, price):
        try:
            super().connect()
            super().get_cursor.execute("""update Inventory set quantity = ?, current_price = ? where id = ?;
            """, (qty, price, id,))
            super().get_connection.commit()
            super().close_db()
            print("updated Inventory successfully.")
            return True
        except Exception as e:
            print("An error occurred.", e)
            return False

    def delete(self, inventory_id):
        part_id = -1
        try:
            # retrieve part id based from the inventory Id.
            rval = self.fetch(inventory_id)
            if rval is not None:
                # set the part Id and delete from Parts.
                part_id = rval[Inv_Col.PART_ID.value]
                rsts = super().delete(part_id)
                if rsts is False:
                    raise Exception("Delete method inside Parts failed. Delete aborted.")
        except Exception as e:
            print("An error occurred when fetching from parts.", e)
        else:
            try:
                super().connect()
                super().get_cursor.execute("""delete from Inventory where id = ?;""", (inventory_id,))
                super().get_connection.commit()
                super().close_db()
                print("deleted inventory successfully.")
            except Exception as e:
                print("An error occurred.", e)

    def fetch(self, id=None):
        # if id is null or None, then get everything, else get by id.
        try:
            super().connect()
            if id is not None:
                rval =  super().get_cursor.execute("""SELECT Inventory.id part_id, p.name, quantity, current_price
                                                  FROM Inventory join Parts p on Inventory.part_id = p.id
                                                  where Inventory.id = ?;""", (id,)).fetchone()
                return rval
            else:
                return super().get_cursor.execute("""SELECT Inventory.id, p.name, quantity, current_price FROM Inventory
                                                  join Parts p on Inventory.part_id = p.id;""").fetchall()
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def reset_database(self):
        sql = """
              DROP TABLE IF EXISTS Inventory:
              Create TABLE Inventory (
                  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  part_id INTEGER NOT NULL,
                  quantity INTEGER NOT NULL,
                  current_price varchar(20)
                  );
              """
        super().execute_script(sql)

inv_options = {"get": "Get all inventory",
               "getby": "Get inventory by Id",
               "update": "Update inventory",
               "add": "Add inventory",
               "delete": "delete inventory",
               "exit": "exit the program"}

user_selection = ""
while user_selection != "exit":
    print("*** Option List ***")
    for option in inv_options.items():
        print(option)

    user_selection = input("Select an option: ")
    inventory = Inventory()

    if user_selection == "get":
        my_inventory = inventory.fetch()
        for item in my_inventory:
            print(item)
        print("Done\n")

    elif user_selection == "getby":
        inv_id = input("Enter inventory Id:")
        my_inventory = inventory.fetch(inv_id)
        print(my_inventory)
        print("\n")

    elif user_selection == "update":
        inv_id = input("Enter inventory Id: ")
        qty = input("Enter quantity amount: ")
        price = input("Enter selling price: ")
        inventory.update(inv_id, qty, price)
        print(inventory.fetch(inv_id))
        print("Done\n")

    elif user_selection == "add":
        name = input("Enter part name: ")
        qty = input("Enter quantity amount: ")
        price = input("Enter selling price: ")
        inventory.add(name, qty, price)
        print("Done\n")

    elif user_selection == "delete":
        inv_id = input("Enter inventory Id: ")
        inventory.delete(inv_id)
        print("Done\n")

    else:
        if user_selection != "exit":
            print("Invalid selection, try again\n")

# parts = Parts()
# parts.add("Coke")

# inventory = Inventory()
# # inventory.delete(8)
# # inventory.add("Ice Cream", 40, "4.99")
# inventory_results = inventory.fetch(4)
# print(len(inventory_results))
# print(inventory_results)
