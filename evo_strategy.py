import numpy as np
import math

def f(theta):
    assert isinstance(theta,np.ndarray)
    assert len(theta)==2
    return 1.0-abs(theta[0]-0.2)-abs(theta[1]-0.7)


def optim(N,f,niter=100,verb=False):
    best_theta = np.array([0.5]*N)
    f_best_theta = f(best_theta)

    for i in range(niter):
        theta = best_theta + np.random.normal( size=(N) , scale= 0.3 if i < (niter/2) else 0.01 )
        f_theta = f(theta)

        if f_theta > f_best_theta:
            best_theta = theta
            f_best_theta = f_theta
            if verb:
                print "iteration ",i," , f(",best_theta,") = ",f_best_theta
    return best_theta

if __name__ == '__main__':
    r = optim(2,f,verb=False)
    print "f(",r[0],",",r[1],") = ",f(r)
