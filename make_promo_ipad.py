#!/usr/bin/env python3
# AI 글벗 App Store iPad 홍보 이미지 (12.9"/13" 규격 2048x2732).
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "/Users/jmwfdisk/Library/Mobile Documents/com~apple~CloudDocs/앱 개발/Ai 글벗/AI 글벗 스크린샷/ipad"
OUT = os.path.join(SRC, "promo")
os.makedirs(OUT, exist_ok=True)

W, H = 2048, 2732
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

def font(size):
    try: return ImageFont.truetype(FONT_PATH, size, index=0)
    except Exception: return ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", size)

# (파일명, 순번, 헤드라인, 서브카피, 상색, 하색)
ITEMS = [
    ("스크린샷, 2026-06-17 19.28.13.png", 1, "큰 화면에서\n문서와 대화", "여러 문서를 가져와 핵심을 묻고 요약받으세요", (0x4F,0x8C,0xFF), (0x2C,0x55,0xB8)),
    ("스크린샷, 2026-06-17 19.30.31.png", 2, "원문을 보며\n필기하고 질문", "PDF 원문·하이라이트·AI 대화를 한 화면에서", (0x6B,0x6B,0xF2), (0x3A,0x33,0x9C)),
    ("스크린샷, 2026-06-17 19.31.13.png", 3, "녹음을 요약·분석·재구성", "회의록·감정 분석·Q&A 재구성까지 자동으로", (0x5B,0x6C,0xFF), (0x35,0x3E,0xB0)),
    ("스크린샷, 2026-06-17 19.31.41.png", 4, "회의·강의·인터뷰\n상황별 AI 녹음", "목적에 맞는 모드로 더 정확하게 요약", (0xFF,0x8A,0x4B), (0xC2,0x4E,0x3A)),
    ("스크린샷, 2026-06-17 19.31.58.png", 5, "녹음·문서·프로젝트\n한눈에", "내 모든 자료를 현황 한 화면에서", (0x32,0xB8,0x8A), (0x1C,0x6E,0x55)),
    ("스크린샷, 2026-06-17 19.32.23.png", 6, "로컬은 무료·오프라인\n클라우드는 고품질", "문서·음성 각각 AI 엔진을 선택하세요", (0x32,0xB8,0x8A), (0x24,0x4A,0x9A)),
    ("스크린샷, 2026-06-17 19.27.18.png", 7, "내 취향대로\n테마까지", "라이트·다크 배경 테마와 글자 크기 조절", (0x8E,0x7B,0xF2), (0x4A,0x3A,0xA0)),
]

def gradient(top, bottom):
    img = Image.new("RGB", (W, H), top); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y/(H-1)
        d.line([(0,y),(W,y)], fill=(int(top[0]+(bottom[0]-top[0])*t), int(top[1]+(bottom[1]-top[1])*t), int(top[2]+(bottom[2]-top[2])*t)))
    return img

def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,img.size[0],img.size[1]], radius=radius, fill=255)
    out = img.convert("RGBA"); out.putalpha(mask); return out

CAPTION_H = 560
BOTTOM_MARGIN = 90
head_f = font(118)
sub_f = font(58)

for fn, num, headline, sub, top, bottom in ITEMS:
    canvas = gradient(top, bottom)
    shot = Image.open(os.path.join(SRC, fn)).convert("RGB")
    target_h = H - CAPTION_H - BOTTOM_MARGIN
    scale = target_h / shot.height
    sw, sh = int(shot.width*scale), int(shot.height*scale)
    if sw > W - 200:
        scale = (W-200)/shot.width; sw, sh = int(shot.width*scale), int(shot.height*scale)
    shot = shot.resize((sw, sh), Image.LANCZOS)
    radius = int(56*scale)
    shot_r = rounded(shot, radius)
    sx = (W - sw)//2
    sy = H - BOTTOM_MARGIN - sh

    shadow = Image.new("RGBA", (W,H), (0,0,0,0))
    ImageDraw.Draw(shadow).rounded_rectangle([sx, sy+16, sx+sw, sy+sh+16], radius=radius, fill=(0,0,0,115))
    shadow = shadow.filter(ImageFilter.GaussianBlur(34))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow)
    canvas.paste(shot_r, (sx, sy), shot_r)

    d = ImageDraw.Draw(canvas)
    lines = headline.split("\n")
    line_h = head_f.getbbox("가")[3] + 22
    sub_h = sub_f.getbbox("가")[3]
    block_h = line_h*len(lines) + 30 + sub_h
    y = max(110, (CAPTION_H - block_h)//2)
    for ln in lines:
        tw = d.textlength(ln, font=head_f)
        d.text(((W-tw)/2, y), ln, font=head_f, fill=(255,255,255), stroke_width=1, stroke_fill=(255,255,255))
        y += line_h
    y += 22
    tw = d.textlength(sub, font=sub_f)
    d.text(((W-tw)/2, y), sub, font=sub_f, fill=(238,241,255))

    out_path = os.path.join(OUT, f"{num:02d}.png")
    canvas.convert("RGB").save(out_path, "PNG")
    print("saved", os.path.basename(out_path), f"{sw}x{sh}")
print("DONE ->", OUT)
