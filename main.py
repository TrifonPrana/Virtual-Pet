import pygame as pg
import json
import random

pg.init()

#Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

ICON_SIZE = 80

DOG_WIDTH = 310
DOG_HEIGHT = 500

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

FOOD_SIZE = 200
TOY_SIZE = 100

GRID = 10

FPS = 60

new_game_data = {
    "happiness": 50,
    "satiety": 30,
    "health": 100,
    "money": 15,
    "coins_per_second": 1,
    "coins_per_click": 1,
    "points_record": 0,
    "costs_of_upgrade": {
        "100": False,
        "1000": False,
        "5000": False,
        "10000": False
    },
    "clothes": [
        {
            "name": "Синяя футболка",
            "price": 20,
            "image": "images/items/blue t-shirt.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Красная футболка",
            "price": 20,
            "image": "images/items/red t-shirt.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Желтая футболка",
            "price": 20,
            "image": "images/items/yellow t-shirt.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Ботинки",
            "price": 30,
            "image": "images/items/boots.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Шляпа",
            "price": 40,
            "image": "images/items/hat.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Бантик",
            "price": 25,
            "image": "images/items/bow.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Кепка",
            "price": 35,
            "image": "images/items/cap.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Солнцезащитные очки",
            "price": 35,
            "image": "images/items/sunglasses.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Серебряная цепочка",
            "price": 70,
            "image": "images/items/silver chain.png",
            "is_using": False,
            "is_bought": False
        },
        {
            "name": "Золотая цепочка",
            "price": 125,
            "image": "images/items/gold chain.png",
            "is_using": False,
            "is_bought": False
        }
    ]
}

icon = pg.image.load("images/toys/blue bone.png")
pg.display.set_icon(icon)

font = pg.font.Font(None,40)
font_mini = pg.font.Font(None,33)
font_max = pg.font.Font(None,200)

def load_image(file,width,height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image,(width,height))
    return image 
def text_render(text):
    return font.render(str(text),True,"black")

