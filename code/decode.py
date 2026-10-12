"""Read the cipher paragraph of 9 September 1520 with the key in data/, and test the key.

    python code/decode.py            the paragraph sign by sign, and what the key gives beside the reading
    python code/decode.py --test     the key applied to the test passage of 7 December 1521, token by token
    python code/decode.py --1520     the key applied to the cipher words of 8 October 1520, word by word
    python code/decode.py --second   the second readings: the transcription compared, the proposals, the points
    python code/decode.py --table    the word-by-word table printed in docs/TEXT.md
    python code/decode.py --blocks   the vocabulary by first letter, as printed in docs/METHOD.md
    python code/decode.py --figures  the counts taken from the data (kept in data/figures.txt)
    python code/decode.py --check    all checks; exit status 0 only if every one passes

Standard library only. The script reads data/, for --figures and --check the pages as well, and for --check
the sizes of the pictures in images/. It writes nothing.
"""

import collections
import difflib
import io
import os
import re
import sys
import traceback
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CROPS = os.path.join(ROOT, "images", "parallels")
LETTERS = {"A": "5 Dec 1521", "B": "24 Oct 1521", "C": "7 Dec 1521", "D": "May 1521"}
MONTHS = {"Dec": "December", "Oct": "October", "May": "May"}
ORDER = "zyxvtsrqpnmlhgfdcb"
NUMBER_WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
)
MODES = ("--test", "--1520", "--second", "--table", "--blocks", "--figures", "--check")
PAGES = (
    "README.md",
    "docs/METHOD.md",
    "docs/TEXT.md",
    "docs/SOURCES.md",
    "data/README.md",
    "images/README.md",
    "runs/README.md",
    "tests/TESTS.md",
)


def read(path):
    """A text file as a string."""
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def rows(name):
    """Lines of a data file without comments and blanks."""
    lines = read(os.path.join(DATA, name)).splitlines()
    return [s for s in lines if s.strip() and not s.startswith("#")]


def table_rows(name, width):
    """The rows of a data table after its header, each cut or padded to the given number of columns."""
    return [(s.split("\t") + [""] * width)[:width] for s in rows(name)[1:]]


def load_signs():
    """The letter signs: id -> (letter, source)."""
    signs = {}
    for sid, letter, _shape, source in table_rows("signs.tsv", 4):
        if sid in signs:
            raise ValueError("sign listed twice: " + sid)
        signs[sid] = (letter, source)
    return signs


def load_groups():
    """The key as a dictionary: group -> (value, source, where found)."""
    groups = {}
    for group, value, source, where in table_rows("groups.tsv", 4):
        if group in groups:
            raise ValueError("group listed twice: " + group)
        groups[group] = (value, source, where)
    return groups


def norm(text):
    """Fold what one cipher sign cannot distinguish: c/c-cedilla, u/v, i/j/y; accents are dropped."""
    t = unicodedata.normalize("NFD", text.lower())
    t = re.sub(r"[^a-z]", "", t)
    return t.replace("v", "u").replace("j", "i").replace("y", "i")


def is_mark(token):
    return token in ("/", ".")


def is_group(token):
    return token.endswith(".") and token != "."


def value(token, signs, groups):
    """(kind, text, source) for one token; text is None if the key has no value for it.

    A token is a mark (/ or a stray dot), a word in clear (=word), a group (gig.), a letter sign (a2), two
    signs that look alike (p1|d3), or, in data/parallels.tsv, a letter sign named only by its letter (+n).
    """
    if is_mark(token):
        return ("mark", "", "")
    if token.startswith("="):
        return ("plain", token[1:], "plain")
    if token.startswith("+"):
        return ("letter", token[1:], "")
    if is_group(token):
        g = groups.get(token[:-1])
        return ("group", g[0], g[1]) if g else ("group", None, "")
    if "|" in token:
        alts = token.split("|")
        if not all(a in signs for a in alts):
            return ("pair", None, "")
        return ("pair", "|".join(signs[a][0] for a in alts), "K")
    if token in signs:
        return ("sign", signs[token][0], signs[token][1])
    return ("sign", None, "")


def spell(tokens, signs, groups):
    """The letters that the key gives for a run of tokens, and the tokens it has no value for."""
    letters, missing = [], []
    for t in tokens:
        kind, text, _source = value(t, signs, groups)
        if kind == "mark":
            continue
        if text is None:
            missing.append(t)
            text = "[" + t + "]"
        letters.append(text)
    return "".join(letters), missing


def paragraph():
    """The paragraph as (line, tokens) pairs."""
    out = []
    for s in rows("paragraph.txt"):
        n, toks = s.split("\t")
        out.append((int(n), toks.split()))
    return out


def flat(lines):
    return [t for _n, toks in lines for t in toks]


def places_only(tokens):
    """The signs and groups of a run of tokens, without marks and words in clear."""
    return [t for t in tokens if not is_mark(t) and not t.startswith("=")]


def reading():
    return rows("reading.txt")[0]


def translation():
    return rows("translation.txt")[0]


def reading_ok(signs, groups, lines=None):
    """True if the key gives a value for every token of the paragraph and the values spell the reading."""
    letters, missing = spell(flat(lines or paragraph()), signs, groups)
    return not missing and norm(letters) == norm(reading())


def words():
    """(line, tokens, word) for each word of the paragraph."""
    return [(int(n), toks.split(), word) for n, toks, word in table_rows("words.tsv", 3)]


def words_ok(ws, signs, groups):
    """True if each word is what its own tokens spell."""
    for _n, ts, word in ws:
        letters, missing = spell(ts, signs, groups)
        if missing or norm(letters) != norm(word):
            return False
    return True


def marks_ok(ws, lines):
    """True if every word divider and the stray dot stand at the end of a word."""
    ends, done = set(), 0
    for _n, ts, _word in ws:
        done += len(ts)
        ends.add(done)
    seen = 0
    for t in flat(lines):
        if is_mark(t):
            if seen not in ends:
                return False
        else:
            seen += 1
    return True


def moved_words(ws, lines):
    """The words, with the first token after the first word divider moved into the word before it."""
    out = [(n, list(ts), w) for n, ts, w in ws]
    seen = 0
    for t in flat(lines):
        if t == "/":
            break
        if not is_mark(t):
            seen += 1
    done = 0
    for i, (_n, ts, _w) in enumerate(out[:-1]):
        done += len(ts)
        if done == seen and out[i + 1][1]:
            ts.append(out[i + 1][1].pop(0))
            break
    return out


def transcription():
    """The paragraph as docs/TEXT.md prints it, line by line."""
    out = []
    for n, toks in paragraph():
        shown = [t[1:] if t.startswith("=") else "[.]" if t == "." else t for t in toks]
        out.append("%d  %s" % (n, " ".join(shown)))
    return out


def letters_named(where):
    """The letters A to D named in the where column of data/groups.tsv."""
    return sorted(set(re.findall(r"\b([ABCD]) images? ", where)))


def table(signs, groups):
    """The word-by-word table of docs/TEXT.md, as Markdown lines."""
    out = ["| line | as written | reads | values from |", "|---|---|---|---|"]
    for n, toks, word in words():
        if toks[0].startswith("="):
            out.append("| %d | %s | %s | written in clear |" % (n, toks[0][1:], word))
            continue
        added = []
        for t in toks:
            kind, _text, source = value(t, signs, groups)
            if source != "S":
                continue
            if kind == "group":
                where = letters_named(groups[t[:-1]][2])
                added.append("`%s` from %s %s" % (t, "letter" if len(where) == 1 else "letters", " and ".join(where)))
            else:
                added.append("`%s` from the letters of 1521" % t)
        if not added:
            src = "Kolosova, from the pair `cim. mu.`" if toks == ["mu."] else "Kolosova"
        elif len(added) == len(toks):
            src = "; ".join(added)
        else:
            src = "; ".join(added) + "; the rest Kolosova"
        out.append("| %d | `%s` | %s | %s |" % (n, " ".join(toks), word, src))
    return out


def test_tokens():
    """(token, what the decipherment of 1521 has, line) for the test passage."""
    return [tuple(r) for r in table_rows("test_passage.tsv", 3)]


def run_test(signs, groups):
    """Compare the key with the decipherment of 1521, token by token."""
    c = dict.fromkeys(("groups", "groups_in", "groups_ok", "signs", "signs_in", "signs_ok", "pairs", "pairs_ok"), 0)
    not_in, wrong = [], []
    for token, want, _line in test_tokens():
        kind, text, _source = value(token, signs, groups)
        if kind in ("mark", "plain"):
            continue
        if kind == "pair" and text is not None:
            c["signs"] += 1
            c["pairs"] += 1
            if norm(want) in [norm(a) for a in text.split("|")]:
                c["pairs_ok"] += 1
            else:
                wrong.append((token, text, want))
            continue
        key = "groups" if kind == "group" else "signs"
        c[key] += 1
        if text is None:
            not_in.append(token)
        else:
            c[key + "_in"] += 1
            if norm(text) == norm(want):
                c[key + "_ok"] += 1
            else:
                wrong.append((token, text, want))
    return c, not_in, wrong


