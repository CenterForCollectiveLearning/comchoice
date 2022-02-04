# PairChoice

## What it is?

PairChoice is an open-source toolkit to analyze pairwise comparison data for Python. 

## What we provide?

- Voting methods (e.g. Borda, Copeland)
- Random Utility Models (e.g. Elo)
- Divisiveness
- Basic data cleaning procedures

## Getting Started

To install pairchoice from source, you need to clone the repository of the project in your laptop.
```
git clone https://github.com/CenterForCollectiveLearning/pairchoice.git
```

Then, you just need to run:

```
python setup.py install
```

## Hello World

Pairchoice needs a `pandas.DataFrame` variable.

| user_id | option_a | option_b | selected |
| --- | --- | --- | --- |
| 1 | A | B | A |
| 1 | B | C | C |
| 1 | A | C | C |
| 2 | A | C | A |
| 3 | B | C | B |

## Do you have any questions?
We invite you to create an issue in the project's GitHub repository (https://github.com/CenterForCollectiveLearning/pairchoice/issues).


