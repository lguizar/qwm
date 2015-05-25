"""
Simulation in regards to Numberphile episode "How to win a guessing game"
https://www.youtube.com/watch?v=ud_frfkt1t0

Situation:
1. 2 random numbers are generated (A and B)
2. 1 is randomly chosen (call it A)
3. A random number (K) is generated by some sort of distribution
4. A decision is made by the following rule: If K > A, then guess that B > A.
If K < A, then guess that 

See blog post: LINK HERE DERRR


"""

# Import libraries
from __future__ import division
from scipy.stats import binom
import numpy as np
import matplotlib.pyplot as plt

# Initialize random seed
np.random.seed(0)

####################### EXPERIMENT 1
# Experiment 1 setup
nTrials = 100
int_min = 10
int_max = 50

# Derive metaparameters
Ks = range(int_min,int_max+1)
int_range = int_max - int_min + 1

# Generate random numbers A and B and K
A = np.random.randint(int_min,int_max+1,nTrials)
B = np.random.randint(int_min,int_max+1,nTrials)
K = np.random.randint(int_min,int_max+1,nTrials)

# Generate a new random number for B and K if it is the same as A
for t in range(nTrials):
    while B[t] == A[t]:
        B[t] = np.random.randint(int_min,int_max+1)
    while K[t] == A[t]:
        K[t] = np.random.randint(int_min,int_max+1)
        
# Perform guessing game
trialsWon = 0
trialRes = np.zeros((nTrials,1))
for t in range(nTrials):
    trialRes[t] = np.logical_xor(A[t]>K[t],A[t]<B[t])
    trialsWon += trialRes[t]
fracWon = trialsWon / nTrials
# Statistics: binomial distribution
pval = binom.cdf(trialsWon,nTrials,0.5)[0]
print('p=',1 - pval)

# Repeat the experiment just choosing the same number every time 
# if flipped over card equals that number, then count it as being lower
trialsWon_k = np.zeros((int_range,1))
for k in range(int_range):
    for t in range(nTrials):
        res = np.logical_xor(A[t]>Ks[k],A[t]<B[t])
        trialsWon_k[k] += res
fracWon_k = trialsWon_k / nTrials

# Plot the results
plt.figure()
plt.plot(Ks, fracWon_k, 'k.',label='constant K')
plt.plot([int_min,int_max],[fracWon,fracWon],'k--', label='randomly generated K')
plt.xlim((9,51))
plt.ylim((0.4,0.8))
plt.xlabel('Choice of K')
plt.ylabel('Fraction of winning trials')
plt.legend(loc='best')

########### EXPERIMENT 2
# does Player 2 perform better if it has knowledge of the distribution and 
# generates K from randomly sampling from this distribution or if it 
# has no knowledge of the distribution but rather generates K by estimating the median over time

# Self-generated 100 random numbers
randHuman = [7, 66, 5.5, 444, 10, -1000, 0, 0.1, 0.2, 33, -33, -5, -12, 6,
             1.2, 333, 42, -44, 5.213, 44.44, 30.3, 829.3, 1, 1.44, 99, -9,
             0.001, 3.4, -2.5, 9.3, -33, -6, -0.9, 111, -473, 2, 93, 85,
             67.32, 7, -5, -1.8, 9.343, 15.2, 5.4, -3.777, 99.2, 100, 0.39,
             65, 22, -49, 38, 1.33,4.01,17,55,0.3,-283,-893,-777,910,762,482,
             109,192,75,988,762,983,492,-291,-432,-753,77,-37,8.3,0.36,-94,
             6,28,-46,-389,-0.3,48,222,8.38,-95,-63,-154,83,94.6,193.5,882,
             -3,-82,9.4,33,555,82]
             
# Expand self-generated 100 random numbers
randHuman = np.hstack((randHuman,[x * 1.5 for x in randHuman]))
randHuman = np.hstack((randHuman,[x / 2 for x in randHuman]))
randHuman = np.hstack((randHuman,[x * 2.5 for x in randHuman]))
randHuman = np.hstack((randHuman,[x / 3 for x in randHuman]))
randHuman = np.hstack((randHuman,[x * 3.5 for x in randHuman]))
randHuman = np.hstack((randHuman,[x / 4 for x in randHuman]))
randHuman = np.hstack((randHuman,[x / 5 for x in randHuman]))
nHuman = len(randHuman)

# Generate A and B
nTrials = np.int(np.floor(nHuman / 2))
A = np.random.permutation(randHuman)
B = A[nTrials:]
A = A[:nTrials]

# Generate K's for both strategies
K_dist_idx = np.random.randint(0,nHuman,nTrials)
K_dist = np.zeros((nTrials,1))
K_median = np.zeros((nTrials,1))
for t in range(nTrials):
    
    if t == 0:
        K_median[t] = 0
    else:
        cum_numbers = np.hstack((A[:t].tolist(),B[:t].tolist()))
        K_median[t] = np.median(cum_numbers)
        
    K_dist[t] = randHuman[K_dist_idx[t]]


# Perform random guessing
trialsWon_dist = 0
trialsWon_median = 0
for t in range(nTrials):
    res = np.logical_xor(A[t]>K_dist[t],A[t]<B[t])[0]
    trialsWon_dist += res
    res = np.logical_xor(A[t]>K_median[t],A[t]<B[t])[0]
    trialsWon_median += res
fracWon_dist = trialsWon_dist / nTrials
fracWon_median = trialsWon_median / nTrials
print fracWon_dist
print fracWon_median