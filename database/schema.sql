CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'user',
  created_at TEXT NOT NULL
);

CREATE TABLE keys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT UNIQUE NOT NULL,
  days INTEGER,
  used_by INTEGER,
  created_at TEXT NOT NULL,
  expires_at TEXT,
  FOREIGN KEY (used_by) REFERENCES users(id)
);

-- Подписки:
-- 30 дней  = 30
-- 180 дней = 180
-- 1 год    = 365
-- навсегда = NULL