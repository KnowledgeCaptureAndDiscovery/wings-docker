import sys
import csv
import wings.data

server = 'http://www.wings-workflows.org/wings-omics-portal'
#server = 'http://ontosoft.isi.edu:8080/wings-portal'
#server = 'http://varuns-mbp.local:9090/wings-portal'
#userid = 'admin'
#password = 'admin123'
#password = '4dm1n!23'
#password = 'admin123'
#domain = 'OpenCV'
userid = 'ravali'
password = 'ravali123'
domain = 'genomics'

# Create manage data api
data = wings.ManageData(server, userid, domain)

# Login with password
data.login(password)

with open(sys.argv[1], 'rb') as csvfile:
	fdata = csv.reader(csvfile)
	for row in fdata:
		rnafile = row[0]
		msfile = row[1]
		sampleid = row[2]
		patientid = row[3]
		data.save_metadata(rnafile, {'hasSpeciesName': 'HS', 'hasParticipantID': patientid, 'hasSampleID': sampleid, 'hasDatasetID': 'COADREAD'});
		data.save_metadata(msfile, {'hasSpeciesName': 'HS', 'hasParticipantID': patientid, 'hasSampleID': sampleid, 'hasDatasetID': 'COADREAD'});
		print ':%s a bio:Patient' % patientid
		#print ':%s bio:isDiagnosedWith bio:ColonCancer' % patientid
		#print ':%s a bio:Sample' % sampleid
		#print ':%s bio:collectedFrom :%s' % (sampleid, patientid)
		#print ':E1_%s a bio:Experiment' % sampleid
		#print ':E1_%s bio:producedData :%s' % (sampleid, msfile)
		#print ':E1_%s bio:experimentedOn :%s' % (sampleid, sampleid)
		#print ':%s a bio:MassSpecData' % msfile
		#print ':E2_%s a bio:Experiment' % sampleid
		#print ':E2_%s bio:producedData :%s' % (sampleid, rnafile)
		#print ':E2_%s bio:experimentedOn :%s' % (sampleid, sampleid)
		#print ':%s a bio:RNASeq' %rnafile


# Add New DataType (type name, parentType name)
#data.new_data_type('TestType', None)
# Define DataType properties
#data.add_type_properties('TestType', {'hasProperty1': 'int', 'hasProperty2': 'string'})

# Upload data for type
#data.upload_data_for_type('/Users/varun/Desktop/learth.ttl', 'TestType')
# Add data item (if data is already uploaded using other means)
#data.add_data_for_type('DummyData', 'TestType')
# Set data location
#data.set_data_location('DummyData', '/Users/varun/Desktop/learth.ttl')

# Save data metadata
#data.save_metadata('DummyData', {'hasProperty1': 10, 'hasProperty2': 'Some text'})

# Delete data
#data.del_data('DummyData')

# Delete data type (and all its subtypes and data contained within)
#data.del_data_type('TestType')

#print data.get_all_items()
#print data.get_datatype_description("Image")
#print data.get_data_description("usalogo")

# Logout
data.logout()