def test_ok(signs, groups):
    """True if no group, sign or pair that the key covers disagrees with the decipherment of 1521."""
    c, _not_in, wrong = run_test(signs, groups)
    return not wrong and c["groups_in"] == c["groups_ok"] and c["signs_in"] == c["signs_ok"]


def run_1520(signs, groups):
    """The passage of 8 October 1520, word by word, against the print of 1898.

    Each word comes back as (line, tokens, print, expected, got). expected is the word the file says the key
    gives where that is not the word of the print, and "" elsewhere. got is None if the key cannot read it.
    """
    out = []
    for line, toks, want, expected, _note in table_rows("passage_1520.tsv", 5):
        letters, missing = spell(toks.split(), signs, groups)
        out.append((int(line), toks.split(), want, expected.strip(), None if missing else letters))
    return out


def as_expected(w):
    """One word of the 1520 passage: the key gives the print's word, or the other word the file names."""
    _line, _toks, want, expected, got = w
    if expected:
        return norm(got) == norm(expected) and norm(expected) != norm(want)
    return norm(got) == norm(want)


def passage_1520_ok(signs, groups):
    return all(as_expected(w) for w in run_1520(signs, groups) if w[4] is not None)


def blocks(groups):
    """The values of the key by the first letter of the group, as Markdown lines."""
    by = {}
    for g, v in groups.items():
        by.setdefault(g[0], []).append(v[0])
    if not set(by) <= set(ORDER):
        raise ValueError("groups beginning with letters outside the order: %s" % sorted(set(by) - set(ORDER)))
    return ["| %s | %s |" % (c, ", ".join(sorted(by[c], key=str.lower))) for c in ORDER if c in by]


def places(text):
    """The (letter, image, line) places named in a where column, as in "A image 3 line 29"."""
    return {(a, int(b), int(c)) for a, b, c in re.findall(r"\b([ABCD]) image (\d+) line (\d+)", text)}


def ten(groups, lines=None):
    """The added groups that the paragraph uses."""
    pg = {t[:-1] for t in flat(lines or paragraph()) if is_group(t)}
    return sorted(g for g in pg if g in groups and groups[g][1] == "S")


def tested_added(groups):
    """The added groups, other than the ten, that the two test passages use."""
    used = {t[:-1] for t, _w, _l in test_tokens() if is_group(t)}
    used |= {t[:-1] for row in table_rows("passage_1520.tsv", 5) for t in row[1].split() if is_group(t)}
    return sorted(g for g in used if g in groups and groups[g][1] == "S" and g not in ten(groups))


def crops():
    """The crops in images/parallels: (letter, image, first line, last line) -> file name."""
    out = {}
    if os.path.isdir(CROPS):
        for name in sorted(os.listdir(CROPS)):
            m = re.fullmatch(r"([ABCD])(\d+)_(\d+)(?:-(\d+))?\.jpg", name)
            if m:
                a, b, c, d = m.groups()
                out[(a, int(b), int(c), int(d or c))] = name
    return out


def image_size(path):
    """(width, height) of a PNG or JPEG file of the repository, read from its header, or None."""
    with open(os.path.join(ROOT, path), "rb") as f:
        b = f.read()
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")
    i = 2
    while i + 9 < len(b) and b[i] == 0xFF:
        marker = b[i + 1]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            return int.from_bytes(b[i + 7 : i + 9], "big"), int.from_bytes(b[i + 5 : i + 7], "big")
        i += 2 + int.from_bytes(b[i + 2 : i + 4], "big")
    return None


def boxes(itext):
    """(file under images/, (left, top, right, bottom)) for each box that images/README.md gives."""
    out = [
        ("paragraph.jpg", tuple(int(x) for x in m))
        for m in re.findall(r"`paragraph\.jpg` shows .*? box (\d+), (\d+), (\d+), (\d+) of image", squeeze(itext))
    ]
    for name, box in re.findall(r"(?m)^\| `([^`]+)` \|(?:[^|\n]*\|)*? (\d+, \d+, \d+, \d+) \|", itext):
        out.append((name, tuple(int(x) for x in box.split(", "))))
    return out


def crop_for(place):
    """The crop that shows a place, or None."""
    letter, image, line = place
    for (a, b, c, d), name in crops().items():
        if (a, b) == (letter, image) and c <= line <= d:
            return name
    return None


def method_places(mtext):
    """group -> the places named for it in the table of the ten groups in docs/METHOD.md, and the links.

    The links come back as (place, the crop file the link points to).
    """
    found, links, current = {}, [], None
    pattern = r"\[([ABCD]), image (\d+), line (\d+)\]\(\.\./images/parallels/([^)]+)\)"
    for line in mtext.splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 5:
            continue
        m = re.fullmatch(r"`([a-z]+)\.`", cells[1])
        if m:
            current = m.group(1)
        elif cells[1]:
            current = None
        for a, b, c, name in re.findall(pattern, cells[3]):
            if current:
                found.setdefault(current, set()).add((a, int(b), int(c)))
                links.append(((a, int(b), int(c)), name))
    return found, links


def clear_words():
    """The short words in clear within the cipher: (letter, image, line, words, text, read or omitted)."""
    return [(a, int(b), int(c), w, t, s) for a, b, c, w, t, s in table_rows("clear_words.tsv", 6)]


def method_clear_words(mtext):
    """The rows of the table of words in clear in docs/METHOD.md, each with the crop that it links to."""
    pattern = (
        r"(?m)^\| \[([ABCD]), image (\d+), line (\d+)\]\(\.\./images/parallels/([^)]+)\) "
        r"\| \*([^*]+)\* \| \*([^*]+)\* \| (\w+) \|$"
    )
    part = section(mtext, "Words in clear within the cipher")
    return [((a, int(b), int(c), w, t, s), name) for a, b, c, name, w, t, s in re.findall(pattern, part)]


def second_raw():
    """The second transcription as the reader named the letters."""
    return [(int(n), toks.split()) for n, toks in (s.split("\t") for s in rows("second_reading.txt"))]


def second_reading():
    """The second transcription, with the reader's letter names mapped: z to r and ʒ to z in the groups."""
    return [
        (n, [t.replace("z", "r").replace("ʒ", "z") if is_group(t) else t for t in toks]) for n, toks in second_raw()
    ]


def second_notes():
    """The tokens named in the comment lines of data/second_reading.txt that begin "# corrected" or "# identified"."""
    text = read(os.path.join(DATA, "second_reading.txt"))
    pattern = r"(?m)^# (corrected in the first from this reading|identified from a description): (.*)$"
    return {k: v.split() for k, v in re.findall(pattern, text)}


def second_mapped():
    """The groups in which the comparison maps the reader's z or ʒ."""
    return [t for _n, toks in second_raw() for t in toks if is_group(t) and ("z" in t or "ʒ" in t)]


def compare_second(first=None):
    """(places in the first transcription, places at which the second has the same, the differences).

    The differences are (tokens of the first, tokens of the second) for each stretch where they part.
    """
    a = flat(first or paragraph())
    b = flat(second_reading())
    same, diffs = 0, []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            same += len(places_only(a[i1:i2]))
        else:
            diffs.append((a[i1:i2], b[j1:j2]))
    return len(places_only(a)), same, diffs


def proposals():
    """(token, kind, proposal, confidence, note) for each proposal of the second reader."""
    return [(t, k, p, int(c), n) for t, k, p, c, n in table_rows("second_proposals.tsv", 5)]


def proposal_agrees(row, signs, groups):
    token, kind, proposal, _conf, _note = row
    if kind == "group":
        g = groups.get(token[:-1])
        return g is not None and norm(g[0]) == norm(proposal)
    if kind == "sign":
        return token in signs and signs[token][0] == proposal
    return False


def parallels():
    """(point, (letter, image, line), word, tokens, kind, note) for each row of data/parallels.tsv."""
    return [
        (int(p), (a, int(b), int(c)), w, t.split(), k, n) for p, a, b, c, w, t, k, n in table_rows("parallels.tsv", 8)
    ]


