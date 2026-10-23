"""Non-quantum kernels used to falsify uniqueness. These are not UNNS predictions."""
import math


def local_shared_route(a:float,b:float)->float:
    """Local common-cause angular overlap. C=-1+2|principal angle|/pi."""
    d=math.atan2(math.sin(a-b),math.cos(a-b))
    return -1.0+2.0*abs(d)/math.pi


def saturated_joint_route(a:float,b:float, sharpness:float=6.0)->float:
    """Smooth operationally no-signalling but CHSH-superquantum joint kernel.
    Kernel choice is an independent axiom, not a result of UNNS recursion.
    """
    if not 0<sharpness<100:
        raise ValueError('sharpness must be in (0,100)')
    return -math.tanh(sharpness*math.cos(a-b))/math.tanh(sharpness)
