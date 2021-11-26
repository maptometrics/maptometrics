#   ----------------------------------------------------------------
#   Name:           MetadataCheck.py
#   Created by:     Neil Rose
#   Created on:     5/28/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks metadata for feature classes
#   ----------------------------------------------------------------

#   import modules
import arcpy
from arcpy import metadata as md
import datetime
import os
import time


#   defined functions
#   Function for creating output messages
def note(message):
    return arcpy.AddMessage(str(message))


#   Set environments
arcpy.env.overwriteOutput = True

#   Set inputs
conn_file = arcpy.GetParameterAsText(0)
conn_base = os.path.basename(conn_file)
report_loc = arcpy.GetParameterAsText(1)

#   Global variables
empty_list = [None, '', ' ']
md_count = 0
md_errors = 0

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('MetadataCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking metadata
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_Metadata_Check.txt'.format(conn_base)), 'w')

report_file.write('MetadataCheck tool reviews the Title, Tags, Summary, and Credits fields of metadata.\n')
report_file.write('If any field is missing, the feature class or table will be flagged as having errors.\n\n\n')

note('-------------------------------------------------------------------')
note('Checking the top level {0} features...'.format(os.path.basename(conn_base)))
note('-------------------------------------------------------------------')
for fc in sorted(arcpy.ListFeatureClasses()):
    fc_errors = 0
    item_md = md.Metadata(fc)
    md_count += 4
    note('Checking the {0} Feature Class.'.format(fc))
    if item_md.title == os.path.basename(fc) or item_md.title in empty_list:
        md_errors += 1
        fc_errors += 1
    if item_md.tags in empty_list:
        md_errors += 1
        fc_errors += 1
    if item_md.summary in empty_list:
        md_errors += 1
        fc_errors += 1
    if item_md.credits in empty_list:
        md_errors += 1
        fc_errors += 1
    if fc_errors > 0:
        report_file.write('fc: {0} - '
                          'Feature Class: {1} - '
                          'There are metadata errors.\n'.format(conn_base, fc))
    else:
        report_file.write('fc: {0} - '
                          'Feature Class: {1} - '
                          'Metadata is complete.\n'.format(conn_base, fc))

note('-------------------------------------------------------------------')
note('Checking the top level {0} tables...'.format(conn_base))
note('-------------------------------------------------------------------')
for tbl in sorted(arcpy.ListTables()):
    tbl_errors = 0
    item_md = md.Metadata(tbl)
    md_count += 4
    note('Checking the {0} Table.'.format(tbl))
    if item_md.title == os.path.basename(tbl) or item_md.title in empty_list:
        md_errors += 1
        tbl_errors += 1
    if item_md.tags in empty_list:
        md_errors += 1
        tbl_errors += 1
    if item_md.summary in empty_list:
        md_errors += 1
        tbl_errors += 1
    if item_md.credits in empty_list:
        md_errors += 1
        tbl_errors += 1
    if tbl_errors > 0:
        report_file.write('tbl: {0} - '
                          'Table: {1} - '
                          'There are metadata errors.\n'.format(conn_base, tbl))
    else:
        report_file.write('tbl: {0} - '
                          'Table: {1} - '
                          'Metadata is complete.\n'.format(conn_base, tbl))

datasets = sorted(arcpy.ListDatasets())
for ds in datasets:
    note('-------------------------------------------------------------------')
    note('Checking the {0} Feature Dataset...'.format(ds))
    note('-------------------------------------------------------------------')
    for fc in sorted(arcpy.ListFeatureClasses(feature_dataset=ds)):
        fc_errors = 0
        item_md = md.Metadata(fc)
        md_count += 4
        note('Checking the {0} Feature Class.'.format(fc))
        if item_md.title == os.path.basename(fc) or item_md.title in empty_list:
            md_errors += 1
            fc_errors += 1
        if item_md.tags in empty_list:
            md_errors += 1
            fc_errors += 1
        if item_md.summary in empty_list:
            md_errors += 1
            fc_errors += 1
        if item_md.credits in empty_list:
            md_errors += 1
            fc_errors += 1
        if fc_errors > 0:
            report_file.write('fc: {0} - '
                              'Feature Class: {1} - '
                              'There are metadata errors.\n'.format(conn_base, fc))
        else:
            report_file.write('fc: {0} - '
                              'Feature Class: {1} - '
                              'Metadata is complete.\n'.format(conn_base, fc))

report_file.write('\n\nMetadata Input Issues: {0}\n'
                  'Metadata Field Count: {1}\n'
                  'Percent Metadata Issues: {2}%'.format(str(md_errors), str(md_count), str(round((md_errors/md_count)*100, 2))))

report_file.close()
note('All feature class and table metadata has been checked. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('MetadataCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
