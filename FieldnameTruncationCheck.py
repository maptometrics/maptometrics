#   ----------------------------------------------------------------
#   Name:           FieldnameTruncationCheck.py
#   Created by:     Neil Rose
#   Created on:     4/28/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks whether fieldnames will be
#                   truncated
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
arcpy.env.overwriteOutput = True

#   Set inputs
conn_file = arcpy.GetParameterAsText(0)
conn_base = os.path.basename(conn_file)
report_loc = arcpy.GetParameterAsText(1)

#   Global variables
fn_count = 0
fn_errors = 0

ignore_list = ['OID', 'ObjectID', 'OBJECTID', 'ATTACHMENTID', 'REL_OBJECTID', 'CONTENT_TYPE', 'ATT_NAME', 'DATA_SIZE',
               'DATA', 'GlobalID', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date', 'Creator',
               'Create_Date', 'Editor', 'Edit_Date', 'compress_id', 'sde_id', 'server_id',
               'direct_connect', 'compress_start', 'start_state_count', 'compress_end', 'end_state_count',
               'compress_status', 'Shape', 'Shape.STArea()', 'Shape.STLength()', 'SHAPE', 'SHAPE.STArea()',
               'SHAPE.STLength()', 'EditDate', 'CreateDate']


#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('FieldnameTruncationCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking reserved words
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_FieldnameTruncation_Check.txt'.format(conn_base)), 'w')

note('-------------------------------------------------------------------')
note('Checking the top level {0} features...'.format(os.path.basename(conn_base)))
note('-------------------------------------------------------------------')
for fc in sorted(arcpy.ListFeatureClasses()):
    note('Checking the {0} Feature Class.'.format(fc))
    for fn in (arcpy.ListFields(fc)):
        fn_count += 1
        if len(fn.name) > 10 and fn.name not in ignore_list:
            fn_errors += 1
            report_file.write('fc: {0} - '
                              'Feature Class: {1} - '
                              'Field Name: {2} will be truncated.\n'.format(conn_base, fc, fn.name))

note('-------------------------------------------------------------------')
note('Checking the top level {0} tables...'.format(conn_base))
note('-------------------------------------------------------------------')
for tbl in sorted(arcpy.ListTables()):
    note('Checking the {0} Table.'.format(tbl))
    for fn in (arcpy.ListFields(tbl)):
        fn_count += 1
        if len(fn.name) > 10 and fn.name not in ignore_list:
            fn_errors += 1
            report_file.write('tbl: {0} - '
                              'Table: {1} - '
                              'Field Name: {2} will be truncated.\n'.format(conn_base, tbl, fn.name))

datasets = sorted(arcpy.ListDatasets())
for ds in datasets:
    note('-------------------------------------------------------------------')
    note('Checking the {0} Feature Dataset...'.format(ds))
    note('-------------------------------------------------------------------')
    for fc in sorted(arcpy.ListFeatureClasses(feature_dataset=ds)):
        note('Checking the {0} Feature Class.'.format(fc))
        for fn in (arcpy.ListFields(fc)):
            fn_count += 1
            if len(fn.name) > 10 and fn.name not in ignore_list:
                fn_errors += 1
                report_file.write('fds: {0} - '
                                  'Feature Dataset: {1} - '
                                  'Feature Class: {2} - '
                                  'Field Name: {3} will be truncated.\n'.format(conn_base, ds, fc, fn.name))

report_file.write('\n\nField Name Truncation Issues: {0}\n'
                  'Field Name Count: {1}\n'
                  'Percent Truncation Issues: {2}%'.format(str(fn_errors), str(fn_count), str(round((fn_errors/fn_count)*100, 2))))

report_file.close()
note('All field names have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('FieldnameTruncationCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
