# Symbolic math

A reimplementation of Lample & Charton (2019) Deep Learning for Symbolic Mathematics
- [arxiv](https://arxiv.org/abs/1912.01412)
- [pdf](https://arxiv.org/pdf/1912.01412)
- [Open Review](https://openreview.net/forum?id=S1eZYeHFDS)

## Workflow

1. generate random math expressions in binary tree form
2. map tree to prefix -> input sequence
3. map tree to inifx to mathematica to prefix -> output sequence
4. seq-to-seq

## TODO

- test suite for the binary tree generation
- generate a dataset of random equations
- solve equations in mathematica to generate the target
- aws 
- train seq-to-seq
