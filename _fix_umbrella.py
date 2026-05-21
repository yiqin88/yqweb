import re

p = '/Users/yiqin/Desktop/Claude Code Projects/yqweb/index.html'
with open(p) as f: html = f.read()

# ============================================================
# Fix 1: Remove the alignment-jumping span-2 rule at 1100px+
# ============================================================
old_grid = '''@media (min-width: 1100px) {
  .demo-grid { grid-template-columns: repeat(2, 1fr); }
  .demo-grid .demo:first-child { grid-row: span 2; }
}'''
new_grid = '''@media (min-width: 1100px) {
  .demo-grid { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 1fr; }
}'''
if old_grid in html:
    html = html.replace(old_grid, new_grid)
    print('OK: alignment-jump rule removed (now uniform 2x2)')
else:
    print('SKIP: grid rule not found verbatim')

# ============================================================
# Fix 2: Add excitement CSS — animated sheen, pulsing live dot, stronger hover
# ============================================================
# Insert excitement styles right before the existing /* ---------- Process ---------- */ comment
excitement_css = '''
/* ---------- Demo card excitement ---------- */
.demo {
  transition: transform .45s cubic-bezier(.2,.7,.2,1), box-shadow .45s ease, border-color .3s;
  position: relative;
}
.demo:hover {
  transform: translateY(-8px);
  box-shadow: 0 28px 60px -18px rgba(21,19,15,0.22), 0 4px 12px rgba(21,19,15,0.06);
  border-color: rgba(21,19,15,0.20);
}
.demo-visual { transition: transform .6s cubic-bezier(.2,.7,.2,1); }
.demo:hover .demo-visual { transform: scale(1.02); }

/* Animated diagonal sheen across the visual */
.demo-visual {
  position: relative;
}
.demo-visual .demo-sheen {
  position: absolute;
  top: -50%; left: -60%;
  width: 70%; height: 200%;
  background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,0.10) 50%, transparent 70%);
  transform: translateX(-20%) skewX(-12deg);
  transition: transform 1s cubic-bezier(.4,0,.2,1);
  pointer-events: none;
  z-index: 1;
}
.demo:hover .demo-visual .demo-sheen {
  transform: translateX(280%) skewX(-12deg);
}

/* Live indicator pill — pulses in top-right of every demo-visual */
.demo-live {
  position: absolute;
  top: 18px; right: 18px;
  z-index: 3;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 11px 5px 9px;
  background: rgba(255,255,255,0.10);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 100px;
  font-family: var(--sans);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-weight: 700;
  color: rgba(255,255,255,0.92);
}
.demo-live::before {
  content: '';
  width: 7px; height: 7px;
  background: #4ADE80;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(74,222,128,0.30);
  animation: livePulse 2.2s ease-in-out infinite;
}
@keyframes livePulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(74,222,128,0.30); }
  50%      { box-shadow: 0 0 0 7px rgba(74,222,128,0.04); }
}

/* Floating decorative orb in each visual for depth */
.demo-visual .demo-orb {
  position: absolute;
  width: 220px; height: 220px;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.35;
  pointer-events: none;
  z-index: 0;
  animation: drift 14s ease-in-out infinite alternate;
}
@keyframes drift {
  from { transform: translate(0, 0); }
  to   { transform: translate(-40px, 30px); }
}

/* Demo-mark gets a subtle inner glow */
.demo-mark {
  position: relative;
  z-index: 2;
  text-shadow: 0 0 60px rgba(255,255,255,0.10);
}

'''
marker = '/* ---------- Process ---------- */'
if marker in html:
    html = html.replace(marker, excitement_css + marker)
    print('OK: excitement CSS inserted')
else:
    print('SKIP: process marker not found')

# ============================================================
# Fix 3: Change "order." to "Photos Order." + add LIVE pills + orbs to all 4 cards
# ============================================================
# Card 1: order portal — change demo-mark, add live pill + orb
old1 = '''        <div class="demo-visual real">
          <div class="demo-mark">order<i>.</i></div>
        </div>'''
new1 = '''        <div class="demo-visual real">
          <div class="demo-sheen"></div>
          <div class="demo-orb" style="background:#FF6A3D; top:-30px; right:-30px;"></div>
          <div class="demo-live">Live · 600+ orders</div>
          <div class="demo-mark">Photos<i> Order</i></div>
        </div>'''
if old1 in html: html = html.replace(old1, new1); print('OK: card 1 (order) updated → Photos Order')
else: print('MISS: card 1')

# Card 2: Slow Hours
old2 = '''        <div class="demo-visual" style="background:linear-gradient(135deg,#3D2B1F,#271B14); color:#F4ECDE;">
          <div class="demo-mark display" style="color:#C76443;">Slow<i> Hours</i></div>
        </div>'''
new2 = '''        <div class="demo-visual" style="background:linear-gradient(135deg,#3D2B1F,#271B14); color:#F4ECDE;">
          <div class="demo-sheen"></div>
          <div class="demo-orb" style="background:#C76443; top:-40px; left:-20px;"></div>
          <div class="demo-live">Demo · Live booking</div>
          <div class="demo-mark display" style="color:#C76443;">Slow<i> Hours</i></div>
        </div>'''
if old2 in html: html = html.replace(old2, new2); print('OK: card 2 (Slow Hours) updated')
else: print('MISS: card 2')

# Card 3: Northwind
old3 = '''        <div class="demo-visual" style="background:linear-gradient(135deg,#0A1628,#1E2A3F); color:#E8F1FB;">
          <div class="demo-mark display" style="color:#00A8C8;">North<i>wind</i></div>
        </div>'''
new3 = '''        <div class="demo-visual" style="background:linear-gradient(135deg,#0A1628,#1E2A3F); color:#E8F1FB;">
          <div class="demo-sheen"></div>
          <div class="demo-orb" style="background:#00A8C8; bottom:-30px; right:-30px;"></div>
          <div class="demo-live">Demo · Photo quote</div>
          <div class="demo-mark display" style="color:#00A8C8;">North<i>wind</i></div>
        </div>'''
if old3 in html: html = html.replace(old3, new3); print('OK: card 3 (Northwind) updated')
else: print('MISS: card 3')

# Card 4: Brightside
old4 = '''        <div class="demo-visual" style="background:linear-gradient(135deg,#1F2D27,#2D6A4F); color:#F5F0E1;">
          <div class="demo-mark display" style="color:#E9C46A;">Bright<i>side</i></div>
        </div>'''
new4 = '''        <div class="demo-visual" style="background:linear-gradient(135deg,#1F2D27,#2D6A4F); color:#F5F0E1;">
          <div class="demo-sheen"></div>
          <div class="demo-orb" style="background:#E9C46A; top:-20px; right:-40px;"></div>
          <div class="demo-live">Demo · Trial booking</div>
          <div class="demo-mark display" style="color:#E9C46A;">Bright<i>side</i></div>
        </div>'''
if old4 in html: html = html.replace(old4, new4); print('OK: card 4 (Brightside) updated')
else: print('MISS: card 4')

with open(p, 'w') as f: f.write(html)
print(f'\nFinal file size: {len(html)} bytes')
