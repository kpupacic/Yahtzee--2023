import random
import pygame

pygame.init()

WIDTH = 600
HEIGHT = 850
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('YAHTZEE.KP')
font = pygame.font.Font('freesansbold.ttf', 18)

timer = pygame.time.Clock()
fps = 60    # frames per second

blue = (74, 85, 162)        # glavna boja
light = (120, 149, 203)     # svjetlija plava
lighter = (197, 223, 248)   # jos svjetlija plava
lightest = (229, 242, 255)  # najsvjetlija plava
yellow = (255, 244, 0)      # zuta za oznacavanje stvari
white = (255, 255, 255)
black = (0, 0, 0)

numbers = [0, 0, 0, 0, 0]
roll = False
rolls_left = 3
dice_selected = [False, False, False, False, False]
selected_choice = [False, False, False, False, False, False, False, False, False, False, False, False, False]
possible = [False, False, False, False, False, False, False, False, False, False, False, False, False]
done = [False, False, False, False, False, False, False, False, False, False, False, False, False]
score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
totals = [0, 0, 0, 0, 0, 0, 0]
clicked = -1
current_score = 0
something_selected = False
bonus_time = False
game_over = False

def check_scores(choice_list, numbers_list, possible_list, score):
    active = 0

    for index in range(len(choice_list)):
        if choice_list[index]:
            active = index
    if active == 0:
        current_score = numbers_list.count(1)       # ako kliknemo na polje za jedinice, broji koliko jedinica ima medu kockicama
    elif active == 1:
        current_score = numbers_list.count(2) * 2   # ako kliknemo na polje za duje, broji koliko duja imamo * 2 (zbog ispisa bodova)
    elif active == 2:
        current_score = numbers_list.count(3) * 3   # ...
    elif active == 3:
        current_score = numbers_list.count(4) * 4
    elif active == 4:
        current_score = numbers_list.count(5) * 5
    elif active == 5:
        current_score = numbers_list.count(6) * 6
    elif active == 6 or active == 7:                # ako kliknemo na tris/poker
        if possible_list[active]:
            current_score = sum(numbers_list)
        else:
            current_score = 0
    elif active == 8:
        if possible_list[active]:
            current_score = 25
        else:
            current_score = 0
    elif active == 9:
        if possible_list[active]:
            current_score = 40
        else:
            current_score = 0
    elif active == 10:
        if possible_list[active]:
            current_score = 50
        else:
            current_score = 0
    elif active == 11:
        current_score = sum(numbers_list)

    return current_score

def draw_stuff():
    global rolls_left
    global game_over
    if game_over:
        over_text = font.render('Game over: Click to restart!', True, white)
        screen.blit(over_text, (280, 290))
    roll_text = font.render('Click to roll', True, lighter)
    screen.blit(roll_text, (70, 180))   # ispisiva roll_text na ekran na odredenu poziciju
    accept_text = font.render('Accept turn', True, lighter)
    screen.blit(accept_text, (370, 180))
    rolls_text = font.render('Rolls left this turn: ' + str(rolls_left), True, lighter)
    screen.blit(rolls_text, (15, 15))
    instructions_text = font.render('Click a die to keep it or release!', True, lighter)
    screen.blit(instructions_text, (280, 15))
    pygame.draw.rect(screen, lightest, [0, 225, 235, HEIGHT - 265])
    pygame.draw.line(screen, light, (0, 40), (WIDTH, 40), 3)    # crta koja odvaja tekst "rolls left this turn" i kockice
    pygame.draw.line(screen, light, (0, 218), (WIDTH, 218), 3)  # crta koja odvaja kockice i tablicu za popunjavanje
    pygame.draw.line(screen, light, (155, 225), (155, HEIGHT - 40), 3)
    pygame.draw.line(screen, light, (233, 225), (233, HEIGHT - 40), 3)

