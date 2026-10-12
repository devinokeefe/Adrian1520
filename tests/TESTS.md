# Tests

    python tests/mutation_test.py

The command can be run from any folder. It copies the repository to a temporary folder and makes 72 deliberate
errors there, one at a time, running `python code/decode.py --check` after each and putting the file back
before the next. What it printed is in [runs/mutation_test.txt](../runs/mutation_test.txt).

Of these, 23 are in the data, 34 on the pages and 15 in the script. In the data a sign or a group of the
paragraph is copied wrongly, the stray dot is deleted, a word divider is put inside a word, a value of the key
is changed, a place of an added group is moved, a word of a deciphered text is copied wrongly, and a sign of
the second transcription, a group named in its notes, a proposal, a point of the parallels, a recorded figure,
a quoted sentence, a word in clear marked as omitted, a word of the reading and a word of the translation are
changed. On the pages the changes touch a figure, a number word, a group or a word of the reading, a row of a
table, a link, a place no longer on its crop, a word of a quoted decipherment, the date of one of the letters,
a group of a list, a point that a table omits, the box of a crop, the line of a sign in the paragraph and the
source of a value, and also three facts quoted from the sources (a PARES number and two page references) and
the line of a group on an image of letter B. In the script a spelling is no longer folded, a pair of
look-alike signs is no longer recognised or is counted the wrong way, the places of one letter are no longer
read, a word divider is accepted inside a word, the second reader's letters are no longer mapped, the notes of
the second transcription are no longer read, a quoted number is accepted inside a longer one, the vocabulary
is sorted another way, a count is taken wrongly, the source of `mu.` is no longer named, a spelling is
replaced too often, a crop is counted from the wrong line, and links to other sites are taken for files.

In all, 66 of the 72 are detected. The six that are not detected are marked in the list in
`mutation_test.py` with the reason, and the script ends with status 0 only if exactly these six pass
unnoticed.

- The checks do not test the three facts quoted from the sources, or the lines of letter B named in
  the description of `qof.`, which lie outside the tables of evidence. The checks test the reading, the
  tests, the figures, the tables and the places of the evidence, which are tied to the crops in
  `images/parallels/`, and they compare a few of the dates and pages that two pages both give.
- j is no longer folded into i. The comparisons fold j into i because one set of signs serves for both, but
  the two words with a j that are compared with the key, *juntar* (points 11 and 26 of the parallels, and
  the evidence for `ru.`) and *embajador* (point 4 of the points of judgement in docs/TEXT.md), meet it in
  groups whose values, *junta* and *embajador*, have a j too, so the rule is never needed.
- Links to other sites are taken for files. The link check skips the addresses of other sites, but the
  pages write those addresses in angle brackets or as code, never as the target of a link, so this rule is
  never needed either.

The test also confirms that the README gives the last line that the check prints and the figures of this
test, and that this page gives the counts above.

## What the tests do not reach

A sign transcribed wrongly from the image is detected only if it changes a letter of the reading or a figure,
and the same error made in a transcription and on a page cannot be detected at all. A change that only weakens
a check, such as a comparison that always succeeds, does not show while the data and the pages are right. The
controls in the check and the errors above show that the checks they touch are made, and the test does not try
an error against every check.
