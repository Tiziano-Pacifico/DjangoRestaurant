import os
import django
from django.conf import settings
from django.apps import apps

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodOnline_main.settings")
django.setup()

MEDIA_ROOT = settings.MEDIA_ROOT

missing_files = []

# Per ogni modello installato
for model in apps.get_models():
    fields = [f for f in model._meta.fields if hasattr(f, 'upload_to')]
    if not fields:
        continue  # Salta se non ci sono campi media

    for instance in model.objects.all():
        for field in fields:
            file_field = getattr(instance, field.name)
            if file_field and file_field.name:
                file_path = os.path.join(MEDIA_ROOT, file_field.name)
                if not os.path.exists(file_path):
                    missing_files.append(file_field.name)

# Risultati
if missing_files:
    print("⚠️ File media mancanti trovati:")
    for path in missing_files:
        print(" -", path)
else:
    print("✅ Tutti i file media sono presenti.")

print(f"\nTotale file mancanti: {len(missing_files)}")
