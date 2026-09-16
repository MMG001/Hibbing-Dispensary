#!/usr/bin/env python3
"""Static site generator for Hibbing Dispensary.
Generates all HTML pages with a shared shell (header, nav, age gate, footer)
using the High Vibe Botanicals design system (Syne / DM Sans / Space Grotesk,
deep forest green, radiant gold, sun-bleached cream)."""
import os, json

OUT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://hibbing-dispensary.pages.dev"  # update after custom domain

with open(os.path.join(OUT, "images", "metadata.json")) as f:
    ALT = json.load(f)
with open(os.path.join(OUT, "images", "dimensions.json")) as f:
    DIMS = json.load(f)
import time
BUILD_V = str(int(time.time()))

LINK_CLS = "text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep"
def L(href, text):
    return f'<a href="{href}" class="{LINK_CLS}">{text}</a>'

CARD_SIZES = "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"

def _webp(n):
    return "/images/" + n[:-4] + ".webp"

def img(name, cls="", loading="lazy"):
    w, h = DIMS.get(name, [None, None])
    dim = f' width="{w}" height="{h}"' if w else ""
    base = name[:-4]
    alt = ALT.get(name, name)
    if loading == "lazy" and base + "-640.jpg" in DIMS:
        webp_ss = f"{_webp(base + '-640.jpg')} 640w, {_webp(name)} {w}w"
        jpg_ss = f"/images/{base}-640.jpg 640w, /images/{name} {w}w"
        return (f'<picture><source type="image/webp" srcset="{webp_ss}" sizes="{CARD_SIZES}"/>'
                f'<img src="images/{name}" srcset="{jpg_ss}" sizes="{CARD_SIZES}" alt="{alt}" title="{alt}" class="{cls}" loading="lazy"{dim}/></picture>')
    if loading == "eager":
        parts = ([f"{_webp(base + '-828.jpg')} 828w"] if base + "-828.jpg" in DIMS else []) + [f"{_webp(name)} {w}w"]
        return (f'<picture><source type="image/webp" srcset="{", ".join(parts)}" sizes="100vw"/>'
                f'<img src="images/{name}" alt="{alt}" title="{alt}" class="{cls}" loading="eager" fetchpriority="high"{dim} sizes="100vw"/></picture>')
    return f'<img src="images/{name}" alt="{alt}" title="{alt}" class="{cls}" loading="{loading}"{dim}/>'


# ============================================================
# v2 INTERLINKED JSON-LD ENTITY GRAPH
# One @graph per page; all nodes cross-referenced by @id.
# Machine IDs (Wikipedia sameAs) verified 2026-09.
# ============================================================
def url_of(filename):
    return SITE_URL + "/" if filename == "index.html" else SITE_URL + "/" + filename.rsplit(".html", 1)[0]

WIKI = {
    "Hibbing": "https://en.wikipedia.org/wiki/Hibbing,_Minnesota",
    "Chisholm": "https://en.wikipedia.org/wiki/Chisholm,_Minnesota",
    "Buhl": "https://en.wikipedia.org/wiki/Buhl,_Minnesota",
    "Keewatin": "https://en.wikipedia.org/wiki/Keewatin,_Minnesota",
    "StLouisCounty": "https://en.wikipedia.org/wiki/St._Louis_County,_Minnesota",
    "ItascaCounty": "https://en.wikipedia.org/wiki/Itasca_County,_Minnesota",
    "Minnesota": "https://en.wikipedia.org/wiki/Minnesota",
}
GEO = {"@type": "GeoCoordinates", "latitude": 47.4272, "longitude": -92.9377}
GEO_CIRCLE = {"@type": "GeoCircle",
    "description": "10-mile service radius anchored on Hibbing, Minnesota",
    "geoMidpoint": GEO, "geoRadius": "16093"}
AREA_SERVED = [
    GEO_CIRCLE,
    {"@type": "City", "name": "Hibbing", "sameAs": WIKI["Hibbing"]},
    {"@type": "City", "name": "Chisholm", "sameAs": WIKI["Chisholm"]},
    {"@type": "City", "name": "Buhl", "sameAs": WIKI["Buhl"]},
    {"@type": "City", "name": "Keewatin", "sameAs": WIKI["Keewatin"]},
    {"@type": "AdministrativeArea", "name": "St. Louis County, Minnesota", "sameAs": WIKI["StLouisCounty"]},
    {"@type": "AdministrativeArea", "name": "Itasca County, Minnesota", "sameAs": WIKI["ItascaCounty"]},
    {"@type": "AdministrativeArea", "name": "Minnesota", "sameAs": WIKI["Minnesota"]},
]

# Per-slug service metadata: (id-slug, name, serviceType, blurb, wikipedia concept)
SERVICES = [
    ("flower", "Cannabis Flower", "Cannabis flower retail",
     "Hand-trimmed craft cannabis strains across indica, sativa, and hybrid, jarred for freshness.",
     "https://en.wikipedia.org/wiki/Cannabis_(drug)"),
    ("edibles", "Edibles & Gummies", "Cannabis edibles retail",
     "Precisely dosed THC gummies and infused edibles with slow onset and long-lasting effects.",
     "https://en.wikipedia.org/wiki/Cannabis_edible"),
    ("concentrates", "Concentrates & Oils", "Cannabis concentrates retail",
     "Live rosin, crumble, and golden cannabis extracts for full-spectrum potency.",
     "https://en.wikipedia.org/wiki/Cannabis_concentrate"),
    ("vaporizers", "Vaporizers & Cartridges", "Cannabis vaporizer retail",
     "Cartridges, devices, and hardware for clean, fast-onset cannabis inhalation.",
     "https://en.wikipedia.org/wiki/Vaporizer_(inhalation_device)"),
    ("pre-rolls", "Pre-Rolls", "Cannabis pre-roll retail",
     "Ready-to-enjoy pre-rolled cannabis joints crafted from whole flower.",
     "https://en.wikipedia.org/wiki/Joint_(cannabis)"),
    ("tinctures-topicals", "Tinctures & Topicals", "Cannabis tinctures and topicals retail",
     "Sublingual cannabis tinctures and skin-applied balms for smoke-free, targeted use.",
     "https://en.wikipedia.org/wiki/Tincture_of_cannabis"),
]
SVC_ID = lambda slug: SITE_URL + "/shop#service-" + slug

def service_nodes(level):
    """Three-level Service rule: 'card' where blurbs are visible (home/shop), 'stub' elsewhere."""
    nodes = []
    for slug, name, stype, blurb, concept in SERVICES:
        n = {"@type": "Service", "@id": SVC_ID(slug), "name": name,
             "url": SITE_URL + "/shop", "provider": {"@id": SITE_URL + "/#business"}}
        if level == "card":
            n.update({"serviceType": stype, "description": blurb,
                      "areaServed": GEO_CIRCLE, "inLanguage": "en-US",
                      "about": {"@type": "Thing", "name": name, "sameAs": concept}})
        nodes.append(n)
    return nodes