class Dice:     # stvaranje kockica
    def __init__(self, x_pos, y_pos, num, key):
        global dice_selected
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.number = num   # vrijednost kockice
        self.key = key      # za dodavanje kockica u listu
        self.die = ''
        self.selected = dice_selected[key]

    def draw(self):
        self.die = pygame.draw.rect(screen, white, [self.x_pos, self.y_pos, 100, 100], 0, 5)    # draw.rect --> crta se rectangle: na sta, boja, di, velicina, solid, rounded edges
        # crtamo "brojeve" na kockicama, jednu po jednu
        if self.number == 1:
            pygame.draw.circle(screen, black, (self.x_pos + 50, self.y_pos + 50), 10) # + 50 --> centriranje u sredinu kockice, 10 --> radijus tockice
        if self.number == 2:
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 80), 10)
        if self.number == 3:
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 50, self.y_pos + 50), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 80), 10)
        if self.number == 4:
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 80), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 80), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 20), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 20), 10)
        if self.number == 5:
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 80), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 80), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 20), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 50, self.y_pos + 50), 10)
        if self.number == 6:
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 50), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 20, self.y_pos + 80), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 20), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 50), 10)
            pygame.draw.circle(screen, black, (self.x_pos + 80, self.y_pos + 80), 10)
        if self.selected:
            self.die = pygame.draw.rect(screen, yellow, [self.x_pos, self.y_pos, 100, 100], 4, 5)
    
    def check_click(self, coordinates):
        if self.die.collidepoint(coordinates):
            if dice_selected[self.key]:
                dice_selected[self.key] = False
            elif not dice_selected[self.key]:
                dice_selected[self.key] = True

class Choice:       # stvaranje tablice za upisivanje bodova
    def __init__(self, x_pos, y_pos, text, select, possible, done, score):     # select --> ?, possible --> je li moguce upisat na to misto, done --> je li gotovo s upisivanjem
        global selected_choice
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.select = select
        self.possible = possible
        self.done = done
        self.score = score

    def draw(self):
        pygame.draw.line(screen, light, (self.x_pos, self.y_pos), (self.x_pos + 225, self.y_pos), 2)                # gornja crta (koja razdvaja) neke opcije
        pygame.draw.line(screen, light, (self.x_pos, self.y_pos + 30), (self.x_pos + 225, self.y_pos + 30), 2)      # donja, zadnja crta (za zadnju opciju), jer se inace samo gornje vide
        if not self.done:               # ako jos nisu upisani bodovi
            if self.possible:           # ako je moguce upisati
                my_text = font.render(self.text, True, blue)
            elif not self.possible:     # ako nije moguce upisati
                my_text = font.render(self.text, True, light)
        else:
            my_text = font.render(self.text, True, blue)
        if self.select:
            pygame.draw.rect(screen, white, [self.x_pos, self.y_pos, 155, 30])
        screen.blit(my_text, (self.x_pos + 7, self.y_pos + 8))
        score_text = font.render(str(self.score), True, blue)
        screen.blit(score_text, (self.x_pos + 165, self.y_pos + 10))

def check_possibilities(possible_list, numbers_list):
    possible_list[0] = True
    possible_list[1] = True
    possible_list[2] = True
    possible_list[3] = True
    possible_list[4] = True
    possible_list[5] = True
    possible_list[11] = True
    max_count = 0               # koliko se puta ponavlja broj koji se najvise puta pojavljuje

    for index in range(1, 7):   # u pythonu for petlje idu od prvog broja, ali zadnjeg ne badaju (znaci ide od 1 do 6)
        if numbers_list.count(index + 1) > max_count:
            max_count = numbers_list.count(index + 1)

    if max_count < 3:               # ako imamo manje od 3 ista broja...
        possible_list[6] = False    # ...tris nije moguc
        possible_list[7] = False    # ...poker nije moguc
        possible_list[8] = False    # ...itd
        possible_list[10] = False
    elif max_count == 3:
        possible_list[6] = True
        possible_list[7] = False
        possible_list[10] = False
        checker = False
        for index in range(len(numbers_list)):
            if numbers_list.count(numbers_list[index]) == 2:
                possible_list[8] = True     # full je moguc
                possible_list[6] = False    # ali tris nije moguc
                checker = True
        if not checker:
            possible_list[8] = False
    elif max_count == 4:
        possible_list[6] = False
        possible_list[7] = True
        possible_list[10] = False
    elif max_count == 5:
        possible_list[6] = False
        possible_list[7] = False
        possible_list[10] = True

    # sad provjera za skalu, ja msn da ja ovo mogu puno lipse napisat
    lowest = 10
    for index in range(len(numbers_list)):
        if numbers_list[index] < lowest:
            lowest = numbers_list[index]
    if (lowest + 1 in numbers_list) and (lowest + 2 in numbers_list) and (lowest + 3 in numbers_list) and (lowest + 4 in numbers_list):
        possible_list[9] = True
    else:
        possible_list[9] = False

    return possible_list

