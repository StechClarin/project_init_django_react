# apps/core/graphql/schema.py
import graphene
from apps.core.utils.schema_loader import load_all_queries

# 1. On charge toutes les queries automatiquement
found_queries = load_all_queries()

# 2. On crée la classe Query dynamiquement
if found_queries:
    # On crée une classe qui hérite de toutes les queries trouvées
    class Query(*found_queries, graphene.ObjectType):
        pass
else:
    # Fallback si aucune query n'existe encore
    class Query(graphene.ObjectType):
        pass

# 3. On crée le schéma
# (Pas de Mutation pour l'instant, c'est du REST)
schema = graphene.Schema(query=Query)