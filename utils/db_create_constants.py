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
		address TINYTEXT,
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
		role CHAR(8) NOT NULL CHECK(role IN ("EMPLOYEE", "ADMIN", "VIP", "MANAGER")),
		date_joined DATE NOT NULL,
		phone_number CHAR(10) NOT NULL UNIQUE 
			CHECK (length(phone_number) == 10)
	)
"""

ORDER = """
	CREATE TABLE IF NOT EXISTS order(
		order_number INTEGER PRIMARY KEY,
		total_number_of_items INTEGER NOT NULL
			CHECK(total_number_of_items >= 1),
		date_ordered DATE NOT NULL
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

ITEM = """
	CREATE TABLE IF NOT EXISTS item(
		seller_email TINYTEXT PRIMARY KEY,
		item_id INTEGER PRIMARY KEY
			CHECK(item_id > 0),
		quantity INTEGER DEFAULT 0 NOT NULL
			CHECK(quantity >= 0),
		price DOUBLE NOT NULL
			CHECK(price >= 0),
		name TINYTEXT NOT NULL,
		type TINYTEXT NOT NULL,
		FOREIGN KEY(seller_email) REFERENCES seller(email)
			ON DELETE CASCADE
			ON UPDATE CASCADE
	)
"""

ITEMS_BOUGHT = """
	CREATE TABLE IF NOT EXISTS items_bought(
		seller_email TINYTEXT PRIMARY KEY,
		item_id INTEGER PRIMARY KEY,
		order_number INTEGER PRIMARY KEY,
		price DOUBLE NOT NULL,
		name TINYTEXT NOT NULL,
		type TINYTEXT NOT NULL,
		number_of_items_bought INTEGER DEFAULT 0 NOT NULL
			CHECK(number_of_items_bought >= 0),
		FOREIGN KEY(seller_email) REFERENCES seller(email)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(item_id) REFERENCES item(item_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(order_number) REFERENCES order(order_number)
			ON DELETE NO ACTION
			ON UPDATE NO ACTION
	)
"""

ITEMS_IN_SHOPPING_CART = """
	CREATE TABLE IF NOT EXISTS items_in_shopping_cart(
		seller_email TINYTEXT PRIMARY KEY,
		item_id INTEGER PRIMARY KEY,
		cart_id INTEGER PRIMARY KEY,
		price DOUBLE NOT NULL
			CHECK(price >= 0),
		name TINYTEXT NOT NULL,
		type TINYTEXT NOT NULL,
		number_of_items_bought INTEGER NOT NULL,
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

BANK_CARD = """
	CREATE TABLE bank_card(
		account_email TINYTEXT PRIMARY KEY,
		card_number CHAR(16) PRIMARY KEY
			CHECK(length(card_number) == 16),
		name TINYTEXT NOT NULL,
		billing_info TINYTEXT NOT NULL,
		FOREIGN KEY(account_email) REFERENCES customer(email)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
	)
"""

INVENTORY = """
	CREATE TABLE IF NOT EXISTS inventory(
		seller_email TINYTEXT PRIMARY KEY,
		item_id INTEGER PRIMARY KEY,
		FOREIGN KEY(seller_email) REFERENCES seller(email)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(item_id) REFERENCES item(item_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
	)
"""

ORDER_PLACED = """
	CREATE TABLE IF NOT EXISTS order_placed(
		customer_email TINYTEXT PRIMARY KEY,
		cart_id INTEGER NOT NULL UNIQUE,
		order_number INTEGER NOT NULL,
		FOREIGN KEY(customer_email) REFERENCES customer(email)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(cart_id) REFERENCES shopping_cart(cart_id)
			ON DELETE CASCADE
			ON UPDATE NO ACTION,
		FOREIGN KEY(order_number) REFERENCES order(order_number)
			ON DELETE NO ACTION
			ON UPDATE NO ACTION
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
	    FOREIGN KEY(order_number) REFERENCES order(order_number)
	        ON DELETE NO ACTION
	        ON UPDATE NO ACTION,
	    FOREIGN KEY(customer_address) REFERENCES customer(address),
	        ON DELETE NO ACTION
	        ON UPDATE CASCADE,
	    CHECK (estimated_time_arrival > order_number.date_ordered)
	)
"""