import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ItemInvSqlite import DataInventoryDB
from tkinter import *


class DataInventoryGUI(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title('ShenZend Cargo Inventory System')
        self.geometry('1300x500')
        self.create_widgets()
        # Set the background color of the main window
        self.configure(bg="#004242")

    def create_widgets(self):
        # Labels and Entry Widgets
        label_name = tk.Label(self, text='Item:')
        label_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        label_category = tk.Label(self, text='Category:')
        label_category.grid(row=1, column=0, padx=10, pady=10)

        self.category_options = ['Fragile', 'Normal', 'Heavy Duty']
        self.entry_category = ttk.Combobox(self, values=self.category_options, state ='readonly')
        self.entry_category.grid(row=1, column=1, padx=10, pady=10)
        


        label_quantity = tk.Label(self, text='Quantity:')
        label_quantity.grid(row=2, column=0, padx=10, pady=10)
        self.entry_quantity = tk.Entry(self, validate='key', validatecommand=(
            self.register(self.validate_int), '%P'))
        self.entry_quantity.grid(row=2, column=1, padx=10, pady=10)

        label_price = tk.Label(self, text='Price:')
        label_price.grid(row=3, column=0, padx=10, pady=10)
        self.entry_price = tk.Entry(self, validate='key', validatecommand=(
            self.register(self.validate_float), '%P'))
        self.entry_price.grid(row=3, column=1, padx=10, pady=10)

        

        # Buttons
        add_button = tk.Button(self, text='Add Entry', command=self.add_entry)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        update_button = tk.Button(
            self, text='Update Entry', command=self.update_entry)
        update_button.grid(row=5, column=0, columnspan=2, pady=10)

        delete_button = tk.Button(
            self, text='Delete Entry', command=self.delete_entry)
        delete_button.grid(row=6, column=0, columnspan=2, pady=10)

        export_csv_button = tk.Button(
            self, text='Export to CSV', command=self.export_to_csv)
        export_csv_button.grid(row=7, column=0, columnspan=2, pady=10)

        import_csv_button = tk.Button(
            self, text='Import from CSV', command=self.import_from_csv)
        import_csv_button.grid(row=8, column=0, columnspan=2, pady=10)

        export_json_button = tk.Button(
            self, text='Export to JSON', command=self.export_to_json)
        export_json_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Treeview for Tabular View
        columns = ('ID', 'Item', 'Category', 'Quantity', 'Price')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=2, rowspan=10,
                       padx=10, pady=10, sticky='nsew')
        self.tree.bind('<ButtonRelease>', self.read_display_data)
        self.refresh_table()

    def validate_int(self, new_value):
        try:
            if new_value:
                int(new_value)
            return True
        except ValueError:
            messagebox.showerror(
                'Error', 'Invalid Input in the "Quantity" field.')
            return False
        
    def validate_float(self, new_value):
        try:
            if new_value:
                float(new_value)
            return True
        except ValueError:
            messagebox.showerror(
                'Error', 'Inavalid Input in the  "Price" field.')
            return False

    def add_entry(self):
        name = self.entry_name.get()
        category = self.entry_category.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        if not (name and category and quantity and price):
            messagebox.showerror('Error', 'Enter all fields.')
        else:
            self.db.insert_entry(name, category, quantity, price)
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def update_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an entry to update')
        else:
            entry_id = self.tree.item(selected_item, 'values')[0]  # Fix here
            name = self.entry_name.get()
            category = self.entry_category.get()
            quantity = self.entry_quantity.get()
            price = self.entry_price.get()
            self.db.update_entry(name, category, quantity, price, entry_id)
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')




    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an entry to delete')
        else:
            entry_id = self.tree.item(selected_item, 'values')[0]  # Fix here
            self.db.delete_entry(entry_id)
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def read_display_data(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            entry = self.tree.item(selected_item)['values']
            self.clear_form()
            self.entry_name.insert(0, entry[1])
            self.entry_category.insert(0, entry[2])
            self.entry_quantity.insert(0, entry[3])
            self.entry_price.insert(0, entry[4])

    def refresh_table(self):
        entries = self.db.fetch_entries()
        self.tree.delete(*self.tree.get_children())
        for entry in entries:
            self.tree.insert('', 'end', values=entry)

    def clear_form(self):
        self.entry_name.delete(0, 'end')
        self.entry_category.delete(0, 'end')
        self.entry_quantity.delete(0, 'end')
        self.entry_price.delete(0, 'end')

    def export_to_csv(self):
        csv_filename = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if csv_filename:
            self.db.export_csv(csv_filename)
            messagebox.showinfo('Success', f'Data exported to {csv_filename}')

    def import_from_csv(self):
        csv_filename = filedialog.askopenfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if csv_filename:
            self.db.import_csv(csv_filename)
            self.refresh_table()
            messagebox.showinfo(
                'Success', f'Data imported from {csv_filename}')

    def export_to_json(self):
        json_filename = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if json_filename:
            self.db.export_json(json_filename)
            messagebox.showinfo('Success', f'Data exported to {json_filename}')



