"""Gera a linha de ícones de IA (logos oficiais) no mesmo formato do skillicons.
Logos: @lobehub/icons-static-svg 1.103.0 (MIT), salvos em assets/logos/.
Uso: python3 gen_ai.py   (rodar dentro de assets/)
"""
import re

ICONS = [  # arquivo, nome (alt), é monocromático?
    ("claude-color", "Claude", False),
    ("openai", "ChatGPT", True),
    ("gemini-color", "Gemini", False),
    ("githubcopilot", "GitHub Copilot", True),
    ("perplexity-color", "Perplexity", False),
    ("deepseek-color", "DeepSeek", False),
    ("grok", "Grok", True),
    ("mcp", "MCP", True),
]
THEMES = {"dark": ("#242938", "#FFFFFF"), "light": ("#F4F2ED", "#111111")}
TILE, STEP, LOGO = 48, 56.25, 30


def inner(path, fg):
    s = open(path).read()
    s = re.sub(r"^<svg[^>]*>", "", s).replace("</svg>", "")
    s = re.sub(r"<title>.*?</title>", "", s)
    return s.replace("currentColor", fg)


for theme, (box, fg) in THEMES.items():
    parts = []
    for i, (f, name, mono) in enumerate(ICONS):
        x = i * STEP
        body = inner(f"logos/{f}.svg", fg)
        if mono:
            body = f'<g fill="{fg}" fill-rule="evenodd">{body}</g>'
        off = (TILE - LOGO) / 2
        parts.append(
            f'<g><title>{name}</title><rect x="{x:.2f}" width="{TILE}" height="{TILE}" rx="11" fill="{box}"/>'
            f'<g transform="translate({x + off:.2f},{off}) scale({LOGO / 24})">{body}</g></g>')
    w = (len(ICONS) - 1) * STEP + TILE
    alt = ", ".join(n for _, n, _ in ICONS)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.2f}" height="{TILE}" '
           f'viewBox="0 0 {w:.2f} {TILE}" role="img" aria-label="{alt}">{"".join(parts)}</svg>')
    open(f"ai-{theme}.svg", "w").write(svg)
