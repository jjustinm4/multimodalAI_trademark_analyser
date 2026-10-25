"""Hardcoded prohibited terms for the absolute grounds screener.

Each entry is (term, category). Categories drive the flag text in the UI.
"""

PROHIBITED_TERMS: list[tuple[str, str]] = [
    # National / international emblems and protected names
    ("United Nations", "international emblem"),
    ("Red Cross", "international emblem"),
    ("Red Crescent", "international emblem"),
    ("Red Crystal", "international emblem"),
    ("Olympic", "protected event name"),
    ("Olympiad", "protected event name"),
    ("Paralympic", "protected event name"),
    ("UNESCO", "international emblem"),
    ("UNICEF", "international emblem"),
    ("NATO", "international emblem"),
    ("Interpol", "international emblem"),
    ("World Health Organization", "international emblem"),
    ("Geneva Cross", "international emblem"),
    ("Stars and Stripes", "national emblem"),
    ("Great Seal", "national emblem"),
    ("Presidential Seal", "national emblem"),
    ("Smokey Bear", "statutorily protected"),
    ("Woodsy Owl", "statutorily protected"),
    # Geographic indications
    ("Champagne", "geographic indication"),
    ("Darjeeling", "geographic indication"),
    ("Scotch", "geographic indication"),
    ("Cognac", "geographic indication"),
    ("Parmigiano Reggiano", "geographic indication"),
    ("Roquefort", "geographic indication"),
    ("Tequila", "geographic indication"),
    ("Bordeaux", "geographic indication"),
    ("Prosecco", "geographic indication"),
    ("Feta", "geographic indication"),
    ("Gorgonzola", "geographic indication"),
    ("Kobe Beef", "geographic indication"),
    ("Basmati", "geographic indication"),
    ("Rioja", "geographic indication"),
    # Scandalous / disparaging (mild placeholders for the PoC)
    ("Scam", "scandalous or disparaging"),
    ("Damn", "scandalous or disparaging"),
    ("Hell Spawn", "scandalous or disparaging"),
    ("Bastard", "scandalous or disparaging"),
    ("Crapware", "scandalous or disparaging"),
    ("Junkie", "scandalous or disparaging"),
    ("Narco", "scandalous or disparaging"),
    ("Heroin", "scandalous or disparaging"),
    # Government agency names
    ("FBI", "government agency"),
    ("CIA", "government agency"),
    ("NASA", "government agency"),
    ("USPTO", "government agency"),
    ("Internal Revenue Service", "government agency"),
    ("Federal Reserve", "government agency"),
    ("Secret Service", "government agency"),
    ("Department of Defense", "government agency"),
    ("Homeland Security", "government agency"),
    ("Social Security", "government agency"),
    ("Coast Guard", "government agency"),
    ("Environmental Protection Agency", "government agency"),
]

TERM_CATEGORY = {t: c for t, c in PROHIBITED_TERMS}
TERMS = [t for t, _ in PROHIBITED_TERMS]
