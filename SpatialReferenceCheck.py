#   ----------------------------------------------------------------
#   Name:           SpatialReferenceCheck.py
#   Created by:     Neil Rose
#   Created on:     5/3/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks all feature classes for
#                   spatial reference
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
wkt_srs = arcpy.GetParameterAsText(2)
base_srs = arcpy.SpatialReference()
base_srs.loadFromString(wkt_srs)

#   Set global lists
srs_list = []

fc_count = 0
fc_errors = 0

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('SpatialReferenceCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking spatial reference systems
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_SRS_Check.txt'.format(conn_base)), 'w')

note('-------------------------------------------------------------------')
note('Checking the top level {0} features...'.format(os.path.basename(conn_base)))
note('-------------------------------------------------------------------')
for fc in sorted(arcpy.ListFeatureClasses()):
    fc_count += 1
    note('Checking the {0} Feature Class.'.format(fc))
    srs = arcpy.Describe(fc).spatialReference.name
    srs_list.append(srs)
    if wkt_srs not in [None, '', ' ']:
        if srs != base_srs.name:
            fc_errors += 1
            report_file.write('fc: {0} - '
                              'Feature Class: {1} - '
                              'SRS: {2} does not match input\n'.format(conn_base, fc, srs))

datasets = sorted(arcpy.ListDatasets())
for ds in datasets:
    note('-------------------------------------------------------------------')
    note('Checking the {0} Feature Dataset...'.format(ds))
    note('-------------------------------------------------------------------')
    for fc in sorted(arcpy.ListFeatureClasses(feature_dataset=ds)):
        fc_count += 1
        note('Checking the {0} Feature Class.'.format(fc))
        srs = arcpy.Describe(fc).spatialReference.name
        srs_list.append(srs)
        if wkt_srs not in [None, '', ' ']:
            if srs != base_srs.name:
                fc_errors += 1
                report_file.write('fds: {0} - '
                                  'Feature Dataset: {1} - '
                                  'Feature Class: {2} - '
                                  'SRS: {2} does not match input\n'.format(conn_base, ds, fc, srs))

unique_srs = set(srs_list)

for srs in unique_srs:
    report_file.write('There are {0} instances of {1}\n'.format(srs_list.count(srs), srs))

if wkt_srs not in [None, '', ' ']:
    report_file.write('\n\nFeature Class SRS Errors: {0}\n'
                      'Feature Class Count: {1}\n'
                      'Percent SRS Error: {2}%'.format(str(fc_errors), str(fc_count), str(round((fc_errors/fc_count)*100, 2))))

report_file.close()
note('All spatial reference systems have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('SpatialReferenceCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
