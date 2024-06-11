
# Semantic Proximity Crawler

Cette application Python est un crawler de site web qui analyse le contenu des pages, identifie les thématiques principales et génère des visualisations de type graph forcé pour représenter ces thématiques.

## Fonctionnalités

- Crawler de site web avec limitation du nombre de pages.
- Extraction de contenu selon des sélecteurs CSS spécifiés.
- Analyse thématique des contenus extraits.
- Génération de visualisations de type graph forcé.
- Interface graphique pour faciliter l'utilisation des scripts.

## Prérequis

- Python 3.6 ou supérieur
- `pip` pour l'installation des dépendances

## Installation

1. Clonez le dépôt sur votre machine locale :

    \`\`\`bash
    git clone https://github.com/friteuseb/semantic_proximity.git
    cd semantic_proximity
    \`\`\`

2. Créez un environnement virtuel (recommandé) et activez-le :

    \`\`\`bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    \`\`\`

3. Installez les dépendances requises :

    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

## Utilisation

### Utilisation avec l'Interface Graphique

Pour utiliser l'interface graphique :

    \`\`\`bash
    python3 gui_crawler.py
    \`\`\`

### Utilisation en Ligne de Commande

#### Crawler et Analyse

Pour crawler un site web et analyser les thématiques :

    \`\`\`bash
    python3 crawler.py <URL_DE_BASE> <SELECTEURS_CSS> <NOMBRE_DE_PAGES>
    \`\`\`

- \`<URL_DE_BASE>\` : L'URL de base du site web à crawler (ex: \`https://example.com\`).
- \`<SELECTEURS_CSS>\` : Les classes ou ID des zones à indexer, séparés par des virgules (ex: \`.content, #main\`).
- \`<NOMBRE_DE_PAGES>\` : Le nombre de pages à crawler (0 pour crawler tout le site).

Exemple :

    \`\`\`bash
    python3 crawler.py https://example.com ".content" 10
    \`\`\`

#### Visualisation des Données

Pour visualiser les données enregistrées dans la base de données :

    \`\`\`bash
    python3 view_data.py
    \`\`\`

#### Génération du Graph Forcé

Pour générer un graph forcé représentant les thématiques des pages :

    \`\`\`bash
    python3 forced_graph.py
    \`\`\`

## Structure du Projet

- \`crawler.py\` : Script principal pour crawler le site et analyser les thématiques.
- \`view_data.py\` : Script pour afficher les données enregistrées dans la base de données.
- \`forced_graph.py\` : Script pour générer un graph forcé des thématiques.
- \`gui_crawler.py\` : Interface graphique pour faciliter l'utilisation des scripts.
- \`requirements.txt\` : Liste des dépendances Python requises.

## Contribuer

Les contributions sont les bienvenues ! Si vous avez des idées d'améliorations ou des corrections à apporter, n'hésitez pas à ouvrir une pull request ou une issue.

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
