from PIL import Image, ImageEnhance, ImageChops
import os

def clean_and_normalize(image_path, target_height=100):
    if not os.path.exists(image_path):
        print(f'Fichier introuvable: {image_path}')
        return
    print(f'Traitement de {image_path}...')
    try:
        img = Image.open(image_path).convert('RGBA')
        data = img.getdata()
        new_data = []
        for item in data:
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        alpha = img.split()[-1]
        bbox = alpha.getbbox()
        if bbox:
            img = img.crop(bbox)
        sharp_enhancer = ImageEnhance.Sharpness(img)
        img = sharp_enhancer.enhance(2.0)
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(1.2)
        aspect_ratio = img.width / img.height
        new_width = int(target_height * aspect_ratio)
        img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)
        output_path = image_path.replace('.jpg', '.png').replace('.jpeg', '.png')
        img.save(output_path, 'PNG')
        print(f'Succes: {output_path}')
    except Exception as e:
        print(f'Erreur: {image_path} - {e}')

# All files in directory (excluding the script itself)
files = ['fond_cv_avec_text.jpg', 'fond_cv.png', 'hard_skills.png', 'languages.png', 'professional_experiences.png', 'soft_skills.png']
for f in files:
    clean_and_normalize(f)