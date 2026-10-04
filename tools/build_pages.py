#!/usr/bin/env python3
"""Regenerates about/contact/privacy/terms from the shared shell in index.html (header, menu, footer)
and the original page content kept in tools/orig/. Run from the repo root: python3 tools/build_pages.py"""
import re,json,html,os
from bs4 import BeautifulSoup
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx=open(f'{R}/index.html').read()
SHELL_TOP=idx[idx.index('<a class="skip"'):idx.index('<main id="main">')]
SHELL_BOT=idx[idx.index('<footer class="ftr">'):idx.index('</body>')]
WA=re.search(r'<path d="(M17\.472[^"]*)"',idx).group(1)
def fix_links(s):
    return s.replace('href="#products"','href="/#products"').replace('href="#ventures"','href="/#ventures"').replace('href="#about"','href="/about.html"')
def shell(page):
    top=fix_links(SHELL_TOP)
    cur={'about':'about.html','contact':'contact.html'}.get(page)
    if cur:
        top=top.replace(f'<a href="{cur}">',f'<a href="{cur}" aria-current="page">',1)
        top=top.replace(f'<a class="l" href="{cur}">',f'<a class="l" href="{cur}" aria-current="page">',1)
    return top,fix_links(SHELL_BOT)
def head(title,desc,path,page_type,extra_ld=None,noindex=False):
    url=f'https://www.laafstyl.org/{path}'
    ld={"@context":"https://schema.org","@graph":[
      {"@type":page_type,"@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"en-ZA",
       "isPartOf":{"@id":"https://www.laafstyl.org/#website"},"about":{"@id":"https://www.laafstyl.org/#org"},
       "breadcrumb":{"@id":url+"#crumbs"}},
      {"@type":"BreadcrumbList","@id":url+"#crumbs","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://www.laafstyl.org/"},
        {"@type":"ListItem","position":2,"name":title.split(' | ')[0].split(':')[0],"item":url}]}]}
    if extra_ld: ld["@graph"].append(extra_ld)
    t=html.escape(title,quote=True); d=html.escape(desc,quote=True)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="author" content="LaafStyl, a trading name of BROD Traders (Pty) Ltd">
<meta name="theme-color" content="#0c0e0d">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="LaafStyl">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_ZA">
<meta property="og:image" content="https://www.laafstyl.org/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="https://www.laafstyl.org/assets/og.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css?v=20261004">
<script type="application/ld+json">
{json.dumps(ld,indent=1,ensure_ascii=False)}
</script>
</head>
<body>
'''
def page(name,title,desc,path,ptype,main,noindex=False,extra_ld=None):
    top,bot=shell(name)
    out=head(title,desc,path,ptype,extra_ld,noindex)+top+'<main id="main">\n'+main+'\n</main>\n\n'+bot+'</body>\n</html>\n'
    open(f'{R}/{path}','w').write(out)
    print('wrote',path,len(out))
def hero(h1,lead,crumb,sub=None):
    s=''.join(f'<span>{x}</span>' for x in (sub or []))
    return f'''<section class="phero"><div class="container">
<p class="crumb"><a href="/">Home</a><span aria-hidden="true">/</span>{crumb}</p>
<h1>{h1}</h1>
{f'<p class="lead">{lead}</p>' if lead else ''}
{f'<p class="sub">{s}</p>' if sub else ''}
</div></section>
<div class="flagbar" aria-hidden="true"><span></span><span></span><span></span><span></span></div>'''
CTA=lambda h,p:f'''<section class="cta" aria-labelledby="h-cta"><div class="container">
<h2 id="h-cta">{h}</h2><p>{p}</p>
<div class="hero-cta"><a class="btn btn-wa" href="https://wa.me/27636691391?text=Hi%20LaafStyl%2C%20I%27d%20like%20to%20get%20in%20touch" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="{WA}"/></svg>WhatsApp 063 669 1391</a>
<a class="btn btn-ghost" href="mailto:laafstylfamily@gmail.com">laafstylfamily@gmail.com</a></div></div></section>'''

# ---------------- about ----------------
about_main=hero('Straight out of 7357',"LaafStyl didn't start in a boardroom. It started on a street in Langebaan, with a group of friends from different families and backgrounds who shared a postcode and a drive to build something real.",'About')+'''
<section class="sec" aria-labelledby="h-story"><div class="container split">
<div class="prose rv">
<h2 id="h-story">From one street to four products</h2>
<p>It started as a social club that the group called <strong>Lifestyle Family</strong>: teenagers in Langebaan, living on the same street, from completely different backgrounds. What pulled them together was proximity and, in time, real friendship.</p>
<p>As they grew up the name evolved into <strong>LaafStyl</strong>, and the question changed from "what are we doing this weekend" to "what if we actually built something?"</p>
<p>Today LaafStyl is a trading name of <strong>BROD Traders (Pty) Ltd</strong>, based in Langebaan. We make websites for small businesses, a WhatsApp AI assistant, a shuttle service and a podcast, and we run two local businesses alongside them. We are open to working with other companies and creatives who share our values: build real things, serve real people, do not overcomplicate it.</p>
</div>
<ol class="tl rv" style="--i:1" aria-label="Timeline">
<li><b>2014</b><h3>Lifestyle Family</h3><p>A group of teenagers on one street in Langebaan start an informal social club.</p></li>
<li><b>2018</b><h3>The name becomes LaafStyl</h3><p>The group settles on the name LaafStyl and starts combining its skills.</p></li>
<li><b>2025</b><h3>BROD Traders registered</h3><p>BROD Traders (Pty) Ltd, registration 2025/529742/07, is registered in Langebaan and LaafStyl becomes its trading name.</p></li>
<li><b>2026</b><h3>Four products, two ventures</h3><p>LaafWeb, LaafConnect, LaafShuttle and LaafEntertain are live, alongside Bright Beginners and ChromeWorkx.</p></li>
</ol></div></section>

