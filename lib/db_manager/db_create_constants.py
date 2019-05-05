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
        FOREIGN KEY(seller_email) REFERENCES item(seller_email),
        FOREIGN KEY(item_id) REFERENCES item(item_id)
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
        FOREIGN KEY(seller_email) REFERENCES seller(email)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(item_id) REFERENCES item(item_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
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
        price DOUBLE NOT NULL
            CHECK(price >= 0),
        name TINYTEXT NOT NULL,
        type TINYTEXT NOT NULL,
        number_of_items_bought INTEGER NOT NULL,
        PRIMARY KEY(cart_id, seller_email, item_id),
        FOREIGN KEY(seller_email) REFERENCES seller(email)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(item_id) REFERENCES item(item_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(cart_id) REFERENCES shopping_cart(cart_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
"""

HAS_SHOPPING_CART = """
    CREATE TABLE IF NOT EXISTS has_shopping_cart(
        customer_email TINYTEXT NOT NULL,
        cart_id INTEGER PRIMARY KEY,
        FOREIGN KEY(customer_email) REFERENCES customer(email),
        FOREIGN KEY(cart_id) REFERENCES items_in_shopping_cart(cart_id)
    )
"""

SHOPPING_CART = """
    CREATE TABLE IF NOT EXISTS shopping_cart(
        cart_id INTEGER PRIMARY KEY
            CHECK(cart_id > 0),
        total_number_of_items INTEGER DEFAULT 0 NOT NULL
            CHECK(total_number_of_items >= 0),
        total_price DOUBLE DEFAULT 0 NOT NULL
            CHECK(total_price >= 0),
        FOREIGN KEY(cart_id) REFERENCES has_shopping_cart(cart_id)
    )
"""

ORDERS = """
    CREATE TABLE IF NOT EXISTS orders(
        order_number INTEGER PRIMARY KEY,
        total_number_of_items INTEGER NOT NULL
            CHECK(total_number_of_items >= 1),
        date_ordered DATE NOT NULL
    )
"""

ORDER_PLACED = """
    CREATE TABLE IF NOT EXISTS order_placed(
        customer_email TINYTEXT,
        cart_id INTEGER NOT NULL UNIQUE,
        order_number INTEGER NOT NULL,
        PRIMARY KEY(cart_id, order_number),
        FOREIGN KEY(customer_email) REFERENCES customer(email)
            ON DELETE CASCADE
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

INVENTORY = """
    CREATE TABLE IF NOT EXISTS inventory(
        seller_email TINYTEXT,
        item_id INTEGER,
        PRIMARY KEY(seller_email, item_id),
        FOREIGN KEY(seller_email) REFERENCES seller(email)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(item_id) REFERENCES item(item_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
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

# After inserting a row in Customer, there will automatically be a relationship between a cart and the email.
SHOPPING_CART_ENTRY_TRIGGER = """
    CREATE TRIGGER IF NOT EXISTS create_shopping_cart
    AFTER INSERT ON customer
        BEGIN
            INSERT INTO has_shopping_cart VALUES(new.email, new.cart_id);
        END;
"""
# Continuing on from the last trigger, this trigger will watch every insert on has_shopping_cart.
# When a row is inserted into has_shopping_cart, it will then create a shopping cart row.
HAS_SHOPPING_CART_ENTRY_TRIGGER = """
    CREATE TRIGGER IF NOT EXISTS has_shopping_cart_entry
    AFTER INSERT ON has_shopping_cart
        BEGIN
            INSERT INTO shopping_cart VALUES(new.cart_id, 0, 0);
        END;
"""
# TODO
ORDER_PLACED_TRIGGER = """
    CREATE TRIGGER IF NOT EXISTS order_placed_entry
    AFTER INSERT ON orders
        BEGIN
            INSERT INTO order_placed(customer_email, cart_id, order_number)
            VALUES(NULL, 123, new.order_number);
        END;
"""
