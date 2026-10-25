"""Nice Classification reference entries: 45 class headings + 24 sub-descriptions = 69."""

NICE_HEADINGS: dict[int, tuple[str, str]] = {
    1: ("Chemicals", "Chemicals for use in industry, science and photography, as well as in agriculture, horticulture and forestry; unprocessed artificial and plastic resins; fertilisers; fire extinguishing compositions; adhesives for industry"),
    2: ("Paints", "Paints, varnishes, lacquers; preservatives against rust and deterioration of wood; colorants, dyes; inks for printing, marking and engraving; raw natural resins"),
    3: ("Cosmetics and cleaning preparations", "Non-medicated cosmetics and toiletry preparations; non-medicated dentifrices; perfumery, essential oils; bleaching preparations and other substances for laundry use; cleaning, polishing and abrasive preparations"),
    4: ("Lubricants and fuels", "Industrial oils and greases, wax; lubricants; dust absorbing, wetting and binding compositions; fuels and illuminants; candles and wicks for lighting"),
    5: ("Pharmaceuticals", "Pharmaceuticals, medical and veterinary preparations; sanitary preparations for medical purposes; dietetic food and substances; dietary supplements; plasters, materials for dressings; disinfectants"),
    6: ("Metal goods", "Common metals and their alloys, ores; metal materials for building and construction; transportable buildings of metal; non-electric cables and wires of common metal; small items of metal hardware; safes"),
    7: ("Machinery", "Machines, machine tools, power-operated tools; motors and engines, except for land vehicles; machine coupling and transmission components; agricultural implements; incubators for eggs; automatic vending machines"),
    8: ("Hand tools", "Hand tools and implements, hand-operated; cutlery; side arms, except firearms; razors"),
    9: ("Computers and scientific devices", "Scientific, research, navigation, surveying, photographic, audiovisual and measuring apparatus; recorded and downloadable media, computer software; computers and computer peripheral devices; mobile applications"),
    10: ("Medical apparatus", "Surgical, medical, dental and veterinary apparatus and instruments; artificial limbs, eyes and teeth; orthopaedic articles; suture materials; therapeutic and assistive devices"),
    11: ("Environmental control apparatus", "Apparatus and installations for lighting, heating, cooling, steam generating, cooking, drying, ventilating, water supply and sanitary purposes"),
    12: ("Vehicles", "Vehicles; apparatus for locomotion by land, air or water; bicycles, electric scooters, automobile parts"),
    13: ("Firearms and fireworks", "Firearms; ammunition and projectiles; explosives; fireworks"),
    14: ("Jewelry", "Precious metals and their alloys; jewellery, precious and semi-precious stones; horological and chronometric instruments, watches"),
    15: ("Musical instruments", "Musical instruments; music stands and stands for musical instruments; conductors' batons"),
    16: ("Paper goods and printed matter", "Paper and cardboard; printed matter; bookbinding material; photographs; stationery and office requisites; artists' materials; plastic sheets for wrapping and packaging"),
    17: ("Rubber goods", "Unprocessed and semi-processed rubber, gutta-percha, asbestos, mica; plastics and resins in extruded form; packing, stopping and insulating materials; flexible pipes, not of metal"),
    18: ("Leather goods", "Leather and imitations of leather; animal skins and hides; luggage and carrying bags; umbrellas and parasols; walking sticks; whips, harness and saddlery; collars, leashes and clothing for animals"),
    19: ("Non-metallic building materials", "Materials, not of metal, for building and construction; rigid pipes, not of metal; asphalt, pitch, tar and bitumen; transportable buildings, not of metal; monuments, not of metal"),
    20: ("Furniture", "Furniture, mirrors, picture frames; containers, not of metal, for storage or transport; unworked or semi-worked bone, horn, whalebone or mother-of-pearl; shells; meerschaum; yellow amber"),
    21: ("Housewares and glass", "Household or kitchen utensils and containers; cookware and tableware; combs and sponges; brushes; cleaning articles; unworked or semi-worked glass; glassware, porcelain and earthenware"),
    22: ("Ropes and fibres", "Ropes and string; nets; tents and tarpaulins; awnings of textile or synthetic materials; sails; sacks for the transport and storage of materials in bulk; padding and stuffing materials; raw fibrous textile materials"),
    23: ("Yarns and threads", "Yarns and threads for textile use"),
    24: ("Fabrics", "Textiles and substitutes for textiles; household linen; curtains of textile or plastic"),
    25: ("Clothing", "Clothing, footwear, headwear"),
    26: ("Fancy goods", "Lace, braid and embroidery, and haberdashery ribbons and bows; buttons, hooks and eyes, pins and needles; artificial flowers; hair decorations; false hair"),
    27: ("Floor coverings", "Carpets, rugs, mats and matting, linoleum and other materials for covering existing floors; wall hangings, not of textile"),
    28: ("Toys and sporting goods", "Games, toys and playthings; video game apparatus; gymnastic and sporting articles; decorations for Christmas trees"),
    29: ("Meats and processed foods", "Meat, fish, poultry and game; meat extracts; preserved, frozen, dried and cooked fruits and vegetables; jellies, jams, compotes; eggs; milk, cheese, butter, yogurt and other milk products; oils and fats for food"),
    30: ("Staple foods", "Coffee, tea, cocoa and substitutes therefor; rice, pasta and noodles; flour and preparations made from cereals; bread, pastries and confectionery; chocolate; ice cream, sorbets; sugar, honey; salt, spices, sauces and condiments"),
    31: ("Natural agricultural products", "Raw and unprocessed agricultural, aquacultural, horticultural and forestry products; raw and unprocessed grains and seeds; fresh fruits and vegetables, fresh herbs; natural plants and flowers; foodstuffs and beverages for animals; malt"),
    32: ("Light beverages", "Beers; non-alcoholic beverages; mineral and aerated waters; fruit beverages and fruit juices; syrups and other non-alcoholic preparations for making beverages"),
    33: ("Wines and spirits", "Alcoholic beverages, except beers; alcoholic preparations for making beverages; wine, spirits, liqueurs"),
    34: ("Smokers' articles", "Tobacco and tobacco substitutes; cigarettes and cigars; electronic cigarettes and oral vaporizers for smokers; smokers' articles; matches"),
    35: ("Advertising and business services", "Advertising; business management, organisation and administration; office functions; marketing services; retail store services; online marketplace services"),
    36: ("Insurance and financial services", "Financial, monetary and banking services; insurance services; real estate affairs; payment processing; investment services"),
    37: ("Construction and repair services", "Construction services; installation and repair services; mining extraction, oil and gas drilling"),
    38: ("Telecommunications", "Telecommunications services; transmission of data, messages and video; providing online forums and chat rooms; streaming of data"),
    39: ("Transportation and storage", "Transport; packaging and storage of goods; travel arrangement; delivery services; logistics"),
    40: ("Treatment of materials", "Treatment of materials; recycling of waste and trash; air purification and treatment of water; printing services; food and drink preservation; custom manufacturing"),
    41: ("Education and entertainment", "Education; providing of training; entertainment; sporting and cultural activities; online courses; publishing of electronic books; organising events and conferences"),
    42: ("Computer and scientific services", "Scientific and technological services and research and design relating thereto; industrial analysis, industrial research and industrial design services; design and development of computer hardware and software; software as a service; cloud computing"),
    43: ("Hotels and restaurants", "Services for providing food and drink; restaurant, cafe and catering services; temporary accommodation; hotel services"),
    44: ("Medical and beauty services", "Medical services; veterinary services; hygienic and beauty care for human beings or animals; agriculture, aquaculture, horticulture and forestry services"),
    45: ("Personal and legal services", "Legal services; security services for the physical protection of tangible property and individuals; dating services, online social networking services; funerary services; babysitting"),
}

