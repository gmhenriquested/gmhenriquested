import sys
out=sys.argv[1]
phrases=["construo produtos com agentes de IA","building multi-agent systems","java · spring boot · typescript · next.js"]
FS=22; CW=FS*0.6  # monospace char width
X0=140; Y=232
def svg(theme):
    if theme=="dark":
        bg="#0A0C10"; fg="#F2F3F5"; mut="#8B93A1"; line="#1C2129"; acc1="#7C5CFF"; acc2="#22D3EE"; acc3="#F472B6"; orbop=".55"
    else:
        bg="#FAFAF8"; fg="#111318"; mut="#5B6270"; line="#E6E7EA"; acc1="#6D4AFF"; acc2="#0891B2"; acc3="#DB2777"; orbop=".22"
    T=12; slot=T/len(phrases)
    css=[]
    groups=[]
    for i,p in enumerate(phrases):
        n=len(p); w=n*CW
        a=i*slot/T*100; b=(i+1)*slot/T*100
        # visibility: on within slot
        css.append(f"@keyframes v{i}{{0%,{a:.2f}%{{opacity:0}}{a+0.01:.2f}%,{b-0.01:.2f}%{{opacity:1}}{b:.2f}%,100%{{opacity:0}}}}")
        # typing: grow during first 35% of slot, hold, shrink last 12%
        t1=a+slot*0.35/T*100; t2=b-slot*0.14/T*100
        css.append(f"@keyframes t{i}{{0%{{transform:scaleX(0)}}{a:.2f}%{{transform:scaleX(0);animation-timing-function:steps({n},end)}}{t1:.2f}%{{transform:scaleX(1)}}{t2:.2f}%{{transform:scaleX(1);animation-timing-function:steps({n},end)}}{b:.2f}%,100%{{transform:scaleX(0)}}}}")
        css.append(f"@keyframes c{i}{{0%{{transform:translateX(0)}}{a:.2f}%{{transform:translateX(0);animation-timing-function:steps({n},end)}}{t1:.2f}%{{transform:translateX({w:.1f}px)}}{t2:.2f}%{{transform:translateX({w:.1f}px);animation-timing-function:steps({n},end)}}{b:.2f}%,100%{{transform:translateX(0)}}}}")
        css.append(f".g{i}{{opacity:0;animation:v{i} {T}s linear infinite}}")
        css.append(f".r{i}{{transform-box:fill-box;transform-origin:left;animation:t{i} {T}s linear infinite}}")
        css.append(f".k{i}{{animation:c{i} {T}s linear infinite}}")
        groups.append(f'''<clipPath id="cp{i}"><rect class="r{i}" x="{X0}" y="{Y-24}" width="{w:.1f}" height="34"/></clipPath>
<g class="g{i}"><text x="{X0}" y="{Y}" class="mono" fill="{fg}" clip-path="url(#cp{i})">{p}</text>
<rect class="k{i} cur" x="{X0+2}" y="{Y-19}" width="11" height="24" rx="1.5" fill="{acc2}"/></g>''')
    # use steps per phrase for typing feel: override timing with steps(n) on the grow segment is complex; use linear+steps via many keyframes not needed
    css_s="\n".join(css)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-label="Gabriel Henriques. Engenharia de Software no IBMEC. Construo produtos com agentes de IA.">
<style>
.name{{font:700 64px -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;letter-spacing:-1.5px}}
.sub{{font:500 20px -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;fill:{mut}}}
.mono{{font:500 {FS}px "SF Mono",ui-monospace,Menlo,Consolas,"Liberation Mono",monospace;white-space:pre}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.blink{{animation:blink 1s steps(1) infinite}}
@keyframes drift1{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(60px,20px)}}}}
@keyframes drift2{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-70px,-15px)}}}}
@keyframes drift3{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(40px,-25px)}}}}
.o1{{animation:drift1 14s ease-in-out infinite}} .o2{{animation:drift2 18s ease-in-out infinite}} .o3{{animation:drift3 16s ease-in-out infinite}}
@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.in1{{animation:rise .9s ease-out both}} .in2{{animation:rise .9s .25s ease-out both}} .in3{{animation:rise .9s .5s ease-out both}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
.dot{{animation:pulse 2.4s ease-in-out infinite}}
{css_s}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}} .g0{{opacity:1}} .r0{{transform:none}}}}
</style>
<defs>
<linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{acc1}"><animate attributeName="stop-color" values="{acc1};{acc2};{acc3};{acc1}" dur="10s" repeatCount="indefinite"/></stop>
<stop offset="1" stop-color="{acc2}"><animate attributeName="stop-color" values="{acc2};{acc3};{acc1};{acc2}" dur="10s" repeatCount="indefinite"/></stop>
</linearGradient>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<clipPath id="card"><rect width="1200" height="320" rx="20"/></clipPath>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{line}" stroke-width="1"/></pattern>
<radialGradient id="fade" cx="0.75" cy="0.5" r="0.7"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gridmask"><rect width="1200" height="320" fill="url(#fade)"/></mask>
</defs>
<g clip-path="url(#card)">
<rect width="1200" height="320" fill="{bg}"/>
<rect width="1200" height="320" fill="url(#grid)" mask="url(#gridmask)" opacity=".7"/>
<g filter="url(#blur)" opacity="{orbop}">
<circle class="o1" cx="900" cy="90" r="120" fill="{acc1}"/>
<circle class="o2" cx="1060" cy="250" r="110" fill="{acc2}"/>
<circle class="o3" cx="760" cy="280" r="90" fill="{acc3}"/>
</g>
</g>
<rect x=".5" y=".5" width="1199" height="319" rx="20" fill="none" stroke="{line}"/>
<g class="in1"><circle class="dot" cx="88" cy="74" r="5" fill="#22C55E"/><text x="104" y="80" class="sub" style="font-size:16px;letter-spacing:2px">DISPONÍVEL PARA ESTÁGIO · OPEN TO INTERNSHIPS</text></g>
<text x="80" y="152" class="name in2" fill="url(#grad)">Gabriel Henriques</text>
<text x="82" y="190" class="sub in2">Engenharia de Software · IBMEC · Brasil</text>
<g class="in3"><text x="82" y="{Y}" class="mono" fill="{acc1}">~ $</text>
{"".join(groups)}
</g>
</svg>'''
for t in ("dark","light"):
    open(f"{out}/header-{t}.svg","w").write(svg(t))
