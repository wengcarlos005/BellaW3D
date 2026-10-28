#!/usr/bin/env python3
"""Gera o site estático da Bella W3D em public/. Uso: python3 src/build.py"""
import hashlib
import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
OUT = ROOT / "public"
sys.path.insert(0, str(SRC))
from content import FAQ, FEATURED, HERO, OCCASIONS, PRODUCTS, SITE  # noqa: E402

TODAY = date.today().isoformat()
BY_ID = {p["id"]: p for p in PRODUCTS}
OCC = {o["id"]: o for o in OCCASIONS}
INK, PINK, PINK_600, TEAL, TINT, MUTED = "#24103A", "#F7647F", "#D1365D", "#3CC0D8", "#FFF3F5", "#6B5F7C"


def esc(s):
    return html.escape(str(s), quote=True)


def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def wa(text):
    return f"https://wa.me/{SITE['whatsapp']}?text={quote(text)}"


def page_url(path):
    return SITE["url"] + ("/" if path == "index" else f"/{path}")


def abs_asset(path):
    return f"{SITE['url']}/{path}"


WA_GENERAL = wa("Olá! Vim pelo site da Bella W3D e gostaria de mais informações.")
WA_CUSTOM = wa("Olá! Vim pelo site da Bella W3D e quero fazer uma peça personalizada.")

# ---------------------------------------------------------------- ícones
STROKE = 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
SYMBOLS = {
    "spark": ('viewBox="0 0 7 7" fill="currentColor" shape-rendering="crispEdges"', '<path d="M3 0h1v2h1v1h2v1H5v1H4v2H3V5H2V4H0V3h2V2h1z"/>'),
    "arrow": (STROKE, '<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "bag": (STROKE, '<path d="M5.5 8h13l-1.1 12.1a1 1 0 0 1-1 .9H7.6a1 1 0 0 1-1-.9L5.5 8z"/><path d="M9 10V7a3 3 0 0 1 6 0v3"/>'),
    "menu": (STROKE, '<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "close": (STROKE, '<path d="M6 6l12 12M18 6L6 18"/>'),
    "truck": (STROKE, '<path d="M3 6.5h11v9H3zM14 9.5h3.6l3.4 3.4v2.6h-7"/><circle cx="7" cy="17.5" r="1.7"/><circle cx="17" cy="17.5" r="1.7"/>'),
    "shield": (STROKE, '<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.2-7.5 9.5-4.3-1.3-7.5-4.9-7.5-9.5V6L12 3z"/><path d="M8.8 12.2l2.2 2.2 4.3-4.4"/>'),
    "chat": (STROKE, '<path d="M20.5 11.5a8 8 0 0 1-11.7 7.1L4 20l1.3-4.4A8 8 0 1 1 20.5 11.5z"/>'),
    "instagram": (STROKE, '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/>'),
    "whatsapp": ('fill="currentColor"', '<path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5 5.2-1.4A9.9 9.9 0 1 0 12.04 2zm0 18.1a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7 3.9zm4.5-6.1c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.56.12-.16.25-.64.8-.78.97-.15.16-.29.18-.54.06a6.7 6.7 0 0 1-3.32-2.9c-.25-.43.25-.4.72-1.33.08-.16.04-.3-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.41-.56-.42h-.47a.9.9 0 0 0-.66.31 2.8 2.8 0 0 0-.86 2.07 4.8 4.8 0 0 0 1 2.56c.12.16 1.74 2.66 4.22 3.73 1.57.68 2.18.74 2.97.62.48-.07 1.46-.6 1.67-1.18.2-.58.2-1.07.15-1.18-.07-.1-.23-.16-.48-.29z"/>'),
}
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
          + "".join(f'<symbol id="i-{k}" {attrs}>{body}</symbol>' for k, (attrs, body) in SYMBOLS.items()) + "</svg>")


def use(name, cls="icon"):
    vb = ' viewBox="0 0 7 7"' if name == "spark" else ' viewBox="0 0 24 24"'
    return f'<svg class="{cls}"{vb} aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


I = {k: use(k) for k in SYMBOLS}
I["spark"] = use("spark", "spark")
I["menu"] = use("menu", "icon i-open")
I["close"] = use("close", "icon i-close")

# ---------------------------------------------------------------- imagens
IMG = {}


def save_webp(im, path, q=78):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "WEBP", quality=q, method=6)


def edge_band(gray, side):
    w, h = gray.size
    n = 0
    for i in range(h if side in "tb" else w):
        j = i if side in "tl" else (h if side == "b" else w) - 1 - i
        box = (0, j, w, j + 1) if side in "tb" else (j, 0, j + 1, h)
        st = ImageStat.Stat(gray.crop(box))
        if st.stddev[0] < 4 and (st.mean[0] > 247 or st.mean[0] < 10):
            n += 1
        else:
            break
    return n


def letterbox_box(im):
    """Caixa sem as tarjas lisas (brancas ou pretas) acima/abaixo da foto; fotos de estúdio com fundo branco ficam inteiras."""
    g = im.convert("L")
    t, b, l, r = (edge_band(g, s) for s in "tblr")
    if l or r or t + b < 30:
        return (0, 0, im.width, im.height)
    return (0, t, im.width, im.height - b)


