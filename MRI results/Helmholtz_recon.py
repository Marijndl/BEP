import numpy as np
from scipy.signal import convolve2d, convolve
from scipy.ndimage import gaussian_filter

def Helmholtz(M, voxs=1e-3, ks = 3, eps_out = False):
    '''Calculates the conductivity using a finite difference kernel
    Parameters:
        M (Array):      Complex input array to calculate conductivity of
        voxs (float):   voxel size in m
        ks (int):       kernel size, now implemented: 3
        eps_out(bool):  export permittivity or not

    Returns:
        sigma (Array):  Array with the calculated conductivty
        eps (Array):    Array with the calculated permittivity
    '''
    mu0 = np.pi*4e-7
    omega = 2*np.pi*128e6
    eps0 = 8.85e-12

    dim = len(M.shape)
    if dim == 2:
        LM = lap2D(M,ks)
    elif dim == 3:
        LM = lap3D(M,ks)
    else:
        assert 'Matrix dimensions are not 2D or 3D'
    sigma = np.imag(LM/M)/(mu0*omega*voxs**2)
    eps = np.real(LM/M)/(mu0*omega**2*eps0*voxs**2)
    if eps_out:
        return sigma, eps
    else:
        return sigma


def Helmholtz_ph(M, voxs=1e-3, ks = 3):
    '''Calculates the conductivity with the phase based Helmholtz recon
    and usnig a finite difference kernel 
    Parameters:
        M (Array):      phase to calculate conductivity from 
        voxs (float):   voxel size in m
        ks (int):       kernel size, now implemented: 3, 773

    Returns:
        sigma (Array): Array with the calculated conductivty
    '''
    mu0 = np.pi*4e-7
    omega = 2*np.pi*128e6

    dim = len(M.shape)
    if dim == 2:
        sigma = lap2D(M, ks)/(mu0*omega*voxs**2)
    elif dim == 3:
        sigma = lap3D(M, ks)/(mu0*omega*voxs**2)
    else:
        assert 'Matrix dimensions are not 2D or 3D'
    return sigma


def lap2D(M, ks):
    '''Calculates the laplacian of a 2D field using finite differencing

    Parameters:
        M (Array): 2D matrix of which to calculate the laplacian with format
                    Nx x Ny

    Returns:
        LM (Array): 2D torch tensor with Laplacian values
    '''
    if len(M.shape) != 2:
        assert 'Matrix does not have 2 dimensions, make sure input is Nx x Ny'
    if ks == 3:
        Lk = (np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])) # 3pt laplacian kernel in 2D
    elif ks == 7:
        Lk = gen_7pt_K_2d()
    else:
        assert 'kernel size not implemented'
        
    return convolve2d(M, Lk, mode='same')


def lap3D(M, ks):
    '''Calculates the laplacian of a 2D field using finite differencing

    Parameters:
        M (Array): 3D matrix of which to calculate the laplacian with format
                    Nx x Ny x Nz

    Returns:
        LM (Array): 3D numpy array with Laplacian values
    '''
    if len(M.shape) != 3:
        assert 'Matrix does not have 2 dimensions, make sure input is Nx x Ny'
    if ks == 3:
        Lk = (np.array([[[0, 0, 0], [0, 1, 0], [0, 0, 0]], 
                        [[0, 1, 0], [1, -6, 1], [0, 1, 0]], 
                        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]])) # 3pt laplacian kernel in 3D
    elif ks == 7:
        Lk = gen_7pt_K_3d()

    else:
        assert 'kernel size not implemented'

    return convolve(M, Lk, mode='same')


