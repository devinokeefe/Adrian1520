# Images

Every picture here is cut from an image of a letter in the Archivo General de Simancas as PARES shows it
(España, Ministerio de Cultura, Archivo General de Simancas). The README of the repository gives the
conditions of use. A box is given in pixels of the PARES image, as left, top, right and bottom, and the image
number is that of the PARES viewer.

## The paragraph

The file `paragraph.jpg` shows the paragraph and the lines around it at the size of the PARES image. It is the
box 170, 868, 1150, 1178 of image 1 of PTR,LEG,2,1,19, the letter of 9 September 1520
(<https://pares.cultura.gob.es/ParesBusquedas20/catalogo/description/12987122>).

## Details of the letter of 1520

These files show the places in the paragraph that rest on judgement ([docs/TEXT.md](../docs/TEXT.md)) and
the words *rentas reales* of the clear text a few lines above it, from the same image and at three times
their size.

| file | box | shows |
|---|---|---|
| `details/line1_quica_esto.png` | 195, 920, 610, 975 | line 1: *quiça* with its first sign `q1`, and the first `roc.` |
| `details/line2_su_dot_mu.png` | 690, 955, 1060, 1005 | line 2: `s3 u3`, the stray dot and `mu.` |
| `details/line3_qag_gof.png` | 400, 990, 800, 1045 | line 3: `qag.` with the straight q and `gof.` with the looped g |
| `details/line3_primeramente.png` | 760, 990, 1150, 1045 | line 3: *primeramente* with the m that lacks its bar |
| `details/line4_quitar.png` | 170, 1028, 470, 1080 | line 4: *quitar* with its first sign `q2` |
| `details/rentas_reales.png` | 880, 708, 1110, 752 | the clear text above the paragraph: *rentas reales*, both words beginning with the r shaped like a 2 |

## Lines of the parallel passages

These are the lines that [docs/METHOD.md](../docs/METHOD.md) and [data/groups.tsv](../data/groups.tsv) name
for the ten added groups and the four others that the tests use, the two signs for q, the groups `qof.` and
`gof.` and the words in clear within the cipher, at the size of the PARES image. Each file is named by letter,
image and lines: `A3_29-33.jpg` is lines 29 to 33 of the third image of letter A, with the lines counted as
docs/METHOD.md says. Each crop runs the width of the page and from a little above the first line named to a
little below the last.

| file | record | PARES | box |
|---|---|---|---|
| `parallels/A1_31-34.jpg` | PTR,LEG,2,1,99, image 1 | 12987701 | 100, 1266, 1185, 1422 |
| `parallels/A2_26-30.jpg` | PTR,LEG,2,1,99, image 2 | 12987701 | 100, 1042, 1166, 1234 |
| `parallels/A3_03-04.jpg` | PTR,LEG,2,1,99, image 3 | 12987701 | 100, 208, 1185, 296 |
| `parallels/A3_29-33.jpg` | PTR,LEG,2,1,99, image 3 | 12987701 | 100, 1127, 1185, 1323 |
| `parallels/A3_36.jpg` | PTR,LEG,2,1,99, image 3 | 12987701 | 100, 1379, 1185, 1433 |
| `parallels/A4_01-04.jpg` | PTR,LEG,2,1,99, image 4 | 12987701 | 100, 144, 1166, 300 |
| `parallels/B3_01.jpg` | PTR,LEG,2,1,100, image 3 | 12987720 | 100, 186, 1170, 238 |
| `parallels/B3_07.jpg` | PTR,LEG,2,1,100, image 3 | 12987720 | 100, 378, 1170, 430 |
| `parallels/B3_18-20.jpg` | PTR,LEG,2,1,100, image 3 | 12987720 | 100, 752, 1170, 846 |
| `parallels/B3_21.jpg` | PTR,LEG,2,1,100, image 3 | 12987720 | 100, 842, 1170, 896 |
| `parallels/B3_24-28.jpg` | PTR,LEG,2,1,100, image 3 | 12987720 | 100, 940, 1170, 1141 |
| `parallels/B3_34.jpg` | PTR,LEG,2,1,100, image 3 | 12987720 | 100, 1296, 1170, 1346 |
| `parallels/B4_12.jpg` | PTR,LEG,2,1,100, image 4 | 12987720 | 100, 528, 1128, 582 |
| `parallels/B4_25.jpg` | PTR,LEG,2,1,100, image 4 | 12987720 | 100, 974, 1128, 1028 |
| `parallels/B5_01.jpg` | PTR,LEG,2,1,100, image 5 | 12987720 | 100, 182, 1130, 234 |
| `parallels/B5_13.jpg` | PTR,LEG,2,1,100, image 5 | 12987720 | 100, 570, 1130, 622 |
| `parallels/C1_28-32.jpg` | PTR,LEG,2,1,101, image 1 | 12987723 | 100, 1196, 1170, 1394 |
| `parallels/C2_08-12.jpg` | PTR,LEG,2,1,101, image 2 | 12987723 | 100, 411, 1170, 608 |
| `parallels/D5_24.jpg` | PTR,LEG,2,1,76, image 5 | 12987566 | 100, 1034, 1095, 1084 |
| `parallels/D5_27-32.jpg` | PTR,LEG,2,1,76, image 5 | 12987566 | 100, 1116, 1095, 1328 |

## The test passages

These are the two passages on which the key was tested ([docs/METHOD.md](../docs/METHOD.md)), at the size of
the PARES image.

| file | record | PARES | box | shows |
|---|---|---|---|---|
| `tests/C1_test_passage.jpg` | PTR,LEG,2,1,101, image 1 | 12987723 | 170, 898, 1195, 1127 | the first test, the first six lines of the cipher paragraph of 7 December 1521 |
| `tests/no23_1520_passage.jpg` | PTR,LEG,2,1,23, image 3 | 12987157 | 170, 178, 1165, 392 | the second test, the paragraph added to the letter of 8 October 1520 |

The PARES address of each record is `https://pares.cultura.gob.es/ParesBusquedas20/catalogo/description/`
followed by the number in the third column.
