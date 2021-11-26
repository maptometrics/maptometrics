#   ----------------------------------------------------------------
#   Name:           DomainDuplicationCheck.py
#   Created by:     Neil Rose
#   Created on:     6/4/2021
#   Modified by:
#   Modified on:
#   Description:    Tool that checks for duplicated domain errors
#   ----------------------------------------------------------------

#   import modules
import arcpy
import datetime
import os
import re
import sys
import time


#   defined functions
#   Function for creating output messages
def note(message):
    return arcpy.AddMessage(str(message))


#   Function to create an empty file geodatabase for transitionary data management
def new_fgdb():
    try:
        arcpy.CreateFileGDB_management(report_loc, 'domains.gdb')
        note('domains.gdb file geodatabase has been created...')
    except IOError as e:
        errno, strerror = e.args
        note('I/O Error({0}): {1}'.format(errno, strerror))
        sys.exit(note('Ending script...'))


#   Function to create a table to store the appended domain tables
def new_tbl():
    new_tbl = arcpy.CreateTable_management(fgdb_domains, 'tbl_of_domains')
    note('Empty tbl_of_domains has been generated...')
    arcpy.AddField_management(new_tbl, 'domCode', 'TEXT', 255)
    arcpy.AddField_management(new_tbl, 'domDesc', 'TEXT', 255)
    arcpy.AddField_management(new_tbl, 'domName', 'TEXT', 255)
    note('New fields have been added to tbl_domains...')


#   Function to list through all domain tables and append them to tbl_of_domains
def list_append():
    arcpy.env.workspace = fgdb_domains
    tables = arcpy.ListTables()
    for table in tables:
        if table != 'tbl_of_domains':
            arcpy.Append_management(table, os.path.join(fgdb_domains, 'tbl_of_domains'), 'NO_TEST')
            arcpy.Delete_management(table)
    note('All domain tables have been appened to tbl_of_domains...')


#   Find and compile identical domain descriptions
def identical_desc():
    tbl_in = os.path.join(fgdb_domains, 'tbl_of_domains')
    fields = ['domDesc']
    tbl_out = os.path.join(fgdb_domains, 'tbl_of_identicals')
    arcpy.FindIdentical_management(tbl_in, tbl_out, fields, '', '', 'ONLY_DUPLICATES')
    note('Duplicate domain descriptions have been identified and compiled...')


#   Find and delete non-identical records in tbl_of_domains
def del_nonidentical():
    identical_list = []
    identical_tbl = os.path.join(fgdb_domains, 'tbl_of_identicals')
    identical_fields = ['IN_FID']
    with arcpy.da.SearchCursor(identical_tbl, identical_fields) as sCursor:
        for sRow in sCursor:
            identical_list.append(sRow[0])
    domain_tbl = os.path.join(fgdb_domains, 'tbl_of_domains')
    domain_fields = ['OBJECTID']
    with arcpy.da.UpdateCursor(domain_tbl, domain_fields) as uCursor:
        for uRow in uCursor:
            if uRow[0] not in identical_list:
                uCursor.deleteRow()
    note('Non-identical records have been removed from tbl_of_domains...')


#   Create mutlivalue dictionary to compile domain description : domain name
def desc_domain_sort():
    note('Building identical description dictionary...')
    duplicate_dict = {}
    domain_tbl = os.path.join(fgdb_domains, 'tbl_of_domains')
    domain_fields = ['domDesc', 'domName']
    with arcpy.da.SearchCursor(domain_tbl, domain_fields) as cursor:
        for row in cursor:
            if row[0] in duplicate_dict:
                duplicate_dict[row[0]].append(row[1])
            else:
                duplicate_dict[row[0]] = [row[1]]
    #   Write values to text
    duplicate_count = 0
    desc_count = 0
    report_file = open(os.path.join(report_loc, '{0}_DomainDuplication_Check.txt'.format(conn_base)), 'w')
    for k, v in duplicate_dict.items():
        desc_count += 1
        duplicate_count += len(v)
        report_file.write('Domain description {0} exists in the following domains {1}\n'.format(k, v))

    report_file.write('\n\nDuplicate Domain Errors: {0}\n'
                      'Duplicate Domain Count: {1}\n'
                      'Percent Duplicate Domain Error: {2}%'.format(str(duplicate_count), str(desc_count), str(round((duplicate_count / desc_count) * 100, 2))))
    report_file.close()


#   Set environments
arcpy.env.overwriteOutput = True

#   Set inputs
conn_file = arcpy.GetParameterAsText(0)
conn_base = os.path.basename(conn_file)
report_loc = arcpy.GetParameterAsText(1)

#   Global variables
fgdb_domains = os.path.join(report_loc, 'domains.gdb')

#   Main script
#   Start timer
start = time.time()
start_time = datetime.datetime.today().time()
note('DomainDuplicationCheck.py beginning at {0}...'.format(str(start_time)))
#   Create empty FGDB
new_fgdb()
#   Begin domains and domain values
arcpy.env.workspace = conn_file

note('------------------------------')
note('Reading and Converting Domains')
note('------------------------------')
domains = arcpy.da.ListDomains(conn_file)

if len(domains) == 0:
    note('This database has no domains...')
    sys.exit(note('Ending script...'))

for domain in domains:
    if domain.domainType == 'CodedValue':
        note('Reading and converting the {0} domain.'.format(domain.name))
        domain_name_clean = re.sub("[^0-9a-zA-Z]+", "_", domain.name)
        out_tbl = os.path.join(fgdb_domains, 'tbl_{0}'.format(domain_name_clean))
        arcpy.DomainToTable_management(conn_file, domain.name, out_tbl, 'domCode', 'domDesc')
        arcpy.AddField_management(out_tbl, 'domName', 'TEXT', 255)
        expression = "'{0}'".format(domain.name)
        arcpy.CalculateField_management(out_tbl, 'domName', expression, 'PYTHON3')

#   Create a table to append all domain tables to
note('------------------------------------')
note('Appending and Deleting Domain Tables')
note('------------------------------------')
new_tbl()
list_append()

#   Find and report identical domain descriptions
note('-----------------------------------------')
note('Identifying Identical Domain Descriptions')
note('-----------------------------------------')
identical_desc()
del_nonidentical()
desc_domain_sort()

#   Find and report identical domain descriptions
note('----------------------------------')
note('Deleting Transitionary Geodatabase')
note('----------------------------------')
arcpy.Delete_management(fgdb_domains)

note('All domain duplications have been analyzed. Please see results in the generated txt file.')
#   End timer
end = time.time()
end_time = datetime.datetime.today().time()
#   Timer math
note('DomainDuplicationCheck.py completed at {0}...'.format(str(end_time)))
note('It took {0} minutes to complete...'.format(str(round(((end - start)/60), 4))))
