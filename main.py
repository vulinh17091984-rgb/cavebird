# main.py - PHẦN 1: CHUYỂN ĐỔI SANG framework KIVY ĐỒ HỌA DI ĐỘNG CHUẨN XUẤT APK
import math
import random
import json
import os
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Mesh
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

# Khóa kích thước màn hình ảo tương thích chuẩn config cũ
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SAVE_FILE = "cave_save.json"

# Định nghĩa bảng màu RGB sang chuẩn Kivy (chia 255)
COLORS = {
    "CAVE_BG": (18/255, 14/255, 24/255, 1),
    "GRID_LINE": (28/255, 22/255, 36/255, 1),
    "ROCK_BASE": (32/255, 26/255, 38/255, 1),
    "ROCK_MID": (46/255, 38/255, 54/255, 1),
    "STALACTITE": (64/255, 54/255, 74/255, 1),
    "CRYSTAL": (0/255, 235/255, 210/255, 1),
    "DIAMOND": (0/255, 235/255, 210/255, 1),
    "LANTERN_GLOW": (255/255, 160/255, 40/255, 1),
    "MAGMA": (255/255, 65/255, 0/255, 1),
    "SHIELD_GLOW": (0/255, 190/255, 255/255, 1),
    "BAT_BODY": (75/255, 65/255, 90/255, 1),
    "BAT_WING": (50/255, 42/255, 62/255, 1),
    "DRAGON_BODY": (220/255, 50/255, 40/255, 1),
    "TEXT": (230/255, 225/255, 240/255, 1)
}

class CaveSkinManager:
    def __init__(self):
        self.current_skin = 0
        self.unlocked_dragon = False
        self.dragon_cost = 15
        self.total_diamonds = 0
        self.high_score = 0
        self.load_game_data()

    def buy_dragon_skin(self):
        if not self.unlocked_dragon and self.total_diamonds >= self.dragon_cost:
            self.total_diamonds -= self.dragon_cost
            self.unlocked_dragon = True
            self.current_skin = 1
            self.save_game_data()
            return True
        return False

    def load_game_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.total_diamonds = data.get("total_diamonds", 0)
                    self.unlocked_dragon = data.get("unlocked_dragon", False)
                    self.current_skin = data.get("current_skin", 0)
            except: pass

    def save_game_data(self):
        data = {"high_score": self.high_score, "total_diamonds": self.total_diamonds, "unlocked_dragon": self.unlocked_dragon, "current_skin": self.current_skin}
        try:
            with open(SAVE_FILE, "w") as f: json.dump(data, f)
        except: pass

skin_shop = CaveSkinManager()
# main.py - PHẦN 2: LOGIC VÒNG LẶP CHÍNH VÀ KHỞI CHẠY KHUNG ỨNG DỤNG KIVY
class CaveBirdGame(Widget):
    def __init__(self, **kwargs):
        super(CaveBirdGame, self).__init__(**kwargs)
        self.game_state = 0 # 0: Menu, 1: Playing, 2: GameOver
        self.score = 0
        self.water_level = 40
        self.player_x = 80
        self.player_y = SCREEN_HEIGHT / 2
        self.player_velocity = 0
        self.gravity = 13.68
        self.jump_strength = -230.0
        self.has_shield = False
        
        # Bắt sự kiện chạm màn hình trên điện thoại Android
        self.bind(on_touch_down=self.handle_touch)
        Clock.schedule_interval(self.update_dt, 1.0 / 60.0)

    def handle_touch(self, instance, touch):
        if self.game_state == 1:
            self.player_velocity = self.jump_strength
        elif self.game_state == 0:
            self.game_state = 1
            self.score = 0
            self.water_level = 40
            self.player_y = SCREEN_HEIGHT / 2
            self.player_velocity = 0
        elif self.game_state == 2:
            self.game_state = 0

    def update_dt(self, dt):
        if dt > 0.1: dt = 0.1
        if self.game_state == 1:
            # Thuật toán vật lý chim bay khớp hoàn toàn logic cũ của bạn
            self.player_velocity += self.gravity * dt * 60
            self.player_y -= self.player_velocity * dt
            
            # Quản lý mực nước dâng lên khi ghi điểm
            if self.score > 0 and self.score % 5 == 0:
                self.water_level += (115 - self.water_level) * 3.0 * dt
            else:
                self.water_level += (40 - self.water_level) * 1.8 * dt
                
            if self.player_y <= self.water_level or self.player_y >= SCREEN_HEIGHT:
                self.game_state = 2
                if self.score > skin_shop.high_score:
                    skin_score = self.score
                    skin_shop.high_score = skin_score
                    skin_shop.save_game_data()

        self.canvas.clear()
        with self.canvas:
            # 1. Vẽ nền hang tối giản
            Color(*COLORS["CAVE_BG"])
            Rectangle(pos=(0,0), size=(SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # 2. Vẽ nhân vật Cave Bird hình tròn bằng Kivy core canvas
            if skin_shop.current_skin == 0:
                Color(*COLORS["BAT_BODY"])
            else:
                Color(*COLORS["DRAGON_BODY"])
            Ellipse(pos=(self.player_x - 12, self.player_y - 12), size=(24, 24))
            
            # Nếu có khiên chắn, vẽ vòng bảo vệ hào quang xung quanh chim
            if self.has_shield:
                Color(*COLORS["SHIELD_GLOW"])
                Ellipse(pos=(self.player_x - 18, self.player_y - 18), size=(36, 36))

            # 3. Vẽ mực nước dâng cuộn sóng ở đáy màn hình
            Color(*COLORS["DIAMOND"])
            Rectangle(pos=(0, 0), size=(SCREEN_WIDTH, self.water_level))

class CaveBirdApp(App):
    def build(self):
        Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        parent = FloatLayout()
        self.game = CaveBirdGame()
        parent.add_widget(self.game)
        
        # Thêm nhãn chữ hiển thị điểm số thời gian thực lên giao diện di động
        self.score_label = Label(text="CHAM MAN HINH DE BAY", pos=(0, SCREEN_HEIGHT/3), font_size='20sp', color=COLORS["TEXT"])
        parent.add_widget(self.score_label)
        Clock.schedule_interval(self.update_hud, 1.0 / 10.0)
        return parent

    def update_hud(self, dt):
        if self.game.game_state == 0:
            self.score_label.text = f"CAVE BIRD\nKỷ lục: {skin_shop.high_score}\n\nBẤM ĐỂ CHƠI"
        elif self.game.game_state == 1:
            self.score_label.text = f"ĐIỂM: {self.game.score}"
        elif self.game.game_state == 2:
            self.score_label.text = f"GAME OVER\nĐiểm của bạn: {self.game.score}\n\nCHẠM ĐỂ QUAY LẠI"

if __name__ == '__main__':
    CaveBirdApp().run()
