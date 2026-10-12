# How the paragraph was read

This page gives the evidence for the key, the details of the two tests and the second readings. The README
says what has been checked and what has not.

## The cipher

The nomenclator has an alphabet and a vocabulary. In the alphabet most letters have several signs: Kolosova's
table has 65 signs for 21 letters, from one each for ll and rr to seven for i. One set of signs serves for u
and v, one for i, j and y, and one for c and ç. The paragraph of 1520 uses 39 different signs, two of which
are the signs for q described below.

The vocabulary consists of groups of two or three ordinary letters (a consonant, a vowel and usually one more)
closed by a dot, each standing for a word or for part of one. Endings are added with letter signs or with
another group: `ded. mud.` is *sola-mente*, `neg. raf.` is *lugar-es*, and `ru.` + n is *entiende-n*.

Kolosova's vocabulary for this cipher (thesis, pp. 249-250) has 92 entries. The thesis prints each group as a
picture cut from the manuscript. Four of the entries are not single groups: *aunque* is `yae. gig.`, *contra*
is `vuh.` with letter signs, *estamos* is `ruc. mih.` and *vuestra Majestad* is `cim. mu.`. Each of their
groups except `mu.` has an entry of its own (*aun*, *que*, *con*, *está*, *-mos*, *vuestra*). One more,
*ésta*, has the same picture as *embajador* and was not entered. The other 87, with `mu.` for *Magestad* taken
from the pair `cim. mu.`, are the 88 groups marked K in [data/groups.tsv](../data/groups.tsv). The README
gives the reason for reading `mu.` alone as *Magestad*, and the order of the vocabulary agrees with it:
*Magestad* would stand first among the words of Kolosova's other groups in m-, which run from *maravilla* to
*Napoles*.

Kolosova's examples of a group whose first letter shows that of its word are c for t in *tomo* and *toma* and
h for p in *por* and *para* (pp. 248 and 241). The table sorts the whole vocabulary of this cipher, Kolosova's
groups and the ones added here, by the first letter of the group:

| group begins | words and parts of words |
|---|---|
| z | aca, agra-, algun, allende, almirante, amor, antes |
| y | ahun, al, assi, bastimento, buen, busca |
| x | cardenal, carga, castillo |
| v | cerca, cierto, con, condestable |
| t | como, cosa, deve, so |
| s | de, del, des, dicho, dilata, dinero, dize, do, don, ducado, duque, el, ello |
| r | embajador, en, entiende, entre, envia, es, esta, esteril, esto, fasta, faze |
| q | Francia, fue, Genova, gran, guarda |
| p | ha, halla, han, have, haver, hay, hijo, imperio |
| n | junta, la, las, le, lo, los, luego, lugar, manera, mas |
| m | Magestad, maravilla, mayor, me, menester, menos, mente, mi, miento, mire, mismo, mos, mucho, muy, Napoles |
| l | ni, no, nombre, nuestra, nuestro, obediencia, obispo, obra, otra, otro |
| h | palabra, para, pasa, peor, perdi, place, poco, pode, por |
| g | presta, presto, pues, qual, quando, quanto, que, quiera, quisie |
| f | razon, re, real, remedio, respecto, reyno, roga, sabe |
| d | se, seria, servi, si, sin, sobre, sola, son, su, tal, tambien, tanta, tanto, tene |
| c | tiempo, tiene, toda, todo, toma, tomo, una, Venecia, ver, vez, virrey, visto, vuestra, vuestro |
| b | ya |

The first letters are the consonants in reverse order, z y x v t s r q p n m l h g f d c b, and the words run
forwards from a to y. Two of Kolosova's groups fall under t, where neither word belongs: `taf.` for *deve* and
`tid.`, which the thesis gives as *so/çu*. Either the clerk departed from the order there or their first
letter has been misread from the pictures. Elsewhere the order holds from one block to the next and is loose
where two blocks meet: *ahun*, *al* and *assi* are under y while *algun* and *antes* are under z, and *con* is
under v while *como* and *cosa* are under t. The order therefore narrows a new value to a stretch of the
alphabet without fixing it. The group `fud.` should be a word between *razon* and *sabe*, `gad.` one between
*presta* and *quisie*, and `qag.` one in f- or g-.

