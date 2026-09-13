import pygame as pg
import sys
import random
import os
import json

pg.init()
pg.mixer.init()

# تنظیمات ثابت موبایل: رزولوشن بالا و فریم ریت 60
W, H = 1280, 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 20)
HOVER_RED = (255, 60, 60)
HOVER_BLACK = (0, 0, 0)

SAVE_FILE = "save.json"

def load_high_score():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except:
            pass
    return 0

def save_high_score(score_val):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump({"high_score": score_val}, f)
    except:
        pass

settings = {
    "music_vol": 0.5,
    "sfx_vol": 0.7
}

# راه‌اندازی پنجره با قابلیت مقیاس‌پذیری خودکار برای موبایل
window = pg.display.set_mode((W, H), pg.SCALED)
screen = pg.Surface((W, H))

pg.display.set_caption("Flappy Doom Mobile")
clock = pg.time.Clock()

FONT_PATH = "assets/font/Doom.ttf"
def get_font(size):
    scaled_size = max(14, int(size * (H / 720.0)))
    if os.path.exists(FONT_PATH):
        try:
            return pg.font.Font(FONT_PATH, scaled_size)
        except:
            pass
    return pg.font.SysFont("arial", scaled_size, bold=True)

def load_sound(filepath):
    if os.path.exists(filepath):
        try:
            return pg.mixer.Sound(filepath)
        except:
            pass
    return None

sound_point = load_sound("assets/sound/point.wav")
sound_wing = load_sound("assets/sound/wing.wav")
sound_hit = load_sound("assets/sound/hit.wav")

music_path = "assets/sound/theme.mp3"
music_loaded = False
if os.path.exists(music_path):
    try:
        pg.mixer.music.load(music_path)
        music_loaded = True
    except:
        pass

def update_volumes():
    pg.mixer.music.set_volume(settings.get("music_vol", 0.5))
    for sfx in [sound_point, sound_wing, sound_hit]:
        if sfx:
            sfx.set_volume(settings.get("sfx_vol", 0.7))

update_volumes()

raw_bird_images = []
bird_dir = "assets/bird"

if os.path.exists(bird_dir):
    files = sorted([f for f in os.listdir(bird_dir) if f.endswith(".png")])
    for f in files:
        if f.lower() != "mask.png":
            filePath = os.path.join(bird_dir, f)
            try:
                img = pg.image.load(filePath).convert_alpha()
                raw_bird_images.append(img)
            except:
                pass

if not raw_bird_images:
    fallback = pg.Surface((45, 35), pg.SRCALPHA)
    fallback.fill((220, 40, 40))
    raw_bird_images.append(fallback)

# تنظیم آیکون بازی با اولین عکس پرنده
if raw_bird_images:
    pg.display.set_icon(raw_bird_images[0])

def load_raw_image(filepath, fallback_color, fallback_size):
    if os.path.exists(filepath):
        try:
            return pg.image.load(filepath).convert_alpha()
        except:
            pass
    surf = pg.Surface(fallback_size, pg.SRCALPHA)
    surf.fill(fallback_color)
    return surf

raw_bg = load_raw_image("assets/images/bg.png", (30, 20, 40), (1280, 720))
raw_menu_bg = load_raw_image("assets/images/menu.png", (20, 10, 30), (1280, 720))
raw_pause_bg = load_raw_image("assets/images/pause.png", (20, 10, 30), (1280, 720))
raw_ground = load_raw_image("assets/images/ground.png", (100, 50, 20), (1280, 120))
raw_pipe_top = load_raw_image("assets/images/top_pipe.png", (40, 180, 40), (90, 600))

ground_h = int(100 * (H / 720.0))
pipe_w = int(110 * (H / 720.0))
pipe_h = int(580 * (H / 720.0))
bird_w = int(70 * (H / 720.0))
bird_h = int(52 * (H / 720.0))

img_bg = pg.transform.smoothscale(raw_bg, (W, H))
img_menu_bg = pg.transform.smoothscale(raw_menu_bg, (W, H))
img_pause_bg = pg.transform.smoothscale(raw_pause_bg, (W, H))
img_ground = pg.transform.smoothscale(raw_ground, (W, ground_h))

img_pipe_top = pg.transform.smoothscale(raw_pipe_top, (pipe_w, pipe_h))
img_pipe_bottom = pg.transform.flip(img_pipe_top, False, True)