def parallel_reads(toks, signs, groups):
    """What the key's values make of the tokens found at a place, in the notation of docs/METHOD.md.

    Group values are joined to what they follow by a hyphen (gran-des, entiende-n), and a run of letter
    signs is written letter by letter (c-o-r-o-n-a). None if a group is not in the key.
    """
    pieces = []
    for t in toks:
        kind, text, _source = value(t, signs, groups)
        if text is None:
            return None
        if kind in ("letter", "sign") and pieces and pieces[-1][0] == "letters":
            pieces[-1][1].append(text)
        elif kind in ("letter", "sign"):
            pieces.append(("letters", [text]))
        else:
            pieces.append(("group", [text]))
    out = ""
    for i, (kind, texts) in enumerate(pieces):
        text = "-".join(texts)
        if i == 0:
            out = text
        elif kind == "group" and pieces[i - 1][0] == "letters":
            out += " " + text
        else:
            out += "-" + text
    return out


def parallel_ok(row, signs, groups):
    """True if the key's values at the tokens found spell the word asked."""
    _point, _place, word, toks, _kind, _note = row
    reads = parallel_reads(toks, signs, groups)
    return reads is not None and norm(reads) == norm(word)


def show_tokens(toks):
    """Tokens as docs/METHOD.md prints them: groups in code, letter signs letter by letter, + between the two."""
    out, prev = [], None
    for t in toks:
        if t.startswith("+"):
            if prev == "letter":
                out[-1] += "-" + t[1:]
            else:
                out.append(("+ " if prev == "group" else "") + t[1:])
            prev = "letter"
        elif prev == "group":
            out[-1] = out[-1][:-1] + " " + t + "`"
        else:
            out.append("`" + t + "`")
            prev = "group"
    return " ".join(out)


def parallel_table(signs, groups):
    """The table of the points on groups of the key in docs/METHOD.md, as Markdown lines."""
    out = ["| point | place | word | tokens found | with the key's values |", "|---|---|---|---|---|"]
    for point, (a, b, c), word, toks, kind, _note in parallels():
        if kind == "key":
            reads = parallel_reads(toks, signs, groups) or "not in the key"
            out.append(
                "| %d | %s, image %d, line %d | %s | %s | %s |" % (point, a, b, c, word, show_tokens(toks), reads)
            )
    return out


def squeeze(text):
    return re.sub(r"\s+", " ", text)


def page(path):
    """A page of the repository as it is written, or "" if it is missing."""
    full = os.path.join(ROOT, path)
    return read(full) if os.path.exists(full) else ""


def prose(path):
    """A page without block-quote marks and with runs of white space collapsed."""
    return squeeze(re.sub(r"(?m)^> ?", "", page(path)))


def section(text, heading):
    """The part of a page under a heading, up to the next heading of the same or a higher level."""
    m = re.search(r"(?m)^(#+) " + re.escape(heading) + r"\s*$", text)
    if not m:
        return ""
    rest = text[m.end() :]
    end = re.search(r"(?m)^#{1,%d} " % len(m.group(1)), rest)
    return rest[: end.start()] if end else rest


def quote_after(text, marker):
    """The block quote that follows the paragraph ending with marker, as one line."""
    i = text.find(marker)
    if i < 0:
        return ""
    lines = text[i:].splitlines()[1:]
    while lines and not lines[0].startswith(">"):
        if lines[0].strip():
            return ""
        lines = lines[1:]
    quote = []
    for s in lines:
        if not s.startswith(">"):
            break
        quote.append(s[1:].strip())
    return " ".join(quote)


def number_word(n):
    return NUMBER_WORDS[n] if n < len(NUMBER_WORDS) else str(n)


def quoted_ok(phrase, n, text):
    """True if the phrase is in the text with the count n in place of {}, {w} or {W}.

    {} is the number in figures, and it must not be part of a longer number. {w} is the number as a word
    (four) and {W} the same with a capital (Four).
    """
    word = number_word(n)
    pattern = re.escape(squeeze(phrase))
    pattern = pattern.replace(re.escape("{w}"), r"\b%s\b" % word)
    pattern = pattern.replace(re.escape("{W}"), r"\b%s\b" % word.capitalize())
    pattern = pattern.replace(re.escape("{}"), r"(?<![\d.,])%d(?!\d)" % n)
    return re.search(pattern, text) is not None


def quoted_failures(fig, texts):
    """The rows of data/quoted.tsv whose phrase is not in its page with the computed figure."""
    bad = []
    for name, path, phrase in table_rows("quoted.tsv", 3):
        if name not in fig or not quoted_ok(phrase, fig[name], texts.get(path, "")):
            bad.append("%s in %s" % (name, path))
    return bad


def brief_spellings(mtext):
    """The (clerk, decipherer) pairs of spellings named in the section on the first test."""
    part = squeeze(section(mtext, "The first test: 7 December 1521"))
    m = re.search(r"The clerk spelt (\w+) words more briefly than the decipherer: (.*?)\.(?: |$)", part)
    if not m:
        return None, []
    return m.group(1), re.findall(r"\*(\w+)\* for (?:the decipherment's )?\*(\w+)\*", m.group(2))


def decipherment_ok(mtext):
    """True if the decipherment column of data/test_passage.tsv is the decipherment quoted in docs/METHOD.md.

    The quotation is taken as printed, with its gap for the words in clear omitted, v. mad read as
    vuestra magestad, and the decipherer's spellings replaced by the clerk's at the places named.
    """
    quote = quote_after(mtext, "The decipherment of 1521 reads:")
    _count, pairs = brief_spellings(mtext)
    if not quote or not pairs:
        return False
    text = quote.replace("[...]", " ").replace("v. mad", "vuestra magestad")
    for clerk, theirs in pairs:
        if not re.search(r"\b%s\b" % theirs, text):
            return False
        text = re.sub(r"\b%s\b" % theirs, clerk, text, count=1)
    column = "".join(want for _t, want, _line in test_tokens())
    return norm(text) == norm(column)


def print_ok(mtext):
    """True if the words of the print in data/passage_1520.tsv come, in order, in the print quoted in METHOD."""
    quote = [norm(w) for w in quote_after(mtext, "in a decipherment by Claudio Pérez y Gredilla:").split()]
    want = [norm(w) for _line, _toks, w, _e, _n in table_rows("passage_1520.tsv", 5)]
    i = 0
    for w in quote:
        if i < len(want) and w == want[i]:
            i += 1
    return bool(want) and i == len(want)


def links_ok():
    """The relative links in the pages that point to no file in the repository."""
    bad = []
    for path in PAGES:
        base = os.path.dirname(os.path.join(ROOT, path))
        for target in re.findall(r"\]\(([^)#]+?)(?:#[^)]*)?\)", page(path)):
            if "://" not in target and not os.path.exists(os.path.normpath(os.path.join(base, target))):
                bad.append("%s in %s" % (target, path))
    return bad


def respelt(mtext):
    """The groups listed in the section of docs/METHOD.md on what changed after the test, and the bullets.

    Each bullet comes back as (the number word it opens with, or "", the groups it names).
    """
    bullets = []
    for part in re.split(r"\n(?=- )", section(mtext, "What changed after the test")):
        bullet = part.split("\n\n")[0]
        if bullet.startswith("- "):
            m = re.match(r"- (\w+) groups ", bullet)
            bullets.append((m.group(1) if m else "", re.findall(r"`([a-z]+)\.`", bullet)))
    named = {g for _word, gs in bullets for g in gs}
    return named, bullets


def removed(mtext):
    """(number word, groups) of the sentence in docs/METHOD.md on the groups removed from the key."""
    m = re.search(r"(\w+) groups of the first reading were removed from the key[^:]*: (.*?)\. ", squeeze(mtext))
    return (m.group(1), re.findall(r"`([a-z]+)\.`", m.group(2))) if m else ("", [])


def parse_tokens(text):
    """Tokens as the pages and the where column write them: groups as gig., letter signs letter by letter
    (d-a-r-a, perhaps after +), each letter becoming a token +d, +a, ... as in data/parallels.tsv."""
    out = []
    for piece in text.replace("`", " ").replace("+", " ").split():
        if is_group(piece):
            out.append(piece)
        else:
            out.extend("+" + x for x in piece.split("-") if x)
    return out


def evidence(where):
    """(place, tokens, deciphered text) for each item of a where column that names lines.

    The column reads "A image 3 line 29: ru. + n sa. nu. + r = entienden de juntar; B image 3 ...", with
    " and " between two items at the same place; remarks in brackets are omitted.
    """
    out = []
    for entry in re.sub(r"\s*\([^)]*\)", "", where).split("; "):
        m = re.fullmatch(r"([ABCD]) image (\d+) line (\d+): (.+)", entry.strip())
        if not m:
            return []
        place = (m.group(1), int(m.group(2)), int(m.group(3)))
        for item in m.group(4).split(" and "):
            toks, sep, said = item.partition(" = ")
            if not sep:
                return []
            out.append((place, parse_tokens(toks), said.strip()))
    return out