Apart from the support it gives to `mu.`, the order supplied no value in the key. Each added value comes from
a parallel passage, named below.

## The letters of 1521

The values that Kolosova's vocabulary lacks were taken from four letters in the same bundle.

| | letter | cipher | deciphered text |
|---|---|---|---|
| A | 5 December 1521 | PTR,LEG,2,1,99, images 1-5 | the decipherment of 1521, same record, images 9-10 |
| B | 24 October 1521 | a sheet wholly in cipher, filed in PTR,LEG,2,1,100, images 3-5 | Danvila, vol. 4, pp. 547-549 |
| C | 7 December 1521 | PTR,LEG,2,1,101, images 1-2 | the decipherment of 1521, same record, image 3 |
| D | May 1521 | a paragraph written into the duplicate of the letter of 6 May 1521, PTR,LEG,2,1,76, image 5 | Danvila, vol. 4, pp. 28-29, in the letter of 23 May 1521 |

For A and C the decipherment of 1521 was read from the images. For B and D the text is Danvila's. B is undated
in the catalogue, and the date in the table is that of the letter whose cipher paragraphs it holds. None of
the ten groups that the paragraph needs rests on B alone.

D is on a sheet marked *Duplicadas* on the back, which copies the cardinal's letters of 1 and 6 May 1521. The
cipher paragraph is written into the copy of 6 May, between its paragraphs on Trujillo and on Saldaña. Danvila
prints both letters from this sheet, omitting the paragraph, under the reference that is written on its back,
and prints the paragraph itself, deciphered, in his text of the letter of 23 May 1521
([SOURCES.md](SOURCES.md) gives the pages). That letter says that the cardinal had his letters duplicated and
sent inside it (*he fecho duplicar mis cartas las quales van insertas en la que va con esta*).

Cipher and deciphered text were aligned passage by passage. Words spelt in letter signs fix the alignment
every few groups, and a group was given a value only where it stands against the same word of the deciphered
text. The 63 added groups are in [data/groups.tsv](../data/groups.tsv) with the image on which each was found.
For the four other added groups that the tests use, `co.`, `sae.`, `dob.` and `cog.`, the file also gives the
line of the places on which their values rest, what is written there and the deciphered text, as it does for
the ten below, and the script spells the text of those places with the key. For the other 49 it names the
image only, and it does the same for further places of `co.`, `sae.` and `dob.` in A. Groups that were noticed
only after the key had been fixed were not entered, and are listed at the end of this page.

The spelling of an added value follows the deciphered texts. They have *faze* for `rof.` in A (*refaze*) and B
(*fazerse*) and *haze* in C (*hazer*), and the key follows A and B. The group `rug.` is *fasta* at both its
places in A.

## Letters that are easily confused

The table of the vocabulary depends on distinguishing letters that look alike in this hand.

- The r that begins the groups for words in e- (Kolosova, p. 243) is shaped like a 2 and is easily taken for
  z. The clear text of the same page begins both words of *rentas reales* with this letter, a few lines above
  the paragraph ([images/details/rentas_reales.png](../images/details/rentas_reales.png)). The z proper, which
  begins the groups for words in a-, has a tail and looks like a 3.
- The q has a straight stem, and the g has a tail closed in a loop, like a figure of eight. So `qag.` (*gran*)
  and `gad.` (*pues*) begin with different letters, and Kolosova's group for *Genova* is `qad.`, with the
  straight q.
- The i has no dot, so `ri.` (*en*) and `ru.` (*entiende*) differ by one short upright stroke (a minim). Both
  are in *entren en Francia entienden* in letter A, with one group between them, and the difference in width
  can be seen there ([A, image 3, line 29](../images/parallels/A3_29-33.jpg)).

