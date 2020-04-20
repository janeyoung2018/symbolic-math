# (Symbolic Math) Reimplementation of [Deep Learning for Symbolic Mathematics](https://arxiv.org/abs/1912.01412)

A reimplementation of Lample & Charton (2019) Deep Learning for Symbolic Mathematics
- [arxiv](https://arxiv.org/abs/1912.01412)
- [pdf](https://arxiv.org/pdf/1912.01412)
- [Open Review](https://openreview.net/forum?id=S1eZYeHFDS)

## Codebase guide

1. generate random math expressions in binary tree form (`random_trees.py`)
2. map tree to prefix (`random_trees.py`)
3. prefix to infix (`infix_prefix.py`)
4. infix to prefix (`infix_prefix.py`)

## Workflow

1. `backward_generation.ipynb` - generate trees, generate target using `sympy`, simplify, make sequence (input & target)

Can also run
```bash
$ python generate_dataset.py --cpu 12 --num 10000 --n 8
```

2. `seq2seq_model.ipynb` basic model

3. `transformer.ipynb` trains model in google cloud.


