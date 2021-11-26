#   ----------------------------------------------------------------
#   Name:           OrphanDomainCheck.py
#   Created by:     Neil Rose
#   Created on:     4/28/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that reports orphaned domains
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
note('OrphanDomainCheck.py beginning at {0}...'.format(str(start_time)))
#   Begin checking reserved words
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_OrphanDomains_Check.txt'.format(conn_base)), 'w')

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
            fc_domain_list.append(fn.domain)

note('-------------------------------------------------------------------')
note('Checking the top level {0} tables...'.format(conn_base))
note('-------------------------------------------------------------------')
for tbl in sorted(arcpy.ListTables()):
    note('Checking the {0} Table...'.format(tbl))
    tbl_desc = arcpy.Describe(tbl)
    for fn in (arcpy.ListFields(tbl)):
        if fn.domain not in [None, '']:
            fc_domain_list.append(fn.domain)

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
                fc_domain_list.append(fn.domain)

note('----------------------------------------------')
note('Comparing GDB Domain list to FC Domain list...')
note('----------------------------------------------')

for domain in sde_domain_list:
    if domain not in fc_domain_list:
        orphan_domain_list.append(domain)
        orphan_domain_count += 1

sde_domain_count = len(sde_domain_list)

for domain in orphan_domain_list:
    report_file.write('{0} is an orphan domain\n'.format(domain))


report_file.write('\n\nOrphaned Domains Errors: {0}\n'
                  'SDE Domain Count: {1}\n'
                  'Percent Orphan Error: {2}%\n\n'.format(str(orphan_domain_count),
                                                          str(sde_domain_count),
                                                          str(round((orphan_domain_count/sde_domain_count)*100, 2))))


report_file.close()
note('All domains have been verified. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('OrphanDomainCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
