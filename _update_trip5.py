import re

p = '/Users/yiqin/Desktop/Claude Code Projects/yqweb/trip-kl-genting-2026/index.html'
with open(p) as f: html = f.read()

changes = []

def replace_block(old, new, label):
    global html
    if old in html:
        html = html.replace(old, new)
        changes.append(f'OK: {label}')
    else:
        changes.append(f'MISS: {label}')

# =================================================================
# DAY 2 — Revert to LIGHT ARRIVAL DAY
# (was the PEAK DAY in the last restructure)
# =================================================================
# We'll replace the entire current Day 2 section
old_day2 = '''<!-- ============================================
     DAY 2 — Wed 24 Jun  · PEAK DAY (cable car + theme park)
     ============================================ -->
<section class="block">
  <div class="container">
    <span class="section-eyebrow">— Day 02 / KL to the peak</span>
    <h2 class="display section-h2">Up to <i>SkyWorlds</i>.</h2>'''
# Use regex to find the entire Day 2 block until end
m = re.search(r'<!-- ============================================\s*\n\s*DAY 2 — Wed 24 Jun.*?</section>', html, re.DOTALL)
if m:
    new_day2 = '''<!-- ============================================
     DAY 2 — Wed 24 Jun  · LIGHT ARRIVAL (settle at Awana)
     ============================================ -->
<section class="block">
  <div class="container">
    <span class="section-eyebrow">— Day 02 / Climb into cool air</span>
    <h2 class="display section-h2">KL morning, <i>Awana</i> afternoon.</h2>
    <p class="section-lead">Light KL morning, climb up to cool air by mid-afternoon. Settle at Awana, rest by the pool, dinner down at Gohtong Jaya. Tomorrow is the big theme-park day.</p>

    <article class="day">
      <div class="day-head">
        <div>
          <div class="day-num">Day 2 <span class="date">Wed, 24 June</span></div>
          <h3 class="day-title display">From hot KL to <i>cool hills</i></h3>
        </div>
        <span class="day-badge">≈ 50 km</span>
      </div>

      <ol class="timeline">
        <li class="timeline-item">
          <span class="timeline-time">7:30<span class="meridiem">am</span></span>
          <div class="timeline-body">
            <strong>Hilton breakfast</strong>
            <p>Honors breakfast may be included — confirm at check-in. Strong coffee for parents, pancakes for kids. Don\u0027t linger past 9 AM.</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">9:30<span class="meridiem">am</span></span>
          <div class="timeline-body">
            <strong>Check out, bags to concierge</strong>
            <p>Standard checkout 12 noon — checking out now frees up the morning. Leave luggage with concierge, walk to KLCC area (10 min).</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">10:00<span class="meridiem">am</span></span>
          <div class="timeline-body">
            <strong>Aquaria KLCC <span class="timeline-pin kid">kid favourite</span></strong>
            <p>Right at opening time — quieter. Underground aquarium beneath KLCC. 90 minutes is enough. Parents can sit while kids ogle stingrays in the tunnel.</p>
            <a href="https://maps.google.com/?q=Aquaria+KLCC" class="maplink" target="_blank">Open in Maps ↗</a>
            <div class="meta">
              <span><b>Tickets:</b> ~RM 75 adult / RM 65 child (book online for 10% off)</span>
            </div>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">11:30<span class="meridiem">am</span></span>
          <div class="timeline-body">
            <strong>Lunch: <i>Restoran Yut Kee</i> <span class="timeline-pin">early lunch</span></strong>
            <p>Hainanese-Malaysian kopitiam since 1928. Roti babi, Hainanese chicken chop, kaya toast. Iconic. <b>Going at 11:30 avoids the lunch rush</b> — tight space, but easier seating for 6 pax. Cash preferred.</p>
            <a href="https://maps.google.com/?q=Restoran+Yut+Kee+Kuala+Lumpur" class="maplink" target="_blank">Open in Maps ↗</a>
            <div class="meta">
              <span><b>Budget:</b> ~RM 150 for 6 pax</span>
              <span><b>Beef-free:</b> yes</span>
            </div>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">1:00<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Pick up car from Hilton, drive to Awana <span class="timeline-pin warn">winding road</span></strong>
            <p>~50 km via Karak Highway. 1 hour at sensible pace. The climb is twisty — kids prone to carsickness should sit front-passenger or take Bonamine 30 min before.</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">2:00<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Check in: Resorts World Awana <span class="timeline-pin parents">early check-in</span></strong>
            <p>Mid-station, cool 18–22°C. Both Superior Deluxe rooms, 2 Queen beds each. <b>Early check-in request sent ~1 week before</b> (see "Before the Trip"). If rooms ready: settle by 2:30 PM. If not: bags to bellman, late lunch at hotel cafe.</p>
            <a href="https://maps.google.com/?q=Resorts+World+Awana,+Genting+Highlands" class="maplink" target="_blank">Open in Maps ↗</a>
            <div class="meta">
              <span><b>Ref:</b> EL0000100460</span>
              <span><b>Pkg:</b> Mid-Year Hotel Escape</span>
            </div>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">3:00<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Awana afternoon: pool, walk, settle <span class="timeline-pin kid">easy</span></strong>
            <p>Awana has a heated outdoor pool — perfect at 20°C. Kids in the water, parents in cafe chairs reading. Or walk the resort grounds and viewpoints. <b>No cable car today</b> — save the round-trip for tomorrow when you have the rest base.</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">6:30<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Dinner: <i>Loong Kee</i> Gohtong Jaya</strong>
            <p>Local Chinese tze char at the foot of the mountain — 15 min drive down from Awana. Generous portions, no-frills authentic. Parents will appreciate proper hawker-style Chinese over resort food. Order claypot dishes, sambal prawns, kang kong belacan, fried tofu.</p>
            <a href="https://maps.google.com/?q=Loong+Kee+Restaurant+Gohtong+Jaya" class="maplink" target="_blank">Open in Maps ↗</a>
            <div class="meta">
              <span><b>Drive:</b> 15 min down from Awana</span>
              <span><b>Budget:</b> ~RM 200–300 for 6</span>
            </div>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">8:30<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Back to Awana, sleep <span class="timeline-pin parents">rest up</span></strong>
            <p>Tomorrow is the big theme-park day. Make sure phones are charged, theme-park tickets ready (Klook QR in the new Tickets section), Tesla parked, kids in bed by 10.</p>
          </div>
        </li>
      </ol>

      <div class="day-aside">
        <strong>Save the cable car for tomorrow</strong>
        Your one round-trip cable car ticket is best used Day 3 — up in the morning, down at night. Today is the Awana day. If anyone really wants a peek at the peak, you can grab a single-trip ticket (~RM 8/pax) for a 30-min there-and-back, but it\u0027s honestly not worth it before tomorrow\u0027s full day.
      </div>
    </article>
  </div>
</section>'''
    html = html[:m.start()] + new_day2 + html[m.end():]
    changes.append('OK: Day 2 (LIGHT ARRIVAL DAY restructure)')
