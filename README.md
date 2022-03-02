<img src="logo.png" alt="drawing" width="200"/>

## What it is?

Pairchoice is an open-source toolkit to analyze rating-based and pairwise comparison datasets for Python. Pairchoice is designed for users that need aggregating individual preferences.

We provided support to the most common aggregation methods used in social choice theory, computational social choice, and operations research.

## Basic background

Before we start, you will frequently find the following concepts: candidate and voter. A candidate is the unit that we want to measure (its score), and the voter is the one who voted for the candidate. In general, the goal is to aggregate voters' individual preferences to elect a candidate. There are multiple voting methods (either absolute or relative judgments). For instance, we can consider reviewing a place in Google Maps as a voting mechanism because a user (voter) rates a place (candidate) on a scale of 1-5 stars (value).

## What we provide?

- Aggregation methods (e.g. Borda count, Copeland)
- Random Utility Models (e.g. Elo)
- Methods to calculate divisive candidates (Divisiveness)
- Convert rating-based datasets to pairwise comparison

## Getting Started

### Via pip

```
pip install pairchoice
```

### From source code

To install pairchoice from source, you need to clone the repository of the project in your laptop.

```
git clone https://github.com/CenterForCollectiveLearning/pairchoice.git
```

Then, you just need to run:

```
python setup.py install
```

## Hands on Coding

Pairchoice requires a `pandas.DataFrame` to be initialized. To work with the library, the dataset must to include the column with the voter, the candidates compared and the candidate selected.

| voter | option_a | option_b | selected |
| ----- | -------- | -------- | -------- |
| 1     | A        | B        | A        |
| 1     | B        | C        | C        |
| 1     | A        | C        | C        |
| 2     | A        | C        | A        |
| 3     | B        | C        | B        |

```
import pandas as pd
from pairchoice import Pairwise

df = pd.read_csv("/path/to/file/pairwise.csv")

pwc = Pairwise(df)
```

### Rating-based to Pairwise comparison

Pairchoice allows converting a rating-based dataset into pairwise comparison data through method `to_pairwise()`.

Let's suppose that we have two candidates and two users. Voter 1 rates candidate A with 5 stars, and rates candidate B with 3 stars. In this case, we could assume that voter 1 will choose candidate A over candidate B.

Original data:
| voter | candidate | rating |
| --- | --- | --- |
| 1 | A | 5 |
| 1 | B | 3 |
| 2 | A | 4 |
| 2 | B | 5 |

Pairwise comparison data:
| voter | option_a | option_b | selected |
| --- | --- | --- | --- |
| 1 | A | B | A |
| 2 | A | B | B |

Here an example how would be the code:

```
pwc = Pairwise(df)

pwc.candidate = "candidate"
pwc.voter = "voter"
pwc.value = "rating"

pwc.to_pairwise()
```

## Classes

### Pairwise

Pairwise includes the features to analyze pairwise comparison data.

### Voting

## Do you have any questions?

We invite you to create an issue in the project's GitHub repository (https://github.com/CenterForCollectiveLearning/pairchoice/issues).

## References
