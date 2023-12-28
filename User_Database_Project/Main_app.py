from ItemInvSqlite import DataInventoryDB
from ItemInvGui import DataInventoryGUI

if __name__ == "__main__":
    db = DataInventoryDB()
    app = DataInventoryGUI(db)
    app.mainloop()