def method_evidence(mtext):
    """(group, place, tokens, deciphered text) for each item of the table of the ten groups in docs/METHOD.md."""
    out, current = [], None
    for line in section(mtext, "The %s groups the paragraph needs" % number_word(10)).splitlines():
        cells = [c.strip() for c in line.split("|")]
        if not line.startswith("|") or len(cells) != 7:
            continue
        m = re.fullmatch(r"`([a-z]+)\.`", cells[1])
        if m:
            current = m.group(1)
        elif cells[1]:
            current = None
        p = re.search(r"\[([ABCD]), image (\d+), line (\d+)\]", cells[3])
        if current and p:
            place = (p.group(1), int(p.group(2)), int(p.group(3)))
            written, said = cells[4].split(" and "), cells[5].split("; ")
            if len(written) != len(said):
                return []
            out.extend((current, place, parse_tokens(w), s) for w, s in zip(written, said, strict=True))
    return out


def evidence_ok(groups, signs):
    """True if every item of evidence for the ten groups contains the group and spells its deciphered text."""
    items = [(g, *e) for g in ten(groups) for e in evidence(groups[g][2])]
    return bool(items) and all(
        g + "." in toks and norm(spell(toks, signs, groups)[0]) == norm(said) for g, _p, toks, said in items
    )


def fenced_after(text, marker):
    """The lines of the first fenced block after the first line that contains marker."""
    lines = text.splitlines()
    i = next((k for k, s in enumerate(lines) if marker in s), None)
    if i is None:
        return []
    start = next((k for k in range(i, len(lines)) if lines[k].startswith("```")), None)
    if start is None:
        return []
    end = next((k for k in range(start + 1, len(lines)) if lines[k].startswith("```")), len(lines))
    return lines[start + 1 : end]


def table_lines(text, header):
    """The lines of the Markdown table whose header line starts with header."""
    lines = text.splitlines()
    i = next((k for k, s in enumerate(lines) if s.startswith(header)), None)
    if i is None:
        return []
    out = []
    for s in lines[i:]:
        if not s.startswith("|"):
            break
        out.append(s)
    return out


def flat_display(text):
    """A display line without spaces, hyphens and plus signs, in lower case and without accents."""
    text = "".join(c for c in unicodedata.normalize("NFD", text.lower()) if not unicodedata.combining(c))
    return re.sub(r"[\s+\-]", "", text)


def first_line_ok(readme, signs):
    """True if the display of the first line in README.md is line 1 of the paragraph and its words."""
    block = [s for s in fenced_after(readme, "first line of the paragraph") if s.strip()]
    if len(block) != 2:
        return False
    toks = paragraph()[0][1]
    want = "".join(t[1:] if t.startswith("=") else t if is_group(t) or is_mark(t) else signs[t][0] for t in toks)
    said = [norm(w) for n, _ts, word in words() if n == 1 for w in word.split()]
    return flat_display(block[0]) == flat_display(want) and [norm(w) for w in block[1].split()] == said


def value_claims(text, signs, groups):
    """(the words of the page, True if the key bears them out) for each place where a page gives the value of
    groups of the key: `gig.` is *que*, `roc.` + s is *estos*, `taf.` for *deve*, `cog.` gives *ver*,
    `qec.` (*fue*), *faze* for `rof.`. Groups that are not in the key are skipped."""
    out = []
    forward = r"`([a-z]+\.(?: [a-z]+\.)*)`(?: \(\*[^*]+\*\))?(?: \+ ([a-z](?:-[a-z])*))? (?:is|for|gives) \*([^*]+)\*"
    for m in re.finditer(forward, text):
        gs, letters, word = m.groups()
        toks = gs.split() + ["+" + x for x in (letters or "").split("-") if x]
        if all(g[:-1] in groups for g in gs.split()):
            out.append((m.group(0), norm(spell(toks, signs, groups)[0]) == norm(word)))
    for m in re.finditer(r"`([a-z]+)\.` \(\*([^*]+)\*\)", text):
        if m.group(1) in groups:
            out.append((m.group(0), norm(groups[m.group(1)][0]) == norm(m.group(2))))
    for m in re.finditer(r"\*([^*]+)\* for `([a-z]+)\.`", text):
        if m.group(2) in groups:
            out.append((m.group(0), norm(groups[m.group(2)][0]) == norm(m.group(1))))
    return out


def judged_ok(ttext):
    """True if each point that rests on judgement in docs/TEXT.md is in the line of the paragraph it names.

    The token of a point is the first one in code in it, or the stray dot; "three groups earlier in the same
    line" is counted among the groups of that line.
    """
    lines = dict(paragraph())
    points = re.split(r"(?m)^\d+\. ", section(ttext, "Points that rest on judgement"))[1:]
    if not points:
        return False
    for point in points:
        text = squeeze(point)
        line = re.search(r"\bline (\d+)\b", text)
        token = "." if text.startswith("The dot") else (re.findall(r"`([^`]+)`", text) or [""])[0]
        if not line or token not in lines.get(int(line.group(1)), []):
            return False
        for other, count in re.findall(r"`([a-z]+\.)`, (\w+) groups? earlier in the same line", text):
            gs = [t for t in lines[int(line.group(1))] if is_group(t)]
            if other not in gs or token not in gs or number_word(gs.index(token) - gs.index(other)) != count:
                return False
    return True


def images_of(where, letter):
    """The image numbers of one letter (A to D) named in a where column."""
    out = set()
    for a, nums in re.findall(r"\b([ABCD]) images? (\d+(?:, \d+)*)", where):
        if a == letter:
            out |= {int(x) for x in re.findall(r"\d+", nums)}
    return out


def q_places(mtext):
    """sign -> (the places linked in its bullet in docs/METHOD.md, the word it begins in the paragraph)."""
    out = {}
    link = r"\[(?:[ABCD], )?image (\d+), line (\d+)\]\(\.\./images/parallels/([ABCD])\d+_[^)]+\)"
    for bullet in re.split(r"\n(?=- )", section(mtext, "The letter q")):
        m = re.match(r"- The sign `(q\d)`", bullet)
        if m:
            text = squeeze(bullet)
            begins = re.search(r"begins \*(\w+)\* in the paragraph", text)
            found = {(a, int(b), int(c)) for b, c, a in re.findall(link, text)}
            out[m.group(1)] = (found, begins.group(1) if begins else "")
    return out


def parallel_rows_for(sign):
    return {r[1] for r in parallels() if r[4] == "q" and r[3] == [sign]}


def parallel_notes_ok(mtext):
    """The sentences under the table of the points say which points have two rows and which it omits."""
    m = re.search(
        r"Point (\d+) has two rows because line (\d+) of ([ABCD]) has `([^`]+)` twice, and point (\d+) because "
        r"`([^`]+)` stands in lines (\d+) and (\d+) of ([ABCD])\. The table omits points ([\d, and]+)\.",
        squeeze(mtext),
    )
    if not m:
        return False
    par = parallels()
    rows_of = {p: [r for r in par if r[0] == p and r[4] == "key"] for p in {r[0] for r in par}}
    first, second = rows_of[int(m.group(1))], rows_of[int(m.group(5))]
    return (
        sorted(p for p in rows_of if len(rows_of[p]) > 1) == [int(m.group(1)), int(m.group(5))]
        and all(r[1][0] == m.group(3) and r[1][2] == int(m.group(2)) and r[3] == m.group(4).split() for r in first)
        and [r[1][2] for r in second] == [int(m.group(7)), int(m.group(8))]
        and all(r[1][0] == m.group(9) and r[3] == m.group(6).split() for r in second)
        and sorted(p for p in rows_of if not rows_of[p]) == [int(x) for x in re.findall(r"\d+", m.group(10))]
    )


