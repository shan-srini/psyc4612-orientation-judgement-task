# PSYC4612 - Selective Visual Array: Orientation Judgement Task

**A script to create visual array orientation judgement stimuli for a PSYC4612 (Labaratory in Cognition) experiment**
_inspired by https://englelab.gatech.edu/attentioncontroltasks_

## Run

```
# make sure you have python3 installed and can create virtualenvs using venv
./run.sh
```

## TODO

- [ ] Stimuli may have overlapping line locations
  - idea: naive approach is probably keeping a set of all pixels occupied by lines then continuously regenerating until getting all points that aren't contained in the set
  - idea: better approach is a grid layout and marking certain grid points as taken or not using set
- [ ] Need to output an image with text that defines target color before each stimuli
- [x] VALID_LINE_BOUNDS doesn't actually work because you need to pick the random points at random range of (BUFFER, IMAGE_SIZE - BUFFER) ... quick fix
