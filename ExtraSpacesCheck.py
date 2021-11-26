#   ----------------------------------------------------------------
#   Name:           ExtraSpacesCheck.py
#   Created by:     Neil Rose
#   Created on:     6/29/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks whether a field has any
#                   spurious leading, internal, or trailing spaces
#   ----------------------------------------------------------------

#   import modules
import arcpy
import datetime
import os
import re
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
error_count = 0

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('ExtraSpacesCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking reserved words
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_ExtraSpaces_Check.txt'.format(conn_base)), 'w')

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
                if type(row[row_counter]) == str:
                    if row[row_counter] != re.sub(' +', ' ', row[row_counter]):
                        tfc_oid_list.append(row[0])
                        error_count += 1
                row_counter += 1
        tfc_oid_errors = set(tfc_oid_list)
        for oid in tfc_oid_errors:
            report_file.write('fc - {0} - OID {1} contains extra whitespace\n'.format(fc, oid))

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
        tfc_oid_list = []
        for row in cursor:
            field_len = len(fields)
            row_counter = 0
            while row_counter < field_len:
                if type(row[row_counter]) == str:
                    if row[row_counter] != re.sub(' +', ' ', row[row_counter]):
                        tfc_oid_list.append(row[0])
                        error_count += 1
                row_counter += 1
        tfc_oid_errors = set(tfc_oid_list)
        for oid in tfc_oid_errors:
            report_file.write('tbl - {0} - OID {1} contains extra whitespace\n'.format(tbl, oid))

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
            tfc_oid_list = []
            for row in cursor:
                field_len = len(fields)
                row_counter = 0
                while row_counter < field_len:
                    if type(row[row_counter]) == str:
                        if row[row_counter] != re.sub(' +', ' ', row[row_counter]):
                            tfc_oid_list.append(row[0])
                            error_count += 1
                    row_counter += 1
            tfc_oid_errors = set(tfc_oid_list)
            for oid in tfc_oid_errors:
                report_file.write('fc - {0} - OID {1} contains extra whitespace\n'.format(fc, oid))

report_file.write('\n\nExtra Spaces Instances: {0}\n'.format(error_count))

report_file.close()
note('All attributes have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('ExtraSpacesCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
