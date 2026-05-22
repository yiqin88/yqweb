p = '/Users/yiqin/Desktop/Claude Code Projects/yqweb/trip-kl-genting-2026/index.html'
with open(p) as f: html = f.read()

# =================================================================
# Add CSS for Places & Expenses to the existing <style> block
# =================================================================
css_additions = """

/* =========================
   PLACES & TICKETS section
   ========================= */
.places-tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 22px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  padding-bottom: 6px;
}
.places-tab {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 9px 14px;
  border-radius: 100px;
  background: var(--paper);
  color: var(--muted);
  border: 1px solid var(--line);
  cursor: pointer;
  white-space: nowrap;
  transition: all .2s;
  flex-shrink: 0;
}
.places-tab:hover { color: var(--ink); border-color: var(--line-2); }
.places-tab.active {
  background: var(--moss);
  color: var(--cream);
  border-color: var(--moss);
}
.places-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}
@media (min-width: 720px) { .places-grid { grid-template-columns: 1fr 1fr; } }

.place-card {
  background: white;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 20px;
  position: relative;
  overflow: hidden;
}
.place-card::before {
  content: '';
  position: absolute;
  left: 0; top: 0;
  width: 3px; height: 100%;
}
.place-card.hotel::before { background: var(--moss); }
.place-card.restaurant::before { background: var(--sunset); }
.place-card.attraction::before { background: var(--gold); }
.place-card.transport::before { background: var(--sky); }

.place-icon-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 8px;
}
.place-type {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--moss);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.place-type .place-icon { font-size: 14px; }
.place-day {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  background: var(--paper);
  color: var(--ink-2);
  padding: 3px 8px;
  border-radius: 100px;
  font-weight: 600;
}
.place-name {
  font-family: var(--display);
  font-weight: 500;
  font-size: 20px;
  letter-spacing: -0.01em;
  line-height: 1.15;
  color: var(--ink);
  margin-bottom: 12px;
}
.place-name i { font-style: italic; color: var(--moss); }
.place-detail {
  font-size: 13px;
  color: var(--ink-2);
  margin-bottom: 5px;
  line-height: 1.5;
  display: flex;
  gap: 6px;
  align-items: flex-start;
}
.place-detail .label {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--mute-2);
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  min-width: 60px;
  padding-top: 2px;
  flex-shrink: 0;
}
.place-detail a {
  color: var(--sunset);
  text-decoration: underline;
  text-decoration-color: rgba(198,106,60,0.4);
  text-underline-offset: 2px;
}
.place-detail .ref {
  font-family: var(--mono);
  font-size: 12px;
  background: var(--paper);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--ink);
  font-weight: 600;
}
.place-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--line);
}
.place-actions a, .place-actions button {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  padding: 7px 12px;
  border-radius: 100px;
  background: var(--paper);
  color: var(--moss);
  border: 1px solid var(--line);
  transition: all .2s;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.place-actions a:hover, .place-actions button:hover {
  background: var(--moss);
  color: var(--cream);
  border-color: var(--moss);
}
.place-qr-area {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--line);
}
.place-qr-img {
  width: 100%;
  max-width: 280px;
  height: auto;
  border-radius: 8px;
  border: 1px solid var(--line);
  display: block;
  cursor: zoom-in;
  transition: transform .2s;
}
.place-qr-img:hover { transform: scale(1.02); }
.place-qr-label {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--mute-2);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 8px;
}
.place-qr-clear {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--sunset);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-weight: 600;
  margin-top: 8px;
  cursor: pointer;
  display: inline-block;
}
.qr-upload-label {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  padding: 7px 12px;
  border-radius: 100px;
  background: rgba(217,167,65,0.18);
  color: var(--sunset-deep);
  border: 1px dashed var(--gold);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all .2s;
}
.qr-upload-label:hover {
  background: var(--gold);
  color: var(--ink);
}
.qr-upload-label input { display: none; }

/* Fullscreen QR modal */
.qr-modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(20, 25, 22, 0.92);
  z-index: 9999;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
  cursor: zoom-out;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
.qr-modal.active { display: flex; }
.qr-modal img {
  max-width: 95%;
  max-height: 90vh;
  border-radius: 12px;
  background: white;
  padding: 16px;
}
.qr-modal .close {
  position: absolute;
  top: 20px; right: 24px;
  color: white;
  font-size: 28px;
  cursor: pointer;
  font-family: var(--mono);
  background: rgba(0,0,0,0.4);
  width: 40px; height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* =========================
   EXPENSES tracker section
   ========================= */
.expense-form {
  background: var(--moss);
  color: var(--cream);
  border-radius: 16px;
  padding: 22px;
  margin-bottom: 22px;
}
.expense-form-title {
  font-family: var(--display);
  font-style: italic;
  font-weight: 500;
  font-size: 18px;
  margin-bottom: 14px;
  color: var(--gold);
}
.expense-form-row {
  display: grid;
  grid-template-columns: 90px 70px 1fr;
  gap: 8px;
  margin-bottom: 10px;
}
@media (min-width: 540px) {
  .expense-form-row { grid-template-columns: 110px 80px 90px 1fr; }
}
.expense-form input, .expense-form select {
  font-family: var(--sans);
  font-size: 14px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid rgba(250,246,238,0.18);
  background: rgba(250,246,238,0.08);
  color: var(--cream);
  width: 100%;
  outline: none;
  transition: all .2s;
}
.expense-form input::placeholder { color: rgba(250,246,238,0.5); }
.expense-form input:focus, .expense-form select:focus {
  background: rgba(250,246,238,0.14);
  border-color: var(--gold);
}
.expense-form select option { background: var(--moss-deep); color: var(--cream); }
.expense-form input[type=text].note-input { grid-column: 1 / -1; }
@media (min-width: 540px) {
  .expense-form input[type=text].note-input { grid-column: auto; }
}
.expense-form button.add-btn {
  font-family: var(--sans);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 11px 22px;
  border-radius: 8px;
  background: var(--gold);
  color: var(--ink);
  border: none;
  cursor: pointer;
  width: 100%;
  margin-top: 8px;
  transition: all .2s;
}
.expense-form button.add-btn:hover {
  background: #C99738;
  transform: translateY(-1px);
}

/* Totals bar */
.expense-totals {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 18px;
}
@media (min-width: 540px) {
  .expense-totals { grid-template-columns: repeat(4, 1fr); }
}
.expense-total-card {
  background: white;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px 16px;
}
.expense-total-card .label {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--mute-2);
  font-weight: 600;
  margin-bottom: 4px;
}
.expense-total-card .amount {
  font-family: var(--display);
  font-weight: 500;
  font-size: 22px;
  color: var(--ink);
  line-height: 1.1;
}
.expense-total-card .amount-sub {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--mute-2);
  margin-top: 3px;
}

/* Filter */
.expense-filter {
  display: flex;
  gap: 6px;
  margin-bottom: 14px;
  overflow-x: auto;
  padding-bottom: 4px;
}
.expense-filter-btn {
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 7px 12px;
  border-radius: 100px;
  background: var(--paper);
  color: var(--muted);
  border: 1px solid var(--line);
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  transition: all .2s;
}
.expense-filter-btn:hover { color: var(--ink); }
.expense-filter-btn.active {
  background: var(--ink);
  color: var(--cream);
  border-color: var(--ink);
}

/* Expense list */
.expense-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.expense-day-group {
  margin-bottom: 16px;
}
.expense-day-header {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--moss);
  font-weight: 700;
  padding: 8px 4px;
  border-bottom: 1px solid var(--line);
  margin-bottom: 6px;
  display: flex;
  justify-content: space-between;
}
.expense-day-header .day-total {
  font-family: var(--mono);
  color: var(--ink);
  font-size: 12px;
}
.expense-item {
  background: white;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 12px 14px;
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 12px;
  align-items: center;
  font-size: 13px;
}
.expense-item .cat-icon {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: var(--paper);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}
.expense-item .note {
  color: var(--ink);
  line-height: 1.4;
}
.expense-item .note small {
  display: block;
  font-family: var(--mono);
  font-size: 10px;
  color: var(--mute-2);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-top: 1px;
}
.expense-item .amount {
  font-family: var(--display);
  font-weight: 500;
  font-size: 16px;
  color: var(--ink);
  white-space: nowrap;
}
.expense-item .amount small {
  display: block;
  font-family: var(--mono);
  font-size: 10px;
  color: var(--mute-2);
  text-align: right;
  margin-top: 1px;
}
.expense-item .del-btn {
  font-family: var(--mono);
  font-size: 14px;
  color: var(--mute-2);
  cursor: pointer;
  padding: 6px;
  line-height: 1;
  transition: color .2s;
}
.expense-item .del-btn:hover { color: var(--sunset-deep); }
.expense-empty {
  text-align: center;
  padding: 40px 20px;
  color: var(--mute-2);
  font-family: var(--display);
  font-style: italic;
  font-size: 16px;
}

/* FX rate */
.fx-rate-bar {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--mute-2);
  letter-spacing: 0.04em;
  text-align: right;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--line);
}
.fx-rate-bar input {
  font-family: var(--mono);
  font-size: 11px;
  width: 50px;
  padding: 3px 6px;
  border: 1px solid var(--line-2);
  border-radius: 4px;
  background: white;
  color: var(--ink);
  text-align: center;
}
.fx-rate-bar .reset-btn {
  font-family: var(--mono);
  font-size: 10px;
  color: var(--sunset);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  cursor: pointer;
  margin-left: 12px;
  font-weight: 600;
}
"""

