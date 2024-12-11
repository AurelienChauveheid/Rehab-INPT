import numpy as np
import csv

def createDict(frameTab, frameAngles, distances, angleInit):

    '''
    frameTab : Tableau des frammes
    frameAngles : Tableau des parmaètres angulaires angulaires du mouvement en radians
    distances : tableau des longuers du bras et avant bras
    angleInit : paramètre angulaire initiaux du bras

    v_angles : tableau des vitesses angulaires instanttanées par frame avec bruit
    pos : tableau des coordonnées X,Y,Z des articulations du bras
    '''

    # definit la dernière frame comme le dernier instant clé renseigné
    frame_end = frameTab[-1]
    v_angles = np.zeros((frame_end , 4))

    # calcule les vitesse angulaires instantané en faisant l'hypothèse d'un mouvement angulaire à vitesse constante
    for ind, frame in enumerate(frameTab):
        if ind == 0:
            for i in range(frame):

                # Pour le premier mvt on utilise la configuration initiale
                v_angles[i] = (frameAngles[ind] - angleInit)/frame
        
        else:
            for i in range(frameTab[ind-1],frame):

                # sinon on utilise comme origine de temps la derniere frame du mouvement précédent
                v_angles[i] = frameAngles[ind]/(frame - frameTab[ind-1])

    # on initilalise le tableau des positions et des angles
    # les angles seront calculées à partir d'angleInit et des viteeses angulaires instantanées
    pos = []
    angles = angleInit.copy()

    for i in range(frame_end):
        
        # genération d'un bruit léger à chaque instant
        angles_noise = noise(sigma = abs(v_angles[i]).sum()/6, eps = abs(v_angles[i]).sum()/2)
        v_angles[i] = v_angles[i] + angles_noise

        # calcule des coordonnées angulaires à l'instant i
        angles = angles + v_angles[i]

        # calcule la position à l'instant i avec les coordonnées angulaires
        pos.append(calculPos(distances, angles))

        # retire le bruit généré à cet itération des coordonnées angulaires
        angles =  angles - angles_noise

    return v_angles, pos

def calculPos(distances, angles):

    '''
    distances : tableau des longuers du bras et avant bras
    angles : paramètre du mouvement 

    renvoie une liste de taille 9 des position X,Y,Z respectives de l'épaule, coude et du poignet
    '''

    [d1, d2] = distances
    [X_shoulder, Y_shoulder, intern_shoulder, elbow] = angles

    # pour calculer dans un premier temps la position du coude on utilisera un repére shérique 
    # centré à l'épaule dans le plan horizontale au sol de l'axe des épaules gauche et droite
    # pour celle du poignet on utilisera le repère sphérique centrée au coude dans le plan (épaule-coude/coude-poignet)

    a_out = np.zeros(3)

    theta_elbow = X_shoulder
    phi_elbow = Y_shoulder

    b_out = a_out + d1*np.array([np.sin(phi_elbow)*np.cos(theta_elbow),
                                 np.sin(phi_elbow)*np.sin(theta_elbow),
                                 np.cos(phi_elbow)])
    
    theta_wrist = intern_shoulder 
    phi_wrist = np.pi - elbow 
    
    c_out = b_out + d2*np.array([np.sin(phi_wrist) * np.cos(theta_wrist),
                                 np.sin(phi_wrist) * np.sin(theta_wrist),
                                 np.cos(phi_wrist)])
    
    return a_out.tolist() + b_out.tolist() + c_out.tolist()

def noise(sigma, eps):

    '''
    sigma : écart type du bruit généré
    eps : seuil à ne pas dépasser pour avoir un bruit léger
    
    renvoie un bruit des paramètres angulaires
    '''

    angles_noise = np.random.normal(0, sigma, 4)
    while abs(angles_noise).sum() > eps:
        angles_noise = np.random.normal(0, sigma, 4)

    return angles_noise

def generate_param(n = 1, init_param = np.array((0,0,0,0))):

    '''
    int n : nombre de mouvement à générer à la suite
    init_param np.array(4)[float] : parametre angulaire intiale du bras

    frameAngles np.array(10,4)[float] : tableau des variations angulaires par indice de frame
    '''

    # intialise les angles initiaux et la sortie
    param = init_param.copy().reshape((4))
    frameAngles = np.zeros((n,4))

    for i in range(n):

        if i!=0:
            param = frameAngles[i-1]

        # génére les variations angulaires possibles en fonction des paramètres initiaux
        X_shoulder = np.random.uniform(-np.pi/4 - param[0], np.pi/4 - param[0])
        Y_shoulder = np.random.uniform(-np.pi/4 - param[1], np.pi/4 - param[1])
        intern_shoulder = np.random.uniform(-param[2], np.pi/2 - param[2])
        elbow = np.random.uniform(-np.pi/4 - param[3], np.pi/4 - param[3])

        # mets à jour le tableau des variations angulaires
        frameAngles[i] = np.array([X_shoulder, Y_shoulder, intern_shoulder, elbow])

    return frameAngles

def dataSimulation(target_folder, nb_simul = 100, distances = np.array([1,1]), fps = 24, vang_max = np.pi/2, vang_min = 8/np.pi):

    '''
    target_folder : chemin pour enregistrer les csv
    nb_simul : nombre de simulation à faire
    distances : longueurs des brass et avant bras
    fps : nombres de frames par seconde
    vang_min : vitesse angulaire minimum du patient
    vang_max : vitesse angulaire maximum du patient
    
    crée les fichiers csv en simulant les mouvements
    '''

    for ind in range(nb_simul):

        # génére les mouvements à partir d'une configuration initiale du bras
        angleInit = generate_param(n = 1).reshape(4)
        frameAngles = generate_param(n = 1, init_param = angleInit).reshape(4)

        # génére une vitesse comprise entre vang_max et vangmin et calcule le tableau de frame en fonction de la vitesse
        v_ang = np.random.uniform()*(vang_max-vang_min) + vang_min
        frameTab = [int(max(abs(frameAngles))*fps/v_ang)]

        # calcule les vitesses instantanées et les positions du mouvement
        v_angles, pos = createDict(frameTab, frameAngles, distances, angleInit)
        
        # crée les csv
        h1 = ["X_shoulder", "Y_shoulder", "intern_shoulder", "elbow"]
        with open(target_folder+"angles/angles_"+str(ind)+".csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(h1)
            writer.writerows(v_angles)

        h2 = ["Xshoulder", "Yshoulder", "Zshoulder", "Xelbow", "Yelbow", "Zelbow", "Xwrist", "Ywrist", "Zwrist"]
        with open(target_folder+"pos/pos_"+str(ind)+".csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(h2)
            writer.writerows(pos)

        h3 = ["X_shoulder", "Y_shoulder", "intern_shoulder", "elbow", "frames"]
        with open(target_folder+"param/param_"+str(ind)+".csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(h3)
            
            # writer.writerows(np.concatenate( (frameAngles, frameTab.reshape) , axis=1))
            

if __name__ == "__main__":

    dataSimulation(target_folder="./workspace/", nb_simul=10000)