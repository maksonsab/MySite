
DROP TABLE IF EXISTS articles;

CREATE TABLE articles (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	title TEXT NOT NULL,
	art_description TEXT NOT NULL,
	content TEXT NOT NULL,
	viewes INTEGER DEFAULT 0 
);
