import io
import sys
import pandas as pd
import numpy as np
import uuid
import os

df1=pd.DataFrame({'*META':['META'],
                    'VERSION':['2'],
                    'MINVERSION':['1']},
                    index=[0])

def parseExchangeRequirementsTable():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
    #############hier bitte anpassen############
    completeTable = pd.read_excel("SampleDataset.xlsx", sheet_name = "Report", skiprows=2) #csv Name muss noch geregelt werden  # delim_whitespace=True,
    return completeTable

def getListOfPsets(completeTable):
    NameOfPsets = completeTable[["Pset"]].drop_duplicates(ignore_index=True)
    df2 = pd.DataFrame([])
    df_new = df2.assign(ID=np.arange(3,3+len(NameOfPsets)),NAME=NameOfPsets,GROUP='GROUP')
    listOfPsets = df_new[['GROUP','ID','NAME']]
    listOfPsets.rename(columns={'GROUP':'*GROUP'},inplace=True)
    return listOfPsets

def getListOfParameters(completeTable, listOfPsets):
    df3 = completeTable[["Merkmal BUW", "Pset",'Datentyp']].drop_duplicates(ignore_index = True)
    grouping = pd.Series(listOfPsets.ID.values,index=listOfPsets.NAME).to_dict()
    df3['GROUP'] = df3['Pset'].map(grouping)
    for name in df3['Merkmal BUW'].unique():
        df3.loc[df3['Merkmal BUW'] == name, 'GUID'] = uuid.uuid4()
    df3['Datentyp'].replace(['String','Integer','Entity','Real','Boolean'],['TEXT','NUMBER','NUMBER','NUMBER','YESNO'],inplace=True)
    df3_new = df3.assign(PARAM='PARAM',VISIBLE='1',DATACATEGORY='',DESCRIPTION='',USERMODIFIABLE='1')
    df3_new.rename(columns={'PARAM':'*PARAM','Merkmal BUW':'NAME','Datentyp':'DATATYPE'},inplace=True)
    listOfParameters = df3_new[['*PARAM','GUID','NAME','DATATYPE','DATACATEGORY','GROUP','VISIBLE','DESCRIPTION','USERMODIFIABLE']]
    return listOfParameters

def getMetaProp(completeTable):
    propertyType = completeTable[["Bezeichnung","IfcEntity","Merkmal BUW","Datentyp","gleich"]].drop_duplicates()
    propertyType['Datentyp'].replace(['String','Integer','Entity','Real','Boolean','Enum','Binary'],['Text','Int','Text','Double','Text','Text','Text'],inplace=True)
    metaProperty = pd.DataFrame([])
    for object in propertyType['Bezeichnung'].unique():
        df4 = pd.read_csv(f'UniqueIds/{object}.txt',header=None)
        df_mrk = propertyType.loc[propertyType['Bezeichnung'] == object]
        df4.columns=['externalId']
        numberOfProperty = len(df_mrk)
        df_ID = df4.iloc[np.arange(len(df4)).repeat(numberOfProperty)].reset_index(drop=True)
        df5 = pd.concat([df_mrk[["Merkmal BUW"]],df_mrk[["Datentyp"]],df_mrk[["gleich"]]],axis=1)
        df5_repeat = pd.concat([df5]*len(df4),ignore_index=True)
        df5_new = pd.concat([df_ID,df5_repeat],axis=1)
        df5_new.columns=['externalId','displayName','metaType','displayValue']
        df5_assign = df5_new.assign(component = object, displayCategory = 'IFC-Parameter',categoryId = 'PG_IFC',filelink = '',filename = '',link = '')
        df5_end = df5_assign[["externalId","component","displayCategory","categoryId","displayName","displayValue","metaType","filelink","filename","link"]]
        metaProperty = metaProperty.append(df5_end)
    print(metaProperty)
    return metaProperty


def getPsetList(completeTable):
    df6 = completeTable[["Merkmal BUW", "Pset",'Datentyp','IfcEntity']].drop_duplicates(ignore_index = True)
    psetList = pd.DataFrame([])
    psetList.to_csv(r'PsetList.txt', header=False, index=False, sep='\t', mode='w')
    for i in df6.IfcEntity.unique():
        for j in df6.Pset.unique():
            df6_new = pd.DataFrame([])
            df6_list = pd.DataFrame([])
            psetList = df6_new.assign(PropertySet='',Pset1=df6.loc[(df6['Pset']==j) & (df6['IfcEntity']==i),'Merkmal BUW'],dtype = df6.loc[(df6['Pset']==j) & (df6['IfcEntity']==i), 'Datentyp'],IfcEntity2='')
            if psetList.empty == False:
                psetList.rename(columns={'PropertySet':'PropertySet:','Pset1':str(j),'dtype':'|','IfcEntity2':str(i)},inplace=True)
            else:
                continue
            psetList.to_csv(r'PsetList.txt', header=True, index=False, sep='\t', mode='a')
    return psetList

completeTable = parseExchangeRequirementsTable()
listOfPsets = getListOfPsets(completeTable)
listOfParameters = getListOfParameters(completeTable, listOfPsets)
metaProperty = getMetaProp(completeTable)
psetList = getPsetList(completeTable)
