#!/usr/bin/env python3
"""SRT -> styled ASS for burning with ffmpeg's ass filter. Text and timing are never changed.

  python scripts/subtitle_styles.py 成片.srt -o 字幕.ass --style highlight --size 1080x1920 \
      --font "Noto Sans SC" --highlights highlights.json
  ffmpeg -i in.mp4 -vf "ass=字幕.ass:fontsdir=fonts" ...

highlights.json: {"3": "200 块", "17": "上下文"}  (1-based screen number -> exact substring)
words.json (karaoke only): [[["你好", 0.04, 0.40], ["世界", 0.40, 0.90]], ...]  one list per screen, output-time seconds
"""
import argparse, json, re, sys

def bgr(hex_rgb, alpha=0):
    """'#FFD400' -> '&H00D400FF'-style ASS colour (alpha 0 = opaque)."""
    h = hex_rgb.lstrip('#')
    return '&H%02X%s%s%s' % (alpha, h[4:6], h[2:4], h[0:2])

# Sizes are fractions of the video width; outline/shadow are fractions of the font size.
STYLES = {
    'standard':  dict(desc='普通字幕：白字黑边淡阴影（默认）', size=.055, bold=1, outline=.05, shadow=.03,
                      text='#FFFFFF', edge='#141414', soft=False, box=False, anim=False, hl=None),
    'highlight': dict(desc='重点高亮：粗白字 + 柔和阴影，每屏最多一个黄色关键词，0.12 秒淡入上浮', size=.067, bold=1,
                      outline=.06, shadow=0, text='#FFFFFF', edge='#101010', soft=True, box=False, anim=True,
                      hl='#FFD400', hl_scale=115),
    'box':       dict(desc='半透明底条：背景花、描边压不住时用', size=.055, bold=1, outline=.18, shadow=0,
                      text='#FFFFFF', edge='#000000', edge_alpha=0x60, soft=False, box=True, anim=False, hl=None),
    'variety':   dict(desc='综艺大字：大字、粗彩色描边，关键词放大弹出', size=.072, bold=1, outline=.10, shadow=.04,
                      text='#FFFFFF', edge='#1D2B64', soft=False, box=False, anim=True, hl='#FFE14D', hl_scale=125,
                      pop=True),
    'minimal':   dict(desc='极简：细一点的字、无描边、只有柔和阴影，适合干净背景', size=.048, bold=0, outline=0,
                      shadow=0, text='#FFFFFF', edge='#000000', soft=True, box=False, anim=True, hl=None),
    'karaoke':   dict(desc='卡拉OK：说到哪个字哪个字变色（需要逐字时间）', size=.060, bold=1, outline=.06, shadow=.03,
                      text='#FFD400', edge='#101010', before='#FFFFFF', soft=False, box=False, anim=False, hl=None,
                      karaoke=True),
}

def parse_srt(text):
    out = []
    for block in re.split(r'\n\s*\n', text.replace('\r', '').strip()):
        lines = block.split('\n')
        m = next((re.match(r'(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)', l) for l in lines if '-->' in l), None)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        s = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        body = ' '.join(l for l in lines[lines.index(next(l for l in lines if '-->' in l)) + 1:] if l.strip())
        out.append((round(s, 3), round(e, 3), body))
    return out

