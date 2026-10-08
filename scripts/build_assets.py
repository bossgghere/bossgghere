#!/usr/bin/env python3
"""Generates the bento-card SVGs in ./assets (dark + light variants).

Run:  python3 scripts/build_assets.py
Edit the CONTENT section to change text; the look lives in THEMES / card().
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'SF Mono',ui-monospace,Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(card="#14141C", stroke="#FFFFFF", stroke_op=".08", text="#F5F5F7",
                 sub="#9A9AA8", faint="#5E5E6E", a1="#6366F1", a2="#A78BFA", glow_op=".28",
                 chip="#FFFFFF", chip_op=".06"),
    "light": dict(card="#F5F5F7", stroke="#000000", stroke_op=".08", text="#1D1D1F",
                  sub="#6E6E73", faint="#A1A1A6", a1="#5558E6", a2="#8B5CF6", glow_op=".16",
                  chip="#000000", chip_op=".05"),
}


def card(w, h, t, body, glow=(0.85, 0.0), uid="c"):
    """Rounded card with a soft accent glow. glow = (x, y) as fraction of the card."""
    gx, gy = glow
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" font-family="{FONT}">
<defs>
  <radialGradient id="{uid}g" cx="{gx}" cy="{gy}" r="0.75">
    <stop offset="0" stop-color="{t['a1']}" stop-opacity="{t['glow_op']}"/>
    <stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="{uid}t" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/>
  </linearGradient>
  <clipPath id="{uid}k"><rect width="{w}" height="{h}" rx="26"/></clipPath>
</defs>
<style>
  .pulse{{animation:p 2.4s ease-in-out infinite}}
  @keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
  .drift{{animation:d 9s ease-in-out infinite alternate}}
  @keyframes d{{from{{transform:translateX(0)}}to{{transform:translateX(-24px)}}}}
</style>
<rect width="{w}" height="{h}" rx="26" fill="{t['card']}"/>
<g clip-path="url(#{uid}k)"><rect class="drift" x="-30" width="{w+60}" height="{h}" fill="url(#{uid}g)"/></g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="25.5" stroke="{t['stroke']}" stroke-opacity="{t['stroke_op']}"/>
{body}
</svg>
"""


def write(name, theme, svg):
    (OUT / f"{name}-{theme}.svg").write_text(svg)


# ---------------------------------------------------------------- CONTENT
def hero(t):
    body = f"""
<g class="pulse"><circle cx="52" cy="58" r="5" fill="#22C55E"/></g>
<text x="68" y="63" font-size="14" font-weight="500" fill="{t['sub']}">Open to freelance &amp; full-time</text>
<text x="48" y="160" font-size="68" font-weight="700" letter-spacing="-2" fill="{t['text']}">Gourav Raut</text>
<text x="50" y="205" font-size="24" font-weight="500" fill="url(#ht)">Full-stack engineer.</text>
<text x="50" y="238" font-size="20" fill="{t['sub']}">I build and ship production apps — mobile, backend, AI.</text>
"""
    return card(830, 280, t, body, glow=(0.9, 0.0), uid="h")


def metric(big, small, t, uid):
    body = f"""
<text x="32" y="86" font-size="58" font-weight="700" letter-spacing="-2" fill="url(#{uid}t)">{big}</text>
<text x="34" y="122" font-size="16" fill="{t['sub']}">{small}</text>
"""
    return card(270, 150, t, body, glow=(0.9, 0.0), uid=uid)


def journey(t):
    items = [
        ("Oct 2026 — now", "Algo Chowk", ["AlgoTrade · FastAPI,", "LangGraph, Gemini"], True),
        ("Jun 2025 — Oct 2026", "SUAS Enterprises", ["Skippr · React Native,", "Supabase, AWS"], False),
        ("Nov 2025 — Apr 2026", "Mandin Studios", ["2 apps · Flutter,", "Node.js, Django"], False),
        ("Aug — Nov 2025", "VOIX Digital", ["SnapLay · Flutter,", "Node.js, AWS"], False),
        ("May — Jul 2025", "Cloud InfraTech", ["EduLink · Flutter,", "MERN"], False),
    ]
    col = 160
    parts = [f'<text x="32" y="46" font-size="13" font-weight="600" letter-spacing="1.5" fill="{t["faint"]}">EXPERIENCE</text>',
             f'<line x1="40" y1="84" x2="{40 + col*4}" y2="84" stroke="{t["stroke"]}" stroke-opacity=".14"/>']
    for i, (when, who, what, now) in enumerate(items):
        x = 40 + i * col
        fill = t["a1"] if now else t["faint"]
        parts.append(f'<circle cx="{x}" cy="84" r="5" fill="{fill}"/>')
        if now:
            parts.append(f'<circle class="pulse" cx="{x}" cy="84" r="9" stroke="{t["a1"]}" stroke-opacity=".5"/>')
        parts.append(f'<text x="{x-5}" y="116" font-size="12" font-family="{MONO}" fill="{t["sub"]}">{when}</text>')
        parts.append(f'<text x="{x-5}" y="142" font-size="16" font-weight="600" fill="{t["text"]}">{who}</text>')
        for j, ln in enumerate(what):
            parts.append(f'<text x="{x-5}" y="{164 + j*18}" font-size="13" fill="{t["sub"]}">{ln}</text>')
    return card(830, 205, t, "\n".join(parts), glow=(0.1, 1.0), uid="j")