# Insert before /* print */ media query
marker = '/* print */'
html = html.replace(marker, css_additions + '\n' + marker)
print('OK: CSS additions injected')

# =================================================================
# Add Places & Expenses sections HTML before <!-- FOOTER --> or footer
# =================================================================
new_sections = """
<!-- ============================================
     PLACES & TICKETS
     ============================================ -->
<section class="block" id="places">
  <div class="container">
    <span class="section-eyebrow">— Places &amp; Tickets</span>
    <h2 class="display section-h2">All in <i>one place.</i></h2>
    <p class="section-lead">Every hotel, restaurant, attraction and ticket — with address, phone, booking ref and a slot to upload the QR code when you have it. Tap a QR to fullscreen for the scanner.</p>

    <div class="places-tabs" id="placesTabs">
      <button class="places-tab active" data-filter="all">All</button>
      <button class="places-tab" data-filter="hotel">Hotels</button>
      <button class="places-tab" data-filter="restaurant">Restaurants</button>
      <button class="places-tab" data-filter="attraction">Attractions</button>
      <button class="places-tab" data-filter="day1">Day 1</button>
      <button class="places-tab" data-filter="day2">Day 2</button>
      <button class="places-tab" data-filter="day3">Day 3</button>
      <button class="places-tab" data-filter="day4">Day 4</button>
      <button class="places-tab" data-filter="day5">Day 5</button>
    </div>

    <div class="places-grid" id="placesGrid">
      <!-- populated by JS -->
    </div>
  </div>
</section>

<!-- ============================================
     EXPENSES tracker
     ============================================ -->
<section class="block" id="expenses">
  <div class="container">
    <span class="section-eyebrow">— Spending tracker</span>
    <h2 class="display section-h2">Where the <i>money goes.</i></h2>
    <p class="section-lead">Quick-log every meal, ticket, snack. Daily totals + trip total. Both currencies. Saved locally on your phone — no account, no cloud.</p>

    <div class="expense-form">
      <div class="expense-form-title">Add a spend</div>
      <div class="expense-form-row">
        <input type="number" id="expAmount" placeholder="Amount" step="0.01" min="0" />
        <select id="expCurrency">
          <option value="MYR">MYR</option>
          <option value="SGD">SGD</option>
        </select>
        <select id="expDay">
          <option value="0">Pre-trip</option>
          <option value="1">Day 1 · Tue</option>
          <option value="2">Day 2 · Wed</option>
          <option value="3">Day 3 · Thu</option>
          <option value="4">Day 4 · Fri</option>
          <option value="5">Day 5 · Sat</option>
        </select>
        <input type="text" id="expNote" class="note-input" placeholder="What was it? e.g. Loong Kee dinner" />
      </div>
      <div class="expense-form-row" style="grid-template-columns: 1fr;">
        <select id="expCategory">
          <option value="food">🍴 Food &amp; drink</option>
          <option value="hotel">🏨 Hotel</option>
          <option value="attraction">🎡 Tickets &amp; attractions</option>
          <option value="transport">🚗 Transport / charging</option>
          <option value="shopping">🛍 Shopping</option>
          <option value="misc">📌 Misc</option>
        </select>
      </div>
      <button class="add-btn" id="expAdd">+ Add spend</button>
    </div>

    <div class="expense-totals" id="expTotals">
      <!-- populated by JS -->
    </div>

    <div class="expense-filter" id="expFilter">
      <button class="expense-filter-btn active" data-day="all">All days</button>
      <button class="expense-filter-btn" data-day="0">Pre-trip</button>
      <button class="expense-filter-btn" data-day="1">Day 1</button>
      <button class="expense-filter-btn" data-day="2">Day 2</button>
      <button class="expense-filter-btn" data-day="3">Day 3</button>
      <button class="expense-filter-btn" data-day="4">Day 4</button>
      <button class="expense-filter-btn" data-day="5">Day 5</button>
    </div>

    <div class="expense-list" id="expList">
      <!-- populated by JS -->
    </div>

    <div class="fx-rate-bar">
      FX rate: 1 SGD = <input type="number" id="fxRate" step="0.01" min="1" value="3.50" /> MYR
      · <span class="reset-btn" id="expReset">Reset all expenses</span>
    </div>
  </div>
</section>

<!-- Fullscreen QR modal -->
<div class="qr-modal" id="qrModal">
  <span class="close" id="qrClose">×</span>
  <img id="qrModalImg" src="" alt="QR" />
</div>

"""

