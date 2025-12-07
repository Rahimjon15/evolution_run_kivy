from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '0')
Config.set('graphics','height', '0')
Config.write()

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from random import randint, choice



GRAVITY = -0.6
JUMP_STRENGTH = 26
GROUND_Y = 100
SPAWN_INTERVAL = 2.0
LEVEL_UP_SCORE = 10
MAX_LEVEL = 5
HIT_EFFECT_TIME = 0.18


class Player(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity_y = 0
        self.is_jumping = False
        self.frames = ["assets/player1.png", "assets/player2.png"]
        self.current_frame = 0
        Clock.schedule_interval(self.animate, 0.15)

    def animate(self, dt):
        if not self.is_jumping:
            self.source = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def update(self):
        self.y += self.velocity_y
        self.velocity_y += GRAVITY
        if self.y <= GROUND_Y:
            self.y = GROUND_Y
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            jump_sound = SoundLoader.load("assets/jump.wav")
            if jump_sound:
                jump_sound.play()
            self.source = self.frames[1]

    def get_hitbox(self):
        margin_x = self.width * 0.16
        margin_y = self.height * 0.12
        return (self.x + margin_x, self.y + margin_y,
                self.right - margin_x, self.top - margin_y)


class Enemy(Image):
    def __init__(self, enemy_type, size_type, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.enemy_type = enemy_type
        self.speed = randint(4, 6)
        self.size = (48, 48) if size_type == "small" else (80, 80)

    def get_hitbox(self):
        margin_x = self.width * 0.14
        margin_y = self.height * 0.12
        return (self.x + margin_x, self.y + margin_y,
                self.right - margin_x, self.top - margin_y)


class StarEffect(Image):
    def __init__(self, center_pos, **kwargs):
        super().__init__(**kwargs)
        self.source = "assets/star.png"
        self.size = (32, 32)
        self.pos = (center_pos[0] - self.width / 2, center_pos[1] - self.height / 2)


class ScrollingBackground(Image):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.size_hint = (None, None)
        self.allow_stretch = True
        self.keep_ratio = False
        self.width = Window.width
        self.height = Window.height
        self.x = 0
        self.y = 0
        self.speed = 2

    def scroll(self):
        self.x -= self.speed
        if self.x <= -self.width:
            self.x = self.width


class EvolutionGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.playing = False
        self.paused = False
        self.level = 1
        self.score = 0
        self.star_count = 0
        self.background_sources = ["assets/bg1.png", "assets/bg2.png", "assets/bg3.png"]
        self.bg_index = 0

        self.bg1 = ScrollingBackground(source=self.background_sources[self.bg_index])
        self.bg2 = ScrollingBackground(source=self.background_sources[self.bg_index])
        self.bg2.x = self.bg1.width
        self.add_widget(self.bg1)
        self.add_widget(self.bg2)

        self.player = Player(source="assets/player1.png", size=(96, 96), pos=(100, GROUND_Y))
        self.add_widget(self.player)

        self.player_prev_y = self.player.y
        self.enemies = []

        # UI
        self.score_label = Label(text="Score: 0", font_size=30,
                                pos=(10, Window.height - 70), color=(1, 1, 1, 1))
        self.add_widget(self.score_label)

        self.level_label = Label(text="Level: 1", font_size=28,
                                pos=(Window.width - 200, Window.height - 70), color=(1, 1, 1, 1))
        self.add_widget(self.level_label)

        self.pause_button = Button(
            background_normal="assets/pause.png",
            size_hint=(None, None),
            size=(64, 64),
            pos=(Window.width - 60, Window.height - 120)
        )
        self.pause_button.bind(on_press=self.toggle_pause)
        self.add_widget(self.pause_button)

        self.stars_label = Label(text="Stars:", font_size=28,
                                pos=(300, Window.height - 70), color=(1, 1, 0, 1))
        self.add_widget(self.stars_label)

        self.star_icons = []
        for i in range(5):
            icon = Image(source="assets/star.png", size=(32, 32), pos=(380 + i * 35, Window.height - 60))
            icon.opacity = 0
            self.add_widget(icon)
            self.star_icons.append(icon)

        self.game_over_label = Label(text="", font_size=48,
                                    pos=(Window.width / 2 - 150, Window.height / 2), color=(1, 0, 0, 1))
        self.add_widget(self.game_over_label)

        self.final_score_label = Label(text="", font_size=32,
                                       pos=(Window.width / 2 - 150, Window.height / 2 - 60), color=(1, 1, 1, 1))
        self.add_widget(self.final_score_label)

        self.play_button = Button(text="Play", size_hint=(None, None),
                                  size=(200, 80), pos=(300, 250), font_size=32)
        self.play_button.bind(on_release=self.start_game)
        self.add_widget(self.play_button)

        self.jump_button = Button(
            text="Jump",
            size_hint=(None, None),
            size=(150, 60),
            pos=(Window.width - 180, 20),
            font_size=24,
            background_color=(0.4, 0.7, 1, 1)
        )
        self.jump_button.bind(on_press=lambda instance: self.player.jump())
        self.add_widget(self.jump_button)

        Window.bind(on_key_down=self.on_key_down)
        self.update_event = Clock.schedule_interval(self.update, 1 / 60)

        self.music = SoundLoader.load("assets/music.mp3")
        if self.music:
            self.music.loop = True

        self.spawn_event = None

    def toggle_pause(self, instance):
        if self.playing:
            self.paused = not self.paused

    def start_game(self, instance):
        self.reset_game()
        self.playing = True
        try:
            self.remove_widget(self.play_button)
        except Exception:
            pass
        if self.spawn_event is not None:
            try:
                self.spawn_event.cancel()
            except Exception:
                pass
            try:
                Clock.unschedule(self.spawn_enemy)
            except Exception:
                pass
            self.spawn_event = None
        self.spawn_event = Clock.schedule_interval(self.spawn_enemy, SPAWN_INTERVAL)
        if self.music:
            self.music.play()

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.star_count = 0
        self.bg_index = 0
        for child in list(self.children):
            if isinstance(child, Enemy):
                try:
                    self.remove_widget(child)
                except Exception:
                    pass
        self.enemies.clear()
        self.bg1.source = self.background_sources[self.bg_index]
        self.bg2.source = self.background_sources[self.bg_index]
        self.bg1.x = 0
        self.bg2.x = Window.width
        self.score_label.text = "Score: 0"
        self.level_label.text = "Level: 1"
        self.game_over_label.text = ""
        self.final_score_label.text = ""
        self.player.pos = (100, GROUND_Y)
        self.player.velocity_y = 0
        self.player.is_jumping = False
        self.player.size = (96, 96)
        for star in self.star_icons:
            star.opacity = 0
        self.player_prev_y = self.player.y

    def safe_remove_widget(self, w):
        try:
            if w in self.children:
                self.remove_widget(w)
        except Exception:
            pass

    def update(self, dt):
        if not self.playing or self.paused:
            self.player_prev_y = self.player.y
            return

        prev_py = self.player_prev_y
        self.bg1.scroll()
        self.bg2.scroll()
        self.bg1.pos = (self.bg1.x, 0)
        self.bg2.pos = (self.bg2.x, 0)
        self.player.update()
        dy = self.player.y - prev_py

        for enemy in self.enemies[:]:
            enemy.x -= enemy.speed

            if enemy.x < -enemy.width:
                try:
                    self.remove_widget(enemy)
                except Exception:
                    pass
                try:
                    self.enemies.remove(enemy)
                except Exception:
                    pass
                if enemy.enemy_type == "monster":
                    self.score += 1
                    self.score_label.text = f"Score: {self.score}"
                    if self.score % LEVEL_UP_SCORE == 0:
                        self.level_up()
                continue

            px1, py1, px2, py2 = self.player.get_hitbox()
            ex1, ey1, ex2, ey2 = enemy.get_hitbox()
            overlap = not (px2 < ex1 or px1 > ex2 or py2 < ey1 or py1 > ey2)

            if overlap:
                if enemy.enemy_type == "bird":
                    if dy > 1.0:  # удар снизу головой
                        if self.star_count < len(self.star_icons):
                            self.star_icons[self.star_count].opacity = 1
                            self.star_count += 1

                        # добавляем визуальный эффект звездочки
                        star_effect = StarEffect(center_pos=enemy.center)
                        self.add_widget(star_effect)
                        Clock.schedule_once(lambda dt: self.safe_remove_widget(star_effect), 0.3)

                        try:
                            self.remove_widget(enemy)
                        except Exception:
                            pass
                        try:
                            self.enemies.remove(enemy)
                        except Exception:
                            pass

                        star_sound = SoundLoader.load("assets/star.wav")
                        if star_sound:
                            star_sound.play()
                        self.player_prev_y = self.player.y
                        continue
                    else:
                        Clock.schedule_once(lambda dt: self.game_over(), HIT_EFFECT_TIME)
                        self.player_prev_y = self.player.y
                        return
                else:
                    # монстр → поражение
                    Clock.schedule_once(lambda dt: self.game_over(), HIT_EFFECT_TIME)
                    self.player_prev_y = self.player.y
                    return

        if len(self.enemies) == 0 and self.playing:
            if self.level < MAX_LEVEL:
                self.next_level()
            else:
                self.you_win()

        self.player_prev_y = self.player.y

    def spawn_enemy(self, dt):
        if not self.playing or self.paused:
            return

        enemy_type = "monster" if self.level == 1 else choice(["monster", "bird"])
        size_type = choice(["small", "large"])
        source = f"assets/{enemy_type}.png"

        if enemy_type == "monster":
            y_pos = GROUND_Y
        else:
            y_pos = GROUND_Y + 220 + randint(-20, 40)

        enemy = Enemy(enemy_type, size_type, source=source, pos=(Window.width, y_pos))
        self.add_widget(enemy)
        self.enemies.append(enemy)

    def level_up(self):
        self.level += 1
        if self.level > MAX_LEVEL:
            self.you_win()
            return
        self.level_label.text = f"Level: {self.level}"
        self.bg_index = (self.bg_index + 1) % len(self.background_sources)
        self.bg1.source = self.background_sources[self.bg_index]
        self.bg2.source = self.background_sources[self.bg_index]
        w, h = self.player.size
        self.player.size = (w * 1.2, h * 1.2)

    def next_level(self):
        for child in list(self.children):
            if isinstance(child, Enemy):
                try:
                    self.remove_widget(child)
                except Exception:
                    pass
        self.enemies.clear()
        Clock.schedule_once(lambda dt: None, 0.1)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 32 and self.playing and not self.paused:
            self.player.jump()

    def game_over(self):
        self.playing = False
        self.paused = False
        self.game_over_label.text = "GAME OVER"
        self.final_score_label.text = f"You scored: {self.score} | Stars: {self.star_count}"
        if self.spawn_event is not None:
            try:
                self.spawn_event.cancel()
            except Exception:
                pass
            try:
                Clock.unschedule(self.spawn_enemy)
            except Exception:
                pass
            self.spawn_event = None
        if self.music:
            self.music.stop()
        try:
            self.add_widget(self.play_button)
        except Exception:
            pass

    def you_win(self):
        self.playing = False
        self.paused = False
        self.game_over_label.text = "YOU WIN!"
        self.final_score_label.text = f"Final Score: {self.score} | Stars: {self.star_count}"
        if self.spawn_event is not None:
            try:
                self.spawn_event.cancel()
            except Exception:
                pass
            try:
                Clock.unschedule(self.spawn_enemy)
            except Exception:
                pass
            self.spawn_event = None
        if self.music:
            self.music.stop()
        try:
            self.add_widget(self.play_button)
        except Exception:
            pass


class EvolutionRunApp(App):
    def build(self):
        return EvolutionGame()


if __name__ == '__main__':
    EvolutionRunApp().run()
