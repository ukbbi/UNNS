import numpy as np

from jhtdb_adapter.physics import physical_fields, block_average_velocity


def test_block_average_constant():
    v = np.zeros((8,8,8,3), dtype=np.float32)
    v[...,0] = 2.0
    v[...,1] = -1.0
    out = block_average_velocity(v, 2)
    assert out.shape == (4,4,4,3)
    assert np.allclose(out[...,0], 2.0)
    assert np.allclose(out[...,1], -1.0)


def test_solid_body_rotation_exact_interior():
    # u=-Omega*y, v=Omega*x, w=0
    n = 16
    h = 0.1
    om = 2.5
    z,y,x = np.meshgrid(
        np.arange(n)*h, np.arange(n)*h, np.arange(n)*h,
        indexing="ij"
    )
    v = np.zeros((n,n,n,3), dtype=np.float32)
    v[...,0] = -om*y
    v[...,1] = om*x

    f = physical_fields(v, h, viscosity=0.000185)
    sl = (slice(2,-2),slice(2,-2),slice(2,-2))
    assert np.allclose(f["divergence"][sl], 0, atol=2e-5)
    assert np.allclose(f["Q"][sl], om**2, rtol=2e-5, atol=2e-5)
    assert np.allclose(f["enstrophy"][sl], 2*om**2, rtol=2e-5, atol=2e-5)
    assert np.allclose(f["strain_sq"][sl], 0, atol=5e-5)
