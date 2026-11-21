"""Fixed-seed descriptive controls, with no significance claims."""
import random

def controls(values, seed, replicates=8):
    r = random.Random(seed)
    for rep in range(replicates):
        yield 'nearby',rep,[max(1,x+r.choice([j for j in range(-16,17) if j])) for x in values]
        matched = [r.randrange(2**(x.bit_length()-1),2**x.bit_length()) for x in values]
        yield 'bitlength_random',rep,matched
        yield 'monotone_random',rep,sorted(matched)
        shuffled = values[:]; r.shuffle(shuffled)
        yield 'order_scramble',rep,shuffled
    yield 'cyclic_shift',0,values[1:]+values[:1]

def alternative(x):
    # Explicit alternatives: y=2s and y=3s, all positive integral sources.
    return {'doubling_incoming':int(x%2==0),'tripling_incoming':int(x%3==0)}
