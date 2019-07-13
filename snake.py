import random
import pygame

width = 500
rows = 25

class Cube(object):
    rows = rows
    w = width

    def __init__(self, start, dirx=1, diry=0, color=(255, 0, 0)):
        self.pos = start
        self.dirx = 1
        self.diry = 0
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, screen):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(screen, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    if self.dirx == 1 and self.diry == 0:
                        break
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_RIGHT]:
                    if self.dirx == -1 and self.diry == 0:
                        break
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_UP]:
                    if self.dirx == 0 and self.diry == 1:
                        break
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_DOWN]:
                    if self.dirx == 0 and self.diry == -1:
                        break
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_ESCAPE]:
                    return False

        for i, b_part in enumerate(self.body):
            p = b_part.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                b_part.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if b_part.dirx == -1 and b_part.pos[0] <= 0:
                    self.reset((15, 15))
                elif b_part.dirx == 1 and b_part.pos[0] >= b_part.rows - 1:
                    self.reset((15, 15))
                elif b_part.diry == 1 and b_part.pos[1] >= b_part.rows - 1:
                    self.reset((15, 15))
                elif b_part.diry == -1 and b_part.pos[1] <= 0:
                    self.reset((15, 15))
                else:
                    b_part.move(b_part.dirx, b_part.diry)
        return True

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 1
        self.diry = 0

    def add_body_part(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, screen):
        for b_part in self.body:
            b_part.draw(screen)


def redraw_window(screen, sneak, food, font, score):
    screen.fill((0, 0, 0))
    update_score(font, score, screen)
    sneak.draw(screen)
    food.draw(screen)
    pygame.display.update()


def update_food_pos(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def update_score(font, score, screen):
    label = font.render('Score: ' + str(score), True, (0, 255, 0))
    screen.blit(label, (10, 10))


def main():
    score = -1
    flag = True

    sneak = Snake((255, 0, 0), (15, 15))
    food = Cube(update_food_pos(rows, sneak), color=(0, 255, 0))

    pygame.init()
    screen = pygame.display.set_mode((width, width))
    font = pygame.font.Font(None, 25)
    pygame.font.init()
    pygame.display.set_caption('Sneak')
    clock = pygame.time.Clock()

    while flag:
        clock.tick(10 + len(sneak.body))
        sneak_len_score = len(sneak.body)-1
        flag = sneak.move()

        if sneak.body[0].pos == food.pos:
            sneak.add_body_part()
            food = Cube(update_food_pos(rows, sneak), color=(0, 255, 0))

        if score != sneak_len_score:
            score = sneak_len_score
            update_score(font, sneak_len_score, screen)

        for x in range(len(sneak.body)):
            if sneak.body[x].pos in list(map(lambda z: z.pos, sneak.body[x + 1:])):
                sneak.reset((15, 15))
                break
                
        redraw_window(screen, sneak, food, font, sneak_len_score)

    pygame.quit()
    quit()


main()