The q and the g decide one word of the paragraph. In letter B, `nof. qof. raf. ru.` + n stands where Danvila
prints *los gouernadores entienden*, and letter A has `nof. gof. raf.` for *los quales*. The two middle groups
differ only in their first letter. In the paragraph the group has the loop and is `gof.`, which gives *dels
quales entienden*; with a q it would give *dels gouernadores entienden*. The two groups of line 3 are enlarged
in [images/details/line3_qag_gof.png](../images/details/line3_qag_gof.png).

The clerk distinguishes the two groups. In B, `qof.` stands for *gouernadores* at four places, each with the
straight stem ([image 3, lines 18 and 20](../images/parallels/B3_18-20.jpg),
[line 28](../images/parallels/B3_24-28.jpg), and [image 5, line 13](../images/parallels/B5_13.jpg)), and
`gof.`, for *qual*, has the loop in the line between ([image 3, line 19](../images/parallels/B3_18-20.jpg))
and in D ([image 5, line 27](../images/parallels/D5_27-32.jpg)). These places were found after the key had
been fixed and are not in its table.

## The ten groups the paragraph needs

Each place is given by letter, image and line. The lines are counted from the top of the image, every line of
writing included, deleted lines among them, but not headings, folio numbers or archive marks. Each link opens
a crop of the lines concerned. In the fourth column a letter after `+` is spelt with letter signs.

| group | value | where | as written there | deciphered text |
|---|---|---|---|---|
| `fud.` | remedio | [D, image 5, line 32](../images/parallels/D5_27-32.jpg) | `cog.` + d-a-d-e-r-o `fud.` | verdadero remedio |
| `ded.` | sola | [A, image 1, line 31](../images/parallels/A1_31-34.jpg) | `ri. cam. ded. tu.` | en una sola cosa |
| `qag.` | gran | [B, image 3, line 27](../images/parallels/B3_24-28.jpg) | `vuh. qag. su.` and `nof. qag. su.` | con grandes; los grandes |
| | | [C, image 2, line 10](../images/parallels/C2_08-12.jpg) | `qag. sa.` | grande |
| `gof.` | qual | [A, image 2, line 26](../images/parallels/A2_26-30.jpg) | `nof. gof. raf.` | los quales |
| | | [A, image 4, line 4](../images/parallels/A4_01-04.jpg) | `nuf. gof.` | lo qual |
| | | [D, image 5, line 30](../images/parallels/D5_27-32.jpg) | `hof. nuf. gof.` | por lo qual |
| `ru.` | entiende | [A, image 3, line 4](../images/parallels/A3_03-04.jpg) | `gig. ru.` + n | que entienden |
| | | [A, image 3, line 29](../images/parallels/A3_29-33.jpg) | `ru.` + n `sa. nu.` + r | entienden de juntar |
| | | [B, image 3, line 28](../images/parallels/B3_24-28.jpg) | `ru.` + n | entienden |
| `ceb.` | toda | [A, image 3, line 31](../images/parallels/A3_29-33.jpg) | `ceb.` + g-u-i-p-u-z-c-o-a | toda Guipuzcoa |
| | | [B, image 3, line 25](../images/parallels/B3_24-28.jpg) | `sa. ceb. yof.` + a | de toda buena |
| `gad.` | pues | [B, image 5, line 13](../images/parallels/B5_13.jpg) | `gad.` | pues |
| | | [C, image 2, line 8](../images/parallels/C2_08-12.jpg) | p-e-r-o `su. gad.` | pero despues |
| `neg.` | lugar | [A, image 2, line 27](../images/parallels/A2_26-30.jpg) | `ri. loh.` + s `neg. raf.` | en otros lugares |
| `cu.` | tiempo | [A, image 1, line 34](../images/parallels/A1_31-34.jpg) | `so. cu.` | del tiempo |
| | | [A, image 3, line 3](../images/parallels/A3_03-04.jpg) | `sa. cu.` | de tiempo |
| | | [A, image 3, line 29](../images/parallels/A3_29-33.jpg) | `yee. sib. cu.` | al dicho tiempo |
| `fed.` | real | [A, image 3, line 36](../images/parallels/A3_36.jpg) | `fed. raf.` | reales |
| | | [A, image 4, line 2](../images/parallels/A4_01-04.jpg) | c-o-r-o-n-a `fed.` | corona real |

