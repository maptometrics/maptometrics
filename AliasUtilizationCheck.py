#   ----------------------------------------------------------------
#   Name:           AliasUtilizationCheck.py
#   Created by:     Neil Rose
#   Created on:     4/28/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks alias usage
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
ignore_list = ['OID', 'ObjectID', 'OBJECTID', 'ATTACHMENTID', 'REL_OBJECTID', 'CONTENT_TYPE', 'ATT_NAME', 'DATA_SIZE',
               'DATA', 'GlobalID', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date', 'Creator',
               'Create_Date', 'Editor', 'Edit_Date', 'compress_id', 'sde_id', 'server_id',
               'direct_connect', 'compress_start', 'start_state_count', 'compress_end', 'end_state_count',
               'compress_status', 'Shape', 'Shape.STArea()', 'Shape.STLength()', 'SHAPE', 'SHAPE.STArea()',
               'SHAPE.STLength()', 'EditDate', 'CreateDate']

fc_count = 0
fc_errors = 0
tbl_count = 0
tbl_errors = 0
fn_count = 0
fn_errors = 0

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('ReservedWordCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking reserved words
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_Alias_Check.txt'.format(conn_base)), 'w')
report_file.write('Due to naming conventions, there may be false positives in Alias Utilization.\n')
report_file.write('Certain field names have been ignored in this check Please check the script to review them.\n\n\n')

note('-------------------------------------------------------------------')
note('Checking the top level {0} features...'.format(os.path.basename(conn_base)))
note('-------------------------------------------------------------------')
for fc in sorted(arcpy.ListFeatureClasses()):
    note('Checking the {0} Feature Class.'.format(fc))
    fc_desc = arcpy.Describe(fc)
    fc_count += 1
    if fc_desc.name == fc_desc.aliasName:
        report_file.write('fc: {0} - Feature Class Name: {1} matches Alias Name.\n'.format(conn_base, fc))
        fc_errors += 1
    for fn in (arcpy.ListFields(fc)):
        fn_count += 1
        if fn.name == fn.aliasName and fn.name not in ignore_list:
            fn_errors += 1
            report_file.write('fc: {0} - '
                              'Feature Class: {1} - '
                              'Field Name: {2} matches Alias Name.\n'.format(conn_base, fc, fn.name))

note('-------------------------------------------------------------------')
note('Checking the top level {0} tables...'.format(conn_base))
note('-------------------------------------------------------------------')
for tbl in sorted(arcpy.ListTables()):
    note('Checking the {0} Table.'.format(tbl))
    tbl_count += 1
    tbl_desc = arcpy.Describe(tbl)
    if tbl_desc.name == tbl_desc.aliasName:
        tbl_errors += 1
        report_file.write('tbl: {0} - Table Name: {1} matches Alias Name.\n'.format(conn_base, tbl))
    for fn in (arcpy.ListFields(tbl)):
        fn_count += 1
        if fn.name == fn.aliasName and fn.name not in ignore_list:
            fn_errors += 1
            report_file.write('tbl: {0} - '
                              'Table: {1} - '
                              'Field Name: {2} matches Alias Name.\n'.format(conn_base, tbl, fn.name))

datasets = sorted(arcpy.ListDatasets())
for ds in datasets:
    note('-------------------------------------------------------------------')
    note('Checking the {0} Feature Dataset...'.format(ds))
    note('-------------------------------------------------------------------')
    for fc in sorted(arcpy.ListFeatureClasses(feature_dataset=ds)):
        note('Checking the {0} Feature Class.'.format(fc))
        fc_count += 1
        fc_desc = arcpy.Describe(fc)
        if fc_desc.name == fc_desc.aliasName:
            fc_errors += 1
            report_file.write('fc: {0} - Feature Class Name: {1} matches Alias Name.\n'.format(conn_base, fc))
        for fn in (arcpy.ListFields(fc)):
            fn_count += 1
            if fn.name == fn.aliasName and fn.name not in ignore_list:
                fn_errors += 1
                report_file.write('fds: {0} - '
                                  'Feature Dataset: {1} - '
                                  'Feature Class: {2} - '
                                  'Field Name: {3} matches Alias Name.\n'.format(conn_base, ds, fc, fn.name))

report_file.write('\n\nFeature Class Alias Errors: {0}\n'
                  'Feature Class Count: {1}\n'
                  'Percent Alias Error: {2}%\n\n'.format(str(fc_errors), str(fc_count), str(round((fc_errors/fc_count)*100, 2))))

report_file.write('Table Alias Errors: {0}\n'
                  'Table Count: {1}\n'
                  'Percent Alias Error: {2}%\n\n'.format(str(tbl_errors), str(tbl_count), str(round((tbl_errors/tbl_count)*100, 2))))

report_file.write('Field Name Alias Errors: {0}\n'
                  'Field Name Count: {1}\n'
                  'Percent Alias Error: {2}%'.format(str(fn_errors), str(fn_count), str(round((fn_errors/fn_count)*100, 2))))

report_file.close()
note('All aliases have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('AliasUtilizationCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