def figures(signs, groups):
    """Counts taken from the data and from the lists that the pages give. data/quoted.tsv says which of them
    the pages quote."""
    toks = flat(paragraph())
    pg = [t[:-1] for t in toks if is_group(t)]
    ps = [t for t in toks if t in signs]
    the_ten = set(ten(groups))
    c, _not_in, _wrong = run_test(signs, groups)
    tg = [t[:-1] for t, _want, _line in test_tokens() if is_group(t) and t[:-1] in groups]
    w20 = run_1520(signs, groups)
    t20 = [t for w in w20 for t in w[1]]
    g20 = [t[:-1] for t in t20 if is_group(t) and t[:-1] in groups]
    n_places, n_same, diffs = compare_second()
    par = parallels()
    on_key = [r for r in par if r[4] == "key"]
    props = [r for r in proposals() if r[1] == "group"]
    per_letter = {}
    for letter, source in signs.values():
        if source == "K":
            per_letter[letter] = per_letter.get(letter, 0) + 1
    method = page("docs/METHOD.md")
    changed, _bullets = respelt(method)
    judged = re.findall(r"(?m)^\d+\. (.*)", section(page("docs/TEXT.md"), "Points that rest on judgement"))
    return {
        "paragraph lines": len(paragraph()),
        "paragraph groups": len(pg),
        "paragraph distinct groups": len(set(pg)),
        "paragraph distinct groups from the published key": len(
            [g for g in set(pg) if g in groups and groups[g][1] == "K"]
        ),
        "paragraph distinct groups from the parallels": len(the_ten),
        "paragraph letter signs": len(ps),
        "paragraph distinct letter signs": len(set(ps)),
        "paragraph signs and groups": len(pg) + len(ps),
        "paragraph words": len(reading().split()),
        "paragraph words in clear": len([t for t in toks if t.startswith("=")]),
        "paragraph words in cipher": len(reading().split()) - len([t for t in toks if t.startswith("=")]),
        "commas in the reading": reading().count(","),
        "signs of dara": sum(len(ts) for _n, ts, w in words() if w == "dara"),
        "points of judgement in docs/TEXT.md besides the dot": len([s for s in judged if not s.startswith("The dot")]),
        "groups in the key, published": len([g for g in groups if groups[g][1] == "K"]),
        "groups in the key, published, without mu.": len([g for g in groups if groups[g][1] == "K" and g != "mu"]),
        "groups in the key, added": len([g for g in groups if groups[g][1] == "S"]),
        "letters of 1521 used for the key": len({x for g in groups.values() for x in letters_named(g[2])}),
        "shortest group": min(len(g) for g in groups),
        "longest group": max(len(g) for g in groups),
        "added groups resting on one place": len([g for g in the_ten if len(places(groups[g][2])) == 1]),
        "added groups that the tests use besides the ten": len(tested_added(groups)),
        "added groups named by image only": len(
            [g for g in groups if groups[g][1] == "S" and not places(groups[g][2])]
        ),
        "places of cu.": len(places(groups["cu"][2])) if "cu" in groups else 0,
        "places of ru.": len(places(groups["ru"][2])) if "ru" in groups else 0,
        "places of the first sign for q": len(q_places(method).get("q1", (set(), ""))[0]),
        "groups among the ten that neither test uses": len(the_ten - set(tg) - set(g20)),
        "confidence of the proposal for ru.": next((r[3] for r in props if r[0] == "ru."), 0),
        "test passage lines": len({line for _t, _want, line in test_tokens()}),
        "test groups": c["groups"],
        "test groups in the key": c["groups_in"],
        "test groups agreeing": c["groups_ok"],
        "test groups not in the key": c["groups"] - c["groups_in"],
        "test groups from the published key": len([g for g in tg if groups[g][1] == "K"]),
        "test groups from the added part": len([g for g in tg if groups[g][1] == "S"]),
        "test groups among the ten": len([g for g in tg if g in the_ten]),
        "test letter signs": c["signs"],
        "test letter signs matched to one sign": c["signs_in"],
        "test letter signs not matched to one sign": c["signs"] - c["signs_in"],
        "test letter signs agreeing": c["signs_ok"],
        "test look-alike pairs": c["pairs"],
        "test signs not in the table": c["signs"] - c["signs_in"] - c["pairs"],
        "test signs for q": len([t for t, _want, _line in test_tokens() if t in ("q1", "q2")]),
        "test words spelt more briefly, as named": len(brief_spellings(method)[1]),
        "1520 passage words": len(w20),
        "1520 passage words the key reads": len([w for w in w20 if w[4] is not None]),
        "1520 passage words the key cannot read": len([w for w in w20 if w[4] is None]),
        "1520 passage words the same as the print": len([w for w in w20 if w[4] and norm(w[4]) == norm(w[2])]),
        "1520 passage words that differ from the print": len([w for w in w20 if w[4] and norm(w[4]) != norm(w[2])]),
        "1520 passage groups": len([t for t in t20 if is_group(t)]),
        "1520 passage letter signs": len([t for t in t20 if not is_group(t)]),
        "1520 passage added groups": len([g for g in g20 if groups[g][1] == "S"]),
        "1520 passage groups among the ten": len([g for g in g20 if g in the_ten]),
        "1520 passage signs for q": len([t for t in t20 if t in ("q1", "q2")]),
        "signs in the published table": len([x for x in signs if signs[x][1] == "K"]),
        "letters in the published table": len({signs[x][0] for x in signs if signs[x][1] == "K"}),
        "most signs for one letter in the published table": max(per_letter.values()),
        "fewest signs for one letter in the published table": min(per_letter.values()),
        "signs for q": len([x for x in signs if signs[x][0] == "q"]),
        "groups in the key": len(groups),
        "groups respelt after the test, as listed": len(changed),
        "groups removed after the test": len(removed(method)[1]),
        "sets of respelt groups": len(respelt(method)[1]),
        "groups respelt after the test, from the published key": len(
            [g for g in changed if g in groups and groups[g][1] == "K"]
        ),
        "second reading places": n_places,
        "second reading places the same": n_same,
        "second reading places that differ": n_places - n_same,
        "second reading stretches that differ": len(diffs),
        "second reading places corrected in the first from it": len(
            second_notes().get("corrected in the first from this reading", [])
        ),
        "second reading signs identified from a description": len(
            second_notes().get("identified from a description", [])
        ),
        "second reading groups with the letters mapped": len(second_mapped()),
        "proposals for the ten groups": len(props),
        "proposals for the ten groups at 80 or more": len([r for r in props if r[3] >= 80]),
        "proposals for the ten groups given as one word that are the key's": len(
            [r for r in props if not r[4] and proposal_agrees(r, signs, groups)]
        ),
        "proposals for the ten groups given as one word at 50 or less": len(
            [r for r in props if not r[4] and r[3] <= 50]
        ),
        "parallel points": len({r[0] for r in par}),
        "parallel points on groups of the key": len({r[0] for r in on_key}),
        "parallel places on groups of the key": len(on_key),
        "parallel places where the key gives the word": len([r for r in on_key if parallel_ok(r, signs, groups)]),
        "parallel points on the sign for q": len({r[0] for r in par if r[4] == "q"}),
        "parallel places of the sign for q": len([r for r in par if r[4] == "q"]),
        "words in clear within the cipher, omitted": len([r for r in clear_words() if r[5] == "omitted"]),
        "words in clear within the cipher, read": len([r for r in clear_words() if r[5] == "read"]),
        "words in clear within the cipher, omitted in Danvila's print of B and D": len(
            [r for r in clear_words() if r[5] == "omitted" and r[0] in "BD"]
        ),
        "words in clear within the cipher, omitted in the decipherment of C": len(
            [r for r in clear_words() if r[5] == "omitted" and r[0] == "C"]
        ),
        "words in clear within the cipher, read in the decipherment of C": len(
            [r for r in clear_words() if r[5] == "read" and r[0] == "C"]
        ),
    }


