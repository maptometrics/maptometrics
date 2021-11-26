#   ----------------------------------------------------------------
#   Name:           DomainDictionary.py
#   Created by:     Neil Rose
#   Created on:     5/6/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that generates a domain dictionary
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
domain_count = 0

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('DomainDictionary.py beginning at {0}...'.format(str(start_time)))
#   Begin domains and domain values
arcpy.env.workspace = conn_file

report_file = open(os.path.join(report_loc, '{0}_Domain_Dictionary.txt'.format(conn_base)), 'w')

note('-------------------')
note('Reading SDE Domains')
note('-------------------')
domains = arcpy.da.ListDomains(conn_file)

for domain in domains:
    note('Reading/writing the {0} domain.'.format(domain.name))
    domain_count += 1
    report_file.write('________________________________________\n')
    report_file.write('Domain name: {0}\n'.format(domain.name))
    if domain.domainType == 'CodedValue':
        coded_values = domain.codedValues
        for val, desc in coded_values.items():
            report_file.write('{0} : {1}\n'.format(str(val), str(desc)))
    elif domain.domainType == 'Range':
        report_file.write('Range: {0} - {1}\n'.format(domain.range[0], domain.range[1]))

report_file.write('\n\n{0} has {1} domains.'.format(conn_base, domain_count))

report_file.close()

note('All domains and domain values have been recorded. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('DomainDictionary.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
