"""Synthetic trademark generator: coined names, Nice classes, goods, owners, dates, statuses.

Deterministic for a given random.Random instance.
"""
import random
from datetime import date, timedelta

# ~200 syllables used to build 2-3 syllable coined words
SYLLABLES = """
zen tar nova tek sol plex arc lux vex ori ka ze ra mi lo vi qua tri neo cor
vat pix bri sky flo gen cy dex max ion nex tra syn ver kin zo lu fi mo ny
pra sto cal dor mer ven fin gro hal jet kor lim mag nim opt pul quo ret sig
tor ul val wex xan yel zir bel cam dun eko fal gal hyl ima jun kel lan mon
nar ola pen qui ros sen tul ura vor wil xen yor zul ax bo cel da el fo gu
hy in jo ke la ma ne or pa qi ru sa ti un vo wa xi ya zu alp bix cro dyn
evo fyr glo hex ilo jax kry lyt myx nyx oxi pyr qor rho sym thy ulo vyn wyn
xyl yra zyn aer bra cle dri ely fra gle hra ira jor kla lom mor nol omi pro
ruk sar tem uri vin wol xer yon zor ame bon cin dal eri fen gor hin ive jin
kon lar mal nin opa pel rin sel tan ume vel zan ari bas cot dia esk
""".split()

VOWELS = "aeiou"

# Class weights: everything gets weight 1, the six high-frequency classes get more.
HEAVY_CLASSES = {9: 12, 25: 9, 35: 9, 42: 11, 41: 7, 43: 7}
CLASS_WEIGHTS = [HEAVY_CLASSES.get(c, 1) for c in range(1, 46)]

STATUSES = ["registered", "pending", "opposed", "dead"]
STATUS_WEIGHTS = [60, 20, 10, 10]

OWNER_PREFIXES = [
    "Apex", "Nova", "Stellar", "Summit", "Pinnacle", "Vertex", "Orion", "Atlas", "Zenith", "Horizon",
    "Quantum", "Crimson", "Silver", "Blue Ridge", "Evergreen", "Northwind", "Ironclad", "Lumen", "Cobalt", "Granite",
    "Harbor", "Meridian", "Polaris", "Redwood", "Sterling",
]
OWNER_SUFFIXES = [
    "Technologies", "Holdings", "Group", "Labs", "Industries", "Ventures", "Partners", "Systems", "Brands", "Enterprises",
    "Solutions", "Collective", "Corporation", "Works", "Co.", "Innovations", "Global", "Studios", "Foods", "Apparel",
]

