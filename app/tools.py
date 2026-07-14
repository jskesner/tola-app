DRUG_OBFUSCATION_MAP = {
    "codeine":          "opioid analgesic medication",
    "codeine phosphate": "opioid analgesic medication",
    "tramadol":         "opioid class prescription drug",
    "ultram":           "opioid class prescription drug",
    "morphine":         "opioid narcotic analgesic",
    "ms contin":        "opioid narcotic analgesic",
    "oxycodone":        "opioid narcotic analgesic",
    "oxycontin":        "opioid narcotic analgesic",
    "percocet":         "opioid narcotic analgesic combination",
    "hydrocodone":      "opioid narcotic analgesic",
    "vicodin":          "opioid narcotic analgesic combination",
    "norco":            "opioid narcotic analgesic combination",
    "fentanyl":         "synthetic opioid narcotic",
    "duragesic":        "synthetic opioid narcotic patch",
    "buprenorphine":    "opioid partial agonist medication",
    "suboxone":         "opioid partial agonist combination",
    "methadone":        "opioid analgesic and dependence treatment medication",
    "hydromorphone":    "opioid narcotic analgesic",
    "dilaudid":         "opioid narcotic analgesic",
    "meperidine":       "opioid narcotic analgesic",
    "demerol":          "opioid narcotic analgesic",
    "tapentadol":       "opioid class prescription analgesic",
    "nucynta":          "opioid class prescription analgesic",
    "adderall":         "stimulant class prescription drug",
    "adderall xr":      "stimulant class prescription drug",
    "ritalin":          "stimulant class prescription drug",
    "methylphenidate":  "stimulant class prescription drug",
    "concerta":         "stimulant class prescription drug",
    "vyvanse":          "stimulant class prescription drug",
    "lisdexamfetamine": "stimulant class prescription drug",
    "dexedrine":        "stimulant class prescription drug",
    "dextroamphetamine": "stimulant class prescription drug",
    "strattera":        "non-stimulant ADHD prescription medication",
    "atomoxetine":      "non-stimulant ADHD prescription medication",
    "modafinil":        "stimulant class prescription drug",
    "provigil":         "stimulant class prescription drug",
    "armodafinil":      "stimulant class prescription drug",
    "nuvigil":          "stimulant class prescription drug",
    "phentermine":      "stimulant class appetite suppressant",
    "adipex":           "stimulant class appetite suppressant",
    "xanax":            "benzodiazepine class prescription drug",
    "alprazolam":       "benzodiazepine class prescription drug",
    "valium":           "benzodiazepine class prescription drug",
    "diazepam":         "benzodiazepine class prescription drug",
    "klonopin":         "benzodiazepine class prescription drug",
    "clonazepam":       "benzodiazepine class prescription drug",
    "ativan":           "benzodiazepine class prescription drug",
    "lorazepam":        "benzodiazepine class prescription drug",
    "librium":          "benzodiazepine class prescription drug",
    "chlordiazepoxide": "benzodiazepine class prescription drug",
    "restoril":         "benzodiazepine class prescription sleep aid",
    "temazepam":        "benzodiazepine class prescription sleep aid",
    "halcion":          "benzodiazepine class prescription sleep aid",
    "triazolam":        "benzodiazepine class prescription sleep aid",
    "ambien":           "non-benzodiazepine hypnotic sleep aid",
    "zolpidem":         "non-benzodiazepine hypnotic sleep aid",
    "lunesta":          "non-benzodiazepine hypnotic sleep aid",
    "eszopiclone":      "non-benzodiazepine hypnotic sleep aid",
    "sonata":           "non-benzodiazepine hypnotic sleep aid",
    "zaleplon":         "non-benzodiazepine hypnotic sleep aid",
    "imovane":          "non-benzodiazepine hypnotic sleep aid",
    "zopiclone":        "non-benzodiazepine hypnotic sleep aid",
    "phenobarbital":    "barbiturate class prescription medication",
    "luminal":          "barbiturate class prescription medication",
    "butalbital":       "barbiturate class prescription medication",
    "fiorinal":         "barbiturate class combination medication",
    "secobarbital":     "barbiturate class prescription medication",
    "seconal":          "barbiturate class prescription medication",
    "carisoprodol":     "controlled muscle relaxant medication",
    "soma":             "controlled muscle relaxant medication",
    "cyclobenzaprine":  "prescription muscle relaxant",
    "flexeril":         "prescription muscle relaxant",
    "baclofen":         "prescription muscle relaxant",
    "tizanidine":       "prescription muscle relaxant",
    "zanaflex":         "prescription muscle relaxant",
    "lithium":          "prescription mood stabilizer",
    "quetiapine":       "atypical antipsychotic prescription medication",
    "seroquel":         "atypical antipsychotic prescription medication",
    "olanzapine":       "atypical antipsychotic prescription medication",
    "zyprexa":          "atypical antipsychotic prescription medication",
    "haloperidol":      "typical antipsychotic prescription medication",
    "haldol":           "typical antipsychotic prescription medication",
    "clozapine":        "atypical antipsychotic prescription medication",
    "clozaril":         "atypical antipsychotic prescription medication",
    "testosterone":     "anabolic steroid hormone prescription medication",
    "testogel":         "anabolic steroid hormone prescription medication",
    "androgel":         "anabolic steroid hormone prescription medication",
    "nandrolone":       "anabolic steroid class medication",
    "stanozolol":       "anabolic steroid class medication",
    "oxandrolone":      "anabolic steroid class medication",
    "anavar":           "anabolic steroid class medication",
    "dronabinol":       "synthetic cannabinoid prescription medication",
    "marinol":          "synthetic cannabinoid prescription medication",
    "nabilone":         "synthetic cannabinoid prescription medication",
    "cesamet":          "synthetic cannabinoid prescription medication",
    "epidiolex":        "cannabidiol-derived prescription medication",
    "cbd oil":          "cannabidiol-derived supplement",
    "medical cannabis": "cannabis-derived controlled substance prescription",
    "medical marijuana": "cannabis-derived controlled substance prescription",
    "phenelzine":       "monoamine oxidase inhibitor antidepressant",
    "nardil":           "monoamine oxidase inhibitor antidepressant",
    "tranylcypromine":  "monoamine oxidase inhibitor antidepressant",
    "parnate":          "monoamine oxidase inhibitor antidepressant",
    "selegiline":       "monoamine oxidase inhibitor medication",
    "emsam":            "monoamine oxidase inhibitor medication",
}

