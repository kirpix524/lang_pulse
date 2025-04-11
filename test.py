from storage.lang_repo import LanguageRepository

lang_repo=LanguageRepository()

langs=lang_repo.get_language_names()
print(langs)