# Shared word pools (~30 each)
POOLS: dict[str, list[str]] = {
    "domain": [
        "healthcare", "logistics", "finance", "education", "retail", "real estate", "agriculture", "hospitality",
        "manufacturing", "insurance", "legal practice", "construction", "energy management", "telecommunications",
        "human resources", "supply chain", "e-commerce", "fitness", "travel", "media production", "gaming",
        "cybersecurity", "automotive", "biotechnology", "fleet management", "event planning", "nonprofit management",
        "restaurant management", "property management", "customer support",
    ],
    "purpose": [
        "tracking fitness goals", "managing personal budgets", "ordering food", "booking travel", "learning languages",
        "monitoring sleep", "sharing photos", "streaming music", "scheduling appointments", "managing tasks",
        "online dating", "meditation", "tracking deliveries", "splitting bills", "renting cars", "finding parking",
        "managing medication", "planning meals", "home automation", "remote team collaboration", "reading e-books",
        "trading stocks", "managing loyalty rewards", "monitoring air quality", "tracking pets", "taking notes",
        "video conferencing", "creating invoices", "language translation", "managing passwords",
    ],
    "thing": [
        "publications", "newsletters", "magazines", "books", "manuals", "guides", "music files", "video recordings",
        "podcasts", "image files", "game software", "comic books", "course materials", "white papers",
        "audio books", "templates", "fonts", "stickers", "ringtones", "wallpapers", "maps", "brochures",
        "databases", "spreadsheets", "reports", "catalogues", "journals", "sheet music", "presentations", "tickets",
    ],
    "device": [
        "smartwatches", "headphones", "earbuds", "computer mice", "keyboards", "webcams", "routers", "smart speakers",
        "fitness trackers", "tablets", "laptop computers", "battery chargers", "USB cables", "power banks",
        "virtual reality headsets", "drones", "dash cameras", "thermostats", "sensors", "monitors", "projectors",
        "barcode scanners", "GPS navigation devices", "smart glasses", "microphones", "hard drives",
        "memory cards", "smart locks", "doorbell cameras", "e-readers",
    ],
    "material": [
        "cotton", "wool", "silk", "linen", "leather", "denim", "cashmere", "polyester", "fleece", "nylon",
        "organic cotton", "merino wool", "bamboo fibre", "suede", "corduroy", "velvet", "hemp", "jersey",
        "flannel", "satin", "tweed", "canvas", "spandex", "recycled polyester", "chambray", "chiffon",
        "knitted", "waterproof", "lightweight", "thermal",
    ],
    "garment": [
        "shirts", "t-shirts", "jackets", "coats", "trousers", "jeans", "dresses", "skirts", "sweaters",
        "hoodies", "shorts", "blouses", "vests", "pyjamas", "scarves", "gloves", "socks", "leggings",
        "tracksuits", "swimwear", "underwear", "blazers", "cardigans", "overalls", "rain jackets",
        "polo shirts", "tank tops", "parkas", "tunics", "jumpsuits",
    ],
    "style": [
        "casual", "athletic", "formal", "outdoor", "children's", "women's", "men's", "vintage", "streetwear",
        "hiking", "running", "orthopaedic", "luxury", "waterproof", "vegan", "minimalist", "skate", "dress",
        "work", "beach", "winter", "tennis", "golf", "climbing", "cycling", "dance", "trail", "slip-on",
        "lace-up", "high-top",
    ],
    "footwear": [
        "shoes", "sneakers", "boots", "sandals", "slippers", "loafers", "trainers", "flip-flops", "clogs",
        "moccasins", "espadrilles", "ankle boots", "pumps", "mules", "oxfords", "brogues", "wellingtons",
        "football boots", "ballet flats", "flats",
    ],
    "headwear": ["hats", "caps", "beanies", "visors", "berets", "headbands", "bucket hats", "sun hats"],
    "service": [
        "marketing", "advertising", "branding", "market research", "public relations", "social media marketing",
        "search engine optimisation", "business consulting", "human resources consulting", "payroll administration",
        "bookkeeping", "data processing", "event promotion", "influencer marketing", "lead generation",
        "customer relationship management", "franchise consulting", "procurement", "business analytics",
        "recruitment", "trade show organisation", "affiliate marketing", "email marketing", "office administration",
        "brand strategy", "sales promotion", "tax preparation", "auction services", "import-export agency",
        "outsourcing",
    ],
    "goods": [
        "clothing", "electronics", "cosmetics", "furniture", "jewellery", "sporting goods", "toys", "books",
        "pet supplies", "kitchenware", "groceries", "home decor", "gardening supplies", "footwear", "beauty products",
        "health supplements", "office supplies", "art supplies", "musical instruments", "bicycles", "outdoor gear",
        "baby products", "watches", "luggage", "eyewear", "craft beer", "coffee", "tea", "wine", "candles",
    ],
    "subject": [
        "computer programming", "mathematics", "foreign languages", "cooking", "photography", "music", "yoga",
        "business management", "personal finance", "art history", "data science", "public speaking",
        "creative writing", "graphic design", "nutrition", "leadership", "first aid", "dance", "chess",
        "robotics", "digital marketing", "woodworking", "sustainability", "film making", "meditation",
        "martial arts", "career development", "parenting", "astronomy", "entrepreneurship",
    ],
    "event": [
        "conferences", "workshops", "seminars", "concerts", "festivals", "exhibitions", "competitions",
        "marathons", "webinars", "hackathons", "film screenings", "comedy shows", "esports tournaments",
        "summer camps", "book fairs", "award ceremonies",
    ],
    "cuisine": [
        "Italian", "Japanese", "Mexican", "Thai", "Indian", "French", "vegan", "Mediterranean", "Korean",
        "Vietnamese", "Lebanese", "Greek", "Spanish", "Chinese", "Ethiopian", "Peruvian", "Nordic", "Caribbean",
        "Turkish", "Brazilian", "Moroccan", "farm-to-table", "seafood", "barbecue", "brunch", "vegetarian",
        "gluten-free", "fusion", "street food", "Hawaiian",
    ],
    "food": [
        "pizza", "burgers", "sushi", "tacos", "noodles", "sandwiches", "salads", "coffee", "smoothies",
        "baked goods", "ice cream", "juice", "dumplings", "ramen", "bubble tea", "crepes", "bagels",
        "fried chicken", "poke bowls", "waffles", "kebabs", "pastries", "doughnuts", "curries",
    ],
    "adj": [
        "organic", "premium", "eco-friendly", "natural", "biodegradable", "professional-grade", "industrial",
        "high-performance", "portable", "handmade", "artisanal", "recycled", "compact", "heavy-duty",
        "fragrance-free", "hypoallergenic", "vegan", "luxury", "lightweight", "commercial", "decorative",
        "custom", "non-toxic", "waterproof", "rechargeable", "reusable", "concentrated", "fast-acting",
        "plant-based", "low-sugar",
    ],
}

