"""Gera os cards de projeto e os chips de IA do perfil (versões dark e light).
Uso: python3 gen_cards.py <pasta-de-saida>
"""
import sys
from html import escape

OUT = sys.argv[1]
SANS = '-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif'
MONO = '"SF Mono",ui-monospace,Menlo,Consolas,"Liberation Mono",monospace'

THEMES = {
    "dark": dict(bg="#0A0C10", fg="#F2F3F5", mut="#9AA3B2", faint="#6B7280", line="#1F2430",
                 pill="#141821", pillfg="#C9D1DC", orb=".45"),
    "light": dict(bg="#FAFAF8", fg="#111318", mut="#4B5260", faint="#6B7280", line="#E4E5E9",
                  pill="#F0F1F3", pillfg="#3A404C", orb=".20"),
}

PROJECTS = [
    dict(slug="maestro", name="Maestro", status="EM CONSTRUÇÃO · PRIVADO", live=False,
         accent=("#7C5CFF", "#22D3EE"),
         desc=["Uma equipe de agentes de IA que toca o dia a dia",
               "de uma empresa. Cada agente tem seu papel e pede",
               "aprovação antes de mexer com dinheiro."],
         en="AI agents that run a company, with a human in the loop.",
         tags=["Next.js", "TypeScript", "Claude Agent SDK", "Drizzle"]),
    dict(slug="chorus", name="Chorus", status="PROTÓTIPO · PRIVADO", live=False,
         accent=("#F472B6", "#7C5CFF"),
         desc=["Um espaço onde os agentes de IA de um time",
               "trabalham juntos dentro dos apps que o time já",
               "usa, como GitHub, Slack e Jira."],
         en="A shared workspace where a team's AI agents collaborate.",
         tags=["Next.js", "MCP", "Composio", "Tailwind"]),
    dict(slug="lastro", name="Lastro", status="MVP · PRIVADO", live=False,
         accent=("#F59E0B", "#F472B6"),
         desc=["Ajuda empresas sem time fiscal a cumprir o novo",
               "split payment da Reforma Tributária (IBS/CBS),",
               "com garantia em caso de erro."],
         en="Insurance-backed tax compliance for Brazil's split payment.",
         tags=["Python", "FastAPI", "PostgreSQL", "Alembic"]),
    dict(slug="analisador", name="Analisador de Ações", status="OPEN SOURCE", live=True,
         accent=("#22C55E", "#22D3EE"),
         desc=["Dá uma nota de 0 a 100 para ações da B3 a partir",
               "de 7 indicadores fundamentalistas, explicando",
               "cada um deles."],
         en="Scores Brazilian stocks from 7 fundamental indicators.",
         tags=["Java 17", "Spring Boot", "WebFlux", "29 testes"]),
]

W, H = 600, 300


def pill_width(text, size=14):
    return len(text) * size * 0.62 + 24


def card(p, theme):
    t = THEMES[theme]
    a1, a2 = p["accent"]
    sid = f'{p["slug"]}-{theme}'
    # tags
    x = 32
    tags = []
    for tag in p["tags"]:
        w = pill_width(tag)
        tags.append(f'<rect x="{x}" y="244" width="{w:.0f}" height="30" rx="15" fill="{t["pill"]}" stroke="{t["line"]}"/>'
                    f'<text x="{x + w / 2:.0f}" y="264" text-anchor="middle" class="tag">{escape(tag)}</text>')
        x += w + 8
    desc = "".join(f'<text x="32" y="{132 + i * 28}" class="desc">{escape(l)}</text>' for i, l in enumerate(p["desc"]))
    sw = len(p["status"]) * 8.3 + 38
    dot = "#22C55E" if p["live"] else a1
    arrow = (f'<g class="arrow"><circle cx="{W - 44}" cy="56" r="18" fill="{t["pill"]}" stroke="{t["line"]}"/>'
             f'<path d="M{W - 50} 62 L{W - 38} 50 M{W - 47} 50 H{W - 38} V59" stroke="{t["fg"]}" stroke-width="2" fill="none" stroke-linecap="round"/></g>') if p["live"] else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p["name"])}: {escape(" ".join(p["desc"]))}">
<style>
.title{{font:700 30px {SANS};letter-spacing:-.6px;fill:{t["fg"]}}}
.desc{{font:400 18px {SANS};fill:{t["mut"]}}}
.en{{font:italic 400 14px {SANS};fill:{t["faint"]}}}
.tag{{font:500 14px {MONO};fill:{t["pillfg"]}}}
.status{{font:600 11px {SANS};letter-spacing:1.4px;fill:{t["mut"]}}}
@keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-40px,18px)}}}}
.orb{{animation:drift 14s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
.dot{{animation:pulse 2.4s ease-in-out infinite}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<defs>
<linearGradient id="bar-{sid}" x1="0" x2="1"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>
<filter id="blur-{sid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>
<clipPath id="clip-{sid}"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#clip-{sid})">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<g filter="url(#blur-{sid})" opacity="{t["orb"]}"><circle class="orb" cx="{W - 60}" cy="40" r="95" fill="{a1}"/><circle class="orb" cx="{W + 10}" cy="150" r="70" fill="{a2}"/></g>
<rect width="{W}" height="4" fill="url(#bar-{sid})"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["line"]}"/>
<rect x="32" y="34" width="{sw:.0f}" height="24" rx="12" fill="{t["pill"]}" stroke="{t["line"]}"/>
<circle class="dot" cx="46" cy="46" r="4" fill="{dot}"/>
<text x="56" y="50" class="status">{escape(p["status"])}</text>
<text x="32" y="98" class="title">{escape(p["name"])}</text>
{arrow}
{desc}
<text x="32" y="224" class="en">{escape(p["en"])}</text>
{"".join(tags)}
</svg>'''


AI = ["Claude API", "Claude Agent SDK", "MCP", "Composio", "Multiagentes"]


def ai_chips(theme):
    # mesmo tamanho dos ícones do skillicons (48px de altura)
    t = THEMES[theme]
    box = "#242938" if theme == "dark" else "#F4F2ED"
    fg = "#F2F3F5" if theme == "dark" else "#1F2328"
    x, parts = 0, []
    for i, label in enumerate(AI):
        w = len(label) * 8.6 + 52
        parts.append(f'<rect x="{x}" y="0" width="{w:.0f}" height="48" rx="12" fill="{box}"/>'
                     f'<circle cx="{x + 22}" cy="24" r="6" fill="url(#g-{theme})" class="d{i % 3}"/>'
                     f'<text x="{x + 36}" y="29.5" class="c">{escape(label)}</text>')
        x += w + 8
    total = x - 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total:.0f}" height="48" viewBox="0 0 {total:.0f} 48" role="img" aria-label="{", ".join(AI)}">
<style>
.c{{font:600 15px {SANS};fill:{fg}}}
@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.d0{{animation:p 2.4s ease-in-out infinite}} .d1{{animation:p 2.4s .8s ease-in-out infinite}} .d2{{animation:p 2.4s 1.6s ease-in-out infinite}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<defs><linearGradient id="g-{theme}" x1="0" x2="1"><stop offset="0" stop-color="#D97757"/><stop offset="1" stop-color="#7C5CFF"/></linearGradient></defs>
{"".join(parts)}
</svg>'''


for theme in THEMES:
    for p in PROJECTS:
        open(f'{OUT}/card-{p["slug"]}-{theme}.svg', "w").write(card(p, theme))
    open(f"{OUT}/ai-{theme}.svg", "w").write(ai_chips(theme))
