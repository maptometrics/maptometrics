#   ----------------------------------------------------------------
#   Name:           DomainAssociationCheck.py
#   Created by:     Neil Rose
#   Created on:     6/24/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks domain association
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
sde_domain_list = []
fc_domain_list = []
orphan_domain_list = []
orphan_domain_count = 0

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('ReservedWordCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking reserved words
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_DomainAssociation_Check.txt'.format(conn_base)), 'w')

note('-------------------')
note('Reading SDE Domains')
note('-------------------')
domains = arcpy.da.ListDomains(conn_file)
for domain in domains:
    sde_domain_list.append(domain.name)

note('-------------------------------------------------------------------')
note('Checking the top level {0} features...'.format(os.path.basename(conn_base)))
note('-------------------------------------------------------------------')
for fc in sorted(arcpy.ListFeatureClasses()):
    note('Checking the {0} Feature Class...'.format(fc))
    fc_desc = arcpy.Describe(fc)
    for fn in (arcpy.ListFields(fc)):
        if fn.domain not in [None, '']:
            report_file.write('fc: {0} - '
                              'Feature Class: {1} - '
                              'Field Name: {2} '
                              'uses {3} domain.\n'.format(conn_base, fc, fn.name, fn.domain))

note('-------------------------------------------------------------------')
note('Checking the top level {0} tables...'.format(conn_base))
note('-------------------------------------------------------------------')
for tbl in sorted(arcpy.ListTables()):
    note('Checking the {0} Table...'.format(tbl))
    tbl_desc = arcpy.Describe(tbl)
    for fn in (arcpy.ListFields(tbl)):
        if fn.domain not in [None, '']:
            report_file.write('tbl: {0} - '
                              'Table: {1} - '
                              'Field Name: {2} '
                              'uses {3} domain.\n'.format(conn_base, tbl, fn.name, fn.domain))

datasets = sorted(arcpy.ListDatasets())
for ds in datasets:
    note('-------------------------------------------------------------------')
    note('Checking the {0} Feature Dataset...'.format(ds))
    note('-------------------------------------------------------------------')
    for fc in sorted(arcpy.ListFeatureClasses(feature_dataset=ds)):
        note('Checking the {0} Feature Class...'.format(fc))
        fc_desc = arcpy.Describe(fc)
        for fn in (arcpy.ListFields(fc)):
            if fn.domain not in [None, '']:
                report_file.write('fds: {0} - '
                                  'Feature Dataset: {1} - '
                                  'Feature Class: {2} - '
                                  'Field Name: {3} '
                                  'uses {4} domain.\n'.format(conn_base, ds, fc, fn.name, fn.domain))

report_file.close()
note('All fieldnames and domains have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('DomainAssociationCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
