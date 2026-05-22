-- =================================================================
-- KL Trip 2026 — Supabase backend
-- Project: YQ Web Service (sslkappqxwgonzlumkbo, Singapore)
-- No auth — public read/write (data is non-sensitive trip planning)
-- =================================================================

-- ===== TABLES =====

CREATE TABLE IF NOT EXISTS kl_trip_expenses (
  id TEXT PRIMARY KEY,
  amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
  currency TEXT NOT NULL CHECK (currency IN ('MYR', 'SGD')),
  day INTEGER NOT NULL CHECK (day >= 0 AND day <= 5),
  category TEXT NOT NULL CHECK (category IN ('food', 'hotel', 'attraction', 'transport', 'shopping', 'misc')),
  note TEXT,
  ts TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS kl_trip_qrs (
  place_id TEXT PRIMARY KEY,
  image_path TEXT NOT NULL,
  uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS kl_trip_fx (
  id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  rate NUMERIC(6, 4) NOT NULL DEFAULT 3.5000,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO kl_trip_fx (id, rate) VALUES (1, 3.5000) ON CONFLICT (id) DO NOTHING;

-- ===== RLS POLICIES =====
-- Public read/write — no auth, just unlisted URL

ALTER TABLE kl_trip_expenses ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Public read" ON kl_trip_expenses;
DROP POLICY IF EXISTS "Public insert" ON kl_trip_expenses;
DROP POLICY IF EXISTS "Public update" ON kl_trip_expenses;
DROP POLICY IF EXISTS "Public delete" ON kl_trip_expenses;
CREATE POLICY "Public read" ON kl_trip_expenses FOR SELECT USING (true);
CREATE POLICY "Public insert" ON kl_trip_expenses FOR INSERT WITH CHECK (true);
CREATE POLICY "Public update" ON kl_trip_expenses FOR UPDATE USING (true);
CREATE POLICY "Public delete" ON kl_trip_expenses FOR DELETE USING (true);

ALTER TABLE kl_trip_qrs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Public read" ON kl_trip_qrs;
DROP POLICY IF EXISTS "Public insert" ON kl_trip_qrs;
DROP POLICY IF EXISTS "Public update" ON kl_trip_qrs;
DROP POLICY IF EXISTS "Public delete" ON kl_trip_qrs;
CREATE POLICY "Public read" ON kl_trip_qrs FOR SELECT USING (true);
CREATE POLICY "Public insert" ON kl_trip_qrs FOR INSERT WITH CHECK (true);
CREATE POLICY "Public update" ON kl_trip_qrs FOR UPDATE USING (true);
CREATE POLICY "Public delete" ON kl_trip_qrs FOR DELETE USING (true);

ALTER TABLE kl_trip_fx ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Public read" ON kl_trip_fx;
DROP POLICY IF EXISTS "Public update" ON kl_trip_fx;
CREATE POLICY "Public read" ON kl_trip_fx FOR SELECT USING (true);
CREATE POLICY "Public update" ON kl_trip_fx FOR UPDATE USING (true);

-- ===== SEED PREPAID EXPENSES =====

INSERT INTO kl_trip_expenses (id, amount, currency, day, category, note) VALUES
  ('seed-awana',          497.64, 'SGD', 0, 'hotel', 'RW Awana — 3 nights (Mid-Year Hotel Escape, paid)'),
  ('seed-firstworld-d2',   32.87, 'SGD', 0, 'hotel', 'First World — Day 2 rest base, booking 10693258AL (paid, kept as backup)'),
  ('seed-firstworld',      32.87, 'SGD', 0, 'hotel', 'First World — Day 3 rest base, booking 10693538AL (paid)'),
  ('seed-hilton',        2000.00, 'MYR', 1, 'hotel', 'Hilton KL — 1 night (Conf 3471664730, paid on arrival)')
ON CONFLICT (id) DO NOTHING;

-- ===== STORAGE BUCKET for QR images =====
-- Run separately if needed:
-- 1. Create bucket via Supabase dashboard or:
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('kl-trip-qrs', 'kl-trip-qrs', true, 2097152, ARRAY['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'])
ON CONFLICT (id) DO NOTHING;

-- Storage policies — public read + public upload
DROP POLICY IF EXISTS "Public read kl-trip-qrs" ON storage.objects;
DROP POLICY IF EXISTS "Public insert kl-trip-qrs" ON storage.objects;
DROP POLICY IF EXISTS "Public update kl-trip-qrs" ON storage.objects;
DROP POLICY IF EXISTS "Public delete kl-trip-qrs" ON storage.objects;
CREATE POLICY "Public read kl-trip-qrs" ON storage.objects FOR SELECT USING (bucket_id = 'kl-trip-qrs');
CREATE POLICY "Public insert kl-trip-qrs" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'kl-trip-qrs');
CREATE POLICY "Public update kl-trip-qrs" ON storage.objects FOR UPDATE USING (bucket_id = 'kl-trip-qrs');
CREATE POLICY "Public delete kl-trip-qrs" ON storage.objects FOR DELETE USING (bucket_id = 'kl-trip-qrs');

-- ===== VERIFY =====
SELECT 'expenses' as table_name, count(*) as rows FROM kl_trip_expenses
UNION ALL
SELECT 'qrs', count(*) FROM kl_trip_qrs
UNION ALL
SELECT 'fx', count(*) FROM kl_trip_fx;