Line 27 of B has `qag. su.` twice. In D, `cog.` + d-a begins at the end of line 31, and in A, `ri. loh.` + s
stands at the end of line 26. After `fud.`, on line 32 of D, the cipher has a letter sign and `gig.` (*que*)
that Danvila's print does not have.

In the last row letter A spells *corona* in letter signs and adds `fed.` for *real*, as the paragraph of 1520
does in its last line.

The groups `cab.` (*todo*) and `ceb.` (*toda*) are a pair, like `cem.` (*vuestro*) and `cim.` (*vuestra*), and
at no place read here does one stand for the other.

The three groups that rest on a single place all fall among Kolosova's own groups with the same first
letter: `fud.` (*remedio*) between *re* and *sabe*, `ded.` (*sola*) between *sin* and *son*, and `neg.`
(*lugar*) between *los* and *mas*. The group `gad.` (*pues*) falls in the gap between the last of Kolosova's
groups in h-, for *por*, and the first in g-, for *quando*. With the group beside them at one place, `ded.`,
`neg.` and `gad.` make familiar words (*sola-mente*, *lugar-es*, *des-pues*).

## The letter q

Kolosova's table has no sign for q, and the letters of 1521 show two.

- The sign `q1` is the first sign for p, which looks like tt, joined by its bar to a tall long s with a small
  ring at the top, and a sign for u follows it. It is in *quatro*
  ([A, image 3, line 32](../images/parallels/A3_29-33.jpg)) and in one *quinientos*
  ([A, image 4, line 1](../images/parallels/A4_01-04.jpg)) in A, in *quiteme* in B
  ([image 3, line 21](../images/parallels/B3_21.jpg)) and in *quatro* in C
  ([image 2, line 12](../images/parallels/C2_08-12.jpg)), and it begins *quiça* in the paragraph
  ([images/details/line1_quica_esto.png](../images/details/line1_quica_esto.png)).
- The sign `q2` is a small ring with a stroke to the right and a tail curling down to the left. It is in the
  other *quinientos* in A ([image 3, line 33](../images/parallels/A3_29-33.jpg)) and in *quitaciones* in B
  ([image 3, line 26](../images/parallels/B3_24-28.jpg)), and it begins *quitar* in the paragraph
  ([images/details/line4_quitar.png](../images/details/line4_quitar.png)).

Whether `q1` is one sign or two written together cannot be decided from the images. Its second part does not
occur alone in the letters read, and the four places in the letters of 1521 show only that the whole stands
for q.

## Words in clear within the cipher

The paragraph opens with two words in clear, *quanto mas*. Kolosova writes of this cipher that its only
markers are words in clear at the head of a paragraph in cipher, function words such as *como*, *quanto*,
*pero* and *quien* that are not to be read; that one of Lope Hurtado's ciphers has something similar; and that
their use depends much on the secretary, so that in many cases they are omitted altogether (p. 229). The
letters of 1521 have words of this kind at the head of cipher passages and within them. Each letter was
searched for them on the images, and the table gives every place found
([data/clear_words.tsv](../data/clear_words.tsv)), with the deciphered text where the cipher resumes: for A
and C the decipherment of 1521, and for B and D Danvila's print.

