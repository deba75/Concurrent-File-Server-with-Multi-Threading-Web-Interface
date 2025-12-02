#!/usr/bin/env python3
"""
Sample Python Script
This file demonstrates that the server can transfer any type of file.
"""

def fibonacci(n):
    """Generate Fibonacci sequence up to n terms"""
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

def factorial(n):
    """Calculate factorial of n"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def main():
    print("Sample Python Script")
    print("=" * 50)
    
    # Fibonacci sequence
    print("\nFibonacci sequence (10 terms):")
    print(fibonacci(10))
    
    # Factorial
    print("\nFactorial of 5:")
    print(factorial(5))
    
    # Prime numbers
    print("\nPrime numbers up to 20:")
    primes = [n for n in range(2, 21) if is_prime(n)]
    print(primes)

if __name__ == "__main__":
    main()
