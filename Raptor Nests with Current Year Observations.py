# Author: Andrew Laws
# Date: 1/15/2018

# Details: BFO biologists asked for a script for their toolbar to create a 
# layer of raptor nest locations from the most recent year. Created for ArcMap 10.3.

import arcpy

workspace = arcpy.GetParameterAsText(0)
fcRaptorNests = arcpy.GetParameterAsText(1)
tblRaptorNestObservation = arcpy.GetParameterAsText(2)
fcRN2017 = arcpy.GetParameterAsText(3)
layersave = arcpy.GetParameterAsText(4)

#arcpy.env.workspace = workspace
arcpy.env.workspace = workspace
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

#Add Raptor Nests as layer
layer = "Raptor Nests"
arcpy.MakeFeatureLayer_management(fcRaptorNests, layer) #where feature class is added

table = "tblRaptorNestObservation"
arcpy.MakeTableView_management(tblRaptorNestObservation, table)
addTable = arcpy.mapping.TableView(table)
arcpy.mapping.AddTableView(df, addTable)
arcpy.SelectLayerByAttribute_management("tblRaptorNestObservation", "NEW_Selection", "DateObserved > date '2016-12-31 00:00:00' and DateObserved < date '2018-01-01 00:00:00'")
arcpy.CopyRows_management("tblRaptorNestObservation", r'T:\WY\HPD\BF\_GIS_USER_PROJECTS\GIS\Projects\WildlifeSurveyData\Working\BFO_WildlifeSurveys_Working.gdb\tblRaptorNestObservation2017',)

#Join tbl to lyr with definition query
arcpy.AddJoin_management(layer, "NestID", r'T:\WY\HPD\BF\_GIS_USER_PROJECTS\GIS\Projects\WildlifeSurveyData\Working\BFO_WildlifeSurveys_Working.gdb\tblRaptorNestObservation2017', "NestID", "KEEP_COMMON")

addLayer = arcpy.mapping.Layer(layer)
arcpy.mapping.AddLayer(df, addLayer, "AUTO_ARRANGE") #where layer was added

#arcpy.RefreshActiveView()
arcpy.SaveToLayerFile_management(layer, layersave, "ABSOLUTE")

#Apply symbology and save layer
arcpy.ApplySymbologyFromLayer_management(layersave, r'T:\WY\HPD\BF\_GIS_USER_PROJECTS\Resources\Wildlife\Data\Layers\Reference\ObservationsSymbology.lyr')

del layer
del addLayer
del fcRaptorNests
del tblRaptorNestObservation
del layersave
del workspace
del mxd
del df