def check(signs, groups):
    results = []

    def ok(name, test):
        """Run one check. An error inside it counts as a failure, with the traceback on standard error."""
        try:
            good = bool(test())
        except Exception:
            traceback.print_exc()
            good = False
        results.append((name, good))

    lines = paragraph()
    toks = flat(lines)
    ws = words()
    method, text = page("docs/METHOD.md"), page("docs/TEXT.md")

    # the reading
    ok("every token of the paragraph has a value in the key", lambda: not spell(toks, signs, groups)[1])
    ok("the letters the key gives are the letters of the reading", lambda: reading_ok(signs, groups))
    ok(
        "every added group in the paragraph names the image and the line where it was found",
        lambda: all(places(groups[g][2]) for g in ten(groups)),
    )

    # the division into words
    ok(
        "the words file has the tokens of the paragraph in order",
        lambda: [t for _n, ts, _w in ws for t in ts] == [t for t in toks if not is_mark(t)],
    )
    ok("each word is what its own tokens spell", lambda: words_ok(ws, signs, groups))
    ok(
        "the words in order are the words of the reading",
        lambda: [norm(x) for _n, _ts, w in ws for x in w.split()] == [norm(x) for x in reading().split()],
    )
    ok("the word dividers and the stray dot stand between words", lambda: marks_ok(ws, lines))

    # the two tests
    ok("test passage: no group or sign that the key covers disagrees with 1521", lambda: test_ok(signs, groups))
    ok(
        "test passage: the decipherment column is the decipherment quoted in docs/METHOD.md",
        lambda: decipherment_ok(method),
    )
    ok(
        "test passage: each word that the clerk wrote in clear is the decipherment's word",
        lambda: all(norm(t[1:]) == norm(want) for t, want, _line in test_tokens() if t.startswith("=")),
    )
    ok(
        "test passage: the number of shorter spellings named in docs/METHOD.md is the number listed there",
        lambda: brief_spellings(method)[0] == number_word(len(brief_spellings(method)[1])),
    )
    ok(
        "passage of 1520: every word the key reads is the print's, or the other word the file names",
        lambda: passage_1520_ok(signs, groups),
    )
    ok(
        "passage of 1520: the words of the print in the file come in order in the print quoted in docs/METHOD.md",
        lambda: print_ok(method),
    )

    # the second readings
    second = squeeze(section(method, "Second readings"))
    ok(
        "second transcription: each place where it differs from data/paragraph.txt is named in docs/METHOD.md",
        lambda: (
            compare_second()[2]
            and all(
                "The first has `%s` where the second has `%s`" % (" ".join(places_only(a)), " ".join(places_only(b)))
                in second
                for a, b in compare_second()[2]
            )
        ),
    )
    notes = second_notes()
    ok(
        "second transcription: the groups corrected from it and the signs identified from the reader's description"
        " are in both transcriptions",
        lambda: (
            len(notes) == 2
            and all(t in flat(paragraph()) and t in flat(second_reading()) for k in notes for t in notes[k])
        ),
    )
    ok(
        "second reading: at every point on groups of the key the tokens found give the word with the key's values",
        lambda: all(parallel_ok(r, signs, groups) for r in parallels() if r[4] == "key"),
    )
    ok(
        "second reading: the points on the sign for q name signs that are q",
        lambda: all(spell(r[3], signs, groups)[0] == "q" for r in parallels() if r[4] == "q"),
    )
    ok(
        "second reading: every place of the points is shown in a crop in images/parallels",
        lambda: all(crop_for(r[1]) for r in parallels()),
    )
    ok(
        "second reading: the proposals for the ten groups and the two signs name the key's values, ru.'s as a guess",
        lambda: (
            all(proposal_agrees(r, signs, groups) for r in proposals() if r[1] in ("group", "sign"))
            and {r[0][:-1] for r in proposals() if r[1] == "group"} == set(ten(groups))
        ),
    )

    # controls: the checks above must be able to fail
    def spoiled(g, word):
        return dict(groups, **{g: (word, *groups.get(g, ("", "S", ""))[1:])})

    def without(g):
        return {k: v for k, v in groups.items() if k != g}

    exchanged = dict(signs)
    if "a2" in signs and "o1" in signs:
        exchanged["a2"], exchanged["o1"] = signs["o1"], signs["a2"]
    moved = moved_words(ws, lines)
    misread = [(n, ["rac." if t == "roc." else t for t in ts]) for n, ts in lines]

    ok(
        "control: a changed group value breaks the reading check",
        lambda: not reading_ok(signs, spoiled("fud", "mucho")),
    )
    ok("control: two exchanged signs break the reading check", lambda: not reading_ok(exchanged, groups))
    ok("control: a group removed from the key is reported as missing", lambda: spell(toks, signs, without("fud"))[1])
    ok(
        "control: a word with a token moved to the next breaks the word checks",
        lambda: not words_ok(moved, signs, groups) and not marks_ok(moved, lines),
    )
    ok(
        "control: a changed group value is caught by the test passage",
        lambda: not test_ok(signs, spoiled("hag", "mucho")),
    )
    ok("control: two exchanged signs are caught by the test passage", lambda: not test_ok(exchanged, groups))
    ok(
        "control: a pair of look-alike signs that gives neither letter is caught by the test passage",
        lambda: not test_ok(dict(signs, d3=("x", "K")), groups),
    )
    ok(
        "control: a changed group value in a word of the print is caught by the passage of 1520",
        lambda: not passage_1520_ok(signs, spoiled("hof", "mucho")),
    )
    ok(
        "control: a changed group value in a word the file names is caught by the passage of 1520",
        lambda: not passage_1520_ok(signs, spoiled("ned", "mucho")),
    )
    ok(
        "control: a changed group value is caught by the points on the parallels",
        lambda: not all(parallel_ok(r, signs, spoiled("cu", "mucho")) for r in parallels() if r[4] == "key"),
    )
    ok(
        "control: a group respelt in the first transcription shows as a difference from the second",
        lambda: len(compare_second(misread)[2]) > len(compare_second()[2]),
    )

    # the figures and the pages
    fig = figures(signs, groups)
    texts = {p: prose(p) for p in PAGES}
    have = dict(s.split("\t") for s in rows("figures.txt"))
    ok("the recorded figures are the ones computed now", lambda: have == {k: str(v) for k, v in fig.items()})
    bad = quoted_failures(fig, texts)
    ok("every figure quoted in the pages is the computed one" + "".join(" [%s]" % b for b in bad), lambda: not bad)
    ok(
        "control: every quoted figure fails when the computed one is one higher",
        lambda: len(quoted_failures({k: v + 1 for k, v in fig.items()}, texts)) == len(rows("quoted.tsv")) - 1,
    )
    ok(
        "control: a number inside a longer number does not count as quoted",
        lambda: not quoted_ok("{} words", 48, "148 words") and quoted_ok("{} words", 48, "has 48 words"),
    )
    ok(
        "the transcription in docs/TEXT.md is the one in data/paragraph.txt, line for line",
        lambda: [s for s in fenced_after(text, "## Transcription") if s.strip()] == transcription(),
    )
    ok(
        "the table in docs/TEXT.md is the one the data give, row for row",
        lambda: table_lines(text, "| line | as written |") == table(signs, groups),
    )
    ok(
        "the vocabulary table in docs/METHOD.md is the one the data give, row for row",
        lambda: table_lines(method, "| group begins |")[2:] == blocks(groups),
    )
    ok(
        "the table of the points on the parallels in docs/METHOD.md is the one the data give, row for row",
        lambda: table_lines(method, "| point | place |") == parallel_table(signs, groups),
    )
    ok(
        "the points that have two rows in that table, and the points it omits, are the ones docs/METHOD.md names",
        lambda: parallel_notes_ok(method),
    )
    itext = page("images/README.md")
    shown_boxes = boxes(itext)
    pictures = {
        os.path.relpath(os.path.join(d, f), os.path.join(ROOT, "images")).replace(os.sep, "/")
        for d, _dirs, files in os.walk(os.path.join(ROOT, "images"))
        for f in files
        if not f.endswith(".md")
    }
    scale = {"details/": 3}
    bad = [
        name
        for name, (left, top, right, bottom) in shown_boxes
        if image_size("images/" + name)
        != (scale.get(name[:8], 1) * (right - left), scale.get(name[:8], 1) * (bottom - top))
    ]
    ok(
        "every picture in images/ has a box in images/README.md, of its size or a third of it for the details "
        "(%d boxes)" % len(shown_boxes) + "".join(" [%s]" % n for n in bad),
        lambda: (
            sorted(n for n, _box in shown_boxes) == sorted(pictures)
            and not bad
            and "from the same image and at three times their size" in squeeze(itext)
        ),
    )
    readme = texts["README.md"]
    ok(
        "the first line as README.md displays it is line 1 of the paragraph",
        lambda: first_line_ok(page("README.md"), signs),
    )
    dara = [t for _n, ts, w in ws if w == "dara" for t in ts if t in signs and signs[t][0] == "a"]
    ok(
        "the two signs for a in *dara* are different, as README.md says",
        lambda: len(dara) == 2 and dara[0] != dara[1] and "the two that stand for *a* are different" in readme,
    )
    claims = [c for p in ("README.md", "docs/METHOD.md", "docs/TEXT.md") for c in value_claims(texts[p], signs, groups)]
    wrong = [c for c, good in claims if not good]
    ok(
        "every value given for a group of the key in the forms that README.md names is the key's (%d places)"
        % len(claims)
        + "".join(" [%s]" % c for c in wrong),
        lambda: len(claims) >= 20 and not wrong,
    )
    ok(
        "the evidence for the ten groups in data/groups.tsv spells, with the key, the deciphered text",
        lambda: evidence_ok(groups, signs),
    )
    tested = tested_added(groups)
    ok(
        "the evidence for the other added groups that the tests use spells the deciphered text, and each place has"
        " its crop",
        lambda: (
            tested
            and all(
                evidence(groups[g][2])
                and all(
                    g + "." in toks and norm(spell(toks, signs, groups)[0]) == norm(said) and crop_for(p)
                    for p, toks, said in evidence(groups[g][2])
                )
                for g in tested
            )
        ),
    )
    ok(
        "the table of the ten groups in docs/METHOD.md gives the evidence of data/groups.tsv, item for item",
        lambda: sorted(method_evidence(method)) == sorted((g, *e) for g in ten(groups) for e in evidence(groups[g][2])),
    )
    told = re.findall(
        r"`(\w+)\.`(?: \+ \w+)? (?:stands where the text has|in|\w+ times for) \*([^*]+)\*",
        squeeze(section(page("README.md"), "How it was read")),
    )
    ok(
        "the deciphered words that README.md gives for the ten groups are in their evidence",
        lambda: (
            len(told) >= 4
            and all(
                g in ten(groups) and any(re.search(r"\b%s\b" % re.escape(w), e[2]) for e in evidence(groups[g][2]))
                for g, w in told
            )
        ),
    )
    single = sorted(g for g in ten(groups) if len(places(groups[g][2])) == 1)
    listed = re.search(r"at a single place \(((?:`\w+\.`(?:, )?)+)\)", readme)
    ok(
        "the groups that README.md names as resting on a single place are the ones that do",
        lambda: listed and sorted(re.findall(r"`(\w+)\.`", listed.group(1))) == single,
    )
    in_test = [g for g in (t[:-1] for t, _w, _l in test_tokens() if is_group(t)) if g in ten(groups)]
    only = re.search(r"Only \w+ of the ten groups that the paragraph needs, `(\w+)\.`, is among the groups", readme)
    ok(
        "the one group of the ten in the first test is the one README.md names",
        lambda: only and sorted(set(in_test)) == [only.group(1)],
    )
    ok(
        "the second test has none of the ten groups and neither test has a q, as README.md says",
        lambda: (
            "the second test has none of the ten, and neither test has a q." in readme
            and fig["1520 passage groups among the ten"] == 0
            and fig["test signs for q"] == fig["1520 passage signs for q"] == 0
        ),
    )
    c_images = {i for g in groups.values() for i in images_of(g[2], "C")}
    ok(
        "the values from letter C all come from its second image, as README.md and docs/METHOD.md say",
        lambda: (
            c_images == {2}
            and "all come from its second image" in readme
            and "all come from its second image" in texts["docs/METHOD.md"]
        ),
    )
    qs = q_places(method)
    ok(
        "each sign for q begins in the paragraph the word that docs/METHOD.md names",
        lambda: set(qs) == {"q1", "q2"} and all(any(ts[0] == q and w == qs[q][1] for _n, ts, w in ws) for q in qs),
    )
    ok(
        "the places linked for each sign for q include those of the points on it, and each has its crop",
        lambda: all(parallel_rows_for(q) <= qs[q][0] and all(crop_for(p) for p in qs[q][0]) for q in qs),
    )
    unknown = [want for t, want, _l in test_tokens() if t.startswith("X")]
    pair_want = [want for t, want, _l in test_tokens() if "|" in t]
    named_signs = re.search(r"not in the table: an? (\w), in \*\w+\*, and an? (?:form of )?(\w), in", squeeze(method))
    ok(
        "the signs of the first test that are not in the table, and the look-alike pair, are as docs/METHOD.md says",
        lambda: (
            named_signs
            and list(named_signs.groups()) == unknown
            and len(pair_want) == 1
            and "The decipherment has %s there." % pair_want[0] in squeeze(method)
        ),
    )
    added_test = collections.Counter(
        t[:-1] for t, _w, _l in test_tokens() if is_group(t) and groups.get(t[:-1], ("", ""))[1] == "S"
    )
    named_added = re.search(r"The \w+ added groups among the \d+ are (.*?)\.(?: |$)", squeeze(method))
    ok(
        "the added groups of the first test are the ones docs/METHOD.md names, as often as it says",
        lambda: (
            named_added
            and collections.Counter(
                g
                for g, twice in re.findall(r"`(\w+)\.`( \(twice\))?", named_added.group(1))
                for _ in range(2 if twice else 1)
            )
            == added_test
        ),
    )
    ok(
        "each point of the parallels that docs/METHOD.md describes in words is the point of data/parallels.tsv",
        lambda: (
            all(
                any(norm(w) in norm(r[2] + " " + r[5]) for r in parallels() if r[0] == int(p))
                for p, sentence in re.findall(r"Point (\d+) is (.*?\.)(?: |$)", second)
                for w in re.findall(r"\*([^*]+)\*", sentence)
            )
            and len(re.findall(r"Point \d+ is", second)) >= 2
        ),
    )
    ok("each point that rests on judgement in docs/TEXT.md is in the line it names", lambda: judged_ok(text))
    ok(
        "*primeramente* runs from the end of line 3 to the start of line 4, as docs/TEXT.md says",
        lambda: (
            dict(paragraph())[4][0] == "mud."
            and any(w == "primeramente" and n == 3 and ts[-1] == "mud." for n, ts, w in ws)
            and "*primeramente* begins at the end of line 3 and takes its ending, `mud.`, from the start of line 4"
            in texts["docs/TEXT.md"]
        ),
    )
    logrono = re.search(r"Writing from Logroño on (\d+ \w+ \d{4}).*?Danvila, vol\. 4, p\. (\d+)\)", readme)
    in_sources = re.search(r"the letter from Logroño of (\d+ \w+ \d{4}) \(p\. (\d+)\)", texts["docs/SOURCES.md"])
    ok(
        "the letter from Logroño has the same date and page in README.md and docs/SOURCES.md",
        lambda: logrono and in_sources and logrono.groups() == in_sources.groups(),
    )
    pares = dict(re.findall(r"(?m)^\| (PTR,LEG,2,1,\d+) \| (\d+) \|", page("docs/SOURCES.md")))
    shown = re.findall(
        r"(?m)^\| `(?:parallels|tests)/[^`]+` \| (PTR,LEG,2,1,\d+), image \d+ \| (\d+) \|", page("images/README.md")
    )
    letter_urls = {
        n
        for p in ("README.md", "data/README.md", "images/README.md")
        for n in re.findall(r"description/(\d+)>", page(p))
    }
    ok(
        "the PARES numbers in README.md, data/README.md and images/README.md are those of docs/SOURCES.md",
        lambda: shown and all(pares.get(r) == n for r, n in shown) and letter_urls == {pares.get("PTR,LEG,2,1,19")},
    )
    differ = [(w[3], w[2]) for w in run_1520(signs, groups) if w[3]]
    ok(
        "the words of 1520 that differ from the print are the ones named in README.md and docs/METHOD.md",
        lambda: (
            differ
            and all("| %s | %s |" % d in method for d in differ)
            and all(re.search(r"\*%s\* for (his )?\*%s\*" % d, texts["README.md"]) for d in differ)
        ),
    )
    named = re.findall(r"`([a-z]+)\.` is \*([a-z]+)\*", texts["README.md"])
    ok(
        "the groups given as examples in README.md have the values of the key",
        lambda: len(named) >= 3 and all(g in groups and groups[g][0] == v for g, v in named),
    )
    ten_part = section(method, "The %s groups the paragraph needs" % number_word(10))
    ok(
        "the ten added groups in docs/METHOD.md have the values of the key",
        lambda: all(
            re.search(r"(?m)^\| `%s\.` \| %s \|" % (re.escape(g), re.escape(groups[g][0])), ten_part)
            for g in ten(groups)
        ),
    )
    found, links = method_places(method)
    ok(
        "the ten added groups in docs/METHOD.md are placed where data/groups.tsv places them",
        lambda: all(found.get(g) == places(groups[g][2]) for g in ten(groups)),
    )
    ok(
        "each place in that table links to the crop that shows its line",
        lambda: links and all(crop_for(p) == name for p, name in links),
    )
    clear = method_clear_words(method)
    ok(
        "the words in clear in docs/METHOD.md are those of data/clear_words.tsv, each linked to its crop",
        lambda: (
            [r for r, _name in clear] == clear_words()
            and {r[5] for r in clear_words()} == {"read", "omitted"}
            and all(crop_for(r[:3]) == name for r, name in clear)
        ),
    )
    ok(
        "none of the ten added groups rests on letter B alone",
        lambda: all(letters_named(groups[g][2]) != ["B"] for g in ten(groups)),
    )
    _c, not_in, _wrong = run_test(signs, groups)
    lacking = re.search(r"groups that are not in the key are (.*?), where", squeeze(method))
    ok(
        "the groups of the test passage that docs/METHOD.md names as not in the key are the ones the key lacks",
        lambda: (
            lacking
            and sorted(re.findall(r"`([a-z]+\.)`", lacking.group(1))) == sorted(t for t in not_in if is_group(t))
        ),
    )
    changed, bullets = respelt(method)
    ok(
        "each count in the list of respelt groups in docs/METHOD.md is the number of groups named, all in the key",
        lambda: (
            bullets and all(not w or w == number_word(len(set(gs))) for w, gs in bullets) and changed <= set(groups)
        ),
    )
    word, gone = removed(method)
    passages = toks + [t for t, _want, _line in test_tokens()] + [t for w in run_1520(signs, groups) for t in w[1]]
    used = {t[:-1] for t in passages if is_group(t)}
    ok(
        "the groups that docs/METHOD.md says were removed are as many as it says, and in no passage or the key",
        lambda: gone and word.lower() == number_word(len(gone)) and not set(gone) & (set(groups) | used),
    )
    changed_too = re.search(
        r"(\w+) entries changed at the same time\. .*? It is now entered as `(\w+)\.`.*? Two added groups, `(\w+)\.` "
        r"\(\*\w+\*\) and `(\w+)\.` .*? None of the (\w+) is in the paragraph or in either test passage\.",
        squeeze(method),
    )
    ok(
        "the entries that docs/METHOD.md says changed with the respellings are as many as it says, in the key, and "
        "in no passage",
        lambda: (
            changed_too.group(1).lower() == changed_too.group(5) == number_word(len(set(changed_too.group(2, 3, 4))))
            and "%s added groups lost a mark of doubt" % number_word(len(changed_too.group(3, 4))) in texts["README.md"]
            and all(g in groups and g not in used for g in changed_too.group(2, 3, 4))
        ),
    )
    abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    first, last = (f(12 * int(v[-4:]) + abbr.index(v.split()[-2]) + 1 for v in LETTERS.values()) for f in (min, max))
    months = re.search(
        r"The (\w+) letters behind the added values are of 1521, (\w+) to (\w+) months after", squeeze(method)
    )
    ok(
        "the letters of 1521 are eight to fifteen months later than the paragraph, as docs/METHOD.md says",
        lambda: (
            months.group(1) == number_word(len(LETTERS))
            and months.group(2) == number_word(first - (12 * 1520 + 9))
            and months.group(3) == number_word(last - (12 * 1520 + 9))
        ),
    )
    others = sorted({r[0] for r in parallels() if r[4] == "other"})
    points_named = re.search(
        r"The reading of point (\d+) separated `qof\.` from `gof\.` in B, and point (\d+) corrected", squeeze(method)
    )
    ok(
        "the points that docs/METHOD.md says made the two other changes are the points on other matters, %s" % others,
        lambda: sorted(int(x) for x in points_named.groups()) == others,
    )
    tests_page = squeeze(page("tests/TESTS.md"))
    juntar = re.search(r"\*juntar\* \(points (\d+) and (\d+) of the parallels", tests_page)
    roc = re.search(r"\*embajador\* \(point (\d+) of the points of judgement", tests_page)
    items = re.split(r"(?m)^(\d+)\. ", section(page("docs/TEXT.md"), "Points that rest on judgement"))
    ok(
        "the points that tests/TESTS.md names for *juntar* and *embajador* are those of the parallels and of "
        "docs/TEXT.md",
        lambda: (
            [int(x) for x in juntar.groups()] == [r[0] for r in parallels() if r[2] == "juntar"]
            and "*embajador*" in items[items.index(roc.group(1)) + 1]
        ),
    )
    ok(
        "the letters A to D in docs/METHOD.md have the dates used here",
        lambda: all(
            "| %s | %s" % (k, re.sub(r"[A-Z][a-z]+", lambda m: MONTHS[m.group(0)], v)) in method
            for k, v in LETTERS.items()
        ),
    )
    ok(
        "the reading printed in README.md and docs/TEXT.md is the one in data/reading.txt",
        lambda: all(squeeze(reading()) in texts[p] for p in ("README.md", "docs/TEXT.md")),
    )
    ok(
        "the translation printed in README.md and docs/TEXT.md is the one in data/translation.txt",
        lambda: all(squeeze(translation()) in texts[p] for p in ("README.md", "docs/TEXT.md")),
    )
    bad_links = links_ok()
    ok(
        "every relative link in the pages points to a file" + "".join(" [%s]" % b for b in bad_links),
        lambda: not bad_links,
    )
    return results


