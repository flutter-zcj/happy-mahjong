"""生成欢乐麻将大厅背景：白天城市天台。

画面自上而下：蓝天白云 → 远景城市与摩天轮 → 樱花树 → 玻璃护栏 → 天台地面。
输出 1920×1080 的横屏 JPEG，供 uni-app 首页以 aspectFill 铺满。
"""

import math
import random

from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
HORIZON = 700
rnd = random.Random(20261103)


def vgrad(size, top, bottom, stop=None):
    """竖直渐变，stop 为 0~1，渐变在中途结束并保持底部颜色。"""
    w, h = size
    img = Image.new("RGB", (1, h))
    px = img.load()
    end = int(h * (stop if stop else 1.0))
    for y in range(h):
        t = min(1.0, y / max(1, end))
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return img.resize((w, h), Image.BILINEAR)


def soft_blob(draw, box, color, blur=0):
    draw.ellipse(box, fill=color)


def cloud(layer, cx, cy, scale, alpha):
    """一朵由多个椭圆叠成的蓬松云。"""
    d = ImageDraw.Draw(layer)
    parts = [
        (-1.00, 0.10, 0.56, 0.30),
        (-0.42, -0.12, 0.52, 0.40),
        (0.26, -0.06, 0.46, 0.34),
        (0.86, 0.14, 0.52, 0.26),
        (0.06, 0.16, 0.72, 0.28),
    ]
    for px, py, rx, ry in parts:
        d.ellipse(
            [
                cx + px * scale - rx * scale,
                cy + py * scale - ry * scale,
                cx + px * scale + rx * scale,
                cy + py * scale + ry * scale,
            ],
            fill=(255, 255, 255, alpha),
        )


