"""HomeDecorPad — theme: CSS, inline SVG art, page shell.

Everything the site needs is inlined into each page on purpose:
the site works with zero external CSS/JS/font dependencies.
"""
import itertools, os

_n = itertools.count(1)
def uid():
    return f"a{next(_n)}"

BRAND = "HomeDecorPad"
SOCIAL = {}
ADSENSE_CLIENT = ""
GA4_ID = ""
PINTEREST_VERIFY = ""
FORMSPREE_ID = "YOUR_FORM_ID"
AMAZON_TAG = "YOUR-AMAZON-TAG-20"
HOME = {}
NAV = {}
FOOTER = {}
PAGES = {}
# Giscus comments — set from content/site.yml via build.py
GISCUS_ENABLED = False
GISCUS_REPO = "RedLaxx/homedecorpad-site"
GISCUS_REPO_ID = "R_kgDOUoGanw"
GISCUS_CATEGORY = "General"
GISCUS_CATEGORY_ID = ""
GISCUS_MAPPING = "pathname"
GISCUS_THEME = "light"
# Cusdis anonymous comments
COMMENT_SYSTEM = "giscus"
CUSDIS_ENABLED = False
CUSDIS_APP_ID = ""
CUSDIS_HOST = "https://cusdis.com"
CUSDIS_THEME = "light"
# Canonical domain. Override when deploying elsewhere, e.g.:
#   SITE_DOMAIN="https://redlaxx.github.io/HomeDecorPad" python3 _build/build.py
DOMAIN = os.environ.get("SITE_DOMAIN", "https://homedecorpad.com").rstrip("/")
EMAIL = "hello@homedecorpad.com"

# --------------------------------------------------------------------------- CSS
CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
:root{
 --bg:#FBF8F3;--paper:#FFFFFF;--oat:#F1E8DB;--sand:#E4D8C7;--line:#E9DFD0;
 --terra:#B5533C;--terra-d:#95402D;--olive:#6E7B5A;--brass:#C08B48;
 --ink:#2B2622;--muted:#6F645B;--max:1180px;--r:14px;
 --shadow:0 10px 30px rgba(70,50,30,.07);
 --serif:"DM Serif Display",Georgia,"Times New Roman",serif;
 --sans:Poppins,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16.5px;line-height:1.72}
img,svg{max-width:100%;display:block}
h1,h2,h3,h4{font-family:var(--serif);font-weight:400;line-height:1.2;margin:0 0 .5em;letter-spacing:.2px}
h1{font-size:clamp(30px,4.4vw,46px)}
h2{font-size:clamp(23px,3vw,30px);margin-top:1.7em}
h3{font-size:21px;margin-top:1.4em}
h4{font-size:18px}
p{margin:0 0 1.15em}
a{color:var(--terra-d);text-decoration:none;border-bottom:1px solid rgba(181,83,60,.3)}
a:hover{color:var(--terra);border-bottom-color:var(--terra)}
ul,ol{padding-left:22px;margin:0 0 1.2em}
li{margin:.42em 0}
li::marker{color:var(--terra)}
hr{border:0;border-top:1px solid var(--line);margin:36px 0}
table{width:100%;border-collapse:collapse;margin:24px 0;font-size:15px}
th,td{border:1px solid var(--line);padding:11px 13px;text-align:left;vertical-align:top}
th{background:var(--oat);font-weight:600;font-size:14px}
blockquote{margin:26px 0;padding:8px 0 8px 22px;border-left:3px solid var(--sand);color:var(--muted);font-style:italic}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;background:var(--oat);padding:2px 6px;border-radius:5px}
:focus-visible{outline:2px solid var(--terra);outline-offset:2px}
.skip{position:absolute;left:-9999px}
.skip:focus{left:12px;top:12px;background:#fff;padding:10px 16px;border-radius:8px;z-index:99}
.container{max-width:var(--max);margin:0 auto;padding:0 22px}
.narrow{max-width:790px;margin-left:auto;margin-right:auto}
.center{text-align:center}
.eyebrow{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--terra);font-weight:600;margin:0 0 10px}
.lede{font-size:18.5px;color:var(--muted);line-height:1.65}
.muted{color:var(--muted);font-size:14px}
.section{padding:52px 0}
.section.tight{padding:34px 0}
.sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:24px;flex-wrap:wrap}
.sec-head h2{margin:0}
.sec-head a{font-size:14px;white-space:nowrap}

