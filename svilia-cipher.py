#!/usr/bin/env python3
"""
 _____ _   _ ___ _     ___    _    ____ ___ ____  _   _ _____ ____
/ ____| \ | |_ _| |   |_ _|  / \  / ___|_ _|  _ \| | | | ____|  _ \\
\___ \|  \| || || |    | |  / _ \| |    | || |_) | |_| |  _| | |_) |
 ___) | |\  || || |___ | | / ___ \ |___ | ||  __/|  _  | |___|  _ <
|____/|_| \_|___|_____|___/_/   \_\____|___|_|   |_| |_|_____|_| \_\\

                  ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗
                 ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗
                 ██║     ██║██████╔╝███████║█████╗  ██████╔╝
                 ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
                 ╚██████╗██║██║     ██║  ██║███████╗██║  ██║
                  ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

         Classical Cryptography Terminal Suite  |  v1.0.0
         Caesar · Vigenère · Atbash · Rail Fence · Beaufort
         Playfair · ROT13 · Columnar · Frequency Analysis
"""

import curses
import curses.textpad
import time
import sys
import os
import math
import random
import string
import json
import re
import argparse
from collections import Counter

# ─────────────────────────────────────────────────────────────────────────────
#  ENGLISH FREQUENCY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

ENGLISH_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
    'z': 0.074
}

COMMON_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it',
    'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this',
    'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or',
    'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'is', 'are', 'was', 'were', 'has', 'had', 'been', 'can', 'could',
}


def english_score(text: str) -> float:
    """Score how English-like a text is (higher = more English)."""
    text_lower = text.lower()
    letters = [c for c in text_lower if c.isalpha()]
    if not letters:
        return 0.0

    # Frequency score
    counts = Counter(letters)
    total = len(letters)
    freq_score = 0.0
    for char, count in counts.items():
        expected = ENGLISH_FREQ.get(char, 0.1)
        actual = (count / total) * 100
        freq_score -= abs(expected - actual)

    # Word bonus
    words = re.findall(r'[a-z]+', text_lower)
    word_bonus = sum(3 for w in words if w in COMMON_WORDS)

    return freq_score + word_bonus


def index_of_coincidence(text: str) -> float:
    """Calculate Index of Coincidence."""
    letters = [c.upper() for c in text if c.isalpha()]
    n = len(letters)
    if n < 2:
        return 0.0
    counts = Counter(letters)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator if denominator else 0.0


def frequency_analysis(text: str) -> list:
    """Return sorted letter frequency list."""
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters)
    if not total:
        return []
    counts = Counter(letters)
    result = []
    for ch in string.ascii_uppercase:
        cnt = counts.get(ch, 0)
        pct = (cnt / total) * 100
        expected = ENGLISH_FREQ.get(ch.lower(), 0)
        result.append((ch, cnt, pct, expected))
    result.sort(key=lambda x: -x[2])
    return result


# ─────────────────────────────────────────────────────────────────────────────
#  CIPHER ENGINES
# ─────────────────────────────────────────────────────────────────────────────

class CaesarCipher:
    NAME = "Caesar"
    DESC = "Shifts each letter by a fixed amount (key: 0-25)"
    KEY_TYPE = "number"
    KEY_HELP = "Enter shift amount (0-25)"

    @staticmethod
    def encrypt(text: str, key) -> str:
        k = int(key) % 26
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base + k) % 26 + base))
            else:
                result.append(ch)
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key) -> str:
        return CaesarCipher.encrypt(text, -int(key))

    @staticmethod
    def brute_force(text: str):
        results = []
        for k in range(26):
            dec = CaesarCipher.decrypt(text, k)
            score = english_score(dec)
            results.append((str(k), dec, score))
        results.sort(key=lambda x: -x[2])
        return results

    @staticmethod
    def crack(text: str):
        return CaesarCipher.brute_force(text)[0]


class Rot13Cipher:
    NAME = "ROT13"
    DESC = "Caesar with fixed key 13 (symmetric — encrypt = decrypt)"
    KEY_TYPE = "none"
    KEY_HELP = "No key needed"

    @staticmethod
    def encrypt(text: str, key=None) -> str:
        return CaesarCipher.encrypt(text, 13)

    @staticmethod
    def decrypt(text: str, key=None) -> str:
        return CaesarCipher.encrypt(text, 13)

    @staticmethod
    def brute_force(text: str):
        return [("13", Rot13Cipher.decrypt(text), 100.0)]

    @staticmethod
    def crack(text: str):
        return ("13", Rot13Cipher.decrypt(text), 100.0)


class AtbashCipher:
    NAME = "Atbash"
    DESC = "Mirrors alphabet A↔Z B↔Y… (Hebrew origin, symmetric)"
    KEY_TYPE = "none"
    KEY_HELP = "No key needed"

    @staticmethod
    def encrypt(text: str, key=None) -> str:
        result = []
        for ch in text:
            if ch.isalpha():
                if ch.isupper():
                    result.append(chr(ord('Z') - (ord(ch) - ord('A'))))
                else:
                    result.append(chr(ord('z') - (ord(ch) - ord('a'))))
            else:
                result.append(ch)
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key=None) -> str:
        return AtbashCipher.encrypt(text)

    @staticmethod
    def brute_force(text: str):
        dec = AtbashCipher.decrypt(text)
        return [("N/A", dec, english_score(dec))]

    @staticmethod
    def crack(text: str):
        return AtbashCipher.brute_force(text)[0]


class VigenereCipher:
    NAME = "Vigenère"
    DESC = "Polyalphabetic substitution using a keyword (key: word)"
    KEY_TYPE = "text"
    KEY_HELP = "Enter keyword (letters only, e.g. SECRET)"

    @staticmethod
    def _process(text: str, key: str, decrypt=False) -> str:
        key = re.sub(r'[^a-zA-Z]', '', key).upper()
        if not key:
            return text
        result = []
        ki = 0
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                shift = ord(key[ki % len(key)]) - ord('A')
                if decrypt:
                    shift = -shift
                result.append(chr((ord(ch) - base + shift) % 26 + base))
                ki += 1
            else:
                result.append(ch)
        return ''.join(result)

    @staticmethod
    def encrypt(text: str, key) -> str:
        return VigenereCipher._process(text, str(key))

    @staticmethod
    def decrypt(text: str, key) -> str:
        return VigenereCipher._process(text, str(key), decrypt=True)

    @staticmethod
    def _kasiski_key_length(text: str) -> list:
        """Estimate key length via Kasiski examination."""
        letters = re.sub(r'[^A-Za-z]', '', text).upper()
        spacings = []
        for length in range(3, 6):
            for i in range(len(letters) - length):
                seq = letters[i:i+length]
                for j in range(i+1, len(letters) - length):
                    if letters[j:j+length] == seq:
                        spacings.append(j - i)
        if not spacings:
            return [3, 4, 5, 6]
        # GCD-based guesses
        from math import gcd
        from functools import reduce
        candidates = []
        for k in range(2, 13):
            score = sum(1 for s in spacings if s % k == 0)
            candidates.append((k, score))
        candidates.sort(key=lambda x: -x[1])
        return [c[0] for c in candidates[:5]]

    @staticmethod
    def brute_force(text: str, max_keylen=8):
        letters = re.sub(r'[^A-Za-z]', '', text).upper()
        results = []
        key_lengths = VigenereCipher._kasiski_key_length(text)
        # Also try lengths 2-max_keylen
        for kl in range(2, max_keylen + 1):
            if kl not in key_lengths:
                key_lengths.append(kl)

        for kl in key_lengths[:8]:
            # For each key length, crack each column with Caesar
            key_chars = []
            for col in range(kl):
                column = letters[col::kl]
                best_shift = 0
                best_score = float('-inf')
                for shift in range(26):
                    dec = CaesarCipher.decrypt(column, shift)
                    score = english_score(dec)
                    if score > best_score:
                        best_score = score
                        best_shift = shift
                key_chars.append(chr(best_shift + ord('A')))
            guessed_key = ''.join(key_chars)
            decrypted = VigenereCipher.decrypt(text, guessed_key)
            score = english_score(decrypted)
            results.append((guessed_key, decrypted, score))

        results.sort(key=lambda x: -x[2])
        return results[:10]

    @staticmethod
    def crack(text: str):
        results = VigenereCipher.brute_force(text)
        return results[0] if results else ("?", text, 0)


