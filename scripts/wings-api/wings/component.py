import os
import re
import json
from .userop import UserOperation


class ManageComponent(UserOperation):

    def __init__(self, server, internal_server, userid, domain):
        super(ManageComponent, self).__init__(server, internal_server, userid, domain)
        self.libns = self.get_export_url() + "components/library.owl#"
        self.dcdom = self.get_export_url() + "data/ontology.owl#"
        self.xsdns = "http://www.w3.org/2001/XMLSchema#"
        self.topcls = "http://www.wings-workflows.org/ontology/component.owl#Component"

    def get_type_id(self, typeid):
        if typeid == "":
            return self.topcls
        elif not re.match(r"(http:|https:)//", typeid):
            return self.libns + typeid + "Class";
        else:
            return typeid + "Class";

    def get_component_id(self, compid):
        if compid == None:
            return ""
        elif not re.match(r"(http:|https:)//", compid):
            return self.libns + compid
        else:
            return compid

    def new_component_type(self, ctype, parent):
        ptype = self.get_component_id(parent)
        ctype = self.get_component_id(ctype)
        pcls = self.get_type_id(ptype);
        postdata = {'parent_cid': ptype, 'parent_type': pcls,
                    'cid': ctype, 'load_concrete': "false"}
        self.session.post(self.get_request_url() +
                          'components/type/addComponent', postdata)

    def new_component(self, cid, parent):
        pid = self.get_component_id(parent)
        cid = self.get_component_id(cid)
        pcls = self.get_type_id(pid)
        postdata = {'parent_cid': pid, 'parent_type': pcls,
                    'cid': cid, 'load_concrete': "true"}
        self.session.post(self.get_request_url() +
                          'components/addComponent', postdata)

    def del_component_type(self, ctype):
        ctype = self.get_component_id(ctype)
        postdata = {'cid': ctype}
        self.session.post(self.get_request_url() +
                          'components/type/delComponent', postdata)

    def del_component(self, cid):
        cid = self.get_component_id(cid)
        postdata = {'cid': cid}
        self.session.post(self.get_request_url() +
                          'components/delComponent', postdata)

    def get_all_items(self):
        resp = self.session.get(
            self.get_request_url() + 'components/getComponentHierarchyJSON')
        return resp.json()

    def get_component_description(self, cid):
        cid = self.get_component_id(cid)
        postdata = {'cid': cid}
        resp = self.session.get(
            self.get_request_url() + 'components/getComponentJSON', params=postdata)
        return resp.json()

    def get_component_type_description(self, ctype):
        ctype = self.get_type_id(ctype)
        postdata = {'cid': ctype, 'load_concrete': False}
        resp = self.session.get(
            self.get_request_url() + 'components/type/getComponentJSON', params=postdata)
        return resp.json()

    def _modify_component_json(self, cid, jsonobj):
        for input in jsonobj["inputs"]:
            input["type"] = input["type"].replace("xsd:", self.xsdns)
            input["type"] = input["type"].replace("dcdom:", self.dcdom)
            input["id"] = cid + "_" + input["role"]
        for output in jsonobj["outputs"]:
            output["type"] = output["type"].replace("xsd:", self.xsdns)
            output["type"] = output["type"].replace("dcdom:", self.dcdom)
            output["id"] = cid + "_" + output["role"]
        jsonobj["id"] = cid
        return jsonobj

    def save_component(self, cid, jsonobj):
        cid = self.get_component_id(cid);
        jsonobj = self._modify_component_json(cid, jsonobj)
        jsonobj["type"] = 2
        postdata = {'component_json': json.dumps(jsonobj), 'cid': cid}
        self.session.post(self.get_request_url() +
                          'components/saveComponentJSON', postdata)

    def save_component_type(self, ctype, jsonobj):
        ctype = self.get_type_id(ctype);
        jsonobj = self._modify_component_json(ctype, jsonobj)
        jsonobj["type"] = 1
        postdata = {'component_json': json.dumps(jsonobj), 'cid': ctype,
                    'load_concrete': False}
        self.session.post(self.get_request_url() +
                          'components/type/saveComponentJSON', postdata)

    def upload_component(self, filepath, cid):
        cid = self.get_component_id(cid)
        fname = os.path.basename(filepath)
        files = {"file": (fname, open(filepath, "rb"))}
        postdata = {"name": fname, "type": "component", "id": cid}
        response = self.session.post(
            self.get_request_url() + "upload", data=postdata, files=files
        )
        if response.status_code == 200:
            details = response.json()
            if details["success"]:
                loc = os.path.basename(details["location"])
                self.set_component_location(cid, details["location"])
                return loc
            
    def set_component_location(self, cid, location):
        postdata = {'cid': self.get_component_id(cid), 'location': location}
        self.session.post(self.get_request_url() +
                          'components/setComponentLocation', postdata)
