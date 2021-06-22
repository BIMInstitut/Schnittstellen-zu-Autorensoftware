import io
import sys
import pandas as pd
import numpy as np
import uuid
import csv
from sharedParameterBuilder import df1, completeTable, listOfPsets, listOfParameters, metaProperty, psetList

def createSharedParameter(listOfPsets,listOfParameters):
    #############hier bitte anpassen############
    f = open("SampleSharedParameterList.txt", "w")
    f.write("# This is a Revit shared parameter file.\n# Do not edit manually.\n")
    f.close()
    #############hier bitte anpassen############
    df1.to_csv(r'SampleSharedParameterList.txt', header=True, index=False, sep='\t', mode='a')
    listOfPsets.to_csv(r'SampleSharedParameterList.txt', header=True, index=False, sep='\t', mode='a',encoding="utf-8")
    listOfParameters.to_csv(r'SampleSharedParameterList.txt', header=True, index=False, sep='\t', mode='a',encoding="utf-8")

def createMetaProperty(metaProperty):
    metaProperty.to_csv(r'MetaProperty.csv', header=True, index=False, sep=',', mode='w', quoting=csv.QUOTE_ALL)

# def createPsetList(psetList):
    # psetList.to_csv(r'PsetList.txt', header=True, index=False, sep='\t', mode='a')

def main():
    createSharedParameter(listOfPsets,listOfParameters)
    createMetaProperty(metaProperty)
    # createPsetList(psetList)

if __name__ == '__main__':
    main()
