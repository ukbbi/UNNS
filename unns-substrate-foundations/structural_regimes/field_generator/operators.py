import numpy as np

def apply_alpha(ladder, alpha):
    """Scale deformation"""
    return np.array(ladder) * alpha


def apply_mu(ladder, mu):
    """Gap deformation"""
    ladder = np.array(ladder)
    gaps = np.diff(ladder)

    # μ acts on gaps
    gaps_mu = gaps * mu

    # reconstruct ladder
    new_ladder = [ladder[0]]
    for g in gaps_mu:
        new_ladder.append(new_ladder[-1] + g)

    return np.array(new_ladder)