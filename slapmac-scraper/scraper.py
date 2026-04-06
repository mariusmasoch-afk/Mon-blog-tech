"""
SlapMac Scraper
Collecte les informations publiques sur l'application SlapMac (mars 2026)
Sources : slapmac.com, Product Hunt, ToolRadar, presse tech
"""

import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

SOURCES = {
    "slapmac_com": "https://slapmac.com",
    "product_hunt": "https://www.producthunt.com/products/slapmac",
    "toolradar": "https://toolradar.com/tools/slapmac",
    "lebigdata": "https://www.lebigdata.fr/slapmac-fait-gemir-votre-mac-quand-vous-lui-donnez-une-fessee-le-dev-devient-riche",
    "iphonesoft": "https://iphonesoft.fr/2026/03/28/slapmac-application-absurde-gemir-macbook",
    "clubic": "https://www.clubic.com/actualite-606787-insolite-un-developpeur-s-enrichit-en-faisant-gemir-les-macbook.html",
}


def fetch(url: str, delay: float = 1.5) -> BeautifulSoup | None:
    """Télécharge une page et retourne un objet BeautifulSoup."""
    try:
        time.sleep(delay)
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        print(f"[ERREUR] {url} → {e}")
        return None


# ---------------------------------------------------------------------------
# Parsers par source
# ---------------------------------------------------------------------------

def parse_slapmac_com(soup: BeautifulSoup) -> dict:
    data = {}

    # Titre / tagline
    hero = soup.find("h1") or soup.find("h2")
    if hero:
        data["tagline"] = hero.get_text(strip=True)

    # Prix
    for tag in soup.find_all(string=True):
        if "$" in tag and any(c.isdigit() for c in tag):
            data["price_raw"] = tag.strip()
            break

    # Lien de téléchargement
    for a in soup.find_all("a", href=True):
        if "download" in a["href"].lower() or "release" in a["href"].lower():
            data["download_url"] = a["href"]
            break

    # Configuration système
    requirements = []
    for tag in soup.find_all(string=True):
        txt = tag.strip()
        if any(kw in txt.lower() for kw in ["macos", "m1", "m2", "sonoma", "silicon"]):
            if len(txt) < 120:
                requirements.append(txt)
    data["system_requirements"] = list(dict.fromkeys(requirements))  # dédoublonnage

    # Voice packs / son
    sound_info = []
    for tag in soup.find_all(string=True):
        txt = tag.strip()
        if any(kw in txt.lower() for kw in ["voice pack", "sound", "130", "clip"]):
            if 10 < len(txt) < 200:
                sound_info.append(txt)
    data["sound_info"] = list(dict.fromkeys(sound_info))

    # Roadmap
    roadmap = []
    for tag in soup.find_all(string=True):
        txt = tag.strip()
        if any(kw in txt.lower() for kw in ["v1.", "roadmap", "coming soon", "planned", "mcp", "ios"]):
            if 5 < len(txt) < 200:
                roadmap.append(txt)
    data["roadmap"] = list(dict.fromkeys(roadmap))

    return data


def parse_product_hunt(soup: BeautifulSoup) -> dict:
    data = {}

    # Description
    desc = soup.find("meta", {"name": "description"}) or soup.find("meta", {"property": "og:description"})
    if desc:
        data["description"] = desc.get("content", "").strip()

    # Votes / score
    for tag in soup.find_all(string=True):
        txt = tag.strip()
        if txt.isdigit() and int(txt) > 100:
            data["upvotes"] = int(txt)
            break

    # Auteur
    for tag in soup.find_all("a", href=True):
        if "@tonnoz" in tag.get_text(strip=True).lower() or "tonnoz" in tag["href"]:
            data["creator"] = tag.get_text(strip=True)
            break

    return data