# 24 sub-descriptions: 4 each for the six high-frequency classes.
NICE_SUBDESCRIPTIONS: list[tuple[int, str]] = [
    (9, "Downloadable mobile application software for smartphones and tablets"),
    (9, "Computer software for data analytics, machine learning and business intelligence"),
    (9, "Downloadable electronic publications, podcasts and digital media files"),
    (9, "Wearable electronic devices, smartwatches, headphones and computer peripherals"),
    (25, "Shirts, t-shirts, jackets, trousers, dresses and other apparel"),
    (25, "Footwear, namely shoes, sneakers, boots and sandals"),
    (25, "Headwear, namely hats, caps and beanies"),
    (25, "Athletic and sportswear clothing, activewear and yoga pants"),
    (35, "Online retail store services featuring consumer goods"),
    (35, "Marketing, digital advertising and social media promotion services for others"),
    (35, "Business consulting, management and human resources services"),
    (35, "Accounting, bookkeeping and office administration services"),
    (41, "Online educational courses, tutoring and training seminars"),
    (41, "Entertainment services, live music concerts and theatre productions"),
    (41, "Organising sporting events, fitness classes and competitions"),
    (41, "Publishing of books, magazines and online non-downloadable publications"),
    (42, "Software as a service (SaaS) featuring software for project management and collaboration"),
    (42, "Cloud computing, data hosting and platform as a service (PaaS)"),
    (42, "Design and development of computer software and websites"),
    (42, "Cybersecurity consulting, data encryption and IT security services"),
    (43, "Restaurant, cafe, bar and coffee shop services"),
    (43, "Catering services and food delivery from restaurants"),
    (43, "Hotel, hostel and temporary accommodation services"),
    (43, "Take-out restaurant services, fast food and food trucks"),
]


def nice_reference_entries() -> list[dict]:
    """Return the 69 reference rows: {class_number, class_name, description}."""
    rows = [
        {"class_number": n, "class_name": name, "description": f"Class {n}: {name}. {desc}"}
        for n, (name, desc) in NICE_HEADINGS.items()
    ]
    rows += [
        {"class_number": n, "class_name": NICE_HEADINGS[n][0], "description": desc}
        for n, desc in NICE_SUBDESCRIPTIONS
    ]
    return rows