def make_choice(clicked_num, selected, done_list):

    for index in range(len(selected)):
        selected[index] = False
    if not done_list[clicked_num]:
        selected[clicked_num] = True

    return selected

def check_totals(totals_list, score_list, bonus):
    
    totals_list[0] = score_list[0] + score_list[1] + score_list[2] + score_list[3] + score_list[4] + score_list[5]
    if totals_list[0] >= 60:
        totals_list[1] = 35
    else:
        totals_list[1] = 0
    totals_list[2] = totals_list[1] + totals_list[0]
    if bonus:
        totals_list[3] += 100
        bonus = False
    totals_list[4] = score_list[7] + score_list[8] + score_list[9] + score_list[10] + score_list[11] + totals_list[3]
    totals_list[5] = totals_list[2]
    totals_list[6] = totals_list[4] + totals_list[5]

    return totals_list, bonus

def restart_function():
    global numbers
    global roll
    global rolls_left
    global dice_selected
    global selected_choice
    global possible
    global done
    global totals
    global clicked
    global current_score
    global something_selected
    global bonus_time
    global game_over
    global score
    numbers = [0, 0, 0, 0, 0]
    roll = False
    rolls_left = 3
    dice_selected = [False,  False, False, False, False]
    selected_choice = [False, False, False, False, False, False, False, False, False, False, False, False, False]
    possible = [False, False, False, False, False, False, False, False, False, False, False, False, False]
    done = [False, False, False, False, False, False, False, False, False, False, False, False, False]
    score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    totals = [0, 0, 0, 0, 0, 0, 0]
    clicked = -1
    current_score = 0
    something_selected = False
    bonus_time = False
    game_over = False

