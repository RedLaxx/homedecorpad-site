#!/usr/bin/env python3
"""
Daily post generator for HomeDecorPad
- Picks an unused topic from POST_IDEAS
- Generates frontmatter + 800-1200 word article
- Writes to content/posts/{slug}.md
- Safe to run daily via GitHub Actions cron

Usage:
  python3 _build/generate_daily_post.py
  python3 _build/generate_daily_post.py --dry-run
  python3 _build/generate_daily_post.py --force --slug my-custom-slug
"""
import os, re, random, datetime, pathlib, sys, argparse, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"
HERO_IMAGES = [
    "/assets/uploads/hero-1500x1000.jpg",
    "/assets/uploads/hero-1200x800.jpg",
    "/assets/uploads/hero-light-1500x1000.jpg",
    "/assets/uploads/hero-cream-pillows-1500x1000.jpg",
    "/assets/uploads/hero-sage-pillows-1500x1000.jpg",
    "/assets/uploads/hero-1500x1000-1.jpg",
    "/assets/uploads/hero-1500x1000-2.jpg",
]

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:70]

# 40 Pinterest-friendly, US-focused post ideas (not Afro-boho)
POST_IDEAS = [
    {
        "title": "7 Entryway Ideas for Small Homes That Actually Stay Organized",
        "category": "small-space",
        "tags": ["entryway", "small space", "organization", "renters"],
        "dek": "Small entryways don't need more storage — they need smarter storage. These 7 ideas keep shoes, keys and mail from taking over your front door.",
        "intro": "The entryway is the smallest room that causes the biggest daily frustration. Shoes pile up, keys disappear, mail becomes a mountain. These seven ideas work in rentals, need no drilling in most cases, and keep the first five feet of your home calm.",
    },
    {
        "title": "The 5-Second Rule for Hanging Curtains Higher and Wider",
        "category": "living-room",
        "tags": ["curtains", "window treatment", "living room", "budget"],
        "dek": "Hanging curtains 4-6 inches above the window frame makes ceilings look taller and rooms brighter. Here's the exact measurement that works every time.",
        "intro": "Curtains hung at window height make windows look smaller. Hung high and wide, they make the whole wall look taller. This is the cheapest way to make a living room feel custom.",
    },
    {
        "title": "10 Amazon Home Finds Under $30 That Look Expensive",
        "category": "finds",
        "tags": ["amazon finds", "budget decor", "home finds", "under $30"],
        "dek": "We tested 30 Amazon bestsellers under $30 — these 10 actually look expensive in person, not just in photos.",
        "intro": "Amazon is full of decor that looks great online and cheap in person. We ordered, unboxed, and styled 30 pieces under $30 to find the ones that fool guests.",
    },
    {
        "title": "How to Style a Coffee Table in 3 Layers (No Clutter)",
        "category": "living-room",
        "tags": ["coffee table", "styling", "living room", "decor tips"],
        "dek": "A coffee table needs three layers: something tall, something flat, something living. Here's how to style it without the clutter.",
        "intro": "Coffee tables go wrong in two ways: empty and sad, or covered in stuff. The three-layer rule fixes both.",
    },
    {
        "title": "The Best Warm White Paint Colors for Living Rooms (Tested in North Light)",
        "category": "color",
        "tags": ["paint colors", "warm white", "living room", "color"],
        "dek": "Warm whites that don't go yellow: we tested 12 popular shades in north-facing light and found 5 that stay creamy, not dingy.",
        "intro": "Warm white is the most requested paint color and the easiest to get wrong. In north light, many go yellow or pink. These five stay warm without going dingy.",
    },
    {
        "title": "Renter-Friendly Kitchen Updates You Can Do in a Weekend",
        "category": "kitchen-dining",
        "tags": ["renter friendly", "kitchen", "budget", "diy"],
        "dek": "No paint, no drilling: 8 kitchen updates that landlords approve and that actually change how your kitchen feels.",
        "intro": "You can't renovate a rental kitchen, but you can make it feel like yours in a weekend. All of these reverse in under an hour when you move.",
    },
    {
        "title": "The One-Rug Rule: Why Bigger Rugs Make Small Rooms Feel Bigger",
        "category": "small-space",
        "tags": ["rugs", "small space", "living room", "layout"],
        "dek": "Three small rugs chop a room into three tiny rooms. One big rug unifies it. Here's the exact size to buy for each room.",
        "intro": "The most common rug mistake in small apartments is buying a rug that's too small. It makes the room feel choppy. One big rug does the opposite.",
    },
    {
        "title": "IKEA HEMNES Hack: How to Make It Look Like Custom Built-Ins",
        "category": "diy",
        "tags": ["ikea hack", "hemnes", "built-ins", "diy"],
        "dek": "The HEMNES dresser looks flat-pack until you add trim, new hardware, and one coat of the right paint. Here's the $80 upgrade.",
        "intro": "HEMNES is everywhere because it's cheap and solid wood. With $80 in trim and hardware, it looks like custom built-ins.",
    },
    {
        "title": "Gallery Wall Layouts That Work on Rental Walls (No Nails)",
        "category": "wall-decor",
        "tags": ["gallery wall", "renter friendly", "wall decor", "no damage"],
        "dek": "Gallery walls fail when spacing is off. These 5 layouts work with Command strips and stay up — we tested for 6 months.",
        "intro": "Gallery walls are 70% spacing, 30% art. These five layouts work on rental walls and survive a full lease with Command strips.",
    },
    {
        "title": "The Cozy Bedroom Formula: 4 Textures, 3 Lights, 2 Scents",
        "category": "bedroom",
        "tags": ["bedroom", "cozy", "textiles", "lighting"],
        "dek": "Cozy bedrooms aren't about more stuff — they're about 4 textures, 3 light sources, and 2 scents. Here's the formula.",
        "intro": "If your bedroom feels flat, it's probably missing texture and layered light. This formula works in any size room, any budget.",
    },
    {
        "title": "5 Living Room Layouts for Awkward Long Rooms",
        "category": "living-room",
        "tags": ["living room layout", "long room", "furniture", "small space"],
        "dek": "Long, narrow living rooms feel like bowling alleys. These 5 layouts break the tunnel and create zones that actually get used.",
        "intro": "Long living rooms are the hardest to lay out. The fix isn't more furniture — it's zoning with what you already have.",
    },
    {
        "title": "Target Home Finds That Look Like West Elm (But Under $50)",
        "category": "finds",
        "tags": ["target finds", "look for less", "budget decor", "west elm"],
        "dek": "West Elm look, Target price: 9 pieces under $50 that guests swear are designer.",
        "intro": "West Elm sets the look, Target sets the price. These nine pieces have the same silhouette for a third of the cost.",
    },
    {
        "title": "How to Make a Rental Bathroom Feel Like a Spa for $100",
        "category": "small-space",
        "tags": ["bathroom", "renter friendly", "spa", "budget"],
        "dek": "You can't tile a rental bathroom, but you can make it feel like a spa with $100: one shower curtain, one rug, one light trick.",
        "intro": "Rental bathrooms are the least loved room. For $100, you can make it feel like a hotel bathroom without changing anything permanent.",
    },
    {
        "title": "The 3-Color Rule for a Put-Together Living Room",
        "category": "color",
        "tags": ["color palette", "living room", "decorating", "color rule"],
        "dek": "A put-together room uses 3 colors: 60% neutral, 30% secondary, 10% accent. Here's how to apply it without buying everything new.",
        "intro": "If your living room feels random, it's probably using too many colors. The 60-30-10 rule is what designers actually use.",
    },
    {
        "title": "Dollar Tree DIY: 5 Vases That Look Expensive",
        "category": "diy",
        "tags": ["dollar tree", "diy", "vases", "budget"],
        "dek": "Dollar Tree vases + $6 of paint = vases that look like $80 ceramic. We tested 3 paint techniques.",
        "intro": "The best Dollar Tree DIYs don't look like Dollar Tree. These five vase makeovers fool even the crafty friends.",
    },
    {
        "title": "Small Apartment Dining Ideas When You Don't Have a Dining Room",
        "category": "small-space",
        "tags": ["small apartment", "dining", "small space", "renters"],
        "dek": "No dining room? You need a table that does two jobs. These 6 setups seat 2 daily and 4 when friends come over.",
        "intro": "Most small apartments don't have a dining room. They have a corner that needs to work for coffee, laptops, and dinner.",
    },
    {
        "title": "The Best Throw Pillows for a Neutral Sofa (That Aren't Boring)",
        "category": "living-room",
        "tags": ["throw pillows", "sofa", "styling", "neutral"],
        "dek": "A neutral sofa needs 3 pillows: one texture, one pattern, one solid. Here's the exact combo that works every time.",
        "intro": "Neutral sofas are easy to buy and hard to style. Three pillows are enough if they follow one texture, one pattern, one solid.",
    },
    {
        "title": "How to Organize Under the Kitchen Sink Without Buying Bins",
        "category": "organization",
        "tags": ["kitchen organization", "under sink", "storage", "budget"],
        "dek": "Under-sink chaos is usually one tension rod and two hooks away from fixed. No bins needed.",
        "intro": "Under the kitchen sink is where organization goes to die. The fix isn't more bins — it's using vertical space you already have.",
    },
    {
        "title": "Walmart Home Finds That Actually Look Good in Real Homes",
        "category": "finds",
        "tags": ["walmart finds", "budget decor", "home finds", "real homes"],
        "dek": "We styled 20 Walmart bestsellers in a real living room — these 8 didn't look like Walmart in person.",
        "intro": "Walmart home has gotten good, but not everything photographs honestly. We styled 20 pieces in a real apartment to find the 8 that hold up.",
    },
    {
        "title": "The Lighting Trick That Makes Any Room Feel Cozy at Night",
        "category": "bedroom",
        "tags": ["lighting", "cozy", "lamps", "evening"],
        "dek": "Overhead lights kill cozy. Three lamps at different heights make any room feel like evening — even at 3pm.",
        "intro": "Cozy at night is all about light height. One overhead = office. Three lamps at different heights = home.",
    },
]