def smooth_HH(M, fac=5, type = 'Gaussian'):
    '''Smoothes the results of the noisy helmholtz reconstruction

    Parameters:
        M (Array):      3D array with reconstructed values
        fac (int):      factor for the smoothing. For 'Gaussian' fac = sigma
                        for 'Mean' fac = kernelsize in all dimensions
        type (string):  type of smoothing, either "Gaussian": gaussian smoothing kernel
                        or "Mean": mean smoothing kernel

    Returns:
                        filtered array
    '''
    if type == 'Gaussian':
        return gaussian_filter(M, fac)
    elif type == 'Mean':
        dim = len(M.shape)
        if dim == 2:
            Lk = np.ones([fac,fac])/(fac**2)
            return convolve2d(M, Lk, mode='same')
        elif dim == 3:
            Lk = np.ones([fac,fac,fac])/(fac**3)
            return convolve(M, Lk, mode='same')
        else:
            assert 'Matrix dimensions are not 2D or 3D'
    else:
        assert 'Only "Gaussian" and "Mean" are implemented'

# From here define kernel functions, be careful, normalization is not yet correct. 
def gen_7pt_K_3d():
    ''' Generates 7 pt finite difference kernel for the laplacian in 3D.
    '''
    Lk = np.zeros([7,7,7])
    Kx = (np.array([[[0.25, 0.5, 0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]],
                [[0.5, 1, 0.5], [1, 2, 1], [0.5, 1, 0.5]],
                [[-0.25, -0.5, -0.25], [-0.5, -1, -0.5], [-0.25, -0.5, -0.25]],
                [[-1, -2, -1], [-2, -4, -2], [-1, -2, -1]],
                [[-0.25, -0.5, -0.25], [-0.5, -1, -0.5], [-0.25, -0.5, -0.25]],
                [[0.5, 1, 0.5], [1, 2, 1], [0.5, 1, 0.5]],
                [[0.25, 0.5, 0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]]]))
    
    Ky = (np.array([[[0.25, 0.5, 0.25], [0.5, 1, 0.5], [-0.25, -0.5, -0.25], [-1, -2, -1], [-0.25, -0.5, -0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]],
                [[0.5, 1, 0.5], [1, 2, 1], [-0.5, -1, -0.5], [-2, -4, -2], [-0.5, -1, -0.5], [1, 2, 1], [0.5, 1, 0.5]],
                [[0.25, 0.5, 0.25], [0.5, 1, 0.5], [-0.25, -0.5, -0.25], [-1, -2, -1], [-0.25, -0.5, -0.25], [0.5, 1, 0.5], [0.25, 0.5, 0.25]]]))
    
    Kz = (np.array([[[0.25, 0.5, -0.25, -1, -0.25, 0.5, 0.25], [0.5, 1, -0.5, -2, -0.5, 1, 0.5], [0.25, 0.5, -0.25, -1, -0.25, 0.5, 0.25]],
                [[0.5, 1, -0.5, -2, -0.5, 1, 0.5], [1, 2, -1, -4, -1, 2, 1], [0.5, 1, -0.5, -2, -0.5, 1, 0.5]],
                [[0.25, 0.5, -0.25, -1, -0.25, 0.5, 0.25], [0.5, 1, -0.5, -2, -0.5, 1, 0.5], [0.25, 0.5, -0.25, -1, -0.25, 0.5, 0.25]]]))

    Lk[:,2:5,2:5] = Kx
    Lk[2:5,:,2:5] = Lk[2:5,:,2:5] + Ky
    Lk[2:5,2:5,:] = Lk[2:5,2:5,:] + Kz
    return Lk/64

def gen_7pt_K_2d():
    ''' Generates 7 pt finite difference kernel for the laplacian in 2D.
    !!!Normalization is not yet exact!!!
    '''
    Lk = n
    Lk = np.zeros([7,7])
    Kx = (np.array([[0.25, 0.5, 0.25],
                [0.5, 1, 0.5],
                [-0.25, -0.5, -0.25],
                [-1, -2, -1],
                [-0.25, -0.5, -0.25],
                [0.5, 1, 0.5],
                [0.25, 0.5, 0.25]]))
    
    Ky = (np.array([[0.5, 1, -0.5, -2, -0.5, 1, 0.5], [1, 2, -1, -4, -1, 2, 1], [0.5, 1, -0.5, -2, -0.5, 1, 0.5]]))

    Lk[:,2:5] = Kx
    Lk[2:5,:] = Lk[2:5,:] + Ky
    return Lk/64*3