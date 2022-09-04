DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS history;

CREATE TABLE users (
    username Text not null,
    password TEXT not null
);

CREATE TABLE history (
    no INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT not null,
    topic Text not null,
    score INTEGER not null
);