import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """检查按下键: 上下左右走_部分程序,空格发子弹,q结束游戏(如果没结束看输入法是不是英文)"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    # 抬起时为False,在另一个函数还方法里调用结果为False,不做反应.
    # 如果想空格连发,也可以仿照上下左右TrueFalse弄,不过连发一次全发出去挺麻烦,不会修就还是单发吧
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """监视键鼠事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 关闭窗口退出
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """在单击开始按钮后开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏鼠标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空小笼包列表和子弹列表
        aliens.empty()
        bullets.empty()
        # create new aliens and adjust ship(x.center and y.bottom)
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应小笼包与子弹的碰撞"""
    # 删除发生碰撞的子弹和小笼包
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 删除现有子弹并新建一笼小笼包,加快游戏进度节奏
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高记录"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图片,并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)   # 设置背景颜色
    for bullet in bullets.sprites():    # 循环子弹组里的元素,为空时不执行
        bullet.draw_bullet()    # 绘制飞船
    ship.blitme()   # 绘制'飞船'
    aliens.draw(screen)
    sb.show_score()  # 显示得分
    # 如果游戏 is False,显示开始按钮
    if not stats.game_active:
        play_button.draw_button()
    # 新屏幕取代旧屏幕
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置,删除子弹"""
    bullets.update()    # 子弹组每个成员执行self.update()操作
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:  # 子弹出界,删除
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个小笼包"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算可容纳几行小笼包"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
    '"小笼包的上下间隔⬆"'
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建小笼包群"""
    # 创建一个小笼包,并计算一行可容纳多少个小笼包
    # 小笼包间距为小笼包宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建第一行小笼包
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个小笼包并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """当有小笼包到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整笼小笼包下移, 并改变他们的移动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的'飞船'"""
    if stats.ships_left > 0:
        # ship_left剩余'飞船'数-1
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空小笼包和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人, 并将'飞船'放到屏幕低部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停0.5s
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有小笼包 get in screen bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 同'飞船'被撞一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新小笼包笼中所有小笼包的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测小笼包和'飞船'之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # 检查是否有小笼包 get in screen bottom
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_ship(ship):
    ship.update()