bird_images = [pg.transform.smoothscale(img, (bird_w, bird_h)) for img in raw_bird_images]

mask_pipe_top = pg.mask.from_surface(img_pipe_top)
mask_pipe_bottom = pg.mask.from_surface(img_pipe_bottom)

class FastOptimizedDoomFire:
    def __init__(self, width, height, ground_h):
        self.w = width
        self.h = height
        self.ground_h = ground_h
        
        # ابعاد آتش برای عملکرد روان روی موبایل
        self.fire_w = 64
        self.fire_h = 25
        
        self.raw_surf = pg.Surface((self.fire_w, self.fire_h))
        self.scaled_surf_w = width
        self.scaled_surf_h = int(45 * (height / 720.0))
        
        # ساخت یک افکت آتش ساده و سبک با پایتون خالص
        self.fire_surface = pg.Surface((self.fire_w, self.fire_h), pg.SRCALPHA)

    def update(self, dt):
        # افکت بصری سبک برای موبایل
        pass

    def draw_fire(self, target_surf):
        # رسم یک لایه آتش گرافیکی سبک روی زمین
        y_pos = self.h - self.ground_h - self.scaled_surf_h + int(10 * (self.h / 720.0))
        # ایجاد رنگ آتشین پویا با مستطیل‌های کوچک یا گرادینت ساده
        temp_fire = pg.Surface((self.w, self.scaled_surf_h), pg.SRCALPHA)
        temp_fire.fill((200, 60, 10, 120)) # رنگ آتشین نیمه‌شفاف
        target_surf.blit(temp_fire, (0, y_pos))

doom_fire = FastOptimizedDoomFire(W, H, ground_h)
pipes = []

