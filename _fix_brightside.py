p = '/Users/yiqin/Desktop/Claude Code Projects/yqweb/demos/brightside/index.html'
with open(p) as f: html = f.read()

# Hero: replace male teacher (8617763) with best-guess female teacher candidate
# Best guess: 8617772 (middle of the Asian-education photoshoot series, likely a different model)
old_hero = "background-image: url('https://images.pexels.com/photos/8617763/pexels-photo-8617763.jpeg?auto=compress&cs=tinysrgb&w=1000');"
new_hero = "background-image: url('https://images.pexels.com/photos/8617772/pexels-photo-8617772.jpeg?auto=compress&cs=tinysrgb&w=1000');"
if old_hero in html:
    html = html.replace(old_hero, new_hero)
    print('OK: hero photo swapped 8617763 → 8617772 (best-guess female teacher)')
else:
    print('MISS: hero photo')

# Visit: replace Western lecture hall (Unsplash 1606761568499) with classroom candidate
# Best guess: 8617790 (end of the Asian-education series, likely a classroom shot)
old_visit = "background-image: url('https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=1200&q=85');"
new_visit = "background-image: url('https://images.pexels.com/photos/8617790/pexels-photo-8617790.jpeg?auto=compress&cs=tinysrgb&w=1200');"
if old_visit in html:
    html = html.replace(old_visit, new_visit)
    print('OK: visit photo swapped 1606761568499 → 8617790 (best-guess small classroom)')
else:
    print('MISS: visit photo')

with open(p, 'w') as f: f.write(html)
print(f'\nFile size: {len(html)}')
