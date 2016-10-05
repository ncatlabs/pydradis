#####################################################################################
#                  Pydradis: Python API Wrapper for Dradis                          #
#                       Copyright (c) 2016 Novacoast                                #
#                           Dev : Pedro M. Sosa                                     #
#####################################################################################
# This file is part of Pydradis.                                                    #
#                                                                                   #
#     Pydradis is free software: you can redistribute it and/or modify              #
#     it under the terms of the GNU Lesser General Public License as published by   #
#     the Free Software Foundation, either version 3 of the License, or             #
#     (at your option) any later version.                                           #
#                                                                                   #
#     Pydradis is distributed in the hope that it will be useful,                   #
#     but WITHOUT ANY WARRANTY; without even the implied warranty of                #
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 #
#     GNU Lesser General Public License for more details.                           #
#                                                                                   #
#     You should have received a copy of the GNU Lesser General Public License      #
#     along with Pydradis.  If not, see <http://www.gnu.org/licenses/>.             #
#####################################################################################


#NOTE#
#There is a lot of repeated code. Since Dradis is still developing their API
# I decided to keep every call separate in case the Dradis API eventually gives us
# further parameters or allow for more intricacies for each call.

import requests
import string
import json

class Pydradis:

    #End Nodes#
    client_endpoint = "/pro/api/clients"
    project_endpoint = "/pro/api/projects"
    node_endpoint = "/pro/api/nodes"
    issue_endpoint = "/pro/api/issues"
    evidence_endpoint = "/pro/api/nodes/<ID>/evidence"
    note_endpoint = "/pro/api/nodes/<ID>/notes" 



    #Constructor
    def __init__(self, apiToken,url,debug=False,verify=True):
        self.__apiToken = apiToken  #API Token 
        self.__url = url            #Dradis URL (eg. https://your_dradis_server.com)
        self.__debug = debug        #Debuging True?
        self.__verify = verify      #Path to SSL certificate


    def debug(self,val):
        self.__debug = val;

    #Send Requests to Dradis (& Debug + Check for Error Codes)
    def contactDradis(self,url,header,reqType,response_code,data=""):
        

        r = 0;

        if (reqType == "GET"):
            r = requests.get(url,headers=header,verify=self.__verify);
        elif (reqType == "POST"):
            r = requests.post(url,headers=header,data=data,verify=self.__verify);
        elif (reqType == "PUT"):
            r = requests.put(url,headers=header,data=data,verify=self.__verify);
        elif (reqType == "DELETE"):
            r = requests.delete(url,headers=header,verify=self.__verify);
        else:
            raise ValueError("Request Type must be GET, POST, PUT or DELETE");
            return None;

        if (self.__debug):
            print("\nServer Response:\n")
            print(r.status_code)
            print("---\n")
            print(r.content)


        if (str(r.status_code) != str(response_code)):
            return None;

        return r.json();

    ####################################
    #         Clients Endpoint         # <P>
    ####################################

    #Get Client List 
    def get_clientlist(self):
        #URL
        url = self.__url+self.client_endpoint;

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Content-type': 'application/json'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        result = [];
        for i in range(0,len(r)):
            result += [[r[i]["name"],r[i]["id"]]]

        return result;

    #Create Client 
    def create_client(self,client_name):
        
        #URL
        url = self.__url+self.client_endpoint
        
        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Content-type': 'application/json'}
        
        #DATA
        data = {"client":{"name":client_name}}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"POST","201",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id'] 

    #Update Client 
    def update_client(self,client_id,new_client_name):
        
        #URL
        url = self.__url+self.client_endpoint+"/"+str(client_id)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Content-type': 'application/json'}
        
        #DATA
        data = {"client":{"name":new_client_name}}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"PUT","200",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id']      

    #Delete Client 
    def delete_client(self,client_id):

        #URL
        url = self.__url+self.client_endpoint+"/"+str(client_id)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"'}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"DELETE","200");

        #RETURN
        if (r == None):
            return None;

        return True;

    #Search For Client 
    def find_client(self,name):
        
        #URL
        url = self.__url+self.client_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Content-type': 'application/json'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        result = [];
        for i in range(0,len(r)):
            if (r[i]["name"] == name):
                return r[i]["id"];
        
        return None;

    #Get Client Info 
    def get_client(self,client_id):

        #URL
        url = self.__url+self.client_endpoint+"/"+str(client_id);

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Content-type': 'application/json'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;
        
        return r;


    ####################################
    #         Projects Endpoint        # <P>
    ####################################

    #Get Project List 
    def get_projectlist(self):

        #URL
        url = self.__url+self.project_endpoint

        #DATA
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        result = [];
        for i in range(0,len(r)):
            result += [[r[i]["name"],r[i]["id"]]]

        return result;

    #Create Project 
    def create_project(self,project_name,client_id=None):
        
        #URL
        url = self.__url+self.project_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Content-type': 'application/json'}
        
        #DATA
        data = {"project":{"name":project_name}}
        if (client_id != None):
            data = {"project":{"name":project_name,"client_id":str(client_id)}}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"POST","201",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id'] 

    #Update Project 
    def update_project(self,pid,new_project_name,new_client_id=None):
        
        #URL
        url = self.__url+self.project_endpoint+"/"+str(pid)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Content-type': 'application/json'}
        
        #DATA
        data = {"project":{"name":new_project_name}}
        if (new_client_id != None):
            data = {"project":{"name":new_project_name,"client_id":str(new_client_id)}}
        

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"PUT","200",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id']     

    #Delete Project 
    def delete_project(self,pid):
        
        #URL
        url = self.__url+self.project_endpoint+"/"+str(pid)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"'}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"DELETE","200");

        #RETURN
        if (r == None):
            return None;

        return True;

    #Search For Project 
    def find_project(self,name):
        
        #URL
        url = self.__url+self.project_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        result = [];
        for i in range(0,len(r)):
            if (r[i]["name"] == name):
                return r[i]["id"];
        
        return None;

    #Get Project Info 
    def get_project(self,pid):

        #URL
        url = self.__url+self.project_endpoint+"/"+str(pid)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;
        
        return r;


    ####################################
    #         Nodes Endpoint           # <P>
    ####################################

    #Get Node List 
    def get_nodelist(self,pid):
        
        #URL
        url = self.__url+self.node_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        result = [];
        for i in range(0,len(r)):
            result += [[r[i]["label"],r[i]["id"]]]

        return result;

    #Create Node 
    def create_node(self,pid,label,type_id=0,parent_id=None,position=1):

        #URL
        url = self.__url+self.node_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}
        
        #DATA
        if (parent_id != None): #If None (Meaning its a toplevel node) then dont convert None to string.
            parent_id = str(parent_id);
        data = {"node":{"label":label, "type_id":str(type_id), "parent_id":parent_id, "position": str(position)}}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"POST","201",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id'] 

    #Update Node 
    def update_node(self,pid,node_id,label=None,type_id=None,parent_id=None,position=None):
        
        #URL
        url = self.__url+self.node_endpoint+"/"+str(node_id);

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #DATA (notice this time we are building a str not a dict)
        if (label==type_id==parent_id==position==None):
            return None;        

        data = '{"node":{'
        if (label != None):
            data += '"label":"'+label+'"'
        if (type_id != None):
            data += ',"type_id":"'+str(type_id)+'"'
        if (parent_id != None):
            data += ',"parent_id":"'+str(parent_id)+'"'
        if (position != None):
            data += ',"position":"'+str(position)+'"'
        data += "}}"


        #CONTACT DRADIS
        r = self.contactDradis(url,header,"PUT","200",data)
        
        #RETURN
        if (r == None):
            return None;

        return r['id']  

    #Delete Node 
    def delete_node(self,pid,node_id):

        #URL
        url = self.__url+self.node_endpoint+"/"+str(node_id)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"DELETE","200");

        #RETURN
        if (r == None):
            return None;

        return True;

    #Find Node  :: Given a nodepath (e.g ac/dc/r) return the node id. (these change between projects) 
    def find_node(self,pid,nodepath):

        #URL
        url = self.__url+self.node_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        #Finding packet by traversing tree structure.
        nodepath = nodepath.split("/");
        #print nodepath
        parent_id = None;
        for node in nodepath:
            for i in range(0,len(r)):
                found = False
                #print "checking",r[i]["label"],"-- Wanting",node
                if ((r[i]["label"] == node) and (r[i]["parent_id"] == parent_id)):
                    # if (self.__debug):
                    #     print "Found:", node, r[i]["id"];
                    #print "Found:",node,r[i]["id"]
                    parent_id = r[i]["id"];
                    found = True
                    break;

            if (not found):
                return None;

        # if (self.__debug):
        #     print "Your node is:",parent_id;

        return parent_id;

    #Get Node Info 
    def get_node(self,pid,node_id):

        #URL
        url = self.__url+self.node_endpoint+"/"+str(node_id)
        
        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;
        
        return r;


    ####################################
    #         Issues Endpoint          # <P>
    ####################################

    #Get Issue List 
    def get_issuelist(self,pid):
        
        #URL
        url = self.__url+self.issue_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        result = [];
        for i in range(0,len(r)):
            result += [[r[i]["title"],r[i]["id"]]]

        return result;

    #Create Issue on Project 
    def create_issue(self,pid,title,text,tags=[]):

        #URL
        url = self.__url+self.issue_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #DATA
        taglines = ""
        if (len(tags) != 0):
            for t in tags:
                taglines+= "#["+t + "]#\r\n"

        data = { 'issue':{'text':'#[Title]#\r\n'+title+'\r\n\r\n#[Description]#\r\n'+str(text)+"\r\n\r\n"+taglines}}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"POST","201",json.dumps(data))

        #RETURN
        if (r == None):
            return None;

        return r['id'];

    #Update Issue 
    def update_issue(self,pid,issue_id,title,text,tags=[]):
        
        #URL
        url = self.__url+self.issue_endpoint+"/"+str(issue_id)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"', 'Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #DATA
        taglines = ""
        if (len(tags) != 0):
            for t in tags:
                taglines+= "#["+t + "]#\r\n"    

        data = { 'issue':{'text':'#[Title]#\r\n'+title+'\r\n\r\n#[Description]#\r\n'+str(text)+"\r\n\r\n"+taglines}}


        #CONTACT DRADIS
        r = self.contactDradis(url,header,"PUT","200",json.dumps(data));

        #RETURN
        if (r == None):
            return None;

        return r['id'];

    #Delete Issue 
    def delete_issue(self,pid,issue_id):
        
        #URL
        url = self.__url+self.issue_endpoint+"/"+str(issue_id)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"DELETE","200");

        #RETURN
        if (r == None):
            return None;

        return True;

    #Find Issue 
    def find_issue(self,pid,keywords):
        
        #URL
        url = self.__url+self.issue_endpoint

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        #Give people the option to just input a string.
        if (type(keywords)==str):
            keywords = [keywords];

        result = [];
        for i in range(0,len(r)):
            str1 = string.upper(r[i]["text"]);
            for k in keywords:
                str2 = string.upper(k);
                if (str1.find(str2) != -1):
                    result += [[r[i]["title"],r[i]["id"]]]
                    break;

        return result;

    #Get Issue (with issue_id) 
    def get_issue(self,pid,issue_id):

        #URL
        url = self.__url+self.issue_endpoint+"/"+str(issue_id)

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        return r;

    ####################################
    #         Evidence Endpoint        # <?>
    ####################################

    #Get Evidence List 
    def get_evidencelist(self,pid,node_id):

        #URL
        url = self.__url+self.evidence_endpoint.replace("<ID>",str(node_id));

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        return r;

    #Create Evidence 
    def create_evidence(self,pid,node_id,issue_id,title,text,tags=[]):

        #URL
        url = self.__url+self.evidence_endpoint.replace("<ID>",str(node_id));

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #DATA
        taglines = ""
        if (len(tags) != 0):
            for t in tags:
                taglines+= "#["+t + "]#\r\n"

        #DATA
        data = { 'evidence':{'content':'#[Title]#\r\n'+title+'\r\n\r\n#[Description]#\r\n'+str(text)+"\r\n\r\n"+taglines,"issue_id":str(issue_id)}}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"POST","201",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id'];

    #Update Evidence 
    def update_evidence(self,pid,node_id,issue_id,evidence_id,title,text,tags=[]):

        #URL
        url = self.__url+self.evidence_endpoint.replace("<ID>",str(node_id))+"/"+str(evidence_id);

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #DATA
        taglines = ""
        if (len(tags) != 0):
            for t in tags:
                taglines+= "#["+t + "]#\r\n"

        data = { 'evidence':{'content':'#[Title]#\r\n'+title+'\r\n\r\n#[Description]#\r\n'+str(text)+"\r\n\r\n"+taglines,"issue_id":str(issue_id)}}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"PUT","200",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id'];

    #Delete Evidence 
    def delete_evidence(self,pid,node_id,evidence_id):

        #URL
        url = self.__url+self.evidence_endpoint.replace("<ID>",str(node_id))+"/"+str(evidence_id);

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"DELETE","200");

        #RETURN
        if (r == None):
            return None;

        return True;

    #Find Evidence 
    def find_evidence(self,pid,node_id,keywords):

        #URL
        url = self.__url+self.evidence_endpoint.replace("<ID>",str(node_id));

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        #Give people the option to just input a string.
        if (type(keywords)==str):
            keywords = [keywords];

        result = [];
        for i in range(0,len(r)):
            str1 = string.upper(r[i]["content"]);
            for k in keywords:
                str2 = string.upper(k);
                if (str1.find(str2) != -1):
                    result += [r[i]]
                    break;

        return result;

    #Get Evidence Info 
    def get_evidence(self,pid,node_id,evidence_id):

        #URL
        url = self.__url+self.evidence_endpoint.replace("<ID>",str(node_id))+"/"+str(evidence_id);

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        return r;


    ####################################
    #         Notes Endpoint           # <?>
    ####################################


    #Get Note List 
    def get_notelist(self,pid,node_id):

        #URL
        url = self.__url+self.note_endpoint.replace("<ID>",str(node_id));

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        result = [];
        for i in range(0,len(r)):
            result += [[r[i]["title"],r[i]["id"]]]

        return result;

    #Create a note on a project 
    def create_note(self,pid,node_id,title,text,tags=[],category=0):
        
        #URL
        url = self.__url+self.note_endpoint.replace("<ID>",str(node_id));

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #DATA
        taglines = ""
        if (len(tags) != 0):
            for t in tags:
                taglines+= "#["+t + "]#\r\n"

        data = { 'note':{'text':'#[Title]#\r\n'+title+'\r\n\r\n#[Description]#\r\n'+str(text)+"\r\n\r\n"+taglines,"category_id":str(category)}}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"POST","201",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id'];

    #Update Note 
    def update_note(self,pid,node_id,note_id,title,text,tags=[],category=1):

        #URL
        url = self.__url+self.note_endpoint.replace("<ID>",str(node_id))+"/"+str(note_id);

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #DATA
        taglines = ""
        if (len(tags) != 0):
            for t in tags:
                taglines+= "#["+t + "]#\r\n"

        data = { 'note':{'text':'#[Title]#\r\n'+title+'\r\n\r\n#[Description]#\r\n'+str(text)+"\r\n\r\n"+taglines,"category_id":str(category)}}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"PUT","200",json.dumps(data))
        
        #RETURN
        if (r == None):
            return None;

        return r['id'];

    #Delete Note 
    def delete_note(self,pid,node_id,note_id):

        #URL
        url = self.__url+self.note_endpoint.replace("<ID>",str(node_id))+"/"+str(note_id);

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid), 'Content-type': 'application/json'}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"DELETE","200");

        #RETURN
        if (r == None):
            return None;

        return True;

    #Find Note 
    def find_note(self,pid,node_id,keywords):
        
        #URL
        url = self.__url+self.note_endpoint.replace("<ID>",str(node_id));

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}

        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        #Give people the option to just input a string.
        if (type(keywords)==str):
            keywords = [keywords];

        result = [];
        for i in range(0,len(r)):
            str1 = string.upper(r[i]["text"]);
            for k in keywords:
                str2 = string.upper(k);
                if (str1.find(str2) != -1):
                    result += [[r[i]["title"],r[i]["id"]]]
                    break;


        return result;

    #Get Note Info 
    def get_note(self,pid,node_id,note_id):

        #URL
        url = self.__url+self.note_endpoint.replace("<ID>",str(node_id))+"/"+str(note_id);

        #HEADER
        header = { 'Authorization' : 'Token token="'+self.__apiToken+'"','Dradis-Project-Id': str(pid)}
        
        #CONTACT DRADIS
        r = self.contactDradis(url,header,"GET","200")

        #RETURN
        if (r == None):
            return None;

        return r;











