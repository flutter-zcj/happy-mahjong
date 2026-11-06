"""生成牌桌桌面贴图：深玉绿绒布 + 细金线 + 四角云纹。

原版牌桌是整片深绿绒布直接铺到底，只在边缘压一圈金色细线，
因此这里不再画厚木框，避免出现平铺格子纹。
输出 2668×1500（逻辑 1334×750 横屏的 2 倍）。
"""

import math

from PIL import Image, ImageDraw, ImageFilter

W, H = 2668, 1500
R = 74


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def main():
    # 底色：上深下浅的玉绿，模拟灯光从上方打下
    base = Image.new("RGB", (W, H), (28, 100, 70))
    px = base.load()
    for y in range(H):
        t = y / H
        c = lerp((24, 92, 64), (34, 116, 84), min(1.0, t * 1.25))
        for x in range(W):
            px[x, y] = c

    # 中央径向柔光，让桌面有灯下聚焦感
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = W // 2, int(H * 0.5)
    for i in range(40):
        r = 640 - i * 14
        gd.ellipse([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9], fill=(96, 205, 150, 4))
    glow = glow.filter(ImageFilter.GaussianBlur(60))

    img = Image.alpha_composite(base.convert("RGBA"), glow)

    # 绒布细颗粒，避免大面积纯色
    noise = Image.effect_noise((W, H), 12).convert("L")
    noise = noise.filter(ImageFilter.GaussianBlur(0.6))
    grain = Image.merge("RGBA", (noise.point(lambda v: 90), noise.point(lambda v: 200), noise.point(lambda v: 160), noise.point(lambda v: 16)))
    img = Image.alpha_composite(img, grain)

    d = ImageDraw.Draw(img)

    # 四角压暗
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, W, H], outline=(0, 0, 0, 0))
    for i in range(30):
        a = int(3 + i * 1.6)
        vd.rounded_rectangle([-i * 3, -i * 3, W + i * 3, H + i * 3], radius=R + i * 3, outline=(2, 24, 16, a), width=6)
    img = Image.alpha_composite(img, vig)

    d = ImageDraw.Draw(img)

    # 外描边：深绿压边，防止贴图边缘出现亮线
    d.rounded_rectangle([1, 1, W - 2, H - 2], radius=R, outline=(18, 64, 46, 255), width=8)

    # 金色双线边框
    d.rounded_rectangle([16, 16, W - 16, H - 16], radius=R - 6, outline=(214, 178, 112, 210), width=3)
    d.rounded_rectangle([30, 30, W - 30, H - 30], radius=R - 14, outline=(214, 178, 112, 90), width=2)

    # 内圈虚线金线
    dash = 26
    gap = 18
    step = dash + gap
    # 上下边
    for x in range(70, W - 70, step):
        d.line([x, 66, min(x + dash, W - 70), 66], fill=(226, 196, 138, 70), width=2)
        d.line([x, H - 66, min(x + dash, W - 70), H - 66], fill=(226, 196, 138, 70), width=2)
    # 左右边
    for y in range(70, H - 70, step):
        d.line([66, y, 66, min(y + dash, H - 70)], fill=(226, 196, 138, 70), width=2)
        d.line([W - 66, y, W - 66, min(y + dash, H - 70)], fill=(226, 196, 138, 70), width=2)

    # 四角云纹：同心圆弧 + 短挑线，呼应原版描金纹样
    def corner(cx, cy, sx, sy):
        for i, r in enumerate((44, 66, 88)):
            a = 200 - i * 45
            d.arc([cx - r, cy - r, cx + r, cy + r],
                  start=0 if sx > 0 and sy > 0 else 90 if sx < 0 and sy > 0 else 180 if sx > 0 and sy < 0 else 270,
                  end=90 if sx > 0 and sy > 0 else 180 if sx < 0 and sy > 0 else 270 if sx > 0 and sy < 0 else 360,
                  fill=(228, 198, 140, a), width=3)
        d.line([cx, cy, cx + sx * 96, cy], fill=(228, 198, 140, 120), width=2)
        d.line([cx, cy, cx, cy + sy * 96], fill=(228, 198, 140, 120), width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(228, 198, 140, 170))

    corner(112, 112, 1, 1)
    corner(W - 112, 112, -1, 1)
    corner(112, H - 112, 1, -1)
    corner(W - 112, H - 112, -1, -1)

    out = img.convert("RGB")
    out.save("/root/build/mahjong-web/src/static/mahjong/bg/table_top.png", optimize=True)
    out.resize((667, 375), Image.LANCZOS).save("/root/build/table_top_preview.jpg", quality=90)
    print("saved", out.size)


if __name__ == "__main__":
    main()