else:
    changes.append('MISS: Day 2 block not found')

# =================================================================
# DAY 3 — restructure to FULL THEME PARK DAY with First World rest base
# =================================================================
m = re.search(r'<!-- ============================================\s*\n\s*DAY 3 — Thu 25 Jun.*?</section>', html, re.DOTALL)
if m:
    new_day3 = '''<!-- ============================================
     DAY 3 — Thu 25 Jun  · FULL THEME PARK DAY (cable car + First World rest base)
     ============================================ -->
<section class="block">
  <div class="container">
    <span class="section-eyebrow">— Day 03 / Theme park day</span>
    <h2 class="display section-h2">SkyWorlds, <i>full send.</i></h2>
    <p class="section-lead">The big one. Cable car up, full day at SkyWorlds, First World room (booking 10693538AL) as the daytime rest base. Cable car down after dinner at peak.</p>

    <article class="day day-genting">
      <div class="day-head">
        <div>
          <div class="day-num">Day 3 <span class="date">Thu, 25 June</span></div>
          <h3 class="day-title display">Rollercoasters <i>&amp; rest</i></h3>
        </div>
        <span class="day-badge">Theme park</span>
      </div>

      <ol class="timeline">
        <li class="timeline-item">
          <span class="timeline-time">8:00<span class="meridiem">am</span></span>
          <div class="timeline-body">
            <strong>Breakfast at The Lodge <span class="timeline-pin">use meal credit</span></strong>
            <p>The Awana buffet. Your booking includes RM 18 × 2 meal credit. Rates: RM 35 adult / RM 15 child. ~RM 134 out of pocket for 4 adults + 2 kids after credit. Fuel up — long day ahead.</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">9:30<span class="meridiem">am</span></span>
          <div class="timeline-body">
            <strong>Awana SkyWay cable car UP <span class="timeline-pin kid">round-trip starts</span></strong>
            <p>10–15 min ride. Glass-bottomed gondolas optional. Skip Chin Swee stop (Day 4). <b>This is your ONE round-trip cable car for the trip</b> — return portion gets used tonight after dinner. Pack a <b>day-bag</b> (change of clothes, kids meds, water, snacks).</p>
            <div class="meta">
              <span><b>Fare:</b> ~RM 10–15 round trip per person</span>
              <span><b>Pack:</b> day-bag only, leave main luggage at Awana</span>
            </div>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">10:00<span class="meridiem">am</span></span>
          <div class="timeline-body">
            <strong>SkyAvenue → SkyWorlds entry <span class="timeline-pin warn">check weather</span></strong>
            <p>Theme park typically opens 11 AM weekday. Use the 30-45 min before opening to find the park entrance, queue early for the popular rides. <b>Check the Genting app the night before</b> — outdoor rides close in heavy fog or rain. If forecast is bad, swap Day 3 with Day 4 plan (Chin Swee + Skytropolis).</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">11:00<span class="meridiem">am</span></span>
          <div class="timeline-body">
            <strong>Genting SkyWorlds — morning session <span class="timeline-pin kid">main event</span></strong>
            <p>Malaysia\u0027s newest outdoor theme park. Charlotte (8) may be under the 130 cm bar for the wildest coasters — Nicholas (11) should clear most. Hit the headliners first while queues are short. Meeting point + a "grandparents\u0027 shaded bench" at central plaza.</p>
            <div class="meta">
              <span><b>Tickets:</b> ~RM 200 adult, RM 170 child (book online, sometimes 20% off)</span>
            </div>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">12:30<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Lunch inside the park</strong>
            <p>Food courts and themed restaurants throughout. Eating off-peak (1:30 PM onwards) skips queues. Park food is meh but convenient — saves the energy of leaving and re-entering.</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">2:00<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Check in <i>First World</i>, rest at the room <span class="timeline-pin parents">use the booking</span></strong>
            <p>Walk from SkyWorlds to First World Hotel (2 min, right next door). Check in to booking <b>10693538AL</b> under Hui Shan\u0027s name. <b>Ask reception for late checkout to 3 PM tomorrow</b> when you check in — extends the room\u0027s usefulness. Parents nap, kids can chill or watch TV. You finally sit.</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">4:00<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>SkyWorlds — afternoon session <span class="timeline-pin kid">round 2</span></strong>
            <p>Back to the park for the rides you missed. Parents can stay at First World if they\u0027re done for the day. The remaining 2.5 hours is plenty to clear the kid-friendly rides Charlotte couldn\u0027t do in the morning rush.</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">6:30<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Park closes, collect parents from First World</strong>
            <p>Pick up day-bag, regroup with the grandparents. Walk to SkyAvenue for dinner.</p>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">7:00<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Dinner at SkyAvenue (peak)</strong>
            <p>Quick eat after a long day. <b>Sushi Zanmai</b> for kids (lots of non-beef options), <b>Imperial Rama</b> for Thai. Not the special dinner of the trip — that\u0027s tomorrow at Genting Palace.</p>
            <div class="meta">
              <span><b>Budget:</b> ~RM 250–350 for 6</span>
            </div>
          </div>
        </li>

        <li class="timeline-item">
          <span class="timeline-time">8:30<span class="meridiem">pm</span></span>
          <div class="timeline-body">
            <strong>Cable car DOWN <span class="timeline-pin kid">round-trip complete</span></strong>
            <p>Last ride down at ~11 PM but no point staying that late — everyone\u0027s exhausted. Cable car back to Awana, sleep. Tomorrow is the slower drive-up day.</p>
          </div>
        </li>
      </ol>

      <div class="day-aside">
        <strong>First World note — daytime use only</strong>
        Per Option Z, the First World room is daytime-only — no one sleeps there tonight. The overnight portion of booking 10693538AL goes unused (~SGD 33 already paid). That\u0027s a deliberate trade-off: simpler logistics, everyone sleeps at Awana, no rollaway or split family. The room\u0027s real value is the 2-4 PM rest break for grandparents during the theme-park grind.
      </div>
    </article>
  </div>
</section>'''
    html = html[:m.start()] + new_day3 + html[m.end():]
    changes.append('OK: Day 3 (THEME PARK DAY restructure)')
