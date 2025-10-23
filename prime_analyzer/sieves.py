# prime_analyzer/sieves.py

"""
Contains implementations of different prime-finding
sieve algorithms.

Each function takes an integer 'n' and returns a list
of all prime numbers less than or equal to 'n'.
"""

def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Finds all primes up to n using the Sieve of Eratosthenes.
    """
    prime = [True for i in range(n + 1)] 
    p = 2
    while p * p <= n: 
        if prime[p] == True: 
            # Update all multiples of p
            for i in range(p * p, n + 1, p): 
                prime[i] = False
        p += 1
        
    prime[0]= False
    prime[1]= False
    
    prime_list = []
    for p in range(n + 1): 
        if prime[p]:
            prime_list.append(p)
            
    return prime_list

def sieve_of_atkin(n: int) -> list[int]:
    """
    Finds all primes up to n using the Sieve of Atkin.
    This is theoretically more efficient than Eratosthenes.
    """
    # Sieve array
    sieve = [False] * (n + 1)
    
    # Pre-compute squares
    x_limit = int(n**0.5)
    
    # 1. First quadratic form
    for x in range(1, x_limit + 1):
        for y in range(1, x_limit + 1):
            num = (4 * x**2) + (y**2)
            if num <= n and (num % 12 == 1 or num % 12 == 5):
                sieve[num] = not sieve[num] # Flip
                
    # 2. Second quadratic form
    for x in range(1, x_limit + 1):
        for y in range(1, x_limit + 1):
            num = (3 * x**2) + (y**2)
            if num <= n and (num % 12 == 7):
                sieve[num] = not sieve[num] # Flip

    # 3. Third quadratic form
    for x in range(1, x_limit + 1):
        for y in range(1, x_limit + 1):
            num = (3 * x**2) - (y**2)
            if x > y and num <= n and (num % 12 == 11):
                sieve[num] = not sieve[num] # Flip

    # 4. Eliminate multiples of prime squares
    for r in range(5, x_limit + 1):
        if sieve[r]:
            for i in range(r**2, n + 1, r**2):
                sieve[i] = False
                
    # 5. Collect primes
    prime_list = [2, 3] # Add base primes
    for p in range(5, n + 1):
        if sieve[p]:
            prime_list.append(p)
            
    return prime_list

# Map to access algorithms by name
ALGORITHM_MAP = {
    "Sieve of Eratosthenes": sieve_of_eratosthenes,
    "Sieve of Atkin": sieve_of_atkin,
}
