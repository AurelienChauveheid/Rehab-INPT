import numpy as np
from copy import copy

def solver_final_point (init_coord, target):

    '''
    input:
    init_coord (np.array(3,3)) : coordonnées initilae du bras
    target np.array(3) : coordonnée de la cible

    output:
    out_coord = (np.array(3,3)) : coordonnées finales du bras pour saisir l'objet

    Le repère des points dépendra de l'acquisition de cceux ci avec une kinect.
    On considére x orienté par les épaules et y par le tronc et z est définie par le système de la kinect

    Calcule la position du noeud du coude pour attraper une cible "target" en vérifiant si la cible est atteignable sinon renvoie False
    '''

    [a,b,c] = init_coord

    [d1,d2] = [np.linalg.norm(a - b), np.linalg.norm(b - c)]
    dtarget = np.linalg.norm(a - target)

    if d1 + d2 < dtarget:
        return False
    
    # on convertit les coordonées carthésiennes de a et target en sphériques pour calculer les deux angles entre eux
    [x,y,z] = target - a

    if x!=0:
        theta = np.arctan(y/x)
    else:
        theta = np.pi/2
    phi = np.arccos(z/np.sqrt(x**2 + y**2 + z**2))
    
    # En utilisant le théorème de pythagore généralisé on a:

    #on calcule les distances finales projetés dans le plan (O,x,y)
    d1p = d1*np.sin(phi)
    d2p = d2*np.sin(phi)
    dtargetp = dtarget*np.sin(phi)

    # On calcule avec le théorème de pythagore généralisé les angles formés dans le triangle
    angle_elbow_radp = np.arccos((d1p**2 + d2p**2 - dtargetp**2)/(2*d1p*d2p))
    angle_shoulder_radp = np.arccos((d1p**2 + dtargetp**2 - d2p**2)/(2*d1p*dtargetp))
    
    #on calcule les coordonnées obtenus à partir des paramètres calculées pour tester la fonction
    # épaule
    a_out = a.copy()
    # coude
    b_out = a_out + d1*np.array([np.sin(phi)*np.cos(theta + angle_shoulder_radp),
                                 np.sin(phi)*np.sin(theta + angle_shoulder_radp),
                                 np.cos(phi)])
    # poignet
    c_out = b_out + d2*np.array([np.sin(phi) * np.cos(angle_elbow_radp),
                                 np.sin(phi) * np.sin(angle_elbow_radp),
                                 np.cos(phi)])
    # cible
    d_out = a_out + dtarget*np.array([np.sin(phi) * np.cos(theta),
                                      np.sin(phi) * np.sin(theta),
                                      np.cos(phi)])
    
    print("\n")
    print("test pour vérifier la conservation de la distance du bras")
    print("longueur de l'avant bras : ",d2)
    print("longueur entre la position du coude finae et la cible : ", np.linalg.norm(target - b_out))

    return np.array([a_out, b_out, c_out, d_out]), np.array([theta, phi, angle_elbow_radp, angle_shoulder_radp])

if __name__ == "__main__":

    init_coord = np.array([[0,0,0],[0,np.sqrt(2)/2,np.sqrt(2)/2],[0,np.sqrt(2),np.sqrt(2)]])
    target = np.array([1e-10,0.5,1.2])
    