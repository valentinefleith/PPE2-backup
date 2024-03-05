def filtre_titre_contains(substr):
    def check_filtre(item):
        return substr in item["title"]
    return check_filtre

contains_a = filtre_title_contains("a")

# pour l'appeler ensuite :
print(contains_a(item))