/* buttons */
.btn{display:inline-block;background:var(--terra);color:#fff;border:1.5px solid var(--terra);border-radius:999px;padding:14px 27px;font-size:15px;font-weight:600;border-bottom:1.5px solid var(--terra)}
.btn:hover{background:var(--terra-d);border-color:var(--terra-d);color:#fff}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--sand)}
.btn.ghost:hover{background:#fff;border-color:var(--terra);color:var(--terra-d)}
.btn.sm{padding:10px 20px;font-size:14px}
.btnrow{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}

/* header */
.site-header{position:sticky;top:0;z-index:60;background:rgba(251,248,243,.95);border-bottom:1px solid var(--line)}
@supports (backdrop-filter:blur(6px)){.site-header{backdrop-filter:blur(8px);background:rgba(251,248,243,.87)}}
.hdr{display:flex;align-items:center;gap:20px;min-height:72px;flex-wrap:wrap;padding:9px 0}
.brand{display:flex;align-items:center;gap:10px;font-family:var(--serif);font-size:23px;color:var(--ink);border:0}
.brand:hover{color:var(--terra-d);border:0}
.brand svg{width:32px;height:32px;flex:0 0 32px}
.nav{display:flex;gap:19px;margin-left:auto;align-items:center;flex-wrap:wrap}
.nav a{font-size:13px;letter-spacing:.07em;text-transform:uppercase;color:var(--ink);border:0;font-weight:500}
.nav a:hover,.nav a[aria-current="page"]{color:var(--terra)}
.nav a.pin{border:1.5px solid var(--terra);border-radius:999px;padding:8px 15px;color:var(--terra)}
.nav a.pin:hover{background:var(--terra);color:#fff}

/* hero */
.hero{display:grid;grid-template-columns:1.04fr 1fr;gap:46px;align-items:center;padding:58px 0 44px}
.hero .art{border-radius:20px;overflow:hidden;box-shadow:var(--shadow);border:1px solid var(--line)}
.hero .art svg{width:100%;display:block}
.hero .art img{width:100%;height:100%;object-fit:cover;display:block}
.trust{display:flex;gap:16px;flex-wrap:wrap;font-size:13.5px;color:var(--muted);margin-top:24px}
.trust span{display:flex;gap:7px;align-items:center}
.trust svg{width:15px;height:15px;flex:0 0 15px}

/* hero slider — top 5 posts */
.hero-slider-wrap{padding:28px 0 10px}
.hero-slider{position:relative;background:#fff;border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:var(--shadow)}
.hero-slider .slides{position:relative;min-height:440px}
.hero-slider .slide{display:none;grid-template-columns:1.15fr 1fr;gap:0;align-items:stretch;min-height:440px}
.hero-slider .slide.active{display:grid}
.hero-slider .slide-img{background:var(--oat);overflow:hidden;position:relative;min-height:440px}
.hero-slider .slide-img .cover{height:100%;min-height:440px}
.hero-slider .slide-img img{width:100%;height:100%;object-fit:cover}
.hero-slider .slide-body{padding:32px 32px 28px;display:flex;flex-direction:column;justify-content:center}
.hero-slider .slide-body h2{font-size:clamp(24px,3.2vw,32px);margin:10px 0 10px;line-height:1.15}
.hero-slider .slide-body h2 a{color:var(--ink);border:0}
.hero-slider .slide-body h2 a:hover{color:var(--terra-d)}
.hero-slider .arrow{position:absolute;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.92);border:1px solid var(--line);width:44px;height:44px;border-radius:50%;font-size:24px;line-height:1;cursor:pointer;z-index:5;box-shadow:0 4px 14px rgba(0,0,0,.08)}
.hero-slider .arrow:hover{background:#fff;border-color:var(--terra);color:var(--terra)}
.hero-slider .arrow.prev{left:14px}
.hero-slider .arrow.next{right:14px}
.hero-slider .dots{position:absolute;bottom:16px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:5;background:rgba(255,255,255,.85);padding:8px 12px;border-radius:999px;border:1px solid var(--line)}
.hero-slider .dot{width:10px;height:10px;border-radius:50%;border:1px solid var(--terra);background:#fff;cursor:pointer;padding:0}
.hero-slider .dot.active{background:var(--terra)}
.hero-static-below{display:grid;grid-template-columns:1.04fr 1fr;gap:46px;align-items:center;padding:42px 0 20px;margin-top:18px}
.hero-static-below .art{border-radius:20px;overflow:hidden;box-shadow:var(--shadow);border:1px solid var(--line)}
.hero-static-below .art img{width:100%;height:100%;object-fit:cover}
@media(max-width:900px){
  .hero-slider .slide{grid-template-columns:1fr}
  .hero-slider .slide-img{min-height:300px}
  .hero-slider .slide-img .cover{min-height:300px}
  .hero-static-below{grid-template-columns:1fr;gap:28px}
  .hero-static-below .art{order:-1}
}

/* chips */
.cats{display:flex;gap:10px;flex-wrap:wrap;padding:2px 0}
.cats a{font-size:13.5px;padding:9px 16px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink)}
.cats a:hover,.cats a.on{border-color:var(--terra);color:var(--terra-d);background:#FFF8F4}
.cats button{font:inherit;font-size:13.5px;padding:9px 16px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);cursor:pointer}
.cats button:hover,.cats button.on{border-color:var(--terra);color:var(--terra-d);background:#FFF8F4}

/* cards */
.grid{display:grid;gap:26px;grid-template-columns:repeat(auto-fill,minmax(295px,1fr))}
.grid.two{grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}
.card{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column;transition:transform .18s ease,box-shadow .18s ease}
.card:hover{transform:translateY(-3px);box-shadow:0 16px 38px rgba(70,50,30,.11)}
.card .cover{overflow:hidden;background:var(--oat)}
.card .cover svg{width:100%;height:100%;transition:transform .35s ease}
.card:hover .cover svg{transform:scale(1.035)}
.card .body{padding:18px 20px 22px;display:flex;flex-direction:column;flex:1}
.card .btnrow{margin-top:16px}
.card .btnrow .btn{padding:9px 18px;font-size:13.5px}
.catwide .btnrow{margin-top:22px}
.card h3{font-size:20.5px;margin:2px 0 8px}
.card h3 a{color:var(--ink);border:0}
.card h3 a:hover{color:var(--terra-d)}
.card p{margin:0;color:var(--muted);font-size:15px}
.chip{display:inline-block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--terra-d);background:#FBF0EA;border-radius:999px;padding:5px 11px;font-weight:600;margin-bottom:10px}
.meta{font-size:13px;color:var(--muted);margin-top:auto;padding-top:14px;display:flex;gap:9px;align-items:center;flex-wrap:wrap}
.meta i{width:4px;height:4px;border-radius:50%;background:var(--sand);display:inline-block}
.c4x3{aspect-ratio:4/3}
.c3x2{aspect-ratio:3/2}
.c16x9{aspect-ratio:16/9}
.c1x1{aspect-ratio:1/1}

/* feature */
.feature{display:grid;grid-template-columns:1.1fr 1fr;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:var(--shadow)}
.feature .cover{overflow:hidden}
.feature .cover svg{width:100%;height:100%}
.feature .body{padding:36px 34px;display:flex;flex-direction:column;justify-content:center}
.feature h2{font-size:clamp(23px,2.7vw,32px);margin:2px 0 12px}
.feature h2 a{color:var(--ink);border:0}
.feature h2 a:hover{color:var(--terra-d)}
.catwide h3{font-size:clamp(22px,2.6vw,30px);margin:2px 0 12px}
.catwide h3 a{color:var(--ink);border:0}
.catwide h3 a:hover{color:var(--terra-d)}
.feature p{color:var(--muted)}

/* panels */
.panel{background:#fff;border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);overflow:hidden}
.panel.split{display:grid;grid-template-columns:1fr 1fr}
.panel .pad{padding:38px 36px}
.panel .cover{overflow:hidden}
.panel .cover svg{width:100%;height:100%}
.cta{background:var(--ink);color:#F3EDE4;border-radius:20px;padding:44px;display:grid;grid-template-columns:1.15fr 1fr;gap:32px;align-items:center}
.cta h2{color:#fff;margin:0 0 10px;font-size:clamp(23px,3vw,32px)}
.cta p{color:#C9BFB2;margin:0;font-size:16px}
.field{display:flex;gap:10px;flex-wrap:wrap}
input[type=email],input[type=text],input[type=search],textarea{font-family:var(--sans);font-size:15px;padding:13px 16px;border-radius:10px;border:1px solid var(--line);background:#fff;color:var(--ink);min-width:210px;flex:1}
textarea{width:100%;min-height:150px;flex:none}
label{display:block;font-size:14px;font-weight:600;margin:0 0 6px}
.form-row{margin-bottom:16px}

/* article */
.post-head{padding:40px 0 6px}
.crumb{font-size:13px;color:var(--muted);margin-bottom:18px}
.crumb a{border:0}
.post-head h1{margin:14px 0 14px}
.post-hero{margin:28px 0 36px;border-radius:18px;overflow:hidden;position:relative;border:1px solid var(--line);aspect-ratio:3/2}
.post-hero svg{width:100%;height:100%;display:block}
.post-hero .tag{position:absolute;left:0;right:0;bottom:20px;display:flex;justify-content:center;padding:0 16px}
.post-hero .tag span{background:rgba(251,248,243,.94);border-radius:12px;padding:11px 20px;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--terra-d);box-shadow:0 8px 22px rgba(60,40,20,.14)}
.article{max-width:768px;margin:0 auto}
.article h2{font-size:clamp(22px,2.7vw,28px)}
.article > p:first-of-type{font-size:18.5px;color:#4A423B}
.callout{background:var(--oat);border-left:4px solid var(--terra);border-radius:0 12px 12px 0;padding:20px 24px;margin:30px 0}
.callout h4{margin:0 0 8px;font-family:var(--serif);font-size:19px}
.callout p:last-child,.callout ul:last-child{margin-bottom:0}
.shop{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px 26px;margin:34px 0;box-shadow:var(--shadow)}
.shop h3{margin:0 0 4px;font-size:21px}
.shop > p:first-of-type{margin-bottom:6px}
.shop ul{list-style:none;padding:0;margin:14px 0 0}
.shop li{display:flex;gap:14px;align-items:flex-start;justify-content:space-between;padding:13px 0;border-bottom:1px dashed var(--line);margin:0}
.shop li:last-child{border-bottom:0;padding-bottom:0}
.shop li b{display:block;font-weight:600}
.shop li b a{color:var(--ink);border-bottom:1px dotted rgba(181,83,60,.5)}
.shop li b a:hover{color:var(--terra-d);border-bottom-style:solid}
.shop li span.d{display:block;font-size:14.5px;color:var(--muted)}
.shop li span.p{color:var(--olive);font-weight:600;white-space:nowrap;font-size:14.5px}
.post-figure{margin:34px 0}
.post-figure img{width:100%;height:auto;border-radius:14px;border:1px solid var(--line)}
.post-figure figcaption{font-size:13.5px;color:var(--muted);margin-top:10px;text-align:center}
.article p img{border-radius:12px;margin:8px 0}
.pincta{background:linear-gradient(135deg,#F8F0E8,#EFE6D9);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:34px 0;display:flex;gap:16px;align-items:center}
.pincta svg{width:30px;height:30px;flex:0 0 30px}
.pincta p{margin:0;font-size:15.5px}
.pincta b{font-family:var(--serif);font-size:18px;display:block}
.ad-slot{border:1px dashed #D8CCBA;border-radius:12px;background:#F6F1E9;color:#9C9184;text-align:center;padding:28px 16px;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;margin:34px 0;min-height:112px;display:flex;align-items:center;justify-content:center;gap:8px}
.faq{margin:38px 0 8px}
.faq h2{margin-top:0}
.faq details{background:#fff;border:1px solid var(--line);border-radius:12px;padding:15px 20px;margin:12px 0}
.faq summary{font-family:var(--serif);font-size:19px;cursor:pointer}
.faq details p{margin:12px 0 2px;color:var(--muted)}
.author{display:flex;gap:16px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:38px 0}
.author .av{width:64px;height:64px;border-radius:50%;overflow:hidden;flex:0 0 64px;border:1px solid var(--line)}
.author .av svg{width:100%;height:100%}
.author p{margin:0;font-size:14.5px;color:var(--muted)}
.author b{display:block;font-family:var(--serif);font-size:18px;color:var(--ink)}
.share{margin:30px 0 0;padding-top:20px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
.steps{counter-reset:s;list-style:none;padding:0}
.steps li{counter-increment:s;position:relative;padding-left:56px;margin:0 0 26px}
.steps li::before{content:counter(s);position:absolute;left:0;top:-2px;width:38px;height:38px;border-radius:50%;background:var(--oat);color:var(--terra-d);font-family:var(--serif);font-size:19px;display:flex;align-items:center;justify-content:center}
.steps li b{font-family:var(--serif);font-size:20px;display:block;margin-bottom:4px}
.steps li p{margin:0;color:var(--muted)}
.prosebox{background:#fff;border:1px solid var(--line);border-radius:16px;padding:28px 30px;box-shadow:var(--shadow)}
.prosebox h2{margin-top:0}
.legalhdr{padding:44px 0 10px}
.legalhdr h1{margin-bottom:8px}
.pill-row{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 0}
.pill-row a{font-size:13px;padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink)}
.pill-row a:hover{border-color:var(--terra);color:var(--terra-d)}

/* footer */
.site-footer{background:var(--ink);color:#EDE6DC;margin-top:64px;padding:54px 0 26px}
.site-footer a{color:#EDE6DC;border:0}
.site-footer a:hover{color:#E9B8A6}
.fgrid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:32px}
.site-footer h4{color:#fff;font-size:17px;margin:0 0 14px}
.site-footer ul{list-style:none;padding:0;margin:0}
.site-footer li{margin:0 0 9px;font-size:14.5px;color:#C9BFB2}
.site-footer .brandline{display:flex;align-items:center;gap:10px;font-family:var(--serif);font-size:23px;color:#fff;margin-bottom:12px}
.site-footer .brandline svg{width:32px;height:32px}
.site-footer p{font-size:14.5px;color:#C9BFB2;max-width:44ch}
.social{display:flex;gap:10px;margin-top:16px}
.social a{width:38px;height:38px;border-radius:50%;border:1px solid rgba(255,255,255,.24);display:flex;align-items:center;justify-content:center}
.social a:hover{background:var(--terra);border-color:var(--terra)}
.social svg{width:17px;height:17px}
.fbot{border-top:1px solid rgba(255,255,255,.14);margin-top:36px;padding-top:18px;font-size:13px;color:#A79C8F;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}
.fbot a{color:#C9BFB2;text-decoration:underline}
.disc{font-size:13px;color:#A79C8F;margin-top:14px;max-width:none}

/* comments - Giscus + Cusdis tabbed */
.comments{margin:48px 0 0;padding-top:36px;border-top:1px solid var(--line)}
.comments-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:18px}
.comments-head h2{margin:0;font-size:clamp(22px,2.8vw,28px)}
.comments-note{font-size:13.5px;color:var(--muted);max-width:48ch}
.giscus{margin-top:18px}
.giscus-frame{border:0;width:100%}
.comments-disabled{background:#fff;border:1px dashed var(--line);border-radius:14px;padding:20px 22px;color:var(--muted);font-size:14.5px}
.comment-tabs{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 18px;border-bottom:1px solid var(--line);padding-bottom:12px}
.comment-tabs button{font:inherit;font-size:13.5px;padding:10px 18px;border-radius:999px;border:1.5px solid var(--line);background:#fff;color:var(--ink);cursor:pointer;font-weight:500}
.comment-tabs button.active,.comment-tabs button:hover{border-color:var(--terra);color:var(--terra-d);background:#FFF8F4}
.tab-pane{display:none}
.tab-pane.active{display:block}
.cusdis{margin-top:8px}
.comment-list{display:flex;flex-direction:column;gap:14px;margin:16px 0 24px}
.comment{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.comment-meta{font-size:13px;color:var(--muted);margin-bottom:6px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.comment-meta b{color:var(--ink);font-family:var(--serif);font-size:15px}
.comment p{margin:0;font-size:15px;line-height:1.6}
.comment-form{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 22px;box-shadow:0 6px 20px rgba(70,50,30,.05)}
.comment-form .form-row{margin-bottom:14px}
.comment-form label{display:block;font-size:13px;font-weight:600;margin:0 0 6px}
.comment-form input[type=text],.comment-form input[type=email],.comment-form textarea{width:100%;font-family:var(--sans);font-size:14.5px;padding:12px 14px;border-radius:10px;border:1px solid var(--line)}

/* consent */
.consent{position:fixed;z-index:80;left:14px;right:14px;bottom:14px;max-width:960px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:0 18px 44px rgba(60,40,20,.2);padding:16px 18px;display:none;gap:14px;align-items:center;flex-wrap:wrap}
.consent.show{display:flex}
.consent p{margin:0;font-size:14px;flex:1;min-width:240px}

@media (max-width:960px){
 .hero,.feature,.panel.split,.cta{grid-template-columns:1fr}
 .hero{gap:30px;padding:38px 0 30px}
 .feature .body,.panel .pad{padding:28px 24px}
 .cta{padding:32px 26px}
 .fgrid{grid-template-columns:1fr 1fr}
 .hdr{gap:12px}
 .nav{gap:14px}
 .section{padding:40px 0}
}
@media (max-width:620px){
 .fgrid{grid-template-columns:1fr}
 .nav{width:100%;gap:12px}
 .nav a{font-size:12px}
 .hero .art{order:-1}
 .post-hero{border-radius:14px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

# --------------------------------------------------------------------------- art
TONES = [
    {"a": "#F4E9DC", "b": "#E8D7C4", "floor": "#DCC9B3", "ink": "#3B322A", "ac": "#B5533C", "s2": "#6E7B5A", "s3": "#C08B48"},
    {"a": "#F1EBE1", "b": "#E3D9C9", "floor": "#D6C9B5", "ink": "#39332C", "ac": "#6E7B5A", "s2": "#B5533C", "s3": "#C08B48"},
    {"a": "#EEE8DE", "b": "#DDD5C7", "floor": "#D0C6B4", "ink": "#37322C", "ac": "#A9803F", "s2": "#6E7B5A", "s3": "#B5533C"},
    {"a": "#EAE7DD", "b": "#DAD9CA", "floor": "#CCCAB9", "ink": "#33322C", "ac": "#5F7150", "s2": "#8A9B74", "s3": "#B5533C"},
    {"a": "#F3E5D9", "b": "#E6D1BF", "floor": "#D9C0A9", "ink": "#3C3127", "ac": "#B5533C", "s2": "#A9803F", "s3": "#6E7B5A"},
    {"a": "#E9E5DF", "b": "#D7D4CC", "floor": "#C7C4BA", "ink": "#32302C", "ac": "#4F6B7A", "s2": "#C08B48", "s3": "#B5533C"},
]


def _vin(t, u):
    return (
        f'<defs><linearGradient id="g{u}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{t["a"]}"/><stop offset="1" stop-color="{t["b"]}"/></linearGradient>'
        f'<filter id="n{u}"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>'
        f'<feColorMatrix type="saturate" values="0"/></filter></defs>'
    )


def _grain(u, w, h):
    return f'<rect width="{w}" height="{h}" filter="url(#n{u})" opacity="0.07" style="mix-blend-mode:multiply"/>'


def _wrap(body, w=800, h=600, t=None, u=None):
    u = u or uid()
    t = t or TONES[0]
    return (
        f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" role="img" '
        f'aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'
        + _vin(t, u)
        + f'<rect width="{w}" height="{h}" fill="url(#g{u})"/>'
        + body
        + _grain(u, w, h)
        + "</svg>"
    )


def _vase(x, base, w, h, c, neck=0.34):
    """flat geometric vase; x = centre, base = bottom y"""
    nw = w * neck
    return (
        f'<rect x="{x-w/2:.0f}" y="{base-h:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{min(w/2,h/2.4):.0f}" fill="{c}"/>'
        f'<rect x="{x-nw/2:.0f}" y="{base-h-h*0.24:.0f}" width="{nw:.0f}" height="{h*0.3:.0f}" rx="{nw/2:.0f}" fill="{c}"/>'
    )


def _stem(x, y, h, c, bend=0, leaf=1):
    d = f"M{x} {y} C{x+bend} {y-h*0.45} {x-bend} {y-h*0.75} {x+bend*0.6} {y-h}"
    s = f'<path d="{d}" stroke="{c}" stroke-width="3" fill="none" stroke-linecap="round"/>'
    if leaf:
        s += f'<ellipse cx="{x+bend*0.5:.0f}" cy="{y-h*0.62:.0f}" rx="13" ry="7" fill="{c}" transform="rotate(-24 {x+bend*0.5:.0f} {y-h*0.62:.0f})"/>'
        s += f'<ellipse cx="{x-bend*0.4:.0f}" cy="{y-h*0.82:.0f}" rx="11" ry="6" fill="{c}" transform="rotate(22 {x-bend*0.4:.0f} {y-h*0.82:.0f})"/>'
    return s


def _pot(x, base, w, h, c, plantc=None, plant=True):
    c2 = plantc or c
    s = f'<path d="M{x-w/2:.0f} {base-h:.0f} h{w:.0f} l-{w*0.13:.0f} {h:.0f} h-{w*0.74:.0f} z" fill="{c}"/>'
    s += f'<rect x="{x-w*0.56:.0f}" y="{base-h-9:.0f}" width="{w*1.12:.0f}" height="10" rx="5" fill="{c}"/>'
    if plant:
        s += _stem(x - w * 0.2, base - h - 6, h * 1.5, c2, -14)
        s += _stem(x + w * 0.2, base - h - 6, h * 1.85, c2, 16)
        s += _stem(x, base - h - 6, h * 1.25, c2, 4)
    return s


def _rug(x, y, w, c, o=0.5):
    return f'<ellipse cx="{x}" cy="{y}" rx="{w/2:.0f}" ry="{w/9:.0f}" fill="{c}" opacity="{o}"/>'


def _frame(x, y, w, h, c, inner=None, o=0.9):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}" opacity="{o}"/>'
    if inner:
        s += f'<rect x="{x+w*0.14:.0f}" y="{y+h*0.14:.0f}" width="{w*0.72:.0f}" height="{h*0.72:.0f}" rx="2" fill="{inner}"/>'
    return s


def _books(x, y, w, c1, c2, c3):
    return (
        f'<rect x="{x}" y="{y-11}" width="{w}" height="11" rx="2" fill="{c1}"/>'
        f'<rect x="{x+3}" y="{y-22}" width="{w-6}" height="11" rx="2" fill="{c2}"/>'
        f'<rect x="{x+1}" y="{y-32}" width="{w-2}" height="10" rx="2" fill="{c3}"/>'
    )


# --- motifs -------------------------------------------------------------------
def m_arch(t, u):
    b = (
        f'<rect x="0" y="430" width="800" height="170" fill="{t["floor"]}"/>'
        f'<rect x="0" y="427" width="800" height="4" fill="{t["ink"]}" opacity="0.12"/>'
        f'<path d="M250 470 V250 a150 150 0 0 1 300 0 V470 z" fill="{t["a"]}" opacity="0.95"/>'
        f'<path d="M250 470 V250 a150 150 0 0 1 300 0 V470" fill="none" stroke="{t["ink"]}" stroke-opacity="0.18" stroke-width="3"/>'
        f'<circle cx="400" cy="255" r="52" fill="{t["s3"]}" opacity="0.55"/>'
        f'<rect x="262" y="176" width="276" height="0" fill="none"/>'
        f'<rect x="196" y="240" width="14" height="230" rx="7" fill="{t["s2"]}" opacity="0.5"/>'
        f'<rect x="592" y="240" width="14" height="230" rx="7" fill="{t["s2"]}" opacity="0.5"/>'
        f'<rect x="120" y="392" width="230" height="12" rx="6" fill="{t["ink"]}" opacity="0.7"/>'
        f'<rect x="136" y="404" width="10" height="66" rx="5" fill="{t["ink"]}" opacity="0.55"/>'
        f'<rect x="324" y="404" width="10" height="66" rx="5" fill="{t["ink"]}" opacity="0.55"/>'
        + _vase(196, 392, 58, 92, t["ac"], 0.4)
        + _vase(286, 392, 40, 62, t["s3"], 0.45)
        + _stem(196, 300, 96, t["s2"], -16)
        + _stem(206, 300, 70, t["s2"], 18)
        + _rug(560, 500, 340, t["ac"], 0.22)
        + _pot(600, 500, 92, 78, t["s2"])
    )
    return _wrap(b, t=t, u=u)


def m_sofa(t, u):
    b = (
        f'<rect x="0" y="430" width="800" height="170" fill="{t["floor"]}"/>'
        + _frame(96, 120, 150, 120, t["s2"], t["a"])
        + _frame(268, 156, 108, 84, t["s3"], t["a"])
        + f'<rect x="286" y="300" width="300" height="26" rx="10" fill="{t["ink"]}" opacity="0.85"/>'
        f'<rect x="272" y="322" width="328" height="86" rx="20" fill="{t["ac"]}"/>'
        f'<rect x="292" y="336" width="140" height="60" rx="14" fill="{t["a"]}" opacity="0.5"/>'
        f'<rect x="442" y="336" width="140" height="60" rx="14" fill="{t["a"]}" opacity="0.5"/>'
        f'<rect x="262" y="404" width="348" height="24" rx="12" fill="{t["ac"]}"/>'
        f'<rect x="284" y="428" width="12" height="26" rx="5" fill="{t["ink"]}" opacity="0.6"/>'
        f'<rect x="576" y="428" width="12" height="26" rx="5" fill="{t["ink"]}" opacity="0.6"/>'
        f'<rect x="646" y="230" width="8" height="200" rx="4" fill="{t["ink"]}" opacity="0.7"/>'
        f'<path d="M616 230 h68 l-14 -54 h-40 z" fill="{t["s3"]}"/>'
        f'<rect x="622" y="428" width="56" height="10" rx="5" fill="{t["ink"]}" opacity="0.7"/>'
        + _rug(400, 500, 380, t["s2"], 0.2)
        + _vase(636, 424, 34, 54, t["s2"], 0.42)
        + _stem(636, 372, 56, t["s2"], 10)
    )
    return _wrap(b, t=t, u=u)


def m_shelf(t, u):
    rows = ""
    y = 250
    for i in range(3):
        rows += f'<rect x="180" y="{y}" width="440" height="12" rx="4" fill="{t["ink"]}" opacity="0.72"/>'
        y += 96
    b = (
        f'<circle cx="400" cy="140" r="58" fill="{t["a"]}" stroke="{t["s3"]}" stroke-width="6"/>'
        f'<circle cx="400" cy="140" r="44" fill="{t["s2"]}" opacity="0.35"/>'
        f'<rect x="0" y="440" width="800" height="160" fill="{t["floor"]}"/>'
        + rows
        + _books(220, 250, 74, t["ac"], t["s2"], t["s3"])
        + _vase(340, 250, 44, 62, t["s2"], 0.42)
        + _vase(392, 250, 34, 44, t["s3"], 0.46)
        + _pot(540, 250, 72, 54, t["ac"], t["s2"], plant=False)
        + _stem(540, 196, 74, t["s2"], -18)
        + _stem(548, 196, 58, t["s2"], 14)
        + _books(250, 346, 80, t["s3"], t["ac"], t["s2"])
        + _vase(420, 346, 50, 78, t["ac"], 0.4)
        + _vase(520, 346, 34, 46, t["s2"], 0.5)
        + _frame(230, 372, 96, 70, t["ink"], t["a"], 0.16)
        + _pot(360, 442, 78, 60, t["ac"], t["s2"], plant=False)
        + _stem(360, 382, 66, t["s2"], -16)
        + _stem(370, 382, 52, t["s3"], 12)
        + _books(560, 442, 70, t["s2"], t["ac"], t["s3"])
        + _rug(400, 528, 320, t["ac"], 0.16)
    )
    return _wrap(b, t=t, u=u)


def m_swatches(t, u):
    cols = [t["a"], t["s3"], t["ac"], t["s2"], t["ink"]]
    b = f'<rect x="0" y="470" width="800" height="130" fill="{t["floor"]}"/>'
    for i, c in enumerate(cols):
        x = 128 + i * 116
        rot = -9 + i * 4.5
        b += (
            f'<g transform="rotate({rot} 400 300)">'
            f'<rect x="{x}" y="150" width="104" height="270" rx="10" fill="#fff" opacity="0.9"/>'
            f'<rect x="{x+9}" y="159" width="86" height="196" rx="6" fill="{c}"/>'
            f'<rect x="{x+16}" y="372" width="72" height="7" rx="3.5" fill="{t["ink"]}" opacity="0.35"/>'
            f'<rect x="{x+16}" y="388" width="46" height="7" rx="3.5" fill="{t["ink"]}" opacity="0.2"/>'
            f"</g>"
        )
    b += (
        f'<path d="M96 512 q80 -30 150 -6 q90 30 178 2 q96 -30 190 -4" stroke="{t["ac"]}" '
        f'stroke-width="9" fill="none" stroke-linecap="round" opacity="0.55"/>'
        f'<circle cx="640" cy="120" r="34" fill="{t["s3"]}" opacity="0.5"/>'
    )
    return _wrap(b, t=t, u=u)


def m_finds(t, u):
    b = (
        f'<rect x="0" y="440" width="800" height="160" fill="{t["floor"]}"/>'
        f'<rect x="86" y="290" width="180" height="150" rx="10" fill="{t["a"]}"/>'
        f'<rect x="86" y="290" width="180" height="34" rx="10" fill="{t["s2"]}"/>'
        f'<rect x="150" y="272" width="52" height="20" rx="4" fill="{t["ink"]}" opacity="0.25"/>'
        f'<rect x="118" y="352" width="116" height="10" rx="5" fill="{t["ink"]}" opacity="0.16"/>'
        f'<rect x="118" y="376" width="80" height="10" rx="5" fill="{t["ink"]}" opacity="0.12"/>'
        f'<rect x="300" y="330" width="150" height="110" rx="10" fill="{t["s3"]}" opacity="0.85"/>'
        f'<rect x="300" y="330" width="150" height="26" rx="10" fill="{t["ac"]}" opacity="0.8"/>'
        f'<path d="M560 250 h150 v190 h-150 z" fill="{t["s2"]}" opacity="0.9"/>'
        f'<path d="M560 250 l75 -46 l75 46 z" fill="{t["s2"]}"/>'
        f'<rect x="600" y="292" width="70" height="9" rx="4.5" fill="{t["a"]}" opacity="0.7"/>'
        f'<rect x="600" y="316" width="48" height="9" rx="4.5" fill="{t["a"]}" opacity="0.5"/>'
        f'<g transform="rotate(-14 210 150)"><rect x="140" y="112" width="150" height="80" rx="12" fill="#fff"/>'
        f'<circle cx="170" cy="152" r="9" fill="none" stroke="{t["ac"]}" stroke-width="5"/>'
        f'<rect x="192" y="138" width="76" height="9" rx="4.5" fill="{t["ink"]}" opacity="0.28"/>'
        f'<rect x="192" y="158" width="52" height="9" rx="4.5" fill="{t["ink"]}" opacity="0.18"/></g>'
        + _vase(486, 470, 66, 110, t["ac"], 0.38)
        + _stem(486, 362, 92, t["s2"], -14)
        + _stem(494, 362, 68, t["s2"], 16)
        + _rug(400, 520, 300, t["s2"], 0.14)
    )
    return _wrap(b, t=t, u=u)


def m_hack(t, u):
    b = (
        f'<rect x="0" y="440" width="800" height="160" fill="{t["floor"]}"/>'
        f'<rect x="90" y="300" width="200" height="140" rx="8" fill="{t["s3"]}" opacity="0.9"/>'
        f'<rect x="90" y="300" width="200" height="14" rx="6" fill="{t["ink"]}" opacity="0.2"/>'
        f'<path d="M112 322 h156" stroke="{t["a"]}" stroke-width="6" stroke-dasharray="14 10"/>'
        f'<rect x="330" y="270" width="200" height="170" rx="8" fill="{t["ac"]}"/>'
        f'<rect x="344" y="384" width="172" height="46" rx="6" fill="{t["a"]}" opacity="0.4"/>'
        f'<rect x="352" y="288" width="76" height="84" rx="5" fill="#fff" opacity="0.85"/>'
        f'<rect x="440" y="288" width="76" height="84" rx="5" fill="#fff" opacity="0.7"/>'
        f'<rect x="320" y="250" width="220" height="26" rx="8" fill="{t["s2"]}"/>'
        f'<rect x="600" y="360" width="130" height="80" rx="10" fill="{t["s2"]}"/>'
        f'<ellipse cx="665" cy="360" rx="65" ry="14" fill="{t["s2"]}"/>'
        f'<rect x="616" y="440" width="9" height="42" rx="4" fill="{t["ink"]}" opacity="0.5"/>'
        f'<rect x="662" y="440" width="9" height="42" rx="4" fill="{t["ink"]}" opacity="0.5"/>'
        f'<rect x="706" y="440" width="9" height="42" rx="4" fill="{t["ink"]}" opacity="0.5"/>'
        f'<rect x="130" y="150" width="14" height="96" rx="6" fill="{t["ink"]}" opacity="0.35" transform="rotate(18 137 198)"/>'
        f'<circle cx="204" cy="182" r="16" fill="none" stroke="{t["ink"]}" stroke-width="9" opacity="0.35"/>'
        + _rug(430, 528, 300, t["ac"], 0.14)
    )
    return _wrap(b, t=t, u=u)


def m_nook(t, u):
    b = (
        f'<rect x="0" y="440" width="800" height="160" fill="{t["floor"]}"/>'
        f'<path d="M300 470 V180 a90 90 0 0 1 180 0 V470 z" fill="{t["a"]}" opacity="0.8"/>'
        f'<rect x="360" y="130" width="120" height="12" rx="6" fill="{t["ink"]}" opacity="0.5"/>'
        f'<rect x="150" y="250" width="196" height="60" rx="26" fill="{t["ac"]}"/>'
        f'<rect x="140" y="300" width="216" height="96" rx="24" fill="{t["ac"]}"/>'
        f'<rect x="164" y="318" width="168" height="62" rx="18" fill="{t["a"]}" opacity="0.45"/>'
        f'<rect x="130" y="386" width="236" height="26" rx="13" fill="{t["ac"]}"/>'
        f'<rect x="154" y="412" width="12" height="30" rx="5" fill="{t["ink"]}" opacity="0.55"/>'
        f'<rect x="330" y="412" width="12" height="30" rx="5" fill="{t["ink"]}" opacity="0.55"/>'
        f'<rect x="556" y="196" width="9" height="246" rx="4" fill="{t["ink"]}" opacity="0.7"/>'
        f'<path d="M522 196 h76 l-16 -58 h-44 z" fill="{t["s3"]}"/>'
        f'<rect x="548" y="442" width="26" height="9" rx="4" fill="{t["ink"]}" opacity="0.6"/>'
        f'<circle cx="470" cy="392" r="34" fill="{t["s2"]}" opacity="0.85"/>'
        f'<rect x="466" y="392" width="9" height="46" rx="4" fill="{t["s2"]}"/>'
        + _books(626, 442, 74, t["s3"], t["s2"], t["ac"])
        + _rug(400, 520, 360, t["s2"], 0.18)
    )
    return _wrap(b, t=t, u=u)


def m_fall(t, u):
    def pumpkin(x, y, w, h, c, u_=None):
        s = (
            f'<ellipse cx="{x}" cy="{y}" rx="{w/2:.0f}" ry="{h/2:.0f}" fill="{c}"/>'
            f'<ellipse cx="{x-w*0.16:.0f}" cy="{y}" rx="{w*0.3:.0f}" ry="{h/2:.0f}" fill="#fff" opacity="0.1"/>'
            f'<rect x="{x-7}" y="{y-h/2-16:.0f}" width="14" height="20" rx="6" fill="{t["s2"]}"/>'
        )
        return s
    b = (
        f'<rect x="0" y="450" width="800" height="150" fill="{t["floor"]}"/>'
        f'<path d="M240 450 V210 a160 160 0 0 1 320 0 V450 z" fill="{t["a"]}" opacity="0.6"/>'
        f'<circle cx="560" cy="130" r="46" fill="{t["s3"]}" opacity="0.4"/>'
        + pumpkin(200, 410, 190, 150, t["s3"])
        + pumpkin(340, 432, 150, 116, t["ac"])
        + pumpkin(452, 424, 118, 92, t["s2"])
        + _vase(620, 448, 64, 104, t["s2"], 0.4)
        + f'<path d="M620 344 C606 300 596 280 580 262" stroke="{t["s3"]}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        f'<path d="M620 344 C632 296 644 276 660 258" stroke="{t["s3"]}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        f'<path d="M620 344 C620 300 620 278 620 254" stroke="{t["s3"]}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        f'<ellipse cx="580" cy="258" rx="9" ry="18" fill="{t["s3"]}"/><ellipse cx="660" cy="254" rx="9" ry="18" fill="{t["s3"]}"/>'
        f'<ellipse cx="620" cy="248" rx="9" ry="20" fill="{t["s3"]}"/>'
        f'<rect x="700" y="386" width="46" height="64" rx="8" fill="{t["a"]}"/>'
        f'<ellipse cx="723" cy="384" rx="23" ry="8" fill="{t["a"]}"/>'
        f'<path d="M723 380 c-9 -16 -2 -30 0 -34 c3 6 9 18 0 34 z" fill="{t["ac"]}"/>'
        + _rug(400, 530, 340, t["ac"], 0.16)
    )
    return _wrap(b, t=t, u=u)


def m_flat(t, u):
    b = (
        f'<rect x="0" y="430" width="800" height="170" fill="{t["floor"]}"/>'
        f'<circle cx="640" cy="150" r="66" fill="{t["s3"]}" opacity="0.42"/>'
        f'<rect x="80" y="200" width="300" height="12" rx="6" fill="{t["ac"]}" opacity="0.75"/>'
        f'<rect x="80" y="234" width="200" height="12" rx="6" fill="{t["ink"]}" opacity="0.22"/>'
        f'<rect x="80" y="288" width="360" height="10" rx="5" fill="{t["ink"]}" opacity="0.12"/>'
        f'<rect x="80" y="312" width="300" height="10" rx="5" fill="{t["ink"]}" opacity="0.1"/>'
        + _vase(560, 440, 78, 128, t["s2"], 0.38)
        + _stem(560, 312, 104, t["s2"], -16)
        + _stem(570, 312, 78, t["s3"], 14)
        + _rug(400, 522, 300, t["s2"], 0.16)
    )
    return _wrap(b, t=t, u=u)


def m_hero(t, u):
    """wide home page hero (1200x675)"""
    b = (
        f'<rect x="0" y="470" width="1200" height="205" fill="{t["floor"]}"/>'
        f'<rect x="0" y="467" width="1200" height="4" fill="{t["ink"]}" opacity="0.1"/>'
        f'<path d="M180 500 V235 a140 140 0 0 1 280 0 V500 z" fill="{t["a"]}" opacity="0.95"/>'
        f'<path d="M180 500 V235 a140 140 0 0 1 280 0 V500" fill="none" stroke="{t["ink"]}" stroke-opacity="0.16" stroke-width="3"/>'
        f'<circle cx="320" cy="238" r="48" fill="{t["s3"]}" opacity="0.5"/>'
        f'<rect x="136" y="228" width="13" height="272" rx="6" fill="{t["s2"]}" opacity="0.45"/>'
        f'<rect x="492" y="228" width="13" height="272" rx="6" fill="{t["s2"]}" opacity="0.45"/>'
        f'<rect x="562" y="120" width="132" height="104" rx="5" fill="{t["s2"]}" opacity="0.85"/>'
        f'<rect x="586" y="142" width="84" height="60" rx="3" fill="{t["a"]}"/>'
        f'<rect x="716" y="158" width="96" height="66" rx="5" fill="{t["s3"]}" opacity="0.8"/>'
        f'<rect x="736" y="176" width="56" height="30" rx="3" fill="{t["a"]}"/>'
        f'<rect x="600" y="330" width="330" height="30" rx="12" fill="{t["ink"]}" opacity="0.85"/>'
        f'<rect x="586" y="356" width="358" height="98" rx="22" fill="{t["ac"]}"/>'
        f'<rect x="608" y="374" width="150" height="66" rx="16" fill="{t["a"]}" opacity="0.5"/>'
        f'<rect x="772" y="374" width="150" height="66" rx="16" fill="{t["a"]}" opacity="0.5"/>'
        f'<rect x="574" y="450" width="382" height="26" rx="13" fill="{t["ac"]}"/>'
        f'<rect x="600" y="476" width="13" height="30" rx="6" fill="{t["ink"]}" opacity="0.55"/>'
        f'<rect x="916" y="476" width="13" height="30" rx="6" fill="{t["ink"]}" opacity="0.55"/>'
        f'<rect x="1006" y="214" width="9" height="292" rx="4" fill="{t["ink"]}" opacity="0.7"/>'
        f'<path d="M970 214 h82 l-17 -62 h-48 z" fill="{t["s3"]}"/>'
        f'<rect x="998" y="500" width="26" height="10" rx="5" fill="{t["ink"]}" opacity="0.6"/>'
        + _pot(1046, 500, 104, 86, t["s2"])
        + _vase(1050, 500, 40, 62, t["s3"], 0.45)
        + _pot(96, 500, 100, 82, t["ac"], t["s2"])
        + _rug(600, 560, 520, t["ac"], 0.18)
    )
    return _wrap(b, 1200, 675, t=t, u=u)


def m_portrait(t, u):
    b = (
        f'<rect x="0" y="440" width="800" height="160" fill="{t["floor"]}"/>'
        f'<path d="M210 470 V200 a190 190 0 0 1 380 0 V470 z" fill="{t["a"]}"/>'
        f'<path d="M210 470 V200 a190 190 0 0 1 380 0 V470" fill="none" stroke="{t["ink"]}" stroke-opacity="0.16" stroke-width="3"/>'
        f'<circle cx="400" cy="330" r="96" fill="{t["s2"]}" opacity="0.35"/>'
        f'<circle cx="400" cy="300" r="62" fill="{t["s3"]}" opacity="0.5"/>'
        f'<path d="M300 470 q100 -96 200 0 z" fill="{t["ac"]}" opacity="0.75"/>'
        f'<rect x="120" y="392" width="120" height="12" rx="6" fill="{t["ink"]}" opacity="0.6"/>'
        + _books(140, 392, 74, t["ac"], t["s3"], t["s2"])
        + _vase(660, 452, 60, 96, t["s2"], 0.4)
        + _stem(660, 356, 74, t["s2"], 14)
        + _rug(400, 524, 320, t["ac"], 0.14)
    )
    return _wrap(b, t=t, u=u)


def m_basket(t, u):
    weave = "".join(
        f'<path d="M{x} 350 v96" stroke="{t["ink"]}" stroke-opacity="0.14" stroke-width="4"/>' for x in range(300, 461, 20)
    )
    b = (
        f'<rect x="0" y="450" width="800" height="150" fill="{t["floor"]}"/>'
        f'<path d="M280 350 h200 l-24 116 h-152 z" fill="{t["s3"]}"/>'
        f'<rect x="272" y="338" width="216" height="18" rx="9" fill="{t["ac"]}"/>'
        + weave
        + f'<path d="M330 340 q50 -60 100 0" stroke="{t["ac"]}" stroke-width="7" fill="none"/>'
        + _stem(380, 340, 120, t["s2"], -20)
        + _stem(396, 340, 96, t["s2"], 22)
        + _stem(388, 340, 148, t["s3"], 6)
        + _books(120, 452, 80, t["ac"], t["s3"], t["s2"])
        + _vase(600, 452, 66, 108, t["ac"], 0.4)
        + _vase(672, 452, 46, 70, t["s2"], 0.46)
        + _rug(400, 526, 340, t["s2"], 0.16)
    )
    return _wrap(b, t=t, u=u)


def m_plain(t, u):
    b = (
        f'<rect x="0" y="430" width="800" height="170" fill="{t["floor"]}"/>'
        f'<circle cx="400" cy="170" r="86" fill="{t["s3"]}" opacity="0.34"/>'
        f'<circle cx="400" cy="170" r="126" fill="none" stroke="{t["ac"]}" stroke-opacity="0.3" stroke-width="3"/>'
        f'<rect x="120" y="300" width="560" height="10" rx="5" fill="{t["ink"]}" opacity="0.1"/>'
        f'<rect x="200" y="330" width="400" height="10" rx="5" fill="{t["ink"]}" opacity="0.08"/>'
        + _vase(240, 452, 56, 90, t["ac"], 0.4)
        + _stem(240, 362, 74, t["s2"], -14)
        + _pot(560, 452, 88, 72, t["s2"])
        + _rug(400, 522, 300, t["ac"], 0.14)
    )
    return _wrap(b, t=t, u=u)


MOTIFS = {
    "arch": m_arch, "sofa": m_sofa, "shelf": m_shelf, "swatches": m_swatches,
    "finds": m_finds, "hack": m_hack, "nook": m_nook, "fall": m_fall,
    "flat": m_flat, "hero": m_hero, "portrait": m_portrait, "basket": m_basket,
    "plain": m_plain,
}


def art(motif, tone=0, cls="c4x3"):
    """Return an inline <svg> wrapped in a .cover div."""
    fn = MOTIFS.get(motif, m_flat)
    svg = fn(TONES[tone % len(TONES)], uid())
    return f'<div class="cover {cls}">{svg}</div>'


def art_raw(motif, tone=0):
    fn = MOTIFS.get(motif, m_flat)
    return fn(TONES[tone % len(TONES)], uid())


# --- small icons --------------------------------------------------------------
ICON = {
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="#6E7B5A" stroke-width="2.4" stroke-linecap="round"><path d="M20 6 9 17l-5-5"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="#C08B48"><path d="M12 2.5l2.9 6.1 6.6.9-4.8 4.6 1.2 6.6L12 17.6 6.1 20.7l1.2-6.6L2.5 9.5l6.6-.9z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="#B5533C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6l1 7-4 3-4-3z"/><path d="M12 13v8"/></svg>',
    "logo": (
        '<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">'
        '<rect width="40" height="40" rx="11" fill="#B5533C"/>'
        '<path d="M11 29V20a9 9 0 0 1 18 0v9z" fill="#F7F1E8"/>'
        '<circle cx="20" cy="18" r="3.6" fill="#C08B48"/>'
        '<rect x="9" y="30" width="22" height="3" rx="1.5" fill="#6E7B5A"/></svg>'
    ),
    "pinterest": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.2-5.1s-.3-.6-.3-1.5c0-1.4.8-2.4 1.8-2.4.9 0 1.3.6 1.3 1.4 0 .9-.6 2.2-.9 3.4-.2 1 .5 1.9 1.6 1.9 1.9 0 3.2-2.4 3.2-5.3 0-2.2-1.5-3.8-4.2-3.8-3 0-4.9 2.2-4.9 4.7 0 .9.3 1.6.7 2.1.2.2.2.3.1.6l-.2.9c-.1.3-.3.4-.6.2-1.4-.6-2.1-2.2-2.1-4C5.1 8 7.2 5 12.2 5c4.1 0 6.8 2.9 6.8 6 0 4.1-2.3 7.2-5.7 7.2-1.1 0-2.2-.6-2.6-1.3l-.7 2.7c-.3 1-.9 2.1-1.4 2.8A10 10 0 1 0 12 2z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1.2" fill="currentColor" stroke="none"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.3-1.5 1.6-1.5h1.3V5c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4.1V11H7.6v3H10v7z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.6 8.1s-.2-1.4-.8-2c-.7-.8-1.5-.8-1.9-.9C16.9 5 12 5 12 5h0s-4.9 0-6.9.2c-.4.1-1.2.1-1.9.9-.6.6-.8 2-.8 2S2.2 9.7 2.2 11.4v1.6c0 1.6.2 3.3.2 3.3s.2 1.4.8 2c.7.8 1.7.7 2.1.8 1.6.1 6.7.2 6.7.2s4.9 0 6.9-.2c.4-.1 1.2-.1 1.9-.9.6-.6.8-2 .8-2s.2-1.6.2-3.3v-1.6c0-1.6-.2-3.2-.2-3.2zM10.1 14.6V8.9l5.2 2.9z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="#B5533C" stroke-width="1.9"><rect x="2.5" y="4.5" width="19" height="15" rx="3"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>',
}

NAV = [
    ("", "Home"),
    ("start-here", "Start Here"),
    ("blog", "Decor Ideas"),
    ("shop-my-home", "Shop My Home"),
    ("about", "About"),
    ("contact", "Contact"),
]

FOOTER_LEGAL = [
    ("privacy-policy", "Privacy Policy"),
    ("cookie-policy", "Cookie Policy"),
    ("terms-of-use", "Terms of Use"),
    ("disclaimer", "Disclaimer"),
    ("affiliate-disclosure", "Affiliate Disclosure"),
    ("contact", "Contact"),
]

FOOTER_CATS = [
    ("blog#living-room", "Living Room Ideas"),
    ("blog#small-space", "Small Space & Renters"),
    ("blog#get-the-look", "Get the Look for Less"),
    ("blog#finds", "Home Finds & Deals"),
    ("blog#diy", "IKEA Hacks & DIY"),
    ("blog#color", "Color & Paint"),
]


def header(rel="", current=""):
    # Use editable navigation from content/navigation.yml if present, else fallback to hardcoded NAV
    def clean_home_href(href, rel):
        # Remove index.html and .html extension for clean URLs
        h = href.strip()
        if h in ("", "index.html", "/index.html", "/", "./", "/"):
            return rel if rel else "./"
        if h.startswith("/"):
            h = h.lstrip("/")
        h = h.replace("/index.html", "/").replace("index.html", "")
        # strip .html extension for clean URLs, but keep fragments #...
        if "#" in h:
            base, frag = h.split("#",1)
            if base.endswith(".html"):
                base = base[:-5]
            h = f"{base}#{frag}"
        else:
            if h.endswith(".html"):
                h = h[:-5]
        if h in ("", "/"):
            return rel if rel else "./"
        return f"{rel}{h}" if not h.startswith(("http://","https://")) else h

    nav_cfg = NAV if isinstance(NAV, dict) and NAV.get("nav_links") else {}
    links_cfg = nav_cfg.get("nav_links") if nav_cfg else None
    if links_cfg:
        links = ""
        for item in links_cfg:
            if not isinstance(item, dict):
                continue
            label = (item.get("label") or "").strip()
            url = (item.get("url") or "").strip()
            style = (item.get("style") or "default").lower()
            if not label or not url:
                continue
            href = url
            if href.startswith("post:"):
                slug = href[5:].strip()
                href = f"blog#{slug}"
            full_href = clean_home_href(href, rel)
            cls = ""
            if style == "outline":
                cls = ' class="pin"'
            elif style == "primary":
                cls = ' class="btn sm" style="text-transform:none;letter-spacing:0;padding:8px 16px"'
            # current page detection — normalize current vs href (strip .html)
            def norm_cur(s):
                s = s.lstrip("/").replace("index.html","")
                if s.endswith(".html"):
                    s = s[:-5]
                return s.rstrip("/")
            cur_href = norm_cur(href)
            cur_current = norm_cur(current)
            cur = ' aria-current="page"' if cur_href == cur_current or (cur_href=="" and cur_current=="") else ""
            links += f'<a href="{full_href}"{cls}{cur}>{label}</a>'
        show_pin = nav_cfg.get("show_pinterest", True)
        pin_url = (nav_cfg.get("pinterest_url") or "https://www.pinterest.com/").strip()
        pin_label = (nav_cfg.get("pinterest_label") or "Pinterest").strip()
        if show_pin and pin_url:
            links += f'<a class="pin" href="{pin_url}" target="_blank" rel="noopener">{pin_label}</a>'
        logo_text = (nav_cfg.get("logo_text") or "").strip() or BRAND
        logo_img = (nav_cfg.get("logo_image") or "").strip()
        if logo_img:
            clean_logo = logo_img.lstrip("/")
            logo_html = f'<img src="{rel}{clean_logo}" alt="{logo_text}" style="height:32px;width:auto">'
        else:
            logo_html = f"{ICON['logo']}<span>{logo_text}</span>"
        brand_href = rel if rel else "./"
        return f"""<header class="site-header">
 <div class="container hdr">
  <a class="brand" href="{brand_href}">{logo_html}</a>
  <nav class="nav" aria-label="Main">{links}</nav>
 </div>
</header>"""
    # fallback to old hardcoded NAV
    links = ""
    for href, label in NAV:
        full_href = clean_home_href(href, rel)
        cls = ' class="pin"' if href in ("shop-my-home", "shop-my-home.html") else ""
        def norm2(s):
            s = s.replace("index.html","")
            if s.endswith(".html"):
                s = s[:-5]
            return s.rstrip("/")
        cur_href = norm2(href)
        cur_current = norm2(current)
        cur = ' aria-current="page"' if cur_href == cur_current else ""
        links += f'<a href="{full_href}"{cls}{cur}>{label}</a>'
    brand_href = rel if rel else "./"
    return f"""<header class="site-header">
 <div class="container hdr">
  <a class="brand" href="{brand_href}">{ICON['logo']}<span>{BRAND}</span></a>
  <nav class="nav" aria-label="Main">{links}<a class="pin" href="https://www.pinterest.com/" target="_blank" rel="noopener">Pinterest</a></nav>
 </div>
</header>"""


def footer(rel=""):
    f_cfg = FOOTER if isinstance(FOOTER, dict) and FOOTER else {}
    desc = f_cfg.get("description") or "Designer-looking rooms without the designer budget. Home decor ideas, budget swaps, paint palettes and room makeovers you can actually pull off this weekend."
    copyright = f_cfg.get("copyright") or f"© 2026 {BRAND}. All rights reserved."
    disc_text = f_cfg.get("disclosure_text") or f"As an Amazon Associate we earn from qualifying purchases. {BRAND} also participates in other affiliate programs and displays advertising; see our <a href=\"{rel}affiliate-disclosure\">Affiliate Disclosure</a> for details. Nothing on this site is professional design, legal, or financial advice."
    explore_cfg = f_cfg.get("explore_links")
    if explore_cfg and isinstance(explore_cfg, list) and isinstance(explore_cfg[0], dict):
        explore_html = ""
        for item in explore_cfg:
            label = (item.get("label") or "").strip()
            url = (item.get("url") or "").strip().lstrip("/")
            if not label or not url:
                continue
            explore_html += f'<li><a href="{rel}{url}">{label}</a></li>'
    else:
        explore_html = f'<li><a href="{rel}start-here">Start Here</a></li><li><a href="{rel}blog">All Decor Ideas</a></li><li><a href="{rel}shop-my-home">Shop My Home</a></li><li><a href="{rel}about">About</a></li><li><a href="{rel}contact">Work With Us</a></li>'

    room_cfg = f_cfg.get("room_guides")
    if room_cfg and isinstance(room_cfg, list) and isinstance(room_cfg[0], dict):
        cats = "".join(f'<li><a href="{rel}{ (item.get("url") or "").lstrip("/") }">{item.get("label")}</a></li>' for item in room_cfg if item.get("label") and item.get("url"))
    else:
        cats = "".join(f'<li><a href="{rel}{h}">{l}</a></li>' for h, l in FOOTER_CATS)

    legal_cfg = f_cfg.get("legal_links")
    if legal_cfg and isinstance(legal_cfg, list) and isinstance(legal_cfg[0], dict):
        legal = "".join(f'<li><a href="{rel}{ (item.get("url") or "").lstrip("/") }">{item.get("label")}</a></li>' for item in legal_cfg if item.get("label") and item.get("url"))
    else:
        legal = "".join(f'<li><a href="{rel}{h}">{l}</a></li>' for h, l in FOOTER_LEGAL)

    social_cfg = f_cfg.get("social") if isinstance(f_cfg.get("social"), dict) else SOCIAL
    soc = ""
    for k, n in [("pinterest", "Pinterest"), ("instagram", "Instagram"), ("facebook", "Facebook"), ("youtube", "YouTube")]:
        url = social_cfg.get(k) if isinstance(social_cfg, dict) else None
        if url:
            url = str(url).strip()
            if url:
                soc += f'<a href="{url}" aria-label="{n}" rel="noopener" target="_blank">{ICON.get(k,"")}</a>'

    return f"""<footer class="site-footer">
 <div class="container">
  <div class="fgrid">
   <div>
    <div class="brandline">{ICON['logo']}<span>{BRAND}</span></div>
    <p>{desc}</p>
    <div class="social">{soc}</div>
   </div>
   <div><h4>Explore</h4><ul>
     {explore_html}
   </ul></div>
   <div><h4>Room Guides</h4><ul>{cats}</ul></div>
   <div><h4>Legal</h4><ul>{legal}</ul></div>
  </div>
  <p class="disc">{disc_text}</p>
  <div class="fbot">
   <span>{copyright}</span>
   <span><a href="{rel}privacy-policy">Privacy</a> &middot; <a href="{rel}cookie-policy">Cookies</a> &middot; <a href="#" onclick="localStorage.removeItem('hdp-consent');location.reload();return false;">Cookie settings</a> &middot; <a href="{rel}sitemap.xml">Sitemap</a></span>
  </div>
 </div>
</footer>
<script>
(function(){{var k='hdp-consent';try{{if(!localStorage.getItem(k)){{var b=document.getElementById('consent');if(b)b.classList.add('show');}}}}catch(e){{}}
function hdp(n){{try{{localStorage.setItem(k,n);}}catch(e){{}}var b=document.getElementById('consent');if(b)b.classList.remove('show');}}}})();
</script>"""


def consent(rel=""):
    return f"""<div class="consent" id="consent" role="dialog" aria-label="Cookie notice">
 <p><b>We use cookies.</b> Essential cookies keep the site working; analytics and advertising cookies help us improve and keep the lights on. Read our <a href="{rel}cookie-policy">Cookie Policy</a>.</p>
 <span class="field"><button class="btn sm" type="button" onclick="hdp('all')">Accept all</button>
 <button class="btn sm ghost" type="button" onclick="hdp('essential')">Essential only</button></span>
</div>"""


def comments_section(rel="", post=None, comments=None):
    """Comment widget — supports built-in anonymous (no login, no external service) + Giscus + Cusdis. Tabbed when both enabled."""
    system = (COMMENT_SYSTEM or "both").lower()
    post = post or {}
    comments = comments or []
    slug = post.get("slug","")
    title = post.get("title","")

    if system == "none":
        return ""

    # Helpers
    def giscus_html():
        if not GISCUS_ENABLED and system != "giscus" and system != "both":
            return ""
        if not GISCUS_CATEGORY_ID:
            return f"""<div class="comments-disabled">
  <p><b>Giscus setup:</b> Install app at <a href="https://github.com/apps/giscus" target="_blank">github.com/apps/giscus</a> → select repo <code>{GISCUS_REPO}</code>. Then go to <a href="https://giscus.app" target="_blank">giscus.app</a> to get IDs.</p>
</div>"""
        return f"""<div class="giscus"></div>
 <script src="https://giscus.app/client.js"
        data-repo="{GISCUS_REPO}"
        data-repo-id="{GISCUS_REPO_ID}"
        data-category="{GISCUS_CATEGORY}"
        data-category-id="{GISCUS_CATEGORY_ID}"
        data-mapping="{GISCUS_MAPPING}"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="{GISCUS_THEME}"
        data-lang="en"
        crossorigin="anonymous"
        async>
 </script>"""

    def cusdis_html():
        if not (CUSDIS_ENABLED or system in ("cusdis","both")):
            return ""
        if not CUSDIS_APP_ID:
            return f"""<div class="comments-disabled">
  <p><b>Cusdis is down or not configured.</b> Get free App ID at <a href="https://cusdis.com" target="_blank">cusdis.com</a> when it's back, or use the built-in anonymous comments below (no external service needed).</p>
</div>"""
        return f"""<div id="cusdis_thread"
  data-host="{CUSDIS_HOST}"
  data-app-id="{CUSDIS_APP_ID}"
  data-page-id="page"
  data-page-url="url"
  data-page-title="title"
  data-theme="{CUSDIS_THEME}"
 ></div>
 <script>
  (function(){{
    var el=document.getElementById('cusdis_thread');
    if(!el)return;
    el.setAttribute('data-page-id', location.pathname);
    el.setAttribute('data-page-url', location.href);
    el.setAttribute('data-page-title', document.title);
  }})();
 </script>
 <script async defer src="{CUSDIS_HOST}/js/cusdis.es.js"></script>"""

    def builtin_html():
        # Built-in anonymous comments — no login, no external service, stored in repo
        # Render existing approved comments
        existing = ""
        if comments:
            items = ""
            for c in comments:
                author = (c.get("author") or "Anonymous").replace("<","&lt;").replace(">","&gt;")[:60]
                body = (c.get("body") or "").replace("<","&lt;").replace(">","&gt;")
                date = c.get("date","")
                # simple markdown-ish line breaks
                body_html = body.replace("\n","<br>")
                items += f'<div class="comment"><div class="comment-meta"><b>{author}</b> <span class="muted">{date}</span></div><p>{body_html}</p></div>'
            existing = f'<div class="comment-list">{items}</div>'
        else:
            existing = '<p class="muted">No comments yet — be the first!</p>'

        # Formspree ID from global — fallback to FormSubmit.co so it works even without Formspree
        form_id = FORMSPREE_ID
        if form_id and form_id != "YOUR_FORM_ID" and len(form_id) > 5:
            form_action = f"https://formspree.io/f/{form_id}"
            extra_hidden = ""
        else:
            # FormSubmit.co works with no signup — first email needs confirmation, then it forwards
            form_action = f"https://formsubmit.co/{EMAIL}"
            extra_hidden = f'<input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{DOMAIN}/thanks">'

        form = f"""<form action="{form_action}" method="POST" class="comment-form" onsubmit="this.querySelector('button').textContent='Sending…';">
  <input type="hidden" name="_subject" value="New comment on {title}">
  <input type="hidden" name="post_slug" value="{slug}">
  <input type="hidden" name="post_url" value="{DOMAIN}/blog/{post.get('cat','')}/{slug}">
  {extra_hidden}
  <div class="form-row"><label for="c-name">Your name</label><input id="c-name" name="name" type="text" placeholder="Alex" required maxlength="60"></div>
  <div class="form-row"><label for="c-comment">Your comment</label><textarea id="c-comment" name="comment" placeholder="Love this idea! I tried it and..." required maxlength="1000" style="min-height:110px"></textarea></div>
  <div class="form-row"><label for="c-email" class="muted" style="font-weight:400">Email (optional, not shown — for reply)</label><input id="c-email" name="email" type="email" placeholder="you@email.com"></div>
  <button class="btn sm" type="submit">Post comment — no login needed</button>
  <p class="muted" style="margin-top:10px;font-size:12.5px">Anonymous, no GitHub needed. Comments are moderated — we approve in Pages CMS → Comments within hours and it appears after next rebuild (1-2 min). {'Using Formspree.' if form_id and form_id!='YOUR_FORM_ID' else 'No Formspree ID yet — using email fallback. Add formspree_id in Site settings for faster delivery.'}</p>
</form>"""

        return f"""{existing}
 <div style="margin-top:26px"><h3 style="font-size:19px;margin:0 0 12px">Leave a comment — no login needed</h3>{form}</div>"""

    # --- BOTH: tabbed, Anonymous (built-in + Cusdis) on top, Giscus below ---
    if system == "both" or (GISCUS_ENABLED and CUSDIS_ENABLED):
        g_html = giscus_html()
        c_html = cusdis_html()
        b_html = builtin_html()
        # Build anonymous pane: built-in always, plus Cusdis if configured (even if down, show note)
        anon_content = b_html
        if CUSDIS_APP_ID:
            anon_content = c_html + "<hr style='margin:28px 0'>" + b_html
        # If both empty, nothing
        if not anon_content and not g_html:
            return ""
        return f"""<section class="comments" id="comments"><div class="container narrow">
 <div class="comments-head"><div><p class="eyebrow">Join the conversation</p><h2>Comments</h2></div>
 <p class="comments-note">Anonymous on top — no login, no GitHub. GitHub comments below.</p></div>

 <div class="comment-tabs">
  <button class="tab active" data-tab="anon" onclick="switchCommentTab('anon')">💬 Anonymous — no login</button>
  <button class="tab" data-tab="giscus" onclick="switchCommentTab('giscus')">🐙 GitHub — with login</button>
 </div>

 <div id="tab-anon" class="tab-pane active">
  {anon_content}
 </div>
 <div id="tab-giscus" class="tab-pane">
  {g_html}
  <noscript><p class="muted">Enable JavaScript to view GitHub comments via Giscus.</p></noscript>
 </div>

 <script>
 function switchCommentTab(which){{
   document.querySelectorAll('.comment-tabs .tab').forEach(b=>b.classList.toggle('active', b.getAttribute('data-tab')===which));
   document.querySelectorAll('.tab-pane').forEach(p=>p.classList.toggle('active', p.id==='tab-'+which));
   try{{localStorage.setItem('hdp-comment-tab', which);}}catch(e){{}}
 }}
 (function(){{
   try{{
     var saved=localStorage.getItem('hdp-comment-tab');
     if(saved) switchCommentTab(saved);
   }}catch(e){{}}
 }})();
 </script>
</div></section>"""

    # --- CUSDIS only ---
    if system == "cusdis":
        c_html = cusdis_html()
        b_html = builtin_html()
        content = c_html if CUSDIS_APP_ID else b_html
        if CUSDIS_APP_ID:
            content = c_html + "<hr style='margin:28px 0'>" + b_html
        return f"""<section class="comments" id="comments"><div class="container narrow">
 <div class="comments-head"><div><p class="eyebrow">Join the conversation</p><h2>Comments</h2></div>
 <p class="comments-note">No login needed — anonymous comments.</p></div>
 {content}
</div></section>"""

    # --- Built-in anonymous only (when comment_system = none? but we want fallback) ---
    if system not in ("giscus","both","cusdis","none"):
        # default to built-in if unknown
        return f"""<section class="comments" id="comments"><div class="container narrow">
 <div class="comments-head"><div><p class="eyebrow">Join the conversation</p><h2>Comments</h2></div></div>
 {builtin_html()}
</div></section>"""

    # --- GISCUS only ---
    g_html = giscus_html()
    if not g_html and not builtin_html():
        return ""
    # If giscus only but we have built-in as fallback for anonymous, show built-in if giscus fails?
    if system == "giscus":
        return f"""<section class="comments" id="comments"><div class="container narrow">
 <div class="comments-head"><div><p class="eyebrow">Join the conversation</p><h2>Comments</h2></div>
 <p class="comments-note">GitHub login required. For anonymous (no login), switch Comment system to Both in Site settings.</p></div>
 {g_html}
</div></section>"""
    # fallback: show built-in
    return f"""<section class="comments" id="comments"><div class="container narrow">
 <div class="comments-head"><div><p class="eyebrow">Join the conversation</p><h2>Comments</h2></div></div>
 {builtin_html()}
</div></section>"""


def _snippets():
    ad = ""
    if ADSENSE_CLIENT:
        ad = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
              f'?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>\n')
    else:
        ad = ('<!-- GOOGLE ADSENSE: add your publisher ID in Pages CMS > Site settings > adsense_client,'
              ' then rebuild. Ads stay off until you do. -->\n')
    ga = ""
    if GA4_ID:
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>\n'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}"
              f"gtag('js',new Date());gtag('config','{GA4_ID}');</script>\n")
    else:
        ga = ('<!-- GOOGLE ANALYTICS 4: add your measurement ID in Pages CMS > Site settings > ga4_id. -->\n')
    pv = (f'<meta name="p:domain_verify" content="{PINTEREST_VERIFY}">\n') if PINTEREST_VERIFY else ""
    return ad, ga, pv


def head(title, desc, rel="", canonical="", schema="", extra="", current="", og="assets/og-default.jpg"):
    adsense_snippet, ga4_snippet, pinterest_snippet = _snippets()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}/{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/{canonical}">
<meta property="og:image" content="{DOMAIN}/{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{DOMAIN}/{og}">
<meta name="theme-color" content="#FBF8F3">

<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='11' fill='%23B5533C'/%3E%3Cpath d='M11 29V20a9 9 0 0 1 18 0v9z' fill='%23F7F1E8'/%3E%3Ccircle cx='20' cy='18' r='3.6' fill='%23C08B48'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- Google Fonts is optional. Delete these two lines and the site still looks right using Georgia/system fonts. -->
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
{adsense_snippet}{ga4_snippet}{pinterest_snippet}
{f'<script type="application/ld+json">{schema}</script>' if schema else ""}
<style>{CSS}</style>
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(rel, current)}"""