class BeaufortCipher:
    NAME = "Beaufort"
    DESC = "Similar to Vigenère but uses subtraction (key: word)"
    KEY_TYPE = "text"
    KEY_HELP = "Enter keyword (letters only)"

    @staticmethod
    def encrypt(text: str, key) -> str:
        key = re.sub(r'[^a-zA-Z]', '', str(key)).upper()
        if not key:
            return text
        result = []
        ki = 0
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                shift = ord(key[ki % len(key)]) - ord('A')
                enc = (shift - (ord(ch.upper()) - ord('A'))) % 26
                out = chr(enc + (ord('A') if ch.isupper() else ord('a')))
                result.append(out)
                ki += 1
            else:
                result.append(ch)
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key) -> str:
        return BeaufortCipher.encrypt(text, key)

    @staticmethod
    def brute_force(text: str):
        return VigenereCipher.brute_force(text)

    @staticmethod
    def crack(text: str):
        results = BeaufortCipher.brute_force(text)
        return results[0] if results else ("?", text, 0)


class RailFenceCipher:
    NAME = "Rail Fence"
    DESC = "Writes text in zigzag across N rails (key: number of rails)"
    KEY_TYPE = "number"
    KEY_HELP = "Enter number of rails (2-10)"

    @staticmethod
    def encrypt(text: str, key) -> str:
        rails = max(2, int(key))
        fence = [[] for _ in range(rails)]
        rail, direction = 0, 1
        for ch in text:
            fence[rail].append(ch)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        return ''.join(''.join(r) for r in fence)

    @staticmethod
    def decrypt(text: str, key) -> str:
        rails = max(2, int(key))
        n = len(text)
        pattern = []
        rail, direction = 0, 1
        for i in range(n):
            pattern.append(rail)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        indices = sorted(range(n), key=lambda i: (pattern[i], i))
        result = [''] * n
        for i, ch in zip(indices, text):
            result[i] = ch
        return ''.join(result)

    @staticmethod
    def brute_force(text: str):
        results = []
        for k in range(2, min(len(text) // 2 + 1, 15)):
            dec = RailFenceCipher.decrypt(text, k)
            score = english_score(dec)
            results.append((str(k), dec, score))
        results.sort(key=lambda x: -x[2])
        return results[:10]

    @staticmethod
    def crack(text: str):
        results = RailFenceCipher.brute_force(text)
        return results[0] if results else ("2", text, 0)


class ColumnarCipher:
    NAME = "Columnar"
    DESC = "Writes text in rows, reads columns in key-sorted order"
    KEY_TYPE = "text"
    KEY_HELP = "Enter keyword (letters only, e.g. ZEBRA)"

    @staticmethod
    def _col_order(key: str) -> list:
        key = re.sub(r'[^a-zA-Z]', '', key).upper()
        return sorted(range(len(key)), key=lambda i: key[i])

    @staticmethod
    def encrypt(text: str, key) -> str:
        key = re.sub(r'[^a-zA-Z]', '', str(key)).upper()
        if not key:
            return text
        num_cols = len(key)
        # Pad text
        padding = (num_cols - len(text) % num_cols) % num_cols
        padded = text + 'X' * padding
        num_rows = len(padded) // num_cols
        grid = [padded[i*num_cols:(i+1)*num_cols] for i in range(num_rows)]
        order = ColumnarCipher._col_order(key)
        result = []
        for col in order:
            for row in grid:
                result.append(row[col])
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key) -> str:
        key = re.sub(r'[^a-zA-Z]', '', str(key)).upper()
        if not key:
            return text
        num_cols = len(key)
        num_rows = math.ceil(len(text) / num_cols)
        order = ColumnarCipher._col_order(key)
        col_len = num_rows
        grid = {}
        idx = 0
        for col in order:
            grid[col] = list(text[idx:idx+col_len])
            idx += col_len
        result = []
        for row in range(num_rows):
            for col in range(num_cols):
                if row < len(grid[col]):
                    result.append(grid[col][row])
        return ''.join(result).rstrip('X')

    @staticmethod
    def brute_force(text: str):
        return [("N/A", text, 0.0)]

    @staticmethod
    def crack(text: str):
        return ("N/A", text, 0.0)


class PlayfairCipher:
    NAME = "Playfair"
    DESC = "Digraph substitution using a 5×5 key matrix"
    KEY_TYPE = "text"
    KEY_HELP = "Enter keyword (e.g. MONARCHY)"

    @staticmethod
    def _build_matrix(key: str) -> list:
        key = re.sub(r'[^a-zA-Z]', '', key).upper().replace('J', 'I')
        seen = []
        for ch in key + string.ascii_uppercase.replace('J', ''):
            if ch not in seen:
                seen.append(ch)
        return [seen[i*5:(i+1)*5] for i in range(5)]

    @staticmethod
    def _pos(matrix, ch):
        ch = ch.upper().replace('J', 'I')
        for r, row in enumerate(matrix):
            if ch in row:
                return r, row.index(ch)
        return 0, 0

    @staticmethod
    def _prepare(text: str) -> list:
        text = re.sub(r'[^a-zA-Z]', '', text).upper().replace('J', 'I')
        pairs = []
        i = 0
        while i < len(text):
            a = text[i]
            if i + 1 >= len(text):
                pairs.append((a, 'X'))
                i += 1
            elif text[i] == text[i+1]:
                pairs.append((a, 'X'))
                i += 1
            else:
                pairs.append((a, text[i+1]))
                i += 2
        return pairs

    @staticmethod
    def encrypt(text: str, key) -> str:
        matrix = PlayfairCipher._build_matrix(str(key))
        pairs = PlayfairCipher._prepare(text)
        result = []
        for a, b in pairs:
            r1, c1 = PlayfairCipher._pos(matrix, a)
            r2, c2 = PlayfairCipher._pos(matrix, b)
            if r1 == r2:
                result += [matrix[r1][(c1+1)%5], matrix[r2][(c2+1)%5]]
            elif c1 == c2:
                result += [matrix[(r1+1)%5][c1], matrix[(r2+1)%5][c2]]
            else:
                result += [matrix[r1][c2], matrix[r2][c1]]
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key) -> str:
        matrix = PlayfairCipher._build_matrix(str(key))
        text = re.sub(r'[^a-zA-Z]', '', text).upper()
        pairs = [(text[i], text[i+1]) for i in range(0, len(text)-1, 2)]
        result = []
        for a, b in pairs:
            r1, c1 = PlayfairCipher._pos(matrix, a)
            r2, c2 = PlayfairCipher._pos(matrix, b)
            if r1 == r2:
                result += [matrix[r1][(c1-1)%5], matrix[r2][(c2-1)%5]]
            elif c1 == c2:
                result += [matrix[(r1-1)%5][c1], matrix[(r2-1)%5][c2]]
            else:
                result += [matrix[r1][c2], matrix[r2][c1]]
        return ''.join(result)

    @staticmethod
    def brute_force(text: str):
        return [("N/A (requires key)", text, 0.0)]

    @staticmethod
    def crack(text: str):
        return ("N/A", text, 0.0)


