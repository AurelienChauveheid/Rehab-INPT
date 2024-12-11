import numpy as np

def matrixRotation(n,theta):

    '''
    entrée : 
    int n : indice de la matrice de rotation/ choix de la coordonnée angulaire
    float theta : valeur de la rotation

    sortie :
    renvoie la matrice rotaion d'indice n d'une rotation theta
    '''

    #intialise la matrice 
    R = np.zeros((3,3))

    # remplis la matrice en foncton de l'indice n et de theta
    R[(n-1)%3][(n-1)%3] = 1
    R[n%3][n%3] = np.cos(theta)
    R[n%3][(n+1)%3] = -np.sin(theta)
    R[(n+1)%3][n%3] = np.sin(theta)
    R[(n+1)%3][(n+1)%3] = np.cos(theta)

    return R

def matrixTranslation(x,y,z,phi,theta,psi):

    '''
    entrée : 
    floar x,y,z : coordonnées des transations selon les axes respectifs x,y,z
    float phi,theta,psi : valeur des rotations autour des axes respectifs x,y,z

    sortie :
    renvoie la matrice de translation 
    '''

    # calcul des différentes matrices de rotations utiles
    R3_phi = matrixRotation(3,phi)
    R1_theta = matrixRotation(1,theta)
    R3_psi = matrixRotation(3,psi)

    # calcul de la matrice de rotation globale
    R = R3_phi @ R1_theta @ R3_psi

    # définit la matrice de translation
    T = np.zeros((4,4))

    # remplis la matrice de translation avec les valeurs calculées
    T[:3]= np.concatenate((R,np.array([[x],[y],[z]])), axis = 1)
    T = np.concatenate((T[:3],np.array([[0,0,0,1]])), axis = 0)

    return T

if __name__ == "__main__":

    # print(matrixRotation(1,np.pi/4))
    # print(matrixRotation(2,np.pi/4))
    # print(matrixRotation(3,np.pi/4))

    theta = np.pi/8
    phi = np.pi/4
    T = matrixTranslation(0,0,0,theta,phi,0)
    print(T)