import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个小笼包的类"""
    def __init__(self, ai_settings, screen):
        """初始化小笼包并设置其他位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载小笼包图像, 并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # 每个小笼包初始位置都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 储存小笼包的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制小笼包"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """检查边缘,(0, 0)是左上角.如果小笼包在边缘, 返回Ture"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向右移动小笼包"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
