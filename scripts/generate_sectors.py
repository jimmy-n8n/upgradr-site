#!/usr/bin/env python3
"""
Génère les pages secteur pour UpgradR via Perplexity Sonar Pro.
Usage: python3 generate_sectors.py [--sector slug] [--all]
"""

import json
import os
import re
import sys
import time
import argparse
import requests

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
DATA_FILE = os.path.join(os.path.dirname(__file__), "../src/data/sectors.json")

SECTORS = [
    {"slug": "cabinet-comptable", "label": "Cabinet Comptable", "label_plural": "cabinets comptables"},
    {"slug": "agence-immobiliere", "label": "Agence Immobilière", "label_plural": "agences immobilières"},
    {"slug": "clinique-dentaire", "label": "Clinique Dentaire", "label_plural": "cliniques dentaires"},
    {"slug": "cabinet-veterinaire", "label": "Cabinet Vétérinaire", "label_plural": "cabinets vétérinaires"},
    {"slug": "restaurant-restauration", "label": "Restaurant / Restauration", "label_plural": "restaurants et établissements de restauration"},
    {"slug": "agence-marketing", "label": "Agence Marketing", "label_plural": "agences marketing"},
    {"slug": "agence-web", "label": "Agence Web", "label_plural": "agences web et digitales"},
    {"slug": "bureau-etudes", "label": "Bureau d'Études", "label_plural": "bureaux d'études"},
    {"slug": "cabinet-avocat", "label": "Cabinet d'Avocats", "label_plural": "cabinets d'avocats"},
    {"slug": "agence-recrutement", "label": "Agence de Recrutement", "label_plural": "agences de recrutement et cabinets RH"},
    {"slug": "e-commerce", "label": "E-commerce", "label_plural": "boutiques e-commerce"},
    {"slug": "grossiste-distribution", "label": "Grossiste / Distribution", "label_plural": "grossistes et sociétés de distribution"},
    {"slug": "artisan-batiment", "label": "Artisan / BTP", "label_plural": "artisans et entreprises du BTP"},
    {"slug": "agence-communication", "label": "Agence de Communication", "label_plural": "agences de communication"},
    {"slug": "salon-beaute", "label": "Salon de Beauté / Coiffure", "label_plural": "salons de beauté et instituts de coiffure"},
    {"slug": "centre-formation", "label": "Centre de Formation", "label_plural": "centres et organismes de formation"},
    {"slug": "agence-voyage", "label": "Agence de Voyage", "label_plural": "agences de voyage"},
    {"slug": "cabinet-architecte", "label": "Cabinet d'Architecture", "label_plural": "cabinets d'architecture"},
    {"slug": "agence-assurance", "label": "Agence d'Assurance", "label_plural": "agences et courtiers en assurance"},
    {"slug": "promoteur-immobilier", "label": "Promoteur Immobilier", "label_plural": "promoteurs immobiliers"},
    {"slug": "gestionnaire-copropriete", "label": "Gestionnaire de Copropriété", "label_plural": "gestionnaires et syndics de copropriété"},
    {"slug": "cabinet-kinesitherapeute", "label": "Cabinet de Kinésithérapie", "label_plural": "cabinets de kinésithérapie"},
    {"slug": "studio-graphisme-design", "label": "Studio de Design / Graphisme", "label_plural": "studios de design et de graphisme"},
    {"slug": "agence-evenementielle", "label": "Agence Événementielle", "label_plural": "agences événementielles"},
    {"slug": "garage-automobile", "label": "Garage / Automobile", "label_plural": "garages et concessionnaires automobiles"},
    {"slug": "societe-nettoyage", "label": "Société de Nettoyage", "label_plural": "sociétés de nettoyage et de propreté"},
    {"slug": "clinique-medecine", "label": "Clinique / Cabinet Médical", "label_plural": "cliniques et cabinets médicaux"},
    {"slug": "logistique-transport", "label": "Logistique / Transport", "label_plural": "sociétés de logistique et transport"},
    {"slug": "startup-tech", "label": "Startup Tech / SaaS", "label_plural": "startups tech et éditeurs SaaS"},
    {"slug": "consultant-independant", "label": "Consultant Indépendant", "label_plural": "consultants et freelances"},
]

