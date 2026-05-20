-- ============================================================
-- NORTHWIND AIRCON DEMO — Supabase setup
-- Run all of this in one go in the SQL Editor
-- ============================================================

-- ============================================================
-- 1. Storage bucket for uploaded aircon photos
-- ============================================================
INSERT INTO storage.buckets (id, name, public)
VALUES ('aircon-uploads', 'aircon-uploads', true)
ON CONFLICT (id) DO NOTHING;

-- Allow anonymous uploads to this bucket only
DROP POLICY IF EXISTS "anon upload aircon" ON storage.objects;
CREATE POLICY "anon upload aircon" ON storage.objects
  FOR INSERT TO anon
  WITH CHECK (bucket_id = 'aircon-uploads');

-- Allow public read for this bucket
DROP POLICY IF EXISTS "public read aircon" ON storage.objects;
CREATE POLICY "public read aircon" ON storage.objects
  FOR SELECT TO anon
  USING (bucket_id = 'aircon-uploads');

-- ============================================================
-- 2. Quotes table
-- ============================================================
CREATE TABLE IF NOT EXISTS public.demo_quotes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  source TEXT NOT NULL DEFAULT 'northwind',
  service_type TEXT NOT NULL,
  units INT NOT NULL DEFAULT 1 CHECK (units BETWEEN 1 AND 10),
  postal TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  mobile TEXT NOT NULL,
  preferred_date DATE,
  notes TEXT,
  photo_url TEXT,
  estimate_low INT,
  estimate_high INT,
  status TEXT NOT NULL DEFAULT 'new'
);

