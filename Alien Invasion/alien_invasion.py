import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()   # 初始化背景设置
    ai_settings = Settings()    # 全局设置
    screen = pygame.display.set_mode(   # 显示screen显示窗口
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')    # 标题
    # 新建开始按钮
    play_button = Button(ai_settings, screen, 'Eat')
    # 创建一个用于储存游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建"飞船"
    ship = Ship(ai_settings, screen)
    # 创建一个小笼包
    alien = Group()
    # 创建子弹编组
    bullets = Group()
    # 创建小笼包群
    gf.create_fleet(ai_settings, screen, ship, alien)
    # 开始游戏循环
    while True:
        # 监视键鼠事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, alien, bullets)
        if stats.game_active:
            # 移动"飞船"
            ship.update()
            # 更新子弹位置
            gf.update_bullets(ai_settings, screen, stats, sb, ship, alien, bullets)
            # 更新小笼包
            gf.update_aliens(ai_settings, screen, stats, sb, ship, alien, bullets)
        # 更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, alien, bullets, play_button)


run_game()
