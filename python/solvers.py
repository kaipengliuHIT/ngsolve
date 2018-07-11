from ngsolve.la import InnerProduct
from math import sqrt
from ngsolve import Projector, Norm

def CG(mat, rhs, pre=None, sol=None, tol=1e-12, maxsteps = 100, printrates = True, initialize = True, conjugate=False):
    """preconditioned conjugate gradient method


    Parameters
    ----------

    mat : Matrix
      The left hand side of the equation to solve. The matrix has to be spd or hermitsch.

    rhs : Vector
      The right hand side of the equation.

    pre : Preconditioner
      If provided the preconditioner is used.

    sol : Vector
      Start vector for CG method, if initialize is set False. Gets overwritten by the solution vector. If sol = None then a new vector is created.

    tol : double
      Tolerance of the residuum. CG stops if tolerance is reached.

    maxsteps : int
      Number of maximal steps for CG. If the maximal number is reached before the tolerance is reached CG stops.

    printrates : bool
      If set to True then the error of the iterations is displayed.

    initialize : bool
      If set to True then the initial guess for the CG method is set to zero. Otherwise the values of the vector sol, if provided, is used.

    conjugate : bool
      If set to True, then the complex inner product is used.


    Returns
    -------
    (vector)
      Solution vector of the CG method.

    """

    u = sol if sol else rhs.CreateVector()
    d = rhs.CreateVector()
    w = rhs.CreateVector()
    s = rhs.CreateVector()

    if initialize: u[:] = 0.0
    d.data = rhs - mat * u
    w.data = pre * d if pre else d
    err0 = sqrt(abs(InnerProduct(d,w)))
    s.data = w
    # wdn = InnerProduct (w,d)
    wdn = w.InnerProduct(d, conjugate=conjugate)

    if wdn==0:
        return u
    
    for it in range(maxsteps):
        w.data = mat * s
        wd = wdn
        # as_s = InnerProduct (s, w)
        as_s = s.InnerProduct(w, conjugate=conjugate)        
        alpha = wd / as_s
        u.data += alpha * s
        d.data += (-alpha) * w

        w.data = pre*d if pre else d
        
        # wdn = InnerProduct (w, d)
        wdn = w.InnerProduct(d, conjugate=conjugate)
        beta = wdn / wd

        s *= beta
        s.data += w

        err = sqrt(abs(wd))
        if err < tol*err0: break
            
        if printrates:
            print ("it = ", it, " err = ", err)

    return u




