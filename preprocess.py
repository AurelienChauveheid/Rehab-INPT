import numpy as np
import pandas as pd
from arm import Arm
import sys

def extractStrokePatientExel(filepath):

    df = pd.read_csv(filepath, header = 0)

    headerline = df.columns
    dfData = df.iloc[1:].fillna(0).astype(float)
    df_Collumns_length = int(dfData.shape[1]/3)
    
    dfCoordinates = pd.DataFrame()

    for i in range(df_Collumns_length):
        name = headerline[i*3]

        column0 = dfData[dfData.columns[i*3]]
        column1 = dfData[dfData.columns[i*3 + 1]]
        column2 = dfData[dfData.columns[i*3 + 2]]

        dfCoordinates[name] = list(zip(column0, column1, column2))
        dfCoordinates = dfCoordinates.map(lambda x: np.array(list(x)))


    return dfCoordinates

def extendNodes(dfCoordinates):
    wrist = np.mean([np.array(dfCoordinates[" WRA"]), np.array(dfCoordinates[" WRB"])], axis = 0)
    elbow = np.mean([np.array(dfCoordinates[" ELB_M"]), np.array(dfCoordinates[" ELB_L"])], axis =0)
    shoulder = np.mean([np.array(dfCoordinates[" SA_1"]), np.array(dfCoordinates[" SA_2"]), np.array(dfCoordinates[" SA_3"])], axis = 0)

    return pd.DataFrame({"Wrist" : wrist, "Elbow" : elbow, "Shoulder" : shoulder})

def preprocess_csv(filepath, sep = ','):

    arrayNodes = []
    with open(filepath, 'r') as f:

        header1 = np.array(f.readline().strip().split(sep))
        header2 = f.readline().strip().split(sep)

        for ligne in f:
            # Enlève les sauts de ligne et divise par le séparateur sep
            arrayNodesRow = np.array(ligne.strip().split(sep))
            arrayNodesRow = np.where(arrayNodesRow == "", "0.0", arrayNodesRow)
            arrayNodesRow = arrayNodesRow.astype(float)
            arrayNodes.append(arrayNodesRow)

    return header1, header2, np.array(arrayNodes)

def extendNodes_csv(header1, arrayNodes):

    DictNodesCarthesian = {}
    DictWES = {}

    for i in range(int(len(header1)/3)):
        name = header1[i*3]

        column0 = arrayNodes.transpose()[i*3]
        column1 = arrayNodes.transpose()[i*3 + 1]
        column2 = arrayNodes.transpose()[i*3 + 2]

        DictNodesCarthesian[name] = np.array([column0.transpose(), column1.transpose(), column2.transpose()]).transpose()

    DictWES["shoulder"] = np.mean([DictNodesCarthesian[" SA_1"], DictNodesCarthesian[" SA_2"], DictNodesCarthesian[" SA_3"]], axis = 0).reshape(-1,3)
    DictWES["elbow"] = np.mean([DictNodesCarthesian[" ELB_M"], DictNodesCarthesian[" ELB_L"]], axis =0).reshape(-1,3)
    DictWES["wrist"] = np.mean([DictNodesCarthesian["WRA"], DictNodesCarthesian[" WRB"]], axis = 0).reshape(-1,3)

    return DictWES

if __name__ == "__main__":

    # dfCoordinates = extractStrokePatientExel(".\workspace\data\Stroke\S1_1_2.csv")
    # dfNodes = extendNodes(dfCoordinates)
    
    # nodes_init = dfNodes.iloc[35]
    # nodes_init = np.array([nodes_init["Shoulder"], nodes_init["Elbow"], nodes_init["Wrist"]])
    # print(nodes_init)

    # arm = Arm(nodes_init)
    # arm.visu_mathplotlib(dfNodes)

    filepath = 'C:/Users/INPT/Documents/modelisation/workspace/data/Stroke/S1_1_2.csv'
    header1, header2, arrayNodes = preprocess_csv(filepath)
    DictWES = extendNodes_csv(header1, arrayNodes)
    print(DictWES["wrist"].shape)
    print(DictWES["wrist"])
    