-- postgres schema for raw texts and future NLP tables

CREATE TABLE IF NOT EXISTS raw_text (
  id          SERIAL PRIMARY KEY,
  title       TEXT,
  link        TEXT UNIQUE,
  lang        VARCHAR(8),
  content     TEXT,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS entities (
  id           SERIAL PRIMARY KEY,
  raw_text_id  INTEGER REFERENCES raw_text(id),
  entity       TEXT,
  type         TEXT,
  start_pos    INTEGER,
  end_pos      INTEGER
);

CREATE TABLE IF NOT EXISTS translations (
  id           SERIAL PRIMARY KEY,
  raw_text_id  INTEGER REFERENCES raw_text(id),
  target_lang  VARCHAR(8),
  translation  TEXT
);