running = True
while running:
    timer.tick(fps)
    screen.fill(blue)
    if game_over:
        restart_button = pygame.draw.rect(screen, light, [275, 275, 280, 30])
    roll_button = pygame.draw.rect(screen, light, [10, 170, 220, 40])
    accept_button = pygame.draw.rect(screen, light, [310, 170, 220, 40])
    
    die1 = Dice(10, 50, numbers[0], 0)
    die2 = Dice(130, 50, numbers[1], 1)
    die3 = Dice(250, 50, numbers[2], 2)
    die4 = Dice(370, 50, numbers[3], 3)
    die5 = Dice(490, 50, numbers[4], 4)

    ones = Choice(0, 230, '1s', selected_choice[0], possible[0], done[0], score[0])
    twos = Choice(0, 260, '2s', selected_choice[1], possible[1], done[1], score[1])
    threes = Choice(0, 290, '3s', selected_choice[2], possible[2], done[2], score[2])
    fours = Choice(0, 320, '4s', selected_choice[3], possible[3], done[3], score[3])
    fives = Choice(0, 350, '5s', selected_choice[4], possible[4], done[4], score[4])
    sixes = Choice(0, 380, '6s', selected_choice[5], possible[5], done[5], score[5])
    
    upper_total1 = Choice(0, 410, 'Upper score', False, False, True, totals[0])
    upper_bonus = Choice(0, 440, 'Bonus if >=60', False, False, True, totals[1])
    
    upper_total2 = Choice(0, 470, 'Upper total', False, False, True, totals[2])
    three_kind = Choice(0, 500, 'Tris', selected_choice[6], possible[6], done[6], score[6])
    four_kind = Choice(0, 530, 'Poker', selected_choice[7], possible[7], done[7], score[7])
    full_house = Choice(0, 560, 'Full', selected_choice[8], possible[8], done[8], score[8])
    straight = Choice(0, 590, 'Straight', selected_choice[9], possible[9], done[9], score[9])
    yahtzee = Choice(0, 620, 'Yahtzee!', selected_choice[10], possible[10], done[10], score[10])
    chance = Choice(0, 650, 'Chance', selected_choice[11], possible[11], done[11], score[11])
    
    bonus = Choice(0, 680, 'Yahtzee bonus', False, False, True, totals[3])
    lower_total1 = Choice(0, 710, 'Lower total', False, False, True, totals[4])
    lower_total2 = Choice(0, 740, 'Upper total', False, False, True, totals[5])
    grand_total = Choice(0, 770, 'Grand total', False, False, True, totals[6])

    possible = check_possibilities(possible, numbers)
    current_score = check_scores(selected_choice, numbers, possible, score)
    totals, bonus_time = check_totals(totals, score, bonus_time)

    if True in selected_choice:
        something_selected = True

    draw_stuff()
    die1.draw()
    die2.draw()
    die3.draw()
    die4.draw()
    die5.draw()
    ones.draw()
    twos.draw()
    threes.draw()
    fours.draw()
    fives.draw()
    sixes.draw()
    upper_total1.draw()
    upper_bonus.draw()
    upper_total2.draw()
    three_kind.draw()
    four_kind.draw()
    full_house.draw()
    straight.draw()
    yahtzee.draw()
    chance.draw()
    bonus.draw()
    lower_total1.draw()
    lower_total2.draw()
    grand_total.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     # prekidamo igru
        if event.type == pygame.MOUSEBUTTONDOWN:    # ako kliknemo na ... dogodi se ...
            if game_over and restart_button.collidepoint(event.pos):
                restart_function()
                game_over = False
            die1.check_click(event.pos)
            die2.check_click(event.pos)
            die3.check_click(event.pos)
            die4.check_click(event.pos)
            die5.check_click(event.pos)
            if 0 <= event.pos[0] <= 155:
                if 230 <= event.pos[1] <= 410 or 500 <= event.pos[1] <= 680:
                    if 230 < event.pos[1] < 260:
                        clicked = 0
                    elif 260 < event.pos[1] < 290:
                        clicked = 1
                    elif 290 < event.pos[1] < 320:
                        clicked = 2
                    elif 320 < event.pos[1] < 350:
                        clicked = 3
                    elif 350 < event.pos[1] < 380:
                        clicked = 4
                    elif 380 < event.pos[1] < 410:
                        clicked = 5
                    elif 500 < event.pos[1] < 530:
                        clicked = 6
                    elif 530 < event.pos[1] < 560:
                        clicked = 7
                    elif 560 < event.pos[1] < 590:
                        clicked = 8
                    elif 590 < event.pos[1] < 620:
                        clicked = 9
                    elif 620 < event.pos[1] < 650:
                        clicked = 10
                    elif 650 < event.pos[1] < 680:
                        clicked = 11
                    selected_choice = make_choice(clicked, selected_choice, done)
            if roll_button.collidepoint(event.pos) and rolls_left > 0:
                roll = True
                rolls_left -= 1
            if accept_button.collidepoint(event.pos) and something_selected and rolls_left < 3:
                if score[10] == 50 and done[10] and possible[10]:
                    bonus_time = True
                for i in range(len(selected_choice)):
                    if selected_choice[i]:
                        done[i] = True
                        score[i] = current_score
                        selected_choice[i] = False
                    for i in range(len(dice_selected)):
                        dice_selected[i] = False
                    numbers = [7, 18, 29, 30, 41]
                    something_selected = False
                    rolls_left = 3

    if roll:
        for number in range(len(numbers)):  # dodjeljujemo vrijednosti kockicama
            if not dice_selected[number]:
                numbers[number] = random.randint(1, 6)
        roll = False

    pygame.display.flip()
pygame.quit()