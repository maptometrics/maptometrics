#   ----------------------------------------------------------------
#   Name:           ReservedWordCheck.py
#   Created by:     Neil Rose
#   Created on:     4/28/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks reserved words
#   ----------------------------------------------------------------

#   import modules
import arcpy
import datetime
import os
import time
from ReservedWords import sql_rsv, altibase_rsv, dameng_rsv, \
    db2_rsv, oracle_rsv, postgressql_rsv, sap_hana_rsv, teradata_rsv


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
db_type = arcpy.GetParameterAsText(1)
report_loc = arcpy.GetParameterAsText(2)

#   Global variables
fn_count = 0
fn_errors = 0
#   Reserve dictionary
rsv_dict = {'SQL': sql_rsv, 'ALTIBASE': altibase_rsv, 'Dameng': dameng_rsv, 'DB2': db2_rsv, 'Oracle': oracle_rsv,
            'PostgresSQL': postgressql_rsv, 'SAP HANA': sap_hana_rsv, 'Teradata': teradata_rsv, 'ESRI GDB': sql_rsv}

for k, v in rsv_dict.items():
    if k == db_type:
        rsv_list = v

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('ReservedWordCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking reserved words
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_{1}_Check.txt'.format(conn_base, db_type)), 'w')

note('-------------------------------------------------------------------')
note('Checking the top level {0} features...'.format(os.path.basename(conn_base)))
note('-------------------------------------------------------------------')
for fc in sorted(arcpy.ListFeatureClasses()):
    note('Checking the {0} Feature Class.'.format(fc))
    for fn in (arcpy.ListFields(fc)):
        fn_count += 1
        if fn.name.upper() in rsv_list:
            fn_errors += 1
            report_file.write('fc: {0} - '
                              'Feature Class: {1} - '
                              'Field Name: {2} '
                              'is a {3} Reserved Word.\n'.format(conn_base, fc, fn.name, db_type))

note('-------------------------------------------------------------------')
note('Checking the top level {0} tables...'.format(conn_base))
note('-------------------------------------------------------------------')
for tbl in sorted(arcpy.ListTables()):
    note('Checking the {0} Table.'.format(tbl))
    for fn in (arcpy.ListFields(tbl)):
        fn_count += 1
        if fn.name.upper() in rsv_list:
            fn_errors += 1
            report_file.write('tbl: {0} - '
                              'Table: {1} - '
                              'Field Name: {2} '
                              'is a {3} Reserved Word.\n'.format(conn_base, tbl, fn.name, db_type))

datasets = sorted(arcpy.ListDatasets())
for ds in datasets:
    note('-------------------------------------------------------------------')
    note('Checking the {0} Feature Dataset...'.format(ds))
    note('-------------------------------------------------------------------')
    for fc in sorted(arcpy.ListFeatureClasses(feature_dataset=ds)):
        note('Checking the {0} Feature Class.'.format(fc))
        for fn in (arcpy.ListFields(fc)):
            fn_count += 1
            if fn.name.upper() in rsv_list:
                fn_errors += 1
                report_file.write('fds: {0} - '
                                  'Feature Dataset: {1} - '
                                  'Feature Class: {2} - '
                                  'Field Name: {3} '
                                  'is a {4} Reserved Word.\n'.format(conn_base, ds, fc, fn.name, db_type))

report_file.write('\n\nField Name Reserved Word Errors: {0}\n'
                  'Field Name Count: {1}\n'
                  'Percent Reserved Word Error: {2}%'.format(str(fn_errors), str(fn_count), str(round((fn_errors/fn_count)*100, 2))))

report_file.close()
note('All field names have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('ReservedWordCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