class Button:
    def __init__(self, text, y_pos_ratio, action_id, font_size=38, hover_color=HOVER_BLACK):
        self.text = text
        self.y_pos_ratio = y_pos_ratio
        self.action_id = action_id
        self.font_size = font_size
        self.hover_color = hover_color

    def draw(self, surface, current_hover_id):
        hovered = (current_hover_id == self.action_id)
        color = self.hover_color if hovered else WHITE
        lbl = get_font(self.font_size).render(self.text, True, color)
        rect = lbl.get_rect(center=(W // 2, int(H * self.y_pos_ratio)))
        surface.blit(lbl, rect)
        return rect

STATE_START_MENU = 0
STATE_COUNTDOWN = 1
STATE_GAMEPLAY = 2
STATE_PAUSE_MENU = 3
STATE_SETTINGS = 4
STATE_CONFIRM_QUIT = 5
STATE_GAMEOVER = 6

current_state = STATE_START_MENU
previous_state = STATE_START_MENU
hovered_btn_id = None

def set_state(new_state):
    global current_state, previous_state
    
    if new_state == STATE_CONFIRM_QUIT:
        if current_state in (STATE_GAMEPLAY, STATE_PAUSE_MENU):
            if music_loaded: 
                pg.mixer.music.pause()
    elif current_state == STATE_CONFIRM_QUIT:
        if new_state == STATE_GAMEPLAY:
            if music_loaded: 
                pg.mixer.music.unpause()
        elif new_state == STATE_PAUSE_MENU:
            pass

    previous_state = current_state
    current_state = new_state

bg_x = 0
ground_x = 0
bird_x = int(200 * (W / 1280.0))
bird_y = int(300 * (H / 720.0))
bird_velocity = 0
gravity = 0.5 * (H / 720.0)
bird_angle = 0
score = 0
high_score = load_high_score()
bird_anim_frame = 0

last_pipe_time = 0
next_pipe_interval = 600
countdown_start_time = 0
countdown_val = 3
waiting_for_first_jump = True

def create_pipe():
    pipe_gap = int(210 * (H / 720.0))
    gap_y = random.randint(int(180 * (H / 720.0)), H - int(250 * (H / 720.0)))
    top_rect = img_pipe_top.get_rect(midbottom=(W + img_pipe_top.get_width(), gap_y - pipe_gap // 2))
    bot_rect = img_pipe_bottom.get_rect(midtop=(W + img_pipe_bottom.get_width(), gap_y + pipe_gap // 2))
    return {"top": top_rect, "bottom": bot_rect, "passed": False}

def reset_game():
    global bird_x, bird_y, bird_velocity, gravity, bird_angle, score, pipes, last_pipe_time, countdown_start_time, countdown_val, next_pipe_interval, waiting_for_first_jump
    bird_x = int(200 * (W / 1280.0))
    bird_y = int(300 * (H / 720.0))
    bird_velocity = 0
    gravity = 0.5 * (H / 720.0)
    bird_angle = 0
    score = 0
    pipes.clear()
    countdown_start_time = pg.time.get_ticks()
    last_pipe_time = pg.time.get_ticks()
    next_pipe_interval = 600
    countdown_val = 3
    waiting_for_first_jump = True
    if music_loaded:
        pg.mixer.music.play(-1)

def get_settings_buttons():
    return [
        Button(f"Music Vol: {int(settings['music_vol']*10)}", 0.35, "vol_music", font_size=40),
        Button(f"SFX Vol: {int(settings['sfx_vol']*10)}", 0.48, "vol_sfx", font_size=40),
        Button("Back", 0.62, "back", font_size=42)
    ]

running = True
while running:
    dt = clock.tick(FPS)
    dt_factor = dt / 16.67
    if dt_factor > 3.0: 
        dt_factor = 3.0
    elif dt_factor < 0.1: 
        dt_factor = 0.1

    now = pg.time.get_ticks()
    game_speed = 3.5 * (H / 720.0) * dt_factor
    ground_speed = 2.0 * (H / 720.0) * dt_factor

    mouse_pos = pg.mouse.get_pos()
    mouse_click = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type in (pg.MOUSEBUTTONDOWN, pg.FINGERDOWN):
            mouse_click = True
            if event.type == pg.FINGERDOWN:
                # تبدیل تاچ موبایل به مختصات صفحه
                mouse_pos = (int(event.x * W), int(event.y * H))

    screen.fill(BLACK)

    # 1. شمارش معکوس
    if current_state == STATE_COUNTDOWN:
        screen.blit(img_bg, (0, 0))
        screen.blit(img_ground, (0, H - ground_h))
        
        doom_fire.update(dt)
        doom_fire.draw_fire(screen)

        elapsed = (now - countdown_start_time) // 1000
        countdown_val = 3 - elapsed

        if countdown_val > 0:
            cd_txt = get_font(120).render(str(countdown_val), True, BLACK)
            screen.blit(cd_txt, cd_txt.get_rect(center=(W // 2, int(H * 0.38))))
        else:
            set_state(STATE_GAMEPLAY)
            last_pipe_time = pg.time.get_ticks()
            next_pipe_interval = 600

    # 2. گیم‌پلی
    elif current_state == STATE_GAMEPLAY:
        bg_x = (bg_x - game_speed * 0.4) % W
        ground_x = (ground_x - ground_speed) % W

        screen.blit(img_bg, (-bg_x, 0))
        screen.blit(img_bg, (-bg_x + W, 0))

        if mouse_click:
            if waiting_for_first_jump:
                waiting_for_first_jump = False
            bird_velocity = -9.0 * (H / 720.0)
            if sound_wing: sound_wing.play()

        if waiting_for_first_jump:
            bird_velocity = 0
            bird_y = int(300 * (H / 720.0))
            bird_angle = 0
        else:
            bird_velocity += gravity * dt_factor
            bird_y += bird_velocity * dt_factor

            if bird_velocity < 0:
                bird_angle = max(-30, bird_angle - 3 * dt_factor)
            else:
                bird_angle = min(70, bird_angle + 2.5 * dt_factor)

        min_distance = int(250 * (H / 720.0))
        
        if not waiting_for_first_jump and now - last_pipe_time > next_pipe_interval:
            if not pipes or (W + img_pipe_top.get_width() - pipes[-1]["top"].x >= min_distance):
                pipes.append(create_pipe())
                last_pipe_time = now
                next_pipe_interval = random.randint(1200, 2200)

        current_bird_img = bird_images[int(bird_anim_frame) % len(bird_images)]
        bird_anim_frame += 0.15 * dt_factor

        rotated_bird = pg.transform.rotate(current_bird_img, -bird_angle)
        bird_rect = rotated_bird.get_rect(center=(bird_x + int(35 * (H/720.0)), int(bird_y) + int(26 * (H/720.0))))
        rotated_mask = pg.mask.from_surface(rotated_bird)

        doom_fire.update(dt)
        doom_fire.draw_fire(screen)

        if not waiting_for_first_jump:
            for p in pipes[:]:
                p["top"].x -= game_speed
                p["bottom"].x -= game_speed

                if not p["passed"] and p["top"].right < bird_x:
                    p["passed"] = True
                    score += 1
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    if sound_point: sound_point.play()

                screen.blit(img_pipe_top, p["top"])
                screen.blit(img_pipe_bottom, p["bottom"])

                offset_top = (p["top"].x - bird_rect.x, p["top"].y - bird_rect.y)
                offset_bottom = (p["bottom"].x - bird_rect.x, p["bottom"].y - bird_rect.y)

                if rotated_mask.overlap(mask_pipe_top, offset_top) or rotated_mask.overlap(mask_pipe_bottom, offset_bottom):
                    if sound_hit: sound_hit.play()
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    if music_loaded: pg.mixer.music.stop()
                    set_state(STATE_GAMEOVER)

            pipes = [p for p in pipes if p["top"].right > -100]

        if not waiting_for_first_jump and (bird_y <= 0 or bird_y + bird_h >= H - ground_h):
            if sound_hit: sound_hit.play()
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            if music_loaded: pg.mixer.music.stop()
            set_state(STATE_GAMEOVER)

        screen.blit(img_ground, (-ground_x, H - ground_h))
        screen.blit(img_ground, (-ground_x + W, H - ground_h))
        screen.blit(rotated_bird, bird_rect.topleft)

        score_txt = get_font(55).render(str(score), True, WHITE)
        screen.blit(score_txt, score_txt.get_rect(center=(W // 2, int(55 * (H / 720.0)))))

        # دکمه لمسی توقف (Pause) گوشه بالا سمت راست
        pause_rect = pg.Rect(W - 80, 20, 60, 60)
        pg.draw.rect(screen, WHITE, pause_rect, 2, border_radius=10)
        p_txt = get_font(30).render("||", True, WHITE)
        screen.blit(p_txt, p_txt.get_rect(center=pause_rect.center))
        if mouse_click and pause_rect.collidepoint(mouse_pos):
            set_state(STATE_PAUSE_MENU)
            if music_loaded: pg.mixer.music.pause()

    # 3. منوی استارت
    elif current_state == STATE_START_MENU:
        if music_loaded and pg.mixer.music.get_busy():
            pg.mixer.music.stop()

        screen.blit(img_menu_bg, (0, 0))

        title = get_font(80).render("FLAPPY DOOM", True, BLACK)
        screen.blit(title, title.get_rect(center=(W // 2, int(H * 0.28))))

        buttons = [
            Button("Start Game", 0.46, "start", font_size=46),
            Button("Settings", 0.58, "settings", font_size=46),
            Button("Quit Game", 0.70, "quit", font_size=46)
        ]

        active_hover = None
        for btn in buttons:
            rect = btn.draw(screen, hovered_btn_id)
            if rect.collidepoint(mouse_pos):
                active_hover = btn.action_id
                if mouse_click:
                    if btn.action_id == "start":
                        reset_game()
                        set_state(STATE_COUNTDOWN)
                    elif btn.action_id == "settings":
                        set_state(STATE_SETTINGS)
                    elif btn.action_id == "quit":
                        set_state(STATE_CONFIRM_QUIT)
        hovered_btn_id = active_hover

    # 4. منوی توقف (Pause)
    elif current_state == STATE_PAUSE_MENU:
        screen.blit(img_pause_bg, (0, 0))

        title = get_font(65).render("PAUSED", True, WHITE)
        screen.blit(title, title.get_rect(center=(W // 2, int(H * 0.20))))

        buttons = [
            Button("Resume", 0.36, "resume", font_size=40),
            Button("Settings", 0.47, "settings", font_size=40),
            Button("Main Menu", 0.58, "main_menu", font_size=40),
            Button("Quit Game", 0.69, "quit", font_size=40)
        ]

        active_hover = None
        for btn in buttons:
            rect = btn.draw(screen, hovered_btn_id)
            if rect.collidepoint(mouse_pos):
                active_hover = btn.action_id
                if mouse_click:
                    if btn.action_id == "resume":
                        set_state(STATE_GAMEPLAY)
                        if music_loaded: pg.mixer.music.unpause()
                    elif btn.action_id == "settings":
                        set_state(STATE_SETTINGS)
                    elif btn.action_id == "main_menu":
                        if music_loaded: pg.mixer.music.stop()
                        set_state(STATE_START_MENU)
                    elif btn.action_id == "quit":
                        set_state(STATE_CONFIRM_QUIT)
        hovered_btn_id = active_hover

    # 5. تنظیمات
    elif current_state == STATE_SETTINGS:
        screen.blit(img_bg, (0, 0))

        title = get_font(45).render("SETTINGS", True, WHITE)
        screen.blit(title, title.get_rect(center=(W // 2, int(H * 0.18))))

        buttons = get_settings_buttons()
        active_hover = None
        for btn in buttons:
            rect = btn.draw(screen, hovered_btn_id)
            if rect.collidepoint(mouse_pos):
                active_hover = btn.action_id
                if mouse_click:
                    if btn.action_id == "vol_music":
                        settings["music_vol"] = round((settings["music_vol"] + 0.1) % 1.1, 1)
                        update_volumes()
                    elif btn.action_id == "vol_sfx":
                        settings["sfx_vol"] = round((settings["sfx_vol"] + 0.1) % 1.1, 1)
                        update_volumes()
                    elif btn.action_id == "back":
                        set_state(previous_state)
        hovered_btn_id = active_hover

    # 6. پایان بازی (Game Over)
    elif current_state == STATE_GAMEOVER:
        screen.fill(BLACK)

        border_thickness = max(4, int(6 * (H / 720.0)))
        pg.draw.rect(screen, WHITE, (2, 2, W - 4, H - 4), border_thickness)

        txt = get_font(95).render("GAME OVER", True, RED)
        screen.blit(txt, txt.get_rect(center=(W // 2, int(H * 0.22))))

        score_display = get_font(32).render(f"Score: {score}", True, WHITE)
        best_display = get_font(32).render(f"Best: {high_score}", True, WHITE)

        box_size = int(180 * (H / 720.0))
        box_rect = pg.Rect(0, 0, box_size, box_size)
        box_rect.center = (W // 2, int(H * 0.45))

        pg.draw.rect(screen, WHITE, box_rect, 2)

        screen.blit(score_display, score_display.get_rect(center=(box_rect.centerx, box_rect.centery - int(25 * (H / 720.0)))))
        screen.blit(best_display, best_display.get_rect(center=(box_rect.centerx, box_rect.centery + int(25 * (H / 720.0)))))

        buttons = [
            Button("Try Again", 0.65, "restart", font_size=38, hover_color=RED),
            Button("Main Menu", 0.75, "main_menu", font_size=38, hover_color=RED)
        ]

        active_hover = None
        for btn in buttons:
            rect = btn.draw(screen, hovered_btn_id)
            if rect.collidepoint(mouse_pos):
                active_hover = btn.action_id
                if mouse_click:
                    if btn.action_id == "restart":
                        reset_game()
                        set_state(STATE_COUNTDOWN)
                    elif btn.action_id == "main_menu":
                        if music_loaded: pg.mixer.music.stop()
                        set_state(STATE_START_MENU)
        hovered_btn_id = active_hover

    # 7. تایید خروج
    elif current_state == STATE_CONFIRM_QUIT:
        screen.fill(BLACK)

        border_thickness = max(4, int(6 * (H / 720.0)))
        pg.draw.rect(screen, WHITE, (2, 2, W - 4, H - 4), border_thickness)

        msg = get_font(65).render("Quit Game?", True, WHITE)
        screen.blit(msg, msg.get_rect(center=(W // 2, int(H * 0.32))))

        buttons = [
            Button("Yes", 0.48, "confirm_yes", font_size=48, hover_color=RED),
            Button("No", 0.62, "confirm_no", font_size=48, hover_color=RED)
        ]

        active_hover = None
        for btn in buttons:
            rect = btn.draw(screen, hovered_btn_id)
            if rect.collidepoint(mouse_pos):
                active_hover = btn.action_id
                if mouse_click:
                    if btn.action_id == "confirm_yes":
                        running = False
                    elif btn.action_id == "confirm_no":
                        set_state(previous_state)
        hovered_btn_id = active_hover

    window.blit(screen, (0, 0))
    pg.display.flip()

pg.quit()
sys.exit()