# Insert before footer
old = '<!-- ============================================\n     FOOTER\n     ============================================ -->'
if old in html:
    html = html.replace(old, new_sections + '\n' + old)
    print('OK: Places + Expenses sections inserted')
else:
    print('MISS: footer marker not found')

# =================================================================
# Add JavaScript for Places + Expenses to existing <script> block
# =================================================================
js_additions = """

/* =========================
   PLACES & TICKETS data + render
   ========================= */
(function() {
  const PLACES = [
    // === HOTELS ===
    { id: 'hilton-kl', cat: 'hotel', icon: '🏨', day: 1, name: 'Hilton <i>Kuala Lumpur</i>',
      address: '3 Jalan Stesen Sentral, Kuala Lumpur 50470, MY',
      phone: '+60 3 2264 2264', email: 'kulhi.reservation@hilton.com',
      ref: 'Conf #3471664730', refExtra: 'Honors #2773814641',
      mapsUrl: 'https://maps.google.com/?q=Hilton+Kuala+Lumpur,+3+Jalan+Stesen+Sentral',
      notes: 'Same-floor request. Early check-in requested for 1 PM arrival.'
    },
    { id: 'awana', cat: 'hotel', icon: '🏨', day: 2, name: 'Resorts World <i>Awana</i>',
      address: 'Genting Highlands, 69000 Pahang, MY',
      phone: '+60 3 2718 1118', email: 'reservation.info@rwgenting.com',
      ref: 'Ref EL0000100460', refExtra: 'Mid-Year Hotel Escape · 3 nights',
      mapsUrl: 'https://maps.google.com/?q=Resorts+World+Awana+Genting',
      notes: '2 Superior Deluxe rooms, 2 Queen each. Adjacent + renovated wing + same floor requested. Confirmed by Michelle Chuah.'
    },
    { id: 'firstworld', cat: 'hotel', icon: '🏨', day: 3, name: 'First World <i>Hotel</i>',
      address: 'Genting Highlands (top of mountain, next to SkyWorlds)',
      phone: '+60 3 2718 1118', email: '',
      ref: 'Booking #10693538AL', refExtra: 'Member #1218997403 (Hui Shan)',
      mapsUrl: 'https://maps.google.com/?q=First+World+Hotel+Genting',
      notes: 'Day 3 daytime rest base only (25-26 Jun). Request late checkout to 3 PM for theme park afternoon.'
    },

    // === ATTRACTIONS / TICKETS ===
    { id: 'klcc-park', cat: 'attraction', icon: '🌳', day: 1, name: 'KLCC <i>Park</i>',
      address: 'Petronas Twin Towers, Kuala Lumpur',
      phone: '', email: '',
      ref: '', refExtra: 'Free entry · Lake Symphony fountain 8-10 PM hourly',
      mapsUrl: 'https://maps.google.com/?q=KLCC+Park',
      notes: 'Playground for Charlotte. Fountain show every hour 8-10 PM.'
    },
    { id: 'aquaria', cat: 'attraction', icon: '🐠', day: 2, name: 'Aquaria <i>KLCC</i>',
      address: 'Concourse Level, KL Convention Centre, KLCC',
      phone: '+60 3 2333 1888', email: '',
      ref: 'Tickets ~RM 75 adult / RM 65 child',
      refExtra: 'Book online for 10% off',
      mapsUrl: 'https://maps.google.com/?q=Aquaria+KLCC',
      notes: 'Opens 10 AM. 90 min visit enough. Underground, air-conditioned, low-walking.'
    },
    { id: 'cable-car', cat: 'attraction', icon: '🚠', day: 3, name: 'Awana <i>SkyWay</i> cable car',
      address: 'Awana SkyWay Station, Genting Highlands',
      phone: '+60 3 2718 1118', email: '',
      ref: 'Round-trip ~RM 10-15/pax', refExtra: 'Used Day 3 — UP 9:30 AM, DOWN 8:30 PM',
      mapsUrl: 'https://maps.google.com/?q=Awana+SkyWay+Genting',
      notes: 'One round-trip ticket used Day 3. Glass-bottom gondolas +RM 5/pax optional.'
    },
    { id: 'skyworlds', cat: 'attraction', icon: '🎢', day: 3, name: 'Genting <i>SkyWorlds</i>',
      address: 'Resorts World Genting (top of mountain)',
      phone: '', email: '',
      ref: '~RM 200 adult / RM 170 child', refExtra: 'Check Klook for promos (often 20% off)',
      mapsUrl: 'https://maps.google.com/?q=Genting+SkyWorlds',
      notes: 'Charlotte may be under 130 cm for wildest rides. Park typically opens 11 AM weekday.'
    },
    { id: 'chinswee', cat: 'attraction', icon: '🛕', day: 4, name: 'Chin Swee <i>Caves Temple</i>',
      address: 'Genting Highlands (mid-level)',
      phone: '', email: '',
      ref: 'Free entry', refExtra: 'Donations welcomed',
      mapsUrl: 'https://maps.google.com/?q=Chin+Swee+Caves+Temple',
      notes: '9-storey pagoda, Buddha statue, mountain views. Drive up from Awana ~15 min, parking available. Lifts between levels.'
    },
    { id: 'skytropolis', cat: 'attraction', icon: '🎠', day: 4, name: 'Skytropolis <i>Indoor</i>',
      address: 'First World Hotel, Genting Highlands',
      phone: '', email: '',
      ref: '~RM 60-80 each', refExtra: 'Day pass cheaper than per-ride',
      mapsUrl: 'https://maps.google.com/?q=Skytropolis+Genting',
      notes: 'Gentle indoor rides. Carousel, mini drop tower, kiddie coaster, bumper cars.'
    },
    { id: 'hilltop-ev', cat: 'transport', icon: '⚡', day: 4, name: 'Genting Hilltop <i>EV chargers</i>',
      address: 'Opposite RW Hotel (formerly Highlands Hotel), Genting',
      phone: '', email: '',
      ref: 'CCS2 + Type 2', refExtra: 'Public access · Day 4 charge stop',
      mapsUrl: 'https://maps.google.com/?q=Genting+Hilltop+EV+chargers',
      notes: 'Confirmed by RW Awana. Park, plug in immediately, walk to Skytropolis. 5+ hours at peak = full charge.'
    },
    { id: 'afamosa', cat: 'transport', icon: '⚡', day: 1, name: 'Freeport <i>A\\u0027Famosa</i> Supercharger',
      address: 'Alor Gajah, Melaka',
      phone: '', email: '',
      ref: 'Tesla Supercharger', refExtra: 'Used Day 1 + Day 5',
      mapsUrl: 'https://maps.google.com/?q=Freeport+A\\u0027Famosa+Outlet',
      notes: '~40 min to 80%. Mall available for kids stretch + early lunch on Day 1, coffee on Day 5.'
    },

    // === RESTAURANTS ===
    { id: 'madam-kwan', cat: 'restaurant', icon: '🍽', day: 1, name: 'Madam <i>Kwan\\u0027s</i>',
      address: 'Pavilion KL, Bukit Bintang',
      phone: '+60 3 2148 2240', email: '',
      ref: '', refExtra: 'Day 1 dinner · book 6 pax',
      mapsUrl: 'https://maps.google.com/?q=Madam+Kwan\\u0027s+Pavilion+KL',
      notes: 'Nasi Lemak Tut Tut, Asam Laksa, Nasi Bojari. Beef-free easy. Budget ~RM 250-350 for 6.'
    },
    { id: 'yutkee', cat: 'restaurant', icon: '🍜', day: 2, name: 'Restoran <i>Yut Kee</i>',
      address: '1 Jalan Kamunting, KL',
      phone: '+60 3 2698 8108', email: '',
      ref: '', refExtra: 'Day 2 lunch · cash preferred',
      mapsUrl: 'https://maps.google.com/?q=Restoran+Yut+Kee+Kuala+Lumpur',
      notes: 'Hainanese kopitiam since 1928. Roti babi, chicken chop, kaya toast. Closed Mondays. Tight space.'
    },
    { id: 'loongkee', cat: 'restaurant', icon: '🥘', day: 2, name: '<i>Loong Kee</i> Gohtong Jaya',
      address: 'Gohtong Jaya, Genting Highlands',
      phone: '', email: '',
      ref: '', refExtra: 'Day 2 dinner · walk-in OK',
      mapsUrl: 'https://maps.google.com/?q=Loong+Kee+Restaurant+Gohtong+Jaya',
      notes: '15 min drive down from Awana. Claypot dishes, sambal prawns, kang kong belacan. Budget ~RM 200-300 for 6.'
    },
    { id: 'awana-lodge', cat: 'restaurant', icon: '🍳', day: 3, name: '<i>The Lodge</i> buffet',
      address: 'Resorts World Awana',
      phone: '+60 3 2718 1118', email: '',
      ref: 'RM 35 adult / RM 15 child', refExtra: 'Day 3 breakfast · meal credit RM 18 x 2',
      mapsUrl: 'https://maps.google.com/?q=Resorts+World+Awana',
      notes: 'Awana buffet. Open 6:30-10:30 AM. ~RM 134 out of pocket for 6 after credit.'
    },
    { id: 'gohtong-breakfast', cat: 'restaurant', icon: '☕', day: 4, name: 'Loke Yun · <i>Wan Loi</i> kopitiam',
      address: 'Gohtong Jaya, Genting',
      phone: '', email: '',
      ref: '', refExtra: 'Day 4 breakfast · 4.5-4.6★',
      mapsUrl: 'https://maps.google.com/?q=Restoran+Loke+Yun+Gohtong+Jaya',
      notes: '15 min drive down. Kopi-O, kaya toast, wan tan mee, fish ball noodles. Cash-friendly. Budget ~RM 100-150 for 6.'
    },
    { id: 'sangong', cat: 'restaurant', icon: '🍲', day: 4, name: '<i>Sangong</i> Charcoal Hot Pot',
      address: 'Gohtong Jaya, Genting',
      phone: '', email: '',
      ref: '', refExtra: 'Day 4 lunch · walk-in OK',
      mapsUrl: 'https://maps.google.com/?q=Sangong+Charcoal+Hot+Pot+Gohtong+Jaya',
      notes: 'Mongolian charcoal hot pot. Half-half spicy/clear. Budget ~RM 350-500 for 6.'
    },
    { id: 'genting-palace', cat: 'restaurant', icon: '🥢', day: 4, name: '<i>Genting Palace</i> at Crockfords',
      address: 'Crockfords, Genting (top)',
      phone: '+60 3 2718 1118', email: '',
      ref: 'Per portion = per dish to share', refExtra: 'Day 4 dinner · reservation essential',
      mapsUrl: 'https://maps.google.com/?q=Crockfords+Genting',
      notes: 'Premium Cantonese. Order 5-6 dishes for 6 pax. Budget ~RM 600-900. Beef-free easy. Call concierge first day to reserve.'
    },
    { id: 'yongpeng-noodles', cat: 'restaurant', icon: '🍜', day: 5, name: 'Yong Peng <i>noodles</i>',
      address: 'Yong Peng town, Johor',
      phone: '', email: '',
      ref: '', refExtra: 'Day 5 breakfast en route · 4.5-4.6★',
      mapsUrl: 'https://maps.google.com/?q=Yong+Peng+wan+tan+mee',
      notes: 'Tian Tian Lai Wan Tan Mee (4.6★) or Restoran Lai Lai (4.5★). Famous Chinese kuey teow, chicken noodles, fish ball.'
    },
  ];

  const STORAGE_QR = 'kl-trip-place-qrs-2026';
  let savedQRs = {};
  try { savedQRs = JSON.parse(localStorage.getItem(STORAGE_QR) || '{}'); } catch(e) {}

  const grid = document.getElementById('placesGrid');
  const tabs = document.getElementById('placesTabs');

  function catLabel(cat) {
    return { hotel:'Hotel', restaurant:'Restaurant', attraction:'Attraction', transport:'Transport' }[cat] || cat;
  }
  function dayLabel(d) {
    return { 0:'Pre-trip', 1:'Day 1', 2:'Day 2', 3:'Day 3', 4:'Day 4', 5:'Day 5' }[d] || ('Day ' + d);
  }

  function renderPlaces(filter) {
    let list = PLACES.slice();
    if (filter !== 'all') {
      if (filter.startsWith('day')) {
        const d = parseInt(filter.replace('day',''), 10);
        list = list.filter(p => p.day === d);
      } else {
        list = list.filter(p => p.cat === filter);
      }
    }
    list.sort((a,b) => a.day - b.day);

    if (list.length === 0) {
      grid.innerHTML = '<div style="grid-column: 1/-1; padding: 40px 20px; text-align: center; color: var(--mute-2); font-family: var(--display); font-style: italic;">Nothing matches that filter.</div>';
      return;
    }

    grid.innerHTML = list.map(p => {
      const qr = savedQRs[p.id];
      const phoneHTML = p.phone ? `<div class="place-detail"><span class="label">Phone</span><span><a href="tel:${p.phone.replace(/\\s/g,'')}">${p.phone}</a></span></div>` : '';
      const emailHTML = p.email ? `<div class="place-detail"><span class="label">Email</span><span><a href="mailto:${p.email}">${p.email}</a></span></div>` : '';
      const refHTML = p.ref ? `<div class="place-detail"><span class="label">Ref</span><span class="ref">${p.ref}</span></div>` : '';
      const refExtraHTML = p.refExtra ? `<div class="place-detail"><span class="label"></span><span style="font-size:12px;color:var(--mute-2);">${p.refExtra}</span></div>` : '';
      const notesHTML = p.notes ? `<div class="place-detail" style="margin-top:8px;padding-top:8px;border-top:1px dashed var(--line);"><span style="font-size:12px;color:var(--ink-2);font-style:italic;">${p.notes}</span></div>` : '';

      const qrHTML = qr
        ? `<div class="place-qr-area">
            <div class="place-qr-label">QR code / ticket</div>
            <img src="${qr}" class="place-qr-img" data-id="${p.id}" alt="QR" />
            <div class="place-qr-clear" data-id="${p.id}">× Remove</div>
          </div>`
        : '';

      return `
        <div class="place-card ${p.cat}">
          <div class="place-icon-row">
            <span class="place-type"><span class="place-icon">${p.icon}</span>${catLabel(p.cat)}</span>
            <span class="place-day">${dayLabel(p.day)}</span>
          </div>
          <div class="place-name">${p.name}</div>
          <div class="place-detail"><span class="label">Where</span><span>${p.address}</span></div>
          ${phoneHTML}
          ${emailHTML}
          ${refHTML}
          ${refExtraHTML}
          ${notesHTML}
          <div class="place-actions">
            <a href="${p.mapsUrl}" target="_blank">📍 Maps</a>
            ${p.phone ? `<a href="tel:${p.phone.replace(/\\s/g,'')}">📞 Call</a>` : ''}
            <label class="qr-upload-label">
              📷 ${qr ? 'Replace' : 'Add'} QR / ticket
              <input type="file" accept="image/*" data-id="${p.id}" class="qr-upload" />
            </label>
          </div>
        </div>
      `;
    }).join('');

    // Wire up file uploaders
    grid.querySelectorAll('.qr-upload').forEach(inp => {
      inp.addEventListener('change', (e) => {
        const file = e.target.files[0];
        const id = inp.dataset.id;
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => {
          savedQRs[id] = ev.target.result;
          try { localStorage.setItem(STORAGE_QR, JSON.stringify(savedQRs)); } catch(err) {
            alert('Could not save QR — likely too large. Try a smaller image.');
            return;
          }
          renderPlaces(currentFilter);
        };
        reader.readAsDataURL(file);
      });
    });

    grid.querySelectorAll('.place-qr-clear').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.id;
        if (!confirm('Remove this QR code?')) return;
        delete savedQRs[id];
        try { localStorage.setItem(STORAGE_QR, JSON.stringify(savedQRs)); } catch(e){}
        renderPlaces(currentFilter);
      });
    });

    // Fullscreen modal trigger
    grid.querySelectorAll('.place-qr-img').forEach(img => {
      img.addEventListener('click', () => {
        document.getElementById('qrModalImg').src = img.src;
        document.getElementById('qrModal').classList.add('active');
      });
    });
  }

  let currentFilter = 'all';
  tabs.addEventListener('click', (e) => {
    const btn = e.target.closest('.places-tab');
    if (!btn) return;
    tabs.querySelectorAll('.places-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderPlaces(currentFilter);
  });

  // Modal close
  const modal = document.getElementById('qrModal');
  modal.addEventListener('click', () => modal.classList.remove('active'));
  document.getElementById('qrClose').addEventListener('click', () => modal.classList.remove('active'));

  renderPlaces('all');
})();

/* =========================
   EXPENSES tracker
   ========================= */
(function() {
  const STORAGE_EXP = 'kl-trip-expenses-2026';
  const STORAGE_FX = 'kl-trip-fx-2026';

  let expenses = [];
  try { expenses = JSON.parse(localStorage.getItem(STORAGE_EXP) || '[]'); } catch(e) {}

  let fxRate = 3.50;
  try { fxRate = parseFloat(localStorage.getItem(STORAGE_FX) || '3.50'); } catch(e) {}
  document.getElementById('fxRate').value = fxRate.toFixed(2);

  const CAT = {
    food:        { icon: '🍴', label: 'Food' },
    hotel:       { icon: '🏨', label: 'Hotel' },
    attraction:  { icon: '🎡', label: 'Tickets' },
    transport:   { icon: '🚗', label: 'Transport' },
    shopping:    { icon: '🛍', label: 'Shopping' },
    misc:        { icon: '📌', label: 'Misc' },
  };

  function save() {
    try { localStorage.setItem(STORAGE_EXP, JSON.stringify(expenses)); } catch(e) {
      alert('Could not save — localStorage full.');
    }
  }

  function toMYR(amount, currency) {
    return currency === 'SGD' ? amount * fxRate : amount;
  }
  function toSGD(amount, currency) {
    return currency === 'MYR' ? amount / fxRate : amount;
  }

  function fmt(amount) {
    return amount.toLocaleString('en-SG', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  let currentFilter = 'all';

  function renderTotals() {
    const totalMYR = expenses.reduce((s, e) => s + toMYR(e.amount, e.currency), 0);
    const totalSGD = totalMYR / fxRate;
    const byCat = {};
    expenses.forEach(e => {
      const m = toMYR(e.amount, e.currency);
      byCat[e.category] = (byCat[e.category] || 0) + m;
    });
    const foodMYR = byCat.food || 0;
    const attrMYR = byCat.attraction || 0;

    document.getElementById('expTotals').innerHTML = `
      <div class="expense-total-card">
        <div class="label">Trip total</div>
        <div class="amount">RM ${fmt(totalMYR)}</div>
        <div class="amount-sub">≈ SGD ${fmt(totalSGD)}</div>
      </div>
      <div class="expense-total-card">
        <div class="label">Entries</div>
        <div class="amount">${expenses.length}</div>
        <div class="amount-sub">spend items</div>
      </div>
      <div class="expense-total-card">
        <div class="label">Food</div>
        <div class="amount">RM ${fmt(foodMYR)}</div>
        <div class="amount-sub">≈ SGD ${fmt(foodMYR / fxRate)}</div>
      </div>
      <div class="expense-total-card">
        <div class="label">Tickets</div>
        <div class="amount">RM ${fmt(attrMYR)}</div>
        <div class="amount-sub">≈ SGD ${fmt(attrMYR / fxRate)}</div>
      </div>
    `;
  }

  function renderList() {
    const list = document.getElementById('expList');
    let filtered = expenses.slice();
    if (currentFilter !== 'all') {
      const d = parseInt(currentFilter, 10);
      filtered = filtered.filter(e => e.day === d);
    }

    if (filtered.length === 0) {
      list.innerHTML = '<div class="expense-empty">Nothing logged yet. Add your first spend above.</div>';
      return;
    }

    // Group by day
    const byDay = {};
    filtered.forEach(e => { (byDay[e.day] = byDay[e.day] || []).push(e); });

    const dayLabels = { 0:'Pre-trip', 1:'Day 1 · Tue 23 Jun', 2:'Day 2 · Wed 24 Jun', 3:'Day 3 · Thu 25 Jun', 4:'Day 4 · Fri 26 Jun', 5:'Day 5 · Sat 27 Jun' };

    const sortedDays = Object.keys(byDay).map(Number).sort((a,b) => a-b);

    list.innerHTML = sortedDays.map(d => {
      const items = byDay[d];
      const dayTotal = items.reduce((s, e) => s + toMYR(e.amount, e.currency), 0);
      return `
        <div class="expense-day-group">
          <div class="expense-day-header">
            <span>${dayLabels[d]}</span>
            <span class="day-total">RM ${fmt(dayTotal)} · SGD ${fmt(dayTotal / fxRate)}</span>
          </div>
          ${items.map(e => `
            <div class="expense-item">
              <div class="cat-icon">${CAT[e.category]?.icon || '📌'}</div>
              <div class="note">${e.note || '(no note)'}<small>${CAT[e.category]?.label || e.category}</small></div>
              <div class="amount">${e.currency} ${fmt(e.amount)}<small>≈ ${e.currency === 'MYR' ? 'SGD ' + fmt(e.amount/fxRate) : 'RM ' + fmt(e.amount*fxRate)}</small></div>
              <span class="del-btn" data-id="${e.id}" title="Delete">✕</span>
            </div>
          `).join('')}
        </div>
      `;
    }).join('');

    list.querySelectorAll('.del-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        if (!confirm('Delete this entry?')) return;
        const id = btn.dataset.id;
        expenses = expenses.filter(e => e.id !== id);
        save();
        renderTotals();
        renderList();
      });
    });
  }

  function render() {
    renderTotals();
    renderList();
  }

  // Add button
  document.getElementById('expAdd').addEventListener('click', () => {
    const amount = parseFloat(document.getElementById('expAmount').value);
    const currency = document.getElementById('expCurrency').value;
    const day = parseInt(document.getElementById('expDay').value, 10);
    const category = document.getElementById('expCategory').value;
    const note = document.getElementById('expNote').value.trim();

    if (!amount || amount <= 0) { alert('Enter an amount'); return; }

    expenses.push({
      id: Date.now() + '-' + Math.random().toString(36).slice(2, 8),
      amount, currency, day, category, note,
      ts: new Date().toISOString()
    });
    save();
    document.getElementById('expAmount').value = '';
    document.getElementById('expNote').value = '';
    render();
  });

  // Filter
  document.getElementById('expFilter').addEventListener('click', (e) => {
    const btn = e.target.closest('.expense-filter-btn');
    if (!btn) return;
    document.querySelectorAll('.expense-filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.day;
    renderList();
  });

  // FX rate change
  document.getElementById('fxRate').addEventListener('change', (e) => {
    const v = parseFloat(e.target.value);
    if (v > 0) {
      fxRate = v;
      try { localStorage.setItem(STORAGE_FX, String(fxRate)); } catch(err){}
      render();
    }
  });

  // Reset
  document.getElementById('expReset').addEventListener('click', () => {
    if (!confirm('Clear ALL expense entries? This cannot be undone.')) return;
    expenses = [];
    save();
    render();
  });

  // Auto-fill day based on current date
  const todayStr = new Date().toISOString().slice(0,10);
  const dayMap = { '2026-06-23':1, '2026-06-24':2, '2026-06-25':3, '2026-06-26':4, '2026-06-27':5 };
  if (dayMap[todayStr]) {
    document.getElementById('expDay').value = String(dayMap[todayStr]);
  }

  render();
})();
"""

# Insert before the closing </script> tag
old_script_end = '})();\n</script>'
if old_script_end in html:
    html = html.replace(old_script_end, '})();\n' + js_additions + '\n</script>')
    print('OK: JS additions injected')
else:
    print('MISS: script close marker not found')

# Save
with open(p, 'w') as f: f.write(html)
print(f'\\nFinal file size: {len(html)} bytes')
