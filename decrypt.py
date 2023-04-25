# Import de la classe Image de la librairie Pillow
from PIL import Image

def decrypt(encrypted=Image):
    # Recuperer seulement le premier tiers de l'image, seule partie contenant l'image cachée
    encrypted = encrypted.crop((0,0,encrypted.size[0],encrypted.size[1]//3))
    # Creer une nouvelle image qui va contenir la nouvelle image + initialisation de la variable progress pour la barre de progression
    newImage, progress = Image.new("RGB", (encrypted.size[0]//3, encrypted.size[1])), -1
    print("Recuperation en cours, veuillez patienter...")

    # Explorer chaque colonne de l'ancienne image
    for k in range(int(encrypted.size[1])):
        # Afficher la barre de progression
        if k*100//encrypted.size[1]!=progress:
            progress = k*100//encrypted.size[1]
            print("Progression: ["+progress*">"+(100-progress)*" "+"] "+str(progress)+"%", end='\r')
            print(end="\x1b[2K")
        # Explorer une ligne sur trois de chaque colonne de l'ancienne image
        for i in range(0,encrypted.size[0],3):
            # Calculer la position du pixel sur la nouvelle image
            position = (k*newImage.size[0]) + (i//3)
            # Calculer les coordonnées du pixel sur la nouvelle image
            x, y = position//newImage.size[1], position%newImage.size[1]
            # Donne la couleur necessaire aux 3 pixels suivants, pour + d'infos voir le compte rendu
            newImage.putpixel((x,y), (int(str(encrypted.getpixel((i,k))[0])[-1] + str(encrypted.getpixel((i,k))[1])[-1] + str(encrypted.getpixel((i,k))[2])[-1]), int(str(encrypted.getpixel((i+1,k))[0])[-1] + str(encrypted.getpixel((i+1,k))[1])[-1] + str(encrypted.getpixel((i+1,k))[2])[-1]), int(str(encrypted.getpixel((i+2,k))[0])[-1] + str(encrypted.getpixel((i+2,k))[1])[-1] + str(encrypted.getpixel((i+2,k))[2])[-1])))

    # Afficher l'image
    newImage.show()

    print("Recuperation terminée !")

