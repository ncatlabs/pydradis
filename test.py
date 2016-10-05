#####################################################################################
#                  Pydradis: Python API Wrapper for Dradis                          #
#                       Copyright (c) 2016 Novacoast                                #
#                            Dev : Pedro M. Sosa                                    #
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

#BUGS FOUND ON DRADIS (as of July 2016)
#1. Nodes Endpoint: IMPORTANT: WHEN CREATING NODES YOU CAN PUT THEM WITH ANY PARENT ID (Negative numbers and non-existant nodes)
#2. Issues Endpoint: No way to change or set an issue's rating.
#3. Note Endpoint: Cant update a note with category=0. (Can create it with category = 0 however)


#An Example Usage Test for Pydradis.py

from pydradis import Pydradis

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if __name__ == "__main__":

    print("Testing PyDradis!")
    
    pd = Pydradis("<DRADIS API KEY>","<DRADIS SERVER URL>",False,False)


    #Client
    print("\n<CLIENT ENDPOINT>")

    print("--Get Clients"),
    if (pd.get_clientlist() != None): print("PASS")
    else: print("FAILED")
    
    print("--Create Client"),
    clientid = pd.create_client("Test V.1")
    if (clientid != None): print("PASS")
    else: print("FAILED")
    
    print("--Update Client"),
    if (pd.update_client(clientid,"Test V.1 - MOD")==clientid): print("PASS")
    else: print("FAILED")
    
    print("--Find Client"),
    if (pd.find_client("Test V.1 - MOD") == clientid): print("PASS")
    else: print("FAILED")


    print("--Get Client"),
    if (str(pd.get_client(clientid)["id"]) == str(clientid)): print("PASS")
    else: print("FAILED")

    #raw_input("\nYou can take this moment to manually inspect Dradis :). Then press enter to continue test...\n")



    #Project
    print("\n<PROJECT ENDPOINT>");

    print("--Get Projects"),
    if (pd.get_projectlist() != None): print("PASS")
    else: print("FAILED")

    print("--Create Project"),
    projectid = pd.create_project("Project T",clientid);
    if (projectid != None): print("PASS")
    else: print("FAILED")

    print("--Update Project"),
    if (pd.update_project(projectid,"Project T - Mod",clientid) == projectid): print("PASS")
    else: print("FAILED")

    print("--Find Project"),
    if (pd.find_project("Project T - Mod") == projectid): print("PASS")
    else: print("FAILED")

    print("--Get Project"),
    if (str(pd.get_project(projectid)["id"]) == str(projectid)): print("PASS")
    else: print("FAILED")

    #raw_input("\nYou can take this moment to manually inspect Dradis :). Then press enter to continue test...\n")



    #Nodes
    print("\n<NODE ENDPOINT>")

    print("--Get Nodes"),
    if (pd.get_nodelist(projectid) != None): print("PASS")
    else: print("FAILED")

    print("--Create Node"),
    nodeid = pd.create_node(projectid,"T",0,None,1);
    nodeid2 = pd.create_node(projectid,"X",0,nodeid,1);
    if ((nodeid != None) and (nodeid2 != None)): print("PASS")
    else: print("FAILED")

    print("--Update Node"),
    if (pd.update_node(projectid,nodeid,"TM",1) == nodeid): print("PASS")

    print("--Find Node (2)"),
    if (pd.find_node(projectid,"TM") == nodeid): print("PASS 1/2"),
    else: print("FAILED 1/2"),
    if (pd.find_node(projectid,"TM/X") == nodeid2): print("PASS 2/2")
    else: print("FAILED 2/2")

    print ("--Get Node Info"),
    if (str(pd.get_node(projectid,nodeid)["id"]) == str(nodeid)): print("PASS")
    else: print("FAILED")

    

    #raw_input("\nYou can take this moment to manually inspect Dradis :). Then press enter to continue test...\n")


    #Issues
    print("\n<ISSUE ENDPOINT>")

    print("--Get Issues"),
    if (pd.get_issuelist(projectid) != None): print("PASS")
    else: print("FAILED")

    print("--Create Issue"),
    issueid = pd.create_issue(projectid,"TEST ISSUE","DESCRIPTION GOES HERE",['URGENT','ADMIN','INTERNAL'])
    if (issueid != None): print("PASS")
    else: print("FAILED")

    print("--Updating Issue"),
    if (pd.update_issue(projectid,issueid,"TEST ISSUE - MOD","SOME OTHER DESCRIPTION",["High",'ALPHA','GUEST','INTERNAL']) == issueid): print("PASS")
    else: print("FAILED")

    print("--Find Issue"),
    if (issueid in pd.find_issue(projectid,"AlphA")[0]): print("PASS")
    else: print("FAILED")

    print("--Get Issue Info"),
    if (str(pd.get_issue(projectid,issueid)["id"])== str(issueid)): print("PASS")
    else: print("FAILED")


    
    #raw_input("\nYou can take this moment to manually inspect Dradis :). Then press enter to continue test...\n")



    #Evidence
    print("\n<EVIDENCE ENDPOINT>")

    print("--Get Evidence"),
    if (pd.get_evidencelist(projectid,nodeid) != None): print("PASS")
    else: print("FAILED")

    print("--Create Evidence"),
    evidenceid = pd.create_evidence(projectid,nodeid,issueid,"SOME EVIDENCE","MORE INFO",["DANGER","ZONE"])
    if (evidenceid != None): print("PASS")
    else: print("FAILED")

    print("--Update Evidence"),
    if (pd.update_evidence(projectid,nodeid,issueid,evidenceid,"SOME EXTRA EVIDENCE","MORE MORE INFO",["ARCHER"]) == evidenceid): print("PASS")
    else: print("FAILED")

    print("--Find Evidence"),
    if (pd.find_evidence(projectid,nodeid,["EXTRA"])[0]["id"] == evidenceid): print("PASS")
    else: print("FAILED")

    print("--Get Evidence"),
    if (str(pd.get_evidence(projectid,nodeid,evidenceid)["id"])==str(evidenceid)): print("PASS")
    else: print("FAILED")

    

    #raw_input("\nYou can take this moment to manually inspect Dradis :). Then press enter to continue test...\n")


    #Notes
    print ("\n<NOTE ENDPOINT>")

    print("--Get Notes"),
    if (pd.get_notelist(projectid,nodeid) != None): print("PASS")
    else: print("FAILED")

    print("--Create Note"),
    noteid = pd.create_note(projectid,nodeid,"NOTE TEST","TEXT TEXT",["TAG A"])
    if (noteid != None): print("PASS")
    else: print("FAILED")

    print("--Update Note"),
    if (pd.update_note(projectid,nodeid,noteid,"TEST NOTE", "NEW TEXT",["TAGC"],1)==noteid): print("PASS")
    else: print("FAILED")

    print("--Find Note"),
    if (noteid in pd.find_note(projectid,nodeid,"TAGC")[0]): print("PASS")
    else: print("FAILED")

    print("--Get Note"),
    if (pd.get_note(projectid,nodeid,noteid)["id"] == noteid): print("PASS")
    else: print("FAILED")


    raw_input("\nYou can take this moment to manually inspect Dradis :). Then press enter to continue test...\n")


    #<Deletions>
    print("\n<<DELETING STUFF>>")

    #raw_input("del_note?")
    print("--Deleting Note"),
    if (pd.delete_note(projectid,nodeid,noteid) == True): print("PASS")
    else: print("FAILED")

    #raw_input("del_evidence?")
    print("--Deleting Evidence"),
    if (pd.delete_evidence(projectid,nodeid,evidenceid) == True): print("PASS")
    else: print("FAILED")

    #raw_input("del_issue?"),
    print("--Deleting Issue"),
    if (pd.delete_issue(projectid,issueid) == True): print("PASS")
    else: print("FAILED")

    #raw_input("del_node?"),
    print("--Deleting Node"),
    if(pd.delete_node(projectid,nodeid) == True): print("PASS")
    else: print("FAILED")

    #raw_input("del_proj?"),
    print("--Deleting Project"),
    if(pd.delete_project(projectid) == True): print("PASS")
    else: print("FAILED")

    #raw_input("del_client?"),
    print("--Deleting Client"),
    if(pd.delete_client(clientid) == True): print("PASS")
    else: print("FAILED")






