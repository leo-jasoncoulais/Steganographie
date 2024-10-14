from os import path
from PIL import Image
from encrypt import encrypt
from decrypt import decrypt

def sanitize_path(file_path: str) -> str:

    return file_path.strip().strip('"').strip("'")

def validate_image_path(message: str) -> str:

    file_path = sanitize_path(input(message))

    while not path.exists(file_path) or not file_path.lower().endswith(('.png', '.jpg')):
        file_path = sanitize_path(input("\033[0;31m[!] Le chemin est invalide ou n'est pas une image. Veuillez ressayer: \033[0m"))

    return file_path

def check_transparency(image: Image) -> bool:
    return any(image.getpixel((i, j))[-1] != 255 for i in range(image.size[0]) for j in range(image.size[1]))

def handle_transparency(little: Image, big: Image):

    if little.mode == "RGBA":
        if check_transparency(little):
            print("\033[0;31m[!] L'image à cacher contient de la transparence.\033[0m")
        little = little.convert("RGB")

    if big.mode == "RGBA":
        if check_transparency(big):
            print("\033[0;31m[!] L'image modèle contient de la transparence.\033[0m")
        big = big.convert("RGB")

    return little, big

def resize_or_crop_images(little: Image, big: Image) -> tuple:

    if big.size[0] // 3 < little.size[0] or big.size[1] // 3 < little.size[1]:

        action = input("Que voulez-vous faire: redimensionner (r), rogner (c), annuler (x) ? ").lower()

        if action == "r":
            big = big.resize((little.size[0] * 3, little.size[1] * 3))

        elif action == "c":
            big = big.crop((0, 0, little.size[0] * 3, little.size[1] * 3))

        elif action == "x":
            return None, None
        
    return little, big

def main():

    action = input("Voulez-vous cacher une image (h) ou en récupérer une (r) ? ").lower()

    while action not in ['h', 'r']:
        action = input("\033[0;31m[!] Choix invalide ! Choisissez entre cacher (h) ou récupérer (r) : \033[0m").lower()

    if action == 'h':

        little_path = validate_image_path("Chemin de l'image à cacher : ")
        big_path = validate_image_path("Chemin de l'image modèle : ")

        little = Image.open(little_path)
        big = Image.open(big_path)

        little, big = handle_transparency(little, big)
        little, big = resize_or_crop_images(little, big)

        if little and big:
            encrypt(little, big)
            
        else:
            print("\033[0;31m[!] Opération annulée.\033[0m")

    else:
        encrypted_path = validate_image_path("Chemin de l'image à révéler : ")
        decrypt(Image.open(encrypted_path))

if __name__ == "__main__":
    main()
