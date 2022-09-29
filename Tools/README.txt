
The .ipynb file enclosed contains several tools used to test the "randomness" of os.urandom() and Qiskit.  Heavily based off of the article at https://medium.com/unitychain/provable-randomness-how-to-test-rngs-55ac6726c5a3 , my project group and I put together these tests in an attempt to determine which number generator was "more random".


The list of tools we made includes
1. Random walk 1D
2. Random walk 2D
3. Longest run of 1's
4. Ratio of 1's to 0's
5. Scatter Plots
6. Pattern Repetition

These tests were conducted in several trials of 100, 500, 1000, and 10,000 data points.

Our findings led us to believe that Qiskit was a little more random due to having seemingly more random results, but os.urandom() was much faster and easier to work wtih.
