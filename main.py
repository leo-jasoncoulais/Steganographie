
# Import des librairies necessaires
from os import path
from PIL import Image
from encrypt import encrypt
from decrypt import decrypt

# Demande de  l'action de l'utilisateur et redemander si la valeur entrée est invalide
select = input("Voulez vous cacher une image (h) ou en recuperer une (r) ? ").lower()
while select != "h" and select != "r": select = input("\033[0;31m[!] La valeur entrée est invalide ! Voulez vous cacher une image (h) ou en recuperer une (r) ? \033[0m").lower()

# Si l'utilisateur veut cacher une image
if select == "h":
    # Demander le chemin vers l'image à cacher, et supprimer les ' et " pour que os.path puisse trouver l'image
    little = input("Veuillez renseigner le chemin menant vers l'image à cacher: ").strip()
    little = (little[1:] if little[0] == '"' or little[0] == "'" else little)
    little = (little[:-1] if little[-1] == '"' or little[-1] == "'" else little)
    # Redemander si le chemin est invalide ou n'est pas un PNG ou un JPG
    while not path.exists(little) or (little[-4:] != ".png" and little[-4:] != ".jpg"):
        little = input("\033[0;31m[!] Le chemin rentré est incorrect ou n'est pas une image. Veuillez ressayer: \033[0m").strip()
        little = (little[1:] if little[0] == '"' or little[0] == "'" else little)
        little = (little[:-1] if little[-1] == '"' or little[-1] == "'" else little)
    # Demander le chemin vers l'image modèle, et supprimer les ' et " pour que os.path puisse trouver l'image
    big = input("Veuillez renseigner le chemin menant vers l'image dans laquelle cacher la précedente (image modèle): ").strip()
    big = (big[1:] if big[0] == '"' or big[0] == "'" else big)
    big = (big[:-1] if big[-1] == '"' or big[-1] == "'" else big)
    # Redemander si le chemin est invalide ou n'est pas un PNG ou un JPG
    while not path.exists(big) or (big[-4:] != ".png" and big[-4:] != ".jpg"):
        big = input("\033[0;31m[!] Le chemin rentré est incorrect ou n'est pas une image. Veuillez ressayer: \033[0m").strip()
        big = (big[1:] if big[0] == '"' or big[0] == "'" else big)
        big = (big[:-1] if big[-1] == '"' or big[-1] == "'" else big)
    # Ouvrir les images + initialisation de la variable continueToRUN (plus tard dans le code, savoir si l'utilisateur veut annuler la transformation)
    little, big, continueToRUN = Image.open(little), Image.open(big), True
    
    # Verifier si une image presente un calque Alpha (RGBA)
    if len(little.getpixel((0,0))) == 4 or len(big.getpixel((0,0))) == 4:
        # Verifier si une image n'est pas totalement opaque
        transparenceLittle = False
        transparenceBig = False
        if len(little.getpixel((0,0))) == 4:
            for i in range(little.size[0]):
                for k in range(little.size[1]): transparenceLittle = (True if little.getpixel((i,k))[-1] != 255 else transparenceLittle)
        if len(big.getpixel((0,0))) == 4:
            for i in range(big.size[0]):
                for k in range(big.size[1]): transparenceBig = (True if big.getpixel((i,k))[-1] != 255 else transparenceBig)
        # Si une image n'est pas totalement opaque, le preciser est arreter le programme (une conversion pourrait se montrer problématique)
        if transparenceLittle and transparenceBig: print("\n\033[0;31m[!] Vos images présentent de la transparence, ce qui n'est pas encore supporté par cet outil. Pour palier à ce problème, convertissez vos images en .JPG\033[0m")
        elif transparenceLittle: print("\n\033[0;31m[!] Votre image à cacher présente de la transparence, ce qui n'est pas encore supporté par cet outil. Pour palier à ce problème, convertissez votre image en .JPG\033[0m")
        elif transparenceBig: print("\n\033[0;31m[!] Votre image modèle présente de la transparence, ce qui n'est pas encore supporté par cet outil. Pour palier à ce problème, convertissez votre image en .JPG\033[0m")
        else:
            print("\n\033[0;34m[?] L'une ou plusieurs de vos images présentent de la transparence. Celle ci sera automatiquement convertie lors du processus.\033[0m")
            # Supprimer le calque alpha (CaD convertir l'image RGBA en RGB)
            if len(little.getpixel((0,0))) == 4:
                little.load()
                newLittle = Image.new("RGB", little.size, (255,255,255))
                newLittle.paste(little, mask=little.split()[3])
                little = newLittle.copy()
            if len(big.getpixel((0,0))) == 4:
                big.load()
                newBig = Image.new("RGB", big.size, (255,255,255))
                newBig.paste(big, mask=big.split()[3])
                big = newBig.copy()

    # Initialisation des variables d'informations pour l'utilisateur et l'automatisation des outils d'edition
    if big.size[0]//3 > little.size[0] or big.size[1]//3 > little.size[1]: toCrop, toDebord = "l'image modèle", "l'image à cacher"
    elif big.size[0]//3 < little.size[0] or big.size[1]//3 < little.size[1]: toCrop, toDebord = "l'image à cacher", "l'image modèle"
    else: toCrop, toDebord = None, None

    # Demander a l'utilisateur si il souhaite: redimensionner, rogner, deborder ou annuler
    if little.size[0]*big.size[1]/big.size[0] == int(little.size[0]*big.size[1]/big.size[0]): raccord = input("\n\033[0;34m[?] Le rapport entre les deux images est incorrect. L'image à cacher doit être 3 fois plus petite en longueur et en largeur.\n\n\033[0mQue voulez vous faire: redimensionner (r), rogner (c), deborder (d), annuler (x) ?\n(Redimensioner une image (conseillé) n'affectera pas sa forme, mais peut alterer sa qualité. En cas de debordement (deconseillé), l'image debordée sera "+toDebord+". En cas de rognement (deconseillé), l'image rognée sera "+toCrop+") ").lower()
    elif big.size[0]//3 != little.size[0] or big.size[1]//3 != little.size[1]: raccord = input("\n\033[0;34m[?] Le rapport entre les deux images est incorrect. L'image à cacher doit être 3 fois plus petite en longueur et en largeur.\n\n\033[0mQue voulez vous faire: redimensionner (r), rogner (c), deborder (d), annuler (x) ?\n(Redimensioner une image (deconseillé) affectera sa forme et sa qualité. En cas de debordement (conseillé), l'image debordée sera "+toDebord+". En cas de rognement (deconseillé), l'image rognée sera "+toCrop+") ").lower()
    else: raccord = None, None

    # Redemander si l'entrée est invalide
    while raccord and raccord != "r" and raccord != "c" and raccord != "d" and raccord != "x": raccord = input("\033[0;31m[!] La valeur entrée est invalide ! Voulez vous: redimensionner (r), rogner (c), deborder (d), annuler (x) ? \033[0m").lower()

    # Si l'utilisateur souhaite redimensionner
    if raccord == "r":
        # Demander a l'utilisateur quelle image il souhaite redimensionner et redemander si l'entrée est invalide
        raccord = input("Voulez vous redimensionner l'image à cacher (h) ou l'image modèle (m) ? ").lower()
        while raccord != "h" and raccord != "m": raccord = input("\033[0;31m[!] La valeur entrée est invalide ! Voulez vous redimensionner l'image à cacher (h) ou l'image modèle (m) ? \033[0m").lower()
        # Redimensionner l'image a cacher PUIS l'image modèle pour respecter le bon rapport
        if raccord == "h":
            little = little.resize((big.size[0]//3, big.size[1]//3))
            big = big.resize((little.size[0]*3, little.size[1]*3))
        # Redimensionner l'image modèle
        elif raccord == "m": big = big.resize((little.size[0]*3, little.size[1]*3))

    # Si l'utilisateur souhaite recadrer
    elif raccord == "c":
        # Si il faut recadrer l'image modèle
        if toCrop == "l'image modèle":
            # Recadrer l'image en son centre et la redimensionner
            if big.size[0]//3 > little.size[0]: big = big.crop(( big.size[0]//2 - 3*(little.size[0]//2), 0, big.size[0]//2 + 3*(little.size[0]//2), big.size[0] ))
            if big.size[1]//3 > little.size[1]: big = big.crop(( 0, big.size[1]//2 - 3*(little.size[1]//2), big.size[1], big.size[1]//2 + 3*(little.size[1]//2) ))
            big = big.resize((little.size[0]*3, little.size[1]*3))
        # Si il faut recadrer l'image à cacher
        elif toCrop == "l'image à cacher":
            # Recadrer l'image en son centre et la redimensionner ET redimensionner l'image modèle pour respecter le bon rapport
            if big.size[0]//3 < little.size[0]: little = little.crop(( little.size[0]//2 - 3*big.size[0]//2, 0, little.size[0]//2 + 3*big.size[0]//2, little.size[0] ))
            if big.size[1]//3 < little.size[1]: little = little.crop(( 0, little.size[1]//2 - 3*big.size[1]//2, little.size[1], little.size[1]//2 + 3*big.size[1]//2 ))
            little = little.resize((big.size[0]//3, big.size[1]//3))
            big = big.resize((little.size[0]*3, little.size[1]*3))
    
    # Si l'utilisateur souhaite faire un debordement
    elif raccord == "d":
        # Si il faut deborder l'image à cacher
        if toDebord == "l'image à cacher":
            # Creer une image avec un fond noir de la bonne taille
            newImage = Image.new("RGB", (big.size[0]//3, big.size[1]//3))
            # Coller l'image à cacher au centre de l'image noire
            if big.size[0]//3 > little.size[0] and big.size[1]//3 > little.size[1]: newImage.paste(little, ( newImage.size[0]//2 - little.size[0]//2, newImage.size[1]//2 - little.size[1]//2 ))
            elif big.size[0]//3 > little.size[0]: newImage.paste(little, ( newImage.size[0]//2 - little.size[0]//2, 0 ))
            elif big.size[1]//3 > little.size[1]: newImage.paste(little, ( 0, newImage.size[1]//2 - little.size[1]//2 ))
            little = newImage
            # Redimensionner l'image modèle
            big = big.resize((little.size[0]*3, little.size[1]*3))
        # Si il faut deborder l'image modèle
        if toDebord == "l'image modèle":
            # Creer une image avec un fond noir de la bonne taille
            newImage = Image.new("RGB", (little.size[0]*3, little.size[1]*3))
            # Coller l'image modèle au centre de l'image noire
            if big.size[0]//3 < little.size[0] and big.size[1]//3 < little.size[1]: newImage.paste(big, ( newImage.size[0]//2 - big.size[0]//2, newImage.size[1]//2 - big.size[1]//2 ))
            elif big.size[0]//3 < little.size[0]: newImage.paste(big, ( newImage.size[0]//2 - big.size[0]//2, 0 ))
            elif big.size[1]//3 < little.size[1]: newImage.paste(big, ( 0, newImage.size[1]//2 - big.size[1]//2 ))
            big = newImage

    # Passer la variable continueToRUN à False si l'utilisateur annule la transformation de façon conforme
    elif raccord == "x": continueToRUN = False
    # Si l'utilisateur n'a pas annulé la transformation, envoyer les images à la fonction encrypt
    if continueToRUN: encrypt(little, big)
# Si l'utilisateur veut reveler une image
else:
    # Demander le chemin vers l'image à reveler, et supprimer les ' et " pour que os.path puisse trouver l'image
    encrypted = input("Veuillez renseigner le chemin menant vers l'image à reveler: ").strip()
    encrypted = (encrypted[1:] if encrypted[0] == '"' or encrypted[0] == "'" else encrypted)
    encrypted = (encrypted[:-1] if encrypted[-1] == '"' or encrypted[-1] == "'" else encrypted)
    # Redemander si le chemin est invalide ou n'est pas un PNG ou un JPG
    while not path.exists(encrypted) or (encrypted[-4:] != ".png" and encrypted[-4:] != ".jpg"):
        encrypted = input("\033[0;31m[!] Le chemin rentré est incorrect ou n'est pas une image. Veuillez ressayer: \033[0m").strip()
        encrypted = (encrypted[1:] if encrypted[0] == '"' or encrypted[0] == "'" else encrypted)
        encrypted = (encrypted[:-1] if encrypted[-1] == '"' or encrypted[-1] == "'" else encrypted)
    # Envoyer l'image à la fonction decrypt
    decrypt(Image.open(encrypted))
