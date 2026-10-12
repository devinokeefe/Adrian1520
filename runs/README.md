# Records of the runs

This folder holds what the script printed. The table says which record belongs to which claim.

| Claim, and where it is made | Command | Record |
|---|---|---|
| Every check of the reading, the two tests, the second readings and the pages ([README](../README.md), Checking) | `python code/decode.py --check` | `check.txt` |
| The paragraph sign by sign, and the letters that the key gives beside the reading ([docs/TEXT.md](../docs/TEXT.md)) | `python code/decode.py` | `paragraph.txt` |
| The first test, token by token ([docs/METHOD.md](../docs/METHOD.md), The first test) | `python code/decode.py --test` | `test.txt` |
| The second test, word by word ([docs/METHOD.md](../docs/METHOD.md), The second test) | `python code/decode.py --1520` | `1520.txt` |
| The second transcription compared, the proposals and the points on the parallels ([docs/METHOD.md](../docs/METHOD.md), Second readings) | `python code/decode.py --second` | `second.txt` |
| The word-by-word table of [docs/TEXT.md](../docs/TEXT.md) | `python code/decode.py --table` | `table.txt` |
| The vocabulary by the first letter of the group ([docs/METHOD.md](../docs/METHOD.md), The cipher) | `python code/decode.py --blocks` | `blocks.txt` |
| [tests/TESTS.md](../tests/TESTS.md), the mutation test | `python tests/mutation_test.py` | `mutation_test.txt` |

The counts quoted in the pages are in `data/figures.txt`, which is what `python code/decode.py --figures`
prints, and the check compares the two.

Each record holds what the script printed on standard output, with LF line ends. The workflow in `.github/`
runs every command in the table, under Linux and under Windows, and compares what it prints with these
records.