| place | in clear | deciphered text | |
|---|---|---|---|
| [B, image 3, line 1](../images/parallels/B3_01.jpg) | *Como quien* | *Acá aparejamos* | omitted |
| [B, image 3, line 7](../images/parallels/B3_07.jpg) | *pero mas* | *El Almirante y el Condestable* | omitted |
| [B, image 3, line 18](../images/parallels/B3_18-20.jpg) | *quanto* | *entre estos gouernadores* | omitted |
| [B, image 3, line 21](../images/parallels/B3_21.jpg) | *pero* | *quitóme* | omitted |
| [B, image 3, line 25](../images/parallels/B3_24-28.jpg) | *como* | *buena obra común ha mas* | omitted |
| [B, image 3, line 34](../images/parallels/B3_34.jpg) | *Quanto* | *El Condestable estima* | omitted |
| [B, image 4, line 12](../images/parallels/B4_12.jpg) | *quien mas* | *El duque del Infantazgo* | omitted |
| [B, image 4, line 25](../images/parallels/B4_25.jpg) | *pero* | *pero conviene* | read |
| [B, image 5, line 1](../images/parallels/B5_01.jpg) | *como* | *digo lo del vender* | omitted |
| [B, image 5, line 13](../images/parallels/B5_13.jpg) | *simo que* | *estos gouernadores pues* | omitted |
| [C, image 1, line 28](../images/parallels/C1_28-32.jpg) | *pero sin* | *no teniendo la pero sin el poder* | read |
| [C, image 1, line 32](../images/parallels/C1_28-32.jpg) | *Quanto menos* | *De exortar a los grandes* | omitted |
| [C, image 2, line 10](../images/parallels/C2_08-12.jpg) | *quanto al* | *Quanto al juntar grande exercito* | read |
| [D, image 5, line 24](../images/parallels/D5_24.jpg) | *Como quien* | *El duque de nagera* | omitted |
| [D, image 5, line 30](../images/parallels/D5_27-32.jpg) | *pero mas* | *V. M. venga* | omitted |

The deciphered text omits the words in clear at twelve of these places and reads them at three. Eleven of the
twelve omissions are in Danvila's print of B and D, and the decipherment of 1521 of
C omits such words at one place and reads them at two. In B, image 3, line 25, the *común* of the print is
spelt in letter signs at the start of the next line. The words that are read are *pero* and *pero sin* inside
a sentence, in B and C, and *quanto al* at the head of one, in C. The nearest in form to *quanto mas* is C's
*Quanto menos*, which opens a new matter and which the decipherer of 1521 omitted. Longer phrases in clear,
which A and C have often, are part of the text: the passage of the first test opens with *Lo que* in clear,
and its third line ends with a clause in clear.

The paragraph is complete without *quanto mas*, which is probably an opening of the kind that is not
read. The reading prints the two words in braces, and no other word of it would change if they were
read as part of the text.

## The first test: 7 December 1521

The test passage is the first six lines of the cipher paragraph on the first image of letter C, which follows
the clear text at the top of the page
([images/tests/C1_test_passage.jpg](../images/tests/C1_test_passage.jpg)). The key's values from that letter
all come from its second image. The clerk wrote the second half of the third line in clear (*haviendo vra al.
de venir tan presto como lo scrive y es necessario*), and the bracketed gap in the quotation stands for those
words. The decipherment of 1521 reads:

> Lo que scrivimos a v. mad de la concession de los capitulos o parte dellos ante su venida no me parece que
> conviene [...] ca ottorgando todos los capitulos seria danyoso a v. mad y concediendo tan solamente parte
> dellos el pueblo se contentaria poco en ausencia

The passage was transcribed sign by sign ([data/test_passage.tsv](../data/test_passage.tsv)), and the script
applies the key to it. Where the decipherment abbreviates *vuestra magestad* as *v. mad*, the file gives the
two words in full against `cim. mu.`.

| | in the passage | in the key | agree with the decipherment of 1521 |
|---|---|---|---|
| groups | 35 | 31 | 31 |
| letter signs | 93 | 90 | 90 |

The four groups that are not in the key are `daf.`, `tib.`, `bab.` and `dah.`, where the decipherment has
*scrivi*, *conviene*, *yo* (in *danyoso*) and *tan*. Two signs are not in the table: a b, in *pueblo*, and a
form of t, in *contentaria*. One sign could not be distinguished from its look-alike in the scan (the first
sign for p, which looks like tt, and the d shaped like an H), and it is entered as either. The decipherment
has d there.

The clerk spelt three words more briefly than the decipherer: *concesion* for the decipherment's
*concession*, *otorgando* for *ottorgando*, and *dello* for *dellos*.