<section class="sec sec-alt" aria-labelledby="h-why"><div class="container">
<div class="sec-hd"><h2 id="h-why">Why we build</h2></div>
<p class="mission rv">To simplify and elevate modern living with practical digital tools, creative entertainment and reliable lifestyle services.</p>
<div class="grid4" style="margin-top:34px">
<div class="mini rv" style="--i:0"><h3>Built in South Africa</h3><p>Shaped by our own languages, infrastructure and way of doing things.</p></div>
<div class="mini rv" style="--i:1"><h3>Open to collaboration</h3><p>If your skills complement ours, let us talk. We grow faster together.</p></div>
<div class="mini rv" style="--i:2"><h3>Practical over perfect</h3><p>We ship things that work, then keep improving them with our customers.</p></div>
<div class="mini rv" style="--i:3"><h3>Built to last</h3><p>LaafStyl turns the skills of our team into products and businesses that can sustain themselves.</p></div>
</div></div></section>

<section class="sec" aria-labelledby="h-crew"><div class="container">
<div class="sec-hd"><h2 id="h-crew">Same street, different skills</h2><p>We started as neighbours and we are still a crew.</p></div>
<div class="grid4">
<div class="mini rv" style="--i:0"><h3>Brydon</h3><span class="role">Web and product</span><p>Builds and runs LaafWeb: front-end, design and client delivery.</p></div>
<div class="mini rv" style="--i:1"><h3>Reekay</h3><span class="role">Operations</span><p>Part of the LaafStyl family since the beginning. Keeps things running.</p></div>
<div class="mini rv" style="--i:2"><h3>Andrew</h3><span class="role">Creative</span><p>Brings the creative side: entertainment, content and culture.</p></div>
<div class="mini rv" style="--i:3"><h3>Keenan</h3><span class="role">Strategy</span><p>Thinks about where LaafStyl is going: long-term vision and partnerships.</p></div>
</div>
<div class="rowlinks"><a class="btn btn-ghost btn-sm" href="/#products">See our products</a><a class="btn btn-ghost btn-sm" href="contact.html">Contact us</a></div>
</div></section>
'''+CTA('Want to work with us?','Message us on WhatsApp or send an email and tell us what you have in mind.')
page('about','About LaafStyl: a Langebaan crew building digital products','LaafStyl started as a group of friends on one street in Langebaan. Today it is a trading name of BROD Traders (Pty) Ltd, making websites, WhatsApp AI, a shuttle service and a podcast.','about.html','AboutPage',about_main)

# ---------------- contact ----------------
contact_main=hero('Get in touch',"We are based in Langebaan on the West Coast of South Africa. WhatsApp is the fastest way to reach us.",'Contact')+f'''
<section class="sec" aria-labelledby="h-main"><div class="container split">
<div>
<h2 id="h-main" class="h2">Talk to LaafStyl</h2>
<p class="prose">For general enquiries, new projects and anything that does not fit neatly into one product, use the main line.</p>
<div class="contact-card rv" style="margin-top:26px"><dl>
<div><dt>WhatsApp and calls</dt><dd><a href="tel:+27636691391">063 669 1391</a><small>General enquiries, new projects, collaborations</small></dd></div>
<div><dt>Email</dt><dd><a href="mailto:laafstylfamily@gmail.com">laafstylfamily@gmail.com</a><small>Proposals, partnerships, formal correspondence. We aim to reply within 24 hours.</small></dd></div>
<div><dt>Where</dt><dd>Langebaan, Western Cape, 7357<small>Most work is done remotely over WhatsApp</small></dd></div>
<div><dt>Hours</dt><dd>Monday to Friday, 8am to 6pm<small>English and Afrikaans spoken</small></dd></div>
</dl>
<div class="hero-cta"><a class="btn btn-wa" href="https://wa.me/27636691391?text=Hi%20LaafStyl%2C%20I%27d%20like%20to%20get%20in%20touch" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="{WA}"/></svg>WhatsApp LaafStyl</a></div></div>
</div>
<div style="display:grid;gap:14px">
<div class="mini rv" style="--i:0"><h3>Websites (LaafWeb)</h3><p>One-page websites for small businesses, from R949 once-off plus R79 a month. Start at <a href="https://web.laafstyl.org">web.laafstyl.org</a>, or contact Brydon on <a href="tel:+27630096779" style="color:var(--ink)">063 009 6779</a>.</p></div>
<div class="mini rv" style="--i:1"><h3>WhatsApp AI (LaafConnect)</h3><p>Questions about the WhatsApp assistant? Message the main line or register at <a href="https://register.laafstyl.org">register.laafstyl.org</a>.</p></div>
<div class="mini rv" style="--i:2"><h3>Shuttle (LaafShuttle)</h3><p>Get a quote and book at <a href="https://shuttle.laafstyl.org">shuttle.laafstyl.org</a>. For route and operator questions call Keenan on <a href="tel:+27827286274" style="color:var(--ink)">082 728 6274</a>.</p></div>
<div class="mini rv" style="--i:3"><h3>Podcast and events (LaafEntertain)</h3><p>Andrew on <a href="tel:+27813163711" style="color:var(--ink)">081 316 3711</a>, or Reekay on <a href="tel:+27738153845" style="color:var(--ink)">073 815 3845</a> for music and entertainment.</p></div>
</div></div></section>