def QMR(mat, rhs, fdofs, pre1=None, pre2=None, sol=None, maxsteps = 100, printrates = True, initialize = True, ep = 1.0, tol = 1e-7):
    """Quasi Minimal Residuum method


    Parameters
    ----------

    mat : Matrix
      The left hand side of the equation to solve

    rhs : Vector
      The right hand side of the equation.

    fdofs : BitArray
      BitArray of free degrees of freedoms.

    pre1 : Preconditioner
      First preconditioner if provided

    pre2 : Preconditioner
      Second preconditioner if provided

    sol : Vector
      Start vector for QMR method, if initialize is set False. Gets overwritten by the solution vector. If sol = None then a new vector is created.

    maxsteps : int
      Number of maximal steps for QMR. If the maximal number is reached before the tolerance is reached QMR stops.

    printrates : bool
      If set to True then the error of the iterations is displayed.

    initialize : bool
      If set to True then the initial guess for the QMR method is set to zero. Otherwise the values of the vector sol, if provided, is used.

    ep : double
      Start epsilon.

    tol : double
      Tolerance of the residuum. QMR stops if tolerance is reached.


    Returns
    -------
    (vector)
      Solution vector of the QMR method.

    """
    u = sol if sol else rhs.CreateVector()
    
    r = rhs.CreateVector()
    v = rhs.CreateVector()  
    v_tld = rhs.CreateVector()
    w = rhs.CreateVector()
    w_tld = rhs.CreateVector()
    y = rhs.CreateVector()
    y_tld = rhs.CreateVector()
    z = rhs.CreateVector()
    z_tld = rhs.CreateVector()  
    p = rhs.CreateVector()
    p_tld = rhs.CreateVector()
    q = rhs.CreateVector()  
    d = rhs.CreateVector()
    s = rhs.CreateVector()

    if (initialize): u[:] = 0.0

    r.data = rhs - mat * u
    v_tld.data = r
    y.data = pre1 * v_tld if pre1 else v_tld
    
    rho = InnerProduct(y,y)
    rho = sqrt(rho)
    
    w_tld.data = r 
    z.data = pre2.T * w_tld if pre2 else w_tld
    
    xi = InnerProduct(z,z)
    xi = sqrt(xi)
    
    gamma = 1.0
    eta = -1.0
    theta = 0.0

    
    for i in range(1,maxsteps+1):
        if (rho == 0.0):
            print('Breakdown in rho')
            return
        if (xi == 0.0):
            print('Breakdown in xi')
            return
        v.data = (1.0/rho) * v_tld
        y.data = (1.0/rho) * y

        w.data = (1.0/xi) * w_tld
        z.data = (1.0/xi) * z

        delta = InnerProduct(z,y)
        if (delta == 0.0):
            print('Breakdown in delta')
            return
        
        y_tld.data = pre2 * y if pre2 else y
        z_tld.data = pre1.T * z if pre1 else z

        if (i > 1):
            p.data = (-xi*delta / ep) * p
            p.data += y_tld

            q.data = (-rho * delta / ep) * q
            q.data += z_tld
        else:
            p.data = y_tld
            q.data = z_tld
        
        p_tld.data = mat * p
        ep = InnerProduct(q, p_tld)
        if (ep == 0.0):
            print('Breakdown in epsilon')
            return

        beta = ep/delta
        if (beta == 0.0):
            print('Breakdown in beta')
            return
        
        v_tld.data = p_tld - beta * v;      

        y.data = pre1 * v_tld if pre1 else v_tld
        
        rho_1 = rho
        rho = InnerProduct(y,y)
        rho = sqrt(rho)     
        
        
        w_tld.data = mat.T * q
        w_tld.data -= beta * w
        
        z.data = pre2.T * w_tld if pre2 else w_tld      
        
        xi = InnerProduct(z,z)
        xi = sqrt(xi)

        gamma_1 = gamma
        theta_1 = theta

        theta = rho/(gamma_1 * abs(beta)) 
        gamma = 1.0 / sqrt(1.0 + theta * theta)
        if (gamma == 0.0):
            print('Breakdown in gamma')
            return
    
        eta = -eta * rho_1 * gamma * gamma / (beta * gamma_1 * gamma_1);        

        if (i > 1):
            d.data = (theta_1 * theta_1 * gamma * gamma) * d
            d.data += eta * p

            s.data = (theta_1 * theta_1 * gamma * gamma) * s    
            s.data += eta * p_tld

        else: 
            d.data = eta * p
            s.data = eta * p_tld
        
        
        u.data += d
        r.data -= s

        #Projected residuum: Better terminating condition necessary?
        ResNorm = sqrt( np.dot(r.FV().NumPy()[fdofs],r.FV().NumPy()[fdofs]))
        #ResNorm = sqrt(InnerProduct(r,r))
        
        if (ResNorm <= tol):
            break
                
        if (printrates):
            print ("it = ", i, " err = ", ResNorm)
            
    return u