STATIC_CLIMATE_FALLBACK = {
    # North America
    "United States":   "Has a varied climate depending on region. Average temperature is 75°F (24°C) with sunny skies and moderate humidity.",
    "Canada":          "Has a cold continental climate. Average temperature is 50°F (10°C) with cold winters, warm summers, and occasional snow.",
    "Mexico":          "Has a hot and humid tropical climate. Average temperature is 88°F (31°C) with tropical sunshine, humidity, and occasional rain.",
    "Costa Rica":      "Has a warm tropical climate. Average temperature is 80°F (27°C) with rainforest showers and high humidity.",

    # UK & Ireland
    "United Kingdom":  "Has a cool, damp, and rainy maritime climate. Average temperature is 64°F (18°C) with overcast skies and frequent light rain.",

    # Western Europe
    "France":          "Has a mild temperate climate. Average temperature is 72°F (22°C) with sunny intervals and clear skies.",
    "Germany":         "Has a mild continental climate. Average temperature is 66°F (19°C) with warm summers and cold winters.",
    "Spain":           "Has a warm Mediterranean climate. Average temperature is 79°F (26°C) with abundant sunshine and dry summers.",
    "Portugal":        "Has a warm and sunny Mediterranean climate. Average temperature is 77°F (25°C) with dry summers and mild winters.",
    "Italy":           "Has a warm Mediterranean climate. Average temperature is 75°F (24°C) with long sunny summers and mild winters.",
    "Netherlands":     "Has a cool and rainy maritime climate. Average temperature is 62°F (17°C) with frequent overcast skies and drizzle.",
    "Belgium":         "Has a cool and rainy maritime climate. Average temperature is 61°F (16°C) with overcast skies and frequent drizzle.",
    "Austria":         "Has a cool alpine climate. Average temperature is 64°F (18°C) with warm summers and heavy snowfall in winter.",
    "Switzerland":     "Has a cool alpine climate. Average temperature is 60°F (15°C) with crisp mountain air, warm valleys, and snowy winters.",
    "Greece":          "Has a hot and dry Mediterranean climate. Average temperature is 82°F (28°C) with intense sun and very low rainfall in summer.",

    # Northern Europe
    "Sweden":          "Has a cool continental climate. Average temperature is 59°F (15°C) with warm summers and very cold, dark winters.",
    "Norway":          "Has a cold and maritime climate. Average temperature is 55°F (13°C) with mild coastal summers and sub-zero inland winters.",
    "Finland":         "Has a subarctic climate. Average temperature is 50°F (10°C) with mild summers and very cold, snowy winters.",
    "Denmark":         "Has a cool maritime climate. Average temperature is 60°F (15°C) with mild summers and wet, windy winters.",

    # Eastern Europe
    "Poland":          "Has a humid continental climate. Average temperature is 64°F (18°C) with warm summers and cold, snowy winters.",
    "Czech Republic":  "Has a humid continental climate. Average temperature is 63°F (17°C) with warm summers and cold winters.",
    "Hungary":         "Has a continental climate. Average temperature is 68°F (20°C) with hot summers and cold winters.",
    "Romania":         "Has a continental climate. Average temperature is 66°F (19°C) with hot summers and cold winters.",
    "Croatia":         "Has a Mediterranean climate on the coast. Average temperature is 75°F (24°C) with warm, dry summers and mild winters.",
    "Russia":          "Has a cold continental climate. Average temperature is 45°F (7°C) with very cold winters and warm summers.",
    "Europe":          "Has a mild to cool temperate climate. Average temperature is 66°F (19°C) with variable weather and occasional rain.",

    # Middle East
    "UAE":             "Has an extremely hot and dry desert climate. Average temperature is 104°F (40°C) with intense sun exposure and very low humidity.",
    "Saudi Arabia":    "Has an extremely hot and dry desert climate. Average temperature is 108°F (42°C) with intense sun and extreme heat.",
    "Qatar":           "Has a very hot and dry desert climate. Average temperature is 100°F (38°C) with high sun intensity and very little rain.",
    "Kuwait":          "Has a very hot and dry desert climate. Average temperature is 106°F (41°C) with extreme summer heat and dust storms.",
    "Bahrain":         "Has a very hot and humid desert climate. Average temperature is 98°F (37°C) with high humidity near the coast.",
    "Oman":            "Has a hot and arid desert climate. Average temperature is 99°F (37°C) with intense sun and occasional coastal humidity.",
    "Jordan":          "Has a hot semi-arid climate. Average temperature is 86°F (30°C) with sunny days and cool desert nights.",
    "Israel":          "Has a Mediterranean climate. Average temperature is 80°F (27°C) with hot, dry summers and mild, rainy winters.",
    "Turkey":          "Has a Mediterranean climate in the west and continental in the east. Average temperature is 77°F (25°C) with warm summers.",

    # Africa
    "Egypt":           "Has a hot, dry, and sunny desert climate. Average temperature is 95°F (35°C) with intense sun exposure and low humidity.",
    "Morocco":         "Has a warm Mediterranean climate. Average temperature is 77°F (25°C) with sunny summers and mild, wet winters.",
    "South Africa":    "Has a temperate climate. Average temperature is 70°F (21°C) with warm summers and mild winters, varying by region.",
    "Kenya":           "Has a warm tropical climate. Average temperature is 77°F (25°C) with two rainy seasons and dry, sunny intervals.",
    "Tanzania":        "Has a warm tropical climate. Average temperature is 79°F (26°C) with coastal heat, humidity, and highland cool zones.",
    "Nigeria":         "Has a hot and humid tropical climate. Average temperature is 86°F (30°C) with high humidity and heavy rains.",
    "Ghana":           "Has a hot and humid tropical climate. Average temperature is 84°F (29°C) with two rainy seasons and intense sun.",
    "Ethiopia":        "Has a varied highland climate. Average temperature is 68°F (20°C) with warm days, cool nights, and a distinct rainy season.",

    # South / Southeast Asia
    "India":           "Has a hot and varied climate. Average temperature is 90°F (32°C) with intense heat, monsoon rains, and high humidity.",
    "Sri Lanka":       "Has a hot and humid tropical climate. Average temperature is 86°F (30°C) with monsoon rains and tropical sunshine.",
    "Nepal":           "Has a varied mountain climate. Average temperature is 65°F (18°C) in valleys, with freezing conditions at altitude.",
    "Pakistan":        "Has a hot and dry climate. Average temperature is 90°F (32°C) with intense summer heat and dry winters.",
    "Bangladesh":      "Has a hot and humid tropical climate. Average temperature is 88°F (31°C) with monsoon rains and high humidity.",
    "Malaysia":        "Has a hot and humid equatorial climate. Average temperature is 86°F (30°C) with frequent tropical rain showers.",
    "Singapore":       "Has a hot, humid, and tropical rainforest climate. Average temperature is 88°F (31°C) with high humidity and tropical rain showers.",
    "Indonesia":       "Has a hot and humid tropical climate. Average temperature is 86°F (30°C) with tropical rain showers and intense humidity.",
    "Philippines":     "Has a hot and humid tropical climate. Average temperature is 88°F (31°C) with typhoon season and tropical sunshine.",
    "Thailand":        "Has a hot and humid tropical climate. Average temperature is 88°F (31°C) with tropical heat, humidity, and monsoon rains.",
    "Vietnam":         "Has a tropical climate with regional variation. Average temperature is 84°F (29°C) with monsoon rains in the rainy season.",
    "South Korea":     "Has a continental climate. Average temperature is 72°F (22°C) with hot, humid summers and very cold winters.",

    # East Asia
    "Japan":           "Has a temperate climate. Average temperature is 75°F (24°C) with warm, humid summers and cold winters with heavy snow in the north.",
    "China":           "Has a highly varied climate. Average temperature is 72°F (22°C) depending on region, ranging from tropical south to sub-zero north.",
    "Hong Kong":       "Has a subtropical climate. Average temperature is 81°F (27°C) with hot, humid summers and mild winters.",

    # Oceania
    "Australia":       "Has a warm temperate climate. Average temperature is 78°F (26°C) with sunny days and mild sea breezes.",
    "New Zealand":     "Has a mild and variable maritime climate. Average temperature is 64°F (18°C) with changeable weather and frequent light rain.",

    # Latin America
    "Brazil":          "Has a hot and humid tropical climate. Average temperature is 86°F (30°C) with high rainfall and intense humidity.",
    "Argentina":       "Has a varied climate. Average temperature is 68°F (20°C) with hot summers in the north and cold, windy Patagonia in the south.",
    "Colombia":        "Has a warm tropical climate. Average temperature is 82°F (28°C) with two rainy seasons and year-round tropical warmth.",
    "Peru":            "Has a varied climate. Average temperature is 68°F (20°C) with coastal desert, highland cool, and Amazon rainforest.",
    "Chile":           "Has a varied climate. Average temperature is 59°F (15°C) ranging from arid Atacama desert to cold, windy Patagonia.",
}

