from io import BytesIO
import numpy as np
from PIL import Image
import FieldClass
import pygame as pg

def afficher_matrice_pygame(image: Image.Image, balls: list[FieldClass.BallClass], field: FieldClass.FieldClass) -> None:
    # Initialiser pygame
    pg.init()

    # Créer une fenêtre
    window = pg.display.set_mode((850, 850))

    last_click_time = 0
    running = True
    while running:
        current_time = pg.time.get_ticks()
        # Charger la nouvelle image avec PIL
        image_pil = image.copy().resize((int(window.get_width()), int(window.get_height())))
        # window.fill((255, 255, 255))
        
        buffer = BytesIO()
        image_pil.save(buffer, format="JPEG")
        buffer.seek(0)
        image_surface = pg.image.load(buffer)

        # Coller la nouvelle image dans la fenêtre
        window.blit(image_surface, (0, 0))
        for ball in balls:
            ball.draw(window, field, window.get_width(), window.get_height())
        # Rafraîchir l'affichage
        pg.display.flip()

        if current_time - last_click_time >= 500:
            last_click_time = current_time
            for ball in balls:
                ball.move(field)
        else:
            progress = (current_time - last_click_time)/500
            for balle in balls:
                balle.old_x = balle.old_x + (balle.x - balle.old_x) * progress
                balle.old_y = balle.old_y + (balle.y - balle.old_y) * progress

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                i = int(mouse_x * field.resolution / window.get_width())
                j = int(mouse_y * field.resolution / window.get_height())
                field.changeVector(i, j)
                image = Image.new('RGB', (field.larg, field.haut), 'white')
                field.draw_field(image)

    # Quitter pygame
    pg.quit()

def main():
    larg = 1000
    haut = 1000
    resolution = 10

    balls = [FieldClass.BallClass(np.random.randint(resolution), np.random.randint(resolution)) for _ in range(1)]

    field = FieldClass.FieldClass(resolution, larg, haut)
    field.remplir_matrice_alea()
    image = Image.new('RGB', (larg, haut), 'white')
    field.draw_field(image)

    image.save('vectorfield.png')
    
    afficher_matrice_pygame(image, balls, field)


main()