#Source: Michael Kolmbauer https://www.numa.uni-linz.ac.at/Teaching/PhD/Finished/kolmbauer-diss.pdf
def MinRes(mat, rhs, pre=None, sol=None, maxsteps = 100, printrates = True, initialize = True, tol = 1e-7):
    """Minimal Residuum method


    Parameters
    ----------

    mat : Matrix
      The left hand side of the equation to solve

    rhs : Vector
      The right hand side of the equation.

    pre : Preconditioner
      If provided the preconditioner is used.

    sol : Vector
      Start vector for MinRes method, if initialize is set False. Gets overwritten by the solution vector. If sol = None then a new vector is created.

    maxsteps : int
      Number of maximal steps for MinRes. If the maximal number is reached before the tolerance is reached MinRes stops.

    printrates : bool
      If set to True then the error of the iterations is displayed.

    initialize : bool
      If set to True then the initial guess for the MinRes method is set to zero. Otherwise the values of the vector sol, if prevented, is used.

    tol : double
      Tolerance of the residuum. MinRes stops if tolerance is reached.


    Returns
    -------
    (vector)
      Solution vector of the QMR method.

    """
    u = sol if sol else rhs.CreateVector()

    v_new = rhs.CreateVector()
    v = rhs.CreateVector()  
    v_old = rhs.CreateVector()
    w_new = rhs.CreateVector()
    w = rhs.CreateVector()
    w_old = rhs.CreateVector()
    z_new = rhs.CreateVector()
    z = rhs.CreateVector()
    mz = rhs.CreateVector()


    if (initialize):
        u[:] = 0.0
        v.data = rhs
    else:
        v.data = rhs - mat * u
        
    z.data = pre * v if pre else v
    
    #First Step
    gamma = sqrt(InnerProduct(z,v))
    gamma_new = 0
    z.data = 1/gamma * z 
    v.data = 1/gamma * v    
    
    ResNorm = gamma      
    ResNorm_old = gamma  
    
    if (printrates):
        print("it = ", 0, " err = ", ResNorm)       
        
    eta_old = gamma
    c_old = 1
    c = 1
    s_new = 0
    s = 0
    s_old = 0

    v_old[:] = 0.0
    w_old[:] = 0.0
    w[:] = 0.0
    
    k = 1
    while (k < maxsteps+1 and ResNorm > tol):
        mz.data = mat*z
        delta = InnerProduct(mz,z)
        v_new.data = mz - delta*v - gamma * v_old
        
        z_new.data = pre * v_new if pre else v_new

        gamma_new = sqrt(InnerProduct(z_new, v_new))
        z_new *= 1/gamma_new
        v_new *= 1/gamma_new
        
        alpha0 = c*delta - c_old*s*gamma    
        alpha1 = sqrt(alpha0*alpha0 + gamma_new*gamma_new) #**
        alpha2 = s*delta + c_old*c*gamma
        alpha3 = s_old * gamma

        c_new = alpha0/alpha1
        s_new = gamma_new/alpha1

        w_new.data = z - alpha3*w_old - alpha2*w
        w_new.data = 1/alpha1 * w_new   

        u.data += c_new*eta_old * w_new
        eta = -s_new * eta_old

        
        #update of residuum
        ResNorm = abs(s_new) * ResNorm_old
        if (printrates):        
            print("it = ", k, " err = ", ResNorm)   

        k += 1

        # shift vectors by renaming
        v_old, v, v_new = v, v_new, v_old
        w_old, w, w_new = w, w_new, w_old
        z, z_new = z_new, z
        
        eta_old = eta
        
        s_old = s
        s = s_new

        c_old = c
        c = c_new

        gamma = gamma_new
        ResNorm_old = ResNorm

    return u




