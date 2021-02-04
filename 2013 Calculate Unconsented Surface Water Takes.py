#A Model fo Assessing the Magnitude of Unconsented Surface Water Use in
#the Canterbury Region


def CalculateFinYear(Month,Year):

    if Month >= 7:
        FinYear =  str(Year) + "_" + str(int(Year) + 1)
    else:
        FinYear =  str(int(Year) - 1) + "_" + str(Year)

    return FinYear


import arcpy,os
from arcpy import env
from time import localtime,strftime

env.overwriteOutput = True
docpath = r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes" + "\\"


print "Inital Setup...."

#Import Variables from Config File.

vals = []
animals = ["Domestic","Dairy Cow","Cow","Deer","Sheep","Pig","Goat","Horse","Emu","Ostrich","Camelid","Poultry"]
entry = open(docpath + '\\' + "Config.csv")
entry.readline()

for e in entry:
    vals.append(e.strip().split(","))

entry.close()    

newentry = False

for val in vals[:-2]:
    if  not (val[0] in animals):
        print  '"' + val[0] + '"' + " is a newly listed variable. Please contact the GIS Team to make this change."
        newentry = True

if newentry == True:
    sys.exit()

for val in vals:
    if val[0] == "Domestic":
        DOMWU = float(val[1])
    elif val[0] == "Dairy Cow":
        DCWU = float(val[1])       
    elif val[0] == "Cow":
        BFWU = float(val[1])
    elif val[0] == "Deer":
        DRWU = float(val[1])
    elif val[0] == "Sheep":
        SHWU = float(val[1])
    elif val[0] == "Pig":
        PGWU = float(val[1])
    elif val[0] == "Goat":
        GTWU = float(val[1])
    elif val[0] == "Horse":
        HRWU = float(val[1])
    elif val[0] == "Emu":
        EUWU = float(val[1])
    elif val[0] == "Ostrich":
        OSWU = float(val[1])
    elif val[0] == "Camelid":
        CMWU = float(val[1])
    elif val[0] == "Poultry":
        POWU = float(val[1])
    elif val[0] == "Leakage":
        leakage = float(val[1])


#output = vals[-1][1]
output = arcpy.GetParameterAsText(1)

