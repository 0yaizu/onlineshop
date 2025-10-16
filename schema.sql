-- schema.sql
PRAGMA foreign_keys = ON; -- 外部キーを有効化
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
	file_name TEXT,
	file_type TEXT,
	FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE orders (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	order_code TEXT NOT NULL,
	user_id INTEGER NOT NULL,
	item_id INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
	price INTEGER NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

-- INSERT INTO users (username, password) VALUES
-- 	('admin', 'password'),
-- 	('user', 'password');

INSERT INTO users (username, password) VALUES
	('admin', 'scrypt:32768:8:1$Or8E1phImwbHDgEY$c009bf5f09584ee138acbf6ea980d8f895e12b756637923752e195c5fe142fb909861185e45187865f459250bfea2e3ef73a8c7348325e96e896beab2af38aee'),
	('user', 'scrypt:32768:8:1$fKz3dc9JvOC9MLbo$f60746a1796b7feba80e71155313fc0aa7231e70623b7d9dea79697de25f2537c55963b2bdda26ccde1e0159a009669cf46b0030622cfdb0eaed89aa49b06c9e');

INSERT INTO items (owner_id, item_name, price, file_name, file_type) VALUES
	(1, 'りんご', 200, 'apple.jpg', 'jpg'),
	(1, 'みかん', 300, 'orange.jpg', 'jpg'),
	(1, 'バナナ', 100, 'banana.jpg', 'jpg');