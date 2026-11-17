"""Gera o card da stack (dark/light) com os ícones embutidos, sem depender de site externo.
Ícones: skillicons.dev (MIT) em assets/skillicons/, logos de IA em assets/logos/.
Uso: python3 gen_stack.py   (rodar dentro de assets/)
"""
import re
from html import escape

SANS = '-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif'
MONO = '"SF Mono",ui-monospace,Menlo,Consolas,"Liberation Mono",monospace'
THEMES = {
    "dark": dict(bg="#0A0C10", fg="#F2F3F5", mut="#9AA3B2", faint="#6B7280", line="#1F2430",
                 pill="#141821", pillfg="#C9D1DC", tile="#242938", logo="#FFFFFF", orb=".35"),
    "light": dict(bg="#FAFAF8", fg="#111318", mut="#4B5260", faint="#6B7280", line="#E4E5E9",
                  pill="#F0F1F3", pillfg="#3A404C", tile="#F4F2ED", logo="#111111", orb=".16"),
}
# (rótulo, ícones skillicons, logos de IA, etiquetas, texto extra)
ROWS = [
    ("BACKEND", "java spring maven python fastapi nodejs", "", [],
     "Spring Data JPA · Spring Security · WebFlux · Thymeleaf · SQLAlchemy"),
    ("FRONTEND", "ts js react nextjs tailwind html css", "", [], "Zod · Lenis"),
    ("IA", "", "claude-color:Claude openai:ChatGPT gemini-color:Gemini githubcopilot:Copilot "
     "perplexity-color:Perplexity deepseek-color:DeepSeek grok:Grok mcp:MCP", [],
     "Claude Agent SDK · Composio · sistemas multiagente"),
    ("DADOS E INFRA", "postgres sqlite docker git github githubactions", "", [], "Drizzle ORM · Alembic · Neon"),
    ("TESTES", "", "", ["JUnit 5", "Mockito", "AssertJ", "JaCoCo", "pytest"], ""),
    ("NO DIA A DIA", "idea obsidian", "", [], ""),
]
MONO_LOGOS = {"openai", "githubcopilot", "grok", "mcp"}
W, PADX, ICX, TILE, STEP = 900, 44, 230, 48, 56
ROW_H = 112


def ns(svg, prefix):
    """Prefixa ids pra não colidirem quando vários SVGs viram um só."""
    ids = set(re.findall(r'id="([^"]+)"', svg))
    for i in ids:
        svg = svg.replace(f'id="{i}"', f'id="{prefix}{i}"')
        svg = svg.replace(f"url(#{i})", f"url(#{prefix}{i})")
        svg = svg.replace(f'href="#{i}"', f'href="#{prefix}{i}"')
    return svg


def skill(name, theme, x, y):
    s = open(f"skillicons/{name}-{theme}.svg").read()
    inner = re.search(r"<svg[^>]*>\s*<g[^>]*>\s*(.*)</g>\s*</svg>\s*$", s, re.S).group(1)
    inner = ns(inner, f"{name}-{theme}-")
    return f'<svg x="{x}" y="{y}" width="{TILE}" height="{TILE}" viewBox="0 0 256 256">{inner}</svg>'


def logo(name, label, theme, x, y):
    t = THEMES[theme]
    s = open(f"logos/{name}.svg").read()
    s = re.sub(r"^<svg[^>]*>", "", s).replace("</svg>", "")
    s = re.sub(r"<title>.*?</title>", "", s).replace("currentColor", t["logo"])
    s = ns(s, f"{name}-{theme}-")
    if name in MONO_LOGOS:
        s = f'<g fill="{t["logo"]}" fill-rule="evenodd">{s}</g>'
    return (f'<g><title>{label}</title><rect x="{x}" y="{y}" width="{TILE}" height="{TILE}" rx="11" fill="{t["tile"]}"/>'
            f'<svg x="{x + 9}" y="{y + 9}" width="30" height="30" viewBox="0 0 24 24">{s}</svg></g>')


def card(theme):
    t = THEMES[theme]
    heights = [ROW_H if row[4] else 76 for row in ROWS]
    H = 40 + sum(heights) - 8
    out = []
    y = 40
    for r, (label, skills, logos, tags, extra) in enumerate(ROWS):
        rh = heights[r]
        out.append(f'<text x="{PADX}" y="{y + 29}" class="lbl">{label}</text>')
        x = ICX
        for n in skills.split():
            out.append(skill(n, theme, x, y)); x += STEP
        for item in logos.split():
            n, lab = item.split(":")
            out.append(logo(n, lab, theme, x, y)); x += STEP
        for tag in tags:
            w = len(tag) * 9.3 + 28
            out.append(f'<rect x="{x}" y="{y + 7}" width="{w:.0f}" height="34" rx="17" fill="{t["pill"]}" stroke="{t["line"]}"/>'
                       f'<text x="{x + w / 2:.0f}" y="{y + 29}" text-anchor="middle" class="tag">{escape(tag)}</text>')
            x += w + 8
        if extra:
            out.append(f'<text x="{ICX}" y="{y + 76}" class="extra">{escape(extra)}</text>')
        if r < len(ROWS) - 1:
            out.append(f'<line x1="{PADX}" x2="{W - PADX}" y1="{y + rh - 14}" y2="{y + rh - 14}" stroke="{t["line"]}"/>')
        y += rh
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Stack: Java, Spring, Python, FastAPI, TypeScript, React, Next.js, Claude, ChatGPT, Gemini, PostgreSQL, Docker e outras">
<style>
.lbl{{font:600 13px {MONO};letter-spacing:2px;fill:{t["faint"]}}}
.extra{{font:400 15px {SANS};fill:{t["mut"]}}}
.tag{{font:500 15px {MONO};fill:{t["pillfg"]}}}
@keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-50px,30px)}}}}
.orb{{animation:drift 18s ease-in-out infinite}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<defs>
<filter id="blur-{theme}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<clipPath id="clip-{theme}"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#clip-{theme})">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<g filter="url(#blur-{theme})" opacity="{t["orb"]}"><circle class="orb" cx="{W - 40}" cy="60" r="110" fill="#7C5CFF"/><circle class="orb" cx="{W + 20}" cy="{H - 60}" r="100" fill="#22D3EE"/></g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["line"]}"/>
{"".join(out)}
</svg>'''


for theme in THEMES:
    open(f"stack-{theme}.svg", "w").write(card(theme))
