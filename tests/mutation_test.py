"""Mutation test: deliberate errors in the data, the pages and the script, one at a time.

Each mutant changes one place in one file: a sign, a group or a value copied wrongly, a word divider moved,
a figure, a link or a row of a table changed on a page, or a rule of the script changed (a spelling no
longer folded, a range of lines counted from the wrong place, a comparison reversed). For every mutant
the script copies the repository to a temporary folder, makes the change there, runs
`python code/decode.py --check` and notes whether it fails and which check fails first. The unmodified copy
is run first and must pass.

Some mutants are marked with the reason why the checks are not expected to detect them: they change facts
that the pages quote from their sources (a PARES number, a page) or a line of an image named outside the tables
of evidence, which no computation here can test, or a rule that the data never call on. The script prints
one line for each mutant and ends with status 0 only if every unmarked mutant is detected and every marked
one is not.

usage: python tests/mutation_test.py      (from any folder)
"""

import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUOTED = "a fact quoted from a source, which no computation here tests"

# (description, file, text, replacement[, reason why it is not expected to be detected]);
# the text must occur exactly once in the file
MUTANTS = [
    # the data
    ("paragraph: a sign of *dara* copied wrongly (a4 as o1)", "data/paragraph.txt", "d2 a3 r2 a4", "d2 a3 r2 o1"),
    ("paragraph: `neg.` copied as `nag.`", "data/paragraph.txt", "neg. raf.", "nag. raf."),
    ("paragraph: the stray dot deleted", "data/paragraph.txt", "s3 u3 . mu.", "s3 u3 mu."),
    ("paragraph: a word divider put inside *males*", "data/paragraph.txt", "m2 a1 l4 e3 s1", "m2 a1 / l4 e3 s1"),
    ("words: the second *las* read as *los*", "data/words.tsv", "5\tnad.\tlas", "5\tnad.\tlos"),
    ("key: Kolosova's `nad.` given as *los*", "data/groups.tsv", "nad\tlas\tK", "nad\tlos\tK"),
    ("key: the added `fud.` given as *remedios*", "data/groups.tsv", "fud\tremedio\tS", "fud\tremedios\tS"),
    (
        "key: the place of `fud.` moved a line up",
        "data/groups.tsv",
        "D image 5 line 32: cog.",
        "D image 5 line 31: cog.",
    ),
    ("signs: `a2` given as o", "data/signs.tsv", "a2\ta\t4\tK", "a2\to\t4\tK"),
    ("first test: the decipherment's *poco* copied as *poca*", "data/test_passage.tsv", "hag.\tpoco", "hag.\tpoca"),
    (
        "second test: the print's *Vega* copied as *Vela*",
        "data/passage_1520.tsv",
        "u1 e2 g1 a2\tVega",
        "u1 e2 g1 a2\tVela",
    ),
    (
        "second test: the word that the key gives for `ned.` deleted",
        "data/passage_1520.tsv",
        "ned.\tlo\tla",
        "ned.\tlo\t",
    ),
    (
        "second transcription: a sign of *corona* copied wrongly",
        "data/second_reading.txt",
        "c1 o3 r3 o1 n3 a2 fed.",
        "c1 o3 r3 o1 n3 a1 fed.",
    ),
    (
        "second transcription: a group corrected from it misnamed",
        "data/second_reading.txt",
        "from this reading: qag. qec.",
        "from this reading: qag. qeg.",
    ),
    ("proposals: *pues* recorded as *para*", "data/second_proposals.tsv", "gad.\tgroup\tpues", "gad.\tgroup\tpara"),
    ("parallels: `fud.` recorded as `fed.`", "data/parallels.tsv", "remedio\tfud.\tkey", "remedio\tfed.\tkey"),
    ("parallels: a place moved to a line with no crop", "data/parallels.tsv", "23\tB\t3\t21", "23\tB\t3\t22"),
    ("figures: a recorded count changed", "data/figures.txt", "parallel points\t29", "parallel points\t28"),
    (
        "quoted: a sentence of the README quoted wrongly",
        "data/quoted.tsv",
        "The paragraph has {} words",
        "The paragraph has {} signs",
    ),
    (
        "words in clear: a place that is read marked as omitted",
        "data/clear_words.tsv",
        "juntar grande exercito\tread",
        "juntar grande exercito\tomitted",
    ),
    ("reading: *remedio* as *remedios*", "data/reading.txt", "dara remedio a", "dara remedios a"),
    ("translation: *ills* as *evils*", "data/translation.txt", "to these ills", "to these evils"),
    (
        "key: a deciphered text of `co.` copied wrongly",
        "data/groups.tsv",
        "= que no tienen",
        "= que no tiene",
    ),
    # the pages
    ("README: the groups of the first test as 36", "README.md", "Of 35 groups", "Of 36 groups"),
    ("README: two guesses as three", "README.md", "two of these as guesses", "three of these as guesses"),
    (
        "README: the corrected agreements as three",
        "README.md",
        "two agree because the first",
        "three agree because the first",
    ),
    ("README: an example group with the wrong value", "README.md", "`leb.` is *no*", "`leb.` is *ni*"),
    (
        "README: *dels* printed as *de los* in the reading",
        "README.md",
        "grandes, dels quales",
        "grandes, de los quales",
    ),
    (
        "README: a word of the print named wrongly",
        "README.md",
        "*Hernando* for *Fernando*",
        "*Hernando* for *Hernandez*",
    ),
    (
        "README: the date of the letter from Logroño changed",
        "README.md",
        "Logroño on 14 August",
        "Logroño on 15 August",
    ),
    ("README: the page of the letter from Logroño changed", "README.md", "vol. 4, p. 379", "vol. 4, p. 378"),
    (
        "METHOD: the value of `ded.` changed in the table",
        "docs/METHOD.md",
        "| `ded.` | sola | [A",
        "| `ded.` | solo | [A",
    ),
    (
        "METHOD: a place linked to the wrong crop",
        "docs/METHOD.md",
        "[A, image 3, line 36](../images/parallels/A3_36.jpg)",
        "[A, image 3, line 36](../images/parallels/A3_29-33.jpg)",
    ),
    (
        "METHOD: a place of `gof.` given the wrong line",
        "docs/METHOD.md",
        "[A, image 4, line 4](../images/parallels/A4_01-04.jpg) | `nuf. gof.`",
        "[A, image 4, line 3](../images/parallels/A4_01-04.jpg) | `nuf. gof.`",
    ),
    (
        "METHOD: a place in letter D no longer on its crop",
        "docs/METHOD.md",
        "line 30](../images/parallels/D5_27-32.jpg) | `hof.",
        "line 26](../images/parallels/D5_27-32.jpg) | `hof.",
    ),
    ("METHOD: a word of the vocabulary table changed", "docs/METHOD.md", "| b | ya |", "| b | yo |"),
    (
        "METHOD: a word of the decipherment of 1521 changed",
        "docs/METHOD.md",
        "se contentaria poco en ausencia",
        "se contentaria mucho en ausencia",
    ),
    (
        "METHOD: three shorter spellings as four",
        "docs/METHOD.md",
        "The clerk spelt three words",
        "The clerk spelt four words",
    ),
    ("METHOD: a word of the print of 1898 changed", "docs/METHOD.md", "Fernando de Vega", "Fernando de Vela"),
    ("METHOD: the date of letter D changed", "docs/METHOD.md", "| D | May 1521", "| D | June 1521"),
    ("METHOD: a group dropped from the list of respelt groups", "docs/METHOD.md", "`rud.`, `rib.`;", "`rud.`;"),
    ("METHOD: a group dropped from the groups removed", "docs/METHOD.md", "`no.` (*junto*), ", ""),
    (
        "METHOD: a line changed in the table of the parallels",
        "docs/METHOD.md",
        "| 27 | D, image 5, line 32 | remedio |",
        "| 27 | D, image 5, line 31 | remedio |",
    ),
    (
        "METHOD: a place of `q1` no longer on its crop",
        "docs/METHOD.md",
        "line 12](../images/parallels/C2_08-12.jpg)",
        "line 13](../images/parallels/C2_08-12.jpg)",
    ),
    (
        "METHOD: the difference between the transcriptions misnamed",
        "docs/METHOD.md",
        "where the second has `p1 o4`",
        "where the second has `p1 o1`",
    ),
    ("METHOD: a group the key lacks misnamed", "docs/METHOD.md", "`bab.` and `dah.`", "`bab.` and `dab.`"),
    (
        "METHOD: a point dropped from those the table omits",
        "docs/METHOD.md",
        "omits points 9, 17, 22 and 23.",
        "omits points 9, 17 and 23.",
    ),
    (
        "images README: a box made a pixel wider than its crop",
        "images/README.md",
        "| 100, 1379, 1185, 1433 |",
        "| 100, 1379, 1186, 1433 |",
    ),
    (
        "TEXT: a sign of the transcription changed",
        "docs/TEXT.md",
        "6  c1 o3 r3 o1 n3 a2 fed. /",
        "6  c1 o3 r3 o1 n3 a3 fed. /",
    ),
    ("TEXT: a word of the table changed", "docs/TEXT.md", "| 5 | `hag.` | poco |", "| 5 | `hag.` | poca |"),
    (
        "TEXT: the source of `mu.` given as Kolosova alone",
        "docs/TEXT.md",
        "| Magestad | Kolosova, from the pair `cim. mu.` |",
        "| Magestad | Kolosova |",
    ),
    ("TEXT: the line of *primeramente* given as 4", "docs/TEXT.md", "(line 3, `m2`;", "(line 4, `m2`;"),
    (
        "data README: a link broken",
        "data/README.md",
        "[docs/SOURCES.md](../docs/SOURCES.md)",
        "[docs/SOURCES.md](../docs/SOURCE.md)",
    ),
    (
        "SOURCES: the PARES number of the letter of 24 October 1521 changed",
        "docs/SOURCES.md",
        "PTR,LEG,2,1,94 (PARES 12987679)",
        "PTR,LEG,2,1,94 (PARES 12987680)",
        QUOTED,
    ),
    ("SOURCES: Höfler's pages changed", "docs/SOURCES.md", "no. XXIII, pp. 43-45", "no. XXIII, pp. 43-46", QUOTED),
    (
        "SOURCES: Danvila's pages for the letters of 1 and 6 May changed",
        "docs/SOURCES.md",
        "and 11-12) from the sheet",
        "and 11-13) from the sheet",
        QUOTED,
    ),
    (
        "METHOD: a line of `qof.` in letter B changed",
        "docs/METHOD.md",
        "lines 18 and 20](../images/parallels/B3_18-20.jpg)",
        "lines 17 and 20](../images/parallels/B3_18-20.jpg)",
        "a line of an image named outside the tables of evidence, which the checks do not test",
    ),
    # the script
    ("script: v no longer folded into u", "code/decode.py", '.replace("v", "u")', ""),
    (
        "script: j no longer folded into i",
        "code/decode.py",
        '.replace("j", "i")',
        "",
        "the compared words with a j, juntar and embajador, have it in groups of the key",
    ),
    (
        "script: a pair of look-alike signs no longer recognised",
        "code/decode.py",
        'if "|" in token:',
        'if "/|" in token:',
    ),
    (
        "script: a pair counted as agreeing when it does not",
        "code/decode.py",
        'if norm(want) in [norm(a) for a in text.split("|")]:\n                c["pairs_ok"]',
        'if norm(want) not in [norm(a) for a in text.split("|")]:\n                c["pairs_ok"]',
    ),
    (
        "script: places in letter D no longer read",
        "code/decode.py",
        r'r"\b([ABCD]) image (\d+) line (\d+)", text',
        r'r"\b([ABC]) image (\d+) line (\d+)", text',
    ),
    ("script: a word divider inside a word accepted", "code/decode.py", "if seen not in ends:", "if seen < 0:"),
    ("script: the second reader's z no longer read as r", "code/decode.py", 't.replace("z", "r").replace', "t.replace"),
    (
        "script: the notes of the second transcription no longer read",
        "code/decode.py",
        "|identified from a description): ",
        "|identified from description): ",
    ),
    (
        "script: a quoted number accepted inside a longer number",
        "code/decode.py",
        r'r"(?<![\d.,])%d(?!\d)" % n',
        r'r"%d" % n',
    ),
    (
        "script: the vocabulary sorted with capitals first",
        "code/decode.py",
        "sorted(by[c], key=str.lower)",
        "sorted(by[c])",
    ),
    (
        "script: the words in clear counted wrongly",
        "code/decode.py",
        '"paragraph words in clear": len([t for t in toks if t.startswith("=")])',
        '"paragraph words in clear": len([t for t in toks if t.startswith("/")])',
    ),
    (
        "script: the source of `mu.` no longer named",
        "code/decode.py",
        'if toks == ["mu."] else "Kolosova"',
        'if toks == ["cim."] else "Kolosova"',
    ),
    (
        "script: every occurrence of a decipherer's spelling replaced",
        "code/decode.py",
        'text = re.sub(r"\\b%s\\b" % theirs, clerk, text, count=1)',
        'text = re.sub(r"\\b%s\\b" % theirs, clerk, text)',
    ),
    ("script: a crop no longer shows its first line", "code/decode.py", "c <= line <= d", "c < line <= d"),
    (
        "script: links to other sites taken for files",
        "code/decode.py",
        'if "://" not in target and',
        "if",
        "the pages give the addresses of other sites in angle brackets or as code, never as a link",
    ),
]


