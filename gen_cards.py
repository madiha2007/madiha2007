import base64
import html

LANG_COLORS = {
    "TypeScript": "#3178C6",
    "JavaScript": "#F1C40F",
    "Java": "#B07219",
    "Python": "#3572A5",
}

def make_card(repo, desc, lang, stars, width=380, height=150):
    lang_color = LANG_COLORS.get(lang, "#7C3AED")
    desc_esc = html.escape(desc) if desc else ""
    repo_esc = html.escape(repo)

    # vertical layout depending on whether description exists
    title_y = 44
    desc_y = 68
    bottom_y = height - 26

    desc_svg = f'<text x="28" y="{desc_y}" font-family="Trebuchet MS, Verdana, sans-serif" font-size="13" fill="#8B5CF6" opacity="0.85">{desc_esc}</text>' if desc else ""

    # 4-point sparkle path helper, centered at (0,0), sized by scale
    def sparkle(cx, cy, s, color, opacity):
        return (f'<g transform="translate({cx},{cy})" opacity="{opacity}">'
                f'<path d="M0 {-10*s} C {1.2*s} {-2*s}, {2*s} {-1.2*s}, {10*s} 0 '
                f'C {2*s} {1.2*s}, {1.2*s} {2*s}, 0 {10*s} '
                f'C {-1.2*s} {2*s}, {-2*s} {1.2*s}, {-10*s} 0 '
                f'C {-2*s} {-1.2*s}, {-1.2*s} {-2*s}, 0 {-10*s} Z" fill="{color}"/></g>')

    # 5-point star path centered at (0,0) with outer radius r
    def star(cx, cy, r, color):
        import math
        pts = []
        for i in range(10):
            ang = math.pi/2 + i * math.pi/5
            rad = r if i % 2 == 0 else r*0.42
            x = cx + rad*math.cos(ang)
            y = cy - rad*math.sin(ang)
            pts.append(f"{x:.1f},{y:.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'

    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8F2FF"/>
      <stop offset="100%" stop-color="#F1E4FF"/>
    </linearGradient>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#C4A6F5" flood-opacity="0.35"/>
    </filter>
  </defs>

  <rect x="6" y="6" width="{width-12}" height="{height-12}" rx="22" fill="url(#bg)" stroke="#D9BBFF" stroke-width="2" filter="url(#soft)"/>

  <!-- sparkle decorations -->
  {sparkle(width-32, 26, 1.0, "#C58AFF", 0.8)}
  {sparkle(width-20, 44, 0.55, "#E0AFFF", 0.6)}
  {sparkle(24, height-18, 0.6, "#D9BBFF", 0.55)}

  <!-- folder icon -->
  <g transform="translate(26,24)">
    <path d="M0 4 C0 1.8 1.8 0 4 0 H12 L16 5 H30 C32.2 5 34 6.8 34 9 V22 C34 24.2 32.2 26 30 26 H4 C1.8 26 0 24.2 0 22 Z"
          fill="#B57BFF" opacity="0.9"/>
  </g>

  <text x="70" y="{title_y}" font-family="Trebuchet MS, Verdana, sans-serif" font-size="19" font-weight="bold" fill="#6B21A8">{repo_esc}</text>

  {desc_svg}

  <circle cx="30" cy="{bottom_y}" r="6" fill="{lang_color}"/>
  <text x="42" y="{bottom_y+4}" font-family="Trebuchet MS, Verdana, sans-serif" font-size="13" fill="#5B21B6">{lang}</text>

  {star(width-62, bottom_y-3, 8, "#F5B301")}
  <text x="{width-48}" y="{bottom_y+4}" font-family="Trebuchet MS, Verdana, sans-serif" font-size="13" fill="#5B21B6">{stars}</text>
</svg>'''
    return svg


cards = [
    ("Daily-Planner", "", "TypeScript", 1),
    ("ott_website", "Ott (Netflix) respository", "JavaScript", 1),
    ("wdig-cg", "", "TypeScript", 1),
    ("dua_app", "", "TypeScript", 1),
]

data_uris = {}
for repo, desc, lang, stars in cards:
    svg = make_card(repo, desc, lang, stars)
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    data_uris[repo] = f"data:image/svg+xml;base64,{b64}"
    with open(f"svg/{repo}.svg", "w", encoding="utf-8") as f:
        f.write(svg)

with open("svg/data_uris.txt", "w", encoding="utf-8") as f:
    for repo, uri in data_uris.items():
        f.write(f"{repo}\n{uri}\n\n")

print("done")