def show_test(signs, groups):
    c, not_in, wrong = run_test(signs, groups)
    for token, want, line in test_tokens():
        kind, text, _source = value(token, signs, groups)
        if kind == "mark":
            continue
        if kind == "plain":
            mark = "in clear"
        elif text is None:
            mark = "not in the key"
        elif kind == "pair":
            mark = "agrees" if norm(want) in [norm(a) for a in text.split("|")] else "DISAGREES"
        else:
            mark = "agrees" if norm(text) == norm(want) else "DISAGREES"
        print("%s  %-7s key: %-10s 1521: %-10s %s" % (line, token, text or "-", want, mark))
    print()
    print(
        "groups: %d, of which %d are in the key; %d of those agree with the decipherment"
        % (c["groups"], c["groups_in"], c["groups_ok"])
    )
    print(
        "letter signs: %d, of which %d match one sign of the table; %d of those agree"
        % (c["signs"], c["signs_in"], c["signs_ok"])
    )
    print("look-alike pairs: %d, of which %d contain the letter of the decipherment" % (c["pairs"], c["pairs_ok"]))
    print("not in the key: " + " ".join(not_in))
    for t, text, want in wrong:
        print("DISAGREES: %s gives %s, decipherment has %s" % (t, text, want))


def show_second(signs, groups):
    n_places, n_same, diffs = compare_second()
    print("second transcription, with z read as r and ʒ as z in the groups:")
    print("  places in the first: %d; the second has the same sign or group at %d" % (n_places, n_same))
    for a, b in diffs:
        print("  the first has %s where the second has %s" % (" ".join(a) or "nothing", " ".join(b) or "nothing"))
    print()
    print("proposals from the sense of the passage:")
    for row in proposals():
        token, kind, proposal, conf, _note = row
        if kind in ("group", "sign"):
            mark = "the key's" if proposal_agrees(row, signs, groups) else "NOT the key's"
        else:
            mark = ""
        print(("  %-15s %-12s %3d  %s" % (token, proposal, conf, mark)).rstrip())
    print()
    print("points on the parallels:")
    for row in parallels():
        point, (a, b, c), word, toks, kind, _note = row
        if kind == "key":
            mark = "the key gives the word" if parallel_ok(row, signs, groups) else "THE KEY GIVES ANOTHER WORD"
        else:
            mark = kind
        print("  %2d  %s %d %2d  %-14s %-24s %s" % (point, a, b, c, word, " ".join(toks), mark))
    print()
    print("\n".join(parallel_table(signs, groups)))


