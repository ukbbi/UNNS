#!/usr/bin/env python3
"""Spectral RK4 solver for transverse 1D Maxwell with a prescribed dielectric pump.
No UNNS input is used in Maxwell propagation.
"""
from __future__ import annotations
import argparse, json, math
import numpy as np


def envelope(t: float, begin: float, end: float) -> float:
    if t <= begin or t >= end: return 0.0
    u=(t-begin)/(end-begin)
    return math.sin(math.pi*u)**2


def simulate(q_first: int = 6, q_second: int = 28, start: int = 2,
             eta:float=.012, cells:int=256, dt:float=.002, t_stage:float=2.0,
             first_on:bool=True,second_on:bool=True) -> dict:
    if eta < 0 or eta >= .20: raise ValueError('eta outside conservative positive-dielectric range')
    if cells < 4*(max(q_first,q_second)+abs(start)): raise ValueError('increase spectral grid')
    if start<=0 or q_first<=0 or q_second<=0: raise ValueError('positive spatial indices required')
    steps=int(round(2*t_stage/dt)); dt=2*t_stage/steps
    z=(2*math.pi/cells)*np.arange(cells)
    k=np.fft.fftfreq(cells,d=1/cells) # integer Fourier indices
    d=np.zeros(cells,dtype=np.complex128); b=np.zeros_like(d)
    d[start]=b[start]=1.0
    def modes(t):
        return ((q_first,envelope(t,0.,t_stage) if first_on else 0.),
                (q_second,envelope(t,t_stage,2*t_stage) if second_on else 0.))
    def rhs(t,dd,bb):
        eps=np.ones(cells,dtype=np.float64)
        for q,f in modes(t):
            if f: eps += 2*eta*f*np.cos(q*(z-t))
        e=np.fft.fft(np.fft.ifft(dd*cells)/eps)/cells
        return -1j*k*bb, -1j*k*e
    def spectrum(dd,bb):
        right=(dd+bb)/2
        idx=(start, start+q_first, start+q_second, start+q_first+q_second,9,36,38)
        return {str(m): {'amplitude': float(abs(right[m])),
                         'power':float(abs(right[m])**2),
                         'total_coefficient':float(abs(dd[m]))} for m in idx if 0<=m<cells//2}
    snapshot_initial=spectrum(d,b)
    snap_mid=None
    min_eps=1-4*eta
    for j in range(steps):
        t=dt*j
        a1,c1=rhs(t,d,b)
        a2,c2=rhs(t+dt/2,d+dt*a1/2,b+dt*c1/2)
        a3,c3=rhs(t+dt/2,d+dt*a2/2,b+dt*c2/2)
        a4,c4=rhs(t+dt,d+dt*a3,b+dt*c3)
        d += dt*(a1+2*a2+2*a3+a4)/6
        b += dt*(c1+2*c2+2*c3+c4)/6
        if j==steps//2-1: snap_mid=spectrum(d,b)
    result={
      'model':'1D transverse Maxwell, d_t D=-d_z B, d_t B=-d_z E, D=epsilon(z,t) E; periodic 2pi torus',
      'pump':{'first_q':q_first,'second_q':q_second,'eta':eta,'stage_duration':t_stage,
              'first_on':first_on,'second_on':second_on,
              'profile':'epsilon=1+2eta[f1(t)cos(q1(z-t))+f2(t)cos(q2(z-t))]',
              'positive_epsilon_lower_bound':min_eps},
      'initial':{'carrier':start,'D_m':1,'B_m':1,'all_other_modes':0},
      'scheme':{'method':'Fourier pseudospectral periodic + time RK4','cells':cells,'dt':dt,'steps':steps},
      'outgoing':{'after_stage_1':snap_mid, 'after_stage_2':spectrum(d,b)},
      'final_total_absmax_odd':float(np.max(np.abs(d[1::2]))),
      'final_total_absmax_odd_B':float(np.max(np.abs(b[1::2]))),
      'final_l2_norm_D':float(np.linalg.norm(d)),
      'final_l2_norm_B':float(np.linalg.norm(b)),
      'initial_spectrum':snapshot_initial
    }
    return result

if __name__=='__main__':
    pa=argparse.ArgumentParser(); pa.add_argument('--first',type=int,default=6);pa.add_argument('--second',type=int,default=28);pa.add_argument('--start',type=int,default=2);pa.add_argument('--eta',type=float,default=.012);pa.add_argument('--cells',type=int,default=256);pa.add_argument('--dt',type=float,default=.002);pa.add_argument('--stage',type=float,default=2.0)
    args=pa.parse_args(); print(json.dumps(simulate(args.first,args.second,args.start,args.eta,args.cells,args.dt,args.stage),indent=2,sort_keys=True))
