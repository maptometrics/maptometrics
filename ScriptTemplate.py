#   ----------------------------------------------------------------
#   Name:           ScriptName.py
#   Created by:     YourName
#   Created on:     CreateDate
#   Modified by:    ModDate
#   Modified on:    ModName
#   Description:    Tool that updates GIS from Cityworks SQL
#   ----------------------------------------------------------------

#   import modules
import arcpy
import datetime
import os
import time


#   defined functions
#   Function for creating output messages
def note(message):
    return arcpy.AddMessage(str(message))


#   Set environments
unc_path = "//app-gisdata/gisdata/"
prj_dir = 'project location'
arcpy.env.workspace = prj_dir
arcpy.env.overwriteOutput = True

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('ScriptName beginning at {0}...'.format(str(start_time)))
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('ScriptName completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