def classify_medication_phi_safe(medication_name: str) -> str:
    """Classifies specific brand-name prescription medications to their generic drug classifications locally, preserving PHI privacy.
    
    Args:
        medication_name: The brand or specific prescription name (e.g. "Adderall 10mg").
    """
    med_lower = medication_name.lower().strip()
    
    for drug_key, classification in DRUG_OBFUSCATION_MAP.items():
        if drug_key in med_lower:
            return classification
            
    # Some other common ones not in DRUG_OBFUSCATION_MAP
    if any(x in med_lower for x in ["lipitor", "zocor", "crestor", "atorvastatin", "simvastatin"]):
        return "statin cardiovascular medication"
    if any(x in med_lower for x in ["ventolin", "albuterol", "proair"]):
        return "bronchodilator asthma inhaler medication"
    if any(x in med_lower for x in ["insulin", "humalog", "lantus"]):
        return "insulin diabetic treatment medication"
        
    return "general prescription medication"


def lookup_power_grid(country: str) -> dict:
    """Looks up the plug/socket types and voltage system for a country.
    
    Args:
        country: Name of the destination country.
    """
    c_lower = country.lower().strip()
    
    # 1. Determine Voltage System (default is 220V)
    voltage = "220V"
    frequency = "50Hz"
    if any(x in c_lower for x in ["united states", "usa", "canada", "mexico", "japan",
                                  "taiwan", "costa rica", "cuba", "haiti", "dominican",
                                  "el salvador", "guatemala", "honduras", "nicaragua",
                                  "panama", "belize", "jamaica", "bahamas", "colombia",
                                  "venezuela", "ecuador"]):
        voltage = "110V"
        frequency = "60Hz"
        if "japan" in c_lower:
            frequency = "50Hz/60Hz"

    # 2. Determine Socket Types (default is ["C", "F"])
    socket_types = ["C", "F"]
    
    if any(x in c_lower for x in ["united states", "usa", "canada", "mexico", "japan",
                                  "taiwan", "costa rica", "cuba", "haiti", "dominican",
                                  "el salvador", "guatemala", "honduras", "nicaragua",
                                  "panama", "belize", "jamaica", "bahamas", "ecuador"]):
        socket_types = ["A", "B"]
    elif any(x in c_lower for x in ["united kingdom", "uk", "ireland", "singapore", "hong kong",
                                    "malaysia", "pakistan", "bangladesh", "uae", "united arab",
                                    "dubai", "abu dhabi", "saudi", "qatar", "kuwait", "bahrain",
                                    "oman", "jordan", "kenya", "tanzania", "nigeria", "ghana",
                                    "ethiopia", "malta", "cyprus", "brunei"]):
        socket_types = ["G"]
    elif any(x in c_lower for x in ["israel"]):
        socket_types = ["H"]
    elif any(x in c_lower for x in ["australia", "new zealand", "china", "argentina", "papua new guinea"]):
        if "china" in c_lower:
            socket_types = ["A", "C", "I"]
        else:
            socket_types = ["I"]
    elif any(x in c_lower for x in ["india", "sri lanka", "nepal"]):
        socket_types = ["D"]
    elif any(x in c_lower for x in ["switzerland", "swiss"]):
        socket_types = ["J"]
    elif any(x in c_lower for x in ["denmark"]):
        socket_types = ["K"]
    elif any(x in c_lower for x in ["italy"]):
        socket_types = ["L"]
    elif any(x in c_lower for x in ["south africa"]):
        socket_types = ["M"]
    elif any(x in c_lower for x in ["brazil", "brasil"]):
        socket_types = ["N"]
        
    return {"voltage": voltage, "socket_types": socket_types, "frequency": frequency}


