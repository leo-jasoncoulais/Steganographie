
# Import de la classe Image de la librairie Pillow
from PIL import Image

def encrypt(little=Image, big=Image):
    # Creer une nouvelle image qui va contenir celle cachée + initilisation de la variable progress pour la barre de progression
    newImage, progress = Image.new('RGB', size=(big.size[0], big.size[1])), -1

    print("\n\033[0;31m[!] Pour la survie de l'image en cours de création, veuillez l'enregistrer pour l'utiliser. Une capture d'écran détruira les données ! De même, evitez les compressions et privilegiez le .PNG !\033[0m\n")
    print("Transformation en cours, veuillez patienter...")

    # Explorer chaque colonne de la petite image
    for i in range(little.size[0]):
        # Afficher la seconde barre de progression
        if i*100//little.size[0]!=progress:
            progress = i*100//little.size[0]
            print("(1/2) - Progression: ["+progress*">"+(100-progress)*" "+"] "+str(progress)+"%", end='\r')
            print(end="\x1b[2K")
        # Explorer chaque ligne de chaque colonne de la petite image
        for k in range(little.size[1]):
            # Calculer la position à laquelle se trouve le pixel (de gauche à droite et de haut en bas)
            position = 3*(i*little.size[1]+k)
            # Calcul des coordonnées du nouveau pixel grâce à la position
            x, y = position%big.size[0],  position//big.size[0]
            # Convertir les intensités du pixel de la petite image en string et rajouter des zéros si necessaires pour la suite du programme
            littlePixel = [ str(little.getpixel(( i, k ))[0]) , str(little.getpixel(( i, k ))[1]) , str(little.getpixel(( i, k ))[2]) ]
            for o in range(len(littlePixel)):
                if int(littlePixel[o]) < 10: littlePixel[o] = "00" + littlePixel[o]
                elif int(littlePixel[o]) < 100: littlePixel[o] = "0" + littlePixel[o]
                
            # Placer les données necessaires sur les 3 pixels suivants, voir compte rendu pour + de details
            for o in range(3):
                bigPixel = [ str(big.getpixel((x+o,y))[0]) , str(big.getpixel((x+o,y))[1]) , str(big.getpixel((x+o,y))[2]) ]
                newPixel = (  int(bigPixel[0][:-1] + littlePixel[o][0]) , int(bigPixel[1][:-1] + littlePixel[o][1]) , int(bigPixel[2][:-1] + littlePixel[o][2]) )
                newImage.putpixel((x+o,y), newPixel)

    # Explorer chaque colonne de la grosse image
    for i in range(big.size[0]):
        # Afficher la seconde barre de progression
        if i*100//big.size[0]!=progress:
            progress = i*100//big.size[0]
            print("(2/2) - Progression: ["+progress*">"+(100-progress)*" "+"] "+str(progress)+"%", end='\r')
            print(end="\x1b[2K")
        # Explorer les lignes pas encore visitées par les boucles precedents. Appliquer les intensités normales de la grosse image
        for k in range(little.size[1],big.size[1]): newImage.putpixel((i,k),big.getpixel((i,k)))

    # Afficher l'image
    newImage.show()

    print("Transformation terminée !")
