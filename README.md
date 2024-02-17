# life

Various implementations of Conway's Game Of Life

## Random data structure idea

You might author a 3x3 world like this:

```
  o
 o 
o  
```

If we remove the newlines we can represent it as a string like this:

```
  o o o  
```

If we convert to 0s and 1s we get this:

```
001010100
```

And then there's probably a bunch of interesting properties that arise from
that!
