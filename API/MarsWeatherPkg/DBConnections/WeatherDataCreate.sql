CREATE TABLE IF NOT EXISTS sols
(sol INTEGER PRIMARY KEY,
date_retrieved TEXT,
season TEXT,
first_utc TEXT,
last_utc TEXT);

CREATE TABLE IF NOT EXISTS AT
(sol INTEGER PRIMARY KEY,
av REAL,
ct REAL,
mn REAL,
mx REAL,
FOREIGN KEY (sol) REFERENCES sols(sol));

CREATE TABLE IF NOT EXISTS HWS
(sol INTEGER PRIMARY KEY,
av REAL,
ct REAL,
mn REAL,
mx REAL,
FOREIGN KEY (sol) REFERENCES sols(sol));

CREATE TABLE IF NOT EXISTS PRE
(sol INTEGER PRIMARY KEY,
av REAL,
ct REAL,
mn REAL,
mx REAL,
FOREIGN KEY (sol) REFERENCES sols(sol));

CREATE TABLE IF NOT EXISTS compass_pt
(compass_sol_id INTEGER PRIMARY KEY AUTOINCREMENT,
compass_pt_num INTEGER,
sol INTEGER,
compass_degrees REAL,
compass_point TEXT,
compass_right REAL,
compass_up REAL,
ct INTEGER,
FOREIGN KEY (sol) REFERENCES sols(sol));

CREATE TABLE IF NOT EXISTS api_keys
(api_key_id INTEGER PRIMARY KEY AUTOINCREMENT,
api_key_hash TEXT,
date_of_creation TEXT,
username TEXT)