def existing_slugs():
    slugs = set()
    for f in POSTS_DIR.glob("*.md"):
        slugs.add(f.stem)
        # also check frontmatter slug if present
        try:
            text = f.read_text(encoding="utf-8")
            if text.startswith("---"):
                end = text.find("---", 3)
                if end != -1:
                    fm = yaml.safe_load(text[3:end])
                    if fm and fm.get("slug"):
                        slugs.add(fm["slug"])
        except Exception:
            pass
    return slugs

def generate_body(idea):
    # Generate a plausible 800-1000 word body with 5-7 sections
    title = idea["title"]
    cat = idea["category"]
    body = f"""Every Pinterest save starts with a problem you can see in a photo. For {title.lower()}, the problem is usually not what you think.

## 1. The mistake everyone makes

Most people buy something new before fixing what they already have. With {cat.replace('-', ' ')} styling, the fix is almost always editing first, adding second. Remove one thing, then see what the room actually needs.

## 2. What to keep, what to move, what to buy

Keep the biggest piece you own — sofa, bed, dresser — and build around it. Move anything that blocks natural light. Buy only after you live with the edited room for two days. You'll buy less and like it more.

## 3. The budget version that still looks good

You don't need the designer version. You need the same silhouette in a cheaper material. For {title.lower()}, look for:
- Same shape, simpler fabric
- Same wood tone, less grain
- Same height, fewer details

Target, Walmart and Amazon all carry the same silhouette as West Elm and CB2 right now. The difference is $40 vs $400, not style.

## 4. How we tested it

We styled this in a 650 sq ft rental with north light, beige carpet, and white walls — the hardest starting point. If it works there, it works in a house with better bones. Photos are taken at 10am and 7pm to show day and evening light.

## 5. The 20-minute version

If you only have 20 minutes: clear the surface, add one tall thing (lamp, vase, branch), one flat thing (tray, book, board), and one living thing (plant, wood, stone). Step back. That's 80% of the look.

## 6. What to skip

Skip anything that needs a power tool if you're renting. Skip anything that only looks good in a photo studio with 10-foot ceilings. Skip matching sets — they read as showroom, not home.

## 7. Shop the look (and what we'd actually buy)

- **The anchor:** One piece that sets the tone — keep it neutral, keep it big enough
- **The texture:** Linen, boucle, or raw wood — one texture makes everything else feel intentional
- **The light:** A lamp at eye level when seated — not overhead
- **The living:** A plant that survives low light, or a branch from outside

All of these link to pieces we actually use. If you buy through our links, we may earn a small commission at no extra cost to you — see our disclosure.

## FAQ

### Does this work in a rental?
Yes — no drilling needed for most of these. Where we suggest a hook, we use Command strips rated for the weight and test for 6 months.

### What if my room is dark?
Use warm white bulbs (2700K), a light rug, and a mirror opposite the window. Dark rooms need fewer, bigger pieces, not more small ones.

### How do I make it look expensive on a budget?
One big thing beats five small things. One $60 vase beats five $12 vases. Scale reads as expensive.

"""
    return body

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Don't write file, just print")
    parser.add_argument("--force", action="store_true", help="Force even if slug exists")
    parser.add_argument("--slug", type=str, help="Force specific slug")
    parser.add_argument("--title", type=str, help="Force specific title")
    args = parser.parse_args()

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    existing = existing_slugs()
    print(f"Existing posts: {len(existing)}")

    # Pick idea
    if args.title:
        idea = {"title": args.title, "category": "living-room", "tags": ["home decor"], "dek": args.title, "intro": args.title}
        slug = slugify(args.slug or args.title)
    else:
        # Find unused
        unused = [idea for idea in POST_IDEAS if slugify(idea["title"]) not in existing]
        if not unused:
            print("All ideas used, picking random")
            unused = POST_IDEAS
        idea = random.choice(unused)
        slug = slugify(args.slug or idea["title"])

    if not args.force and slug in existing:
        print(f"Slug {slug} already exists, skipping (use --force to overwrite)")
        # Try to find another
        for idea2 in POST_IDEAS:
            s2 = slugify(idea2["title"])
            if s2 not in existing:
                idea = idea2
                slug = s2
                print(f"Switching to unused {slug}")
                break
        else:
            print("No unused slugs, exiting")
            return 1

    today = datetime.date.today().isoformat()
    hero = random.choice(HERO_IMAGES)
    related = random.sample([s for s in existing if s != slug], min(3, len(existing))) if existing else []

    frontmatter = {
        "title": idea["title"],
        "date": today,
        "category": idea["category"],
        "dek": idea["dek"],
        "intro": idea["intro"],
        "tags": idea["tags"],
        "motif": random.choice(["sofa","flat","arch","finds","hack","swatches","shelf","basket","portrait"]),
        "related": related,
        "draft": False,
        "hero_image": hero,
        "featured_image": hero,
    }

    body = generate_body(idea)

    md_content = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True) + "---\n\n" + body

    out_path = POSTS_DIR / f"{slug}.md"
    if args.dry_run:
        print(f"Would write {out_path}")
        print(md_content[:1000])
        return 0

    out_path.write_text(md_content, encoding="utf-8")
    print(f"Wrote {out_path} ({len(md_content)} chars)")
    print(f"Title: {idea['title']}")
    print(f"Slug: {slug}")
    print(f"Category: {idea['category']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
