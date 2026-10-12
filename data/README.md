# Data

All the files are UTF-8 text with tabs between columns. Lines beginning with `#` are comments that say what
the file is and where it comes from.

| file | what |
|---|---|
| `paragraph.txt` | the six lines of the paragraph, sign by sign |
| `signs.tsv` | the letter signs: an id, the letter, a description of the shape, and the source |
| `groups.tsv` | the groups: the group, its value, the source, and for the added groups where the value was found (for the ten that the paragraph needs and the four others that the tests use, the image and the line of the places whose text the check spells with the key) |
| `words.tsv` | the paragraph divided into words, each with its signs and groups |
| `reading.txt` | the text as read, in one line, with the two opening words in clear in braces |
| `translation.txt` | the English translation, in one line |
| `test_passage.tsv` | the first test: six lines of the letter of 7 December 1521, sign by sign, with the decipherment of 1521 beside each |
| `passage_1520.tsv` | the second test: the cipher words of a paragraph of the letter of 8 October 1520, with the word printed in 1898 beside each |
| `second_reading.txt` | the second transcription of the paragraph, as the second reader wrote it |
| `second_proposals.tsv` | the values that the second reader proposed from the sense of the passage for the places that Kolosova's key left open |
| `parallels.tsv` | the second reading of the parallel passages: at each point, the word in question and the tokens found |
| `clear_words.tsv` | the short words in clear within the cipher of letters A to D, and whether the deciphered text has them |
| `figures.txt` | the counts the script takes from the data and from the lists that the pages give |
| `quoted.tsv` | the sentences of the pages that quote those counts, so that the script can check the prose |

## Conventions

- A letter sign is written as its letter and a number: `a2` is the second sign from the top in the column for
  a in Kolosova's table (thesis, p. 227). The `u` signs serve for u and v, the `i` signs for i, j and y, and
  the `c` signs for c and ç. The two signs for q, which the table lacks, are written `q1` and `q2`.
- A group is written in its own letters with the closing dot: `gig.`
- The clerk's word divider is written `/`. A lone `.` is a dot on the page that belongs to no group.
- A word that the clerk wrote in clear inside a cipher passage has `=` in front: `=quanto`.
- A sign that could be either of two that look alike is written with both, as `p1|d3`. The signs written `X1`
  and `X2` are not in the table.
- In `parallels.tsv` a letter sign is written `+` and its letter (`+n`), since the second reader described the
  signs rather than matching them to the table.
- Source `K` is Kolosova's thesis. Source `S` is this study, and the letters A to D named in the `where`
  column are listed at the top of `groups.tsv`.
- Values are in the spelling of the letters themselves, without accents.
- In `second_reading.txt` the groups are as the reader wrote them, and the
  [README](../README.md#second-readings) says how the script reads the reader's letters before comparing.

## Where the images are

The paragraph is on the first image of
<https://pares.cultura.gob.es/ParesBusquedas20/catalogo/description/12987122>. The other records are listed in
[docs/SOURCES.md](../docs/SOURCES.md), and the crops in `images/` in [images/README.md](../images/README.md).
The transcriptions were made from enlargements of the PARES images.
