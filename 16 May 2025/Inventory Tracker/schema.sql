CREATE TABLE IF NOT EXISTS PRODUCTS (
    p_id INTEGER PRIMARY KEY AUTOINCREMENT,
    p_name TEXT NOT NULL,
    price REAL,
    category TEXT 
);

CREATE TABLE IF NOT EXISTS WAREHOUSES (
    w_id INTEGER PRIMARY KEY AUTOINCREMENT,
    w_name TEXT,
    w_location TEXT,
    capacity TEXT,
    contact_no TEXT
);

CREATE TABLE IF NOT EXISTS INVENTORY (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    p_id int,
    w_id int,
    quantity int default 0,
    last_updated TIMESTAMP default CURRENT_TIMESTAMP,

    FOREIGN KEY (p_id) REFERENCES PRODUCTS (p_id),
    FOREIGN KEY (w_id) REFERENCES WAREHOUSES (w_id)
    UNIQUE (p_id, w_id)
);

CREATE TABLE IF NOT EXISTS TRANSCATIONS (
    transcation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    p_id int,
    w_id int,
    quantity int not null,
    transcation_type TEXT CHECK(transcation_type IN ('sale', 'purchase')) NOT NULL,
    transcation_date TIMESTAMP default CURRENT_TIMESTAMP,
   
    FOREIGN KEY (p_id) REFERENCES PRODUCTS (p_id),
    FOREIGN KEY (w_id) REFERENCES WAREHOUSES (w_id)
);
