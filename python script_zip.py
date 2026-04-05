import zipfile
import os
import shutil

def extraire_cover(zip_path):
    # Vérifier que le fichier existe
    if not os.path.isfile(zip_path):
        print("Fichier ZIP introuvable.")
        return

    # Nom du dossier = nom du zip sans extension
    dossier_nom = os.path.splitext(os.path.basename(zip_path))[0]
    dossier_path = os.path.join(os.path.dirname(zip_path), dossier_nom)

    # ✅ Si le dossier existe déjà → on skip
    if os.path.exists(dossier_path):
        print(f"⏭ Déjà traité : {dossier_nom}")
        return

    # Créer le dossier
    os.makedirs(dossier_path, exist_ok=True)

    # ✅ Déplacer le ZIP dans le dossier
    zip_nouveau_path = os.path.join(dossier_path, os.path.basename(zip_path))
    shutil.move(zip_path, zip_nouveau_path)

    with zipfile.ZipFile(zip_nouveau_path, 'r') as zip_ref:
        fichiers = zip_ref.namelist()

        extensions_images = ('.png', '.jpg', '.jpeg', '.webp')
        image_trouvee = None

        for fichier in fichiers:
            if fichier.lower().endswith(extensions_images):
                image_trouvee = fichier
                break

        if image_trouvee is None:
            print(f"Aucune image trouvée dans {dossier_nom}")
            return

        zip_ref.extract(image_trouvee, dossier_path)

        chemin_image_extraite = os.path.join(dossier_path, image_trouvee)
        chemin_final = os.path.join(dossier_path, "cover.png")

        # ✅ Si cover existe déjà → skip sécurité
        if os.path.exists(chemin_final):
            print(f"⚠ cover déjà existant : {dossier_nom}")
            return

        if os.path.abspath(chemin_image_extraite) != os.path.abspath(chemin_final):
            shutil.move(chemin_image_extraite, chemin_final)

        # Nettoyage des sous-dossiers
        dossier_interne = os.path.join(dossier_path, image_trouvee.split('/')[0])
        if os.path.isdir(dossier_interne):
            shutil.rmtree(dossier_interne)

        print(f"✔ Terminé : {dossier_nom}")


def traiter_dossier(dossier):
    for fichier in os.listdir(dossier):
        if fichier.lower().endswith(".zip"):
            chemin_zip = os.path.join(dossier, fichier)
            extraire_cover(chemin_zip)


# 📁 Ton dossier
#dossier_test = r"C:\Users\kingm\PycharmProjects\PythonProject\Data\TesteMihon"

# Nouveau chemin
dossier_test = r"C:\Users\kingm\PycharmProjects\MihonStructure\Data\TesteMihon"
traiter_dossier(dossier_test)