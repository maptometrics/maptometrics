#   ----------------------------------------------------------------
#   Name:           EmptyDataCheckCheck.py
#   Created by:     Neil Rose
#   Created on:     5/3/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks for empty datasets
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
prj_dir = r'{0}\GIS\SystemsArchitecture\DataAudit2021\DataAuditTools\Dependencies'
arcpy.env.workspace = prj_dir
arcpy.env.overwriteOutput = True

#   Set inputs
conn_file = arcpy.GetParameterAsText(0)
conn_base = os.path.basename(conn_file)
report_loc = arcpy.GetParameterAsText(1)

#   Set global lists
fc_count = 0
fc_errors = 0
tbl_count = 0
tbl_errors = 0

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('SpatialReferenceCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking spatial reference systems
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_EmptyData_Check.txt'.format(conn_base)), 'w')

note('-------------------------------------------------------------------')
note('Checking the top level {0} features...'.format(os.path.basename(conn_base)))
note('-------------------------------------------------------------------')
for fc in sorted(arcpy.ListFeatureClasses()):
    fc_count += 1
    note('Checking the {0} Feature Class...'.format(fc))
    results = arcpy.GetCount_management(fc)[0]
    if int(results) < 1:
        fc_errors += 1
        report_file.write('fc: {0} - Feature Class: {1} contains no data.\n'.format(conn_base, fc))

note('-------------------------------------------------------------------')
note('Checking the top level {0} tables...'.format(conn_base))
note('-------------------------------------------------------------------')
for tbl in sorted(arcpy.ListTables()):
    tbl_count += 1
    note('Checking the {0} Feature Class...'.format(tbl))
    results = arcpy.GetCount_management(tbl)[0]
    if int(results) < 1:
        tbl_errors += 1
        report_file.write('tbl: {0} - Table: {1} contains no data.\n'.format(conn_base, tbl))

datasets = sorted(arcpy.ListDatasets())
for ds in datasets:
    note('-------------------------------------------------------------------')
    note('Checking the {0} Feature Dataset...'.format(ds))
    note('-------------------------------------------------------------------')
    for fc in sorted(arcpy.ListFeatureClasses(feature_dataset=ds)):
        fc_count += 1
        note('Checking the {0} Feature Class...'.format(fc))
        results = arcpy.GetCount_management(fc)[0]
        if int(results) < 1:
            fc_errors += 1
            report_file.write('fds: {0} - Feature Dataset: {1} - Feature Class: {2} contains no data.\n'.format(conn_base, ds, fc))

report_file.write('\n\nFeature Classes With No Data: {0}\n'
                  'Feature Class Count: {1}\n'
                  'Percent Empty Feature Classes: {2}%\n\n'.format(str(fc_errors), str(fc_count), str(round((fc_errors/fc_count)*100, 2))))

report_file.write('Tables With No Data: {0}\n'
                  'Table Count: {1}\n'
                  'Percent Empty Tables: {2}%\n\n'.format(str(tbl_errors), str(tbl_count), str(round((tbl_errors/tbl_count)*100, 2))))

report_file.close()
note('All datasets have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('EmptyDataCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