CREATE INDEX IF NOT EXISTS idx_demo_quotes_created ON public.demo_quotes (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_demo_quotes_source ON public.demo_quotes (source, status);

-- Lock down — same pattern as web_briefs and demo_reservations
ALTER TABLE public.demo_quotes ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.demo_quotes FROM anon;

-- ============================================================
-- 3. RPC — validated insert with auto-estimate
-- ============================================================
CREATE OR REPLACE FUNCTION public.submit_aircon_quote(payload jsonb)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_id UUID;
  v_units INT;
  v_service TEXT;
  v_postal TEXT;
  v_base INT;
  v_low INT;
  v_high INT;
BEGIN
  IF (payload->>'name') IS NULL OR length(trim(payload->>'name')) < 1 THEN
    RAISE EXCEPTION 'name_required';
  END IF;
  IF (payload->>'email') IS NULL OR (payload->>'email') !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' THEN
    RAISE EXCEPTION 'invalid_email';
  END IF;
  IF (payload->>'mobile') IS NULL OR length(trim(payload->>'mobile')) < 4 THEN
    RAISE EXCEPTION 'mobile_required';
  END IF;
  v_postal := trim(COALESCE(payload->>'postal', ''));
  IF v_postal !~ '^[0-9]{6}$' THEN
    RAISE EXCEPTION 'invalid_postal';
  END IF;
  v_service := COALESCE(payload->>'service_type', '');
  IF v_service NOT IN ('general','chemwash','repair','install','multi','unsure') THEN
    RAISE EXCEPTION 'invalid_service_type';
  END IF;

  v_units := GREATEST(1, LEAST(10, COALESCE((payload->>'units')::INT, 1)));

  -- Estimate calculation (server-side, matches the JS hint)
  v_base := CASE v_service
    WHEN 'general'   THEN 50
    WHEN 'chemwash'  THEN 120
    WHEN 'repair'    THEN 80
    WHEN 'install'   THEN 300
    WHEN 'multi'     THEN 60
    ELSE 0
  END;

  IF v_base > 0 THEN
    v_low  := v_base * v_units;
    v_high := (v_base * v_units * 1.25)::INT;
  ELSE
    v_low := NULL; v_high := NULL;
  END IF;

  INSERT INTO public.demo_quotes (
    source, service_type, units, postal,
    name, email, mobile,
    preferred_date, notes, photo_url,
    estimate_low, estimate_high
  ) VALUES (
    COALESCE(payload->>'source', 'northwind'),
    v_service,
    v_units,
    v_postal,
    trim(payload->>'name'),
    lower(trim(payload->>'email')),
    trim(payload->>'mobile'),
    NULLIF(payload->>'preferred_date', '')::DATE,
    NULLIF(trim(payload->>'notes'), ''),
    NULLIF(trim(payload->>'photo_url'), ''),
    v_low, v_high
  ) RETURNING id INTO new_id;

  RETURN jsonb_build_object(
    'ok', true,
    'id', new_id,
    'estimate_low', v_low,
    'estimate_high', v_high
  );
END;
$$;

GRANT EXECUTE ON FUNCTION public.submit_aircon_quote(jsonb) TO anon;

-- ============================================================
-- 4. Telegram + Resend notification trigger
-- ============================================================
CREATE OR REPLACE FUNCTION public.notify_new_quote()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  bot_token TEXT;
  resend_key TEXT;
  chat_id BIGINT := 337869645;
  msg TEXT;
  service_pretty TEXT;
  estimate_pretty TEXT;
  safe_name TEXT;
  safe_notes TEXT;
  date_pretty TEXT;
  email_subject TEXT;
  email_html TEXT;
BEGIN
  SELECT decrypted_secret INTO bot_token  FROM vault.decrypted_secrets WHERE name = 'telegram_bot_token' LIMIT 1;
  SELECT decrypted_secret INTO resend_key FROM vault.decrypted_secrets WHERE name = 'resend_api_key'     LIMIT 1;

  service_pretty := CASE NEW.service_type
    WHEN 'general'   THEN 'General Servicing'
    WHEN 'chemwash'  THEN 'Chemical Wash'
    WHEN 'repair'    THEN 'Repair / Top-up'
    WHEN 'install'   THEN 'New Install'
    WHEN 'multi'     THEN 'Multiple / Combo'
    WHEN 'unsure'    THEN 'Not sure — needs advice'
    ELSE NEW.service_type
  END;

  IF NEW.estimate_low IS NOT NULL THEN
    estimate_pretty := 'S$' || NEW.estimate_low || '–' || NEW.estimate_high;
  ELSE
    estimate_pretty := 'Custom quote (no auto-estimate)';
  END IF;

  -- HTML-escape user input
  safe_name  := replace(replace(replace(COALESCE(NEW.name, ''),  '&','&amp;'), '<','&lt;'), '>','&gt;');
  safe_notes := replace(replace(replace(COALESCE(NEW.notes, ''), '&','&amp;'), '<','&lt;'), '>','&gt;');

  -- ===== TELEGRAM =====
  IF bot_token IS NOT NULL THEN
    msg := '❄️ Northwind Aircon (DEMO)' || E'\n— New quote request —\n\n' ||
           'Service: ' || service_pretty || E'\n' ||
           'Units: ' || NEW.units || E'\n' ||
           'Postal: ' || NEW.postal || E'\n' ||
           'Estimate: ' || estimate_pretty || E'\n\n' ||
           'Name: ' || COALESCE(NEW.name,  '?') || E'\n' ||
           'Email: ' || COALESCE(NEW.email, '?') || E'\n' ||
           'Mobile: ' || COALESCE(NEW.mobile,'?') ||
           COALESCE(E'\nPreferred: ' || NEW.preferred_date::TEXT, '') ||
           COALESCE(E'\n\nNotes: ' || NEW.notes, '') ||
           COALESCE(E'\n\nPhoto: ' || NEW.photo_url, E'\n\nNo photo provided');

    BEGIN
      PERFORM net.http_post(
        url := 'https://api.telegram.org/bot' || bot_token || '/sendMessage',
        headers := jsonb_build_object('Content-Type', 'application/json'),
        body := jsonb_build_object(
          'chat_id', chat_id,
          'text', msg,
          'disable_web_page_preview', false
        )
      );
    EXCEPTION WHEN OTHERS THEN
      RAISE WARNING 'telegram send (quote) failed: %', SQLERRM;
    END;
  END IF;

  -- ===== RESEND (customer-facing quote acknowledgement) =====
  IF resend_key IS NOT NULL AND NEW.source = 'northwind' AND NEW.email IS NOT NULL THEN
    date_pretty := COALESCE(to_char(NEW.preferred_date, 'FMDay, FMDD Mon YYYY'), 'Not specified');
    email_subject := 'Your Northwind Aircon quote — ' || service_pretty || ' for ' || NEW.units || ' unit(s)';

    email_html :=
      '<!DOCTYPE html><html><body style="margin:0;padding:0;background:#F1F4F9;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;">' ||
      '<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#F1F4F9;padding:40px 20px;"><tr><td align="center">' ||
      '<table cellpadding="0" cellspacing="0" border="0" width="560" style="max-width:560px;background:#FFFFFF;border-radius:8px;overflow:hidden;">' ||
      '<tr><td style="background:#0A1628;padding:32px 36px;">' ||
        '<div style="font-family:Georgia,serif;font-weight:700;font-size:26px;color:#FFFFFF;letter-spacing:-0.01em;line-height:1;">Northwind <span style="color:#00A8C8;">Aircon</span></div>' ||
      '</td></tr>' ||
      '<tr><td style="padding:36px;">' ||
        '<p style="font-size:13px;color:#0066CC;letter-spacing:0.12em;text-transform:uppercase;font-weight:600;margin:0 0 10px;">Quote received</p>' ||
        '<p style="font-family:Georgia,serif;font-size:28px;color:#0A1628;line-height:1.2;margin:0 0 24px;font-weight:700;">Thanks ' || safe_name || ', we got it.</p>' ||
        '<p style="font-size:15px;line-height:1.55;color:#1E2A3F;margin:0 0 24px;">Our team will email your full quote within the hour during opening hours (9am-9pm SGT). Here is what we have on file:</p>' ||

        '<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#F1F4F9;border-radius:8px;margin-bottom:24px;"><tr><td style="padding:22px 24px;">' ||
        '<table cellpadding="0" cellspacing="0" border="0" width="100%" style="font-size:14px;color:#1E2A3F;line-height:1.9;">' ||
        '<tr><td style="color:#5B6B85;width:120px;font-size:12px;text-transform:uppercase;letter-spacing:0.08em;">Service</td><td style="font-weight:600;">' || service_pretty || '</td></tr>' ||
        '<tr><td style="color:#5B6B85;font-size:12px;text-transform:uppercase;letter-spacing:0.08em;">Units</td><td style="font-weight:600;">' || NEW.units || '</td></tr>' ||
        '<tr><td style="color:#5B6B85;font-size:12px;text-transform:uppercase;letter-spacing:0.08em;">Postal</td><td style="font-weight:600;">' || NEW.postal || '</td></tr>' ||
        '<tr><td style="color:#5B6B85;font-size:12px;text-transform:uppercase;letter-spacing:0.08em;">Preferred</td><td style="font-weight:600;">' || date_pretty || '</td></tr>' ||
        '</table></td></tr></table>' ||

        CASE WHEN NEW.estimate_low IS NOT NULL THEN
          '<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:linear-gradient(135deg,#E8F1FB,#FFFFFF);border:1px solid rgba(0,102,204,0.2);border-radius:8px;margin-bottom:24px;"><tr><td style="padding:22px 24px;">' ||
          '<p style="font-size:12px;color:#5B6B85;letter-spacing:0.08em;text-transform:uppercase;margin:0 0 6px;font-weight:600;">Estimated quote</p>' ||
          '<p style="font-family:Georgia,serif;font-size:28px;color:#0066CC;line-height:1;margin:0 0 6px;font-weight:700;letter-spacing:-0.02em;">S$' || NEW.estimate_low || '&ndash;' || NEW.estimate_high || '</p>' ||
          '<p style="font-size:12px;color:#5B6B85;margin:0;">Final price confirmed after our team reviews your photo &amp; details.</p>' ||
          '</td></tr></table>'
        ELSE '' END ||

        CASE WHEN length(safe_notes) > 0
          THEN '<p style="font-size:13px;color:#5B6B85;line-height:1.55;margin:0 0 24px;font-style:italic;">Your note: "' || safe_notes || '"</p>'
          ELSE '' END ||

        '<p style="font-size:14px;line-height:1.55;color:#5B6B85;margin:0 0 24px;">Need to change anything or follow up urgently? Just reply to this email or call <b style="color:#0A1628;">+65 6789 4321</b>.</p>' ||

        '<hr style="border:none;border-top:1px solid rgba(10,22,40,0.08);margin:28px 0;">' ||
        '<p style="font-size:13px;line-height:1.6;color:#5B6B85;margin:0;"><b style="color:#0A1628;">Northwind Aircon Services</b><br>15 Kallang Pudding Road #03-12, Singapore 349324<br>Mon-Fri 8am-9pm &middot; Sat 9am-7pm &middot; Sun 10am-5pm</p>' ||
      '</td></tr>' ||

      '<tr><td style="background:#0A1628;padding:22px 36px;">' ||
        '<p style="font-family:Courier New,monospace;font-size:11px;color:rgba(255,255,255,0.6);line-height:1.6;margin:0;letter-spacing:0.04em;">' ||
        '<span style="color:#00A8C8;">— THIS IS A DEMO —</span><br>' ||
        'Northwind Aircon is a fictional company used to demonstrate Pro-tier features. You submitted a quote on a portfolio site built by <a href="https://web.yqservices.org" style="color:#FFFFFF;">YQ Web</a>. ' ||
        'Want one like this? <a href="https://web.yqservices.org/#brief" style="color:#FFFFFF;">Start a brief.</a></p>' ||
      '</td></tr>' ||
      '</table></td></tr></table></body></html>';

    BEGIN
      PERFORM net.http_post(
        url := 'https://api.resend.com/emails',
        headers := jsonb_build_object(
          'Content-Type', 'application/json',
          'Authorization', 'Bearer ' || resend_key
        ),
        body := jsonb_build_object(
          'from', 'Northwind Aircon <hello@yqservices.org>',
          'to', jsonb_build_array(NEW.email),
          'reply_to', 'yq@aznet.sg',
          'subject', email_subject,
          'html', email_html
        )
      );
    EXCEPTION WHEN OTHERS THEN
      RAISE WARNING 'resend send (quote) failed: %', SQLERRM;
    END;
  END IF;

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_notify_new_quote ON public.demo_quotes;
CREATE TRIGGER trg_notify_new_quote
AFTER INSERT ON public.demo_quotes
FOR EACH ROW
EXECUTE FUNCTION public.notify_new_quote();