# 10-15 templates per Nice class. Placeholders are POOLS keys.
GOODS_TEMPLATES: dict[int, list[str]] = {
    1: ["{adj} industrial chemicals", "chemical additives for use in {domain}", "fertilisers for agricultural use",
        "{adj} adhesives for industrial purposes", "unprocessed artificial resins", "soil conditioning preparations",
        "chemical reagents for laboratory use", "fire extinguishing compositions", "{adj} plant growth regulators",
        "water treatment chemicals", "biochemical catalysts for {domain}"],
    2: ["{adj} interior paints", "exterior wall paints and primers", "wood stains and varnishes",
        "anti-rust coatings for metal", "printing inks", "{adj} colourants for {goods}", "automotive paint",
        "lacquers for furniture", "artists' paints", "powder coatings for industrial use"],
    3: ["{adj} skin care preparations", "{adj} shampoos and conditioners", "perfumes and eau de toilette",
        "{adj} laundry detergents", "cosmetic makeup preparations", "essential oils for aromatherapy",
        "{adj} toothpaste", "nail polish and nail care preparations", "{adj} soaps", "{adj} household cleaning preparations",
        "sunscreen preparations", "hair styling gels and waxes"],
    4: ["industrial lubricants", "motor oils for vehicles", "{adj} candles", "scented candles and wicks",
        "fuel for heating", "biofuels", "charcoal for barbecues", "wax for industrial use", "lamp oils",
        "dust binding compositions"],
    5: ["{adj} dietary supplements", "pharmaceutical preparations for treating allergies", "vitamin supplements",
        "veterinary preparations", "first aid kits", "{adj} disinfectants", "medicated skin creams",
        "protein supplements for athletes", "pain relief medication", "herbal remedies", "baby formula",
        "medicated lozenges"],
    6: ["metal building materials", "metal hardware, namely screws, nails and bolts", "aluminium sheets",
        "metal storage containers", "steel pipes", "metal door handles", "safes of metal", "metal fencing panels",
        "{adj} metal water bottles", "metal tool boxes"],
    7: ["power-operated tools", "{adj} industrial robots", "electric motors for machines", "agricultural machinery",
        "3D printers", "vacuum cleaners", "kitchen food processors, electric", "lawn mowers", "packaging machines",
        "machine parts, namely gears and bearings", "pumps for industrial use"],
    8: ["hand tools", "kitchen knives", "{adj} cutlery", "razors and razor blades", "garden pruning shears",
        "screwdrivers and wrenches", "manicure sets", "hand-operated drills", "multi-tools", "shaving implements"],
    9: ["software for {domain}", "mobile application for {purpose}", "downloadable electronic {thing}",
        "downloadable software for {purpose}", "computer software for data analytics in {domain}",
        "{device}", "wearable {device}", "computer hardware", "downloadable mobile game software",
        "computer security software", "artificial intelligence software for {domain}",
        "downloadable software development kits", "protective cases for {device}", "smart home {device}",
        "virtual reality software"],
    10: ["medical diagnostic apparatus", "surgical instruments", "{adj} orthopaedic supports", "dental instruments",
         "hearing aids", "blood pressure monitors", "massage apparatus", "veterinary instruments",
         "medical thermometers", "physiotherapy apparatus", "wearable health monitoring devices"],
    11: ["LED lighting fixtures", "air purifiers", "{adj} water filters", "heating apparatus", "air conditioners",
         "cooking ovens", "ceiling fans", "water heaters", "bathroom fixtures", "electric kettles", "refrigerators"],
    12: ["electric bicycles", "electric scooters", "automobiles", "bicycle parts", "car seat covers",
         "motorcycles", "tyres for vehicles", "strollers", "drones for transport", "electric vehicle charging adaptors",
         "boats"],
    13: ["fireworks", "firearms", "ammunition", "signal flares", "air guns", "explosive powders",
         "gun cases", "rocket launching apparatus", "party poppers", "pyrotechnic products"],
    14: ["{adj} jewellery", "wristwatches", "smartwatch straps", "necklaces and bracelets", "rings",
         "precious stones", "earrings", "jewellery boxes", "clocks", "cufflinks", "keyrings"],
    15: ["guitars", "electronic keyboards", "drums", "violins", "musical instrument cases", "ukuleles",
         "music stands", "guitar strings", "harmonicas", "synthesizers"],
    16: ["printed books", "stationery", "notebooks and journals", "greeting cards", "art prints",
         "{adj} paper packaging", "office supplies", "printed magazines about {subject}", "calendars",
         "pens and pencils", "stickers", "educational printed materials about {subject}"],
    17: ["rubber seals", "insulating materials", "plastic film for packaging", "garden hoses", "rubber gaskets",
         "foam padding", "acoustic insulation panels", "flexible tubes, not of metal", "weatherstripping",
         "{adj} plastic sheeting"],
    18: ["{adj} handbags", "backpacks", "luggage", "wallets", "umbrellas", "leather goods", "pet collars and leashes",
         "travel bags", "briefcases", "tote bags", "clothing for pets", "saddlery"],
    19: ["wood flooring", "ceramic tiles", "concrete building materials", "{adj} non-metal building materials",
         "glass panels for building", "stone for construction", "asphalt", "plastic pipes", "timber",
         "prefabricated houses, not of metal"],
    20: ["{adj} furniture", "office chairs", "mattresses", "mirrors", "picture frames", "pillows", "bookshelves",
         "outdoor furniture", "pet beds", "storage containers, not of metal", "kitchen cabinets", "standing desks"],
    21: ["{adj} cookware", "kitchen utensils", "glassware", "coffee mugs", "{adj} water bottles", "lunch boxes",
         "cleaning brushes", "porcelain tableware", "food storage containers", "toothbrushes", "wine glasses",
         "pet feeding bowls"],
    22: ["camping tents", "ropes", "tarpaulins", "hammocks", "fishing nets", "awnings", "sails",
         "cotton stuffing materials", "mesh bags", "climbing ropes"],
    23: ["{material} yarns", "sewing threads", "embroidery threads", "knitting yarn", "spun silk",
         "elastic threads", "cotton threads", "wool yarn", "nylon threads", "metallic threads for embroidery"],
    24: ["{material} fabrics", "bed linen", "towels", "curtains", "blankets", "table linen", "upholstery fabrics",
         "{adj} bath towels", "quilts", "sleeping bags", "textile wall hangings"],
    25: ["{material} {garment}", "{style} {footwear}", "{style} {garment}", "{material} {headwear}",
         "{style} clothing", "{material} {garment} and {garment}", "{style} {headwear}", "{style} sportswear",
         "children's {garment}", "{material} outerwear", "{style} activewear", "belts for clothing",
         "{adj} {garment}", "uniforms", "{style} {footwear} and {headwear}"],
    26: ["hair accessories", "buttons", "lace and embroidery", "sewing needles", "artificial flowers",
         "ribbons and bows", "hair extensions", "zippers", "patches for clothing", "badges for wear"],
    27: ["{adj} carpets", "rugs", "yoga mats", "door mats", "wallpaper", "floor coverings", "artificial turf",
         "bath mats", "gym mats", "vinyl flooring"],
    28: ["toys", "board games", "video game consoles", "sporting goods", "fitness equipment", "puzzles",
         "{adj} toys", "golf equipment", "skateboards", "playing cards", "dolls", "fishing tackle", "yoga blocks",
         "game controllers"],
    29: ["{adj} dairy products", "processed meats", "frozen vegetables", "yogurt", "cheese", "jams and jellies",
         "edible oils", "{adj} plant-based meat substitutes", "canned fish", "nut butters", "soups",
         "potato chips"],
    30: ["coffee", "tea", "chocolate", "{adj} snack bars", "bread and pastries", "pasta", "sauces and condiments",
         "ice cream", "breakfast cereals", "honey", "spices", "{adj} confectionery", "rice", "baking mixes"],
    31: ["fresh fruits and vegetables", "pet food", "{adj} animal feed", "live plants", "seeds for planting",
         "fresh flowers", "raw grains", "fresh herbs", "malt for brewing", "bird seed", "unprocessed nuts"],
    32: ["craft beers", "energy drinks", "{adj} fruit juices", "mineral water", "sparkling water",
         "non-alcoholic beverages", "smoothies", "sports drinks", "kombucha", "syrups for making beverages"],
    33: ["wines", "spirits", "vodka", "gin", "whisky", "liqueurs", "hard cider", "sparkling wine", "rum",
         "pre-mixed alcoholic beverages"],
    34: ["cigars", "tobacco", "electronic cigarettes", "lighters for smokers", "matches", "pipe tobacco",
         "rolling papers", "smokers' articles", "oral vaporizers", "ashtrays"],
    35: ["{service} services", "online retail store services featuring {goods}", "{service} services for {domain}",
         "retail store services featuring {goods}", "business management consulting in the field of {domain}",
         "advertising services for {goods}", "online marketplace for buyers and sellers of {goods}",
         "{service} and {service} services", "wholesale distributorship of {goods}",
         "promoting the goods of others in the field of {goods}", "business administration services",
         "personnel recruitment services in {domain}"],
    36: ["banking services", "insurance services", "real estate brokerage", "financial investment services",
         "payment processing services", "cryptocurrency exchange services", "mortgage lending", "financial advisory",
         "crowdfunding services", "insurance brokerage for {domain}", "venture capital financing"],
    37: ["construction services", "building renovation", "electrical installation", "plumbing services",
         "vehicle repair", "roofing services", "computer hardware repair", "HVAC installation",
         "cleaning of buildings", "solar panel installation", "painting and decorating"],
    38: ["telecommunication services", "video streaming services", "internet service provider services",
         "providing online chat rooms", "mobile phone services", "podcast transmission", "email services",
         "providing online forums about {subject}", "satellite transmission", "video conferencing services"],
    39: ["delivery of goods", "freight transport", "travel arrangement", "warehousing", "ride-sharing services",
         "logistics for {domain}", "car rental", "courier services", "parcel tracking", "airline services",
         "moving services", "bicycle rental"],
    40: ["custom 3D printing", "recycling of waste", "water treatment", "printing services", "metal treatment",
         "custom manufacturing of {goods}", "food preservation", "dyeing of textiles", "air purification",
         "woodworking services"],
    41: ["educational services, namely courses in {subject}", "online courses in {subject}",
         "organising {event}", "entertainment services, namely {event}", "providing training in {subject}",
         "fitness classes", "publishing of electronic books about {subject}", "tutoring in {subject}",
         "organising sporting {event}", "music production services", "providing non-downloadable online {thing}",
         "workshops and seminars in {subject}", "film production", "providing online video games"],
    42: ["software as a service for {domain}", "platform as a service featuring software for {purpose}",
         "design and development of software for {domain}", "cloud computing services for {domain}",
         "providing temporary use of non-downloadable software for {purpose}", "website hosting services",
         "IT consulting in the field of {domain}", "data encryption services", "scientific research in {domain}",
         "software as a service featuring artificial intelligence for {domain}", "cybersecurity services for {domain}",
         "user interface design services", "computer programming for {domain}", "technical support services"],
    43: ["restaurant services featuring {cuisine} cuisine", "cafe services", "{cuisine} restaurant services",
         "catering services", "take-out restaurant services featuring {food}", "bar services",
         "hotel services", "food truck services featuring {food}", "coffee shop services", "{cuisine} catering",
         "providing food and drink featuring {food}", "bakery cafe services", "temporary accommodation services",
         "restaurant services featuring {food}"],
    44: ["medical clinic services", "beauty salon services", "spa services", "veterinary services",
         "dental services", "physiotherapy", "hairdressing services", "nutrition counselling", "mental health counselling",
         "landscape gardening", "pet grooming"],
    45: ["legal services", "security guard services", "online social networking services", "dating services",
         "intellectual property consulting", "personal styling services", "funeral services",
         "background checks", "pet sitting", "licensing of intellectual property", "babysitting services"],
}