def build_product_images():
    for p in PRODUCTS:
        src = next(SRC.glob(f"img/produtos/{p['id']}.*"))
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        box = letterbox_box(im)
        # Versão ampliada (EDSR x2) das fotos pequenas, gerada uma vez em img/produtos-hd/.
        hd = SRC / f"img/produtos-hd/{p['id']}.jpg"
        if hd.exists():
            big = Image.open(hd).convert("RGB")
            k = big.width / im.width
            im, box = big, tuple(round(v * k) for v in box)
        im = im.crop(box)
        side = min(min(im.size), 900)
        sq = ImageOps.fit(im, (side, side), Image.LANCZOS, centering=p.get("focus", (0.5, 0.5)))
        widths = [360] + ([600] if side >= 700 else []) + [side]
        base = f"assets/img/produtos/{p['slug']}"
        for w in widths:
            out = sq if w == side else sq.resize((w, w), Image.LANCZOS)
            save_webp(out, OUT / f"{base}-{w}.webp", q=80 if w <= 360 else 86)
        og = sq.resize((630, 630), Image.LANCZOS)
        (OUT / "assets/img/og").mkdir(parents=True, exist_ok=True)
        og.save(OUT / f"assets/img/og/{p['slug']}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
        IMG[p["id"]] = {"base": base, "widths": widths, "side": side}


def img(pid, prefix, sizes, alt=None, eager=False):
    d = IMG[pid]
    srcset = ", ".join(f"{prefix}{d['base']}-{w}.webp {w}w" for w in d["widths"])
    default = next((w for w in d["widths"] if w >= 600), d["widths"][-1])
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{prefix}{d["base"]}-{default}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{d["side"]}" height="{d["side"]}" alt="{esc(alt or BY_ID[pid]["name"])}" {load} decoding="async">')


def build_brand_images():
    logo = Image.open(SRC / "img/marca/logo.png").convert("RGBA")
    for w in (180, 300):
        save_webp(logo.resize((w, round(w * logo.height / logo.width)), Image.LANCZOS), OUT / f"assets/img/logo-{w}.webp", q=86)
    logo.resize((560, round(560 * logo.height / logo.width)), Image.LANCZOS).quantize(
        colors=256, method=Image.Quantize.FASTOCTREE).save(OUT / "assets/img/logo.png", optimize=True)

    card = Image.open(SRC / "img/marca/cartao-obrigada.jpg").convert("RGB")
    for w in (720, 1200):
        save_webp(card.resize((w, round(w * card.height / card.width)), Image.LANCZOS), OUT / f"assets/img/marca/cartao-obrigada-{w}.webp")
    shutil.copy(SRC / "img/marca/qr-instagram.svg", OUT / "assets/img/marca/qr-instagram.svg")

    mark = Image.open(SRC / "img/marca/simbolo.png").convert("RGBA")

    def icon(size, pad, bg=None):
        c = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
        inner = size - 2 * pad
        k = inner / max(mark.size)
        m = mark.resize((round(mark.width * k), round(mark.height * k)), Image.LANCZOS)
        c.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
        return c

    bg = (255, 227, 233, 255)
    def png(im, path):
        im.quantize(colors=128, method=Image.Quantize.FASTOCTREE).save(path, optimize=True)

    png(icon(180, 26, bg), OUT / "apple-touch-icon.png")
    for s in (192, 512):
        png(icon(s, round(s * 0.16), bg), OUT / f"assets/img/icon-{s}.png")
    png(icon(32, 1), OUT / "assets/img/icon-32.png")
    icon(256, 6).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


def font(name, size):
    return ImageFont.truetype(str(SRC / f"fonts/build/{name}.ttf"), size)


def build_og_home():
    W, H = 1200, 630
    c = Image.new("RGB", (W, H), TINT)
    d = ImageDraw.Draw(c)
    logo = Image.open(SRC / "img/marca/logo.png").convert("RGBA")
    lh = 100
    logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
    c.paste(logo, (64, 52), logo)
    head = font("brico-800", 56)
    y = 188
    for line in ("Lembrancinhas e", "presentes", "personalizados", "em 3D"):
        d.text((64, y), line, font=head, fill=INK)
        y += 60
    pill_f = font("fig-700", 21)
    label = f"Peças a partir de {brl(min(p['price'] for p in PRODUCTS if p['price']))}"
    tw = d.textlength(label, font=pill_f)
    py = y + 22
    d.rounded_rectangle((64, py, 64 + tw + 40, py + 46), radius=23, fill=PINK_600)
    d.text((84, py + 11), label, font=pill_f, fill="#FFFFFF")
    sub = font("fig-500", 24)
    d.text((64, 548), f"Envio para todo o Brasil  ·  {SITE['instagram_handle']}", font=sub, fill=MUTED)
    tiles = ["taca", "balao", "gatinho", "capelo"]
    size, gap, x0, y0 = 228, 16, 660, 79
    for i, pid in enumerate(tiles):
        src = OUT / f"{IMG[pid]['base']}-{IMG[pid]['widths'][-1]}.webp"
        t = Image.open(src).convert("RGB").resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=26, fill=255)
        c.paste(t, (x0 + (i % 2) * (size + gap), y0 + (i // 2) * (size + gap)), mask)
    c.save(OUT / "assets/img/og/bella-w3d.jpg", "JPEG", quality=88, optimize=True, progressive=True)


# ---------------------------------------------------------------- partes
NAV = [("catalogo", "Catálogo"), ("personalizados", "Personalizados"), ("sobre", "Sobre"), ("contato", "Contato")]


def jsonld(data):
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{raw}</script>'


def head(pg, pre, ver):
    og_img = pg.get("og_image", abs_asset("assets/img/og/bella-w3d.jpg"))
    og_w, og_h = pg.get("og_size", (1200, 630))
    extra = ""
    if pg.get("price"):
        extra = (f'<meta property="product:price:amount" content="{pg["price"]:.2f}">'
                 f'<meta property="product:price:currency" content="BRL">')
    robots = '<meta name="robots" content="noindex">' if pg.get("noindex") else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(pg['title'])}</title>
<meta name="description" content="{esc(pg['desc'])}">
{robots}<link rel="canonical" href="{page_url(pg['path'])}">
<meta name="theme-color" content="#FFFCFA">
<meta property="og:type" content="{pg.get('og_type', 'website')}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(pg.get('og_title', pg['title']))}">
<meta property="og:description" content="{esc(pg['desc'])}">
<meta property="og:url" content="{page_url(pg['path'])}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="{og_w}">
<meta property="og:image:height" content="{og_h}">
<meta property="og:image:alt" content="{esc(pg.get('og_alt', SITE['tagline']))}">
{extra}<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="icon" href="{pre}assets/img/icon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preload" href="{pre}assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{pre}assets/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/css/site.css?v={ver['css']}">
<script src="{pre}assets/js/site.js?v={ver['js']}" defer></script>
{''.join(jsonld(j) for j in pg.get('jsonld', []))}
</head>"""


def cur(on):
    return ' aria-current="page"' if on else ""


def header(pre, home, active):
    links = "".join(f'<li><a href="{pre}{slug}"{cur(slug == active)}>{label}</a></li>' for slug, label in NAV)
    menu_links = f'<li><a href="{home}"{cur(active == "index")}>Início {I["arrow"]}</a></li>' + "".join(
        f'<li><a href="{pre}{slug}"{cur(slug == active)}>{label} {I["arrow"]}</a></li>' for slug, label in NAV)
    return f"""<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div class="announce"><p>{I['spark']}<span>Envio para todo o Brasil</span><span class="dot" aria-hidden="true">·</span><span>Compra segura pela Shopee</span></p></div>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="{home}" aria-label="Bella W3D, página inicial"><img src="{pre}assets/img/logo-180.webp" srcset="{pre}assets/img/logo-180.webp 180w, {pre}assets/img/logo-300.webp 300w" sizes="(min-width: 960px) 94px, 80px" width="180" height="104" alt="Bella W3D"></a>
    <nav class="nav" aria-label="Principal"><ul>{links}</ul></nav>
    <div class="header-actions">
      <a class="btn btn-primary btn-sm header-shop" href="{SITE['shopee']}" target="_blank" rel="noopener">{I['bag']}<span>Loja na Shopee</span></a>
      <button class="icon-btn menu-btn" type="button" aria-expanded="false" aria-controls="menu" data-menu-btn><span class="sr-only">Abrir menu</span>{I['menu']}{I['close']}</button>
    </div>
  </div>
  <div class="menu" id="menu" hidden>
    <div class="wrap">
      <nav aria-label="Menu"><ul>{menu_links}</ul></nav>
      <div class="menu-ctas">
        <a class="btn btn-primary btn-block" href="{SITE['shopee']}" target="_blank" rel="noopener">{I['bag']} Comprar na Shopee</a>
        <a class="btn btn-outline btn-block" href="{WA_GENERAL}" target="_blank" rel="noopener"><span class="wa">{I['whatsapp']}</span> Falar no WhatsApp</a>
      </div>
    </div>
  </div>
</header>"""


def footer(pre, home):
    occ = "".join(f'<li><a href="{pre}catalogo#{o["id"]}">{o["label"]}</a></li>' for o in OCCASIONS)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="wordmark" href="{home}">Bella W3D</a>
        <p>Lembrancinhas e presentes personalizados em impressão 3D. Envio para todo o Brasil.</p>
        <a class="btn btn-light btn-sm" href="{WA_GENERAL}" target="_blank" rel="noopener"><span class="wa">{I['whatsapp']}</span> Falar no WhatsApp</a>
      </div>
      <nav class="footer-col footer-col--occ" aria-label="Ocasiões"><h2>Ocasiões</h2><ul>{occ}</ul></nav>
      <nav class="footer-col" aria-label="Loja"><h2>Loja</h2><ul>
        <li><a href="{pre}catalogo">Catálogo</a></li>
        <li><a href="{pre}personalizados">Personalizados</a></li>
        <li><a href="{SITE['shopee']}" target="_blank" rel="noopener">Loja na Shopee</a></li>
      </ul></nav>
      <nav class="footer-col" aria-label="Bella W3D"><h2>Bella W3D</h2><ul>
        <li><a href="{pre}sobre">Sobre</a></li>
        <li><a href="{pre}contato">Contato</a></li>
        <li><a href="{home}#perguntas">Perguntas frequentes</a></li>
      </ul></nav>
    </div>
    <div class="footer-bottom">
      <p>© {SITE['year']} Bella W3D. Todos os direitos reservados.</p>
      <ul class="socials">
        <li><a href="{SITE['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{I['instagram']}</a></li>
        <li><a href="{WA_GENERAL}" target="_blank" rel="noopener" aria-label="WhatsApp">{I['whatsapp']}</a></li>
        <li><a href="{SITE['shopee']}" target="_blank" rel="noopener" aria-label="Loja na Shopee">{I['bag']}</a></li>
      </ul>
    </div>
  </div>
</footer>"""


def layout(pg, body, ver):
    pre = pg.get("prefix", "../" * pg.get("depth", 0))
    home = pre or "./"
    float_btn = "" if pg.get("buybar") else (
        f'<a class="wa-float" href="{WA_GENERAL}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">{I["whatsapp"]}</a>')
    cls = ' class="has-buybar"' if pg.get("buybar") else ""
    return (head(pg, pre, ver) + f"\n<body{cls}>\n{SPRITE}\n" + header(pre, home, pg["active"]) +
            f'\n<main id="conteudo">\n{body}\n</main>\n' + footer(pre, home) + "\n" + float_btn +
            pg.get("buybar", "") + "\n</body>\n</html>\n")


def crumbs(items, pre):
    lis = []
    for label, href in items:
        lis.append(f'<li><a href="{href}">{esc(label)}</a></li>' if href else f'<li><span aria-current="page">{esc(label)}</span></li>')
    return f'<nav class="crumbs" aria-label="Você está em"><ol>{"".join(lis)}</ol></nav>'


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": url} for i, (name, url) in enumerate(items)]}


CARD_SIZES = "(min-width: 1100px) 260px, (min-width: 760px) 30vw, 46vw"


def card(p, pre):
    tags = " ".join(p["occasions"] + (["personalizaveis"] if p.get("personal") else []))
    badge = '<span class="badge">Personalizável</span>' if p.get("personal") else ""
    price = (f'<p class="card-price">{brl(p["price"])}</p>' if p["price"]
             else '<p class="card-price is-quote">Preço sob consulta</p>')
    return (f'<li data-tags="{tags}"><a class="card" href="{pre}produtos/{p["slug"]}">'
            f'<div class="card-media">{img(p["id"], pre, CARD_SIZES)}{badge}</div>'
            f'<div class="card-body"><p class="card-tag">{OCC[p["occasions"][0]]["label"]}</p>'
            f'<h3 class="card-title">{esc(p["name"])}</h3>{price}</div></a></li>')


def faq_html(items):
    return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def cta_band(title, text, href, label, icon_html):
    return (f'<div class="cta-band"><div><h2>{title}</h2><p>{text}</p></div>'
            f'<a class="btn btn-primary" href="{href}" target="_blank" rel="noopener">{icon_html} {label}</a></div>')


def ig_block(pre):
    return f"""<div class="ig">
  <div>
    <h2 class="h2">Acompanhe as novidades no Instagram</h2>
    <p class="lead">Lançamentos, ideias de presentes e peças novas. Siga {SITE['instagram_handle']}.</p>
    <a class="btn btn-primary ig-cta" href="{SITE['instagram']}" target="_blank" rel="noopener">{I['instagram']} Seguir {SITE['instagram_handle']}</a>
  </div>
  <figure class="ig-qr"><span class="ig-qr-box"><img src="{pre}assets/img/marca/qr-instagram.svg" width="132" height="132" alt="QR code do Instagram {SITE['instagram_handle']}" loading="lazy" decoding="async"></span><figcaption>Aponte a câmera do celular</figcaption></figure>
</div>"""


ORG_LD = {
    "@context": "https://schema.org", "@type": "Organization", "name": SITE["name"], "url": SITE["url"] + "/",
    "logo": abs_asset("assets/img/logo.png"), "description": SITE["description"],
    "sameAs": [SITE["instagram"], SITE["shopee"]],
    "contactPoint": {"@type": "ContactPoint", "telephone": "+55-21-96487-6543", "contactType": "customer service",
                     "areaServed": "BR", "availableLanguage": "Portuguese"},
}

# ---------------------------------------------------------------- páginas
def page_home():
    pre = ""
    def slot(i, pids):
        sizes = "(min-width: 960px) 340px, 55vw" if i == 0 else "(min-width: 960px) 260px, 42vw"
        imgs = "".join(img(pid, pre, sizes, eager=(i == 0 and j == 0)) for j, pid in enumerate(pids))
        imgs = imgs.replace("<img ", '<img class="is-on" ', 1)
        return f"<figure data-rotate>{imgs}</figure>"
    hero = "".join(slot(i, pids) for i, pids in enumerate(HERO))
    min_price = min(p["price"] for p in PRODUCTS if p["price"])
    occs = [f'<li><a class="occ" href="catalogo#{o["id"]}">{img(o["cover"], pre, "(min-width: 1100px) 180px, (min-width: 760px) 30vw, 46vw", alt="")}'
            f'<span class="occ-label"><span>{o.get("short", o["label"])}</span>{I["arrow"]}</span></a></li>' for o in OCCASIONS[:6]]
    featured = "".join(card(BY_ID[i], pre) for i in FEATURED)
    body = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">{I['spark']} Ateliê de impressão 3D</p>
      <h1>Lembrancinhas e presentes <em>personalizados</em> em 3D</h1>
      <p class="lead">Peças criativas para festas, formaturas, datas especiais e o quarto das crianças. Feitas sob encomenda e preparadas com carinho para você.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="catalogo">Ver catálogo {I['arrow']}</a>
        <a class="btn btn-outline" href="{WA_CUSTOM}" target="_blank" rel="noopener"><span class="wa">{I['whatsapp']}</span> Pedir personalizado</a>
      </div>
      <ul class="checks">
        <li>{I['truck']} Envio para todo o Brasil</li>
        <li>{I['shield']} Compra segura pela Shopee</li>
        <li>{I['chat']} Atendimento pelo WhatsApp</li>
      </ul>
    </div>
    <div class="collage">{hero}<p class="price-tag">Peças a partir de<strong>{brl(min_price)}</strong></p></div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="t-ocasioes">
  <div class="wrap">
    <div class="section-head"><h2 id="t-ocasioes">Encontre o presente certo para cada ocasião</h2><a class="link-arrow" href="catalogo">Ver tudo {I['arrow']}</a></div>
    <ul class="occ-grid">{''.join(occs)}</ul>
  </div>
</section>

<section class="section section--tint" aria-labelledby="t-destaques">
  <div class="wrap">
    <div class="section-head"><div><h2 id="t-destaques">Peças em destaque</h2><p>Algumas das nossas favoritas, prontas para encomendar.</p></div><a class="link-arrow" href="catalogo">Ver catálogo completo {I['arrow']}</a></div>
    <ul class="grid grid--4">{featured}</ul>
  </div>
</section>

<section class="section" aria-labelledby="t-personalize">
  <div class="wrap split">
    <figure class="split-media split-media--square">{img('etiquetas', pre, '(min-width: 900px) 540px, 100vw', alt='Etiqueta personalizada com o nome Alice em uma sacola de presente')}</figure>
    <div>
      <h2 class="h2" id="t-personalize">Do seu jeito: com nome, tema e cores</h2>
      <p class="lead">Muitas peças podem levar o nome de quem você ama ou o tema da sua festa. Conte sua ideia que a gente ajuda a tirar do papel.</p>
      <ol class="steps">
        <li><strong>Conte sua ideia</strong><span>Pelo WhatsApp: nome, tema, cores e quantidade.</span></li>
        <li><strong>Combine os detalhes</strong><span>Alinhamos modelo, valor e prazo antes de produzir.</span></li>
        <li><strong>Receba em casa</strong><span>Sua peça é produzida, embalada com carinho e enviada para todo o Brasil.</span></li>
      </ol>
      <div class="split-ctas"><a class="btn btn-primary" href="{WA_CUSTOM}" target="_blank" rel="noopener">{I['whatsapp']} Pedir personalizado</a><a class="link-arrow" href="personalizados">Como funciona {I['arrow']}</a></div>
    </div>
  </div>
</section>

<section class="section section--tint" aria-labelledby="t-carinho">
  <div class="wrap split split--reverse">
    <figure class="split-media"><img src="assets/img/marca/cartao-obrigada-720.webp" srcset="assets/img/marca/cartao-obrigada-720.webp 720w, assets/img/marca/cartao-obrigada-1200.webp 1200w" sizes="(min-width: 900px) 540px, 100vw" width="1200" height="800" alt="Cartão de agradecimento da Bella W3D que acompanha os pedidos" loading="lazy" decoding="async"></figure>
    <div>
      <h2 class="h2" id="t-carinho">Cada pedido sai daqui com carinho</h2>
      <p class="lead">Cada peça é pensada para marcar um momento especial. Os pedidos são embalados com cuidado e acompanham um cartãozinho de agradecimento.</p>
      <div class="split-ctas"><a class="link-arrow" href="sobre">Conheça a Bella W3D {I['arrow']}</a></div>
    </div>
  </div>
</section>

<section class="section" id="perguntas" aria-labelledby="t-faq">
  <div class="wrap faq-layout">
    <div>
      <h2 class="h2" id="t-faq">Perguntas frequentes</h2>
      <p class="lead">Ficou com alguma dúvida que não está aqui? É só chamar a gente.</p>
      <a class="link-arrow" href="{WA_GENERAL}" target="_blank" rel="noopener">Falar no WhatsApp {I['arrow']}</a>
    </div>
    <div class="faq">{faq_html(FAQ)}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">{ig_block(pre)}</div>
</section>"""
    pg = {
        "path": "index", "active": "index",
        "title": "Bella W3D | Lembrancinhas e Presentes Personalizados em 3D",
        "desc": SITE["description"],
        "jsonld": [ORG_LD, {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"],
                            "url": SITE["url"] + "/", "inLanguage": "pt-BR"}, faq_ld(FAQ)],
    }
    return pg, body


def page_catalog():
    pre = ""
    chips = ['<button class="chip" type="button" data-filter="todos" aria-pressed="true">Todos</button>',
             '<button class="chip" type="button" data-filter="personalizaveis" aria-pressed="false">Personalizáveis</button>']
    chips += [f'<button class="chip" type="button" data-filter="{o["id"]}" aria-pressed="false">{o["label"]}</button>' for o in OCCASIONS]
    cards = "".join(card(p, pre) for p in PRODUCTS)
    body = f"""<div class="wrap">
  {crumbs([("Início", "./"), ("Catálogo", None)], pre)}
  <header class="page-head">
    <h1>Catálogo</h1>
    <p class="lead">Lembrancinhas, presentes e decoração em impressão 3D. Toque em uma peça para ver os detalhes e comprar.</p>
  </header>
  <div class="filters"><div class="chips" role="group" aria-label="Filtrar por ocasião">{''.join(chips)}</div></div>
  <h2 class="sr-only">Produtos</h2>
  <p class="result-count" data-count aria-live="polite">{len(PRODUCTS)} peças</p>
  <ul class="grid grid--4">{cards}</ul>
  <section class="section">{cta_band('Não encontrou o que procurava?', 'Conte sua ideia e a gente vê como transformar em peça.', WA_CUSTOM, 'Falar no WhatsApp', I['whatsapp'])}</section>
</div>"""
    pg = {
        "path": "catalogo", "active": "catalogo",
        "title": "Catálogo de Lembrancinhas e Presentes em 3D | Bella W3D",
        "desc": "Catálogo da Bella W3D: lembrancinhas, chaveiros, decoração e brinquedos Montessori em impressão 3D, "
                "com opções personalizadas e envio para todo o Brasil.",
        "jsonld": [breadcrumb_ld([("Início", SITE["url"] + "/"), ("Catálogo", page_url("catalogo"))]),
                   {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
                       {"@type": "ListItem", "position": i + 1, "url": page_url(f"produtos/{p['slug']}"), "name": p["name"]}
                       for i, p in enumerate(PRODUCTS)]}],
    }
    return pg, body


def related(p):
    seen, out = {p["id"]}, []
    pools = [[q for q in PRODUCTS if p["occasions"][0] in q["occasions"]],
             [q for q in PRODUCTS if set(p["occasions"]) & set(q["occasions"])],
             [BY_ID[i] for i in FEATURED]]
    for pool in pools:
        for q in pool:
            if q["id"] not in seen and len(out) < 4:
                seen.add(q["id"])
                out.append(q)
    return out


def page_product(p):
    pre = "../"
    url = page_url(f"produtos/{p['slug']}")
    shop = p.get("shopee") or SITE["shopee"]
    wa_p = wa(f"Olá! Tenho interesse no produto {p['name']}: {url}")
    priced = p["price"] is not None
    pills = "".join(f'<a class="pill" href="../catalogo#{o}">{OCC[o]["label"]}</a>' for o in p["occasions"])
    if p.get("personal"):
        pills += '<a class="pill" href="../catalogo#personalizaveis">Personalizável</a>'
    if priced:
        price = f'<p class="pdp-price">{brl(p["price"])}</p><p class="pdp-note">Valor de referência. Confira preço e frete atualizados na Shopee.</p>'
        ctas = (f'<a class="btn btn-primary" href="{shop}" target="_blank" rel="noopener">{I["bag"]} Comprar na Shopee</a>'
                f'<a class="btn btn-outline" href="{wa_p}" target="_blank" rel="noopener"><span class="wa">{I["whatsapp"]}</span> Pedir pelo WhatsApp</a>')
        bar_cta = f'<a class="btn btn-primary" href="{shop}" target="_blank" rel="noopener">{I["bag"]} Comprar</a>'
        bar_price = brl(p["price"])
    else:
        price = '<p class="pdp-price is-quote">Preço sob consulta</p><p class="pdp-note">Fale com a gente para saber valores, números e cores disponíveis.</p>'
        ctas = (f'<a class="btn btn-primary" href="{wa_p}" target="_blank" rel="noopener">{I["whatsapp"]} Consultar pelo WhatsApp</a>'
                f'<a class="btn btn-outline" href="{shop}" target="_blank" rel="noopener">{I["bag"]} Ver loja na Shopee</a>')
        bar_cta = f'<a class="btn btn-primary" href="{wa_p}" target="_blank" rel="noopener">{I["whatsapp"]} Consultar</a>'
        bar_price = "Sob consulta"
    ticks = [p.get("material", "Impresso em 3D")]
    if p.get("kit"):
        ticks.append(f"Kit com {p['kit']} unidades")
    if p.get("personal"):
        ticks.append("Personalizável com nome")
    ticks += ["Feito sob encomenda", "Envio para todo o Brasil"]
    box = ""
    if p.get("personal"):
        box = ('<div class="pdp-box"><h2>Como personalizar</h2><p>Na hora da compra, mande pelo WhatsApp o nome, o tema ou '
               'as cores que você quer na peça. <a href="../personalizados">Veja como funciona</a>.</p></div>')
    rel = "".join(card(q, pre) for q in related(p))
    body = f"""<div class="wrap">
  {crumbs([("Início", "../"), ("Catálogo", "../catalogo"), (p['name'], None)], pre)}
  <article class="pdp">
    <figure class="pdp-media">{img(p['id'], pre, '(min-width: 900px) 560px, 100vw', eager=True)}</figure>
    <div>
      <div class="pdp-tags">{pills}</div>
      <h1>{esc(p['name'])}</h1>
      {price}
      <div class="pdp-ctas" data-buy-anchor>{ctas}</div>
      <p class="pdp-desc">{esc(p['desc'])}</p>
      <ul class="ticks">{''.join(f'<li>{t}</li>' for t in ticks)}</ul>
      {box}
    </div>
  </article>
</div>
<section class="section section--tint" aria-labelledby="t-rel">
  <div class="wrap">
    <div class="section-head"><h2 id="t-rel">Você também pode gostar</h2><a class="link-arrow" href="../catalogo">Ver catálogo {I['arrow']}</a></div>
    <ul class="grid grid--4">{rel}</ul>
  </div>
</section>"""
    buybar = (f'\n<div class="buybar" data-buybar><p class="buybar-price">{bar_price}<small>{esc(p["name"])}</small></p>{bar_cta}'
              f'<a class="icon-btn" href="{wa_p}" target="_blank" rel="noopener" aria-label="Pedir pelo WhatsApp">{I["whatsapp"]}</a></div>')
    img_abs = abs_asset(f"assets/img/og/{p['slug']}.jpg")
    material = p.get("material", "Impresso em 3D")
    lds = [breadcrumb_ld([("Início", SITE["url"] + "/"), ("Catálogo", page_url("catalogo")), (p["name"], url)])]
    if priced:
        lds.insert(0, {
            "@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["desc"],
            "image": [img_abs], "brand": {"@type": "Brand", "name": SITE["name"]},
            "category": OCC[p["occasions"][0]]["label"], "url": url,
            "offers": {"@type": "Offer", "price": f"{p['price']:.2f}", "priceCurrency": "BRL",
                       "availability": "https://schema.org/MadeToOrder", "url": url,
                       "seller": {"@type": "Organization", "name": SITE["name"]}},
        })
    price_txt = f"por {brl(p['price'])}" if priced else "sob consulta"
    pg = {
        "path": f"produtos/{p['slug']}", "active": "catalogo", "depth": 1,
        "title": f"{p['name']} | Bella W3D",
        "desc": f"{p['name']} {price_txt}. {p['short']} {material} e enviado para todo o Brasil.",
        "og_type": "product", "og_image": img_abs, "og_size": (630, 630), "og_alt": p["name"],
        "price": p["price"], "jsonld": lds, "buybar": buybar,
    }
    return pg, body


def page_custom():
    pre = ""
    faq = [FAQ[2], FAQ[3], FAQ[4]]
    cards = "".join(card(p, pre) for p in PRODUCTS if p.get("personal"))
    body = f"""<div class="wrap">
  {crumbs([("Início", "./"), ("Personalizados", None)], pre)}
  <header class="page-head">
    <h1>Peças personalizadas em impressão 3D</h1>
    <p class="lead">Nome, tema, cores e quantidade do seu jeito, para festas, presentes e datas especiais.</p>
  </header>
</div>
<section class="section" aria-labelledby="t-oque">
  <div class="wrap split">
    <figure class="split-media split-media--square">{img('taca', pre, '(min-width: 900px) 540px, 100vw', alt='Taças com marcadores personalizados com o nome de cada convidado', eager=True)}</figure>
    <div>
      <h2 class="h2" id="t-oque">O que dá para personalizar</h2>
      <p class="lead">Cada pedido é combinado com você, para a peça ficar com a cara de quem vai receber.</p>
      <ul class="ticks" style="margin-top:22px">
        <li>Nomes e iniciais</li>
        <li>Temas de festas e datas comemorativas</li>
        <li>Cores, conforme a disponibilidade</li>
        <li>Kits em quantidade para eventos</li>
      </ul>
      <div class="split-ctas"><a class="btn btn-primary" href="{WA_CUSTOM}" target="_blank" rel="noopener">{I['whatsapp']} Pedir personalizado</a></div>
    </div>
  </div>
</section>
<section class="section section--tint" aria-labelledby="t-como">
  <div class="wrap">
    <div class="section-head"><h2 id="t-como">Como funciona</h2></div>
    <ol class="steps" style="max-width:720px;margin-top:0">
      <li><strong>Conte sua ideia pelo WhatsApp</strong><span>Diga qual peça você quer, o nome ou tema, as cores, a quantidade e a data em que precisa receber.</span></li>
      <li><strong>Combine os detalhes</strong><span>A gente confirma o que é possível fazer e alinha modelo, valor e prazo com você.</span></li>
      <li><strong>Produção e envio</strong><span>Sua peça é produzida sob encomenda, embalada com cuidado e enviada para todo o Brasil.</span></li>
    </ol>
  </div>
</section>
<section class="section" aria-labelledby="t-pers">
  <div class="wrap">
    <div class="section-head"><h2 id="t-pers">Peças que você pode personalizar</h2><a class="link-arrow" href="catalogo#personalizaveis">Ver no catálogo {I['arrow']}</a></div>
    <ul class="grid grid--4">{cards}</ul>
  </div>
</section>
<section class="section section--tint" aria-labelledby="t-pfaq">
  <div class="wrap faq-layout">
    <div><h2 class="h2" id="t-pfaq">Dúvidas sobre personalizados</h2><p class="lead">Cada pedido é combinado com você antes da produção.</p></div>
    <div class="faq">{faq_html(faq)}</div>
  </div>
</section>
<section class="section"><div class="wrap">{cta_band('Tem uma ideia em mente?', 'Mande uma mensagem e vamos criar juntos.', WA_CUSTOM, 'Pedir personalizado', I['whatsapp'])}</div></section>"""
    pg = {
        "path": "personalizados", "active": "personalizados",
        "title": "Peças Personalizadas em Impressão 3D | Bella W3D",
        "desc": "Peças personalizadas em impressão 3D com nome, tema e cores: lembrancinhas de festa, presentes e kits "
                "para eventos. Peça pelo WhatsApp e receba em todo o Brasil.",
        "jsonld": [breadcrumb_ld([("Início", SITE["url"] + "/"), ("Personalizados", page_url("personalizados"))]), faq_ld(faq)],
    }
    return pg, body


def page_about():
    pre = ""
    body = f"""<div class="wrap">
  {crumbs([("Início", "./"), ("Sobre", None)], pre)}
  <header class="page-head">
    <h1>Sobre a Bella W3D</h1>
    <p class="lead">Um ateliê de impressão 3D dedicado a criar peças afetivas: lembrancinhas, presentes e brinquedos que fazem parte de momentos especiais.</p>
  </header>
</div>
<section class="section" aria-label="Nossa história">
  <div class="wrap split">
    <figure class="split-media"><img src="assets/img/marca/cartao-obrigada-720.webp" srcset="assets/img/marca/cartao-obrigada-720.webp 720w, assets/img/marca/cartao-obrigada-1200.webp 1200w" sizes="(min-width: 900px) 540px, 100vw" width="1200" height="800" alt="Cartão de agradecimento da Bella W3D que acompanha os pedidos" fetchpriority="high" decoding="async"></figure>
    <div class="prose">
      <p>Na Bella W3D, a impressão 3D vira presente. Criamos peças sob encomenda, de lembrancinhas de festa a brinquedos inspirados no método Montessori, pensadas para quem vai receber.</p>
      <p>Cada pedido é preparado com atenção aos detalhes, embalado com cuidado e acompanha um cartãozinho de agradecimento. Vendemos pela Shopee, com compra protegida, e atendemos pelo WhatsApp para tirar dúvidas e combinar peças personalizadas.</p>
    </div>
  </div>
</section>
<section class="section section--tint" aria-labelledby="t-valores">
  <div class="wrap">
    <div class="section-head"><h2 id="t-valores">O que move a gente</h2></div>
    <ul class="values">
      <li><h3>{I['spark']} Personalização</h3><p>Peças com nome, tema e cores que fazem sentido para quem vai receber.</p></li>
      <li><h3>{I['spark']} Cuidado em cada pedido</h3><p>Atenção aos detalhes da produção à embalagem, com um cartãozinho de agradecimento.</p></li>
      <li><h3>{I['spark']} Para todo o Brasil</h3><p>Vendemos pela Shopee e enviamos para qualquer lugar do país.</p></li>
    </ul>
  </div>
</section>
<section class="section"><div class="wrap">{cta_band('Vamos criar algo juntos?', 'Veja o catálogo ou conte sua ideia pelo WhatsApp.', WA_GENERAL, 'Falar no WhatsApp', I['whatsapp'])}</div></section>"""
    pg = {
        "path": "sobre", "active": "sobre",
        "title": "Sobre a Bella W3D | Ateliê de Impressão 3D",
        "desc": "Conheça a Bella W3D, ateliê de impressão 3D que cria lembrancinhas, presentes e brinquedos sob encomenda, "
                "com carinho em cada pedido e envio para todo o Brasil.",
        "jsonld": [breadcrumb_ld([("Início", SITE["url"] + "/"), ("Sobre", page_url("sobre"))])],
    }
    return pg, body


def page_contact():
    pre = ""
    body = f"""<div class="wrap">
  {crumbs([("Início", "./"), ("Contato", None)], pre)}
  <header class="page-head">
    <h1>Fale com a Bella W3D</h1>
    <p class="lead">Dúvidas, pedidos personalizados ou orçamentos para eventos: escolha o canal que preferir.</p>
  </header>
</div>
<section class="section" style="padding-top:28px" aria-label="Canais de atendimento">
  <div class="wrap">
    <ul class="contact-list">
      <li><a class="contact-item" href="{WA_GENERAL}" target="_blank" rel="noopener"><span class="contact-icon ci-wa">{I['whatsapp']}</span><div><h2>WhatsApp</h2><p>{SITE['whatsapp_display']} · dúvidas, personalizados e orçamentos</p></div><span class="go">{I['arrow']}</span></a></li>
      <li><a class="contact-item" href="{SITE['instagram']}" target="_blank" rel="noopener"><span class="contact-icon ci-ig">{I['instagram']}</span><div><h2>Instagram</h2><p>{SITE['instagram_handle']} · novidades e lançamentos</p></div><span class="go">{I['arrow']}</span></a></li>
      <li><a class="contact-item" href="{SITE['shopee']}" target="_blank" rel="noopener"><span class="contact-icon ci-shop">{I['bag']}</span><div><h2>Loja na Shopee</h2><p>shopee.com.br/bella_w3d · compra com pagamento protegido</p></div><span class="go">{I['arrow']}</span></a></li>
    </ul>
    <p class="lead" style="margin-top:28px">Antes de chamar, que tal dar uma olhada nas <a class="link-arrow" href="./#perguntas">perguntas frequentes</a>?</p>
  </div>
</section>
<section class="section section--tight"><div class="wrap">{ig_block(pre)}</div></section>"""
    pg = {
        "path": "contato", "active": "contato",
        "title": "Contato | Bella W3D: WhatsApp, Instagram e Shopee",
        "desc": f"Fale com a Bella W3D pelo WhatsApp {SITE['whatsapp_display']}, pelo Instagram {SITE['instagram_handle']} "
                "ou compre na nossa loja da Shopee. Pedidos personalizados e orçamentos para eventos.",
        "jsonld": [breadcrumb_ld([("Início", SITE["url"] + "/"), ("Contato", page_url("contato"))])],
    }
    return pg, body


def page_404():
    body = f"""<section class="notfound"><div class="wrap">
  <h1>Página não encontrada</h1>
  <p class="lead">O endereço pode ter mudado ou a página não existe mais. Que tal começar pelo catálogo?</p>
  <div class="hero-ctas"><a class="btn btn-primary" href="/catalogo">Ver catálogo {I['arrow']}</a><a class="btn btn-outline" href="/">Ir para o início</a></div>
</div></section>"""
    pg = {"path": "404", "active": "", "noindex": True, "prefix": "/", "title": "Página não encontrada | Bella W3D",
          "desc": "A página que você procurou não foi encontrada."}
    return pg, body


# ---------------------------------------------------------------- saída
def write(pg, body, ver):
    path = OUT / f"{pg['path']}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(layout(pg, body, ver), encoding="utf-8")


def copy_static():
    css = (SRC / "assets/site.css").read_bytes()
    js = (SRC / "assets/site.js").read_bytes()
    (OUT / "assets/css").mkdir(parents=True, exist_ok=True)
    (OUT / "assets/js").mkdir(parents=True, exist_ok=True)
    (OUT / "assets/css/site.css").write_bytes(css)
    (OUT / "assets/js/site.js").write_bytes(js)
    shutil.copytree(SRC / "fonts/web", OUT / "assets/fonts")
    return {"css": hashlib.sha1(css).hexdigest()[:8], "js": hashlib.sha1(js).hexdigest()[:8]}


def write_meta(paths):
    urls = "".join(f"<url><loc>{page_url(p)}</loc><lastmod>{TODAY}</lastmod></url>" for p in paths)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    manifest = {
        "name": SITE["name"], "short_name": SITE["name"], "description": SITE["tagline"], "lang": "pt-BR",
        "start_url": "/", "display": "standalone", "background_color": "#FFFCFA", "theme_color": "#FFFCFA",
        "icons": [{"src": f"/assets/img/icon-{s}.png", "sizes": f"{s}x{s}", "type": "image/png", "purpose": "any maskable"} for s in (192, 512)],
    }
    (OUT / "site.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    ver = copy_static()
    build_product_images()
    build_brand_images()
    build_og_home()
    pages = [page_home(), page_catalog(), page_custom(), page_about(), page_contact()]
    pages += [page_product(p) for p in PRODUCTS]
    for pg, body in pages:
        write(pg, body, ver)
    write(*page_404(), ver)
    write_meta([pg["path"] for pg, _ in pages])
    n = sum(1 for _ in OUT.rglob("*") if _.is_file())
    print(f"ok: {len(pages) + 1} páginas, {n} arquivos em {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
