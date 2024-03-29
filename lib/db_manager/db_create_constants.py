USER = """
    CREATE TABLE IF NOT EXISTS user(
            first TINYTEXT NOT NULL,
            last TINYTEXT NOT NULL,
            email PRIMARY KEY
    )
"""

CUSTOMER = """
    CREATE TABLE IF NOT EXISTS customer(
        email TINYTEXT PRIMARY KEY REFERENCES user(email),
        address TINYTEXT NOT NULL,
        phone_number CHAR(10) NOT NULL UNIQUE 
            CHECK(length(phone_number) == 10)
    )
"""

SELLER = """
    CREATE TABLE IF NOT EXISTS seller(
        email TINYTEXT PRIMARY KEY REFERENCES user(email),
        address TINYTEXT NOT NULL,
        phone_number CHAR(10) NOT NULL UNIQUE
            CHECK(length(phone_number) == 10)
    )
"""

EMPLOYEE = """
    CREATE TABLE IF NOT EXISTS employee(
        email TINYTEXT PRIMARY KEY REFERENCES user(email),
        role TINYTEXT NOT NULL
        CHECK(role IN ("EMPLOYEE", "ADMIN", "VIP", "MANAGER")),
        date_joined DATE NOT NULL,
        phone_number CHAR(10) NOT NULL UNIQUE 
            CHECK (length(phone_number) == 10)
    )
"""

LOGIN_INFO = """
    CREATE TABLE IF NOT EXISTS login_info(
        email TINYTEXT PRIMARY KEY,
        password CHAR(77) NOT NULL
            CHECK(length(password) == 77),
        role TINYTEXT NOT NULL
            CHECK(role IN ("SELLER", "ADMIN", "CUSTOMER", "DEVELOPER"))
 
    )
"""

ITEM = """
    CREATE TABLE IF NOT EXISTS item(
        seller_email TINYTEXT,
        item_id INTEGER
            CHECK(item_id > 0),
        quantity INTEGER DEFAULT 1 NOT NULL
            CHECK(quantity >= 0),
        price DOUBLE NOT NULL
            CHECK(price >= 0),
        name TINYTEXT NOT NULL,
        type TINYTEXT NOT NULL,
        PRIMARY KEY(seller_email, item_id),
        FOREIGN KEY(seller_email) REFERENCES seller(email)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
"""

ITEM_FREQUENCY = """
    CREATE TABLE IF NOT EXISTS item_frequency(
        seller_email TINYTEXT,
        item_id INTEGER,
        frequency INTEGER DEFAULT 1 NOT NULL,
        PRIMARY KEY(seller_email, item_id),
        FOREIGN KEY(seller_email, item_id) REFERENCES item(seller_email, item_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
"""

ITEMS_BOUGHT = """
    CREATE TABLE IF NOT EXISTS items_bought(
        seller_email TINYTEXT,
        item_id INTEGER,
        order_number INTEGER,
        price DOUBLE NOT NULL,
        name TINYTEXT NOT NULL,
        type TINYTEXT NOT NULL,
        number_of_items_bought INTEGER DEFAULT 0 NOT NULL
            CHECK(number_of_items_bought >= 0),
        PRIMARY KEY(seller_email, item_id, order_number),
        FOREIGN KEY(seller_email, item_id) REFERENCES item(seller_email, item_id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        FOREIGN KEY(order_number) REFERENCES orders(order_number)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    )
"""

ITEMS_IN_SHOPPING_CART = """
    CREATE TABLE IF NOT EXISTS items_in_shopping_cart(
        cart_id INTEGER,
        seller_email TINYTEXT,
        item_id INTEGER,
        number_of_items_bought INTEGER NOT NULL
            CHECK(number_of_items_bought >= 1),
        PRIMARY KEY(cart_id, seller_email, item_id),
        FOREIGN KEY(seller_email, item_id) REFERENCES item(seller_email, item_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(cart_id) REFERENCES shopping_cart(cart_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
"""

INVENTORY = """
    CREATE TABLE IF NOT EXISTS inventory(
        seller_email TINYTEXT,
        item_id INTEGER,
        PRIMARY KEY(seller_email, item_id),
        FOREIGN KEY(seller_email, item_id) REFERENCES item(seller_email, item_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
"""

SHOPPING_CART = """
    CREATE TABLE IF NOT EXISTS shopping_cart(
        cart_id INTEGER PRIMARY KEY
            CHECK(cart_id > 0),
        total_number_of_items INTEGER DEFAULT 0 NOT NULL
            CHECK(total_number_of_items >= 0),
        total_price DOUBLE DEFAULT 0 NOT NULL
            CHECK(total_price >= 0)
    )
"""

HAS_SHOPPING_CART = """
    CREATE TABLE IF NOT EXISTS has_shopping_cart(
        customer_email TINYTEXT NOT NULL,
        cart_id INTEGER PRIMARY KEY,
        FOREIGN KEY(customer_email) REFERENCES customer(email)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(cart_id) REFERENCES shopping_cart(cart_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
    )
"""

ORDERS = """
    CREATE TABLE IF NOT EXISTS orders(
        order_number INTEGER PRIMARY KEY,
        customer_email TINYTEXT NOT NULL,
        total_number_of_items INTEGER NOT NULL
            CHECK(total_number_of_items >= 1),
        date_ordered DATE NOT NULL,
        FOREIGN KEY(customer_email) REFERENCES customer(email)
            ON DELETE NO ACTION
            ON UPDATE CASCADE
    )
"""

ORDER_PLACED = """
    CREATE TABLE IF NOT EXISTS order_placed(
        customer_email TINYTEXT,
        cart_id INTEGER NOT NULL,
        order_number INTEGER NOT NULL,
        PRIMARY KEY(cart_id, order_number),
        FOREIGN KEY(customer_email) REFERENCES customer(email)
            ON DELETE NO ACTION
            ON UPDATE CASCADE,
        FOREIGN KEY(cart_id) REFERENCES shopping_cart(cart_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
        FOREIGN KEY(order_number) REFERENCES orders(order_number)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    )
"""

BANK_CARD = """
    CREATE TABLE bank_card(
        account_email TINYTEXT,
        card_number CHAR(16)
            CHECK(length(card_number) == 16),
        name TINYTEXT NOT NULL,
        billing_info TINYTEXT NOT NULL,
        PRIMARY KEY(account_email, card_number),
        FOREIGN KEY(account_email) REFERENCES customer(email)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    )
"""

SHIPPING_INFO = """
    CREATE TABLE IF NOT EXISTS shipping_info(
        order_number INTEGER PRIMARY KEY,
        customer_address TINYTEXT NOT NULL,
        estimated_time_arrival DATE NOT NULL,
        shipping_type TINYTEXT NOT NULL,
        shipping_company TINYTEXT NOT NULL,
        shipping_state TINYTEXT NOT NULL,
        tracking_number CHAR(22) NOT NULL,
        FOREIGN KEY(order_number) REFERENCES orders(order_number)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        FOREIGN KEY(customer_address) REFERENCES customer(address),
            ON DELETE NO ACTION
            ON UPDATE CASCADE,
        CHECK (estimated_time_arrival > order_number.date_ordered)
    )
"""