def fill_template(rng: random.Random, template: str) -> str:
    out = template
    # Fill one placeholder at a time so repeated keys get different values.
    while "{" in out:
        start = out.index("{")
        end = out.index("}", start)
        key = out[start + 1 : end]
        out = out[:start] + rng.choice(POOLS[key]) + out[end + 1 :]
    return out


def make_goods(rng: random.Random, nice_class: int) -> str:
    return fill_template(rng, rng.choice(GOODS_TEMPLATES[nice_class]))


def make_owners(rng: random.Random, n: int = 500) -> list[str]:
    combos = [f"{p} {s}" for p in OWNER_PREFIXES for s in OWNER_SUFFIXES]
    rng.shuffle(combos)
    return combos[:n]


def coined_word(rng: random.Random) -> str:
    n = rng.choice([2, 2, 3, 3, 3])
    word = "".join(rng.choice(SYLLABLES) for _ in range(n))
    if len(word) > 11:
        word = word[:11]
    return word.capitalize()


# --- phonetic variants for collision groups ---------------------------------

def _swap_sibilant(w: str, rng: random.Random) -> str:
    pairs = [("z", "s"), ("s", "z"), ("x", "z"), ("z", "x"), ("x", "ks"), ("s", "x")]
    rng.shuffle(pairs)
    for a, b in pairs:
        if a in w:
            i = rng.choice([k for k, ch in enumerate(w) if w.startswith(a, k)])
            return w[:i] + b + w[i + len(a) :]
    return w


