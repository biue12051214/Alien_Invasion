import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """飞船所有信息"""
    def __init__(self, ai_settings, screen):
        """初始化飞船, 并设置其起始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load("images/ship.bmp")   # 加载图片
        self.rect = self.image.get_rect()   # 获取图片外接矩形
        self.screen_rect = screen.get_rect()    # 获取屏幕外接矩形
        # 将'飞船'放到底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)  # 设置成浮点类型
        self.moving_right = False   # 移动标志
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """上下左右移动'飞船'"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.rect.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制'飞船'"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船底部居中"""
        self.center = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
