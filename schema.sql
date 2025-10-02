-- schema.sql
PRAGMA foreign_keys = ON;
-- 外部キーを有効化
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);
CREATE TABLE items (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	owner_id INTEGER NOT NULL,
	item_name TEXT NOT NULL,
	price INTEGER NOT NULL,
	FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE orders (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	order_code TEXT NOT NULL,
	user_id INTEGER NOT NULL,
	item_id INTEGER NOT NULL,
	price INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);
INSERT INTO users (username, password)
VALUES ('admin', 'password'),
	('user', 'password');
INSERT INTO items (owner_id, item_name, price) VALUES
	(1, 'りんご', 200),
	(1, 'みかん', 300),
	(1, 'バナナ', 100);