def _double_vowel(w: str, rng: random.Random) -> str:
    idx = [i for i, ch in enumerate(w) if ch in VOWELS]
    if not idx:
        return w
    i = rng.choice(idx)
    return w[: i + 1] + w[i] + w[i + 1 :]


def _toggle_trailing_vowel(w: str, rng: random.Random) -> str:
    if w[-1] in VOWELS and len(w) > 3:
        return w[:-1]
    return w + rng.choice("aeo")


def _misc_swap(w: str, rng: random.Random) -> str:
    pairs = [("c", "k"), ("k", "c"), ("ph", "f"), ("f", "ph"), ("i", "y"), ("y", "i"), ("qu", "kw"), ("v", "w")]
    rng.shuffle(pairs)
    for a, b in pairs:
        if a in w:
            return w.replace(a, b, 1)
    return w


VARIANT_OPS = [_swap_sibilant, _double_vowel, _toggle_trailing_vowel, _misc_swap]


def phonetic_variants(base: str, rng: random.Random, k: int) -> list[str]:
    """Generate k distinct sound-alike variants of base."""
    seen = {base.lower()}
    out: list[str] = []
    attempts = 0
    while len(out) < k and attempts < 60:
        attempts += 1
        w = base.lower()
        for op in rng.sample(VARIANT_OPS, rng.choice([1, 1, 2])):
            w = op(w, rng)
        if w not in seen and len(w) >= 3:
            seen.add(w)
            out.append(w.capitalize())
    return out