def building(d, x, base, w, h, color, window=None, roof=0):
    """画一栋楼，可选女儿墙与窗格点阵。"""
    d.rectangle([x, base - h, x + w, base], fill=color)
    if roof:
        d.rectangle([x - w * 0.06, base - h - roof, x + w * 1.06, base - h], fill=color)
    if window:
        cols = max(1, int(w // 26))
        rows = max(1, int((h - 24) // 34))
        for c in range(cols):
            for r in range(rows):
                if rnd.random() < 0.42:
                    continue
                wx = x + 12 + c * (w - 20) / max(1, cols) 
                wy = base - h + 18 + r * 34
                if wx + 12 > x + w - 6 or wy + 16 > base - 10:
                    continue
                d.rectangle([wx, wy, wx + 10, wy + 14], fill=window)


def ferris_wheel(d, cx, cy, r, color, pod):
    """摩天轮：外环、内环、辐条与吊舱。"""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=6)
    d.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82], outline=color, width=3)
    d.ellipse([cx - r * 0.1, cy - r * 0.1, cx + r * 0.1, cy + r * 0.1], fill=color)
    for i in range(12):
        a = math.pi * 2 * i / 12
        ex, ey = cx + math.cos(a) * r, cy + math.sin(a) * r
        d.line([cx, cy, ex, ey], fill=color, width=3)
        # 吊舱挂在环外
        px, py = cx + math.cos(a) * (r + 12), cy + math.sin(a) * (r + 12)
        d.rounded_rectangle([px - 11, py - 4, px + 11, py + 18], radius=6, fill=pod)
    # 支架
    d.line([cx - r * 0.72, HORIZON, cx, cy], fill=color, width=8)
    d.line([cx + r * 0.72, HORIZON, cx, cy], fill=color, width=8)


def blossom(d, cx, cy, r, base, light):
    """一团樱花：密集小圆点，外圈更浅。"""
    for _ in range(int(r * r / 46)):
        a = rnd.uniform(0, math.pi * 2)
        rr = rnd.uniform(0, 1) ** 0.62 * r
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.86
        s = rnd.uniform(r * 0.055, r * 0.135)
        d.ellipse([x - s, y - s, x + s, y + s], fill=light if rr > r * 0.55 else base)


def branch(d, pts, color, width):
    d.line(pts, fill=color, width=width, joint="curve")


def main():
    img = vgrad((W, H), (118, 189, 236), (226, 243, 252), stop=0.78).convert("RGBA")

    # 高空薄雾光晕
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.radial = None
    for i in range(26):
        rr = 520 - i * 18
        a = 6
        gd.ellipse([W * 0.78 - rr, 300 - rr, W * 0.78 + rr, 300 + rr], fill=(255, 250, 226, a))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img = Image.alpha_composite(img, glow)

    # 云
    clouds = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cloud(clouds, 190, 220, 210, 200)
    cloud(clouds, 760, 150, 250, 170)
    cloud(clouds, 980, 400, 170, 150)
    cloud(clouds, 420, 470, 150, 120)
    cloud(clouds, 90, 640, 180, 110)
    cloud(clouds, 690, 560, 210, 90)
    clouds = clouds.filter(ImageFilter.GaussianBlur(9))
    img = Image.alpha_composite(img, clouds)

    # 远景城市（低对比、淡）
    far = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(far)
    x = -60
    while x < W + 80:
        w = rnd.randint(70, 150)
        h = rnd.randint(150, 330)
        building(fd, x, HORIZON - 40, w, h, (188, 212, 230, 210), roof=8)
        x += w + rnd.randint(6, 26)
    far = far.filter(ImageFilter.GaussianBlur(2.4))
    img = Image.alpha_composite(img, far)

    # 中景城市 + 摩天轮
    mid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mid)
    ferris_wheel(md, 1360, 420, 150, (206, 226, 240, 255), (222, 238, 249, 255))
    x = -40
    while x < W + 60:
        w = rnd.randint(85, 160)
        h = rnd.randint(230, 470)
        col = (206, 224, 238, 255) if rnd.random() < 0.5 else (216, 232, 244, 255)
        building(md, x, HORIZON, w, h, col, window=(240, 248, 253, 200), roof=rnd.choice([0, 0, 10, 18]))
        x += w + rnd.randint(4, 22)
    mid = mid.filter(ImageFilter.GaussianBlur(0.8))
    img = Image.alpha_composite(img, mid)

    # 樱花树：左侧主树 + 右侧补齐
    tree = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tree)
    branch(td, [-30, 120, 120, 250, 250, 300], (150, 118, 118, 190), 9)
    branch(td, [60, 190, 20, 330, 40, 430], (150, 118, 118, 170), 7)
    branch(td, [150, 270, 300, 330, 400, 300], (150, 118, 118, 160), 6)
    blossom(td, 60, 150, 190, (247, 190, 212, 235), (253, 226, 238, 235))
    blossom(td, 250, 250, 150, (250, 202, 221, 225), (254, 234, 242, 225))
    blossom(td, 360, 150, 120, (249, 196, 217, 200), (253, 230, 240, 200))
    blossom(td, W - 40, 360, 190, (247, 190, 212, 210), (253, 228, 240, 210))
    blossom(td, W - 210, 540, 130, (249, 199, 219, 170), (254, 233, 242, 170))
    tree = tree.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.alpha_composite(img, tree)

    # 玻璃护栏：横向浅带 + 竖柱 + 上沿高光
    rail = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rail)
    rd.rectangle([0, HORIZON - 120, W, HORIZON + 6], fill=(214, 235, 247, 130))
    for x in range(0, W + 1, 96):
        rd.rectangle([x - 3, HORIZON - 120, x + 3, HORIZON + 6], fill=(255, 255, 255, 130))
    rd.rectangle([0, HORIZON - 132, W, HORIZON - 116], fill=(255, 255, 255, 210))
    rd.rectangle([0, HORIZON - 12, W, HORIZON + 8], fill=(246, 252, 255, 220))
    rail = rail.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img, rail)

    # 天台地面：浅蓝灰渐变 + 反光
    deck = Image.new("RGBA", (W, H - HORIZON), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deck)
    dh = H - HORIZON
    for y in range(dh):
        t = y / dh
        c = (
            int(226 - 26 * t),
            int(238 - 20 * t),
            int(247 - 12 * t),
            int(238 - 34 * t),
        )
        dd.line([0, y, W, y], fill=c)
    # 地砖接缝
    for i in range(1, 7):
        y = int(dh * (i / 7) ** 1.35)
        dd.line([0, y, W, y], fill=(255, 255, 255, 70), width=2)
    deck = deck.filter(ImageFilter.GaussianBlur(1.4))
    img.paste(deck, (0, HORIZON), deck)

    # 地面上一圈柔和投影，让人物与卡片有站立感
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([W * 0.36, HORIZON + 140, W * 0.60, HORIZON + 200], fill=(120, 160, 190, 46))
    shadow = shadow.filter(ImageFilter.GaussianBlur(36))
    img = Image.alpha_composite(img, shadow)

    out = img.convert("RGB")
    out.save("/root/build/mahjong-web/src/static/mahjong/bg/hall_day.jpg", quality=88, optimize=True)
    out.resize((960, 540), Image.LANCZOS).save("/root/build/hall_day_preview.jpg", quality=88)
    print("saved", out.size)


if __name__ == "__main__":
    main()
