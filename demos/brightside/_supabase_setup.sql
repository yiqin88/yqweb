-- ============================================================
-- BRIGHTSIDE TUITION CENTRE — Supabase setup
-- Run entire block in Supabase SQL Editor
-- ============================================================

-- ============================================================
-- 1. Table
-- ============================================================
CREATE TABLE IF NOT EXISTS public.demo_trial_bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  source TEXT NOT NULL DEFAULT 'brightside',
  class_selected TEXT NOT NULL,
  child_name TEXT NOT NULL,
  child_level TEXT NOT NULL,
  parent_name TEXT NOT NULL,
  parent_email TEXT NOT NULL,
  parent_mobile TEXT NOT NULL,
  notes TEXT,
  status TEXT NOT NULL DEFAULT 'new'
);

CREATE INDEX IF NOT EXISTS idx_trial_created ON public.demo_trial_bookings (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_trial_source  ON public.demo_trial_bookings (source, status);

ALTER TABLE public.demo_trial_bookings ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.demo_trial_bookings FROM anon;

-- ============================================================
-- 2. RPC — submit_trial_booking
-- ============================================================
CREATE OR REPLACE FUNCTION public.submit_trial_booking(payload jsonb)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_id UUID;
BEGIN
  IF (payload->>'child_name') IS NULL OR length(trim(payload->>'child_name')) < 1 THEN
    RAISE EXCEPTION 'child_name_required';
  END IF;
  IF (payload->>'parent_name') IS NULL OR length(trim(payload->>'parent_name')) < 1 THEN
    RAISE EXCEPTION 'parent_name_required';
  END IF;
  IF (payload->>'parent_email') IS NULL OR (payload->>'parent_email') !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' THEN
    RAISE EXCEPTION 'invalid_email';
  END IF;
  IF (payload->>'parent_mobile') IS NULL OR length(trim(payload->>'parent_mobile')) < 4 THEN
    RAISE EXCEPTION 'mobile_required';
  END IF;
  IF (payload->>'class_selected') IS NULL OR length(trim(payload->>'class_selected')) < 1 THEN
    RAISE EXCEPTION 'class_required';
  END IF;

  INSERT INTO public.demo_trial_bookings (
    source, class_selected, child_name, child_level,
    parent_name, parent_email, parent_mobile, notes
  ) VALUES (
    COALESCE(payload->>'source', 'brightside'),
    trim(payload->>'class_selected'),
    trim(payload->>'child_name'),
    trim(COALESCE(payload->>'child_level', '')),
    trim(payload->>'parent_name'),
    lower(trim(payload->>'parent_email')),
    trim(payload->>'parent_mobile'),
    NULLIF(trim(payload->>'notes'), '')
  ) RETURNING id INTO new_id;

  RETURN jsonb_build_object('ok', true, 'id', new_id);
END;
$$;

GRANT EXECUTE ON FUNCTION public.submit_trial_booking(jsonb) TO anon;

-- ============================================================
-- 3. Trigger — Telegram + Resend email
-- ============================================================
CREATE OR REPLACE FUNCTION public.notify_new_trial()
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
  safe_child TEXT;
  safe_parent TEXT;
  safe_notes TEXT;
  email_subject TEXT;
  email_html TEXT;
BEGIN
  SELECT decrypted_secret INTO bot_token  FROM vault.decrypted_secrets WHERE name = 'telegram_bot_token' LIMIT 1;
  SELECT decrypted_secret INTO resend_key FROM vault.decrypted_secrets WHERE name = 'resend_api_key'     LIMIT 1;

  safe_child  := replace(replace(replace(COALESCE(NEW.child_name,'')  , '&','&amp;'), '<','&lt;'), '>','&gt;');
  safe_parent := replace(replace(replace(COALESCE(NEW.parent_name,'') , '&','&amp;'), '<','&lt;'), '>','&gt;');
  safe_notes  := replace(replace(replace(COALESCE(NEW.notes,'')       , '&','&amp;'), '<','&lt;'), '>','&gt;');

  -- ===== TELEGRAM =====
  IF bot_token IS NOT NULL THEN
    msg := '📚 Brightside Tuition (DEMO)' || E'\n— New free trial booking —\n\n' ||
           'Class: ' || NEW.class_selected || E'\n\n' ||
           'Child: ' || COALESCE(NEW.child_name, '?') || E'\n' ||
           'Level: ' || COALESCE(NEW.child_level, '?') || E'\n\n' ||
           'Parent: ' || COALESCE(NEW.parent_name, '?') || E'\n' ||
           'Email: ' || COALESCE(NEW.parent_email, '?') || E'\n' ||
           'Mobile: ' || COALESCE(NEW.parent_mobile, '?') ||
           COALESCE(E'\n\nNotes: ' || NEW.notes, '');

    BEGIN
      PERFORM net.http_post(
        url := 'https://api.telegram.org/bot' || bot_token || '/sendMessage',
        headers := jsonb_build_object('Content-Type', 'application/json'),
        body := jsonb_build_object('chat_id', chat_id, 'text', msg, 'disable_web_page_preview', true)
      );
    EXCEPTION WHEN OTHERS THEN
      RAISE WARNING 'telegram send (trial) failed: %', SQLERRM;
    END;
  END IF;

  -- ===== RESEND (parent confirmation) =====
  IF resend_key IS NOT NULL AND NEW.source = 'brightside' AND NEW.parent_email IS NOT NULL THEN
    email_subject := 'Brightside trial confirmed — ' || NEW.class_selected;

    email_html :=
      '<!DOCTYPE html><html><body style="margin:0;padding:0;background:#F5F0E1;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;">' ||
      '<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#F5F0E1;padding:40px 20px;"><tr><td align="center">' ||
      '<table cellpadding="0" cellspacing="0" border="0" width="560" style="max-width:560px;background:#FBFAF7;border-radius:8px;overflow:hidden;">' ||

      '<tr><td style="background:#1F2D27;padding:36px 40px;">' ||
        '<div style="font-family:Georgia,serif;font-weight:600;font-size:32px;color:#FBFAF7;letter-spacing:-0.02em;line-height:1;">Bright<span style="color:#2D6A4F;font-style:italic;">side</span></div>' ||
        '<p style="font-family:Georgia,serif;font-style:italic;color:#E9C46A;font-size:14px;margin:6px 0 0;">Better grades. Without the stress.</p>' ||
      '</td></tr>' ||

      '<tr><td style="padding:40px;">' ||
        '<p style="font-size:12px;color:#2D6A4F;letter-spacing:0.12em;text-transform:uppercase;font-weight:600;margin:0 0 10px;">Free trial confirmed</p>' ||
        '<p style="font-family:Georgia,serif;font-size:30px;color:#1F2D27;line-height:1.15;margin:0 0 24px;font-weight:600;font-style:italic;">See you soon, ' || safe_parent || '.</p>' ||
        '<p style="font-size:15px;line-height:1.55;color:#2A3A33;margin:0 0 24px;">We have ' || safe_child || ' booked in for one free trial class. Here are the details:</p>' ||

        '<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#F5F0E1;border-radius:8px;margin-bottom:24px;border-left:4px solid #E9C46A;"><tr><td style="padding:22px 24px;">' ||
        '<p style="font-size:12px;color:#5A6962;letter-spacing:0.06em;text-transform:uppercase;margin:0 0 8px;font-weight:600;">Class booked</p>' ||
        '<p style="font-family:Georgia,serif;font-size:22px;color:#1F2D27;line-height:1.2;margin:0;font-weight:600;letter-spacing:-0.01em;">' || NEW.class_selected || '</p>' ||
        '</td></tr></table>' ||

        '<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:white;border:1px solid rgba(31,45,39,0.1);border-radius:8px;margin-bottom:24px;"><tr><td style="padding:22px 24px;">' ||
        '<table cellpadding="0" cellspacing="0" border="0" width="100%" style="font-size:14px;color:#2A3A33;line-height:1.9;">' ||
        '<tr><td style="color:#5A6962;width:100px;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;">Student</td><td style="font-weight:600;">' || safe_child || COALESCE(' &middot; ' || NEW.child_level, '') || '</td></tr>' ||
        '<tr><td style="color:#5A6962;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;">Parent</td><td style="font-weight:600;">' || safe_parent || '</td></tr>' ||
        '<tr><td style="color:#5A6962;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;">Mobile</td><td style="font-weight:600;">' || NEW.parent_mobile || '</td></tr>' ||
        '</table></td></tr></table>' ||

        CASE WHEN length(safe_notes) > 0
          THEN '<p style="font-size:13px;color:#5A6962;line-height:1.55;margin:0 0 24px;font-style:italic;border-left:3px solid #2D6A4F;padding-left:14px;">Your note: "' || safe_notes || '"</p>'
          ELSE '' END ||

        '<p style="font-size:14px;line-height:1.55;color:#2A3A33;margin:0 0 16px;"><b style="color:#1F2D27;">What to bring:</b> School textbook, writing materials, water bottle. We provide notes.</p>' ||
        '<p style="font-size:14px;line-height:1.55;color:#2A3A33;margin:0 0 24px;"><b style="color:#1F2D27;">Where:</b> Block 510 Bishan Street 11, #03-12. 2 min from Bishan MRT, above the kopitiam.</p>' ||
        '<p style="font-size:14px;line-height:1.55;color:#5A6962;margin:0 0 24px;">Need to reschedule or have questions? Just reply to this email or message us on <b style="color:#1F2D27;">+65 6789 1234</b>.</p>' ||

        '<hr style="border:none;border-top:1px solid rgba(31,45,39,0.1);margin:28px 0;">' ||
        '<p style="font-family:Georgia,serif;font-style:italic;font-size:18px;color:#2D6A4F;margin:0;">— Ms Lim &amp; the Brightside team</p>' ||
      '</td></tr>' ||

      '<tr><td style="background:#1F2D27;padding:22px 36px;">' ||
        '<p style="font-family:Courier New,monospace;font-size:11px;color:rgba(251,250,247,0.6);line-height:1.6;margin:0;letter-spacing:0.04em;">' ||
        '<span style="color:#E9C46A;">— THIS IS A DEMO —</span><br>' ||
        'Brightside is a fictional tuition centre used to demonstrate Pro-tier features. You booked a trial on a portfolio site built by <a href="https://web.yqservices.org" style="color:#FBFAF7;">YQ Web</a>. ' ||
        'Want one like this? <a href="https://web.yqservices.org/#brief" style="color:#FBFAF7;">Start a brief.</a></p>' ||
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
          'from', 'Brightside Tuition <hello@yqservices.org>',
          'to', jsonb_build_array(NEW.parent_email),
          'reply_to', 'yq@aznet.sg',
          'subject', email_subject,
          'html', email_html
        )
      );
    EXCEPTION WHEN OTHERS THEN
      RAISE WARNING 'resend send (trial) failed: %', SQLERRM;
    END;
  END IF;

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_notify_new_trial ON public.demo_trial_bookings;
CREATE TRIGGER trg_notify_new_trial
AFTER INSERT ON public.demo_trial_bookings
FOR EACH ROW
EXECUTE FUNCTION public.notify_new_trial();
