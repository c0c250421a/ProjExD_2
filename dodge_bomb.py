import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650

DELTA = {pg.K_UP:(0,-5), # 上矢印キー
         pg.K_DOWN:(0,5), # 下矢印キー
         pg.K_LEFT:(-5,0), # 左矢印キー
         pg.K_RIGHT:(5,0), # 右矢印キー
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectもしくは爆弾Rect
    戻り値：判定結果タプル(横,縦)
    True:画面内 , False:画面外
    """
    x , y = True , True
    if rct.left < 0 or WIDTH < rct.right:
        x = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        y = False
    return x,y

def gameover(screen :pg.surface) -> None:
    bg_img = pg.image.load("fig/pg_bg.jpg")
    screen.blit(bg_img,[0,0])

    bl_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bl_img, (0,0,0), pg.Rect(0,0,WIDTH, HEIGHT))
    bl_img.set_alpha(200)
    screen.blit(bl_img,[0,0])

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver",True, (255, 255, 255))
    screen.blit(txt, [400, 300])

    kk_img = pg.image.load("fig/8.png")
    screen.blit(kk_img,[700,300])

    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randrange(0,1100), random.randrange(0,650)
    vx = 5 
    vy = 5
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] # 横の移動
                sum_mv[1] += mv[1] # 縦の移動
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        x , y = check_bound(bb_rct)
        if not x:
            vx *= -1
        if not y:
            vy *= -1
        bb_rct.move_ip(vx,vy)
        screen.blit(bb_img,bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