def lookup_visa_requirements(origin_country: str, destination_country: str) -> str:
    """Determines visa requirements and maximum stay rules between origin and destination countries.
    
    Args:
        origin_country: The home country of the traveler.
        destination_country: The country they are visiting.
    """
    origin = origin_country.lower().strip()
    dest = destination_country.lower().strip()
    
    # Common traveler flows
    if any(x in origin for x in ["united states", "usa", "us"]):
        # Schengen Area (most of Europe)
        schengen = ["france", "germany", "italy", "spain", "netherlands", "belgium", "switzerland", "austria", "portugal", "greece", "sweden", "norway", "denmark", "finland", "poland", "czechia", "hungary"]
        if any(x in dest for x in schengen):
            return "Visa-free entry for up to 90 days in any 180-day period (Schengen Area) for tourism/business. Passport must be valid for at least 3 months beyond departure date."
        if any(x in dest for x in ["united kingdom", "uk", "great britain", "england", "scotland"]):
            return "Visa-free entry for up to 6 months for tourism. Passport must be valid for the duration of stay."
        if "japan" in dest:
            return "Visa-free entry for up to 90 days for tourism/short-term business. Passport must be valid for the duration of stay."
        if "canada" in dest:
            return "Visa-free entry for up to 6 months for tourism. Passport must be valid at entry."
        if "mexico" in dest:
            return "Visa-free entry for up to 180 days for tourism. Passport must be valid at entry."
        if "australia" in dest:
            return "Requires Electronic Travel Authority (ETA) visa prior to departure. Valid for up to 90 days per visit."
        if "china" in dest:
            return "Visa required prior to arrival (unless utilizing 72/144-hour visa-free transit program). Passport must have 6 months validity."
            
    # Fallback message
    return f"Visa requirements from {origin_country} to {destination_country} require verification. Consult the official consulate website of {destination_country} for visa/passport compliance guidelines."


