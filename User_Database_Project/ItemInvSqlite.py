import sqlite3
import json
import csv


class DataInventoryDB:
    def __init__(self, dbName='DataInventory.db'):
        self.dbName = dbName
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        # Create a table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                quantity INTEGER,
                price REAL
            )''')
        self.conn.commit()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

    def commit_close(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                quantity INTEGER,
                price REAL
            )''')
        self.commit_close()

    def fetch_entries(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Inventory')
        entries = self.cursor.fetchall()
        self.conn.close()
        return entries

    def insert_entry(self, name, category, quantity, price):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Inventory (name, category, quantity, price) VALUES (?, ?, ?, ?)',
                            ( name, category, quantity, price))
        self.commit_close()

    def delete_entry(self, entry_id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Inventory WHERE id = ?', (entry_id,))
        self.commit_close()

    def update_entry(self, new_name, new_category, new_quantity, new_price, entry_id):
        self.connect_cursor()
        self.cursor.execute('''
            UPDATE Inventory
            SET name = ?, category = ?, quantity = ?, price = ?
            WHERE id = ?''', (new_name, new_category, new_quantity, new_price, entry_id))
        self.commit_close()

    def id_exists(self, entry_id):
        self.connect_cursor()
        self.cursor.execute(
            'SELECT COUNT(*) FROM Inventory WHERE id = ?', (entry_id,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self, csv_filename='Inventory.csv'):
        entries = self.fetch_entries()
        with open(csv_filename, "w") as filehandle:
            for entry in entries:
                filehandle.write(
                    f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

    def import_csv(self, filename):
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            data = [tuple(row[1:]) for row in csv_reader]

        self.connect_cursor()

        try:
            self.cursor.executemany('''
            INSERT INTO Inventory (name, category, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', data)
            self.commit_close()
        except sqlite3.Error as e:
            print("Error importing CSV:", e)

    def export_json(self, json_filename='Inventory.json'):
        entries = self.fetch_entries()
        data = [{'id': entry[0], 'name': entry[1], 'category': entry[2], 'quantity': entry[3], 'price': entry[4]}
                for entry in entries]

        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)