def Newton(a, u, freedofs=None, maxit=100, maxerr=1e-11, inverse="umfpack", el_int=False, dampfactor=1, printing=True):
    """
    Newton's method for solving non-linear problems of the form A(u)=0.

    Parameters
    ----------
    a : BilinearForm
      The BilinearForm of the non-linear variational problem. It does not have to be assembled.

    u : GridFunction
      The GridFunction where the solution is saved. The values are used as initial guess for Newton's method.

    freedofs : BitArray
      The FreeDofs on which the assembled matrix is inverted. If argument is 'None' then the FreeDofs of the underlining FESpace is used.

    maxit : int
      Number of maximal iteration for Newton. If the maximal number is reached before the maximal error Newton might no converge and a warning is displayed.

    maxerr : float
      The maximal error which Newton should reach before it stops. The error is computed by the square root of the inner product of the residuum and the correction.

    inverse : string
      A string of the sparse direct solver which should be solved for inverting the assembled Newton matrix.

    el_int : bool
      Flag if eliminate internal flag is used. If this is set to True then Newton uses static condensation to invert the matrix. If freedofs is not None, the user has to take care that the local dofs are set to zero in the freedofs array.

    dampfactor : float
      Set the damping factor for Newton's method. If it is 1 then no damping is done. If value is < 1 then the damping is done by the formula 'min(1,dampfactor*it)' for the correction, where 'it' denotes the Newton iteration.

    printing : bool
      Set if Newton's method should print informations about the actual iteration like the error. 

    Returns
    -------
    (int, int)
      List of two integers. The first one is 0 if Newton's method did converge, -1 otherwise. The second one gives the number of Newton iterations needed.

    """
    w = u.vec.CreateVector()
    r = u.vec.CreateVector()

    err = 1
    numit = 0
    inv = None
    
    for it in range(maxit):
        numit += 1
        if printing:
            print("Newton iteration ", it)
            print ("energy = ", a.Energy(u.vec))
        a.Apply(u.vec, r)
        a.AssembleLinearization(u.vec)

        if freedofs == None:
            inv = a.mat.Inverse(u.space.FreeDofs(el_int), inverse=inverse)
        else:
            inv = a.mat.Inverse(freedofs, inverse=inverse)

        if el_int:
            r.data += a.harmonic_extension_trans * r
            w.data = inv * r
            w.data += a.harmonic_extension * w
            w.data += a.inner_solve * r
        else:
            w.data = inv * r
            
        err = sqrt(abs(InnerProduct(w,r)))
        if printing:
            print("err = ", err)

        energy = a.Energy(u.vec)
        u.vec.data -= min(1, it*dampfactor)*w
        
        if abs(err) < maxerr: break
    else:
        print("Warning: Newton might not converge!")
        return (-1,numit)
    return (0,numit)




