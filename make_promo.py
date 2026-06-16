#!/usr/bin/env python3
# AI 글벗 App Store 홍보 이미지 생성 (6.5" 규격 1242x2688): 스크린샷 + 헤드라인/서브카피 + 브랜드 그라데이션.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "/Users/jmwfdisk/Library/Mobile Documents/com~apple~CloudDocs/앱 개발/Ai 글벗/AI 글벗 스크린샷"
OUT = os.path.join(SRC, "promo")
os.makedirs(OUT, exist_ok=True)

W, H = 1242, 2688          # App Store 6.5" 디스플레이
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

def font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size, index=0)
    except Exception:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", size)

# (파일명, 출력순번, 헤드라인, 서브카피, 그라데이션 상색, 하색)
ITEMS = [
    ("스크린샷, 2026-06-17 00.11.38.png", 1, "녹음하면\n회의록이 완성됩니다", "통화·회의를 자동 요약하고 할 일·일정까지 정리", (0x5B,0x6C,0xFF), (0x35,0x3E,0xB0)),
    ("스크린샷, 2026-06-17 00.14.04.png", 2, "회의·강의·인터뷰\n상황별 AI 녹음", "목적에 맞는 모드로 더 정확하게 요약", (0xFF,0x8A,0x4B), (0xC2,0x4E,0x3A)),
    ("스크린샷, 2026-06-17 00.12.11.png", 3, "긴 문서도\n물어보면 답이 나와요", "공문서식 번호까지 깔끔하게 정리된 AI 답변", (0x4F,0x8C,0xFF), (0x2C,0x55,0xB8)),
    ("스크린샷, 2026-06-17 00.13.20.png", 4, "문서의 핵심만\n3초 만에", "요약·핵심 포인트·근거 페이지까지 한 번에", (0x5B,0x6C,0xE0), (0x35,0x3E,0xB0)),
    ("스크린샷, 2026-06-17 00.12.25.png", 5, "사진·파일을\n그대로 첨부해 질문", "카메라·사진·문서를 올려 바로 대화", (0x32,0xB8,0x8A), (0x1C,0x6E,0x55)),
    ("스크린샷, 2026-06-17 00.12.44.png", 6, "여러 문서를 묶어\n한 번에 질문", "관련 자료를 모아 프로젝트로 대화", (0x6B,0x6B,0xF2), (0x44,0x3A,0xA0)),
    ("스크린샷, 2026-06-17 00.14.23.png", 7, "내 녹음을\n한곳에서 관리", "즐겨찾기·폴더로 깔끔하게 정리", (0x5B,0x6C,0xFF), (0x2E,0x37,0x9C)),
    ("스크린샷, 2026-06-17 00.14.35.png", 8, "녹음·문서·프로젝트\n한눈에", "내 모든 자료를 현황 한 화면에서", (0x4F,0x8C,0xFF), (0x2C,0x55,0xB8)),
    ("스크린샷, 2026-06-17 00.14.56.png", 9, "로컬은 무료·오프라인\n클라우드는 고품질", "문서·음성 각각 AI 엔진을 선택하세요", (0x32,0xB8,0x8A), (0x24,0x4A,0x9A)),
    ("스크린샷, 2026-06-17 00.15.40.png", 10, "내 취향대로\n테마까지", "라이트·다크 배경 테마와 글자 크기 조절", (0x8E,0x7B,0xF2), (0x4A,0x3A,0xA0)),
]

def gradient(top, bottom):
    img = Image.new("RGB", (W, H), top)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        r = int(top[0] + (bottom[0]-top[0]) * t)
        g = int(top[1] + (bottom[1]-top[1]) * t)
        b = int(top[2] + (bottom[2]-top[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    return img

def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0], img.size[1]], radius=radius, fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out

CAPTION_H = 430
BOTTOM_MARGIN = 52
head_f = font(86)
sub_f = font(43)

for fn, num, headline, sub, top, bottom in ITEMS:
    canvas = gradient(top, bottom)

    shot = Image.open(os.path.join(SRC, fn)).convert("RGB")
    target_h = H - CAPTION_H - BOTTOM_MARGIN
    scale = target_h / shot.height
    sw, sh = int(shot.width * scale), int(shot.height * scale)
    if sw > W - 80:                       # 폭이 넘치면 폭 기준으로 다시 맞춤
        scale = (W - 80) / shot.width
        sw, sh = int(shot.width * scale), int(shot.height * scale)
    shot = shot.resize((sw, sh), Image.LANCZOS)
    radius = int(56 * scale)
    shot_r = rounded(shot, radius)
    sx = (W - sw) // 2
    sy = H - BOTTOM_MARGIN - sh           # 하단 정렬

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([sx, sy+12, sx+sw, sy+sh+12], radius=radius, fill=(0,0,0,110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow)
    canvas.paste(shot_r, (sx, sy), shot_r)

    d = ImageDraw.Draw(canvas)
    lines = headline.split("\n")
    line_h = head_f.getbbox("가")[3] + 16
    sub_h = sub_f.getbbox("가")[3]
    block_h = line_h * len(lines) + 22 + sub_h
    y = max(80, (CAPTION_H - block_h) // 2)
    for ln in lines:
        tw = d.textlength(ln, font=head_f)
        d.text(((W - tw) / 2, y), ln, font=head_f, fill=(255,255,255), stroke_width=1, stroke_fill=(255,255,255))
        y += line_h
    y += 16
    tw = d.textlength(sub, font=sub_f)
    d.text(((W - tw) / 2, y), sub, font=sub_f, fill=(238,241,255))

    out_path = os.path.join(OUT, f"{num:02d}.png")
    canvas.convert("RGB").save(out_path, "PNG")
    print("saved", out_path, f"{sw}x{sh}")

print("DONE ->", OUT)
