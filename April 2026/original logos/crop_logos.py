from PIL import Image, ImageEnhance, ImageChops
import os

def clean_and_normalize(image_path, target_height=100):
    if not os.path.exists(image_path):
        print(f"Fichier ignoré (introuvable) : {image_path}")
        return

    print(f"Traitement de {image_path}...")
    try:
        # 1. Ouverture et conversion en RGBA pour gérer la transparence
        img = Image.open(image_path).convert("RGBA")
        
        # 2. Nettoyage du fond (remplace le blanc/presque blanc par du transparent)
        # Très utile pour les JPG comme IMG_4647.jpg ou les PNG avec fond blanc solide
        data = img.getdata()
        new_data = []
        for item in data:
            # Si le pixel est très clair (presque blanc), on le rend transparent
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)

        # 3. Recadrage (Crop) automatique des bordures transparentes
        alpha = img.split()[-1]
        bbox = alpha.getbbox()
        if bbox:
            img = img.crop(bbox)

        # 4. Amélioration : Netteté et Contraste (enlève le flou)
        # Augmentation de la netteté
        sharp_enhancer = ImageEnhance.Sharpness(img)
        img = sharp_enhancer.enhance(2.0) 
        
        # Augmentation légère du contraste
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(1.2)

        # 5. Normalisation de la taille (hauteur fixe pour cohérence visuelle)
        aspect_ratio = img.width / img.height
        new_width = int(target_height * aspect_ratio)
        img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)

        # 6. Sauvegarde (on force le PNG pour conserver la transparence)
        # Si le fichier d'origine était un jpg, on change son nom pour l'HTML
        output_path = image_path.replace('.jpg', '.png').replace('.jpeg', '.png')
        img.save(output_path, "PNG")
        print(f"Succès : {output_path} nettoyé et normalisé.")

    except Exception as e:
        print(f"Erreur lors du traitement de {image_path} : {e}")

if __name__ == "__main__":
    # Liste de tous les logos téléchargés
    logos = [
        "logo_mobirider.png", 
        "logo_motorola.png", 
        "logo_ffly4u.png", 
        "logo_freescale.png", 
        "logo_inpg.png", 
        "logo_intel.png", 
        "logo_noema.png", 
        "logo_nttdocomo.png", 
        "logo_viettel.png",
        "IMG_4647.jpg", # Ancien logo mobi rider
        "IMG_4648.jpg"  # Ancien logo motorola
    ]
    
    for logo in logos:
        clean_and_normalize(logo)