def random_date(rng: random.Random, start=date(2015, 1, 1), end=date(2026, 10, 1)) -> date:
    return start + timedelta(days=rng.randint(0, (end - start).days))


def generate_marks(rng: random.Random, n: int = 5000) -> list[dict]:
    """Generate n mark records (no embeddings). Every 10th base mark spawns 3-5 sound-alikes."""
    owners = make_owners(rng)
    used: set[str] = set()
    records: list[dict] = []
    base_count = 0

    def add(text: str, nice_class: int, group: int | None):
        records.append(
            {
                "mark_text": text,
                "nice_class": nice_class,
                "goods_description": make_goods(rng, nice_class),
                "status": rng.choices(STATUSES, STATUS_WEIGHTS)[0],
                "owner_name": rng.choice(owners),
                "filing_date": random_date(rng),
                "collision_group": group,
            }
        )
        used.add(text.lower())

    while len(records) < n:
        word = coined_word(rng)
        if word.lower() in used:
            continue
        cls = rng.choices(range(1, 46), CLASS_WEIGHTS)[0]
        group = base_count if base_count % 10 == 0 else None
        add(word, cls, group)
        if group is not None:
            for v in phonetic_variants(word, rng, rng.randint(3, 5)):
                if len(records) >= n or v.lower() in used:
                    continue
                # Half of the variants land in the same class to create real conflicts.
                vcls = cls if rng.random() < 0.5 else rng.choices(range(1, 46), CLASS_WEIGHTS)[0]
                add(v, vcls, group)
        base_count += 1

    return records[:n]