The four added groups among the 31 are `sae.` (twice), `dob.` and `ded.`.

## The second test: 8 October 1520

The four letters behind the added values are of 1521, eight to fifteen months after the paragraph. One short
passage in the same cipher is closer. In his letter of 8 October 1520 (PTR,LEG,2,1,23, image 3;
[images/tests/no23_1520_passage.jpg](../images/tests/no23_1520_passage.jpg)) the cardinal added a paragraph
that begins *Despues de scripto lo de hasta aqui*, "after what is above had been written", and it has 22 words
in cipher among words in clear. Danvila printed it in 1898 in a decipherment by Claudio Pérez y Gredilla:

> acerca lo del Mariscal de Navarra sobre lo qual screui con personas propias á Fernando de Vega y al Teniente
> que tiene en Simancas todo lo que convenia el mesmo Teniente me ha respondido lo que vra M.at vera por lo que
> va con esta

The cipher words were transcribed after the key was fixed and its groups respelt
([data/passage_1520.tsv](../data/passage_1520.tsv)), and nothing in the key comes from them. The script prints
the comparison word by word with the option `--1520`.

The key reads 20 of the 22 words. The two it cannot read are *Navarra*, written with a group it does not have
(`mal.`), and the second *Teniente*, which is spelt in letter signs and begins with the form of t that is
missing from the table. Of the 20 words, 16 are letter for letter the words of the print, and the table gives
the other four.

| cipher | the key gives | the print has |
|---|---|---|
| m-a-r-i-c-h-a-l | marichal | Mariscal |
| h-e-r-n-a-n-d-o | Hernando | Fernando |
| `co.` + n-t-e | tienente | Teniente |
| `ned.` | la | lo |

*Hernando* is a common form of *Fernando* at the time, and *marichal* may be a form of *mariscal* or a slip.
In *tienente* the clerk saved signs by writing the group for *tiene* and adding n-t-e, and spelt the word in
full a line later. At the last place the key's *por la que va con esta*, "by the one that goes with this",
speaks of an enclosed letter, as *la que va con esta* does in the letter of 23 May 1521. On the image the
group reads `ned.` (line 5 of the crop), so the print's *lo* is more likely a slip of the decipherer or of the
printer.

At its last word the passage has `ruc.`, which Kolosova lists as the verb *está*. Here the word is the
demonstrative, which the thesis treats as a separate word with a group of its own, the one whose picture is
that of *embajador* (pp. 243 and 249).

The passage has 15 groups. Three of them carry values that were added from the letters of 1521: `cog.` gives
*ver* in *vera*, a value that comes from letter D alone, and `co.` gives *tiene* once as a word and once as
the first part of *tienente*.

## Second readings

The paragraph, and chosen places in the parallel passages, were read a second time from enlargements of the
images, each by a reader who had not seen the first transcription.

### The paragraph

The second transcription ([data/second_reading.txt](../data/second_reading.txt)) was made with Kolosova's
table of signs and vocabulary to hand (thesis, pp. 227 and 249-250), and with instructions that described how
the cipher is written. They named the two words in clear with which the paragraph opens, gave the group for
*todo* with a sign for s as an example of an ending, and warned that g and q look alike and that the clerk's z
at the start of a group can look like r, which was then the view of the first transcription. Two overview
images showed the paragraph in its place, with three lines of clear text above it and two below. The
letters of 1521, the first transcription and the rest of the letter of 1520 were out of view.

Compared with the reader's letters read as the [README](../README.md#second-readings) describes, the second
transcription has the same sign or group as the first at 111 of the 112 positions. The
first has `q1` where the second has `p1 o4`, dividing the first sign of *quiça* into p and o and making
*pouica*, which is no word. The letters of 1521, which the second reader did not see, show the pair standing
for q, and the division was not adopted.

Not all of the 111 agreements are independent. In two groups, `qag.` and `qec.`, the first transcription had
read the first letter as g and was corrected from the second, which has q; on the image both have the straight
stem. Two signs the reader could not find in the table were described in words, an "L with a loop", likened
to m without its top bar, and "a small o with a side stroke and a looped tail". In the comparison they carry
the identifiers of the first transcription, `m2` and `q2`.

