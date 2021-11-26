#   ----------------------------------------------------------------
#   Name:           NullBlankCheck.py
#   Created by:     Neil Rose
#   Created on:     6/29/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks whether a field uses NULL or
#                   a blank for no attribute data
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
var_check = arcpy.GetParameterAsText(2)
if var_check == 'Blank':
    if_type = ''
    var_type = 'Blank'
else:
    if_type = None
    var_type = 'Null'


#   Global variables
error_count = 0

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('NullBlankCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking reserved words
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_{1}_Check.txt'.format(conn_base, var_type)), 'w')

note('-------------------------------------------------------------------')
note('Checking the top level {0} features...'.format(os.path.basename(conn_base)))
note('-------------------------------------------------------------------')
for fc in sorted(arcpy.ListFeatureClasses()):
    note('Checking the {0} Feature Class.'.format(fc))
    field_list = arcpy.ListFields(fc)
    fields = []
    for field in field_list:
        fields.append(field.name)
    with arcpy.da.SearchCursor(fc, fields) as cursor:
        tfc_oid_list = []
        for row in cursor:
            field_len = len(fields)
            row_counter = 0
            while row_counter < field_len:
                if row[row_counter] == if_type:
                    tfc_oid_list.append(row[0])
                    error_count += 1
                row_counter += 1
        tfc_oid_errors = set(tfc_oid_list)
        for oid in tfc_oid_errors:
            report_file.write('fc - {0} - OID {1} contains 1 or more {2} values\n'.format(fc, oid, var_type))

note('-------------------------------------------------------------------')
note('Checking the top level {0} tables...'.format(conn_base))
note('-------------------------------------------------------------------')
for tbl in sorted(arcpy.ListTables()):
    note('Checking the {0} Table.'.format(tbl))
    field_list = arcpy.ListFields(tbl)
    fields = []
    for field in field_list:
        fields.append(field.name)
    with arcpy.da.SearchCursor(tbl, fields) as cursor:
        tbl_oid_list = []
        for row in cursor:
            field_len = len(fields)
            row_counter = 0
            while row_counter < field_len:
                if row[row_counter] == if_type:
                    tbl_oid_list.append(row[0])
                    error_count += 1
                row_counter += 1
        tbl_oid_errors = set(tbl_oid_list)
        for oid in tbl_oid_errors:
            report_file.write('fc - {0} - OID {1} contains 1 or more {2} values\n'.format(tbl, oid, var_type))

datasets = sorted(arcpy.ListDatasets())
for ds in datasets:
    note('-------------------------------------------------------------------')
    note('Checking the {0} Feature Dataset...'.format(ds))
    note('-------------------------------------------------------------------')
    for fc in sorted(arcpy.ListFeatureClasses(feature_dataset=ds)):
        note('Checking the {0} Feature Class.'.format(fc))
        field_list = arcpy.ListFields(fc)
        fields = []
        for field in field_list:
            fields.append(field.name)
        with arcpy.da.SearchCursor(fc, fields) as cursor:
            fc_oid_list = []
            for row in cursor:
                field_len = len(fields)
                row_counter = 0
                while row_counter < field_len:
                    if row[row_counter] == if_type:
                        fc_oid_list.append(row[0])
                        error_count += 1
                    row_counter += 1
            fc_oid_errors = set(fc_oid_list)
            for oid in fc_oid_errors:
                report_file.write('fc - {0} - OID {1} contains 1 or more {2} values\n'.format(fc, oid, var_type))

report_file.write('\n\n{0} Instances: {1}\n'.format(var_type, error_count))

report_file.close()
note('All attributes have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('NullBlankCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