def run_check(folder):
    """(exit status, the first check that failed, whether the script stopped with an error, what it printed)."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, os.path.join("code", "decode.py"), "--check"],
        cwd=folder,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )
    failed = [line[6:] for line in proc.stdout.splitlines() if line.startswith("FAIL  ")]
    first = failed[0].split(" [")[0] if failed else ""
    return proc.returncode, first, "Traceback" in proc.stderr, proc.stdout


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    wrong = 0
    with tempfile.TemporaryDirectory() as tmp:
        folder = os.path.join(tmp, "repo")
        shutil.copytree(
            ROOT,
            folder,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".ruff_cache", ".github", ".venv", "venv"),
        )
        status, _, _, output = run_check(folder)
        if status != 0:
            raise SystemExit("mutation_test: the unmodified repository fails its check")
        print("unmodified repository: the check passes")
        last_line = output.splitlines()[-1]
        for number, mutant in enumerate(MUTANTS, start=1):
            description, name, old, new = mutant[:4]
            reason = mutant[4] if len(mutant) > 4 else ""
            path = os.path.join(folder, *name.split("/"))
            with open(path, encoding="utf-8", newline="") as handle:
                text = handle.read()
            if "\r\n" in text:  # a copy whose line ends were converted
                old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
            if text.count(old) != 1:
                raise SystemExit(
                    "mutation_test: mutant %d: the text occurs %d times in %s" % (number, text.count(old), name)
                )
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text.replace(old, new))
            status, first, error, _ = run_check(folder)
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
            if status != 0:
                verdict = "detected (%s%s)" % (first or "the script stopped", ", with an error" if error else "")
            else:
                verdict = "NOT DETECTED" + (" (expected: %s)" % reason if reason else "")
            wrong += (status != 0) == bool(reason)
            print("%2d  %s: %s" % (number, description, verdict), flush=True)
    detected = sum(1 for m in MUTANTS if len(m) == 4)
    print(
        "%d of %d mutants detected as expected; %d not detected, as expected"
        % (detected, len(MUTANTS), len(MUTANTS) - detected)
        if not wrong
        else "%d mutants not as expected" % wrong
    )
    return 1 if wrong or not figures_quoted(detected, last_line) else 0


def figures_quoted(detected, last_line):
    """The figures of this test and of the check that README.md and tests/TESTS.md quote are the true ones."""
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    kinds = {"data": 0, "pages": 0, "script": 0}
    for m in MUTANTS:
        kinds["script" if m[1].endswith(".py") else "pages" if m[1].endswith(".md") else "data"] += 1
    quoted = sum(1 for m in MUTANTS if len(m) > 4 and m[4] == QUOTED)
    others = len(MUTANTS) - detected
    pares = sum(1 for m in MUTANTS if len(m) > 4 and m[4] == QUOTED and "PARES number" in m[0])
    page_refs = sum(1 for m in MUTANTS if len(m) > 4 and m[4] == QUOTED and "pages" in m[0])
    rules = sum(1 for m in MUTANTS if len(m) > 4 and m[1].endswith(".py"))
    kinds_quoted = "(%s PARES number and %s page references)" % ("a" if pares == 1 else words[pares], words[page_refs])
    phrases = [
        ("README.md", "line is `%s` and the exit status is 0" % last_line),
        ("README.md", "The mutation test makes %d deliberate errors" % len(MUTANTS)),
        ("README.md", "if %d are detected and the other %s are not" % (detected, words[others])),
        ("README.md", "these are %s facts quoted from the sources" % words[quoted]),
        ("tests/TESTS.md", "makes %d deliberate errors there" % len(MUTANTS)),
        (
            "tests/TESTS.md",
            "Of these, %d are in the data, %d on the pages and %d in the script."
            % (kinds["data"], kinds["pages"], kinds["script"]),
        ),
        ("tests/TESTS.md", "%s facts quoted from the sources" % words[quoted]),
        ("tests/TESTS.md", "In all, %d of the %d are detected." % (detected, len(MUTANTS))),
        ("tests/TESTS.md", "The %s that are not detected" % words[others]),
        ("README.md", kinds_quoted),
        ("tests/TESTS.md", kinds_quoted),
        ("README.md", "and %s rules of the script that the data and the pages never call on" % words[rules]),
    ]
    good = True
    for name, phrase in phrases:
        with open(os.path.join(ROOT, *name.split("/")), encoding="utf-8") as handle:
            if phrase not in " ".join(handle.read().split()):
                print("%s does not say: %s" % (name, phrase))
                good = False
    return good


if __name__ == "__main__":
    sys.exit(main())
