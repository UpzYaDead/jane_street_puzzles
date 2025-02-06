## January 2025
![Screenshot from 2025-01-31 19-55-36](https://github.com/user-attachments/assets/f80d0e95-3a3f-4ec4-ac94-83d66a60a726)

The basis is a standard backtracking sudoku solver. 
I am not particularly happy with the solution, as it is quite brute force.

The speedup that is necessary is to observe that after a row is completed, (we move left to right, up to down) we 
can calculate the gcd of the solution _up to that point_. By completing more row, the gcd can only decrease or 
stay the same. We keep track of the biggest gcd up to this point, and compare it with the gcd of a (not finished)
solution. If the gcd of a new solution _up to that point_ is smaller than our current highest, we backtrack.

It turned out that this was not fast enough. Then we guessed that that the solution is probably > 1000. This hack
ensured that almost all solutions drop out after two rows are filled in. 

Another small speedup is that for the gcd, we can swap rows without affecting the gcd. So we swap the first and the 
second row, so that we have less options to consider, as we were able to already fill in the "2" by following
regular sudoku rules.