# ─────────────────────────────────────────────────────────────────────────────
#  CIPHER REGISTRY
# ─────────────────────────────────────────────────────────────────────────────

CIPHERS = [
    CaesarCipher,
    Rot13Cipher,
    AtbashCipher,
    VigenereCipher,
    BeaufortCipher,
    RailFenceCipher,
    ColumnarCipher,
    PlayfairCipher,
]

# ─────────────────────────────────────────────────────────────────────────────
#  COLOR PALETTE
# ─────────────────────────────────────────────────────────────────────────────

# Color pair IDs
C_NORMAL     = 0
C_HEADER     = 1
C_ACCENT     = 2
C_SUCCESS    = 3
C_WARNING    = 4
C_ERROR      = 5
C_DIM        = 6
C_HIGHLIGHT  = 7
C_BORDER     = 8
C_TITLE      = 9
C_INPUT      = 10
C_MENU_SEL   = 11
C_CHART_BAR  = 12
C_CYAN       = 13

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(C_HEADER,    curses.COLOR_CYAN,    -1)
    curses.init_pair(C_ACCENT,    curses.COLOR_MAGENTA, -1)
    curses.init_pair(C_SUCCESS,   curses.COLOR_GREEN,   -1)
    curses.init_pair(C_WARNING,   curses.COLOR_YELLOW,  -1)
    curses.init_pair(C_ERROR,     curses.COLOR_RED,     -1)
    curses.init_pair(C_DIM,       8,                    -1)
    curses.init_pair(C_HIGHLIGHT, curses.COLOR_BLACK,   curses.COLOR_CYAN)
    curses.init_pair(C_BORDER,    curses.COLOR_CYAN,    -1)
    curses.init_pair(C_TITLE,     curses.COLOR_WHITE,   -1)
    curses.init_pair(C_INPUT,     curses.COLOR_GREEN,   -1)
    curses.init_pair(C_MENU_SEL,  curses.COLOR_BLACK,   curses.COLOR_MAGENTA)
    curses.init_pair(C_CHART_BAR, curses.COLOR_CYAN,    -1)
    curses.init_pair(C_CYAN,      curses.COLOR_CYAN,    -1)


# ─────────────────────────────────────────────────────────────────────────────
#  DRAWING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def safe_addstr(win, y, x, text, attr=0):
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x < 0 or x >= w:
        return
    max_len = w - x - 1
    if max_len <= 0:
        return
    try:
        win.addstr(y, x, text[:max_len], attr)
    except curses.error:
        pass


def draw_box(win, y, x, h, w, color_pair=C_BORDER, title=""):
    attr = curses.color_pair(color_pair)
    # Corners
    safe_addstr(win, y,     x,     "╔", attr)
    safe_addstr(win, y,     x+w-1, "╗", attr)
    safe_addstr(win, y+h-1, x,     "╚", attr)
    safe_addstr(win, y+h-1, x+w-1, "╝", attr)
    # Horizontal
    for i in range(1, w-1):
        safe_addstr(win, y,     x+i, "═", attr)
        safe_addstr(win, y+h-1, x+i, "═", attr)
    # Vertical
    for i in range(1, h-1):
        safe_addstr(win, y+i, x,     "║", attr)
        safe_addstr(win, y+i, x+w-1, "║", attr)
    # Title
    if title:
        title_str = f" {title} "
        tx = x + (w - len(title_str)) // 2
        safe_addstr(win, y, tx, title_str, attr | curses.A_BOLD)


def draw_hline(win, y, x, w, color_pair=C_BORDER):
    attr = curses.color_pair(color_pair)
    safe_addstr(win, y, x, "╠", attr)
    for i in range(1, w-1):
        safe_addstr(win, y, x+i, "═", attr)
    safe_addstr(win, y, x+w-1, "╣", attr)