else:
    changes.append('MISS: Day 3 block not found')

# =================================================================
# DAY 4 — keep as DRIVE UP DAY (small tweaks only)
# Day 4 was set up correctly already; just verify it's clean
# =================================================================
# Day 4 was already restructured as DRIVE UP DAY in the previous edit.
# No changes needed.
changes.append('SKIP: Day 4 unchanged (already DRIVE UP DAY)')

# =================================================================
# Update First World hotel card in Hotels section
# - Was booking 10693258AL (24-25, wrong dates)
# - Now booking 10693538AL (25-26, correct dates)
# =================================================================
old_hotel_card = '''      <div class="info-card">
        <div class="info-card-label">Night 2 (rest base) · 24 Jun</div>
        <h3 class="display">First World <i>Hotel</i></h3>
        <div class="rows">
          <div class="row"><span>Check-in</span><b>Wed 24 Jun</b></div>
          <div class="row"><span>Check-out</span><b>Thu 25 Jun, noon</b></div>
          <div class="row"><span>Use as</span><b>Rest base · top of mountain</b></div>
          <div class="row"><span>Why</span><b>Right next to SkyWorlds</b></div>
          <div class="row"><span>Booking #</span><b class="mono">10693258AL</b></div>
          <div class="row"><span>Member #</span><b class="mono">1218997403</b></div>
          <div class="row"><span>Booked by</span><b>Hui Shan</b></div>
          <div class="row"><span>Total</span><b>SGD 32.87</b></div>
        </div>
        <div class="actions">
          <a href="https://maps.google.com/?q=First+World+Hotel+Genting" target="_blank">Maps</a>
        </div>
      </div>'''

