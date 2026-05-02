-- 001_create_keywords_table.sql
-- Creates schema for storing keyword candidates and SERP snapshots

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS keywords (
  id             SERIAL PRIMARY KEY,
  keyword        TEXT NOT NULL,
  seed           TEXT NULL, -- original seed keyword that generated this candidate
  country        TEXT DEFAULT 'us',
  language       TEXT DEFAULT 'en',
  volume         INTEGER,
  difficulty     NUMERIC(5,2),
  cpc            NUMERIC(10,4),
  num_results    BIGINT,
  score          NUMERIC(8,6),
  serp_features  JSONB,
  top_results    JSONB,     -- store top-10 SERP snapshot (list of objects)
  source         TEXT,      -- e.g., 'mock' | 'semrush_api'
  created_at     TIMESTAMPTZ DEFAULT now(),
  updated_at     TIMESTAMPTZ DEFAULT now()
);

-- indices for faster queries
CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords (keyword);
CREATE INDEX IF NOT EXISTS idx_keywords_score ON keywords (score DESC);
CREATE INDEX IF NOT EXISTS idx_keywords_seed ON keywords (seed);

-- simple upsert helper (example usage)
-- INSERT INTO keywords (keyword, seed, volume, difficulty, score)
-- VALUES (...)
-- ON CONFLICT (keyword) DO UPDATE SET
--   volume = EXCLUDED.volume,
--   difficulty = EXCLUDED.difficulty,
--   score = EXCLUDED.score,
--   updated_at = now();