def ts(t):
    cs = int(round(t * 100))
    return '%d:%02d:%02d.%02d' % (cs // 360000, cs // 6000 % 60, cs // 100 % 60, cs % 100)

def est_width(text, fs):
    """Rule from references/subtitles.md: CJK 1, Latin letters/digits 0.55, space 0.35 (em ~ 0.72 x ASS size)."""
    u = sum(.35 if c == ' ' else .55 if ord(c) < 128 else 1 for c in text)
    return u * fs * .72

def esc(t):
    return t.replace('{', '｛').replace('}', '｝').replace('\\', '＼')

def build(screens, style='standard', width=1080, height=1920, font='Noto Sans SC', bottom=.78,
          highlights=None, words=None):
    st = STYLES[style]
    fs = round(width * st['size'])
    ol = round(fs * st['outline'], 1)
    sh = round(fs * st['shadow'], 1)
    marginv = round(height * (1 - bottom))
    y, x = height - marginv, width // 2
    side = round(width * .05)
    highlights = {int(k): v for k, v in (highlights or {}).items()}
    if st.get('karaoke') and not words:
        raise SystemExit('karaoke 需要 --words（逐字时间），没有就换别的样式，不要平均分配假装逐字')
    edge_a = st.get('edge_alpha', 0)
    styles = ['Style: Main,%s,%d,%s,%s,%s,%s,%d,0,0,0,100,100,%d,0,%d,%s,%s,2,%d,%d,%d,1' % (
        font, fs, bgr(st['text']), bgr(st.get('before', st['text'])), bgr(st['edge'], edge_a), bgr('#000000', 0x80),
        -1 if st['bold'] else 0, round(fs * .02), 3 if st['box'] else 1, ol, sh, side, side, marginv)]
    if st['soft']:
        styles.append('Style: Soft,%s,%d,%s,%s,%s,&H00000000,%d,0,0,0,100,100,%d,0,1,%s,0,2,%d,%d,%d,1' % (
            font, fs, bgr('#000000', 0x70), bgr('#000000', 0x70), bgr('#000000', 0x70), -1 if st['bold'] else 0,
            round(fs * .02), max(ol, round(fs * .1, 1)), side, side, marginv))
    events, warnings, used = [], [], 0
    for i, (s, e, text) in enumerate(screens, 1):
        if est_width(text, fs) > width - 2 * side:
            warnings.append('第 %d 屏可能超宽：%s（按 subtitles.md 拆屏，不要缩字号）' % (i, text))
        if st['anim']:
            rise = round(fs * .14)
            tag = r'\move(%d,%d,%d,%d,0,120)\fad(120,0)' % (x, y + rise, x, y)
            soft_tag = r'\move(%d,%d,%d,%d,0,120)\fad(120,0)' % (x, y + rise + round(fs * .07), x, y + round(fs * .07))
        else:
            tag, soft_tag = r'\pos(%d,%d)' % (x, y), r'\pos(%d,%d)' % (x, y + round(fs * .07))
        if st.get('karaoke'):
            screen = words[i - 1] if i <= len(words) else []
            if ''.join(w for w, _, _ in screen) != text:
                raise SystemExit('第 %d 屏的逐字时间和 SRT 文字对不上，先改 --words 再做卡拉OK' % i)
            # Emit each gap as a silent \k so highlights follow the absolute word times.
            body, cursor = '', s
            for w, ws, we in screen:
                gap = round((ws - cursor) * 100)
                if gap > 0:
                    body += r'{\k%d}' % gap
                body += r'{\kf%d}%s' % (max(1, round((we - ws) * 100)), esc(w))
                cursor = max(cursor, we)
            plain = esc(text)
        else:
            w = highlights.get(i) if st['hl'] else None
            if w and w in text:
                a, b = text.split(w, 1)
                sc = st['hl_scale']
                pop = r'\t(0,150,\fscx%d\fscy%d)' % (sc, sc) if st.get('pop') else ''
                start = sc + 15 if st.get('pop') else sc
                body = (esc(a) + r'{\c%s\fscx%d\fscy%d%s}' % (bgr(st['hl']), start, start, pop) + esc(w)
                        + r'{\c%s\fscx100\fscy100}' % bgr(st['text']) + esc(b))
                plain = (esc(a) + r'{\fscx%d\fscy%d}' % (sc, sc) + esc(w) + r'{\fscx100\fscy100}' + esc(b))
                used += 1
            else:
                if w:
                    warnings.append('第 %d 屏没有找到高亮词“%s”，已跳过' % (i, w))
                body = plain = esc(text)
        if st['soft']:
            events.append('Dialogue: 0,%s,%s,Soft,,0,0,0,,{\\an2\\blur%d%s}%s' % (ts(s), ts(e), max(4, fs // 12), soft_tag, plain))
        events.append('Dialogue: 1,%s,%s,Main,,0,0,0,,{\\an2\\blur0.6%s}%s' % (ts(s), ts(e), tag, body))
    head = ('[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\nWrapStyle: 2\nScaledBorderAndShadow: yes\n'
            'YCbCr Matrix: TV.709\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, '
            'OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, '
            'Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n%s\n\n[Events]\nFormat: Layer, Start, End, '
            'Style, Name, MarginL, MarginR, MarginV, Effect, Text\n') % (width, height, '\n'.join(styles))
    return head + '\n'.join(events) + '\n', warnings, used

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('srt', nargs='?'); p.add_argument('-o', '--out')
    p.add_argument('--style', default='standard', choices=sorted(STYLES))
    p.add_argument('--size', default='1080x1920', help='视频宽x高')
    p.add_argument('--font', default='Noto Sans SC', help='字体族名（ffmpeg ass 滤镜用 fontsdir 指向字体文件夹）')
    p.add_argument('--bottom', type=float, default=.78, help='字幕底边在画面高度的位置，0–1；不要进最下面约 18%%')
    p.add_argument('--highlights'); p.add_argument('--words')
    p.add_argument('--list', action='store_true', help='列出样式')
    a = p.parse_args(argv)
    if a.list:
        for k, v in STYLES.items():
            print('%-10s %s' % (k, v['desc']))
        return
    if not a.srt or not a.out:
        p.error('需要 SRT 文件和 -o 输出路径')
    if a.bottom > .82:
        p.error('--bottom 超过 0.82 会进平台按钮区')
    w, h = (int(v) for v in a.size.lower().split('x'))
    load = lambda f: json.load(open(f, encoding='utf-8')) if f else None
    ass, warnings, used = build(parse_srt(open(a.srt, encoding='utf-8-sig').read()), a.style, w, h, a.font, a.bottom,
                                load(a.highlights), load(a.words))
    open(a.out, 'w', encoding='utf-8-sig').write(ass)
    for msg in warnings:
        print(msg, file=sys.stderr)
    print('wrote %s (%s, %d highlighted)' % (a.out, a.style, used))

if __name__ == '__main__':
    main()