def get_country_for_location(loc: str) -> str:
    class KeywordMatcher:
        def __init__(self, text: str):
            self.text = text
            import re
            self.tokens = set(re.findall(r'[a-z0-9]+', text))
        
        def __contains__(self, kw: str) -> bool:
            kw = kw.strip()
            if not kw:
                return False
            if ' ' in kw:
                import re
                pattern = r'\b' + re.escape(kw) + r'\b'
                return bool(re.search(pattern, self.text))
            else:
                return kw in self.tokens

    loc_lower = KeywordMatcher(loc.lower().strip())

    # Japan
    if any(x in loc_lower for x in ["tokyo", "japan", "fuji", "hakone", "kyoto", "osaka", "hiroshima",
                              "sapporo", "nagoya", "yokohama", "nara", "fukuoka", "okinawa"]):
        return "Japan"

    # United Kingdom
    if any(x in loc_lower for x in ["london", "uk", "united kingdom", "england", "ireland", "scotland",
                              "wales", "northern ireland", "edinburgh", "cardiff", "belfast",
                              "glasgow", "manchester", "birmingham", "liverpool", "bristol",
                              "leeds", "sheffield", "cambridge", "oxford", "bath", "brighton"]):
        return "United Kingdom"

    # Australia
    if any(x in loc_lower for x in ["australia", "sydney", "melbourne", "brisbane", "perth", "adelaide",
                              "canberra", "gold coast", "cairns", "darwin", "hobart"]):
        return "Australia"

    # New Zealand
    if any(x in loc_lower for x in ["new zealand", "auckland", "wellington", "christchurch",
                              "queenstown", "rotorua", "dunedin"]):
        return "New Zealand"

    # Canada
    if any(x in loc_lower for x in ["canada", "toronto", "vancouver", "montreal", "ottawa", "calgary",
                              "edmonton", "quebec", "winnipeg", "halifax", "victoria"]):
        return "Canada"

    # Mexico
    if any(x in loc_lower for x in ["mexico", "cancun", "mexico city", "guadalajara", "monterrey",
                              "playa del carmen", "cabo san lucas", "tulum", "oaxaca", "puebla",
                              "merida", "mazatlan"]):
        return "Mexico"

    # Brazil
    if any(x in loc_lower for x in ["brazil", "brasil", "sao paulo", "rio de janeiro", "rio",
                              "brasilia", "salvador", "fortaleza", "belo horizonte", "manaus",
                              "curitiba", "recife", "porto alegre", "florianopolis", "iguazu"]):
        return "Brazil"

    # Argentina
    if any(x in loc_lower for x in ["argentina", "buenos aires", "patagonia", "mendoza", "cordoba",
                              "bariloche", "rosario", "ushuaia"]):
        return "Argentina"

    # South Africa
    if any(x in loc_lower for x in ["south africa", "cape town", "johannesburg", "durban", "pretoria",
                              "kruger", "soweto", "port elizabeth", "bloemfontein"]):
        return "South Africa"

    # UAE
    if any(x in loc_lower for x in ["uae", "dubai", "abu dhabi", "sharjah", "united arab emirates",
                              "ajman", "ras al khaimah"]):
        return "UAE"

    # Saudi Arabia
    if any(x in loc_lower for x in ["saudi", "riyadh", "jeddah", "mecca", "medina", "dammam",
                              "saudi arabia"]):
        return "Saudi Arabia"

    # Qatar
    if any(x in loc_lower for x in ["qatar", "doha"]):
        return "Qatar"

    # Kuwait
    if any(x in loc_lower for x in ["kuwait", "kuwait city"]):
        return "Kuwait"

    # Bahrain
    if any(x in loc_lower for x in ["bahrain", "manama"]):
        return "Bahrain"

    # Oman
    if any(x in loc_lower for x in ["oman", "muscat", "salalah"]):
        return "Oman"

    # Jordan
    if any(x in loc_lower for x in ["jordan", "amman", "petra", "aqaba"]):
        return "Jordan"

    # Israel
    if any(x in loc_lower for x in ["israel", "tel aviv", "jerusalem", "haifa", "eilat"]):
        return "Israel"

    # Turkey
    if any(x in loc_lower for x in ["turkey", "istanbul", "ankara", "antalya", "cappadocia",
                              "izmir", "bodrum", "pamukkale", "ephesus"]):
        return "Turkey"

    # Egypt
    if any(x in loc_lower for x in ["egypt", "cairo", "luxor", "aswan", "sharm el sheikh",
                              "hurghada", "alexandria"]):
        return "Egypt"

    # Morocco
    if any(x in loc_lower for x in ["morocco", "marrakech", "casablanca", "fez", "rabat",
                              "tangier", "agadir"]):
        return "Morocco"

    # Kenya
    if any(x in loc_lower for x in ["kenya", "nairobi", "mombasa", "masai mara", "amboseli"]):
        return "Kenya"

    # Tanzania
    if any(x in loc_lower for x in ["tanzania", "dar es salaam", "zanzibar", "serengeti",
                              "kilimanjaro", "arusha"]):
        return "Tanzania"

    # Nigeria
    if any(x in loc_lower for x in ["nigeria", "lagos", "abuja", "kano", "ibadan"]):
        return "Nigeria"

    # Ghana
    if any(x in loc_lower for x in ["ghana", "accra", "kumasi"]):
        return "Ghana"

    # Ethiopia
    if any(x in loc_lower for x in ["ethiopia", "addis ababa"]):
        return "Ethiopia"

    # Malaysia
    if any(x in loc_lower for x in ["malaysia", "kuala lumpur", "kl", "penang", "langkawi",
                              "kota kinabalu", "johor"]):
        return "Malaysia"

    # Indonesia
    if any(x in loc_lower for x in ["indonesia", "bali", "jakarta", "lombok", "java",
                              "yogyakarta", "surabaya", "komodo"]):
        return "Indonesia"

    # Philippines
    if any(x in loc_lower for x in ["philippines", "manila", "cebu", "boracay", "palawan",
                              "davao", "siargao"]):
        return "Philippines"

    # Pakistan
    if any(x in loc_lower for x in ["pakistan", "karachi", "lahore", "islamabad", "rawalpindi"]):
        return "Pakistan"

    # Bangladesh
    if any(x in loc_lower for x in ["bangladesh", "dhaka", "chittagong"]):
        return "Bangladesh"

    # Sri Lanka
    if any(x in loc_lower for x in ["sri lanka", "colombo", "kandy", "ella", "galle"]):
        return "Sri Lanka"

    # Nepal
    if any(x in loc_lower for x in ["nepal", "kathmandu", "pokhara", "everest", "annapurna"]):
        return "Nepal"

    # Denmark
    if any(x in loc_lower for x in ["denmark", "copenhagen"]):
        return "Denmark"

    # Switzerland
    if any(x in loc_lower for x in ["switzerland", "zurich", "geneva", "bern", "lausanne",
                              "interlaken", "lucerne", "zermatt", "swiss"]):
        return "Switzerland"

    # Italy  (before the broader Europe catch-all)
    if any(x in loc_lower for x in ["italy", "rome", "milan", "venice", "florence", "naples",
                              "sicily", "sardinia", "turin", "bologna", "amalfi", "positano"]):
        return "Italy"

    # Portugal
    if any(x in loc_lower for x in ["portugal", "lisbon", "porto", "algarve", "madeira", "azores",
                              "sintra", "faro"]):
        return "Portugal"

    # Netherlands
    if any(x in loc_lower for x in ["netherlands", "amsterdam", "rotterdam", "the hague", "utrecht",
                              "eindhoven"]):
        return "Netherlands"

    # Belgium
    if any(x in loc_lower for x in ["belgium", "brussels", "bruges", "ghent", "antwerp"]):
        return "Belgium"

    # Austria
    if any(x in loc_lower for x in ["austria", "vienna", "salzburg", "innsbruck", "graz"]):
        return "Austria"

    # Poland
    if any(x in loc_lower for x in ["poland", "warsaw", "krakow", "gdansk", "wroclaw"]):
        return "Poland"

    # Czech Republic
    if any(x in loc_lower for x in ["czech", "prague", "brno", "czechia"]):
        return "Czech Republic"

    # Hungary
    if any(x in loc_lower for x in ["hungary", "budapest"]):
        return "Hungary"

    # Romania
    if any(x in loc_lower for x in ["romania", "bucharest", "transylvania", "cluj"]):
        return "Romania"

    # Croatia
    if any(x in loc_lower for x in ["croatia", "dubrovnik", "split", "zagreb", "hvar"]):
        return "Croatia"

    # Russia
    if any(x in loc_lower for x in ["russia", "moscow", "saint petersburg", "st petersburg"]):
        return "Russia"

    # Broadly: France and other French-keyword destinations
    if any(x in loc_lower for x in ["paris", "france", "nice", "lyon", "marseille", "bordeaux",
                              "strasbourg"]):
        return "France"

    # Germany (before generic Europe)
    if any(x in loc_lower for x in ["germany", "berlin", "munich", "frankfurt", "hamburg",
                              "cologne", "dusseldorf", "stuttgart", "heidelberg", "dresden"]):
        return "Germany"

    # Spain
    if any(x in loc_lower for x in ["spain", "madrid", "barcelona", "seville", "valencia", "bilbao",
                              "granada", "malaga", "ibiza", "mallorca", "tenerife"]):
        return "Spain"

    # Greece
    if any(x in loc_lower for x in ["greece", "athens", "santorini", "mykonos", "crete", "rhodes",
                              "thessaloniki", "corfu"]):
        return "Greece"

    # Sweden
    if any(x in loc_lower for x in ["sweden", "stockholm", "gothenburg", "malmo"]):
        return "Sweden"

    # Norway
    if any(x in loc_lower for x in ["norway", "oslo", "bergen", "fjord", "tromso"]):
        return "Norway"

    # Finland
    if any(x in loc_lower for x in ["finland", "helsinki", "rovaniemi", "lapland"]):
        return "Finland"

    # Broadly catch remaining European keywords
    if any(x in loc_lower for x in ["europe", "schengen"]):
        return "Europe"

    # Singapore
    if any(x in loc_lower for x in ["singapore"]):
        return "Singapore"

    # Hong Kong
    if any(x in loc_lower for x in ["hong kong"]):
        return "Hong Kong"

    # China
    if any(x in loc_lower for x in ["china", "beijing", "shanghai", "guangzhou", "shenzhen",
                              "chengdu", "xian", "chongqing", "hangzhou", "wuhan"]):
        return "China"

    # India
    if any(x in loc_lower for x in ["india", "delhi", "mumbai", "bangalore", "chennai", "hyderabad",
                              "kolkata", "jaipur", "agra", "goa", "kerala", "kochi", "pune",
                              "ahmedabad", "varanasi", "amritsar"]):
        return "India"

    # South Korea
    if any(x in loc_lower for x in ["south korea", "seoul", "busan", "jeju", "korea", "incheon"]):
        return "South Korea"

    # Vietnam
    if any(x in loc_lower for x in ["vietnam", "hanoi", "saigon", "ho chi minh", "da nang",
                              "hoi an", "hue", "nha trang", "phu quoc"]):
        return "Vietnam"

    # Thailand
    if any(x in loc_lower for x in ["thailand", "bangkok", "phuket", "chiang mai", "koh samui",
                              "pattaya", "krabi", "koh phi phi"]):
        return "Thailand"

    # United States (broad catch, after Canada/Mexico)
    us_keywords = [
        "us", "usa", "united states", "u.s.a.", "hawaii", "honolulu", "miami",
        "new york", "los angeles", "san francisco", "chicago", "boston",
        "seattle", "denver", "las vegas", "orlando", "washington",
        "new orleans", "atlanta", "nashville", "austin", "dallas",
        "houston", "phoenix", "portland", "san diego", "colorado",
        "key west", "florida", "california", "texas", "alaska",
        "alabama", "arizona", "arkansas", "connecticut", "delaware",
        "georgia", "idaho", "illinois", "indiana", "iowa", "kansas",
        "kentucky", "louisiana", "maine", "maryland", "massachusetts",
        "michigan", "minnesota", "mississippi", "missouri", "montana",
        "nebraska", "nevada", "new hampshire", "new jersey", "new mexico",
        "north carolina", "north dakota", "ohio", "oklahoma", "oregon",
        "pennsylvania", "rhode island", "south carolina", "south dakota",
        "tennessee", "utah", "vermont", "virginia", "west virginia",
        "wisconsin", "wyoming", "rockies", "rocky mountains", "grand canyon",
        "yellowstone", "yosemite"
    ]
    if any(x in loc_lower for x in us_keywords):
        return "United States"

    # Colombia
    if any(x in loc_lower for x in ["colombia", "bogota", "medellin", "cartagena", "cali"]):
        return "Colombia"

    # Peru
    if any(x in loc_lower for x in ["peru", "lima", "cusco", "machu picchu", "arequipa"]):
        return "Peru"

    # Chile
    if any(x in loc_lower for x in ["chile", "santiago", "patagonia"]):
        return "Chile"

    # Costa Rica
    if any(x in loc_lower for x in ["costa rica", "san jose"]):
        return "Costa Rica"

    # LLM Fallback for unmapped locations
    try:
        from google.genai import Client
        client = Client()
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f"What country is the travel destination '{loc}' located in? Return ONLY the clean, standard country name."
        )
        resolved = response.text.strip().replace(".", "")
        resolved = resolved.split("\n")[0].replace("`", "").strip()
        if resolved and len(resolved) < 50:
            return resolved
    except Exception:
        pass

    return loc.title()


