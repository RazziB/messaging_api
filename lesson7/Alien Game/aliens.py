# קודם מייבאים את הספריה
import pygame
# מאתחלים את הספריה
pygame.init()
# יצירת החלון ושמירתו בתוך משתנה בשם שנבחר
# על הדרך גם נקבע את גודל החלון
win = pygame.display.set_mode((800,600))
# נפתח את קבצי התמונות שבהם נרצה להשתמש
background = pygame.image.load("python/43016/Alien Game/images/background.png")

# יצירת משתנה שיחזיק את הערך 'אמת' עד שנסגור את החלון
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # background פקודה לציור התמונה שנמצאת במשתנה 
    # לתוך הסוגריים אנחנו צריכים להכניס את שם המשתנה, ואת המיקום שבו אנו רוצים שהתמונה תתחיל ממנו 
    win.blit( background, (0,0) )
    # פקודה לעדכון המסך עם כל השינויים שעשינו
    pygame.display.update()
    
   

# פקודה לעצירת החלון של המשחק בסוף
pygame.quit()
