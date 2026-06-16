import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650

DELTA = {pg.K_UP:(0,-5),  # 上矢印キー
         pg.K_DOWN:(0,5),  # 下矢印キー
         pg.K_LEFT:(-5,0),  # 左矢印キー
         pg.K_RIGHT:(5,0),  # 右矢印キー
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
    """
    ゲームオーバー画面の表示を行う
    こうかとんが爆弾に触れた時に、
    画面をブラックアウトし泣いているこうかとん画像と「GameOver」の文字を表示。
    引数：screenのSurface
    戻り値:なし
    """
    bg_img = pg.image.load("fig/pg_bg.jpg")  # 背景画像
    screen.blit(bg_img,[0,0])

    bl_img = pg.Surface((WIDTH, HEIGHT))  # 黒い四角形
    pg.draw.rect(bl_img, (0,0,0), pg.Rect(0,0,WIDTH, HEIGHT))
    bl_img.set_alpha(200)
    screen.blit(bl_img,[0,0])

    fonto = pg.font.Font(None, 80)  # 「GameOver」の文字
    txt = fonto.render("GameOver",True, (255, 255, 255))
    screen.blit(txt, [400, 300])

    kk_img = pg.image.load("fig/8.png")  # こうかとん（泣）
    screen.blit(kk_img,[700,300])

    pg.display.update()
    time.sleep(5)

def timer(tmr : int , screen : pg.surface) -> None:
    """
    タイマーを表示する関数
    引数:tmr(whileが一回回るごとに1増える変数),screenのSurface
    戻り値:なし
    """
    fonto = pg.font.Font(None, 80)
    txt = fonto.render(str(tmr / 50) ,True, (0, 0, 0))  # whileのtmrを利用してタイマー表示
    screen.blit(txt, [0, 0])

def get_kk_imgs(img : pg.surface) -> dict[tuple[int, int], pg.Surface]:
    """
    こうかとんが向いている向きを指定する関数
    現在移動合計値をタプルで管理しているため、
    タプルをキーとして画像を回転させている。
    引数：画像Surface
    戻り値:移動合計値タプルをキーにした角度を変えた画像
    """
    kk_dict = {
                (0,0): pg.transform.rotozoom(img , 0 , 1),  # キー押下がない場合
                (5,0): pg.transform.rotozoom(img , 0, 1),  # 右
                (5,5): pg.transform.rotozoom(img , 45, 1),  # 右上
                (0,5): pg.transform.rotozoom(img , 90, 1),  # 上
                (-5,0): pg.transform.rotozoom(img , 180 ,1),  # 左
                (-5,-5): pg.transform.rotozoom(img , 135 , 1),  # 左下
                (-5,5): pg.transform.rotozoom(img , 225 , 1),  # 左上
                (0,-5): pg.transform.rotozoom(img , 270 , 1),  # 下
                (5,-5): pg.transform.rotozoom(img , 315, 1),  # 右下
    }
    return kk_dict

def  init_bb_imgs(img : pg.Surface) -> tuple[list[pg.Surface], list[int]] :
    """
    爆弾の大きさと速度を変えるためのリストを出力する関数
    引数:爆弾の画像Surface
    戻り値:画像Surfaceのリストと速度のリストのタプル
    """
    bb_imgs = []
    for r in range(1, 11):  # 10段階に分けて大きさを設定
        img = pg.Surface((20*r, 20*r))
        pg.draw.circle(img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(img)

    bb_accs = [a for a in range(1, 11)]  # 10段階に分けて速さを設定

    return bb_imgs,bb_accs

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

    kk_imgs = get_kk_imgs(kk_img)  # 画像の向きを決める辞書を取得
    bb_imgs,bb_accs = init_bb_imgs(bb_img)  # 爆弾の大きさと速度の辞書を取得

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
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横の移動
                sum_mv[1] += mv[1]  # 縦の移動
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 動きをなかったことにする
        kk_img = kk_imgs[tuple(sum_mv)]  # whileの手前で取得した辞書を基に画像を回転
        kk_img = pg.transform.flip(kk_img, True, False)  # 初期状態を右にするために左右反転
        if sum_mv[0] == -5:  # 左を向いたときに上下反転
            kk_img = pg.transform.flip(kk_img, False, True)
        screen.blit(kk_img, kk_rct)

        x , y = check_bound(bb_rct)
        if not x:
            vx *= -1
        if not y:
            vy *= -1
        avx = vx*bb_accs[min(tmr//500, 9)]  # 10秒ごとに速度を適用
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]  # 10秒ごとに大きさを適用
        bb_rct.move_ip(avx,avy)
        bb_rct.width = bb_img.get_rect().width  # 大きさを更新
        bb_rct.height = bb_img.get_rect().height
        bb_img.set_colorkey((0, 0, 0))  # 背景を透過
        screen.blit(bb_img,bb_rct)

        timer(tmr,screen)  #タイマーを表示

        pg.display.update()

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