def NewtonMinimization(a, u, freedofs=None, maxit=100, maxerr=1e-11, inverse="umfpack", el_int=False, dampfactor=1, linesearch=False, printing=True):
    """
    Newton's method for solving non-linear problems of the form A(u)=0 involving energy integrators.


    Parameters
    ----------
    a : BilinearForm
      The BilinearForm of the non-linear variational problem. It does not have to be assembled.

    u : GridFunction
      The GridFunction where the solution is saved. The values are used as initial guess for Newton's method.

    freedofs : BitArray
      The FreeDofs on which the assembled matrix is inverted. If argument is 'None' then the FreeDofs of the underlining FESpace is used.

    maxit : int
      Number of maximal iteration for Newton. If the maximal number is reached before the maximal error Newton might no converge and a warning is displayed.

    maxerr : float
      The maximal error which Newton should reach before it stops. The error is computed by the square root of the inner product of the residuum and the correction.

    inverse : string
      A string of the sparse direct solver which should be solved for inverting the assembled Newton matrix.

    el_int : bool
      Flag if eliminate internal flag is used. If this is set to True then Newton uses static condensation to invert the matrix. If freedofs is not None, the user has to take care that the local dofs are set to zero in the freedofs array.

    dampfactor : float
      Set the damping factor for Newton's method. If it is 1 then no damping is done. If value is < 1 then the damping is done by the formula 'min(1,dampfactor*it)' for the correction, where 'it' denotes the Newton iteration.

    linesearch : bool
      If True then linesearch is used to guarantee that the energy decreases in every Newton iteration.

    printing : bool
      Set if Newton's method should print informations about the actual iteration like the error. 

    Returns
    -------
    (int, int)
      List of two integers. The first one is 0 if Newton's method did converge, -1 otherwise. The second one gives the number of Newton iterations needed.

    """
    w = u.vec.CreateVector()
    r = u.vec.CreateVector()
    uh = u.vec.CreateVector()

    err = 1
    numit = 0
    inv = None
    
    for it in range(maxit):
        numit += 1
        if printing:
            print("Newton iteration ", it)
            print ("energy = ", a.Energy(u.vec))
        a.Apply(u.vec, r)
        a.AssembleLinearization(u.vec)

        if freedofs == None:
            inv = a.mat.Inverse(u.space.FreeDofs(el_int),inverse=inverse)
        else:
            inv = a.mat.Inverse(freedofs,inverse=inverse)

        if el_int:
            r.data += a.harmonic_extension_trans * r
            w.data = inv * r
            w.data += a.harmonic_extension * w
            w.data += a.inner_solve * r
        else:
            w.data = inv * r
            
        err = sqrt(abs(InnerProduct(w,r)))
        if printing:
            print("err = ", err)

        energy = a.Energy(u.vec)
        uh.data = u.vec - min(1, it*dampfactor)*w
            
        tau = min(1, it*dampfactor)
        if linesearch:
            while a.Energy(uh) > energy+1e-15:
                tau *= 0.5
                uh.data = u.vec - tau * w
                if printing:
                    print ("tau = ", tau)
                    print ("energy uh = ", a.Energy(uh))
        u.vec.data = uh
        if abs(err) < maxerr: break
    else:
        print("Warning: Newton might not converge!")
        return (-1,numit)
    return (0,numit)



def PreconditionedRichardson(a, rhs, pre=None, freedofs=None, maxit=100, tol=1e-8, el_int=False, dampfactor=1.0, printing=True):
    """ Preconditioned Richardson Iteration

    Parameters
    ----------
    a : BilinearForm
      The left hand side of the equation to solve

    rhs : Vector
      The right hand side of the equation.

    pre : Preconditioner
      If provided the preconditioner is used.
    
    freedofs : BitArray
      The FreeDofs on which the Richardson iteration acts. If argument is 'None' then the FreeDofs of the underlying FESpace is used.

    maxit : int
      Number of maximal iteration for Richardson iteration. If the maximal number is reached before the tolerance is reached a warning is displayed.

    tol : double
      Tolerance of the residuum. Richardson iteration stops if residuum < tolerance*initial_residuum is reached.

    el_int : bool
      Flag if eliminate internal flag is used. If this is set to True then Richardson iteration acts only on the non-local dofs. If freedofs is not None, the user has to take care that the local dofs are set to zero in the freedofs array.

    dampfactor : float
      Set the damping factor for the Richardson iteration. If it is 1 then no damping is done. Values greater than 1 are allowed.

    printing : bool
      Set if Richardson iteration should print informations about the actual iteration like the residuum. 

    Returns
    -------
    (vector)
      Solution vector of the Preconditioned Richardson iteration.

    """

    u = rhs.CreateVector()
    r = rhs.CreateVector()
    u[:] = 0

    projector = Projector(freedofs if freedofs else a.space.FreeDofs(coupling=el_int), False)
    
    r.data = rhs # r.data = rhs - a.mat*u
    r.data -= projector*r

    it = 0
    initial_res_norm = Norm(r)
    if printing:
        print("it =", it, " ||res||_2 =", initial_res_norm) 
    
    for it in range(1, maxit+1):
        u.data += dampfactor*(pre*r if pre else r)
        r.data = rhs - a.mat*u
        r.data -= projector*r

        res_norm = Norm(r)
        if printing:
            print("it =", it, " ||res||_2 =", res_norm)  
        if res_norm < tol*initial_res_norm:
            break
    else:
        print("Warning: Preconditioned Richardson did not converge to TOL")    

    return u   