if os.path.exists (r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output") == False:
    os.mkdir(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output")
            
if os.path.exists (r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology") == False:
    os.mkdir(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology")

if os.path.exists (r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes") == False:
    os.mkdir(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes")

if arcpy.Exists(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb") == False:
    arcpy.CreateFileGDB_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes", "Scratch.gdb")

else:
    arcpy.Compact_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb")

env.workspace = r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb"
env.scratchWorkspace = r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb"

for f in arcpy.ListFeatureClasses():
    if arcpy.TestSchemaLock(f):
        arcpy.Delete_management(f)


print "Extracting Datasets...."
arcpy.AddMessage("\nExtracting Datasets....")

#arcpy.MakeFeatureLayer_management(r"C:\Users\hamishl\Documents\ArcGIS\Default.gdb\Square","Input") ##INPUT
arcpy.MakeFeatureLayer_management(arcpy.GetParameterAsText(0),"Input")

arcpy.Dissolve_management("Input",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area_Extent")
arcpy.Delete_management("Input")
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area_Extent","Extent")

#print "\tUrban Area"
#arcpy.AddMessage("\tUrban Area")
#arcpy.MakeFeatureLayer_management(r"Database Connections\DC GISSQL2012 GISuser.sde\GIS.DBO.STATISTICS_NZTM_UrbanArea_Generalised",
    #"Urban","NOT(UA2013_NAM IN ( 'Rural (Incl.some Off Shore Islands)', 'Rural Centre', 'Oceanic', 'Oceanic-in Region but not in TA','Inland Water not in Urban Area'))")
#arcpy.SelectLayerByLocation_management("Urban","INTERSECT","Extent")
#arcpy.CopyFeatures_management("Urban",r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Urban_Area")
#arcpy.Delete_management("Urban")
    
print "\tParcels"
arcpy.AddMessage("\tParcels")
#arcpy.MakeFeatureLayer_management(r"Database Connections\DC GISSQL2012 GISuser.sde\GIS.DBO.VCADASTRAL_NZTM_PARCELS_VALUATION","Property")
arcpy.MakeFeatureLayer_management(r"Database Connections\DC GISSQL2012 LDS GISuser.sde\LDS.DBO.CADASTRAL_NZTM_PARCELS_VALUATION","Property")

arcpy.SelectLayerByLocation_management("Property","INTERSECT","Extent")
arcpy.SelectLayerByAttribute_management("Property","SUBSET_SELECTION","NOT(FEATCODE in ('Hydro', 'Railway', 'Road', 'Road Strata', 'Streambed'))")
arcpy.CopyFeatures_management("Property",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Int_Parcels")
arcpy.Clip_analysis(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Int_Parcels","Extent",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Parcels")

print "\tNon Parcels"
arcpy.AddMessage("\tNon Parcels")
arcpy.SelectLayerByAttribute_management("Property","NEW_SELECTION","FEATCODE in ('Hydro', 'Railway', 'Road', 'Road Strata', 'Streambed')")
arcpy.CopyFeatures_management("Property",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Int_Non_Parcels")
arcpy.Clip_analysis(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Int_Non_Parcels","Extent",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Non_Parcels")
                                                                                
arcpy.Delete_management("Property")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Int_Parcels")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Int_Non_Parcels")

print "\tWater Supply"
arcpy.AddMessage("\tWater Supply")

arcpy.MakeFeatureLayer_management(r"Database Connections\DC GISSQLEXT2012 GISWebuser.sde\GISPUBLIC.DBO.CLAGG_NZTM_WATER_SUPPLY","Water")
arcpy.SelectLayerByLocation_management("Water","INTERSECT","Extent","1000 METERS")
arcpy.CopyFeatures_management("Water",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Reticulation")
arcpy.Delete_management("Water")

print "\tLanduse"
arcpy.AddMessage("\tLanduse")
arcpy.MakeFeatureLayer_management(r"Database Connections\DC GISSQL2012 GISuser.sde\GIS.DBO.ASUREQUALITY_Agribase","Agribase")
arcpy.SelectLayerByLocation_management("Agribase","INTERSECT","Extent",selection_type="NEW_SELECTION")
arcpy.CopyFeatures_management("Agribase",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse")


#print "Removing Urban Areas....."
#arcpy.AddMessage("Removing Urban Areas....")
#arcpy.MakeFeatureLayer_management(r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Urban_Area","Urban")
#arcpy.Union_analysis([[r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Area_Extent",1],[r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Urban_Area",2]],r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Rural_Extent")
#arcpy.MakeFeatureLayer_management(r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Rural_Extent","Rural")
#arcpy.SelectLayerByAttribute_management("Rural","NEW_SELECTION","FID_Urban_Area <> -1")
#arcpy.DeleteFeatures_management("Rural")
#arcpy.Delete_management("Extent")
#arcpy.Delete_management("Urban")
#arcpy.Delete_management("Rural")


#if int(arcpy.GetCount_management(r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Rural_Extent").getOutput(0)) == 0:
    #arcpy.MakeFeatureLayer_management(r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Area_Extent","Extent")
#else:
    #arcpy.MakeFeatureLayer_management(r"C:\Temp\Hydrology\Permitted Takes\Scratch.gdb\Rural_Extent","Extent")


print "Removing Non Parcel Areas...."
arcpy.AddMessage("Removing Non Parcel Areas....")

arcpy.MakeFeatureLayer_management(docpath + "\Input\Data.gdb\Meshblocks2013","Mesh_Blocks")

arcpy.Clip_analysis("Mesh_Blocks","Extent",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Meshblocks2013")


arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Meshblocks2013","Mesh_Blocks2")
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Parcels","Property")
arcpy.Clip_analysis("Mesh_Blocks2","Property",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area")


arcpy.Delete_management("Mesh_Blocks")

print "Recalculating Meshblock Ratios..."
arcpy.AddMessage("Recalculating Meshblock Ratios...")


cursor = arcpy.da.UpdateCursor("Area",["SHAPE@AREA","POPULATION","DWELLINGS","DENSITY","PROPERTY_SQM"]) #"HUMAN_SQM",

for row in cursor:

    if row[2] <> None:
        prop = float(row[0]) * float(row[4])
        human = float(row[3]) * float(prop)
    else:
        prop = 0
        human = 0
        
    #human_ratio = round(row[1],0)/float(row[0])
    dwell_ratio = round(row[2],0)/float(row[0])
    
    cursor.updateRow([row[0],long(round(human,0)),long(round(prop,0)),row[3],dwell_ratio])


print "Removing Stock Water Networks...."
arcpy.AddMessage("Removing Stock Water Networks....")

arcpy.Intersect_analysis([[docpath + '\\' + "\Input\Stock Water Takes.gdb\NZTM_Stock_Water_Parcels",1],[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area",2]],r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area1")
arcpy.Union_analysis([[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area1",1],[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Non_Parcels",2]],r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area2")
arcpy.Union_analysis ([[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area2",1],[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area",2]],r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area3")
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area3","New_Area")
arcpy.SelectLayerByAttribute_management("New_Area","New_Selection","FID_Area2 <> -1")
arcpy.DeleteFeatures_management("New_Area")

arcpy.Delete_management("New_Area")

if arcpy.TestSchemaLock(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area"):
    arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area")

if arcpy.TestSchemaLock(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area1"):
    arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area1")
 


print "Removing Reticulated Areas...."
arcpy.AddMessage("Removing Reticulated Areas....")

arcpy.MakeFeatureLayer_management(r"Database Connections\DC GISSQL2012 LDS GISuser.sde\LDS.DBO.CADASTRAL_NZTM_Roads","Roads")
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Reticulation","Water")

arcpy.SelectLayerByLocation_management("Property","INTERSECT","Water",25,"NEW_SELECTION")
arcpy.SelectLayerByAttribute_management("Property","REMOVE_FROM_SELECTION","FEATCODE = 'road'")
arcpy.CopyFeatures_management("Property",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Property1")

arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Property1","Parcels_1")
arcpy.SelectLayerByLocation_management("Parcels_1","INTERSECT","Roads",0,"NEW_SELECTION")
arcpy.SelectLayerByLocation_management("Property","INTERSECT","Parcels_1",10,"NEW_SELECTION")
arcpy.SelectLayerByAttribute_management("Parcels_1","CLEAR_SELECTION")
arcpy.SelectLayerByLocation_management("Property","HAVE_THEIR_CENTER_IN","Parcels_1",selection_type="REMOVE_FROM_SELECTION")
arcpy.SelectLayerByAttribute_management("Property","REMOVE_FROM_SELECTION","FEATCODE = 'road'")


arcpy.CopyFeatures_management("Property",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Property2")
arcpy.Merge_management(["Property1","Property2"],r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Water_Supply_Parcels")

arcpy.Delete_management("Parcels_1")

arcpy.Intersect_analysis([[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Water_Supply_Parcels",1],[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area3",2]],r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area4")
arcpy.Union_analysis ([[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area4",1],[r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area3",2]],r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Non_Reticulated_Area")
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Non_Reticulated_Area","New_Area")
arcpy.SelectLayerByAttribute_management("New_Area","New_Selection","FID_Area4 <> -1")
arcpy.Rename_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area2", "Stock_Water_Area")

arcpy.DeleteFeatures_management("New_Area")

arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Stock_Water_Area","Stock_Water")
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Non_Reticulated_Area","Reticulated_Area")
fields = ["POPULATION","DWELLINGS","DENSITY","HUMAN_SQM","PROPERTY_SQM","ESTIMATED","SHAPE","Shape","OBJECTID","SHAPE_Length","SHAPE_Area","Shape_Length","Shape_Area"]
delfields = []

for f in arcpy.ListFields("Stock_Water"):
    if (str(f.name) in fields) == False:
        delfields.append(str(f.name))

arcpy.DeleteField_management("Stock_Water",delfields)
arcpy.Delete_management("Stock_Water")

delfields = []

for f in arcpy.ListFields("Reticulated_Area"):
    if (str(f.name) in fields) == False:
        delfields.append(str(f.name))

arcpy.DeleteField_management("Reticulated_Area",delfields)
arcpy.Delete_management("Reticulated_Area")

        
print "Calculating Human Population per Catchment not on Reticulation...."
arcpy.AddMessage("Calculating Human Population per Catchment not on Reticulation....")


arcpy.AddField_management("Extent","HUMAN_NO","Long")
arcpy.AddField_management("Extent","DENSITY","Float")
arcpy.AddField_management("Extent","PROPERTY_NO","Long")

arcpy.Clip_analysis("Mesh_Blocks2",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Non_Reticulated_Area",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Population")
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Population","Pop")



cursor = arcpy.da.UpdateCursor("Extent",["DENSITY","PROPERTY_NO"])

for row in cursor:
    dwell = 0
    #human = 0
    density = 0
    cnt = 0

    for srow in arcpy.da.SearchCursor("Pop",["SHAPE@AREA","DENSITY","PROPERTY_SQM"]):
        if srow[2] <> None:
            dwell = dwell + (float(srow[0]) * float(srow[2]))
            #human = human + ((float(srow[0]) * float(srow[2])) * float(srow[1]))

        if srow[1] <> None:
            density = density + float(srow[1])

        cnt = cnt + 1

    if cnt <> 0 :    
        avg_density = float(density/cnt)
    else:
        avg_density = 0

    cursor.updateRow([avg_density,long(round(dwell,0))])


arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Parcels")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Meshblocks2013")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Property1")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Property2")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area1")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area3")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Area4")

print "Processing Agribase Data ...."
arcpy.AddMessage("Processing Agribase Data ....")

arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse","Land_Use")
arcpy.Dissolve_management("Land_Use",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve_Int","FARM_ID;BEF_NOS;CAM_NOS;DAI_NOS;DEE_NOS;EMU_NOS;GOAT_NOS;HORS_NOS;OSTR_NOS;PIGS_NOS;POU_NOS;SHP_NOS","",
                          "SINGLE_PART")

arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve_Int","Land_Use2")
arcpy.SelectLayerByLocation_management("Land_Use2","INTERSECT","Extent","10 Kilometers","NEW_SELECTION")
arcpy.CopyFeatures_management("Land_Use2",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve_Int2")

arcpy.Dissolve_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve_Int2",r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve",
                          "FARM_ID;BEF_NOS;CAM_NOS;DAI_NOS;DEE_NOS;EMU_NOS;GOAT_NOS;HORS_NOS;OSTR_NOS;PIGS_NOS;POU_NOS;SHP_NOS","","MULTI_PART")

arcpy.Delete_management("Land_Use")
arcpy.Delete_management("Land_Use2")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve_Int")
arcpy.Delete_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve_Int2")

print "Calculating Weighted Animal Square Meter Ratio...."
arcpy.AddMessage("Calculating Weighted Animal Square Meter Ratio....")

arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve","Landuse_Dis")
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse_Dissolve","Landuse_Dis2")

arcpy.AddField_management("Landuse_Dis","BEF_SQM","Float")
arcpy.AddField_management("Landuse_Dis","DEE_SQM","Float")
arcpy.AddField_management("Landuse_Dis","DAI_SQM","Float")
arcpy.AddField_management("Landuse_Dis","SHP_SQM","Float")
arcpy.AddField_management("Landuse_Dis","PIG_SQM","Float")
arcpy.AddField_management("Landuse_Dis","GOAT_SQM","Float")
arcpy.AddField_management("Landuse_Dis","HORS_SQM","Float")
arcpy.AddField_management("Landuse_Dis","EMU_SQM","Float")
arcpy.AddField_management("Landuse_Dis","OSTR_SQM","Float")
arcpy.AddField_management("Landuse_Dis","CAM_SQM","Float")
arcpy.AddField_management("Landuse_Dis","POU_SQM","Float")

cursor = arcpy.da.UpdateCursor("Landuse_Dis",["FARM_ID","BEF_SQM","DEE_SQM","DAI_SQM","SHP_SQM","PIG_SQM","GOAT_SQM","HORS_SQM","EMU_SQM","OSTR_SQM","CAM_SQM","POU_SQM"])
previd = None


for row in cursor:
    if str(row[0]) <> previd: #Removes Duplicate Farm Properties
        previd2 = None
        area = 0.0
        befno = 0.0
        deeno = 0.0
        daino = 0.0
        shpno = 0.0
        pigno = 0.0
        goatno = 0.0
        horsno = 0.0
        emuno = 0.0
        ostno = 0.0
        camno = 0.0
        pouno = 0.0
        for srow in arcpy.da.SearchCursor("Landuse_Dis2",["SHAPE@AREA","BEF_NOS","DEE_NOS","DAI_NOS","SHP_NOS","PIGS_NOS","GOAT_NOS","HORS_NOS","EMU_NOS","OSTR_NOS","CAM_NOS","POU_NOS","FARM_ID"],"FARM_ID = '" + row[0] + "'"):
            if str(srow[12]) <> previd2: #Removes Duplicate Farm Properties when searching
                area = float(area + srow[0])
                befno = float(befno + srow[1])
                deeno = float(deeno + srow[2])
                daino = float(daino + srow[3])
                shpno = float(shpno + srow[4])
                pigno = float(pigno + srow[5])
                goatno = float(goatno + srow[6])
                horsno = float(horsno + srow[7])
                emuno = float(emuno + srow[8])
                ostno = float(ostno + srow[9])
                camno = float(camno + srow[10])
                pouno = float(pouno + srow[11])
                
                previd2 = str(srow[12])
                

        cursor.updateRow([row[0],float(befno/area),float(deeno/area),float(daino/area),float(shpno/area),float(pigno/area),float(goatno/area),float(horsno/area),float(emuno/area),float(ostno/area),float(camno/area),float(pouno/area)])
    else:
        cursor.updateRow([row[0],0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        
    previd = str(row[0])

arcpy.Intersect_analysis ([["Non_Reticulated_Area",1],["Landuse_Dis",2]], r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse")


arcpy.AddField_management("Extent","COW_NO","Long")
arcpy.AddField_management("Extent","DEER_NO","Long")
arcpy.AddField_management("Extent","DAIRY_NO","Long")
arcpy.AddField_management("Extent","SHEEP_NO","Long")
arcpy.AddField_management("Extent","PIGS_NO","Long")
arcpy.AddField_management("Extent","GOAT_NO","Long")
arcpy.AddField_management("Extent","HORS_NO","Long")
arcpy.AddField_management("Extent","EMU_NO","Long")
arcpy.AddField_management("Extent","OSTR_NO","Long")
arcpy.AddField_management("Extent","CAM_NO","Long")
arcpy.AddField_management("Extent","POU_NO","Long")
arcpy.AddField_management("Extent","WATER_USE_M3","Float")

cursor = arcpy.da.UpdateCursor("Extent",["COW_NO","DEER_NO","DAIRY_NO","SHEEP_NO","PIGS_NO","GOAT_NO","HORS_NO","EMU_NO","OSTR_NO","CAM_NO","POU_NO"])
arcpy.MakeFeatureLayer_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb\Landuse","Blocks")

for row in cursor:

    cow = 0
    deer = 0
    dairy = 0
    sheep = 0
    pig = 0
    goat = 0
    horse = 0
    emu = 0
    ostrich = 0
    camelid = 0
    poultry = 0

    previd = None

    for srow in arcpy.da.SearchCursor("Blocks",["SHAPE@AREA","BEF_SQM","DEE_SQM","DAI_SQM","SHP_SQM","PIG_SQM","GOAT_SQM","HORS_SQM","EMU_SQM","OSTR_SQM","CAM_SQM","POU_SQM","FARM_ID"]):

        if str(srow[12]) <> previd: #Reason: Duplicity occurs when farm is broken up into more than one parcel of land.

            cow = cow + float(srow[0]) * float(srow[1])
            deer  =  deer + float(srow[0]) * float(srow[2])
            dairy = dairy + float(srow[0]) * float(srow[3])
            sheep =  sheep + float(srow[0]) * float(srow[4])
            pig =  pig + float(srow[0]) * float(srow[5]) 
            goat = goat + float(srow[0]) * float(srow[6])
            horse = horse + float(srow[0]) * float(srow[7])
            emu = emu + float(srow[0]) * float(srow[8])
            ostrich = ostrich + float(srow[0]) * float(srow[9])
            camelid = camelid + float(srow[0]) * float(srow[10])
            poultry =  poultry + float(srow[0]) * float(srow[11])

        previd = str(srow[12])


    cursor.updateRow([cow,deer,dairy,sheep,pig,goat,horse,emu,ostrich,camelid,poultry])
            
        
    


print "Calculating Water Use per Catchment...."
arcpy.AddMessage("Calculating Water Use per Catchment....")

cursor = arcpy.da.UpdateCursor("Extent",["COW_NO","DAIRY_NO","DEER_NO","SHEEP_NO","PIGS_NO","GOAT_NO","HORS_NO","EMU_NO","OSTR_NO","CAM_NO","POU_NO",
                                       "HUMAN_NO","DENSITY","PROPERTY_NO","WATER_USE_M3"])

for row in cursor:
    use = (float((row[13] * row[12]) * DOMWU) + float(row[1] * DCWU) + float(row[0] * BFWU) + float(row[2] * DRWU) + float(row[3] * SHWU) +
        float(row[4] * PGWU) + float(row[5] * GTWU) + float(row[6] * HRWU) + float(row[7] * EUWU) + float(row[8] * OSWU) + float(row[9] * CMWU) + float(row[10] * POWU) + leakage)
    
    cursor.updateRow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],long(float(row[12]) * float(row[13])),row[12],row[13],float(use * 0.001)])

print "Exporting Results..."
arcpy.AddMessage("Exporting Results...")

arcpy.Copy_management(r"\\fs02\ManagedShares2\Data\Surface Water\shared\permitted_takes\Output\Hydrology\Permitted Takes\Scratch.gdb",output + "\\Permitted Takes Output " + str(strftime("%Y%m%d%H%M",localtime())) + ".gdb")

entry = open(output + "\\Permitted Takes Output " + str(strftime("%Y%m%d%H%M",localtime())) + ".csv","w")

entry.write("Estimated Population not on a Reticulated System or Stock Water Network\n")
entry.write("\n")
entry.write("User,Est. Population,Factor (Ltrs/head/day),Est. Total Water Use (m3/day)\n")

vals =  [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]] for row in
            arcpy.da.SearchCursor("Extent",["COW_NO","DAIRY_NO","DEER_NO","SHEEP_NO","PIGS_NO","GOAT_NO","HORS_NO","EMU_NO","OSTR_NO","CAM_NO","POU_NO","HUMAN_NO",
                                           "DENSITY","PROPERTY_NO","WATER_USE_M3"])]
if (len(vals)) == 0:
    val = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
else:
    val = vals[0]


entry.write("Humans*,"+ str(val[11]) + "," + str(DOMWU) + "," + str(float(((val[13] * val[12]) * DOMWU)* 0.001)) + "\n")
entry.write("Dairy Cattle," + str(val[1]) + "," + str(DCWU) + "," + str(float((val[1] * DCWU) * 0.001)) + "\n")
entry.write("Beef Cattle," + str(val[0]) + "," + str(BFWU) + "," + str(float((val[0] * BFWU) * 0.001)) + "\n")
entry.write("Sheep," + str(val[3]) + "," + str(SHWU) + "," + str(float((val[3] * SHWU) * 0.001)) + "\n")
entry.write("Deer," + str(val[2]) + "," + str(DRWU) + "," + str(float((val[2] * DRWU) * 0.001)) + "\n")
entry.write("Pigs," + str(val[4]) + "," + str(PGWU) + "," + str(float((val[4] * PGWU) * 0.001)) + "\n")
entry.write("Goats," + str(val[5]) + "," + str(GTWU) + "," + str(float((val[5] * GTWU) * 0.001)) + "\n")
entry.write("Horses," + str(val[6]) + "," + str(HRWU) + "," + str(float((val[6] * HRWU) * 0.001)) + "\n")
entry.write("Ostriches and Emus," + str(long(val[7] + val[8])) + "," + str(OSWU)  + "," + str(float((val[7] * EUWU) * 0.001) + float((val[8] * OSWU) * 0.001)) + "\n")
entry.write("Alpacas and Llamas," + str(val[9]) + "," + str(CMWU) + "," + str(float((val[9] * CMWU) * 0.001)) + "\n")
entry.write("Poultry," + str(val[10]) + "," + str(POWU) + "," + str(float((val[10] * POWU) * 0.001)) + "\n")
entry.write("\n")  
entry.write("Leakage,,," + str(leakage) + "\n")
entry.write("\n")
entry.write("TOTAL,,," + str(val[14]) + "\n")
entry.write("\n")
entry.write("* Based on average property-population density of "  + str(round(float(val[12]),3)) + "\n")
entry.write("Estimated Number of Properties (based on 2013 Census (Statistics NZ)) = "  + str(val[13]) + "\n")
entry.write("Estimated Stock Numbers based on data from Agribase (AsureQuality)\n")

entry.close()
            
arcpy.AddMessage("\nSummary report  saved  as " + output + "\\Permitted Takes Output " + str(strftime("%Y%m%d%H%M",localtime())) + ".csv\n" )


print "\nProcess Complete"
