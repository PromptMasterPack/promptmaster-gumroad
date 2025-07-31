import os
import json
from fpdf import FPDF

# Modèles génériques (50 patterns)
TEMPLATES = [
    "Comment un {niche} peut-il augmenter son taux d'engagement ?",
    "Donnez 5 idées de contenu pour un(e) {niche}.",
    "Quel ton doit utiliser un(e) {niche} pour toucher son audience ?",
    "Proposez un plan de publication hebdomadaire pour un(e) {niche}.",
    "Comment un(e) {niche} peut-il optimiser son profil LinkedIn ?",
    # … ajoutez jusqu’à 50 modèles différents …
]

def gen_prompts_for(niche):
    prompts = []
    for i, tpl in enumerate(TEMPLATES, 1):
        prompts.append(f"{i}. {tpl.format(niche=niche)}")
    return prompts

def pdf_for_niche(niche):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    prompts = gen_prompts_for(niche)
    for line in prompts:
        pdf.multi_cell(0, 10, line)
    return pdf

def main():
    # Charge la liste des niches
    with open("niches.json", "r", encoding="utf-8") as f:
        niches = json.load(f)
    os.makedirs("assets", exist_ok=True)
    for entry in niches:
        niche = entry["niche"]
        pdf = pdf_for_niche(niche)
        filename = f"assets/PromptMaster_{niche.replace(' ', '_')}.pdf"
        pdf.output(filename)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