Kolosova's key left the reading open at the ten groups and at the two signs for q. The reader then proposed
values for these places from the sense of the passage, with a confidence for each, separately from the
transcription ([data/second_proposals.tsv](../data/second_proposals.tsv)). Nine of the proposals for the
groups are the values that the letters of 1521 give, seven of them at a confidence of 80 per cent or more and
two, *remedio* for `fud.` and *qual* for `gof.`, at 50 per cent or less. For `ru.` + n the proposal was "a
plural verb, perhaps *entienden*", at 30 per cent. The reader also proposed q for the sign in line 4 and m
for the doubtful sign in *primeramente*. For the first word in cipher the proposal was *publica*, which the
letters of 1521 do not support, and for `so.` + s it was *de los*.

### The parallel passages

Another reader was given enlarged strips of seven passages from letters A to D with their deciphered text,
and neither the key nor the paragraph. For A and C the deciphered text was this study's transcription of the
decipherment of 1521, and for B and D Danvila's print. At 29 numbered points, chosen in this study, the
reader was asked which signs or groups stand for a given word ([data/parallels.tsv](../data/parallels.tsv)).
The instructions said that the same group always has the same value, and warned that g and q look alike
and that the group then written `zi.`, now `ri.` (*en*), can look like a u with a stroke in front, since the
i has no dot.

Of the 29 points, 25 concern groups of the key, at 27 places, and at each the tokens that the reader found
give the word with the key's values:

| point | place | word | tokens found | with the key's values |
|---|---|---|---|---|
| 1 | A, image 1, line 31 | sola | `ded.` | sola |
| 2 | A, image 1, line 34 | tiempo | `cu.` | tiempo |
| 3 | A, image 1, line 32 | es | `raf.` | es |
| 4 | A, image 2, line 26 | quales | `gof. raf.` | qual-es |
| 5 | A, image 2, line 27 | lugares | `neg. raf.` | lugar-es |
| 6 | A, image 2, line 30 | des | `su.` | des |
| 7 | A, image 3, line 3 | tiempo | `cu.` | tiempo |
| 8 | A, image 3, line 4 | entienden | `ru.` + n | entiende-n |
| 10 | A, image 3, line 29 | entienden | `ru.` + n | entiende-n |
| 11 | A, image 3, line 29 | juntar | `nu.` + r | junta-r |
| 12 | A, image 3, line 29 | tiempo | `cu.` | tiempo |
| 13 | A, image 3, line 31 | toda | `ceb.` | toda |
| 14 | A, image 3, line 36 | reales | `fed. raf.` | real-es |
| 15 | A, image 4, line 2 | corona real | c-o-r-o-n-a `fed.` | c-o-r-o-n-a real |
| 16 | A, image 4, line 4 | qual | `gof.` | qual |
| 18 | B, image 3, line 24 | poco | `hag.` | poco |
| 19 | B, image 3, line 25 | toda | `ceb.` | toda |
| 20 | B, image 3, line 27 | grandes | `qag. su.` | gran-des |
| 20 | B, image 3, line 27 | grandes | `qag. su.` | gran-des |
| 21 | B, image 3, line 28 | entienden | `ru.` + n | entiende-n |
| 24 | C, image 2, line 8 | despues | `su. gad.` | des-pues |
| 25 | C, image 2, line 10 | grande | `qag. sa.` | gran-de |
| 26 | C, image 2, line 10 | juntar | `nu.` + r | junta-r |
| 27 | D, image 5, line 32 | remedio | `fud.` | remedio |
| 28 | D, image 5, line 30 | qual | `gof.` | qual |
| 29 | D, image 5, line 31 | todo | `cab.` | todo |
| 29 | D, image 5, line 32 | todo | `cab.` | todo |

Point 20 has two rows because line 27 of B has `qag. su.` twice, and point 29 because `cab.` stands in lines
31 and 32 of D. The table omits points 9, 17, 22 and 23.

