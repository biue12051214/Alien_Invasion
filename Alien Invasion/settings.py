class Settings:
    """储存游戏所有设置"""
    def __init__(self):
        self.screen_width = 1000    # 屏幕宽
        self.screen_height = 700    # 屏幕长
        self.bg_color = (50, 180, 240)  # 背景色(0~255, 0~255, 0~255)
        self.ship_speed_factor = 1.5    # "飞船"速度
        self.ship_limit = 3    # 拥有"飞船"数
        self.bullet_speed_factor = 2  # 子弹速度
        self.bullet_width = 7   # 子弹宽
        self.bullet_height = 13  # 子弹高
        self.bullet_color = 250, 160, 160    # 子弹颜色(开始按钮颜色在button.py里)
        self.bullets_allowed = 7    # 屏幕中最多可出现子弹数目
        self.alien_speed_factor = 0.1   # 小笼包首次出场速度(外星人)
        self.fleet_drop_speed = 3  # 小笼包到达屏幕边缘后向下的速度
        self.speedup_scale = 1.1    # 小笼包底速度递增系数,越大越难
        self.score_scale = 1.2  # 小笼包底分数递增系数
        self.fleet_direction = 1    # 1向右移,-1左移
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_points = 7   # 一个外星人多少分

    def increase_speed(self):
        """提高速度设置, 小笼包点数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
