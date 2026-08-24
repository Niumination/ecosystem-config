#!/usr/bin/env python3
"""Kalkulator kontras WCAG 2.1 — relative luminance + grade.

Usage:
  python3 wcag-contrast.py f1f5f9 050811          # hex pair
  python3 wcag-contrast.py --batch                # contoh token dark theme
  python3 wcag-contrast.py 22,32,54 5,8,17        # rgb triplets

Grade (WCAG 2.1 AA/AAA):
  - Teks normal:  AA >=4.5 | AAA >=7
  - Teks besar (>=18.66px bold / >=24px): AA >=3 | AAA >=4.5
  - UI component / ikon / batas: >=3
"""
import sys


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(rgb):
    r, g, b = (_lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    l1, l2 = lum(a), lum(b)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def parse(s):
    s = s.strip().lstrip('#')
    if ',' in s:
        return tuple(int(x) for x in s.split(',')[:3])
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def grade(c):
    return '✅' if c >= 4.5 else ('⚠️' if c >= 3 else '❌')


def main():
    if '--batch' in sys.argv:
        bg = parse('050811')
        pairs = [
            ('teks utama #f1f5f9', 'f1f5f9'),
            ('teks sekunder #94a3b8', '94a3b8'),
            ('teks muted #7c8ba0', '7c8ba0'),
            ('cyan #00f0ff', '00f0ff'),
            ('amber #ffb800', 'ffb800'),
            ('emerald #00ff87', '00ff87'),
            ('red #ff3366', 'ff3366'),
            ('blue #3b82f6', '3b82f6'),
            ('purple #8b5cf6', '8b5cf6'),
        ]
        for name, fg in pairs:
            c = contrast(parse(fg), bg)
            print(f'{grade(c)} {c:5.2f}:1  {name} on #{bg[0]:02x}{bg[1]:02x}{bg[2]:02x}')
        return
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    fg, bg = parse(sys.argv[1]), parse(sys.argv[2])
    c = contrast(fg, bg)
    print(f'{grade(c)} {c:.2f}:1  fg #{sys.argv[1].lstrip("#")} on bg #{sys.argv[2].lstrip("#")}')
    print('AA teks normal >=4.5 | besar >=3 | UI/ikon >=3 | AAA >=7')
    return 0


if __name__ == '__main__':
    sys.exit(main())