def center_text(win, y, text, attr=0):
    h, w = win.getmaxyx()
    x = max(0, (w - len(text)) // 2)
    safe_addstr(win, y, x, text, attr)


def typewriter(win, y, x, text, attr=0, delay=0.02):
    for i, ch in enumerate(text):
        safe_addstr(win, y, x+i, ch, attr)
        win.refresh()
        time.sleep(delay)


# ─────────────────────────────────────────────────────────────────────────────
#  SPLASH SCREEN
# ─────────────────────────────────────────────────────────────────────────────

LOGO = [
    " ███████╗██╗   ██╗██╗██╗     ██╗ █████╗ ",
    " ██╔════╝██║   ██║██║██║     ██║██╔══██╗",
    " ███████╗██║   ██║██║██║     ██║███████║",
    " ╚════██║╚██╗ ██╔╝██║██║     ██║██╔══██║",
    " ███████║ ╚████╔╝ ██║███████╗██║██║  ██║",
    " ╚══════╝  ╚═══╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝",
]

LOGO2 = [
    "  ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ ",
    " ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗",
    " ██║     ██║██████╔╝███████║█████╗  ██████╔╝",
    " ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗",
    " ╚██████╗██║██║     ██║  ██║███████╗██║  ██║",
    "  ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
]


def splash_screen(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    total_lines = len(LOGO) + len(LOGO2) + 6
    start_y = max(0, (h - total_lines) // 2)

    colors = [C_CYAN, C_ACCENT, C_SUCCESS, C_WARNING, C_ERROR, C_CYAN]

    # Animate logo lines
    for i, line in enumerate(LOGO):
        color = curses.color_pair(colors[i % len(colors)]) | curses.A_BOLD
        cx = max(0, (w - len(line)) // 2)
        safe_addstr(stdscr, start_y + i, cx, line, color)
        stdscr.refresh()
        time.sleep(0.07)

    for i, line in enumerate(LOGO2):
        color = curses.color_pair(colors[(i+2) % len(colors)]) | curses.A_BOLD
        cx = max(0, (w - len(line)) // 2)
        safe_addstr(stdscr, start_y + len(LOGO) + i, cx, line, color)
        stdscr.refresh()
        time.sleep(0.07)

    subtitle = "Classical Cryptography Terminal Suite  |  v1.0.0"
    center_text(stdscr, start_y + len(LOGO) + len(LOGO2) + 1,
                subtitle, curses.color_pair(C_DIM))

    ciphers_line = "Caesar · Vigenère · Atbash · Rail Fence · Beaufort · Playfair · ROT13 · Columnar"
    center_text(stdscr, start_y + len(LOGO) + len(LOGO2) + 2,
                ciphers_line, curses.color_pair(C_DIM))

    prompt = "[ Press any key to enter ]"
    center_text(stdscr, start_y + len(LOGO) + len(LOGO2) + 4,
                prompt, curses.color_pair(C_ACCENT) | curses.A_BLINK)
    stdscr.refresh()

    # Glitch animation
    for _ in range(8):
        glitch_chars = "!@#$%^&*<>?/\\|~`"
        gx = random.randint(0, max(1, w-20))
        gy = random.randint(start_y, start_y + len(LOGO) + len(LOGO2) - 1)
        safe_addstr(stdscr, gy, gx,
                    ''.join(random.choice(glitch_chars) for _ in range(random.randint(2,8))),
                    curses.color_pair(C_ERROR) | curses.A_DIM)
        stdscr.refresh()
        time.sleep(0.06)

    stdscr.getch()


# ─────────────────────────────────────────────────────────────────────────────
#  INPUT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_input(win, prompt, y, x, max_len=60, color=C_INPUT, secret=False):
    """Single-line input field with backspace support."""
    curses.curs_set(1)
    safe_addstr(win, y, x, prompt, curses.color_pair(C_ACCENT) | curses.A_BOLD)
    ix = x + len(prompt)
    buf = []

    while True:
        # Draw input field
        field_str = ('*' * len(buf) if secret else ''.join(buf))
        field_display = field_str[-max_len:] if len(field_str) > max_len else field_str
        safe_addstr(win, y, ix, field_display + ' ' * (max_len - len(field_display)),
                    curses.color_pair(color) | curses.A_UNDERLINE)
        win.move(y, ix + len(field_display))
        win.refresh()

        ch = win.getch()
        if ch in (curses.KEY_ENTER, 10, 13):
            break
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if buf:
                buf.pop()
        elif ch == 27:  # ESC
            curses.curs_set(0)
            return None
        elif 32 <= ch <= 126:
            buf.append(chr(ch))

    curses.curs_set(0)
    return ''.join(buf)


def get_multiline_input(win, prompt, y, x, box_h, box_w):
    """Multi-line text area."""
    curses.curs_set(1)
    draw_box(win, y-1, x-1, box_h+2, box_w+2, C_BORDER, prompt)
    lines = [""]
    cur_line = 0
    cur_col = 0
    scroll_offset = 0

    while True:
        # Render visible lines
        for i in range(box_h):
            li = i + scroll_offset
            line = lines[li] if li < len(lines) else ""
            display = line[:box_w]
            safe_addstr(win, y+i, x, display + ' ' * (box_w - len(display)),
                        curses.color_pair(C_INPUT))

        # Move cursor
        vis_line = cur_line - scroll_offset
        if 0 <= vis_line < box_h:
            win.move(y + vis_line, x + min(cur_col, box_w-1))
        win.refresh()

        ch = win.getch()
        if ch == 27:  # ESC = cancel
            curses.curs_set(0)
            return None
        elif ch in (curses.KEY_ENTER, 10, 13):
            if len(lines) < 50:
                rest = lines[cur_line][cur_col:]
                lines[cur_line] = lines[cur_line][:cur_col]
                cur_line += 1
                lines.insert(cur_line, rest)
                cur_col = 0
                if cur_line - scroll_offset >= box_h:
                    scroll_offset += 1
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if cur_col > 0:
                lines[cur_line] = lines[cur_line][:cur_col-1] + lines[cur_line][cur_col:]
                cur_col -= 1
            elif cur_line > 0:
                prev_len = len(lines[cur_line-1])
                lines[cur_line-1] += lines[cur_line]
                lines.pop(cur_line)
                cur_line -= 1
                cur_col = prev_len
                if cur_line < scroll_offset:
                    scroll_offset = max(0, scroll_offset-1)
        elif ch == curses.KEY_UP:
            if cur_line > 0:
                cur_line -= 1
                cur_col = min(cur_col, len(lines[cur_line]))
                if cur_line < scroll_offset:
                    scroll_offset -= 1
        elif ch == curses.KEY_DOWN:
            if cur_line < len(lines)-1:
                cur_line += 1
                cur_col = min(cur_col, len(lines[cur_line]))
                if cur_line - scroll_offset >= box_h:
                    scroll_offset += 1
        elif ch == curses.KEY_LEFT:
            if cur_col > 0:
                cur_col -= 1
        elif ch == curses.KEY_RIGHT:
            if cur_col < len(lines[cur_line]):
                cur_col += 1
        elif ch == curses.KEY_F10:
            break  # Submit
        elif 32 <= ch <= 126:
            lines[cur_line] = lines[cur_line][:cur_col] + chr(ch) + lines[cur_line][cur_col:]
            cur_col += 1
            if cur_col > box_w:
                # Word wrap
                pass

    curses.curs_set(0)
    return '\n'.join(lines).rstrip('\n')


# ─────────────────────────────────────────────────────────────────────────────
#  PANELS
# ─────────────────────────────────────────────────────────────────────────────

def draw_status_bar(win, msg, color=C_DIM):
    h, w = win.getmaxyx()
    bar = f" {msg} "
    bar = bar + " " * (w - len(bar))
    safe_addstr(win, h-1, 0, bar[:w-1], curses.color_pair(color) | curses.A_REVERSE)


def draw_header(win, title="SVILIA CIPHER"):
    h, w = win.getmaxyx()
    header = f"  ⚔  {title}  ⚔  "
    padding = " " * ((w - len(header)) // 2)
    full = (padding + header + padding)[:w-1]
    safe_addstr(win, 0, 0, full, curses.color_pair(C_HEADER) | curses.A_BOLD | curses.A_REVERSE)


def show_result_panel(stdscr, title, content_lines, status=""):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    draw_header(stdscr, title)
    draw_box(stdscr, 1, 0, h-2, w, C_BORDER)

    max_display = h - 6
    scroll = 0
    total = len(content_lines)

    while True:
        # Clear content area
        for i in range(2, h-3):
            safe_addstr(stdscr, i, 1, " " * (w-2))

        # Draw lines
        for i in range(min(max_display, total - scroll)):
            li = i + scroll
            if li < total:
                line, color, bold = content_lines[li]
                attr = curses.color_pair(color)
                if bold:
                    attr |= curses.A_BOLD
                safe_addstr(stdscr, i+2, 2, line[:w-4], attr)

        # Scroll indicator
        if total > max_display:
            pct = int((scroll / (total - max_display)) * 100)
            scroll_msg = f" [{scroll+1}-{min(scroll+max_display, total)}/{total}] {pct}% "
            safe_addstr(stdscr, h-3, w-len(scroll_msg)-2, scroll_msg, curses.color_pair(C_DIM))

        if status:
            draw_status_bar(stdscr, status + "  |  ↑↓ Scroll  |  Q Quit", C_DIM)
        else:
            draw_status_bar(stdscr, "↑↓ Scroll  |  Q/ESC Quit  |  C Copy text", C_DIM)

        stdscr.refresh()
        ch = stdscr.getch()
        if ch in (ord('q'), ord('Q'), 27):
            break
        elif ch == curses.KEY_UP and scroll > 0:
            scroll -= 1
        elif ch == curses.KEY_DOWN and scroll < total - max_display:
            scroll += 1
        elif ch == curses.KEY_PPAGE:
            scroll = max(0, scroll - max_display)
        elif ch == curses.KEY_NPAGE:
            scroll = min(max(0, total - max_display), scroll + max_display)


# ─────────────────────────────────────────────────────────────────────────────
#  ENCRYPT / DECRYPT SCREEN
# ─────────────────────────────────────────────────────────────────────────────

def run_cipher_screen(stdscr, cipher_class, mode="encrypt"):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = f"{cipher_class.NAME} — {'ENCRYPT' if mode == 'encrypt' else 'DECRYPT'}"
    draw_header(stdscr, title)
    draw_box(stdscr, 1, 0, h-2, w, C_BORDER)

    safe_addstr(stdscr, 2, 2, f"Cipher: {cipher_class.NAME}", curses.color_pair(C_ACCENT) | curses.A_BOLD)
    safe_addstr(stdscr, 3, 2, f"Info:   {cipher_class.DESC}", curses.color_pair(C_DIM))

    draw_hline(stdscr, 4, 0, w, C_BORDER)

    # Get text input
    safe_addstr(stdscr, 5, 2, "Enter your text (multi-line, F10 to confirm, ESC to cancel):",
                curses.color_pair(C_WARNING) | curses.A_BOLD)

    input_h = min(8, h - 18)
    input_w = w - 8
    text = get_multiline_input(stdscr, "TEXT INPUT", 7, 4, input_h, input_w)
    if text is None:
        return

    # Get key if needed
    key = None
    if cipher_class.KEY_TYPE != "none":
        draw_hline(stdscr, 7 + input_h + 2, 0, w, C_BORDER)
        key = get_input(stdscr, f"Key ({cipher_class.KEY_HELP}): ",
                        7 + input_h + 4, 2, max_len=40)
        if key is None:
            return
        if cipher_class.KEY_TYPE == "number":
            try:
                key = int(key)
            except ValueError:
                draw_status_bar(stdscr, "Invalid key — must be a number. Press any key.", C_ERROR)
                stdscr.getch()
                return

    # Process
    try:
        if mode == "encrypt":
            result = cipher_class.encrypt(text, key)
        else:
            result = cipher_class.decrypt(text, key)
    except Exception as e:
        draw_status_bar(stdscr, f"Error: {e}  Press any key.", C_ERROR)
        stdscr.getch()
        return

    # Show result
    lines = []
    lines.append(("━" * (w - 4), C_BORDER, False))
    lines.append((f"  MODE:    {'ENCRYPT' if mode == 'encrypt' else 'DECRYPT'}", C_ACCENT, True))
    lines.append((f"  CIPHER:  {cipher_class.NAME}", C_ACCENT, False))
    if key is not None:
        lines.append((f"  KEY:     {key}", C_WARNING, False))
    lines.append(("", C_NORMAL, False))
    lines.append(("  ── INPUT ──", C_DIM, False))
    for l in text.split('\n'):
        lines.append((f"  {l}", C_DIM, False))
    lines.append(("", C_NORMAL, False))
    lines.append(("  ── OUTPUT ──", C_SUCCESS, True))
    for l in result.split('\n'):
        lines.append((f"  {l}", C_SUCCESS, False))
    lines.append(("", C_NORMAL, False))
    lines.append(("━" * (w - 4), C_BORDER, False))

    # Stats
    alpha_in  = sum(1 for c in text if c.isalpha())
    alpha_out = sum(1 for c in result if c.isalpha())
    lines.append((f"  Input length: {len(text)} chars  |  Alpha chars: {alpha_in}", C_DIM, False))
    lines.append((f"  Output length: {len(result)} chars  |  Alpha chars: {alpha_out}", C_DIM, False))

    # Base64 of result
    try:
        b64 = base64.b64encode(result.encode()).decode()
        lines.append(("", C_NORMAL, False))
        lines.append(("  ── BASE64 ENCODED OUTPUT ──", C_DIM, False))
        # Break b64 into chunks
        for i in range(0, len(b64), w-8):
            lines.append((f"  {b64[i:i+w-8]}", C_DIM, False))
    except Exception:
        pass

    show_result_panel(stdscr, f"RESULT — {cipher_class.NAME}", lines, "")


# ─────────────────────────────────────────────────────────────────────────────
#  BRUTE FORCE / AUTO-CRACK SCREEN
# ─────────────────────────────────────────────────────────────────────────────

def run_crack_screen(stdscr, cipher_class):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = f"{cipher_class.NAME} — AUTO-CRACK / BRUTE FORCE"
    draw_header(stdscr, title)
    draw_box(stdscr, 1, 0, h-2, w, C_BORDER)

    safe_addstr(stdscr, 2, 2, f"Cipher: {cipher_class.NAME}", curses.color_pair(C_ACCENT) | curses.A_BOLD)
    safe_addstr(stdscr, 3, 2, f"Info:   {cipher_class.DESC}", curses.color_pair(C_DIM))
    draw_hline(stdscr, 4, 0, w, C_BORDER)
    safe_addstr(stdscr, 5, 2, "Paste ciphertext (multi-line, F10 to confirm, ESC to cancel):",
                curses.color_pair(C_WARNING) | curses.A_BOLD)

    input_h = min(8, h - 16)
    input_w = w - 8
    text = get_multiline_input(stdscr, "CIPHERTEXT", 7, 4, input_h, input_w)
    if text is None:
        return

    # Show loading animation
    stdscr.clear()
    draw_header(stdscr, f"CRACKING {cipher_class.NAME}...")
    draw_box(stdscr, 1, 0, h-2, w, C_BORDER)
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    for i in range(20):
        safe_addstr(stdscr, h//2, w//2 - 12,
                    f" {frames[i%len(frames)]}  Analyzing ciphertext...  ",
                    curses.color_pair(C_ACCENT) | curses.A_BOLD)
        ioc = index_of_coincidence(text)
        safe_addstr(stdscr, h//2+2, w//2-12,
                    f"    IoC: {ioc:.4f}  (EN≈0.065, RND≈0.038)    ",
                    curses.color_pair(C_DIM))
        stdscr.refresh()
        time.sleep(0.05)

    results = cipher_class.brute_force(text)

    lines = []
    lines.append(("━" * (w-4), C_BORDER, False))
    lines.append((f"  BRUTE FORCE RESULTS — {cipher_class.NAME}", C_TITLE, True))
    ioc = index_of_coincidence(text)
    lines.append((f"  Index of Coincidence: {ioc:.5f}  (English ≈ 0.065, Random ≈ 0.038)", C_DIM, False))
    lines.append(("━" * (w-4), C_BORDER, False))
    lines.append(("", C_NORMAL, False))

    for rank, (key, dec, score) in enumerate(results[:10]):
        color = C_SUCCESS if rank == 0 else (C_WARNING if rank < 3 else C_DIM)
        star  = "★ BEST →" if rank == 0 else f"  #{rank+1}    "
        lines.append((f"  {star}  Key: {str(key):<15}  Score: {score:8.2f}", color, rank == 0))
        # Show first 120 chars of decrypted
        preview = dec.replace('\n', ' ')[:w-12]
        lines.append((f"          {preview}", color, False))
        lines.append(("", C_NORMAL, False))

    show_result_panel(stdscr, f"CRACK RESULTS — {cipher_class.NAME}", lines)


# ─────────────────────────────────────────────────────────────────────────────
#  FREQUENCY ANALYSIS SCREEN
# ─────────────────────────────────────────────────────────────────────────────

def run_freq_analysis_screen(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    draw_header(stdscr, "FREQUENCY ANALYSIS")
    draw_box(stdscr, 1, 0, h-2, w, C_BORDER)

    safe_addstr(stdscr, 2, 2, "Frequency Analysis  —  Compare letter distribution vs English",
                curses.color_pair(C_ACCENT) | curses.A_BOLD)
    safe_addstr(stdscr, 3, 2, "Useful for identifying substitution ciphers and estimating key length.",
                curses.color_pair(C_DIM))
    draw_hline(stdscr, 4, 0, w, C_BORDER)
    safe_addstr(stdscr, 5, 2, "Enter text to analyze (F10 to confirm, ESC to cancel):",
                curses.color_pair(C_WARNING) | curses.A_BOLD)

    input_h = min(8, h - 16)
    input_w = w - 8
    text = get_multiline_input(stdscr, "ANALYSIS INPUT", 7, 4, input_h, input_w)
    if text is None:
        return

    freq_data = frequency_analysis(text)
    ioc       = index_of_coincidence(text)
    total_alpha = sum(c for _, c, _, _ in freq_data)

    lines = []
    lines.append(("━" * (w-4), C_BORDER, False))
    lines.append((f"  FREQUENCY ANALYSIS REPORT", C_TITLE, True))
    lines.append((f"  Total characters: {len(text)}   |   Alpha: {total_alpha}   |   IoC: {ioc:.5f}", C_DIM, False))

    eng_ioc = 0.065
    if ioc > 0.060:
        hint = "→ Likely monoalphabetic (Caesar, Atbash, Playfair…)"
        hint_color = C_WARNING
    elif ioc > 0.045:
        hint = "→ Possibly short Vigenère key or mixed text"
        hint_color = C_ACCENT
    else:
        hint = "→ Likely polyalphabetic (Vigenère, Beaufort…) or random"
        hint_color = C_ERROR
    lines.append((f"  {hint}", hint_color, True))
    lines.append(("━" * (w-4), C_BORDER, False))
    lines.append(("", C_NORMAL, False))

    bar_max = 40
    lines.append(("  Letter  Count   %Text   Bar (cyan=actual, yellow=English expected)", C_DIM, True))
    lines.append(("  ─────────────────────────────────────────────────────────────────", C_DIM, False))

    for ch, cnt, pct, expected in freq_data:
        if total_alpha == 0:
            break
        bar_actual   = int((pct / 15) * bar_max)
        bar_expected = int((expected / 15) * bar_max)
        bar_str = "█" * bar_actual
        diff = pct - expected
        diff_str = f"{diff:+.2f}%" if diff else "  0.00%"
        color = C_SUCCESS if abs(diff) < 1.5 else (C_WARNING if abs(diff) < 4 else C_ERROR)
        lines.append((
            f"  [{ch}]  {cnt:5d}  {pct:6.2f}%  {bar_str:<{bar_max}}  exp:{expected:.2f}%  {diff_str}",
            color, cnt == max(c for _, c, _, _ in freq_data)
        ))

    lines.append(("", C_NORMAL, False))
    lines.append(("━" * (w-4), C_BORDER, False))
    lines.append(("  TOP BIGRAMS", C_DIM, True))
    text_upper = re.sub(r'[^A-Za-z]', '', text).upper()
    bigrams = Counter(text_upper[i:i+2] for i in range(len(text_upper)-1))
    for bg, cnt in bigrams.most_common(10):
        lines.append((f"  {bg}: {cnt}", C_ACCENT, False))

    show_result_panel(stdscr, "FREQUENCY ANALYSIS", lines)


# ─────────────────────────────────────────────────────────────────────────────
#  CIPHER SELECTOR SUBMENU
# ─────────────────────────────────────────────────────────────────────────────

def run_cipher_selector(stdscr, action="encrypt"):
    selected = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        draw_header(stdscr, f"SELECT CIPHER — {action.upper()}")
        draw_box(stdscr, 1, 0, h-2, w, C_BORDER)

        safe_addstr(stdscr, 2, 2, "Choose a cipher to use:", curses.color_pair(C_ACCENT) | curses.A_BOLD)
        safe_addstr(stdscr, 3, 2, "↑↓ Navigate   Enter Select   ESC Back",
                    curses.color_pair(C_DIM))
        draw_hline(stdscr, 4, 0, w, C_BORDER)

        for i, cipher in enumerate(CIPHERS):
            y = 5 + i * 2
            if y >= h - 3:
                break
            prefix = "  ▶  " if i == selected else "     "
            name_str = f"{prefix}{cipher.NAME:<14}"
            desc_str = f"  {cipher.DESC}"

            if i == selected:
                attr = curses.color_pair(C_MENU_SEL) | curses.A_BOLD
                safe_addstr(stdscr, y, 1, " " * (w-2), attr)
                safe_addstr(stdscr, y, 1, name_str, attr)
                safe_addstr(stdscr, y, 1 + len(name_str), desc_str[:w-len(name_str)-4], attr)
            else:
                safe_addstr(stdscr, y, 1, name_str, curses.color_pair(C_CYAN) | curses.A_BOLD)
                safe_addstr(stdscr, y, 1+len(name_str), desc_str[:w-len(name_str)-4],
                            curses.color_pair(C_DIM))

        draw_status_bar(stdscr, f"↑↓ Select   Enter Confirm   ESC Back to main menu", C_DIM)
        stdscr.refresh()

        ch = stdscr.getch()
        if ch == curses.KEY_UP:
            selected = (selected - 1) % len(CIPHERS)
        elif ch == curses.KEY_DOWN:
            selected = (selected + 1) % len(CIPHERS)
        elif ch in (curses.KEY_ENTER, 10, 13):
            cipher_class = CIPHERS[selected]
            if action == "encrypt":
                run_cipher_screen(stdscr, cipher_class, "encrypt")
            elif action == "decrypt":
                run_cipher_screen(stdscr, cipher_class, "decrypt")
            elif action == "crack":
                run_crack_screen(stdscr, cipher_class)
        elif ch == 27:
            break


# ─────────────────────────────────────────────────────────────────────────────
#  CIPHER REFERENCE SCREEN
# ─────────────────────────────────────────────────────────────────────────────

def run_reference_screen(stdscr):
    ref_text = [
        ("SVILIA CIPHER — Cryptography Reference Guide", C_TITLE, True),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("1. CAESAR CIPHER", C_ACCENT, True),
        ("═" * 60, C_BORDER, False),
        ("  One of the oldest and simplest encryption techniques.", C_NORMAL, False),
        ("  Each letter is shifted by a fixed number of positions.", C_NORMAL, False),
        ("  Key space: 26 keys (trivially brute-forced).", C_NORMAL, False),
        ("  Example: 'HELLO' with key 3 → 'KHOOR'", C_SUCCESS, False),
        ("  Known plaintext attack: trivial.", C_WARNING, False),
        ("  Historical use: Julius Caesar's military communications.", C_DIM, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("2. ROT13", C_ACCENT, True),
        ("═" * 60, C_BORDER, False),
        ("  Caesar with key=13. Self-inverse: applying it twice gives", C_NORMAL, False),
        ("  the original text. Used historically in Usenet to hide", C_NORMAL, False),
        ("  spoilers. NOT secure in any way.", C_WARNING, False),
        ("  Example: 'HELLO' → 'URYYB'", C_SUCCESS, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("3. ATBASH CIPHER", C_ACCENT, True),
        ("═" * 60, C_BORDER, False),
        ("  Substitution cipher where A↔Z, B↔Y, C↔X, etc.", C_NORMAL, False),
        ("  Origin: Hebrew alphabet, used in the Bible (Jeremiah).", C_NORMAL, False),
        ("  Symmetric: encrypting twice gives original.", C_NORMAL, False),
        ("  Example: 'HELLO' → 'SVOOL'", C_SUCCESS, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("4. VIGENÈRE CIPHER", C_ACCENT, True),
        ("═" * 60, C_BORDER, False),
        ("  Polyalphabetic substitution using a repeating keyword.", C_NORMAL, False),
        ("  Each letter of the keyword defines a Caesar shift.", C_NORMAL, False),
        ("  Much stronger than Caesar — called 'le chiffre indéchiffrable'", C_NORMAL, False),
        ("  for centuries. Broken by Kasiski (1863) and Friedman (1920s).", C_NORMAL, False),
        ("  IoC test: if IoC ≈ 0.065 → monoalpha, ≈ 0.038 → poly.", C_WARNING, False),
        ("  Key: any word. Example key='KEY', 'HELLO' → 'RIJVS'", C_SUCCESS, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("5. BEAUFORT CIPHER", C_ACCENT, True),
        ("═" * 60, C_BORDER, False),
        ("  Similar to Vigenère but uses subtraction instead of addition.", C_NORMAL, False),
        ("  Self-reciprocal: same operation for encrypt and decrypt.", C_NORMAL, False),
        ("  Used in some early rotor cipher machines.", C_NORMAL, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("6. RAIL FENCE CIPHER", C_ACCENT, True),
        ("═" * 60, C_BORDER, False),
        ("  Transposition cipher. Text written in zigzag across N rails,", C_NORMAL, False),
        ("  then read off row by row.", C_NORMAL, False),
        ("  Key: number of rails (e.g. 3).", C_NORMAL, False),
        ("  Example 3 rails: 'WEAREDISCOVEREDFLEEAATONCE'", C_SUCCESS, False),
        ("  Rail 1: W . . . E . . . C . . . R . . . L . . . T . . . E", C_DIM, False),
        ("  Rail 2: . E . R . D . S . O . E . E . F . E . A . O . C .", C_DIM, False),
        ("  Rail 3: . . A . . . I . . . V . . . D . . . E . . . N . .", C_DIM, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("7. COLUMNAR TRANSPOSITION", C_ACCENT, True),
        ("═" * 60, C_BORDER, False),
        ("  Write plaintext in rows, read off columns in key-sorted order.", C_NORMAL, False),
        ("  Key is a word; columns are permuted by alphabetical order.", C_NORMAL, False),
        ("  More secure than rail fence; used in WWI/WWII.", C_NORMAL, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("8. PLAYFAIR CIPHER", C_ACCENT, True),
        ("═" * 60, C_BORDER, False),
        ("  Digraph substitution using a 5×5 key matrix (I=J).", C_NORMAL, False),
        ("  Encrypts pairs of letters using three rules:", C_NORMAL, False),
        ("    • Same row  → shift right", C_NORMAL, False),
        ("    • Same col  → shift down", C_NORMAL, False),
        ("    • Rectangle → swap corners in same row", C_NORMAL, False),
        ("  Used by British military in WWI.", C_NORMAL, False),
        ("  Harder to break than simple substitution, but IoC still high.", C_WARNING, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("CRYPTANALYSIS TIPS", C_TITLE, True),
        ("═" * 60, C_BORDER, False),
        ("  • IoC ≈ 0.065 → monoalphabetic (Caesar, Atbash, Playfair)", C_WARNING, False),
        ("  • IoC ≈ 0.038 → polyalphabetic (Vigenère, Beaufort)", C_WARNING, False),
        ("  • Most frequent letter in English ciphertext → likely 'E'", C_WARNING, False),
        ("  • Kasiski test: repeated sequences → key length estimate", C_WARNING, False),
        ("  • Friedman test: IoC → key length estimate", C_WARNING, False),
        ("", C_NORMAL, False),
        ("═" * 60, C_BORDER, False),
        ("  SVILIA CIPHER  |  github.com/yourusername/svilia-cipher", C_DIM, True),
        ("═" * 60, C_BORDER, False),
    ]
    show_result_panel(stdscr, "CIPHER REFERENCE", ref_text)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────────────────────────────────────

MENU_ITEMS = [
    ("⚔  ENCRYPT",              "encrypt"),
    ("🔓  DECRYPT",              "decrypt"),
    ("💀  AUTO-CRACK / BRUTE",   "crack"),
    ("📊  FREQUENCY ANALYSIS",   "freq"),
    ("📖  CIPHER REFERENCE",     "ref"),
    ("✖   EXIT",                 "exit"),
]


def draw_main_menu(stdscr, selected):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Header
    draw_header(stdscr)

    # Logo (small version)
    mini_logo = [
        " ███████╗██╗   ██╗██╗██╗     ██╗ █████╗ ",
        " ██╔════╝██║   ██║██║██║     ██║██╔══██╗",
        " ███████╗╚██╗ ██╔╝██║██║     ██║███████║",
        " ╚════██║ ╚████╔╝ ██║██║     ██║██╔══██║",
        " ███████║  ╚██╔╝  ██║███████╗██║██║  ██║",
        " ╚══════╝   ╚═╝   ╚═╝╚══════╝╚═╝╚═╝  ╚═╝",
    ]
    logo_colors = [C_CYAN, C_CYAN, C_ACCENT, C_ACCENT, C_HEADER, C_HEADER]

    logo_y = 2
    for i, line in enumerate(mini_logo):
        if logo_y + i < h - 5:
            cx = max(0, (w - len(line)) // 2)
            safe_addstr(stdscr, logo_y + i, cx, line,
                        curses.color_pair(logo_colors[i]) | curses.A_BOLD)

    subtitle_y = logo_y + len(mini_logo) + 1
    sub = "Classical Cryptography Terminal Suite  ·  v1.0.0"
    center_text(stdscr, subtitle_y, sub, curses.color_pair(C_DIM))

    cipher_line = "Caesar · Vigenère · Atbash · Rail Fence · Beaufort · Playfair · ROT13 · Columnar"
    center_text(stdscr, subtitle_y + 1, cipher_line, curses.color_pair(C_DIM))

    # Menu box
    menu_w = 42
    menu_h = len(MENU_ITEMS) * 2 + 2
    menu_x = (w - menu_w) // 2
    menu_y = subtitle_y + 3

    if menu_y + menu_h < h - 2:
        draw_box(stdscr, menu_y, menu_x, menu_h, menu_w, C_BORDER, " MAIN MENU ")

        for i, (label, _) in enumerate(MENU_ITEMS):
            item_y = menu_y + 1 + i * 2
            if item_y >= menu_y + menu_h - 1:
                break
            if i == selected:
                attr = curses.color_pair(C_MENU_SEL) | curses.A_BOLD
                safe_addstr(stdscr, item_y, menu_x + 1,
                            f"  {label:<{menu_w-4}}  ", attr)
            else:
                attr = curses.color_pair(C_CYAN) | curses.A_BOLD
                if i == len(MENU_ITEMS) - 1:
                    attr = curses.color_pair(C_ERROR)
                safe_addstr(stdscr, item_y, menu_x + 2, f"  {label}", attr)

    draw_status_bar(stdscr, "↑↓ Navigate   Enter Select   Q Quit", C_DIM)
    stdscr.refresh()


def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    init_colors()

    splash_screen(stdscr)

    selected = 0
    while True:
        draw_main_menu(stdscr, selected)
        ch = stdscr.getch()

        if ch == curses.KEY_UP:
            selected = (selected - 1) % len(MENU_ITEMS)
        elif ch == curses.KEY_DOWN:
            selected = (selected + 1) % len(MENU_ITEMS)
        elif ch in (curses.KEY_ENTER, 10, 13):
            action = MENU_ITEMS[selected][1]
            if action == "exit":
                break
            elif action in ("encrypt", "decrypt", "crack"):
                run_cipher_selector(stdscr, action)
            elif action == "freq":
                run_freq_analysis_screen(stdscr)
            elif action == "ref":
                run_reference_screen(stdscr)
        elif ch in (ord('q'), ord('Q')):
            break
        elif ch == ord('1'):
            run_cipher_selector(stdscr, "encrypt")
        elif ch == ord('2'):
            run_cipher_selector(stdscr, "decrypt")
        elif ch == ord('3'):
            run_cipher_selector(stdscr, "crack")
        elif ch == ord('4'):
            run_freq_analysis_screen(stdscr)
        elif ch == ord('5'):
            run_reference_screen(stdscr)


# ─────────────────────────────────────────────────────────────────────────────
#  CLI MODE (no TUI)
# ─────────────────────────────────────────────────────────────────────────────

CIPHER_MAP = {c.NAME.lower().replace(' ', '-'): c for c in CIPHERS}
CIPHER_MAP.update({
    "caesar": CaesarCipher,
    "rot13": Rot13Cipher,
    "atbash": AtbashCipher,
    "vigenere": VigenereCipher,
    "beaufort": BeaufortCipher,
    "rail-fence": RailFenceCipher,
    "railfence": RailFenceCipher,
    "columnar": ColumnarCipher,
    "playfair": PlayfairCipher,
})


def cli_mode():
    parser = argparse.ArgumentParser(
        description="SVILIA CIPHER — Classical Cryptography Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
CIPHERS:  caesar, rot13, atbash, vigenere, beaufort, rail-fence, columnar, playfair

EXAMPLES:
  svilia.py -c caesar -e -k 13 -t "Hello World"
  svilia.py -c vigenere -d -k SECRET -t "Zincs Pgvnu"
  svilia.py -c caesar --crack -t "Khoor Zruog"
  svilia.py -c vigenere --crack -t "Zincs Pgvnu"
  svilia.py --freq -t "Khoor Zruog"
  svilia.py --tui
        """
    )
    parser.add_argument('--tui', action='store_true', help='Launch interactive TUI')
    parser.add_argument('-c', '--cipher', help='Cipher name')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt')
    parser.add_argument('--crack', action='store_true', help='Auto-crack / brute force')
    parser.add_argument('-k', '--key', help='Key (number or word)')
    parser.add_argument('-t', '--text', help='Input text')
    parser.add_argument('-f', '--file', help='Input file path')
    parser.add_argument('--freq', action='store_true', help='Frequency analysis only')
    parser.add_argument('--list', action='store_true', help='List all ciphers')

    args = parser.parse_args()

    if args.tui or len(sys.argv) == 1:
        curses.wrapper(main_menu)
        return

    if args.list:
        print("\n  SVILIA CIPHER — Available Ciphers\n")
        print(f"  {'Name':<16} {'Key Type':<10}  Description")
        print(f"  {'─'*16} {'─'*10}  {'─'*40}")
        for c in CIPHERS:
            print(f"  {c.NAME:<16} {c.KEY_TYPE:<10}  {c.DESC}")
        print()
        return

    # Get text
    text = args.text
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    if not text:
        parser.print_help()
        return

    # Frequency analysis only
    if args.freq:
        freq_data = frequency_analysis(text)
        ioc = index_of_coincidence(text)
        print(f"\n  FREQUENCY ANALYSIS\n  IoC: {ioc:.5f}")
        print(f"  {'Letter':<8} {'Count':<8} {'%Text':<10} {'Expected':<10} {'Diff'}")
        print(f"  {'─'*6}   {'─'*5}   {'─'*7}   {'─'*8}   {'─'*8}")
        for ch, cnt, pct, expected in freq_data:
            diff = pct - expected
            print(f"  [{ch}]     {cnt:<8} {pct:<10.2f} {expected:<10.2f} {diff:+.2f}%")
        return

    if not args.cipher:
        parser.print_help()
        return

    cipher_class = CIPHER_MAP.get(args.cipher.lower())
    if not cipher_class:
        print(f"  Unknown cipher: {args.cipher}")
        print(f"  Use --list to see available ciphers.")
        return

    # Key handling
    key = args.key
    if cipher_class.KEY_TYPE == "number" and key:
        try:
            key = int(key)
        except ValueError:
            print(f"  Key must be a number for {cipher_class.NAME}")
            return

    # Action
    banner = f"""
  ╔══════════════════════════════════════╗
  ║      SVILIA CIPHER  ⚔  v1.0.0      ║
  ╚══════════════════════════════════════╝
  Cipher: {cipher_class.NAME}
"""
    print(banner)

    if args.crack:
        print(f"  ── AUTO-CRACK RESULTS ──\n")
        results = cipher_class.brute_force(text)
        for rank, (k, dec, score) in enumerate(results[:5]):
            star = "★ BEST" if rank == 0 else f"  #{rank+1}"
            print(f"  {star}  Key: {str(k):<15}  Score: {score:.2f}")
            print(f"        {dec[:120]}")
            print()
    elif args.encrypt:
        result = cipher_class.encrypt(text, key)
        print(f"  Mode:   ENCRYPT")
        print(f"  Key:    {key}")
        print(f"  Input:  {text[:80]}{'...' if len(text)>80 else ''}")
        print(f"\n  Output:\n  {result}\n")
        print(f"  Base64: {base64.b64encode(result.encode()).decode()}\n")
    elif args.decrypt:
        result = cipher_class.decrypt(text, key)
        print(f"  Mode:   DECRYPT")
        print(f"  Key:    {key}")
        print(f"  Input:  {text[:80]}{'...' if len(text)>80 else ''}")
        print(f"\n  Output:\n  {result}\n")
    else:
        parser.print_help()


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) == 1 or '--tui' in sys.argv:
        try:
            curses.wrapper(main_menu)
        except KeyboardInterrupt:
            print("\n  Goodbye from SVILIA CIPHER ⚔\n")
    else:
        try:
            cli_mode()
        except KeyboardInterrupt:
            print("\n  Interrupted.\n")
