import os
import re
import json
from .userop import UserOperation


class ManageData(UserOperation):

    def __init__(self, server, internal_server, userid, domain):
        super(ManageData, self).__init__(server, internal_server, userid, domain)
        self.dcdom = self.get_export_url() + "data/ontology.owl#"
        self.dclib = self.get_export_url() + "data/library.owl#"

    def get_type_id(self, typeid):
        if typeid == None:
            return 'http://www.wings-workflows.org/ontology/data.owl#DataObject'
        elif not re.match(r"(http:|https:)//", typeid):
            return self.dcdom + typeid
        else:
            return typeid

    def get_data_id(self, dataid):
        if not re.match(r"(http:|https:)//", dataid):
            return self.dclib + dataid
        else:
            return dataid

    def new_data_type(self, dtype, parent):
        parent = self.get_type_id(parent)
        dtype = self.get_type_id(dtype)
        postdata = {'parent_type': parent, 'data_type': dtype}
        self.session.post(self.get_request_url() +
                          'data/newDataType', postdata)

    def add_type_properties(self, dtype, properties):
        xsd = 'http://www.w3.org/2001/XMLSchema#'
        dtype = self.get_type_id(dtype)
        data = {'add': {}, 'del': {}, 'mod': {}}
        for pname in properties:
            pid = self.get_type_id(pname)
            prange = xsd + properties[pname]
            data['add'][pid] = {'prop': pname, 'pid': pid, 'range': prange}
        postdata = {'data_type': dtype, 'props_json': json.dumps(data)}
        self.session.post(self.get_request_url() +
                          'data/saveDataTypeJSON', postdata)

    def add_data_for_type(self, dataid, dtype):
        dtype = self.get_type_id(dtype)
        dataid = self.get_data_id(dataid)
        postdata = {'data_id': dataid, 'data_type': dtype}
        self.session.post(self.get_request_url() +
                          'data/addDataForType', postdata)

    def del_data_type(self, dtype):
        dtype = self.get_type_id(dtype)
        postdata = {'data_type': json.dumps([dtype]), 'del_children': 'true'}
        self.session.post(self.get_request_url() +
                          'data/delDataTypes', postdata)

    def del_data(self, dataid):
        dataid = self.get_data_id(dataid)
        postdata = {'data_id': dataid}
        self.session.post(self.get_request_url() + 'data/delData', postdata)

    def get_all_items(self):
        resp = self.session.get(
            self.get_request_url() + 'data/getDataHierarchyJSON')
        return resp.json()

    def get_data_description(self, dataid):
        dataid = self.get_data_id(dataid)
        postdata = {'data_id': dataid}
        resp = self.session.post(
            self.get_request_url() + 'data/getDataJSON', postdata)
        return resp.json()

    def get_datatype_description(self, dtype):
        dtype = self.get_type_id(dtype)
        postdata = {'data_type': dtype}
        resp = self.session.post(
            self.get_request_url() + 'data/getDataTypeJSON', postdata)
        return resp.json()

    def upload_data_for_type(self, filepath, dtype):
        dtype = self.get_type_id(dtype)
        fname = os.path.basename(filepath)
        files = {'file': (fname, open(filepath, 'rb'))}
        postdata = {'name': fname, 'type': 'data'}
        response = self.session.post(self.get_request_url() + 'upload',
                                     data=postdata, files=files)
        if response.status_code == 200:
            details = response.json()
            if details['success']:
                dataid = os.path.basename(details['location'])
                dataid = re.sub(r"(^\d.+$)", r"_\1", dataid)
                self.add_data_for_type(dataid, dtype)
                self.set_data_location(dataid, details['location'])
                return dataid

    def save_metadata(self, dataid, metadata):
        pvals = []
        for key in metadata:
            if(metadata[key]):
                pvals.append(
                    {'name': self.dcdom + key, 'value': metadata[key]})
        postdata = {'propvals_json': json.dumps(
            pvals), 'data_id': self.get_data_id(dataid)}
        self.session.post(self.get_request_url() +
                          'data/saveDataJSON', postdata)

    def set_data_location(self, dataid, location):
        postdata = {'data_id': self.get_data_id(dataid), 'location': location}
        self.session.post(self.get_request_url() +
                          'data/setDataLocation', postdata)
