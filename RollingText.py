import pygame
pygame.font.init()


# Rolling dialogues
class RollingText:
    def __init__(self, text, font, pos=(0, 0), color=(0, 0, 0), rolling_speed=0.35):
        self.text = text
        self.font = font
        self.counter = 0
        self.rolling_speed = rolling_speed
        self.drawn_text = ""
        self.over = False
        self.pos = pos
        self.color = color

    def reset(self):
        self.over = False
        self.drawn_text = ""
        self.counter = 0

    def update(self):
        if self.counter <= len(self.text):
            self.drawn_text = self.text[0:int(self.counter)+1]
            self.counter += self.rolling_speed
        else:
            self.over = True

    def draw(self, screen):
        text_surf = self.font.render(self.drawn_text, False, self.color)
        screen.blit(text_surf, self.pos)


class DialogueBoxText:  # Splits the text in two rolling texts
    def __init__(self, text, font, pos=(0,0), color=(0, 0, 0), rolling_speed=0.035):
        text1 = text[:42]
        text2 = text[42:]
        self.rolling_text1 = RollingText(text1, font, pos=pos, color=color, rolling_speed=rolling_speed)
        self.rolling_text2 = RollingText(text2, font, pos=(pos[0], pos[1]+50), color=color, rolling_speed=rolling_speed)
        self.current_text = self.rolling_text1
        self.over = False

    def update(self):
        if self.rolling_text2.over:
            self.over = True
        else:
            self.current_text.update()
            if self.current_text.over and self.current_text != self.rolling_text2:
                self.current_text = self.rolling_text2

    def reset(self):
        self.over = False
        self.rolling_text1.reset()
        self.rolling_text2.reset()
        self.current_text = self.rolling_text1

    def draw(self, screen):
        self.rolling_text1.draw(screen)
        self.rolling_text2.draw(screen)


class Game:
    def __init__(self, rts):
        self.idx = 0
        self.rts = rts
        self.current_text = self.rts[self.idx]

    def update(self, action):
        self.current_text.update()
        if action and self.current_text.over:
            self.idx += 1
        self.current_text = self.rts[self.idx]

    def draw(self, screen):
        self.current_text.draw(screen)


if __name__ == '__main__':
    res = (800, 600)
    screen = pygame.display.set_mode(res)
    play = True
    texts = ["Salut mon vieux, des nouvelles de Ferier ?", "Ca fait un bail que je l'ai pas vu ce chien.",
             "J'espère que tout va bien pour lui"]

    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    rts = [RollingText(t, font) for t in texts]
    game = Game(rts)
    action = False
    txt_dialogue = DialogueBoxText("Salut je fais une longue phrase juste pour tester si tu marches.", font, color=(255, 255, 255), rolling_speed=0.06)

    while play:
        action = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    action = True

        screen.fill((0, 0, 0))
        txt_dialogue.update()
        txt_dialogue.draw(screen)
        #game.update(action)
        #game.draw(screen)
        pygame.display.update()