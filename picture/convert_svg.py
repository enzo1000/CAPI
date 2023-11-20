from PIL import Image
from io import BytesIO

# Charger le contenu du fichier SVG
# with open('cartes/cartes_0.svg', 'r') as file:
#     svg_data = file.read()

# # Convertir le SVG en image avec Pillow
# svg_image = Image.open(BytesIO(svg_data.encode('utf-8')))
# svg_image.save('cartes/carte0.png', format='PNG')



# Charger le contenu du fichier SVG
with open('cartes/cartes_0.svg', 'r') as file:
    svg_data = file.read()

# Convertir le SVG en image avec Pillow
svg_image = Image.fromstring('RGB', (1, 1), svg_data)

# Enregistrer l'image convertie au format PNG
svg_image.save('cartes/cartes_0.svg', format='PNG')