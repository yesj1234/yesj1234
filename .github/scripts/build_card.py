"""README 맨 위 VS Code 창 카드(다크·라이트 SVG 두 장)를 만든다. 색은 블로그 app.pcss 의 토큰과 같다."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[2] / "assets"

THEMES = {
    "dark": {
        "bg": "#1f1f1f", "tabs": "#181818", "tab_active": "#1f1f1f", "border": "#2b2b2b",
        "text": "#d4d4d4", "faint": "#6e7681", "line_active": "#c6c6c6", "highlight": "#2a2d2e",
        "accent": "#4daafc", "statusbar": "#0078d4",
        "comment": "#6a9955", "key": "#569cd6", "string": "#ce9178", "punct": "#d4d4d4",
        "brackets": ["#ffd700", "#da70d6", "#179fff"],
    },
    "light": {
        "bg": "#ffffff", "tabs": "#f8f8f8", "tab_active": "#ffffff", "border": "#e5e5e5",
        "text": "#1f2328", "faint": "#8c959f", "line_active": "#1f2328", "highlight": "#f0f0f0",
        "accent": "#005fb8", "statusbar": "#005fb8",
        "comment": "#008000", "key": "#800000", "string": "#0451a5", "punct": "#393a34",
        "brackets": ["#0431fa", "#319331", "#7b3814"],
    },
}

# (들여쓰기, 키, 값). 값이 list 면 [a, b] 로 그린다. 키가 None 이면 주석 줄
LINES = [
    (0, None, "# jack — builds the Flutter app and the server behind it"),
    (0, "name", "Yang Seung Jun"),
    (0, "role", "Flutter developer, app + server"),
    (0, "stack", None),
    (1, "app", ["Flutter", "BLoC", "Melos", "Clean Architecture"]),
    (1, "server", ["Django", "FastAPI", "Celery"]),
    (1, "native", ["WidgetKit", "ActivityKit", "watchOS", "Wear OS"]),
    (1, "tooling", ["Claude Code", "agent harness", "WebDriverAgent"]),
    (0, "blog", "https://yesj1234.github.io"),
    (0, "now", "writing down what I build"),
]

W, PAD_X = 720, 0
TAB_H, STATUS_H, LINE_H, TOP_GAP = 36, 24, 26, 14
FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SIZE = 15
CHAR = SIZE * 0.6  # 고정폭 글꼴 한 글자 폭(근사)
GUTTER = 56


def tspan(text, color):
    return f'<tspan fill="{color}">{escape(text)}</tspan>'


def render_line(indent, key, value, t):
    parts = ["  " * indent and tspan("  " * indent, t["text"])]
    if key is None:
        return "".join(parts) + tspan(value, t["comment"])
    parts.append(tspan(key, t["key"]) + tspan(":", t["punct"]))
    if value is None:
        return "".join(parts)
    if isinstance(value, list):
        bracket = t["brackets"][0]
        inner = tspan(", ", t["punct"]).join(tspan(v, t["string"]) for v in value)
        return "".join(parts) + " " + tspan("[", bracket) + inner + tspan("]", bracket)
    return "".join(parts) + " " + tspan(value, t["string"])


def build(name, t):
    body_h = TOP_GAP * 2 + LINE_H * len(LINES)
    h = TAB_H + body_h + STATUS_H
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
        f'font-family="{FONT}" font-size="{SIZE}">',
        f'<rect width="{W}" height="{h}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        # 탭 바
        f'<path d="M0 10a10 10 0 0 1 10-10h{W-20}a10 10 0 0 1 10 10v{TAB_H-10}h-{W}z" fill="{t["tabs"]}"/>',
        f'<line x1="0" y1="{TAB_H}" x2="{W}" y2="{TAB_H}" stroke="{t["border"]}"/>',
    ]
    for i, color in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        out.append(f'<circle cx="{20 + i * 20}" cy="{TAB_H/2}" r="6" fill="{color}"/>')
    tab_x = 92
    out += [
        f'<rect x="{tab_x}" y="0" width="150" height="{TAB_H}" fill="{t["tab_active"]}"/>',
        f'<rect x="{tab_x}" y="0" width="150" height="2" fill="{t["accent"]}"/>',
        f'<text x="{tab_x + 16}" y="{TAB_H/2 + 5}" font-size="13" fill="{t["text"]}">'
        f'<tspan fill="{t["key"]}">!</tspan> profile.yaml</text>',
    ]
    # 현재 줄 강조와 커서
    last = len(LINES)
    cursor_y = TAB_H + TOP_GAP + LINE_H * (last - 1)
    out.append(f'<rect x="1" y="{cursor_y}" width="{W-2}" height="{LINE_H}" fill="{t["highlight"]}"/>')
    for n, (indent, key, value) in enumerate(LINES, start=1):
        base = TAB_H + TOP_GAP + LINE_H * n - 8
        num_color = t["line_active"] if n == last else t["faint"]
        out.append(f'<text x="{GUTTER - 16}" y="{base}" text-anchor="end" fill="{num_color}">{n}</text>')
        out.append(f'<text x="{GUTTER}" y="{base}" xml:space="preserve">{render_line(indent, key, value, t)}</text>')
    text_len = len(f'{LINES[-1][1]}: {LINES[-1][2]}')
    cx = GUTTER + CHAR * text_len + 2
    out.append(
        f'<rect x="{cx:.1f}" y="{cursor_y + 5}" width="2" height="{LINE_H - 10}" fill="{t["text"]}">'
        '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
    )
    # 상태 바
    sy = h - STATUS_H
    out += [
        f'<path d="M0 {sy}h{W}v{STATUS_H-10}a10 10 0 0 1-10 10h-{W-20}a10 10 0 0 1-10-10z" fill="{t["statusbar"]}"/>',
        f'<text x="14" y="{sy + 16}" font-size="12" fill="#ffffff">⎇ main</text>',
        f'<text x="{W - 14}" y="{sy + 16}" font-size="12" fill="#ffffff" text-anchor="end" xml:space="preserve">'
        f'Ln {last}, Col {text_len + 1}    UTF-8    YAML</text>',
        "</svg>",
    ]
    (OUT / f"profile-{name}.svg").write_text("\n".join(out), encoding="utf-8")


OUT.mkdir(exist_ok=True)
for theme_name, theme in THEMES.items():
    build(theme_name, theme)