def parse_press_article(soup: BeautifulSoup, source_name: str) -> dict:
    data = {"source": source_name}

    # Titre de l'article
    title = (
        soup.find("h1")
        or soup.find("meta", {"property": "og:title"})
    )
    if title:
        data["title"] = (
            title.get_text(strip=True)
            if title.name == "h1"
            else title.get("content", "").strip()
        )

    # Premier paragraphe significatif
    paragraphs = [
        p.get_text(strip=True)
        for p in soup.find_all("p")
        if len(p.get_text(strip=True)) > 80
    ]
    if paragraphs:
        data["intro"] = paragraphs[0]
        data["paragraphs_count"] = len(paragraphs)

    # Chiffres clés mentionnés dans le texte
    full_text = soup.get_text()
    metrics = []
    for kw in ["$5,000", "$5000", "5 000", "7 000", "7,000", "4 million", "10 million", "72 heures", "72 hours", "3 days"]:
        if kw.lower() in full_text.lower():
            metrics.append(kw)
    if metrics:
        data["key_figures_found"] = metrics

    return data


# ---------------------------------------------------------------------------
# Scraper principal
# ---------------------------------------------------------------------------

def run_scraper() -> dict:
    results = {
        "scraped_at": datetime.utcnow().isoformat() + "Z",
        "app": "SlapMac",
        "release_date": "2026-03-28",
        "developer": "Tonino Catapano (@tonnoz)",
        "sources": {},
    }

    print("Scraping slapmac.com...")
    soup = fetch(SOURCES["slapmac_com"])
    if soup:
        results["sources"]["slapmac_com"] = parse_slapmac_com(soup)

    print("Scraping Product Hunt...")
    soup = fetch(SOURCES["product_hunt"])
    if soup:
        results["sources"]["product_hunt"] = parse_product_hunt(soup)

    print("Scraping ToolRadar...")
    soup = fetch(SOURCES["toolradar"])
    if soup:
        results["sources"]["toolradar"] = parse_press_article(soup, "ToolRadar")

    print("Scraping LeBigData...")
    soup = fetch(SOURCES["lebigdata"])
    if soup:
        results["sources"]["lebigdata"] = parse_press_article(soup, "LeBigData")

    print("Scraping iPhoneSoft...")
    soup = fetch(SOURCES["iphonesoft"])
    if soup:
        results["sources"]["iphonesoft"] = parse_press_article(soup, "iPhoneSoft")

    print("Scraping Clubic...")
    soup = fetch(SOURCES["clubic"])
    if soup:
        results["sources"]["clubic"] = parse_press_article(soup, "Clubic")

    # Consolidation des données statiques connues
    results["consolidated"] = {
        "price_usd": 6.9,
        "platforms": ["macOS 14.6+ (Sonoma)"],
        "chip_requirement": "Apple Silicon M1 Pro+",
        "sound_packs": 7,
        "sound_clips": 130,
        "features": [
            "Détection de choc via accéléromètre",
            "Volume proportionnel à la force du coup",
            "Mode USB Moaner (son au branchement USB)",
            "Mode Lid Creak (son à l'ouverture/fermeture du couvercle)",
            "Compteur de gifles persistant",
            "Sensibilité et cooldown réglables",
            "Menu bar uniquement (sans icône dans le Dock)",
            "Lancement au démarrage",
        ],
        "roadmap": {
            "v1.3": ["Custom sound packs", "Serveur MCP local pour IA"],
            "future": ["Application iOS"],
        },
        "viral_metrics": {
            "revenue_72h": "$5,000",
            "installs_3_days": "7,000+",
            "instagram_views": "4,000,000",
            "x_views": "10,000,000",
            "product_hunt_votes": "474+",
        },
        "download_url": "https://release.slapmac.com/v1/apps/com.tonnoz.slapmac/download",
        "website": "https://slapmac.com",
        "product_hunt": "https://www.producthunt.com/products/slapmac",
    }

    return results


if __name__ == "__main__":
    data = run_scraper()

    output_file = "slapmac_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé. Données sauvegardées dans '{output_file}'")
    print(f"Sources scrapées : {len(data['sources'])}")