def node_business():
    return {
        "@type": ["Store", "LocalBusiness"],
        "@id": SITE_URL + "/#business",
        "name": "Hibbing Dispensary",
        "description": "Hibbing Dispensary is a licensed adult-use cannabis dispensary in Hibbing, Minnesota, selling lab-tested cannabis flower, edibles, concentrates, vapes, pre-rolls, tinctures, and topicals to adults 21 and over.",
        "slogan": "Legal cannabis for sale — order ahead, pick up in store.",
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/images/THC-Cannabis-Hero.jpg",
        "image": SITE_URL + "/images/THC-Cannabis-Store.jpg",
        "foundingDate": "2026",
        "address": {"@type": "PostalAddress", "streetAddress": "302 E Howard Street",
            "addressLocality": "Hibbing", "addressRegion": "MN", "postalCode": "55746", "addressCountry": "US"},
        "geo": GEO,
        "hasMap": "https://www.google.com/maps/search/?api=1&query=302+E+Howard+Street+Hibbing+MN+55746",
        "areaServed": AREA_SERVED,
        "telephone": "+1-218-000-0000",
        "email": "hello@hibbingdispensary.com",
        "priceRange": "$$",
        "paymentAccepted": "Cash, Debit",
        "currenciesAccepted": "USD",
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "10:00", "closes": "21:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "11:00", "closes": "18:00"}],
        "audience": {"@type": "PeopleAudience", "audienceType": "Adult cannabis consumers", "suggestedMinAge": 21,
            "geographicArea": {"@type": "AdministrativeArea", "name": "Hibbing, Minnesota", "sameAs": WIKI["Hibbing"]}},
        "keywords": "cannabis dispensary, Hibbing MN, legal cannabis for sale, order ahead cannabis, THC, CBD, edibles, flower, concentrates",
        "knowsAbout": [
            {"@type": "Thing", "name": "Cannabis", "sameAs": "https://en.wikipedia.org/wiki/Cannabis_(drug)"},
            {"@type": "Thing", "name": "THC", "sameAs": "https://en.wikipedia.org/wiki/Tetrahydrocannabinol"},
            {"@type": "Thing", "name": "CBD", "sameAs": "https://en.wikipedia.org/wiki/Cannabidiol"},
            {"@type": "Thing", "name": "Minnesota cannabis law", "sameAs": "https://www.revisor.mn.gov/statutes/cite/342.09"}],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Cannabis Menu",
            "itemListElement": [{"@id": SVC_ID(s[0])} for s in SERVICES]},
        "sameAs": ["https://github.com/MMG001/Hibbing-Dispensary"],
        "potentialAction": [
            {"@type": "OrderAction", "name": "Order ahead for in-store pickup",
             "target": {"@type": "EntryPoint", "urlTemplate": SITE_URL + "/shop", "inLanguage": "en-US",
                "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]}},
            {"@type": "AskAction", "name": "Send an inquiry",
             "target": {"@type": "EntryPoint", "urlTemplate": SITE_URL + "/contact#contact-form", "inLanguage": "en-US",
                "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]},
             "name-input": {"@type": "PropertyValueSpecification", "valueName": "name", "valueRequired": True},
             "email-input": {"@type": "PropertyValueSpecification", "valueName": "email", "valueRequired": True},
             "message-input": {"@type": "PropertyValueSpecification", "valueName": "message", "valueRequired": True}},
            {"@type": "CommunicateAction", "name": "Call the dispensary",
             "target": {"@type": "EntryPoint", "urlTemplate": "tel:+12180000000",
                "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]}},
            {"@type": "CommunicateAction", "name": "Email the dispensary",
             "target": {"@type": "EntryPoint", "urlTemplate": "mailto:hello@hibbingdispensary.com",
                "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]}},
        ],
    }

def node_website():
    return {"@type": "WebSite", "@id": SITE_URL + "/#website", "name": "Hibbing Dispensary",
            "url": SITE_URL + "/", "publisher": {"@id": SITE_URL + "/#business"}, "inLanguage": "en-US"}

def node_breadcrumb(filename, crumbs):
    items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]
    return {"@type": "BreadcrumbList", "@id": url_of(filename) + "#breadcrumb", "itemListElement": items}

def node_webpage(filename, title, desc, og_image, page_type="WebPage", main_entity=None):
    n = {"@type": page_type, "@id": url_of(filename) + "#webpage", "url": url_of(filename),
         "name": title, "description": desc,
         "isPartOf": {"@id": SITE_URL + "/#website"}, "about": {"@id": SITE_URL + "/#business"},
         "breadcrumb": {"@id": url_of(filename) + "#breadcrumb"},
         "primaryImageOfPage": SITE_URL + "/" + og_image, "inLanguage": "en-US"}
    if main_entity:
        n["mainEntity"] = {"@id": main_entity}
    return n

def build_graph(filename, title, desc, og_image, page_type, crumbs, svc_level, extra_nodes=None, webpage_props=None):
    wp = node_webpage(filename, title, desc, og_image, page_type,
        main_entity=(extra_nodes[0]["@id"] if extra_nodes else None))
    if webpage_props:
        wp.update(webpage_props)
    graph = [node_website(), node_business(), wp,
        node_breadcrumb(filename, crumbs)] + service_nodes(svc_level) + (extra_nodes or [])
    return {"@context": "https://schema.org", "@graph": graph}

ICONS = "air,arrow_forward,call,close,cookie,diversity_3,expand_more,group,home_work,local_mall,location_on,mail,menu,schedule,school,science,shopping_bag,spa,storefront,verified,water_drop"
ICONS_URL = "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=" + ICONS + "&display=block"
TEXT_FONTS_URL = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Caveat:wght@600..700&family=Manrope:wght@400..800&display=swap"

def head(title, desc, canonical, og_image="images/THC-Cannabis-Hero.jpg", graph=None, preload_hero=True):
    canon = url_of(canonical)
    if preload_hero:
        base = og_image.replace("images/", "")[:-4]
        w = DIMS.get(base + ".jpg", [1568])[0]
        parts = ([f"/images/{base}-828.webp 828w"] if base + "-828.jpg" in DIMS else []) + [f"/images/{base}.webp {w}w"]
        preload = (f'<link rel="preload" as="image" href="/{og_image}" '
                   f'imagesrcset="{", ".join(parts)}" imagesizes="100vw" fetchpriority="high"/>\n')
    else:
        preload = ""
    jsonld = f'<script type="application/ld+json">{json.dumps(graph)}</script>\n' if graph else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{canon}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:image" content="{SITE_URL}/{og_image}"/>
<meta property="og:image:alt" content="{ALT.get(og_image.replace('images/',''), title)}"/>
<meta property="og:locale" content="en_US"/>
<meta property="og:site_name" content="Hibbing Dispensary"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{desc}"/>
<meta name="twitter:image" content="{SITE_URL}/{og_image}"/>
{jsonld}
{preload}<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="{TEXT_FONTS_URL}" rel="stylesheet" media="print" onload="this.media='all'"/>
<link href="{ICONS_URL}" rel="stylesheet" media="print" onload="this.media='all'"/>
<noscript><link href="{TEXT_FONTS_URL}" rel="stylesheet"/><link href="{ICONS_URL}" rel="stylesheet"/></noscript>
<link href="/css/app.css?v={BUILD_V}" rel="stylesheet"/>
<style>
  .material-symbols-outlined {{ font-variation-settings: 'FILL' 0, 'wght' 400; }}
  html {{ scroll-behavior: smooth; }}
  .sticker {{ transform: rotate(-2deg); }}
  .sticker-r {{ transform: rotate(2deg); }}
  .blob {{ border-radius: 46% 54% 52% 48% / 44% 46% 54% 56%; }}
  .dropdown:hover .dropdown-menu, .dropdown:focus-within .dropdown-menu {{ opacity: 1; visibility: visible; transform: translateY(0); }}
  .dropdown-menu {{ opacity: 0; visibility: hidden; transform: translateY(8px); transition: all .18s ease; }}
  .hero-fade {{ background: linear-gradient(90deg, rgba(0,0,0,.82) 0%, rgba(0,0,0,.55) 45%, rgba(0,0,0,.15) 100%); }}
  @media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} * {{ transition: none !important; }} }}
</style>
</head>
<body class="bg-surface text-ink font-body antialiased">
"""

EDU_LINKS = [
    ("cannabis-101.html", "Cannabis 101"),
    ("cannabis-for-beginners.html", "Cannabis for Beginners"),
    ("cannabis-strains.html", "Cannabis Strains"),
    ("cbd-vs-thc.html", "CBD vs THC"),
    ("benefits-of-cannabis.html", "Benefits of Cannabis"),
    ("cannabis-laws.html", "Cannabis Laws"),
]

def header_nav(active=""):
    def cls(page):
        base = "font-label text-sm font-semibold tracking-wider uppercase transition-colors"
        return f'{base} text-gold' if page == active else f'{base} text-white hover:text-gold-bright'
    edu_items = "".join(
        f'<a href="{href}" class="block px-5 py-3 font-label text-sm font-semibold text-forest hover:bg-surface-low hover:text-forest-deep transition-colors">{label}</a>'
        for href, label in EDU_LINKS)
    return f"""
<!-- ===================== HEADER ===================== -->
<header class="bg-forest-deep sticky top-0 z-40 border-b border-forest shadow-sm">
  <div class="mx-auto max-w-shell px-4 md:px-10 flex items-center justify-between h-20">
    <a href="index.html" class="flex items-center gap-3" aria-label="Hibbing Dispensary home">
      <span class="material-symbols-outlined text-gold text-3xl" aria-hidden="true">spa</span>
      <span class="font-display font-extrabold text-white text-xl md:text-2xl leading-none">Hibbing<br class="hidden md:block"/> Dispensary</span>
    </a>
    <nav class="hidden lg:flex items-center gap-8" aria-label="Main navigation">
      <a href="index.html" class="{cls('home')}">Home</a>
      <a href="shop.html" class="{cls('shop')}">Shop</a>
      <div class="dropdown relative">
        <a href="education.html" class="{cls('education')} inline-flex items-center gap-1">Education
          <span class="material-symbols-outlined text-base" aria-hidden="true">expand_more</span></a>
        <div class="dropdown-menu absolute left-0 top-full pt-3 w-64">
          <div class="bg-white rounded-xl shadow-modal border border-outline-soft/40 overflow-hidden py-2">
            <a href="education.html" class="block px-5 py-3 font-label text-sm font-semibold text-forest hover:bg-surface-low transition-colors border-b border-outline-soft/40">Education Hub</a>
            {edu_items}
          </div>
        </div>
      </div>
      <a href="about.html" class="{cls('about')}">About</a>
      <div class="dropdown relative">
        <a href="contact.html" class="{cls('contact')} inline-flex items-center gap-1">Contact
          <span class="material-symbols-outlined text-base" aria-hidden="true">expand_more</span></a>
        <div class="dropdown-menu absolute right-0 top-full pt-3 w-56">
          <div class="bg-white rounded-xl shadow-modal border border-outline-soft/40 overflow-hidden py-2">
            <a href="contact.html" class="block px-5 py-3 font-label text-sm font-semibold text-forest hover:bg-surface-low hover:text-forest-deep transition-colors">Visit &amp; Contact</a>
            <a href="faq.html" class="block px-5 py-3 font-label text-sm font-semibold text-forest hover:bg-surface-low hover:text-forest-deep transition-colors">FAQ</a>
          </div>
        </div>
      </div>
    </nav>
    <div class="flex items-center gap-3">
      <a href="shop.html" class="hidden sm:inline-flex items-center gap-2 bg-gold text-forest-deep font-label font-bold text-sm uppercase tracking-wider px-6 py-3 rounded-lg hover:shadow-pop hover:bg-gold-bright transition-all">
        <span class="material-symbols-outlined text-lg" aria-hidden="true">shopping_bag</span>Shop Now</a>
      <button id="menu-btn" class="lg:hidden text-white p-2" aria-label="Open menu" aria-expanded="false">
        <span class="material-symbols-outlined text-3xl">menu</span></button>
    </div>
  </div>
  <!-- Mobile menu -->
  <div id="mobile-menu" class="hidden lg:hidden bg-forest-deep border-t border-forest px-4 pb-6">
    <a href="index.html" class="block py-3 font-label font-semibold text-white uppercase tracking-wider text-sm border-b border-forest/60">Home</a>
    <a href="shop.html" class="block py-3 font-label font-semibold text-white uppercase tracking-wider text-sm border-b border-forest/60">Shop</a>
    <a href="education.html" class="block py-3 font-label font-semibold text-white uppercase tracking-wider text-sm">Education</a>
    <div class="pl-4 border-l-2 border-gold/50 mb-2">
      {"".join(f'<a href="{h}" class="block py-2 font-body text-sm text-white/80 hover:text-gold-bright">{l}</a>' for h, l in EDU_LINKS)}
    </div>
    <a href="about.html" class="block py-3 font-label font-semibold text-white uppercase tracking-wider text-sm border-b border-forest/60">About</a>
    <a href="contact.html" class="block py-3 font-label font-semibold text-white uppercase tracking-wider text-sm">Contact</a>
    <div class="pl-4 border-l-2 border-gold/50 mb-2">
      <a href="faq.html" class="block py-2 font-body text-sm text-white/80 hover:text-gold-bright">FAQ</a>
    </div>
    <a href="shop.html" class="mt-4 inline-flex items-center gap-2 bg-gold text-forest-deep font-label font-bold text-sm uppercase tracking-wider px-6 py-3 rounded-lg">Shop Now</a>
  </div>
</header>
"""

FOOTER = """
<!-- ===================== FOOTER ===================== -->
<footer class="bg-forest-deep text-white">
  <div class="mx-auto max-w-shell px-4 md:px-10 py-14 grid gap-10 md:grid-cols-4">
    <div>
      <div class="flex items-center gap-2 mb-4">
        <span class="material-symbols-outlined text-gold text-2xl" aria-hidden="true">spa</span>
        <span class="font-display font-extrabold text-lg">Hibbing Dispensary</span>
      </div>
      <p class="text-white/70 text-sm leading-relaxed">Your locally rooted cannabis dispensary on the Iron Range. Craft flower, edibles, concentrates, tinctures, and topicals — curated with care in Hibbing, Minnesota.</p>
    </div>
    <div>
      <h3 class="font-label font-bold uppercase tracking-widest text-gold-bright text-xs mb-4">Explore</h3>
      <ul class="space-y-2 text-sm text-white/80">
        <li><a href="shop.html" class="hover:text-gold-bright transition-colors">Shop the Menu</a></li>
        <li><a href="education.html" class="hover:text-gold-bright transition-colors">Cannabis Education</a></li>
        <li><a href="about.html" class="hover:text-gold-bright transition-colors">Our Story</a></li>
        <li><a href="contact.html" class="hover:text-gold-bright transition-colors">Visit Us</a></li>
        <li><a href="faq.html" class="hover:text-gold-bright transition-colors">FAQ</a></li>
      </ul>
    </div>
    <div>
      <h3 class="font-label font-bold uppercase tracking-widest text-gold-bright text-xs mb-4">Learn</h3>
      <ul class="space-y-2 text-sm text-white/80">
        <li><a href="cannabis-101.html" class="hover:text-gold-bright transition-colors">Cannabis 101</a></li>
        <li><a href="cannabis-for-beginners.html" class="hover:text-gold-bright transition-colors">Cannabis for Beginners</a></li>
        <li><a href="cbd-vs-thc.html" class="hover:text-gold-bright transition-colors">CBD vs THC</a></li>
        <li><a href="cannabis-laws.html" class="hover:text-gold-bright transition-colors">Minnesota Cannabis Laws</a></li>
      </ul>
    </div>
    <div>
      <h3 class="font-label font-bold uppercase tracking-widest text-gold-bright text-xs mb-4">Visit</h3>
      <address class="not-italic text-sm text-white/80 space-y-2">
        <p class="flex items-start gap-2"><span class="material-symbols-outlined text-gold text-lg" aria-hidden="true">location_on</span>302 E Howard Street, Hibbing, MN 55746</p>
        <p class="flex items-start gap-2"><span class="material-symbols-outlined text-gold text-lg" aria-hidden="true">call</span><a href="tel:+12180000000" class="hover:text-gold-bright">(218) 000-0000</a></p>
        <p class="flex items-start gap-2"><span class="material-symbols-outlined text-gold text-lg" aria-hidden="true">schedule</span>Mon–Sat 10am–9pm · Sun 11am–6pm</p>
      </address>
    </div>
  </div>
  <div class="border-t border-forest">
    <div class="mx-auto max-w-shell px-4 md:px-10 py-5 text-center text-xs text-white/60 leading-relaxed">
      <p>For adults 21 and over. Cannabis products have intoxicating psychoactive effects. Keep out of reach of children and pets. Do not operate a vehicle or machinery while under the influence.</p>
    </div>
  </div>
  <!-- Lower footer -->
  <div class="bg-forest-night border-t border-forest">
    <div class="mx-auto max-w-shell px-4 md:px-10 py-5 flex flex-col md:flex-row items-center justify-between gap-3">
      <p class="text-xs text-white/60">© 2026 Hibbing Dispensary. All rights reserved. · Designed by <a href="https://webcreativeseo.com" rel="noopener" target="_blank" class="hover:text-gold-bright underline decoration-white/30 underline-offset-2">webcreativeseo.com</a></p>
      <nav class="flex flex-wrap items-center justify-center gap-x-3 gap-y-1 text-xs text-white/70" aria-label="Legal">
        <a href="privacy-policy.html" class="hover:text-gold-bright transition-colors">Privacy Policy</a><span aria-hidden="true">|</span>
        <a href="terms.html" class="hover:text-gold-bright transition-colors">Terms &amp; Conditions</a><span aria-hidden="true">|</span>
        <a href="equal-opportunity.html" class="hover:text-gold-bright transition-colors">Equal Opportunity Employer</a><span aria-hidden="true">|</span>
        <a href="sitemap.html" class="hover:text-gold-bright transition-colors">Sitemap</a>
      </nav>
    </div>
  </div>
</footer>

<!-- ===================== AGE GATE ===================== -->
<div id="age-gate" class="fixed inset-0 z-50 hidden items-center justify-center bg-forest-night/95 px-4" role="dialog" aria-modal="true" aria-labelledby="age-gate-title">
  <div class="max-w-md w-full bg-forest rounded-2xl shadow-modal border border-gold/30 p-8 text-center text-white">
    <span class="material-symbols-outlined text-gold text-5xl mb-4" aria-hidden="true">spa</span>
    <h2 id="age-gate-title" class="font-display font-extrabold text-3xl mb-3">Are you 21 or older?</h2>
    <p class="text-white/80 text-sm mb-8 leading-relaxed">You must be at least 21 years of age to enter this site. Cannabis products are for adult use only under Minnesota law.</p>
    <div class="flex gap-3 justify-center">
      <button id="age-yes" class="bg-gold text-forest-deep font-label font-bold uppercase tracking-wider text-sm px-8 py-3 rounded-lg hover:bg-gold-bright transition-colors">Yes, I'm 21+</button>
      <a href="https://www.google.com" class="border-2 border-white/40 text-white font-label font-bold uppercase tracking-wider text-sm px-8 py-3 rounded-lg hover:bg-white/10 transition-colors">No, Exit</a>
    </div>
  </div>
</div>

<script src="js/main.js?v=BUILDV_PLACEHOLDER" defer></script>
</body>
</html>
"""

import re as _re
def clean_links(html):
    """Root-relative clean URLs so hrefs match canonicals/sitemap (Cloudflare Pages serves /about for about.html)."""
    html = _re.sub(r'(href=["\'])index\.html', r'\1/', html)
    html = _re.sub(r'(href=["\'])([a-z0-9\-]+)\.html', r'\1/\2', html)
    html = html.replace('src="images/', 'src="/images/').replace('href="images/', 'href="/images/')
    html = html.replace('src="js/main.js"', 'src="/js/main.js"')
    return html

def page(filename, title, desc, active, body, og_image="images/THC-Cannabis-Hero.jpg",
         page_type="WebPage", crumbs=None, svc_level="stub", extra_nodes=None, webpage_props=None):
    crumbs = crumbs or ([("Home", SITE_URL + "/")] if filename == "index.html"
        else [("Home", SITE_URL + "/"), (title.split(" — ")[0].split(" | ")[0], url_of(filename))])
    graph = build_graph(filename, title, desc, og_image, page_type, crumbs, svc_level, extra_nodes, webpage_props)
    hero_pages = filename not in ("privacy-policy.html", "terms.html", "equal-opportunity.html", "sitemap.html")
    html = head(title, desc, filename, og_image, graph, preload_hero=hero_pages) + header_nav(active) + body + FOOTER
    html = html.replace("BUILDV_PLACEHOLDER", BUILD_V)
    html = clean_links(html)
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)
    print("built:", filename)

# breadcrumb + hero banner for interior pages
def hero_banner(image, eyebrow, title, sub=""):
    subhtml = f'<p class="text-white/85 text-lg max-w-2xl">{sub}</p>' if sub else ""
    return f"""
<section class="relative overflow-hidden bg-forest-deep">
  {img(image, "absolute inset-0 h-full w-full object-cover", loading="eager")}
  <div class="absolute inset-0 hero-fade" aria-hidden="true"></div>
  <div class="relative mx-auto max-w-shell px-4 md:px-10 py-20 md:py-28">
    <span class="sticker inline-block bg-gold text-forest-deep font-label font-bold text-xs uppercase tracking-widest px-4 py-1.5 rounded-full mb-5">{eyebrow}</span>
    <h1 class="font-display font-extrabold text-white text-4xl md:text-6xl leading-tight mb-4 max-w-3xl">{title}</h1>
    {subhtml}
  </div>
</section>
"""

# ============================================================ HOME
home_body = f"""
<main id="main">
<!-- HERO -->
<section class="relative overflow-hidden bg-forest-deep text-white">
  <div class="mx-auto max-w-shell px-4 md:px-10 py-20 md:py-28 grid gap-12 lg:grid-cols-2 items-center">
    <div>
      <span class="font-script font-bold text-gold text-2xl md:text-3xl">Craft cannabis, Iron Range grown</span>
      <h1 class="font-display font-extrabold text-4xl md:text-6xl leading-[1.06] mt-3 mb-6">Hibbing's Craft <em class="not-italic text-gold">Cannabis</em> Dispensary</h1>
      <p class="text-white/85 text-lg md:text-xl max-w-2xl mb-9 leading-relaxed">Legal cannabis for sale to adults 21+ — order ahead online and pick up in store. A curated variety of flower, edibles, concentrates, tinctures, and topicals, with budtenders who take the time to help you dose with confidence. Proudly serving Hibbing and Iron Range neighbors within a five-mile radius.</p>
      <div class="flex flex-wrap gap-4">
        <a href="shop.html" class="inline-flex items-center gap-2 bg-gold text-forest-deep font-label font-bold uppercase tracking-wider text-sm px-8 py-4 rounded-full hover:bg-gold-bright hover:shadow-pop transition-all">
          <span class="material-symbols-outlined" aria-hidden="true">storefront</span>Shop the Menu</a>
        <a href="education.html" class="inline-flex items-center gap-2 border-2 border-white/60 text-white font-label font-bold uppercase tracking-wider text-sm px-8 py-4 rounded-full hover:bg-white/10 transition-colors">
          <span class="material-symbols-outlined" aria-hidden="true">school</span>New? Start Here</a>
      </div>
    </div>
    <div class="relative w-full max-w-xl mx-auto lg:mx-0 lg:justify-self-end">
      {img("Hibbing-Hero.jpg", "blob w-full aspect-square object-cover border-8 border-gold/25", loading="eager")}
      <span class="absolute -top-3 -left-2 text-5xl -rotate-12" aria-hidden="true">🍃</span>
      <span class="absolute bottom-4 -right-2 text-4xl rotate-12" aria-hidden="true">🍃</span>
    </div>
  </div>
</section>

<!-- FEATURE STRIP -->
<section aria-label="Store highlights" class="bg-forest text-white border-t border-white/10">
  <div class="mx-auto max-w-shell px-4 md:px-10 py-5 flex flex-wrap items-center justify-center lg:justify-between gap-x-10 gap-y-4">
    <span class="inline-flex items-center gap-2 font-body font-bold text-sm"><span class="text-gold" aria-hidden="true">✦</span>21+ with valid ID, every visit</span>
    <span class="inline-flex items-center gap-2 font-body font-bold text-sm"><span class="text-gold" aria-hidden="true">✦</span>OCM licensed · Minnesota</span>
    <span class="inline-flex items-center gap-2 font-body font-bold text-sm"><span class="text-gold" aria-hidden="true">✦</span>Cash &amp; debit · ATM on-site</span>
    <span class="inline-flex items-center gap-2 font-body font-bold text-sm"><span class="text-gold" aria-hidden="true">✦</span>Open 7 days a week</span>
    <a href="shop.html" class="inline-flex items-center gap-2 bg-[#43a819] text-forest-deep border-2 border-white rounded-full px-5 py-2.5 shadow-modal hover:bg-[#4dbb1f] transition-colors">
      <span class="font-label text-[11px] font-bold uppercase tracking-widest">Pickup</span>
      <span class="font-body font-bold text-sm">Ready in ~15 min</span>
    </a>
  </div>
</section>

<!-- CATEGORIES -->
<section class="py-20 bg-white">
  <div class="mx-auto max-w-shell px-4 md:px-10">
    <div class="flex items-end justify-between mb-10 flex-wrap gap-4">
      <div>
        <span class="font-script font-bold text-forest text-2xl">The lineup</span>
        <h2 class="font-display font-extrabold text-3xl md:text-4xl text-forest-deep mt-1">Carefully Curated Cannabis, Crafted With Care</h2>
        <p class="text-ink-soft mt-3 max-w-xl">Every category, every consumption style — from fast-onset inhalation to slow-burn edibles that last several hours.</p>
      </div>
      <a href="shop.html" class="inline-flex items-center gap-2 bg-gold text-forest-deep font-label font-bold uppercase tracking-wider text-sm px-7 py-3.5 rounded-full hover:bg-gold-bright hover:shadow-pop transition-all">View Full Menu</a>
    </div>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">

      <a href="shop.html" class="group relative bg-surface rounded-3xl overflow-hidden shadow-card hover:shadow-pop hover:-translate-y-1.5 transition-all">
        <div class="aspect-[16/10] overflow-hidden">{img("THC-Cannabis-01.jpg", "h-full w-full object-cover group-hover:scale-105 transition-transform duration-300")}</div>
        <span class="absolute top-4 right-5 font-display font-extrabold text-4xl text-white/90 drop-shadow-lg" aria-hidden="true">01</span>
        <div class="p-6">
          <h3 class="font-display font-bold text-xl text-forest-deep">Flower</h3>
          <p class="text-sm text-ink-soft mt-1 mb-3">Hand-trimmed strains, jarred fresh</p>
          <span class="font-label font-bold text-sm text-forest inline-flex items-center gap-1.5">View More<span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform" aria-hidden="true">arrow_forward</span></span>
        </div>
      </a>
      <a href="shop.html" class="group relative bg-surface rounded-3xl overflow-hidden shadow-card hover:shadow-pop hover:-translate-y-1.5 transition-all">
        <div class="aspect-[16/10] overflow-hidden">{img("THC-Edible-Gummies-01.jpg", "h-full w-full object-cover group-hover:scale-105 transition-transform duration-300")}</div>
        <span class="absolute top-4 right-5 font-display font-extrabold text-4xl text-white/90 drop-shadow-lg" aria-hidden="true">02</span>
        <div class="p-6">
          <h3 class="font-display font-bold text-xl text-forest-deep">Edibles</h3>
          <p class="text-sm text-ink-soft mt-1 mb-3">Gummies dosed for a slow, lasting ride</p>
          <span class="font-label font-bold text-sm text-forest inline-flex items-center gap-1.5">View More<span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform" aria-hidden="true">arrow_forward</span></span>
        </div>
      </a>
      <a href="shop.html" class="group relative bg-surface rounded-3xl overflow-hidden shadow-card hover:shadow-pop hover:-translate-y-1.5 transition-all">
        <div class="aspect-[16/10] overflow-hidden">{img("THC-Concentrates-02.jpg", "h-full w-full object-cover group-hover:scale-105 transition-transform duration-300")}</div>
        <span class="absolute top-4 right-5 font-display font-extrabold text-4xl text-white/90 drop-shadow-lg" aria-hidden="true">03</span>
        <div class="p-6">
          <h3 class="font-display font-bold text-xl text-forest-deep">Concentrates</h3>
          <p class="text-sm text-ink-soft mt-1 mb-3">Live rosin, extracts &amp; golden oils</p>
          <span class="font-label font-bold text-sm text-forest inline-flex items-center gap-1.5">View More<span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform" aria-hidden="true">arrow_forward</span></span>
        </div>
      </a>
      <a href="shop.html" class="group relative bg-surface rounded-3xl overflow-hidden shadow-card hover:shadow-pop hover:-translate-y-1.5 transition-all">
        <div class="aspect-[16/10] overflow-hidden">{img("THC-Vaporizer-01.jpg", "h-full w-full object-cover group-hover:scale-105 transition-transform duration-300")}</div>
        <span class="absolute top-4 right-5 font-display font-extrabold text-4xl text-white/90 drop-shadow-lg" aria-hidden="true">04</span>
        <div class="p-6">
          <h3 class="font-display font-bold text-xl text-forest-deep">Vaporizers</h3>
          <p class="text-sm text-ink-soft mt-1 mb-3">Cartridges &amp; hardware for clean inhalation</p>
          <span class="font-label font-bold text-sm text-forest inline-flex items-center gap-1.5">View More<span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform" aria-hidden="true">arrow_forward</span></span>
        </div>
      </a>
      <a href="shop.html" class="group relative bg-surface rounded-3xl overflow-hidden shadow-card hover:shadow-pop hover:-translate-y-1.5 transition-all">
        <div class="aspect-[16/10] overflow-hidden">{img("THC-Prerolls-01.jpg", "h-full w-full object-cover group-hover:scale-105 transition-transform duration-300")}</div>
        <span class="absolute top-4 right-5 font-display font-extrabold text-4xl text-white/90 drop-shadow-lg" aria-hidden="true">05</span>
        <div class="p-6">
          <h3 class="font-display font-bold text-xl text-forest-deep">Pre-Rolls</h3>
          <p class="text-sm text-ink-soft mt-1 mb-3">Rolled tight, ready when you are</p>
          <span class="font-label font-bold text-sm text-forest inline-flex items-center gap-1.5">View More<span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform" aria-hidden="true">arrow_forward</span></span>
        </div>
      </a>
      <a href="shop.html" class="group relative bg-surface rounded-3xl overflow-hidden shadow-card hover:shadow-pop hover:-translate-y-1.5 transition-all">
        <div class="aspect-[16/10] overflow-hidden">{img("About-Us-page.jpg", "h-full w-full object-cover group-hover:scale-105 transition-transform duration-300")}</div>
        <span class="absolute top-4 right-5 font-display font-extrabold text-4xl text-white/90 drop-shadow-lg" aria-hidden="true">06</span>
        <div class="p-6">
          <h3 class="font-display font-bold text-xl text-forest-deep">Tinctures &amp; Topicals</h3>
          <p class="text-sm text-ink-soft mt-1 mb-3">Drops under the tongue, balms for the skin</p>
          <span class="font-label font-bold text-sm text-forest inline-flex items-center gap-1.5">View More<span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform" aria-hidden="true">arrow_forward</span></span>
        </div>
      </a>
    </div>
  </div>
</section>

<!-- ONSET GUIDE STRIP -->
<section class="py-20 bg-surface">
  <div class="mx-auto max-w-shell px-4 md:px-10">
    <span class="font-script font-bold text-forest text-2xl">Know before you glow</span>
    <h2 class="font-display font-extrabold text-3xl md:text-4xl text-forest-deep mt-1 mb-3">Know Your Onset</h2>
    <p class="text-ink-soft mb-10 max-w-2xl">How you consume changes when the effects arrive — and how long they last. Read the full breakdown in <a href="cannabis-101.html" class="text-forest font-bold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep">Cannabis 101</a>, or <a href="contact.html" class="text-forest font-bold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep">ask a budtender</a> to help you find your dose.</p>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <div class="bg-white rounded-3xl p-7 shadow-card hover:-translate-y-1 transition-transform">
        <span class="inline-grid place-items-center w-14 h-14 rounded-full bg-gold-soft text-2xl mb-4" aria-hidden="true">💨</span>
        <h3 class="font-display font-bold text-xl text-forest-deep mb-2">Inhalation</h3>
        <p class="text-sm text-ink-soft leading-relaxed">Flower, pre-rolls &amp; vapes. Onset in minutes; effects typically fade within one to three hours. Easiest to fine-tune.</p>
      </div>
      <div class="bg-white rounded-3xl p-7 shadow-card hover:-translate-y-1 transition-transform">
        <span class="inline-grid place-items-center w-14 h-14 rounded-full bg-gold-soft text-2xl mb-4" aria-hidden="true">🍬</span>
        <h3 class="font-display font-bold text-xl text-forest-deep mb-2">Edibles</h3>
        <p class="text-sm text-ink-soft leading-relaxed">Gummies &amp; infused treats. Onset can take 30 minutes to two hours — and effects can last several hours. Start low, go slow.</p>
      </div>
      <div class="bg-white rounded-3xl p-7 shadow-card hover:-translate-y-1 transition-transform">
        <span class="inline-grid place-items-center w-14 h-14 rounded-full bg-gold-soft text-2xl mb-4" aria-hidden="true">💧</span>
        <h3 class="font-display font-bold text-xl text-forest-deep mb-2">Tinctures</h3>
        <p class="text-sm text-ink-soft leading-relaxed">Drops under the tongue for a middle-ground onset between inhalation and edibles.</p>
      </div>
      <div class="bg-white rounded-3xl p-7 shadow-card hover:-translate-y-1 transition-transform">
        <span class="inline-grid place-items-center w-14 h-14 rounded-full bg-gold-soft text-2xl mb-4" aria-hidden="true">🧴</span>
        <h3 class="font-display font-bold text-xl text-forest-deep mb-2">Topicals</h3>
        <p class="text-sm text-ink-soft leading-relaxed">Balms and creams applied to the skin for targeted relief without psychoactive effects.</p>
      </div>
    </div>
  </div>
</section>

<!-- PROMO TRIO -->
<section class="py-20 bg-surface">
  <div class="mx-auto max-w-shell px-4 md:px-10 grid gap-6 md:grid-cols-3">
    <div class="rounded-3xl p-9 bg-gradient-to-br from-forest to-forest-deep text-white flex flex-col justify-between items-start gap-6 min-h-[220px]">
      <div><span class="font-script font-bold text-gold text-2xl">100% legal</span>
      <h3 class="font-display font-extrabold text-2xl leading-tight mt-1">Licensed Minnesota Cannabis Store</h3></div>
      <a href="shop.html" class="bg-gold text-forest-deep font-label font-bold uppercase tracking-wider text-sm px-7 py-3 rounded-full hover:bg-gold-bright transition-colors">Shop Now</a>
    </div>
    <div class="rounded-3xl p-9 bg-gold text-forest-deep flex flex-col justify-between items-start gap-6 min-h-[220px]">
      <div><span class="font-script font-bold text-forest text-2xl">Skip the wait</span>
      <h3 class="font-display font-extrabold text-2xl leading-tight mt-1">Order Ahead — Pickup in ~15 Minutes</h3></div>
      <a href="shop.html" class="bg-forest text-white font-label font-bold uppercase tracking-wider text-sm px-7 py-3 rounded-full hover:bg-forest-deep transition-colors">Order Now</a>
    </div>
    <div class="rounded-3xl p-9 bg-gradient-to-br from-forest-deep to-forest-night text-white flex flex-col justify-between items-start gap-6 min-h-[220px]">
      <div><span class="font-script font-bold text-gold text-2xl">Every day</span>
      <h3 class="font-display font-extrabold text-2xl leading-tight mt-1">Open 7 Days a Week on Howard Street</h3></div>
      <a href="contact.html" class="bg-gold text-forest-deep font-label font-bold uppercase tracking-wider text-sm px-7 py-3 rounded-full hover:bg-gold-bright transition-colors">Visit Us</a>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="py-20 bg-forest-deep text-white">
  <div class="mx-auto max-w-shell px-4 md:px-10">
    <span class="font-script font-bold text-gold text-2xl">How it works</span>
    <h2 class="font-display font-extrabold text-3xl md:text-4xl mt-1 mb-10">From Our Menu to Your Hands</h2>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <div class="rounded-3xl border border-white/15 p-7">
        <span class="font-script font-bold text-gold text-xl">step 01</span>
        <h3 class="font-display font-bold text-lg mt-2 mb-2">Browse the menu</h3>
        <p class="text-sm text-white/75">Explore flower, edibles, concentrates and more on the <a href="shop.html" class="text-gold underline underline-offset-2 hover:text-gold-bright">online menu</a>.</p>
      </div>
      <div class="rounded-3xl border border-white/15 p-7">
        <span class="font-script font-bold text-gold text-xl">step 02</span>
        <h3 class="font-display font-bold text-lg mt-2 mb-2">Place your order</h3>
        <p class="text-sm text-white/75">Order ahead online — we start prepping right away.</p>
      </div>
      <div class="rounded-3xl border border-white/15 p-7">
        <span class="font-script font-bold text-gold text-xl">step 03</span>
        <h3 class="font-display font-bold text-lg mt-2 mb-2">Bring a valid ID</h3>
        <p class="text-sm text-white/75">21+ every visit. Everyone gets carded, even you.</p>
      </div>
      <div class="rounded-3xl border border-white/15 p-7">
        <span class="font-script font-bold text-gold text-xl">step 04</span>
        <h3 class="font-display font-bold text-lg mt-2 mb-2">Pick up in store</h3>
        <p class="text-sm text-white/75">Ready in about 15 minutes. Cash &amp; debit, ATM on-site.</p>
      </div>
    </div>
  </div>
</section>

<!-- STORE / VISIT -->
<section class="py-20 bg-surface-low">
  <div class="mx-auto max-w-shell px-4 md:px-10 grid gap-10 lg:grid-cols-2 items-center">
    <div class="grid grid-cols-2 gap-4">
      {img("THC-Cannabis-Store-02.jpg", "rounded-xl shadow-card object-cover h-full w-full col-span-2 aspect-[16/9]")}
      {img("THC-Cannabis-Store.jpg", "rounded-xl shadow-card object-cover aspect-square")}
      {img("THC-Cannabis-Store-03.jpg", "rounded-xl shadow-card object-cover aspect-square")}
    </div>
    <div>
      <span class="sticker-r inline-block bg-forest text-cream font-label font-bold text-xs uppercase tracking-widest px-4 py-1.5 rounded-full mb-5">Visit the Shop</span>
      <h2 class="font-display font-bold text-3xl md:text-4xl text-forest-deep mb-4">A Dispensary Built for the Range</h2>
      <p class="text-ink-soft leading-relaxed mb-6">Walk in and feel the difference: labeled jars you can look at up close, lab-tested products, and budtenders who ask the right questions before recommending anything. Whether you're here for high-THC flower or a gentle CBD tincture, we'll help you find it.</p>
      <ul class="space-y-3 text-sm text-ink mb-8">
        <li class="flex gap-3"><span class="material-symbols-outlined text-forest" aria-hidden="true">verified</span>Every batch lab-tested with certificates of analysis available</li>
        <li class="flex gap-3"><span class="material-symbols-outlined text-forest" aria-hidden="true">group</span>Friendly, judgment-free guidance for first-timers and connoisseurs</li>
        <li class="flex gap-3"><span class="material-symbols-outlined text-forest" aria-hidden="true">local_mall</span>Order ahead online, pick up in store</li>
      </ul>
      <a href="contact.html" class="inline-flex items-center gap-2 bg-forest text-white font-label font-bold uppercase tracking-wider text-sm px-8 py-4 rounded-lg hover:bg-forest-deep hover:shadow-pop transition-all">
        <span class="material-symbols-outlined" aria-hidden="true">location_on</span>Get Directions</a>
    </div>
  </div>
</section>

<!-- EDUCATION TEASER -->
<section class="py-20 bg-surface">
  <div class="mx-auto max-w-shell px-4 md:px-10">
    <div class="text-center mb-12">
      <h2 class="font-display font-bold text-3xl md:text-4xl text-forest-deep">Learn Before You Leaf</h2>
      <p class="text-ink-soft mt-3 max-w-2xl mx-auto">From your first visit to advanced strain knowledge — our education hub covers the effects, benefits, and laws of cannabis in Minnesota.</p>
    </div>
    <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
""" + "".join(f"""
      <a href="{href}" class="group bg-white rounded-xl overflow-hidden shadow-card hover:shadow-pop hover:-translate-y-1 transition-all border border-outline-soft/30">
        <div class="aspect-[16/8] overflow-hidden">{img(im, "h-full w-full object-cover group-hover:scale-105 transition-transform duration-300")}</div>
        <div class="p-5">
          <h3 class="font-display font-bold text-lg text-forest-deep group-hover:text-forest">{label}</h3>
          <p class="text-sm text-ink-soft mt-1">{blurb}</p>
        </div>
      </a>""" for href, label, blurb, im in [
        ("cannabis-101.html", "Cannabis 101", "The plant, THC, terpenes, and how it all works.", "THC-Cannabis-101-Hero.jpg"),
        ("cannabis-for-beginners.html", "Cannabis for Beginners", "Your first visit, your first dose, done right.", "THC-Cannabis-For-Beginers-Hero.jpg"),
        ("cbd-vs-thc.html", "CBD vs THC", "Two cannabinoids, two very different effects.", "CBD-vs-THC-Hero.jpg"),
      ]) + """
    </div>
    <div class="text-center mt-10">
      <a href="education.html" class="inline-flex items-center gap-2 border-2 border-forest text-forest font-label font-bold uppercase tracking-wider text-sm px-8 py-3.5 rounded-lg hover:bg-forest hover:text-white transition-colors">Explore the Education Hub</a>
    </div>
  </div>
</section>

<!-- NEWSLETTER -->
<section class="py-16 bg-forest-deep text-white">
  <div class="mx-auto max-w-3xl px-4 text-center">
    <h2 class="font-display font-bold text-3xl mb-3">Deals, Drops &amp; Dispensary News</h2>
    <p class="text-white/75 mb-8">Join the list for new strain drops, member deals, and education events. No spam — just the good stuff.</p>
    <form class="flex flex-col sm:flex-row gap-3 max-w-lg mx-auto" action="#" method="post">
      <label for="nl-email" class="sr-only">Email address</label>
      <input id="nl-email" type="email" required placeholder="you@example.com" class="flex-1 rounded-lg border-0 bg-white/10 text-white placeholder-white/50 px-5 py-3.5 focus:ring-2 focus:ring-gold"/>
      <button type="submit" class="bg-gold text-forest-deep font-label font-bold uppercase tracking-wider text-sm px-8 py-3.5 rounded-lg hover:bg-gold-bright transition-colors">Sign Up</button>
    </form>
  </div>
</section>
</main>
"""
page("index.html", "Cannabis Dispensary in Hibbing, MN | Hibbing Dispensary",
     "Licensed cannabis dispensary in Hibbing, MN. Legal cannabis for sale — order ahead online for 15-minute pickup. Flower, edibles, concentrates & more. 21+.",
     "home", home_body, "images/Hibbing-Hero.jpg", svc_level="card")

# ============================================================ SHOP
shop_body = f"""
<main id="main">
{hero_banner("THC-Cannabis-Store.jpg", "Live Menu", "Shop the Menu", "Real-time inventory of flower, edibles, concentrates, vapes, pre-rolls, tinctures, and topicals. Order online, pick up in store.")}

<section class="py-16 bg-surface">
  <div class="mx-auto max-w-shell px-4 md:px-10">

    <!--
    ============================================================
    DUTCHIE E-COMMERCE EMBED SLOT
    ============================================================
    Replace everything between the DUTCHIE-START and DUTCHIE-END
    markers below with your Dutchie embed snippet. It typically
    looks like:

      <div id="dutchie--embed__script"></div>
      <script async
        src="https://dutchie.com/api/v2/embedded-menu/YOUR-STORE-ID.js">
      </script>

    Nothing else on this page needs to change.
    ============================================================
    -->
    <!-- DUTCHIE-START -->
    <div id="dutchie-menu-placeholder" class="bg-white rounded-2xl border-2 border-dashed border-forest/30 shadow-card p-10 md:p-16 text-center">
      <span class="material-symbols-outlined text-forest text-6xl mb-4" aria-hidden="true">storefront</span>
      <h2 class="font-display font-bold text-2xl md:text-3xl text-forest-deep mb-3">Online Menu Coming Soon</h2>
      <p class="text-ink-soft max-w-xl mx-auto mb-8">Our live Dutchie ordering menu will appear right here, so you can order ahead and pick up in about 15 minutes. In the meantime, visit us in store or <a href='contact.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>contact us</a> to ask about today's selection of <a href='cannabis-strains.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>strains</a>, edibles, and concentrates.</p>
      <div class="flex flex-wrap justify-center gap-4">
        <a href="contact.html" class="bg-forest text-white font-label font-bold uppercase tracking-wider text-sm px-8 py-3.5 rounded-lg hover:bg-forest-deep transition-colors">Contact Us</a>
        <a href="education.html" class="border-2 border-forest text-forest font-label font-bold uppercase tracking-wider text-sm px-8 py-3.5 rounded-lg hover:bg-forest hover:text-white transition-colors">Learn While You Wait</a>
      </div>
    </div>
    <!-- DUTCHIE-END -->

  </div>
</section>

<!-- CATEGORY PREVIEW -->
<section class="py-16 bg-surface-low border-t border-outline-soft/40">
  <div class="mx-auto max-w-shell px-4 md:px-10">
    <h2 class="font-display font-bold text-3xl text-forest-deep mb-10">What You'll Find on the Shelf</h2>
    <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
""" + "".join(f"""
      <div class="bg-white rounded-xl overflow-hidden shadow-card border border-outline-soft/30">
        <div class="aspect-[4/3] overflow-hidden">{img(im, "h-full w-full object-cover")}</div>
        <div class="p-5">
          <h3 class="font-display font-bold text-lg text-forest-deep">{name}</h3>
          <p class="text-sm text-ink-soft mt-1 leading-relaxed">{blurb}</p>
        </div>
      </div>""" for im, name, blurb in [
        ("THC-Cannabis-02.jpg", "Craft Flower", "Trichome-rich strains across indica, sativa, and hybrid — jarred for freshness and hand-selected by our team."),
        ("THC-Edible-Gummies-02.jpg", "Edibles &amp; Gummies", "Precisely dosed gummies in a variety of flavors. Slow onset, long-lasting effects — perfect for a measured experience."),
        ("THC-Concentrates-03.jpg", "Concentrates", "Live rosin, crumble, and golden extracts for experienced consumers who want full-spectrum potency."),
        ("THC-Vaporizer-02.jpg", "Vapes &amp; Hardware", "Cartridges, tinctures, and devices for clean, convenient inhalation with fast onset."),
      ]) + """
    </div>
  </div>
</section>
</main>
"""
page("shop.html", "Order Cannabis Online in Hibbing, MN | Hibbing Dispensary",
     "Shop our cannabis dispensary menu: flower, edibles, gummies, concentrates, vapes, pre-rolls, tinctures & topicals. Order ahead for in-store pickup in Hibbing, MN.",
     "shop", shop_body, "images/THC-Cannabis-Store.jpg", page_type="CollectionPage", svc_level="card")

# ============================================================ EDUCATION HUB
def edu_card(href, label, blurb, im):
    return f"""
      <a href="{href}" class="group bg-white rounded-xl overflow-hidden shadow-card hover:shadow-pop hover:-translate-y-1 transition-all border border-outline-soft/30">
        <div class="aspect-[16/7] overflow-hidden">{img(im, "h-full w-full object-cover group-hover:scale-105 transition-transform duration-300")}</div>
        <div class="p-6">
          <h2 class="font-display font-bold text-xl text-forest-deep group-hover:text-forest">{label}</h2>
          <p class="text-sm text-ink-soft mt-2 leading-relaxed">{blurb}</p>
          <span class="mt-4 inline-flex items-center gap-1 font-label font-semibold uppercase tracking-wider text-xs text-forest border-b-2 border-gold pb-0.5">Read the Guide<span class="material-symbols-outlined text-sm" aria-hidden="true">arrow_forward</span></span>
        </div>
      </a>"""

edu_body = f"""
<main id="main">
{hero_banner("THC-Cannabis-101-Hero.jpg", "Education Hub", "Cannabis, Explained", "Everything you need to consume with confidence — the plant, the effects, the strains, and the laws that govern cannabis in Minnesota.")}
<section class="py-16 bg-surface">
  <div class="mx-auto max-w-shell px-4 md:px-10">
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {edu_card("cannabis-101.html", "Cannabis 101", "Start at the roots: what cannabis is, how THC and other cannabinoids work, and why onset and consumption method matter.", "THC-Cannabis-101-Hero.jpg")}
      {edu_card("cannabis-for-beginners.html", "Cannabis for Beginners", "Your first dispensary visit and your first dose, step by step — what to ask, what to try, and how to start low and go slow.", "THC-Cannabis-For-Beginers-Hero.jpg")}
      {edu_card("cannabis-strains.html", "Cannabis Strains", "Indica, sativa, hybrid — and why terpenes tell you more. How to find the strains that give you the effects you want.", "THC-Cannabis-Strains-Hero.jpg")}
      {edu_card("cbd-vs-thc.html", "CBD vs THC", "Two famous cannabinoids with very different jobs: one delivers psychoactive effects, the other doesn't. Learn which fits your goals.", "CBD-vs-THC-Hero.jpg")}
      {edu_card("benefits-of-cannabis.html", "Benefits of Cannabis", "From relaxation and sleep to appetite and everyday comfort — what people use cannabis for and how different products deliver.", "Benefits-of-Cannabis-Hero.jpg")}
      {edu_card("cannabis-laws.html", "Cannabis Laws", "Minnesota's adult-use rules in plain English: possession limits, where you can consume, and where to read the actual statutes.", "THC-Cannabis-Hero.jpg")}
    </div>
  </div>
</section>
</main>
"""
page("education.html", "Cannabis Education | Hibbing Dispensary, Hibbing MN",
     "Free cannabis education from Hibbing Dispensary: Cannabis 101, beginner guides, strains, CBD vs THC, benefits of cannabis, and Minnesota cannabis laws.",
     "education", edu_body, "images/THC-Cannabis-101-Hero.jpg", page_type="CollectionPage")

# ============================================================ ARTICLE HELPERS
def article(filename, hero_im, eyebrow, title, sub, sections, next_href, next_label):
    body_sections = ""
    for heading, paras in sections:
        ps = "".join(f'<p class="text-ink-soft leading-relaxed mb-5">{p}</p>' for p in paras)
        body_sections += f'<h2 class="font-display font-bold text-2xl md:text-3xl text-forest-deep mt-12 mb-4">{heading}</h2>{ps}'
    related = [(h, l) for h, l in EDU_LINKS if h != filename][:3]
    related_html = "".join(f"""
      <a href="{h}" class="group bg-white rounded-xl p-5 shadow-card border border-outline-soft/30 hover:shadow-pop hover:-translate-y-0.5 transition-all">
        <h3 class="font-display font-bold text-forest-deep group-hover:text-forest">{l}</h3>
        <span class="mt-2 inline-flex items-center gap-1 font-label font-semibold uppercase tracking-wider text-xs text-forest">Read guide<span class="material-symbols-outlined text-sm" aria-hidden="true">arrow_forward</span></span>
      </a>""" for h, l in related)
    crumbs = [("Home", SITE_URL + "/"), ("Education", url_of("education.html")), (title, url_of(filename))]
    art_node = {"@type": "Article", "@id": url_of(filename) + "#article",
        "headline": title, "description": sub,
        "image": SITE_URL + "/images/" + hero_im, "datePublished": "2026-09-14", "dateModified": "2026-09-14",
        "author": {"@id": SITE_URL + "/#business"}, "publisher": {"@id": SITE_URL + "/#business"},
        "mainEntityOfPage": {"@id": url_of(filename) + "#webpage"}, "inLanguage": "en-US",
        "audience": {"@type": "PeopleAudience", "audienceType": "Adult cannabis consumers", "suggestedMinAge": 21}}
    body = f"""
<main id="main">
{hero_banner(hero_im, eyebrow, title, sub)}
<section class="py-16 bg-surface">
  <div class="mx-auto max-w-3xl px-4 md:px-8">
    <nav aria-label="Breadcrumb" class="mb-8">
      <ol class="flex flex-wrap items-center gap-2 font-label text-xs font-semibold uppercase tracking-wider text-ink-soft">
        <li><a href="index.html" class="hover:text-forest">Home</a></li>
        <li aria-hidden="true" class="text-forest">/</li>
        <li><a href="education.html" class="hover:text-forest">Education</a></li>
        <li aria-hidden="true" class="text-forest">/</li>
        <li aria-current="page" class="text-forest">{title.split(":")[0]}</li>
      </ol>
    </nav>
    <p class="mb-10 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-ink-soft/80 border-l-4 border-gold pl-4 py-1">
      <span class="font-semibold text-forest">Written &amp; reviewed by the Hibbing Dispensary budtender team</span>
      <span aria-hidden="true">·</span><span>Updated September 2026</span>
      <span aria-hidden="true">·</span><span>Educational content — not medical or legal advice</span>
    </p>
    <article>{body_sections}</article>
    <div class="mt-14">
      <h2 class="font-display font-bold text-2xl text-forest-deep mb-5">Keep Learning</h2>
      <div class="grid gap-4 sm:grid-cols-3">{related_html}</div>
    </div>
    <div class="mt-14 bg-forest rounded-2xl p-8 text-white flex flex-col sm:flex-row items-center justify-between gap-6">
      <div>
        <h2 class="font-display font-bold text-xl mb-1">Questions? Ask a budtender.</h2>
        <p class="text-white/75 text-sm">Our team loves helping you find the right product and the right dose.</p>
      </div>
      <div class="flex gap-3 shrink-0">
        <a href="contact.html" class="bg-gold text-forest-deep font-label font-bold uppercase tracking-wider text-xs px-6 py-3 rounded-lg hover:bg-gold-bright transition-colors">Contact Us</a>
        <a href="{next_href}" class="border-2 border-white/50 text-white font-label font-bold uppercase tracking-wider text-xs px-6 py-3 rounded-lg hover:bg-white/10 transition-colors">Next: {next_label}</a>
      </div>
    </div>
  </div>
</section>
</main>
"""
    page(filename, f"{title} — Hibbing Dispensary", sub, "education", body, f"images/{hero_im}", crumbs=crumbs, extra_nodes=[art_node])

# ============================================================ CANNABIS 101
article("cannabis-101.html", "THC-Cannabis-101-Hero.jpg", "Education · Cannabis 101",
  "Cannabis 101: How the Plant Works",
  "The essential guide to cannabis, THC, cannabinoids, and why the way you consume changes everything about the effects you feel.",
  [
    ("Meet the plant", [
      "Cannabis is a flowering plant whose resinous buds contain more than a hundred active compounds called cannabinoids. The two most famous are THC — the compound responsible for cannabis's psychoactive effects — and CBD, which does not produce a high. Alongside cannabinoids, aromatic compounds called terpenes give each strain its distinct smell, flavor, and character.",
      "When you visit <a href='about.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>a dispensary</a>, everything on <a href='shop.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>the shelf</a> — flower, edibles, concentrates, oils, tinctures, and topicals — starts with this same plant. Producers extract, infuse, and craft it into different forms, each with its own onset time, duration, and intensity.",
    ]),
    ("THC, CBD, and the endocannabinoid system", [
      "Your body has a built-in network called the endocannabinoid system that helps regulate mood, appetite, sleep, and pain perception. THC binds directly to receptors in this system, which is why it produces noticeable psychoactive effects — euphoria, relaxation, altered perception, and appetite stimulation. (For a deeper side-by-side, see our <a href='cbd-vs-thc.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>CBD vs THC guide</a>.)",
      "CBD interacts with the same system differently, offering many of the plant's benefits without intoxication. Many products blend the two; the THC:CBD ratio on a label is one of the most useful numbers you can learn to read.",
    ]),
    ("Why consumption method matters", [
      "Inhalation — smoking flower or vaping — delivers cannabinoids through the lungs. Onset arrives within minutes, and effects typically last one to three hours. Because feedback is fast, inhalation makes it easy to dose gradually.",
      "Edibles like gummies take a very different route: your digestive system. Onset can take anywhere from 30 minutes to two hours, and effects can last several hours — often longer and stronger than inhalation. This is why every budtender will tell you to start low and wait before taking more — a rule we unpack in <a href='cannabis-for-beginners.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>Cannabis for Beginners</a>.",
      "Cannabis tinctures are infused oils you drop under the tongue, where cannabinoids absorb through the tissue for a middle-ground onset of about 15 to 45 minutes. Topicals — balms, lotions, and salves you apply directly to the skin — deliver localized benefits and generally do not produce psychoactive effects at all.",
    ]),
    ("Reading a product label", [
      "Every licensed product in Minnesota is lab-tested and labeled with its THC and CBD content. For flower, potency appears as a percentage; for edibles and tinctures, it appears in milligrams per serving. A standard beginner edible dose is 2–5 mg of THC. <a href='contact.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>Ask our team</a> to walk you through any label — that's what we're here for. Ready to browse? The full menu variety lives on our <a href='shop.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>shop page</a>, and our <a href='cannabis-strains.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>strain guide</a> will help you narrow it down.",
    ]),
  ], "cannabis-for-beginners.html", "Cannabis for Beginners")

# ============================================================ BEGINNERS
article("cannabis-for-beginners.html", "THC-Cannabis-For-Beginers-Hero.jpg", "Education · Beginners",
  "Cannabis for Beginners: Your First Visit, Done Right",
  "New to cannabis or coming back after a long break? Here's exactly what to expect, what to ask, and how to have a great first experience.",
  [
    ("Before you arrive", [
      "Bring a valid government-issued ID showing you're 21 or older — you'll need it at the door, no exceptions. Think about what you want from the experience: relaxation, better sleep, social energy, creativity, or relief without a high. The clearer your goal, the better we can guide you. (Not sure how the plant works yet? Skim <a href='cannabis-101.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>Cannabis 101</a> first — five minutes well spent.)",
    ]),
    ("What to ask your budtender", [
      "There are no silly questions at a dispensary. Good ones to start with: What do you recommend for a first-timer? How strong is this, and how much should I take? How long until I feel it, and how long will it last? What's the difference between <a href='cannabis-strains.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>these two strains</a>? Our budtenders will never rush you — take your time and ask everything.",
    ]),
    ("Start low, go slow", [
      "The golden rule of cannabis. If you choose an edible, start with 2–5 mg of THC and wait at least two full hours before considering more — onset is slow, and effects can last several hours. If you choose flower or a vape, take one small inhalation and wait 10–15 minutes to feel the effects before continuing.",
      "It's much easier to take a little more than to undo taking too much. If you ever feel uncomfortably high: you are safe, it will pass. Find a calm place, drink water, eat a snack, and rest — the feeling fades with time.",
    ]),
    ("Beginner-friendly picks", [
      "Low-dose gummies give you precise, repeatable dosing with no smoke. Balanced THC:CBD tinctures let you experiment a few drops at a time. Pre-rolls with moderate THC are an easy, no-equipment way to try flower. And if you want zero psychoactive effects, <a href='cbd-vs-thc.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>CBD-dominant products</a> and topicals let you explore <a href='benefits-of-cannabis.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>the plant's benefits</a> while staying completely clear-headed. When you're ready, you can <a href='shop.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>order ahead online</a> and your pickup will be waiting.",
    ]),
    ("Plan the practical stuff", [
      "Never drive after consuming — arrange a ride or consume at home. Store products in their original child-resistant packaging, away from kids and pets. And under <a href='cannabis-laws.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>Minnesota law</a>, consume on private property, not in public spaces or vehicles.",
    ]),
  ], "cannabis-strains.html", "Cannabis Strains")

# ============================================================ STRAINS
article("cannabis-strains.html", "THC-Cannabis-Strains-Hero.jpg", "Education · Strains",
  "Cannabis Strains: Finding Your Perfect Match",
  "Indica, sativa, hybrid — and the terpenes that actually shape your experience. A guide to navigating the variety on our shelves.",
  [
    ("Indica, sativa, and hybrid", [
      "Traditionally, indica strains are associated with relaxing, body-centered effects — the classic evening wind-down. Sativa strains are associated with uplifting, energetic, head-focused effects that suit daytime and social use. Hybrids blend both parents and make up most of what you'll find on a modern menu, ranging from indica-leaning to sativa-leaning.",
      "These categories are a useful starting point, but they're not the whole story. Two strains labeled 'indica' can feel quite different — which is where terpenes come in.",
    ]),
    ("Terpenes: the flavor and the feel", [
      "Terpenes are the aromatic oils that give strains their smell and contribute to their effects. Myrcene (earthy, musky) leans relaxing. Limonene (citrus) leans bright and mood-lifting. Pinene (pine) is associated with alertness. Caryophyllene (pepper, spice) is studied for soothing properties. Linalool (lavender) leans calming.",
      "Smell is data: when a strain's aroma appeals to you, that's often a good sign. Ask to see and smell our jars — finding your terpene preferences is one of the most enjoyable parts of exploring cannabis.",
    ]),
    ("Potency isn't everything", [
      "It's tempting to shop by THC percentage alone, but a 20% THC strain with the right terpene profile can deliver a far better experience than a 30% strain that doesn't suit you. Consider the full picture: <a href='cannabis-101.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>THC, CBD</a>, terpenes, and how a strain is grown and cured. If intoxication level is your main question, our <a href='cbd-vs-thc.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>CBD vs THC guide</a> covers ratios in depth.",
    ]),
    ("How to explore the variety", [
      "Keep a simple strain journal: note the name, how much you consumed, and how it made you feel. After a few entries, patterns emerge — and our budtenders can use your notes to recommend strains you'll love. New drops arrive regularly, so <a href='shop.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>check the menu</a> often — and if you're brand new to all this, start with our <a href='cannabis-for-beginners.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>beginner's guide</a>.",
    ]),
  ], "cbd-vs-thc.html", "CBD vs THC")

# ============================================================ CBD VS THC
article("cbd-vs-thc.html", "CBD-vs-THC-Hero.jpg", "Education · Cannabinoids",
  "CBD vs THC: What's the Difference?",
  "The two best-known cannabinoids explained side by side — how each feels, what each is used for, and how to choose the right ratio.",
  [
    ("The one-sentence answer", [
      "THC produces the psychoactive effects — the 'high' — while CBD does not; both interact with your body's <a href='cannabis-101.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>endocannabinoid system</a>, but in very different ways.",
    ]),
    ("THC: the psychoactive cannabinoid", [
      "Tetrahydrocannabinol binds directly to CB1 receptors in the brain, producing euphoria, relaxation, altered sensory perception, and appetite stimulation. People reach for THC for recreation, deep relaxation, sleep support, and comfort. Effects depend heavily on dose and consumption method: inhalation hits in minutes and fades within a few hours, while edibles arrive slowly and last several hours. Choosing between <a href='cannabis-strains.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>strains</a> fine-tunes the experience further.",
    ]),
    ("CBD: benefits without the buzz", [
      "Cannabidiol doesn't produce intoxication. People use it for calm, everyday comfort, and recovery while staying fully clear-headed. CBD is available in the same variety of forms — oils, tinctures, gummies, and topicals — and can even soften the intensity of THC when the two are taken together.",
    ]),
    ("Choosing a ratio", [
      "Products are often labeled with a THC:CBD ratio. THC-dominant (like 20:1) delivers the classic psychoactive experience. Balanced (1:1) offers gentler effects with added CBD smoothness — a favorite for newcomers. CBD-dominant (1:20) provides plant benefits with little to no high. If you're unsure, start balanced and adjust from there.",
    ]),
    ("Which is right for you?", [
      "Want the full experience? THC-dominant flower, vapes, or edibles. Want to stay sharp while feeling better? CBD-dominant tinctures or gummies. Want targeted relief on a sore spot? A topical balm applied to the skin — no psychoactive effects at all. Our budtenders can help you <a href='contact.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>dial in the exact ratio</a> for your goals — or browse both THC and CBD options on <a href='shop.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>the menu</a> now.",
    ]),
  ], "benefits-of-cannabis.html", "Benefits of Cannabis")

# ============================================================ BENEFITS
article("benefits-of-cannabis.html", "Benefits-of-Cannabis-Hero.jpg", "Education · Benefits",
  "The Benefits of Cannabis",
  "Why millions of adults include cannabis in their lives — from relaxation and sleep to appetite, comfort, and connection.",
  [
    ("Relaxation and stress relief", [
      "The most common reason adults consume cannabis is simple: unwinding. THC's psychoactive effects can melt the edge off a long day, while CBD offers a calmer, clear-headed version of the same relief. Many people find a small evening dose — a few drops of tincture or a low-dose gummy — becomes their favorite ritual.",
    ]),
    ("Sleep support", [
      "Indica-leaning strains and edibles are popular nighttime companions. Because <a href='cannabis-101.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>edibles last several hours</a>, many consumers prefer them for staying asleep through the night. Terpenes like myrcene and linalool add to the sedating character of certain strains.",
    ]),
    ("Comfort and recovery", [
      "Cannabis has a long history of use for everyday aches and physical comfort. Topicals are a standout here: balms and salves infused with cannabinoids can be applied directly to the skin for localized relief without any psychoactive effects — you can use them any time of day and stay completely clear-headed.",
    ]),
    ("Appetite and enjoyment", [
      "THC famously stimulates appetite and heightens taste and sensory enjoyment — a genuine benefit for people who struggle to eat, and a pleasure for everyone else. Food, music, and nature all get a little more vivid.",
    ]),
    ("Social connection and creativity", [
      "Shared pre-rolls and low-dose edibles have become a social alternative to alcohol for many adults — no hangover, easier moderation. <a href='cannabis-strains.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>Sativa-leaning strains</a> are prized for sparking conversation, laughter, and creative flow.",
    ]),
    ("A note on responsibility", [
      "Benefits come with responsible use: <a href='cannabis-for-beginners.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>know your dose</a>, never drive under the influence per <a href='cannabis-laws.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>Minnesota law</a>, store products away from children and pets, and talk to your doctor if you take medications or have health conditions. Cannabis affects everyone differently — the best experience is an informed one. This page is for education only and isn't medical advice.",
    ]),
  ], "cannabis-laws.html", "Cannabis Laws")

# ============================================================ LAWS
article("cannabis-laws.html", "THC-Cannabis-Hero.jpg", "Education · Minnesota Law",
  "Minnesota Cannabis Laws, in Plain English",
  "What Minnesota's adult-use cannabis law means for you — possession limits, where you can consume, and where to read the official statutes.",
  [
    ("Adult use is legal in Minnesota", [
      "Minnesota legalized adult-use cannabis for people 21 and older. <a href='about.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>Licensed dispensaries like ours</a> sell lab-tested <a href='shop.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>flower, edibles, concentrates, tinctures, and topicals</a> to adults with valid ID. The industry is regulated by the state's Office of Cannabis Management.",
    ]),
    ("The basics every consumer should know", [
      "You must be 21+ with valid ID to purchase or possess cannabis. State law sets limits on how much you can possess in public and at home, and on the potency of edible servings. Consumption is allowed on private property (with the owner's permission) — not in public places, schools, or vehicles. Driving under the influence of cannabis remains illegal, full stop. And transporting cannabis across state lines is prohibited, even to states where it's legal.",
      "Home cultivation of a limited number of plants is also permitted for adults, subject to statutory rules about where and how plants are grown.",
    ]),
    ("Read the actual law", [
      'Rules evolve as the program matures, so go straight to the source. The current statutes live at <a href="https://www.revisor.mn.gov/statutes/cite/342.09" class="text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep" rel="noopener" target="_blank">Minnesota Statutes, Chapter 342 (revisor.mn.gov)</a>, and the <a href="https://mn.gov/ocm/" class="text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep" rel="noopener" target="_blank">Minnesota Office of Cannabis Management</a> publishes consumer guidance, license information, and program updates.',
    ]),
    ("Our commitment to compliance", [
      "Hibbing Dispensary operates in full compliance with Minnesota law: every product is lab-tested, properly labeled, and sold in child-resistant packaging, and every customer is ID-verified at 21+. If you ever have a question about what's legal, <a href='contact.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>ask us</a> — and when in doubt, check the statutes above. This page is a plain-language summary, not legal advice.",
    ]),
  ], "cannabis-101.html", "Cannabis 101")

# ============================================================ ABOUT
about_body = f"""
<main id="main">
{hero_banner("About-Us-page.jpg", "Our Story", "Rooted in Hibbing", "A hometown dispensary built by neighbors, for neighbors — bringing craft cannabis and honest guidance to the Iron Range.")}

<section class="py-20 bg-surface">
  <div class="mx-auto max-w-shell px-4 md:px-10 grid gap-12 lg:grid-cols-2 items-center">
    <div>
      <h2 class="font-display font-bold text-3xl md:text-4xl text-forest-deep mb-5">Why We Opened Our Doors</h2>
      <p class="text-ink-soft leading-relaxed mb-5">Hibbing built itself on hard work, community, and doing things right — and that's exactly how we built this dispensary. When Minnesota opened the door to legal adult-use cannabis, we saw a chance to bring the Range something it deserved: a local shop with lab-tested products, fair prices, and staff who actually take the time to help.</p>
      <p class="text-ink-soft leading-relaxed mb-5">We stock <a href='shop.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>a curated variety</a>, not an overwhelming wall: craft flower from growers we trust, precisely dosed edibles and gummies, small-batch concentrates and oils, tinctures for the no-smoke crowd, and topicals and balms for targeted comfort. New to all of it? Our <a href='education.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>education hub</a> was written for you.</p>
      <p class="text-ink-soft leading-relaxed">Whether it's your first visit or your five-hundredth, you'll get the same welcome — no judgment, no rush, no pressure. We operate fully within <a href='cannabis-laws.html' class='text-forest font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-forest-deep'>Minnesota's adult-use cannabis law</a>, serving Hibbing and Iron Range neighbors within a five-mile radius — from downtown Howard Street to Chisholm and Keewatin.</p>
    </div>
    {img("THC-Cannabis-Store-02.jpg", "rounded-2xl shadow-pop object-cover w-full aspect-[4/3]")}
  </div>
</section>

<section class="py-16 bg-forest text-white">
  <div class="mx-auto max-w-shell px-4 md:px-10">
    <h2 class="font-display font-bold text-3xl mb-10 text-center">What We Stand For</h2>
    <div class="grid gap-6 md:grid-cols-3">
      <div class="bg-forest-deep/60 rounded-xl p-7 border border-gold/20 text-center">
        <span class="material-symbols-outlined text-gold text-4xl mb-3" aria-hidden="true">science</span>
        <h3 class="font-display font-bold text-xl mb-2">Tested &amp; Transparent</h3>
        <p class="text-sm text-white/80 leading-relaxed">Every product on our shelf is lab-tested for potency and purity. Certificates of analysis are available — just ask.</p>
      </div>
      <div class="bg-forest-deep/60 rounded-xl p-7 border border-gold/20 text-center">
        <span class="material-symbols-outlined text-gold text-4xl mb-3" aria-hidden="true">diversity_3</span>
        <h3 class="font-display font-bold text-xl mb-2">Education First</h3>
        <p class="text-sm text-white/80 leading-relaxed">We'd rather teach you to dose confidently than sell you more than you need. Informed customers are customers for life.</p>
      </div>
      <div class="bg-forest-deep/60 rounded-xl p-7 border border-gold/20 text-center">
        <span class="material-symbols-outlined text-gold text-4xl mb-3" aria-hidden="true">home_work</span>
        <h3 class="font-display font-bold text-xl mb-2">Local to the Core</h3>
        <p class="text-sm text-white/80 leading-relaxed">Locally owned, locally staffed, invested in Hibbing. Your dollars stay on the Range.</p>
      </div>
    </div>
  </div>
</section>

<section class="py-20 bg-surface-low">
  <div class="mx-auto max-w-shell px-4 md:px-10 grid gap-12 lg:grid-cols-2 items-center">
    {img("THC-Cannabis-Store-03.jpg", "rounded-2xl shadow-pop object-cover w-full aspect-[4/3] order-last lg:order-first")}
    <div>
      <h2 class="font-display font-bold text-3xl md:text-4xl text-forest-deep mb-5">Come Say Hi</h2>
      <p class="text-ink-soft leading-relaxed mb-8">Browse the jars, smell the strains, ask us anything. We're at 302 E Howard Street in downtown Hibbing, open seven days a week.</p>
      <div class="flex flex-wrap gap-4">
        <a href="contact.html" class="bg-forest text-white font-label font-bold uppercase tracking-wider text-sm px-8 py-4 rounded-lg hover:bg-forest-deep hover:shadow-pop transition-all">Visit &amp; Contact Info</a>
        <a href="shop.html" class="border-2 border-forest text-forest font-label font-bold uppercase tracking-wider text-sm px-8 py-4 rounded-lg hover:bg-forest hover:text-white transition-colors">Browse the Menu</a>
      </div>
    </div>
  </div>
</section>
</main>
"""
page("about.html", "About Our Cannabis Dispensary | Hibbing, MN",
     "Hibbing Dispensary is a locally owned, OCM-licensed cannabis dispensary in Hibbing, Minnesota — lab-tested products, education-first budtenders, Iron Range roots.",
     "about", about_body, "images/About-Us-page.jpg", page_type="AboutPage")

# ============================================================ CONTACT
contact_body = f"""
<main id="main">
{hero_banner("THC-Cannabis-Store-02.jpg", "Get in Touch", "Visit Hibbing Dispensary", "Stop by the shop, give us a call, or send a note — we're happy to answer questions about products, dosing, or anything cannabis.")}

<section class="py-16 bg-surface">
  <div class="mx-auto max-w-shell px-4 md:px-10 grid gap-8 lg:grid-cols-3">
    <div class="bg-white rounded-xl shadow-card border border-outline-soft/30 p-7">
      <span class="material-symbols-outlined text-gold text-3xl mb-3" aria-hidden="true">location_on</span>
      <h2 class="font-display font-bold text-xl text-forest-deep mb-2">Visit the Shop</h2>
      <address class="not-italic text-sm text-ink-soft leading-relaxed">302 E Howard Street<br/>Hibbing, MN 55746</address>
      <p class="text-xs text-ink-soft/80 mt-2">Downtown on Howard Street — a short walk from the Greyhound Bus Museum, serving Hibbing, Chisholm, Keewatin, and neighbors within 5 miles.</p>
      <p class="text-sm text-ink-soft mt-3">Mon–Sat 10am–9pm<br/>Sun 11am–6pm</p>
      <p class="text-xs text-ink-soft/70 mt-3">Valid 21+ ID required at the door.</p>
    </div>
    <div class="bg-white rounded-xl shadow-card border border-outline-soft/30 p-7">
      <span class="material-symbols-outlined text-gold text-3xl mb-3" aria-hidden="true">call</span>
      <h2 class="font-display font-bold text-xl text-forest-deep mb-2">Call Us</h2>
      <p class="text-sm text-ink-soft leading-relaxed">Questions about today's menu, dosing, or an order?</p>
      <a href="tel:+12180000000" class="mt-3 inline-block font-label font-bold text-forest text-lg hover:text-forest-deep">(218) 000-0000</a>
    </div>
    <div class="bg-white rounded-xl shadow-card border border-outline-soft/30 p-7">
      <span class="material-symbols-outlined text-gold text-3xl mb-3" aria-hidden="true">mail</span>
      <h2 class="font-display font-bold text-xl text-forest-deep mb-2">Email &amp; Lab Certs</h2>
      <p class="text-sm text-ink-soft leading-relaxed">General inquiries and certificate-of-analysis requests:</p>
      <a href="mailto:hello@hibbingdispensary.com" class="mt-3 inline-block font-label font-semibold text-forest hover:text-forest-deep break-all">hello@hibbingdispensary.com</a>
    </div>
  </div>
</section>

<section id="contact-form" class="py-16 bg-surface-low border-t border-outline-soft/40">
  <div class="mx-auto max-w-3xl px-4 md:px-8">
    <h2 class="font-display font-bold text-3xl text-forest-deep mb-2">Send Us a Note</h2>
    <p class="text-ink-soft mb-8">We usually reply within one business day.</p>
    <!-- FORM HANDLER: point the action at your form service (e.g. Formspree,
         Cloudflare Workers, or Web3Forms) to receive submissions. -->
    <form action="#" method="post" class="grid gap-5 sm:grid-cols-2">
      <div>
        <label for="f-name" class="block font-label font-semibold text-xs uppercase tracking-wider text-forest mb-2">Name</label>
        <input id="f-name" name="name" type="text" required class="w-full rounded-lg border border-bark/25 bg-cream px-4 py-3 focus:border-forest focus:ring-2 focus:ring-gold/50"/>
      </div>
      <div>
        <label for="f-email" class="block font-label font-semibold text-xs uppercase tracking-wider text-forest mb-2">Email</label>
        <input id="f-email" name="email" type="email" required class="w-full rounded-lg border border-bark/25 bg-cream px-4 py-3 focus:border-forest focus:ring-2 focus:ring-gold/50"/>
      </div>
      <div class="sm:col-span-2">
        <label for="f-topic" class="block font-label font-semibold text-xs uppercase tracking-wider text-forest mb-2">Topic</label>
        <select id="f-topic" name="topic" class="w-full rounded-lg border border-bark/25 bg-cream px-4 py-3 focus:border-forest focus:ring-2 focus:ring-gold/50">
          <option>Product question</option><option>Dosing guidance</option><option>Lab results / COA request</option><option>Careers</option><option>Something else</option>
        </select>
      </div>
      <div class="sm:col-span-2">
        <label for="f-msg" class="block font-label font-semibold text-xs uppercase tracking-wider text-forest mb-2">Message</label>
        <textarea id="f-msg" name="message" rows="5" required class="w-full rounded-lg border border-bark/25 bg-cream px-4 py-3 focus:border-forest focus:ring-2 focus:ring-gold/50"></textarea>
      </div>
      <div class="sm:col-span-2">
        <button type="submit" class="bg-forest text-white font-label font-bold uppercase tracking-wider text-sm px-10 py-4 rounded-lg hover:bg-forest-deep hover:shadow-pop transition-all">Send Message</button>
      </div>
    </form>
  </div>
</section>
</main>
"""
page("contact.html", "Visit Our Cannabis Dispensary in Hibbing, MN | Contact",
     "Visit Hibbing Dispensary at 302 E Howard Street in downtown Hibbing, MN. Hours, directions, phone, email, and lab certificate requests. Open 7 days, 21+.",
     "contact", contact_body, "images/THC-Cannabis-Store-02.jpg", page_type="ContactPage")


# ============================================================ FAQ
# Q&A data is the single source for both the visible page and the
# FAQPage schema (v2 rule: markup must mirror visible content).
FAQS = [
    ("Do I need to be 21 to shop at Hibbing Dispensary?",
     "Yes. Minnesota law requires all customers to be 21 or older with a valid government-issued ID. We check every ID at the door, every visit — no exceptions."),
    ("What forms of payment do you accept?",
     "We accept cash and debit cards, and there is an ATM on-site. Due to federal banking rules, credit cards are not accepted at cannabis dispensaries."),
    ("Can I order ahead for pickup?",
     "Yes. Order through our online menu and your order is typically ready for in-store pickup in about 15 minutes. Bring the same valid 21+ ID you used to order."),
    ("What products do you carry?",
     "We stock a curated variety of lab-tested cannabis: craft flower, edibles and gummies, concentrates and oils, vaporizers and cartridges, pre-rolls, tinctures, and topicals."),
    ("I'm new to cannabis. How much should I take?",
     "Start low and go slow. For edibles, begin with 2 to 5 mg of THC and wait at least two hours before taking more, since onset is slow and effects can last several hours. For flower or vapes, take one small inhalation and wait 10 to 15 minutes. Our budtenders are happy to help you find the right starting dose."),
    ("Are your products lab-tested?",
     "Yes. Every product on our shelf is tested by a licensed laboratory for potency and purity, and certificates of analysis are available on request — just ask a budtender or email us."),
    ("How much cannabis can I legally possess in Minnesota?",
     "Minnesota's adult-use law sets possession limits for public and home storage. Limits can change as rules are updated, so check the current statutes at the Minnesota Office of Cannabis Management or Minnesota Statutes Chapter 342, or read our plain-English cannabis laws guide."),
    ("Where am I allowed to consume cannabis?",
     "On private property with the owner's permission. Consumption is not allowed in public places, schools, or vehicles, and driving under the influence of cannabis is illegal."),
    ("Do you offer delivery?",
     "Not yet — we currently offer in-store shopping and order-ahead pickup. Join our newsletter or follow us for updates as our services grow."),
    ("What cities do you serve?",
     "We're located at 302 E Howard Street in downtown Hibbing and proudly serve Iron Range neighbors within about 10 miles, including Chisholm, Buhl, and Keewatin."),
]

faq_items_html = "".join(f"""
      <details class="group bg-white rounded-xl shadow-card border border-outline-soft/30 overflow-hidden">
        <summary class="flex items-center justify-between gap-4 cursor-pointer list-none px-6 py-5 font-display font-bold text-lg text-forest-deep hover:text-forest [&::-webkit-details-marker]:hidden">
          {q}
          <span class="material-symbols-outlined text-gold shrink-0 transition-transform group-open:rotate-180" aria-hidden="true">expand_more</span>
        </summary>
        <p class="px-6 pb-6 text-ink-soft leading-relaxed">{a}</p>
      </details>""" for q, a in FAQS)

faq_body = f"""
<main id="main">
{hero_banner("THC-Cannabis-Store-03.jpg", "Good Questions", "Frequently Asked Questions", "Straight answers about shopping with us, dosing, payment, and Minnesota cannabis rules.")}
<section class="py-16 bg-surface">
  <div class="mx-auto max-w-3xl px-4 md:px-8">
    <div class="space-y-4">{faq_items_html}</div>
    <div class="mt-14 bg-forest rounded-2xl p-8 text-white flex flex-col sm:flex-row items-center justify-between gap-6">
      <div>
        <h2 class="font-display font-bold text-xl mb-1">Didn't find your answer?</h2>
        <p class="text-white/75 text-sm">Ask us directly — no question is too basic, and our <a href="education.html" class="text-gold-bright font-semibold underline decoration-gold decoration-2 underline-offset-2 hover:text-white">education hub</a> goes deeper on every topic.</p>
      </div>
      <a href="contact.html" class="shrink-0 bg-gold text-forest-deep font-label font-bold uppercase tracking-wider text-xs px-6 py-3 rounded-lg hover:bg-gold-bright transition-colors">Contact Us</a>
    </div>
  </div>
</section>
</main>
"""
faq_schema_props = {"mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
    for q, a in FAQS]}
page("faq.html", "Dispensary FAQ | Hibbing Dispensary, Hibbing MN",
     "Answers to common questions about shopping at Hibbing Dispensary: 21+ ID rules, cash and debit payment, order-ahead pickup, dosing for beginners, lab testing, and Minnesota cannabis law.",
     "contact", faq_body, "images/THC-Cannabis-Store-03.jpg",
     page_type="FAQPage",
     crumbs=[("Home", SITE_URL + "/"), ("Contact", url_of("contact.html")), ("FAQ", url_of("faq.html"))],
     webpage_props=faq_schema_props)

# ============================================================ LEGAL PAGES
def legal_page(filename, title, intro, sections):
    body_sections = ""
    for h, ps in sections:
        body_sections += f'<h2 class="font-display font-bold text-2xl text-forest-deep mt-10 mb-3">{h}</h2>' + \
            "".join(f'<p class="text-ink-soft leading-relaxed mb-4 text-sm md:text-base">{p}</p>' for p in ps)
    body = f"""
<main id="main">
<section class="bg-forest-deep py-16">
  <div class="mx-auto max-w-3xl px-4 md:px-8">
    <h1 class="font-display font-extrabold text-white text-4xl md:text-5xl">{title}</h1>
    <p class="text-white/70 mt-3 text-sm">Last updated: September 2026</p>
  </div>
</section>
<section class="py-14 bg-surface">
  <div class="mx-auto max-w-3xl px-4 md:px-8">
    <p class="text-ink-soft leading-relaxed">{intro}</p>
    {body_sections}
  </div>
</section>
</main>
"""
    page(filename, f"{title} — Hibbing Dispensary", intro[:150], "", body)

legal_page("privacy-policy.html", "Privacy Policy",
  "Hibbing Dispensary respects your privacy. This policy explains what information we collect, how we use it, and the choices you have. This is a template policy — review it with your legal counsel before launch.",
  [
    ("Information we collect", [
      "We collect information you provide directly, such as your name and email when you contact us or join our mailing list, and age-verification confirmation when you enter the site. When you place an online order through our menu provider, that provider collects order and identity information under its own privacy policy.",
      "Like most websites, we and our service providers may automatically collect basic technical data such as browser type, pages visited, and approximate location for analytics and site security.",
    ]),
    ("How we use information", [
      "We use your information to respond to inquiries, fulfill orders, send communications you've opted into, comply with Minnesota cannabis regulations (including age verification), and improve our website and services. We do not sell your personal information.",
    ]),
    ("Sharing", [
      "We share information only with service providers who help us operate (such as our e-commerce menu provider, email service, and web host), and when required by law or regulation.",
    ]),
    ("Your choices", [
      "You can unsubscribe from marketing emails at any time using the link in any message. To request access to or deletion of your personal information, contact us at hello@hibbingdispensary.com.",
    ]),
    ("Contact", [
      "Questions about this policy? Email hello@hibbingdispensary.com or write to Hibbing Dispensary, 302 E Howard Street, Hibbing, MN 55746.",
    ]),
  ])

legal_page("terms.html", "Terms &amp; Conditions",
  "By using this website, you agree to these terms. This is a template — review it with your legal counsel before launch.",
  [
    ("Age requirement", [
      "This website and our products are intended solely for adults 21 years of age and older. By using this site you confirm that you are at least 21 years old. Valid government-issued identification is required for all purchases.",
    ]),
    ("Legal compliance", [
      "Hibbing Dispensary operates under Minnesota's adult-use cannabis laws (Minnesota Statutes, Chapter 342) and the rules of the Minnesota Office of Cannabis Management. Products may not be transported across state lines. It is illegal to drive under the influence of cannabis.",
    ]),
    ("Product information", [
      "Content on this site, including education articles, is provided for general information only and is not medical or legal advice. Cannabis products have intoxicating psychoactive effects and affect individuals differently. Consult a healthcare professional before use, particularly if you are pregnant, nursing, taking medication, or have a medical condition.",
    ]),
    ("Orders", [
      "Online orders are processed through our third-party menu provider and are subject to its terms of service. All sales are subject to identity and age verification at pickup. We reserve the right to refuse service as permitted by law.",
    ]),
    ("Intellectual property", [
      "All content on this site — text, images, and branding — is the property of Hibbing Dispensary or its licensors and may not be reproduced without permission.",
    ]),
    ("Limitation of liability", [
      "To the fullest extent permitted by law, Hibbing Dispensary is not liable for indirect or consequential damages arising from use of this website. These terms are governed by the laws of the State of Minnesota.",
    ]),
  ])

legal_page("equal-opportunity.html", "Equal Opportunity Employer",
  "Hibbing Dispensary is proud to be an equal opportunity employer committed to building a team that reflects the community we serve.",
  [
    ("Our commitment", [
      "We provide equal employment opportunities to all employees and applicants without regard to race, color, religion, sex, sexual orientation, gender identity, national origin, age, disability, veteran status, marital status, or any other characteristic protected by federal, state, or local law.",
      "This commitment applies to all aspects of employment: recruiting, hiring, training, promotion, compensation, benefits, and termination.",
    ]),
    ("Accessibility", [
      "We are committed to providing reasonable accommodations to qualified individuals with disabilities throughout the application process and employment. To request an accommodation, contact hello@hibbingdispensary.com.",
    ]),
    ("Join the team", [
      "Interested in working with us? Send your resume and a short note to hello@hibbingdispensary.com with the subject line 'Careers'. Applicants must be 21 or older per Minnesota cannabis regulations.",
    ]),
  ])

# ============================================================ SITEMAP PAGE + XML
ALL_PAGES = [
  ("index.html", "Home"), ("shop.html", "Shop"), ("education.html", "Education Hub"),
  ("cannabis-101.html", "Cannabis 101"), ("cannabis-for-beginners.html", "Cannabis for Beginners"),
  ("cannabis-strains.html", "Cannabis Strains"), ("cbd-vs-thc.html", "CBD vs THC"),
  ("benefits-of-cannabis.html", "Benefits of Cannabis"), ("cannabis-laws.html", "Cannabis Laws"),
  ("about.html", "About Us"), ("contact.html", "Contact"), ("faq.html", "FAQ"),
  ("privacy-policy.html", "Privacy Policy"), ("terms.html", "Terms &amp; Conditions"),
  ("equal-opportunity.html", "Equal Opportunity Employer"), ("sitemap.html", "Sitemap"),
]
groups = [
  ("Main", ALL_PAGES[0:3] + ALL_PAGES[9:12]),
  ("Education", ALL_PAGES[3:9]),
  ("Legal", ALL_PAGES[12:16]),
]
sitemap_cols = "".join(f"""
    <div>
      <h2 class="font-display font-bold text-xl text-forest-deep mb-4">{g}</h2>
      <ul class="space-y-2">{"".join(f'<li><a href="{h}" class="text-ink-soft hover:text-forest font-medium">{l}</a></li>' for h, l in items)}</ul>
    </div>""" for g, items in groups)
sitemap_body = f"""
<main id="main">
<section class="bg-forest-deep py-16">
  <div class="mx-auto max-w-shell px-4 md:px-10">
    <h1 class="font-display font-extrabold text-white text-4xl md:text-5xl">Sitemap</h1>
    <p class="text-white/70 mt-3">Every page on hibbingdispensary — in one place.</p>
  </div>
</section>
<section class="py-14 bg-surface">
  <div class="mx-auto max-w-shell px-4 md:px-10 grid gap-10 md:grid-cols-3">{sitemap_cols}</div>
</section>
</main>
"""
page("sitemap.html", "Sitemap — Hibbing Dispensary", "A complete map of all pages on the Hibbing Dispensary website.", "", sitemap_body)

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for h, _ in ALL_PAGES:
    xml += f"  <url><loc>{url_of(h)}</loc></url>\n"
xml += "</urlset>\n"
with open(os.path.join(OUT, "sitemap.xml"), "w") as f: f.write(xml)
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print("built: sitemap.xml, robots.txt")

# ============================================================
# v2 AUTOMATED INTEGRITY CHECK — fails the build on any
# dangling @id, invalid JSON-LD, or multiple graphs per page
# ============================================================
import re as _re2, glob as _glob

def _collect_ids(obj, defined, referenced):
    if isinstance(obj, dict):
        keys = set(obj.keys())
        if "@id" in obj:
            if keys - {"@id"}:
                defined.add(obj["@id"])
            else:
                referenced.add(obj["@id"])
        for v in obj.values():
            _collect_ids(v, defined, referenced)
    elif isinstance(obj, list):
        for v in obj:
            _collect_ids(v, defined, referenced)

failures = []
for f in sorted(_glob.glob(os.path.join(OUT, "*.html"))):
    html = open(f).read()
    scripts = _re2.findall(r'<script type="application/ld\+json">(.*?)</script>', html, _re2.S)
    if len(scripts) != 1:
        failures.append(f"{os.path.basename(f)}: expected exactly 1 JSON-LD @graph, found {len(scripts)}")
        continue
    try:
        data = json.loads(scripts[0])
    except Exception as e:
        failures.append(f"{os.path.basename(f)}: JSON parse error: {e}")
        continue
    if "@graph" not in data:
        failures.append(f"{os.path.basename(f)}: missing @graph wrapper")
        continue
    defined, referenced = set(), set()
    _collect_ids(data["@graph"], defined, referenced)
    dangling = referenced - defined
    if dangling:
        failures.append(f"{os.path.basename(f)}: dangling @id refs: {sorted(dangling)}")

if failures:
    raise SystemExit("SCHEMA INTEGRITY FAILED:\n" + "\n".join(failures))
print(f"schema integrity: OK ({len(_glob.glob(os.path.join(OUT, '*.html')))} pages, 1 @graph each, no dangling @ids)")
