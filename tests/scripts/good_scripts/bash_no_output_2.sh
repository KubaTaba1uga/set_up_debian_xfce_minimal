#!/bin/bash
# Program for Fibonacci
# Series

# Static input fo N
N=600

# First Number of the
# Fibonacci Series
a=0

# Second Number of the
# Fibonacci Series
b=1

for (( i=0; i<N; i++ ))
do
	fn=$((a + b))
	a=$b
	b=$fn
done


