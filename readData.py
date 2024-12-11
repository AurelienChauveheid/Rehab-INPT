import csv
import numpy as np
import tensorflow as tf
from tensorflow import keras
from STGCN.GCN.sgcn_lstm import Sgcn_Lstm

def preprocess_csv(filepath, sep = ','):

    arrayNodes = []
    with open(filepath, 'r') as f:

        header = np.array(f.readline().strip().split(sep))

        for ligne in f:
            # Enlève les sauts de ligne et divise par le séparateur sep
            arrayNodesRow = np.array(ligne.strip().split(sep))
            arrayNodesRow = np.where(arrayNodesRow == "", "0.0", arrayNodesRow)
            arrayNodesRow = arrayNodesRow.astype(float)
            arrayNodes.append(arrayNodesRow)

    return header, np.array(arrayNodes)

def read_data(n, folderpath):

    # TODO : determiner nb_frame max et faire de la data augmentation en conséquences

    input = []

    '''
    index_Spine_Base=0
    index_Spine_Mid=4
    index_Neck=8
    index_Head=12   # no orientation
    index_Shoulder_Left=16
    index_Elbow_Left=20
    index_Wrist_Left=24
    index_Hand_Left=28
    index_Shoulder_Right=32
    index_Elbow_Right=36
    index_Wrist_Right=40
    index_Hand_Right=44
    index_Hip_Left=48
    index_Knee_Left=52
    index_Ankle_Left=56
    index_Foot_Left=60  # no orientation    
    index_Hip_Right=64
    index_Knee_Right=68
    index_Ankle_Right=72
    index_Foot_Right=76   # no orientation
    index_Spine_Shoulder=80
    index_Tip_Left=84     # no orientation
    index_Thumb_Left=88   # no orientation
    index_Tip_Right=92    # no orientation
    index_Thumb_Right=96  # no orientation
    '''

    for i in range(n):

        header, arrayNodes = preprocess_csv(folderpath + str(i) + ".csv")
        input.append([])

        for Nodes in arrayNodes:

            a = np.zeros(16).tolist()
            b = np.concatenate( (Nodes.reshape((3,3)), 2*np.ones(3).reshape((3,1))), axis = 1).flatten().tolist()
            c = np.zeros(100 - 28).tolist()

            input[-1].append(a + b + c)

        if i%100 == 0:
            print(i)

    input_size = max([len(input[i]) for i in range(len(input))])
    
    for i in range(len(input)):
        for j in range(abs(input_size - len(input[i]))):
            input[i].append(input[i][-1])
        
    return tf.convert_to_tensor(input, dtype=tf.float32)

if __name__ == "__main__":

    # header, arrayNodes = preprocess_csv("./workspace/pos/pos_0.csv")
    # print(arrayNodes.shape)
    # print(arrayNodes[:5])
    # print(torch.tensor(arrayNodes)[:5])

    input = read_data(100, "workspace/pos/pos_")
    print(input.shape)
    
    with open('STGCN/pretrain_model/rehabilitation.json', 'r') as f:
        model_json = f.read()
    
    model = tf.keras.models.model_from_json(model_json, custom_objects={'tf': tf})
    model.load_weights("STGCN/pretrain_model/rehabilitation/model/best_model.hdf5")
