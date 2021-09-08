def pretty_matrix(m):
  print("[", end="")
  for i, row in enumerate(m):
    print(", ".join(map(str, row)), end="\n " if i != len(m) - 1 else "")
  print("]")

m = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
]

pretty_matrix(m)