class Button:
    def __init__(self,text,x,y,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,text_font=font,func=None):
        self.func=func

        self.image = load_image("images/button.png",width,height)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.text_font = text_font
        self.text = self.text_font.render(str(text),True,"black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        screen.blit(self.text,self.text_rect)
    def is_clicked(self,event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.func()

class Clothes_Menu:
    def __init__(self,game,data):
        self.game = game

        self.menu_page = load_image("images/menu/menu_page.png",SCREEN_WIDTH,SCREEN_HEIGHT)

        self.items = []

        for item in data: 
            item_object = Item(item["name"],item["price"],item["image"],item["is_using"],item["is_bought"])
            self.items.append(item_object)

        self.current_item = 0

        self.render_item()
        
        #Создаем кнопки
        self.next_button = Button("Вперед",SCREEN_WIDTH - BUTTON_WIDTH - GRID*8,SCREEN_HEIGHT - GRID*14
        ,width=BUTTON_WIDTH//1.2,height=BUTTON_HEIGHT//1.2,func=self.to_next)

        self.back_button = Button("Назад",GRID*12,SCREEN_HEIGHT - GRID*14
        ,width=BUTTON_WIDTH//1.2,height=BUTTON_HEIGHT//1.2,func=self.to_previous)

        

        self.buy_button = Button("Купить",SCREEN_WIDTH//2 - BUTTON_WIDTH//1.5 // 2,SCREEN_HEIGHT//2 + GRID*10
        ,width=BUTTON_WIDTH//1.5,height=BUTTON_HEIGHT//1.5,func=self.buy)

        
        self.bottom_width = SCREEN_WIDTH+10
        self.bottom_label_off = load_image("images/menu/bottom_label_off.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png",SCREEN_WIDTH,SCREEN_HEIGHT)

    def to_next(self):
        if self.current_item +1 != len(self.items):
            self.current_item +=1
            self.render_item()
    
    def to_previous(self):
        if not self.current_item -1 <0:
            self.current_item -=1
            self.render_item()
    def buy(self):
        if self.items[self.current_item].is_bought != True:
            if self.game.money >= self.items[self.current_item].price: 
                self.items[self.current_item].is_bought = True
                self.game.money -= self.items[self.current_item].price
    def use(self):
        if self.items[self.current_item].is_bought:
            self.items[self.current_item].is_using = not self.items[self.current_item].is_using
            print(self.items[self.current_item].is_using)
    def render_item(self):
        self.item_rect = self.items[self.current_item].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2,SCREEN_HEIGHT // 2)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH//2,GRID*18)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH//2,GRID*12)

    def draw(self,screen):  
        screen.blit(self.menu_page,(0,0))

        screen.blit(self.items[self.current_item].image,self.item_rect)

        screen.blit(self.name_text,self.name_text_rect)
        screen.blit(self.price_text,self.price_text_rect)

        self.next_button.draw(screen)
        self.back_button.draw(screen)

        self.buy_button.draw(screen)
        self.prepare_button()
        self.use_button.draw(screen)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on,(0, 0))
        else:
            screen.blit(self.bottom_label_off,(0, 0))
        if self.items[self.current_item].is_bought:
            screen.blit(self.top_label_on,(0, 0))   
        else:
            screen.blit(self.top_label_off,(0, 0))

        self.prepare_labels_text()

        screen.blit(self.buy_text,self.buy_text_rect)
        screen.blit(self.use_text,self.use_text_rect)
    def prepare_button(self):
        if self.items[self.current_item].is_using == True:
            self.use_button_text = "Снять"
        elif self.items[self.current_item].is_using == False:
            self.use_button_text = "Надеть"

        self.use_button = Button(self.use_button_text,GRID*12,SCREEN_HEIGHT//2 + GRID*8
        ,width=BUTTON_WIDTH//1.2,height=BUTTON_HEIGHT//1.2,func=self.use)
    def prepare_labels_text(self):
        if self.items[self.current_item].is_using != True:
            self.preparing_use_text = "Не надето"
        elif self.items[self.current_item].is_using == True:
            self.preparing_use_text = "Надето"
        if self.items[self.current_item].is_bought != True:
            self.preparing_buy_text = "Не куплено"
        elif self.items[self.current_item].is_bought == True:
            self.preparing_buy_text = "Куплено"
    
        self.use_text = font_mini.render(self.preparing_use_text,True,"black")
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.center = (SCREEN_WIDTH - GRID*20,GRID*13)

        self.buy_text = font_mini.render(self.preparing_buy_text,True,"black")
        self.buy_text_rect = self.buy_text.get_rect()
        self.buy_text_rect.center = (SCREEN_WIDTH - GRID*20,GRID*20)
class Item:
    def __init__(self,name,price,file,is_bought,is_using):
        self.name = name
        self.price = price
        self.file = file
        self.image = load_image(file,DOG_WIDTH//1.7,DOG_HEIGHT//1.7)
        self.is_using = is_using
        self.is_bought = is_bought

        self.full_image = load_image(file,DOG_WIDTH,DOG_HEIGHT)
      

class Food_Menu:
    def __init__(self,game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png",SCREEN_WIDTH,SCREEN_HEIGHT)

        self.items = [Food("Яблоко",15,"images/food/apple.png",5),
                        Food("Мясо",40,"images/food/meat.png",15),
                        Food("Косточка",45,"images/food/bone.png",15,fun_power=10),
                        Food("Корм",65,"images/food/dog food.png",25),
                        Food("Элитный корм",115,"images/food/dog food elite.png",50,medicine_power=5),
                        Food("Лекарство",225,"images/food/medicine.png",25,medicine_power = 20)
                    ]      
        
        self.current_item = 0
        
        self.render_item()
        #Создаем кнопки
        self.next_button = Button("Вперед",SCREEN_WIDTH - BUTTON_WIDTH - GRID*8,SCREEN_HEIGHT - GRID*14
        ,width=BUTTON_WIDTH//1.2,height=BUTTON_HEIGHT//1.2,func=self.to_next)

        self.back_button = Button("Назад",GRID*12,SCREEN_HEIGHT - GRID*14
        ,width=BUTTON_WIDTH//1.2,height=BUTTON_HEIGHT//1.2,func=self.to_previous)

        

        self.buy_eat_button = Button("Купить",SCREEN_WIDTH//2 - BUTTON_WIDTH//1.5 // 2,SCREEN_HEIGHT//2 + GRID*10
        ,width=BUTTON_WIDTH//1.5,height=BUTTON_HEIGHT//1.5,func=self.buy_eat)
    def to_next(self):
        if self.current_item +1 != len(self.items):
            self.current_item +=1
            self.render_item()
    def to_previous(self):
        if not self.current_item -1 <0:
            self.current_item -=1
            self.render_item()

    def render_item(self):
        self.item_rect = self.items[self.current_item].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2,SCREEN_HEIGHT // 2)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH//2,GRID*18)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH//2,GRID*12)

        self.satiety_text = text_render(f"Даст сытости:{self.items[self.current_item].satiety}")
        self.satiety_text_rect = self.satiety_text.get_rect()
        self.satiety_text_rect.center = (SCREEN_WIDTH//2,GRID*43)

        self.medicinepower_text = text_render(f"Добавит {self.items[self.current_item].medicine_power} здоровья.")
        self.medicinepower_text_rect = self.medicinepower_text.get_rect()
        self.medicinepower_text_rect.center = (SCREEN_WIDTH//2,GRID*46)

        self.funpower_text = text_render(f"Добавит {self.items[self.current_item].fun_power} веселья.")
        self.funpower_text_rect = self.funpower_text.get_rect()
        self.funpower_text_rect.center = (SCREEN_WIDTH//2,GRID*46)
        
    def draw(self,screen):  
        screen.blit(self.menu_page,(0,0))

        screen.blit(self.items[self.current_item].image,self.item_rect)

        screen.blit(self.name_text,self.name_text_rect)
        screen.blit(self.price_text,self.price_text_rect)
        # screen.blit(self.satiety_number_text,self.satiety_number_text_rect)
        screen.blit(self.satiety_text,self.satiety_text_rect)
        if self.items[self.current_item].name == "Лекарство" or self.items[self.current_item].name == "Элитный корм":
            screen.blit(self.medicinepower_text,self.medicinepower_text_rect)
        if self.items[self.current_item].name == "Косточка":
            screen.blit(self.funpower_text,self.funpower_text_rect)

        self.next_button.draw(screen)
        self.back_button.draw(screen)

        self.buy_eat_button.draw(screen)
    def buy_eat(self):
        if self.game.money >= self.items[self.current_item].price: 
            self.game.satiety += self.items[self.current_item].satiety
            self.game.health += self.items[self.current_item].medicine_power
            self.game.happiness += self.items[self.current_item].fun_power

            self.game.money -= self.items[self.current_item].price
class Food:
    def __init__(self,name,price,image,satiety,medicine_power=0,fun_power=0):
        self.name = name
        self.price = price
        self.image = image
        self.satiety = satiety
        self.medicine_power = medicine_power
        self.fun_power = fun_power
        self.image = load_image(image,FOOD_SIZE,FOOD_SIZE)

class Upgrades_Menu:
    def __init__(self,game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png",SCREEN_WIDTH,SCREEN_HEIGHT)

        self.current_item = 0

        self.items = ["+1 за клик","+10 за клик"]
        #Создаем кнопки
        self.next_button = Button("Вперед",SCREEN_WIDTH - BUTTON_WIDTH - GRID*8,SCREEN_HEIGHT - GRID*14
        ,width=BUTTON_WIDTH//1.2,height=BUTTON_HEIGHT//1.2,func=self.to_next)

        self.back_button = Button("Назад",GRID*12,SCREEN_HEIGHT - GRID*14
        ,width=BUTTON_WIDTH//1.2,height=BUTTON_HEIGHT//1.2,func=self.to_previous)
    def draw(self,screen):  
            screen.blit(self.menu_page,(0,0))
    def to_next(self):
        if self.current_item +1 != len(self.items):
            self.current_item +=1
            self.render_item()
    def to_previous(self):
        if not self.current_item -1 <0:
            self.current_item -=1
            self.render_item()

class Game_Menu:
    def __init__(self,game):
        self.game = game
        self.game_bg = load_image("images/game_background.png",SCREEN_WIDTH,SCREEN_HEIGHT) 

        self.points = 0
        self.points_text = text_render(f"Очки: {self.points}.")
        self.points_text_rect = self.points_text.get_rect()
        self.points_text_rect.center = (GRID*70,GRID*10)

        self.points_record = 0
        self.points_record_text = text_render(f"Рекорд: {self.points_record}.")
        self.points_record_text_rect = self.points_text.get_rect()
        self.points_record_text_rect.center = (GRID*69.5,GRID*12.5)

        self.boom = load_image("images/toys/boom.png",TOY_SIZE,TOY_SIZE)
    def draw(self,screen):
        screen.blit(self.game_bg,(0, 0))

        self.points_text = text_render(f"Очки: {self.points}.")
        screen.blit(self.points_text,self.points_text_rect)

        self.points_record_text = text_render(f"Рекорд: {self.points_record}.")
        screen.blit(self.points_record_text,self.points_record_text_rect)
        
        self.game.dog.draw(screen)
        self.game.dog.update()

        if random.randint(1,100) <= 4:
            self.game.toy_bones.add(Toy())
        
        self.game.toy_bones.draw(screen)
        self.game.toy_bones.update()

        if pg.sprite.spritecollide(self.game.dog,self.game.toy_bones,True,pg.sprite.collide_rect_ratio(0.6)):
            self.points +=1
            self.game.happiness +=1
            self.points_text = text_render(f"Очки: {self.points}.")


        if self.points >= self.points_record:
            self.points_record=self.points


        if random.randint(1,200) >=199:
            self.game.bomb.add(Bomb())
        self.game.bomb.draw(screen)
        self.game.bomb.update()
        if pg.sprite.spritecollide(self.game.dog,self.game.bomb,True,pg.sprite.collide_rect_ratio(0.6)):
            self.game.money += self.points //2
            self.points = 0
            self.points_text = text_render(f"Очки: {self.points}.")
class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        file = random.choice(["images/toys/ball.png","images/toys/red bone.png","images/toys/blue bone.png"])

        self.image =load_image(file,TOY_SIZE,TOY_SIZE)
        self.rect= self.image.get_rect()

        self.rect.x = random.randint(GRID*9,SCREEN_WIDTH - GRID*23)
        self.rect.y = 30
    def update(self):
        if self.rect.y +2 <= 400:
            self.rect.y += 2
        else:
            self.kill()
    def draw(self,screen):
        screen.blit(self.image,self.rect)
class Bomb(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image =load_image("images/toys/bomb.png",TOY_SIZE,TOY_SIZE)
        self.rect= self.image.get_rect()

        self.rect.x = random.randint(GRID*9,SCREEN_WIDTH - GRID*23)
        self.rect.y = 30
    def update(self):
        if self.rect.y +2 <= 400:
            self.rect.y += 2
        else:
            self.kill()
    def draw(self,screen):
        if not pg.sprite.spritecollide(self.game.dog,self.game.bomb,True,pg.sprite.collide_rect_ratio(0.6)):
            self.image =load_image("images/toys/bomb.png",TOY_SIZE,TOY_SIZE)
        else:
            self.image =load_image("images/toys/boom.png",TOY_SIZE,TOY_SIZE)
        self.rect = self.image.get_rect()
        screen.blit(self.image,self.rect)
    def boom(self,screen):
        self.image =load_image("images/toys/boom.png",TOY_SIZE,TOY_SIZE)
        self.rect = self.image.get_rect()
        screen.blit(self.image,self.rect)
class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = load_image("images/dog.png",DOG_WIDTH//2,DOG_HEIGHT//2)
        self.rect = self.image.get_rect()

        self.rect.centerx = SCREEN_WIDTH//2
        self.rect.centery = SCREEN_HEIGHT - GRID*14
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_RIGHT] and self.rect.x +3<=671:
            self.rect.x +=3
            #print(self.rect.y)
        if keys[pg.K_d] or keys[pg.K_LEFT] and self.rect.x -3>=86:
            self.rect.x -=3
            #print(self.rect.x)
    def draw(self,screen):
        screen.blit(self.image,self.rect)


class Game:
    def __init__(self):
        #Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.mode = "Main"
        pg.display.set_caption("Виртуальный питомец")

        # data=new_game_data
        self.play_menu = Game_Menu(self)
        with open("save.json","r",encoding="utf-8") as f:
            data =json.load(f)
            self.happiness = data["happiness"]
            self.health = data["health"]
            self.satiety = data["satiety"]
            self.money = data["money"]
            self.play_menu.points_record = data["points_record"]
            self.coins_per_second = data["coins_per_second"]
            self.coins_per_click = data["coins_per_click"]
        #Загрузка фона и иконок
        self.background = load_image("images/background.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.happines_image = load_image('images/happiness.png',ICON_SIZE,ICON_SIZE)
        self.health_image = load_image('images/health.png',ICON_SIZE,ICON_SIZE)
        self.satiety_image = load_image('images/satiety.png',ICON_SIZE,ICON_SIZE)
        self.money_image = load_image("images/money.png",ICON_SIZE,ICON_SIZE)
        #Загрузка изображений для виртуального инопланетного чудовища
        self.body = load_image("images/dog.png",DOG_WIDTH,DOG_HEIGHT)
        #Загрузка лиц
        self.happy_face = load_image("images/happy_face.png",DOG_WIDTH,DOG_HEIGHT)
        self.sad_face = load_image("images/sad_face.png",DOG_WIDTH,DOG_HEIGHT)
        self.sick_face = load_image("images/sick_face.png",DOG_WIDTH,DOG_HEIGHT)

        self.button_x = SCREEN_WIDTH - BUTTON_WIDTH - GRID

        self.eat_button = Button("Еда",self.button_x,GRID*9,func=self.eat_menu_on)
        self.clothes_button = Button("Одежда",self.button_x,GRID*10+BUTTON_HEIGHT,func=self.clothes_menu_on)
        self.play_button = Button("Игры",self.button_x,GRID*11+BUTTON_HEIGHT * 2,func=self.play_menu_on)
        self.upgrades_button = Button("Улучшения",self.button_x,GRID*24+BUTTON_HEIGHT,func=self.upgrades_menu_on)

        #Создаем объекты для меню 
        self.clothes_menu = Clothes_Menu(self,data["clothes"])
        self.food_menu = Food_Menu(self)

        self.upgrades_menu = Upgrades_Menu(self)
        #Создаем объекты для собачки и игрушек
        self.dog = Dog()
        self.toy_bones = pg.sprite.Group()
        self.bomb = pg.sprite.Group()
        #Создание событий для кликера
        self.INCREASE_COINS=pg.USEREVENT +1
        pg.time.set_timer(self.INCREASE_COINS,1000)

        self.DECREASE = pg.USEREVENT+2
        pg.time.set_timer(self.DECREASE,1000)

        self.clock = pg.time.Clock()
        self.run()
    def clothes_menu_on(self):
        self.mode = "Clothes menu"
        print(self.mode)
        self.clothes_menu.draw(self.screen)
    def eat_menu_on(self):
        self.mode = "Food menu"
        print(self.mode)
        self.food_menu.draw(self.screen)
    def upgrades_menu_on(self):
        self.mode = "Upgrades menu"
        print(self.mode)
        self.upgrades_menu.draw(self.screen)
    def play_menu_on(self):
        self.mode = "Play menu"
        print(self.mode)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == "Game over":
                    data = new_game_data

                    with open("save.json", "w", encoding="utf8") as json_file:
                        json.dump(data, json_file, ensure_ascii=False,indent=4)
                else:
                    data = {"happiness": self.happiness,
                            "satiety": self.satiety,
                            "health": self.health,
                            "money": self.money,
                            "coins_per_second":self.coins_per_second,
                            "coins_per_click":self.coins_per_click,
                            "points_record":self.play_menu.points_record,
                            "clothes":[]
                    }

                    for item in self.clothes_menu.items:
                        data["clothes"].append({"name": item.name,
                                                "price": item.price,
                                                "image": item.file,
                                                "is_using": item.is_using,
                                                "is_bought": item.is_bought})
                    with open("save.json", "w", encoding="utf8") as json_file:
                        json.dump(data, json_file, ensure_ascii=False,indent=4)
                pg.quit()   
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.play_menu.points = 0
                    # self.points_text = text_render(f"Очки: {self.play_menu.points}.")
                    # screen.blit(self.points_text,self.points_text_rect)
                    self.mode = "Main"
            if event.type == self.INCREASE_COINS:
                self.money +=self.coins_per_second
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.mode != "Play menu":
                self.money += self.coins_per_click
            if event.type == self.DECREASE:
                if random.randint(0,100) >= 25:
                    chance = random.randint(1,120)
                    if chance <= 65:   
                        self.happiness -= 1
                    elif 100>= chance: 
                        self.satiety -= 2
                    if self.satiety <= 5:
                        if random.randint(0,100) >= 35:
                            self.health -= random.randint(1,3)
                    elif self.satiety >= 50 and self.health <=45:
                        if random.randint(0,100) >= 20:
                            self.health +=random.randint(2,5)
                    if self.health <= 30:
                        if random.randint(0,100) >= 35:
                            self.happiness -= random.randint(2,5)

            if self.mode == "Main":
                self.clothes_button.is_clicked(event)
                self.eat_button.is_clicked(event)
                self.play_button.is_clicked(event)
                self.upgrades_button.is_clicked(event)
            elif self.mode == "Clothes menu":
                self.clothes_menu.next_button.is_clicked(event)
                self.clothes_menu.back_button.is_clicked(event)
                self.clothes_menu.buy_button.is_clicked(event)
                self.clothes_menu.use_button.is_clicked(event)
            elif self.mode == "Food menu":
                self.food_menu.next_button.is_clicked(event)
                self.food_menu.back_button.is_clicked(event)
                self.food_menu.buy_eat_button.is_clicked(event)
            elif self.mode == "Upgrades menu":
                self.upgrades_menu.next_button.is_clicked(event)
                self.upgrades_menu.back_button.is_clicked(event)
            # elif self.mode == "Game over":
            #     self.new_game_button.is_clicked(event)
                
    def update(self):
        if self.health <=0:
            self.mode = "Game over"

    def draw(self,draw_body=True):
        #Отрисовываем задний фон
        self.screen.blit(self.background,(0,0))
        #Отрисовываем иконки и текст
        self.screen.blit(self.happines_image,(GRID,GRID))
        self.screen.blit(self.satiety_image,(GRID,GRID+ICON_SIZE))
        self.screen.blit(self.health_image,(GRID,GRID*2 +ICON_SIZE*2)) 

        self.screen.blit(self.body,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10)) 

        self.screen.blit(text_render(self.happiness),(GRID+ICON_SIZE,GRID*4))
        self.screen.blit(text_render(self.satiety),(GRID+ICON_SIZE,GRID*4+ICON_SIZE))
        self.screen.blit(text_render(self.health),(GRID+ICON_SIZE,GRID * 5 + ICON_SIZE * 2))

        self.screen.blit(self.money_image,(SCREEN_WIDTH - GRID - ICON_SIZE*2,GRID))
        self.screen.blit(text_render(self.money),(SCREEN_WIDTH - GRID - ICON_SIZE,GRID * 4))
        #Отрисовываем лица
        if self.happiness >= 70:#Хаппи хапи хаппи - ✅
            #self.screen.blit(self.body,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10))
            self.screen.blit(self.happy_face,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10))
        elif 30< self.happiness < 70:#Намальна -✅
            self.screen.blit(self.body,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10)) 
        elif 10< self.happiness < 30:#Я песик песик песик и вовсе не падаль - ✅
            #self.screen.blit(self.body,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10))
            self.screen.blit(self.sad_face,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10))
        elif self.happiness <=10:#☠️ - ✅
            #self.screen.blit(self.body,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10))
            self.screen.blit(self.sick_face,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10))
        #Отрисовываем кнопки
        self.clothes_button.draw(self.screen)
        self.eat_button.draw(self.screen)
        self.upgrades_button.draw(self.screen)
        self.play_button.draw(self.screen)

        for item in self.clothes_menu.items:
                if item.is_using:
                    self.screen.blit(item.full_image,(SCREEN_WIDTH // 2 - DOG_WIDTH//2,GRID*10))

        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)
        elif self.mode == "Food menu":
            self.food_menu.draw(self.screen)
        elif self.mode == "Play menu":
            self.play_menu.draw(self.screen)
        elif self.mode == "Upgrades menu":
            self.upgrades_menu.draw(self.screen)
        if self.mode == "Game over":
            game_over_text = font_max.render("ПРОИГРЫШ",True,"red")
            game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2,SCREEN_HEIGHT//2))
            self.screen.blit(self.background,(0, 0))
            self.screen.blit(game_over_text,game_over_text_rect)
            # self.new_game_button = Button("Начать снова",SCREEN_WIDTH//2-105,SCREEN_HEIGHT-150,func=self.set_new_game_data)
            # self.new_game_button.draw(self.screen)
    def set_new_game_data(self):
        self.mode = "Main"
        self.draw()
        self.data = new_game_data
    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            pg.display.flip()
            self.clock.tick(FPS)
        


if __name__ == "__main__":
    game = Game()