def main():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")
    args = sys.argv[1:]
    if len(args) > 1 or (args and args[0] not in MODES):
        print(__doc__)
        return 2
    signs, groups = load_signs(), load_groups()
    arg = args[0] if args else ""
    if arg == "--test":
        show_test(signs, groups)
        return 0
    if arg == "--1520":
        for n, toks, want, _expected, got in run_1520(signs, groups):
            mark = "not in the key" if got is None else ("same" if norm(got) == norm(want) else "DIFFERS")
            print("%d  %-28s key: %-10s print: %-10s %s" % (n, " ".join(toks), got or "-", want, mark))
        return 0
    if arg == "--second":
        show_second(signs, groups)
        return 0
    if arg == "--blocks":
        print("\n".join(blocks(groups)))
        return 0
    if arg == "--figures":
        for k, v in figures(signs, groups).items():
            print("%s\t%s" % (k, v))
        return 0
    if arg == "--table":
        print("\n".join(table(signs, groups)))
        return 0
    if arg == "--check":
        results = check(signs, groups)
        for name, good in results:
            print(("ok    " if good else "FAIL  ") + name)
        n = sum(1 for _name, good in results if good)
        print("%d of %d checks passed" % (n, len(results)))
        return 0 if n == len(results) else 1
    lines = paragraph()
    for n, toks in lines:
        parts = []
        for t in toks:
            kind, text, _source = value(t, signs, groups)
            if kind in ("mark", "plain"):
                parts.append(t if kind == "mark" else text)
            else:
                parts.append("%s=%s" % (t, "[?]" if text is None else text))
        print("%d  %s" % (n, " ".join(parts)))
    print()
    print("the key gives:  " + " ".join(spell(ts, signs, groups)[0] for _n, ts, _w in words()))
    print("the reading is: " + reading())
    same = reading_ok(signs, groups, lines)
    print(
        "the same letters, apart from c/ç, u/v and i/y, which the cipher does not distinguish"
        if same
        else "THE TWO DIFFER"
    )
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
