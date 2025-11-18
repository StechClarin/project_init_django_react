# Fichier: Makefile
# -----------------------------------------------------------------
# L'équivalent de la section "scripts" de composer.json
#
# Utilisation:
#   make run              (Lance le serveur de dev)
#   make migrate          (Applique les migrations)
#   make config-server    (Configure le serveur)
#   make scaffold model=Student app=apps.students
# -----------------------------------------------------------------

# La commande par défaut (si on tape juste "make")
.DEFAULT_GOAL := help

## -----------------------------------------------------------------
## COMMANDES PRINCIPALES
## -----------------------------------------------------------------

config-server: ## Configure le serveur (migrations, seeds)
	@echo "--- Configuration du serveur (migrations) ---"
	./snake automigrate
	# ./snake craft seed:all # A décommenter si tu as des seeders

run: ## Lance le serveur de développement
	@echo "--- Lancement du serveur sur http://127.0.0.1:8000 ---"
	./snake runserver

## -----------------------------------------------------------------
## COMMANDES BASE DE DONNÉES
## -----------------------------------------------------------------

migrate: ## Applique les migrations
	./snake migrate

automigrate: ## Crée et applique les migrations (pour une app ou toutes)
	./snake craft automigrate $(app)

fresh: ## Réinitialise les migrations d'une app
	@echo "--- ATTENTION: Réinitialisation des migrations pour [$(app)] ---"
	./snake craft fresh $(app)

## -----------------------------------------------------------------
## COMMANDES CRAFT (Génération)
## -----------------------------------------------------------------

scaffold: ## Génère un scaffold complet (model, api, gql)
	@echo "--- Création du scaffold pour [$(model)] dans [$(app)] ---"
	./snake craft scaffold $(model) $(app)

model: ## Génère un modèle
	./snake craft model $(model) $(app)

apiview: ## Génère une vue API (ViewSet)
	./snake craft apiview $(model) $(app)

## -----------------------------------------------------------------
## AIDE
## -----------------------------------------------------------------
help: ## Affiche ce message d'aide
	@echo "Commandes disponibles pour ce projet :"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'