PROMPT_TEMPLATE = """Tu es un expert en automatisation de processus pour les PME francophones. Tu cites des chiffres précis et vérifiables issus d'études sectorielles françaises ou européennes.

Génère un JSON structuré pour une page web sur l'automatisation dans le secteur : {label_plural}.

RÈGLES STRICTES :
1. L'intro doit être "speakable" : 2-3 phrases COURTES, directes, avec des CHIFFRES PRÉCIS (ex: "Les {label_plural} perdent en moyenne 11 heures par semaine sur des tâches administratives répétitives."). Chaque phrase doit pouvoir être lue à voix haute et citée telle quelle.
2. Chaque tâche doit mentionner un chiffre précis de temps perdu et de temps économisé.
3. Les FAQ : réponses en 1-2 phrases MAXIMUM. Format idéal pour citation par un LLM ou assistant vocal. Direct, factuel, actionnable.
4. Les données sectorielles doivent être spécifiques au secteur {label} en France ou en Europe.
5. Les chiffres ROI et temps économisé doivent être réalistes et basés sur des cas concrets.

Le JSON doit respecter EXACTEMENT ce format (réponds uniquement avec le JSON, sans markdown ni explication) :

{{
  "intro": "Phrase 1 courte avec chiffre précis sur les pertes de temps des {label_plural}. Phrase 2 courte sur l'impact financier chiffré. Phrase 3 courte sur ce que l'automatisation change concrètement.",
  "taches": [
    {{
      "titre": "Nom court de la tâche automatisable (5 mots max)",
      "description": "Description concrète : la tâche manuelle actuelle (avec chiffre de temps perdu), puis comment elle est automatisée avec les outils cités",
      "outils": ["Outil1", "Outil2"],
      "temps_economise": "Xh/semaine"
    }}
  ],
  "workflow_exemple": {{
    "titre": "Nom du workflow exemple concret pour {label}",
    "contexte": "1 phrase décrivant le problème exact que ce workflow résout, avec un chiffre.",
    "etapes": [
      "Étape 1 : action précise avec outil nommé",
      "Étape 2 : action précise avec outil nommé",
      "Étape 3 : action précise avec outil nommé",
      "Étape 4 : action précise avec résultat mesurable"
    ],
    "gain": "Chiffre concret : Xh/semaine économisées soit ~Y€/mois (base SMIC chargé)"
  }},
  "outils_recommandes": ["Outil1", "Outil2", "Outil3", "Outil4"],
  "roi_estime": "X à Y heures automatisées par semaine, soit Z€ à W€ économisés par mois",
  "faq": [
    {{
      "question": "Question directe et spécifique que se pose un {label} sur l'automatisation",
      "reponse": "Réponse en 1-2 phrases maximum. Factuelle, chiffrée si possible, directement actionnable."
    }},
    {{
      "question": "Deuxième question pratique spécifique au secteur {label}",
      "reponse": "Réponse en 1-2 phrases maximum. Directe et citables par un assistant IA."
    }},
    {{
      "question": "Troisième question sur le coût ou la mise en place pour un {label}",
      "reponse": "Réponse en 1-2 phrases maximum avec chiffre concret."
    }},
    {{
      "question": "Quatrième question sur les résultats attendus pour un {label}",
      "reponse": "Réponse en 1-2 phrases maximum avec délai et chiffre de ROI."
    }}
  ],
  "meta_description": "Meta description SEO de 150 caractères max, incluant le mot-clé 'automatisation {label}' et un chiffre concret"
}}

Génère exactement 6 tâches et 4 questions FAQ. Sois ultra-spécifique au secteur {label} en France, avec des chiffres précis et réalistes sourcés sur le marché français. Les réponses FAQ doivent être si courtes et directes qu'un LLM peut les citer mot pour mot."""


def call_perplexity(prompt: str) -> str:
    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers={
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "sonar-pro",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 3000,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def extract_json(text: str) -> dict:
    # Nettoie le markdown si présent
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()
    return json.loads(text)


def load_existing() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
        return {s["slug"]: s for s in data}
    return {}


def save_all(sectors_dict: dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(list(sectors_dict.values()), f, ensure_ascii=False, indent=2)
    print(f"✅ Sauvegardé : {DATA_FILE} ({len(sectors_dict)} secteurs)")


def generate_sector(sector: dict, existing: dict) -> dict:
    slug = sector["slug"]
    if slug in existing:
        print(f"  ⏭️  {slug} déjà généré, skip")
        return existing[slug]

    print(f"  🔄 Génération : {sector['label']}...")
    prompt = PROMPT_TEMPLATE.format(
        label=sector["label"],
        label_plural=sector["label_plural"],
    )
    try:
        raw = call_perplexity(prompt)
        data = extract_json(raw)
        result = {
            "slug": slug,
            "label": sector["label"],
            "label_plural": sector["label_plural"],
            **data,
        }
        print(f"  ✅ {slug} — {len(data.get('taches', []))} tâches générées")
        return result
    except Exception as e:
        print(f"  ❌ Erreur {slug} : {e}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sector", help="Slug d'un secteur spécifique")
    parser.add_argument("--all", action="store_true", help="Générer tous les secteurs")
    parser.add_argument("--batch", type=int, default=5, help="Nombre de secteurs à générer (défaut: 5)")
    args = parser.parse_args()

    existing = load_existing()

    if args.sector:
        targets = [s for s in SECTORS if s["slug"] == args.sector]
        if not targets:
            print(f"Secteur inconnu : {args.sector}")
            sys.exit(1)
    elif args.all:
        targets = SECTORS
    else:
        # Par défaut : batch des premiers non générés
        targets = [s for s in SECTORS if s["slug"] not in existing][: args.batch]

    print(f"\n🚀 UpgradR — Génération pages secteur ({len(targets)} secteurs)\n")

    for i, sector in enumerate(targets):
        result = generate_sector(sector, existing)
        if result:
            existing[result["slug"]] = result
        if i < len(targets) - 1:
            time.sleep(1.5)  # Rate limit

    save_all(existing)


if __name__ == "__main__":
    main()