Two points, 17 and 23, concern the signs for q, at 5 places. Their questions asked how q is written there,
without describing the signs, and the reader described them as above. Point 22 is the group in B where Danvila
prints *gouernadores*. Its question asked the reader to compare the tokens with the same tokens at other
points, and the reader read the group as `qof.`, with the straight q of `qag.`, and so distinguished it from
`gof.`. The first reading had not done so at that place, though no value in the key had been taken from it.
Point 9 is the o at the end of a word that the text supplied gave by mistake as *en punto*. The reader read
*enxuto*, which is what the decipherment of 1521 has.

Each point that the second readings raised was checked on the images before anything was changed.

## What changed after the test

No group changed its word after the first test, but 23 groups were respelt, in the key and in every
transcription together, so that each mark on the page keeps the word it had. They fall into five sets.

- nine groups in r- that had been written with z: `ri.`, `ru.`, `raf.`, `roc.`, `reb.`, `rac.`, `ruc.`,
  `rud.`, `rib.`;
- seven groups in z- that had been written with a 3 for the tailed z: `zi.`, `zed.`, `zie.`, `zoe.`, `zuf.`,
  `zid.`, `zee.`;
- four groups in q- that had been written with g: `qec.`, `qag.`, `qah.`, `qib.`;
- two groups whose first letter had been misread, `rug.` (*fasta*) and `rof.` (*faze*), the second of which
  had also been entered with C's spelling *haze*;
- one group written without its vowel, `cim.` (*vuestra*).

Of these, 13 are groups of Kolosova's vocabulary. Since the groups in r- had been written with z and those in
z- with 3, a spelling can name one group in the tested key and another now: as tested, `zi.` was *en*,
which is now `ri.`, and `3i.` was *aca*, which is now `zi.`.

Three entries changed at the same time. Kolosova's group for *Genova* had been entered as `gad.`, with a g,
and rejected for *pues*, the value that letter C gives the same letters. It is now entered as `qad.`, with the
straight q, beside `gad.` for *pues*. Two added groups, `ga.` (*presta*) and `ge.` (*presto*), had been
entered with their letters marked as uncertain and are now entered without the mark. None of the three is in
the paragraph or in either test passage.

The second readings brought about some of these changes and two others. The q of `qag.` and `qec.` came from
the second transcription of the paragraph, and the q of `qah.` and `qib.` and the entry of `qad.` followed
from it. The reading of point 22 separated `qof.` from `gof.` in B, and point 9 corrected *en punto* to
*enxuto* in the transcription of A's decipherment.

Four groups of the first reading were removed from the key because their places had not been checked again
after these corrections: `xud.` (*caso*), `no.` (*junto*), `lab.` (*ningun*) and `puh.` (*intencion*). None of
them is in the paragraph or in either test passage. The first test was run again on the respelt transcription
and gave the same counts. The second was transcribed after the respelling and has been run only on it.

The place of `gad.` in B, image 5, line 13, was found after both tests and entered as a second place in its
evidence. The value of the group did not change.

## Groups seen in passing

These values were noticed while the passages were being checked. None is in the key or was tested, and each
rests on one reading, at one place except `qof.`, which is at four places in B (above), and `mal.`, which is
in D ([image 5, line 24](../images/parallels/D5_24.jpg), *de navarra*) as well as in the passage of the second
test. The last four are the groups of the first test passage that the key lacks, with the word that the
decipherment of 1521 has at each; all four fit the order of the vocabulary.

| group | word |
|---|---|
| `qof.` | gouernador |
| `qid.` or `qud.` | gente |
| `qog.` | gruesa |
| `rag.` | falta |
| `ra.` | ella |
| `zud.` | aleman |
| `zuc.` | agora |
| `cul.` | uno |
| `xeg.` | cargo |
| `fo.` | Rey |
| `fof.` | the *ren-* of *rentas* |
| `yac.` | artilleria |
| `mal.` | Navarra |
| `daf.` | scrivi |
| `tib.` | conviene |
| `bab.` | yo, in *danyoso* |
| `dah.` | tan |