new_hotel_card = '''      <div class="info-card">
        <div class="info-card-label">Day 3 rest base · 25 Jun</div>
        <h3 class="display">First World <i>Hotel</i></h3>
        <div class="rows">
          <div class="row"><span>Check-in</span><b>Thu 25 Jun, 3 PM</b></div>
          <div class="row"><span>Check-out</span><b>Fri 26 Jun, noon</b></div>
          <div class="row"><span>Use as</span><b>Day 3 rest base (theme park day)</b></div>
          <div class="row"><span>Why</span><b>Right next to SkyWorlds</b></div>
          <div class="row"><span>Booking #</span><b class="mono">10693538AL</b></div>
          <div class="row"><span>Member #</span><b class="mono">1218997403</b></div>
          <div class="row"><span>Booked by</span><b>Hui Shan (S8779658B)</b></div>
          <div class="row"><span>Total</span><b>SGD 32.87</b></div>
        </div>
        <div class="actions">
          <a href="https://maps.google.com/?q=First+World+Hotel+Genting" target="_blank">Maps</a>
        </div>
      </div>'''

replace_block(old_hotel_card, new_hotel_card, 'First World hotel card → new booking 10693538AL (25-26)')

# =================================================================
# Food list — re-tag for new day assignments
# Day 2 dinner = Loong Kee (was Day 3 lunch)
# =================================================================
html = html.replace(
    '<h4 class="display">Loong Kee Gohtong Jaya</h4>\n          <span class="food-tag must">Day 3 lunch</span>',
    '<h4 class="display">Loong Kee Gohtong Jaya</h4>\n          <span class="food-tag must">Day 2 dinner</span>'
)
changes.append('OK: Loong Kee re-tagged Day 2 dinner')

# Mushroom Farm — note it's not in the current plan
html = html.replace(
    '<h4 class="display">Mushroom Farm Restaurant 香菇园饭店</h4>\n          <span class="food-tag must">Day 3 dinner</span>',
    '<h4 class="display">Mushroom Farm Restaurant 香菇园饭店</h4>\n          <span class="food-tag">Optional swap</span>'
)
changes.append('OK: Mushroom Farm tagged as optional swap')

# Save
with open(p, 'w') as f: f.write(html)
print(f'\\nFile size: {len(html)} bytes\\n\\nChanges:')
for c in changes: print(f'  {c}')