def lookup_recommended_vaccines(country_name: str) -> list[str]:
    """Determines recommended travel vaccinations based on country health guidelines.
    
    Args:
        country_name: Canonical country name.
    """
    c = country_name.lower().strip()
    vaccines = []
    
    high_risk_yellow_fever = {"kenya", "brazil", "colombia", "peru", "nigeria", "ghana", "uganda", "congo", "tanzania", "angola", "ethiopia", "ecuador", "venezuela"}
    high_risk_typhoid_hep_a = {"india", "thailand", "vietnam", "indonesia", "cambodia", "nepal", "bangladesh", "philippines", "malaysia", "costa rica", "panama", "jamaica", "dominican republic", "honduras", "guatemala", "mexico", "morocco", "egypt", "south africa"}
    high_risk_je = {"india", "thailand", "vietnam", "indonesia", "cambodia", "nepal", "bangladesh", "philippines", "malaysia", "china"}
    
    if c in high_risk_yellow_fever:
        vaccines.append("Yellow Fever")
    if c in high_risk_typhoid_hep_a:
        vaccines.append("Typhoid")
        vaccines.append("Hepatitis A")
    if c in high_risk_je:
        vaccines.append("Japanese Encephalitis")
        
    return list(vaccines)


def parse_weather_suggections_fallback(weather_info: str) -> list[tuple[str, int, str, str]]:
    """Evaluates 7-tier weather keyword rules and returns static pack suggections.
    
    Args:
        weather_info: Weather description text.
    """
    suggestions = [
        ("Comfortable Walking Shoes", 1, "Footwear", "High"),
        ("Toothbrush & Toiletries", 1, "Hygiene", "High")
    ]
    
    w_lower = weather_info.lower()
    
    # 1. Rain / Mist / Showers / Damp
    if any(keyword in w_lower for keyword in ["rain", "shower", "mist", "damp", "drizzle", "fog"]):
        suggestions.append(("Compact Umbrella", 1, "Accessories", "Medium"))
        suggestions.append(("Waterproof Rain Jacket", 1, "Clothing", "Medium"))
        suggestions.append(("Quick-Dry Clothing", 1, "Clothing", "Low"))

    # 2. Sun / Sunny / Humid / Sun exposure
    if any(keyword in w_lower for keyword in ["sunny", "sunshine", "sun exposure", "humidity", "humid"]):
        suggestions.append(("Sunscreen SPF 50", 1, "Hygiene", "High"))
        suggestions.append(("Sunglasses with UV protection", 1, "Accessories", "Low"))
        suggestions.append(("Wide-Brimmed Sun Hat", 1, "Accessories", "Medium"))

    # 3. Freezing / Sub-zero / Summit / Alpine / Snow
    if any(keyword in w_lower for keyword in ["freezing", "sub-zero", "summit", "alpine", "snow"]):
        suggestions.append(("Thermal Base Layer Top & Bottom", 1, "Clothing", "High"))
        suggestions.append(("Windproof & Waterproof Outer Shell Jacket", 1, "Clothing", "High"))
        suggestions.append(("Heavy Fleece or Down Jacket", 1, "Clothing", "High"))
        suggestions.append(("Insulated Thermal Pants", 1, "Clothing", "Medium"))
        suggestions.append(("Warm Thermal Socks", 1, "Clothing", "High"))
        suggestions.append(("Insulated Gloves & Beanie", 1, "Clothing", "High"))
        suggestions.append(("Fleece Neck Gaiter", 1, "Clothing", "Medium"))

    # 4. Cold / Winter / Wind (Temp < 50°F / 10°C)
    elif any(keyword in w_lower for keyword in ["cold", "winter", "windy"]) or "38°f" in w_lower or "45°f" in w_lower:
        suggestions.append(("Heavy Winter Coat", 1, "Clothing", "High"))
        suggestions.append(("Warm Wool Sweaters", 2, "Clothing", "Medium"))
        suggestions.append(("Long Denim Pants or Chinos", 2, "Clothing", "Medium"))
        suggestions.append(("Knit Gloves & Scarf", 1, "Clothing", "Medium"))
        suggestions.append(("Thick Winter Socks", 2, "Clothing", "Medium"))

    # 5. Cool / Maritime (Temp 50°F to 65°F)
    elif any(keyword in w_lower for keyword in ["cool", "maritime"]) or "58°f" in w_lower or "62°f" in w_lower or "64°f" in w_lower:
        suggestions.append(("Lightweight Layering Sweater", 2, "Clothing", "High"))
        suggestions.append(("Windbreaker Jacket", 1, "Clothing", "Medium"))
        suggestions.append(("Long Pants or Jeans", 2, "Clothing", "High"))
        suggestions.append(("Sturdy Closed-Toe Shoes", 1, "Footwear", "High"))

    # 6. Mild / Temperate (Temp 65°F to 75°F)
    elif any(keyword in w_lower for keyword in ["mild", "temperate"]) or "66°f" in w_lower or "72°f" in w_lower or "76°f" in w_lower:
        suggestions.append(("Light Cardigan or Cardigan Sweater", 1, "Clothing", "Medium"))
        suggestions.append(("Long Sleeve Shirts", 2, "Clothing", "Medium"))
        suggestions.append(("Chinos or Casual Pants", 2, "Clothing", "High"))
        suggestions.append(("Comfortable Walking Sneakers", 1, "Footwear", "High"))

    # 7. Hot / Tropical / Desert (Temp > 75°F)
    if any(keyword in w_lower for keyword in ["hot", "tropical", "desert"]) or any(t in w_lower for t in ["82°f", "85°f", "86°f", "88°f", "90°f", "95°f", "104°f"]):
        suggestions.append(("Lightweight Breathable Shorts", 2, "Clothing", "High"))
        suggestions.append(("Linen or Moisture-Wicking Shirts", 3, "Clothing", "High"))
        suggestions.append(("Swimwear / Swim Trunks", 1, "Clothing", "Medium"))
        suggestions.append(("Breathable Sandals or Flip-Flops", 1, "Footwear", "Medium"))
        suggestions.append(("UV-Protection Lightweight Clothing", 1, "Clothing", "Medium"))
        suggestions.append(("Cooling Towel", 1, "Accessories", "Low"))
        
    return suggestions


