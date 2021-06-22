# Schnittstellen-zu-Autorensoftware

--Deutsch--<br />
Ziel ist es, Schnittstellen zwischen der BUW-Prozessdatenbank (BUW-Datenbank) und Autorensoftwares wie Revit oder ArchiCAD zu entwickeln, um den automatischen Import der erforderlichen Parameter aus dem Exchange Requirement (ER) in BIM-Modelle zu erreichen.


--English--<br />
The goal is to develop interfaces between BUW Process Database (BUW Database) and authoring softwares such as Autodesk Revit or ArchiCAD, to achieve the automatic importing of required parameters from Exchange Requirement (ER) into BIM Models. 


## RevitImportGenerator

The interface for Revit ist developed based on a plugin named MetaProp: https://github.com/jeremytammik/rvtmetaprop. Anyone wants to use the Parser for Revit should install MetaProp in Revit first.The Revit Import Generator consists of three files: two python files and one sample dataset. The dataset can be pulled directly from the BUW Database. The Generator was written based on the specific form. Therefore, user must firstly fill the dataset according to the given sample, and change the name of file in python file if it's needed. Another prerequisite is to write specific uniqueIDs of objects in Revit into UniqueIds. One simple way to get those IDs is using Dynamo. If no specific objects are referred to, the codes relevant to UniqueIDs should be commented out. By running the revitImportGenerator.py, three new files will be generated (see the folder of SampleResults): <br />

### 1. Shared Parameter List<br />
It is used in Revit for generating shared parameters. Shared parameters can be assigned to existing or new objects by defining project parameters in Revit. However, attributes assigned through shared parameters have no values. The value of parameter should be filled in for each instance manually.<br />

### 2. PsetList<br />
PsetList is needed by the export of Revit model into IFC file. Assigned attributes can therefore be grouped under different property sets according to this list.<br />

### 3. MetaProperty<br />
This CSV file is for assigning attributes as well as their values to specific revit instances. This file can be imported via the Meta Prop plugin.