def project(tag, title, lines, stack, t, uid):
    desc = "\n".join(
        f'<text x="32" y="{108 + i*22}" font-size="15" fill="{t["sub"]}">{ln}</text>' for i, ln in enumerate(lines))
    body = f"""
<text x="32" y="44" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t['faint']}">{tag}</text>
<text x="32" y="82" font-size="26" font-weight="700" letter-spacing="-.5" fill="{t['text']}">{title}</text>
{desc}
<text x="32" y="188" font-size="12" font-family="{MONO}" fill="{t['faint']}">{stack}</text>
<text x="368" y="44" font-size="22" text-anchor="end" fill="url(#{uid}t)">↗</text>
"""
    return card(405, 215, t, body, glow=(0.95, 0.0), uid=uid)


def stack(t):
    rows = [
        ("Mobile", "Flutter · React Native · Expo"),
        ("Backend", "Node.js · Django · PostgreSQL · Supabase · Prisma"),
        ("AI &amp; Web3", "LangGraph · Gemini · n8n · Solidity"),
        ("Cloud", "AWS · Cloudflare · Vercel · Nginx"),
    ]
    parts = [f'<text x="32" y="46" font-size="13" font-weight="600" letter-spacing="1.5" fill="{t["faint"]}">STACK</text>']
    for i, (k, v) in enumerate(rows):
        y = 84 + i * 30
        parts.append(f'<text x="32" y="{y}" font-size="15" font-weight="600" fill="{t["text"]}">{k}</text>')
        parts.append(f'<text x="160" y="{y}" font-size="15" fill="{t["sub"]}">{v}</text>')
    return card(830, 200, t, "\n".join(parts), glow=(0.95, 1.0), uid="s")


def studio(t):
    body = f"""
<text x="32" y="46" font-size="13" font-weight="600" letter-spacing="1.5" fill="{t['faint']}">STUDIO</text>
<text x="32" y="88" font-size="30" font-weight="700" letter-spacing="-.8" fill="{t['text']}">One Day Studio</text>
<text x="32" y="116" font-size="16" fill="{t['sub']}">We ship full production apps — fast.</text>
<text x="798" y="60" font-size="26" text-anchor="end" fill="url(#ot)">↗</text>
"""
    return card(830, 140, t, body, glow=(0.95, 0.0), uid="o")


# ---------------------------------------------------------------- BUILD
for th, t in THEMES.items():
    write("hero", th, hero(t))
    write("m1", th, metric("10K+", "downloads on SnapLay", t, "m1"))
    write("m2", th, metric("800+", "students trained", t, "m2"))
    write("m3", th, metric("0→1", "idea to Play Store", t, "m3"))
    write("journey", th, journey(t))
    write("p-skippr", th, project("COMMUNITY APP", "Skippr",
          ["Concierge platform for residential", "communities. OTP auth, service", "requests, admin dashboard."],
          "React Native · Supabase · AWS", t, "p1"))
    write("p-snaplay", th, project("OTT PLATFORM", "SnapLay",
          ["Streaming app with 10K+ downloads.", "Razorpay, Firebase Auth, ads —", "30% faster media delivery."],
          "Flutter · Node.js · AWS", t, "p2"))
    write("p-polymarket", th, project("TRADING BOT", "Polymarket Bot",
          ["Runs user-defined strategies,", "manages Polygon wallets, sizes", "positions and controls risk."],
          "TypeScript · Node.js · Web3", t, "p3"))
    write("p-algotrade", th, project("TRADING RESEARCH", "AlgoTrade",
          ["Plain-English trading ideas to", "backtested strategies for Indian", "stocks, indices and options."],
          "Python · FastAPI · LangGraph · Gemini", t, "p4"))
    write("stack", th, stack(t))
    write("studio", th, studio(t))

print(f"wrote {len(list(OUT.glob('*.svg')))} svgs to {OUT}")
