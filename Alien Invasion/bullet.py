import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """'飞船'子弹进行管理"""
    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        # 创建子弹初始位置(0, 0),引入设置中的子弹宽高
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        # 设置中心点x轴坐标与'飞船'一致
        self.rect.centerx = ship.rect.centerx
        # 设置y轴坐标顶部与'飞船'一致
        self.rect.top = ship.rect.top
        # 设置成小数进行计算
        self.y = float(self.rect.y)
        # 定义子弹颜色与速度与settings.py中同
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """子弹向上走"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