def parse_activity_gear_fallback(activities: list[str]) -> list[tuple[str, int, str, str, str]]:
    """Evaluates planned activity keywords and returns fallback clothing and accessories.
    
    Args:
        activities: List of activity strings.
    """
    fallback_items = []
    
    for act in activities:
        act_lower = act.lower().strip()
        
        if "hike" in act_lower or "hiking" in act_lower or "trek" in act_lower:
            fallback_items.extend([
                ("Hiking Boots", 1, "Footwear", "High", "Sturdy boots for hiking."),
                ("Trail Map & Compass", 1, "Navigation", "Medium", "Physical map of the trail."),
                ("Reusable Water Bottle", 1, "Accessories", "High", "Hydration for the trail."),
                ("Daypack", 1, "Accessories", "Medium", "Small pack to carry daily hiking gear.")
            ])
        elif "swim" in act_lower or "pool" in act_lower or "beach" in act_lower:
            fallback_items.extend([
                ("Swimwear", 2, "Clothing", "High", "Bathing suit for swimming."),
                ("Quick-dry Towel", 1, "Accessories", "Medium", "Compact towel for swimming/beach."),
                ("Goggles", 1, "Accessories", "Low", "Eye protection for swimming.")
            ])
        elif "dinner" in act_lower or "fancy" in act_lower or "formal" in act_lower:
            fallback_items.extend([
                ("Formal Outfit", 1, "Clothing", "High", "Nice attire for formal dinners."),
                ("Dress Shoes", 1, "Footwear", "Medium", "Shoes matching the formal outfit.")
            ])
        elif "business" in act_lower or "meeting" in act_lower or "conference" in act_lower:
            fallback_items.extend([
                ("Business Attire", 2, "Clothing", "High", "Professional wear for meetings."),
                ("Notebook & Pen", 1, "Office", "Medium", "Taking notes during meetings."),
                ("Business Cards", 20, "Office", "Low", "Networking cards.")
            ])
        elif "ski" in act_lower or "snowboarding" in act_lower or "winter sports" in act_lower:
            fallback_items.extend([
                ("Ski Goggles", 1, "Accessories", "High", "Eye protection in the snow."),
                ("Warm Gloves / Mittens", 1, "Clothing", "High", "Thermal hand wear."),
                ("Ski Socks", 3, "Clothing", "High", "Thick socks for ski boots.")
            ])
        elif "academic" in act_lower or "academics" in act_lower or "boarding school" in act_lower:
            fallback_items.extend([
                ("Student ID Card", 1, "General", "High", "Student identification card."),
                ("Academic Notebooks & Stationery", 1, "General", "Medium", "Notebooks and pens for class."),
                ("Calculator & School Textbooks", 1, "General", "Medium", "Educational materials and calculator.")
            ])
        elif "study-abroad" in act_lower or "study abroad" in act_lower:
            fallback_items.extend([
                ("Student ID Card", 1, "General", "High", "Student identification card."),
                ("Study Abroad Visa & Enrollment Letter", 1, "General", "High", "Visa and study verification documentation."),
                ("Emergency Contact Info & Travel Insurance Card", 1, "General", "High", "Important safety and medical insurance documentation.")
            ])
            
    return fallback_items
