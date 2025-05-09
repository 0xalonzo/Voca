import pygame
import sounddevice as sd
import soundfile as sf
from gtts import gTTS
import os

pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("AAC Device")

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)

class Button:
    def __init__(self, x, y, width, height, text, speech_text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.speech_text = speech_text
        self.color = BLUE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def speak(self):
        try:
            # change color of button
            self.color = (0, 200, 0) # green
            pygame.display.flip()  # this might be mkaing the screen flicker
            
            # generate speech
            filename = f"temp_{hash(self.speech_text)}.mp3"
            if not os.path.exists(filename):
                tts = gTTS(text=self.speech_text, lang='en')
                tts.save(filename)
            
            # play audio 
            data, samplerate = sf.read(filename)
            sd.play(data, samplerate)
            
            # visual feedback for 300ms
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 300:
                # process events during wait
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                # keeps button display
                screen.fill(WHITE)
                for btn in buttons:
                    btn.draw(screen)
                pygame.display.flip()
                pygame.time.delay(10)
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # reset colors
            self.color = BLUE
            # redo all buttons
            screen.fill(WHITE)
            for btn in buttons:
                btn.draw(screen)
            pygame.display.flip()

# buttons
buttons = [
    Button(100, 100, 200, 100, "Hello", "Hello, how are you?"),
    Button(400, 100, 200, 100, "Food", "I would like some food."),
    Button(100, 300, 200, 100, "Help", "I need help, please."),
    Button(400, 300, 200, 100, "Yes", "Yes!"),
]

# main
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    # thsi one is complicated
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    button.speak()
    
    # button stuff
    # draw
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(mouse_pos):
            # hover
            pygame.draw.rect(screen, (0, 150, 255), button.rect)
        button.draw(screen)
    
    pygame.display.flip()
    clock.tick(60) # fps  

pygame.quit()