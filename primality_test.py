"""
Contains basic mathematical functions which allow to test for the compositeness of large numbers.
Includes the Euclidean Algorithm, the Extended Euclidean Algorithm, Fast Modular Exponentiation,
and the Miller-Rabin Primality test.

From Prof. Mackall
"""

import random

def FastModularExp(b,r,m):
    """Computes b^r mod m by successive squaring"""

    binary_r=bin(r)

    n=1
    k=b % m

    for i in range(len(binary_r)-2):
        if binary_r[-i-1] == '1':
            n=((n*k) % m)
        k=(k**2) % m
    return n


def EuclideanAlgorithm(a,b):
    """Finds the gcd of a,b"""

    #Setup so that the gcd is calculated for all integers a,b entered in any order
    a=abs(a)
    b=abs(b)

    x=max(a,b)
    y=min(a,b)

    if y==0:
        return x

    else:
        #Euclidean algorithm
        r=-1
        while r !=0:
            r= x % y
            x=y
            y=r
    
    return x

def ExtEuclideanAlgorithm(a,b):
    """Finds the gcd of a,b and produces integers s,t so that as+bt=gcd(a,b).
    Returns a dictionary of the form {a:s, b:t}."""

    #Setup so that the gcd is calculated for all integers a,b entered in any order
    x=abs(a)
    y=abs(b)

    #Eliminating cases where the Euclidean algorithm isn't used
    if x==y:
        if a>0:
            d={a:1, b:0}
            return d
        else:
            d={a:-1, b:0}
            return d

    if x>y:
        k=1 #Keeps track that x and y have not swapped
        if y==0:
            d={a:abs(a)//a, b:0}
            return d

    if y>x:
        if x==0:
            d={a:0, b:abs(b)//b}
            return d
        else:
            k=-1 #Keeps track that x and y have swapped
            x=abs(b)
            y=abs(a)

    #Extended Euclidean algorithm
    r=-1
    (c,d)=(-1,-1)
    (s,t)=(1,0)
    (u,v)=(0,1)
    while r !=0:
        q= x//y
        r= x % y
        
        (c,d)=(s,t)
        (s,t)=(u,v)
        (u,v)=(c-q*s,d-q*t)

        x=y
        y=r

    if k==-1:
        if a//abs(a) != 1:
            t=-t
        if b//abs(b) != 1:
            s=-s
        d={a:t, b:s}
    else:
        if a//abs(a) != 1:
            s=-s
        if b//abs(b) != 1:
            t=-t
        d={a:s, b:t}

    return d

def MillerRabin(q, a=None):
    """Tests if q is composite using Miller-Rabin primality test with random base
    a if a isn't specified. If the test fails, declares that q is probably prime."""

    #Eliminating even q    
    if q % 2 == 0:
        return (False, q) #q is even
    
    #Select base for test, if none given as input
    if a == None:
        a=random.randrange(2,q)

    #Count powers of two dividing q-1, tracked using k
    k=0
    r=-1
    m=q-1
    while r != 1:
        r = m % 2
        if r == 0:
            m=m//2
            k+=1

    s=FastModularExp(a,m,q)
    
    if (s == 1 or s == q-1):
        return (True, q) #q is probably prime
    else:
        for i in range(k-1):
            t=s**2 % q
            if t == 1:
                return (False, EuclideanAlgorithm(s-1,q)) #q is composite, returns a divisor of q
            elif t == q-1: #q is probably prime
                return (True, q)
            s=t
    return (False, q) #q is composite, but no divisor found


def SmallPrime(k=10):
    """Randomly generates a number with ~154 digits that is likely to be prime.
    Input is an integer k determining security; larger k values increases likelihood to be prime."""

    p=random.randrange((10**148)-1,(10**154)+1,2)
    prime = False
    while not prime:
        p+=2
        (prime, div)=MillerRabin(p)
        for i in range(k):
            (prime, div)=MillerRabin(p)
            if not prime:
                break
    
    if EuclideanAlgorithm(557940830126698960967415390,p)!=1: #Calculates gcd of p and product of first 20 primes
        p=SmallPrime(k)

    return p


def BigPrime(k=10):
    """Randomly generates a number with ~164 digits that is likely to be prime.
        Input is an integer k determining security; larger k values increases likelihood to be prime."""
    
    p=random.randrange((10**158)-1,(10**164)+1,2)
    prime = False
    while not prime:
        p+=2
        (prime, div)=MillerRabin(p)
        for i in range(k):
            (prime, div)=MillerRabin(p)
            if not prime:
                break
    
    if EuclideanAlgorithm(557940830126698960967415390,p)!=1: #Calculates gcd of p and product of first 20 primes
        p=BigPrime(k)

    return p