<section class="sec sec-alt" aria-labelledby="h-collab"><div class="container prose">
<h2 id="h-collab" class="h2">Open to collaboration</h2>
<p>We are looking for partners: companies, creatives, developers and organisations who want to build something real. If you have skills, markets or ideas that complement what we do, send us an email.</p>
<div class="rowlinks"><a class="btn btn-ghost" href="mailto:laafstylfamily@gmail.com">Email us</a></div>
</div></section>
'''
page('contact','Contact LaafStyl: WhatsApp 063 669 1391, Langebaan','Contact LaafStyl in Langebaan, Western Cape. WhatsApp 063 669 1391 or email laafstylfamily@gmail.com for websites, WhatsApp AI, shuttle bookings and the podcast.','contact.html','ContactPage',contact_main)

# ---------------- legal docs ----------------
def doc(name,cls,secclass,textclass,title,desc,path):
    s=BeautifulSoup(open(f'{R}/tools/orig/{name}.html').read(),'html.parser')
    h1=s.select_one('h1').get_text(' ',strip=True)
    sub=[x.get_text(' ',strip=True) for x in s.select('.hero-sub span') if 'dot' not in (x.get('class') or [])]
    intro=s.select_one('.priv-intro,.terms-intro')
    popia=s.select_one('.popia-bar')
    toc=[(a.get('href'),a.get_text(' ',strip=True)) for a in s.select('.priv-toc-links a,.terms-toc-links a')]
    secs=[]
    for sec in s.select(f'.{secclass}'):
        t=sec.select_one('.section-title').get_text(' ',strip=True)
        body=sec.select_one(f'.{textclass}')
        for tb in body.select('table'):
            w=s.new_tag('div'); w['class']='tbl'; tb.wrap(w)
        secs.append((sec.get('id'),t,body.decode_contents()))
    intro_html=intro.decode_contents() if intro else ''
    if popia:
        intro_html+=f'<p><strong>{popia.select_one(".popia-bar-title").get_text(" ",strip=True)}.</strong> {popia.select_one(".popia-bar-desc").get_text(" ",strip=True)}</p>'
    out=hero(h1,None,h1,sub)+'<section class="sec"><div class="container"><div class="doc">\n'
    out+=f'<div class="intro">{intro_html}</div>\n'
    out+='<nav class="toc" aria-labelledby="h-toc"><h2 id="h-toc">Contents</h2><div>'+''.join(f'<a href="{h}">{html.escape(t)}</a>' for h,t in toc)+'</div></nav>\n'
    for i,t,b in secs:
        t=re.sub(r'^\d+\.\s*','',t)
        out+=f'<section class="dsec" id="{i}"><h2>{html.escape(t)}</h2>\n{b}\n</section>\n'
    out+='</div></div></section>'
    page(name,title,desc,path,'WebPage',out)
doc('privacy','priv','priv-section','priv-text','Privacy Policy | LaafStyl','How BROD Traders (Pty) Ltd, trading as LaafStyl, collects, uses, stores and protects personal information under POPIA.','privacy.html')
doc('terms','terms','terms-section','terms-text','Terms of Service | LaafStyl','The terms that apply to LaafStyl products and services operated by BROD Traders (Pty) Ltd, trading as LaafStyl, Langebaan.','terms.html')
