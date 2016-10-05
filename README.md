PyDradis
=======
<h3>
Dradis API Python Wrapper
<br>
Copyright &copy; 2016 Novacoast
</h3>

Usage Example
-
This is a wrapper for the [Dradis Pro API](http://securityroots.com/dradispro/support/guides/rest_api/index.html)

Setup:

```python
from pydradis import Pydradis

debug = True #Do you want to see debug info?
verify = True #Force ssl certificate verification?
pd = Pydradis("<DRADIS API KEY>","<DRADIS SERVER URL>",debug,verify)

```

All endpoints have 6 functions that work roughly the same:

- *Get:* Given an element id, returns the element info.

- *Get Lists:* Returns list of Clients, Projects, etc..

- *Create:* Creates elements and returns their id.

- *Update:* Updates elements and returns their id.

- *Delete:* Deletes elements and returns True if successful.

- *Find:* Given keyword(s), return a list of possible elements.

<h4>Client Endpoint</h4>

- get_clientlist()
```python
>>> pd.get_clientlist()
[[u'NASA', 2], [u'ACME Inc.', 5]]
```

- get_client(int client_id)
```python
>>> pd.get_client(2)
{u'client_since': u'2016-08-29', u'name': u'NASA', u'created_at': u'2016-08-29T05:43:47.000Z', u'updated_at': u'2016-08-29T05:44:30.000Z', u'id': 3, u'projects': [{u'id': 6, u'name': u'Internal Pentest #1'}]}
```

- create_client(string client_name)
```python
>>> pd.create_client("Wayne Industries")
42
```

- update_client(string client_name)
```python
>>> pd.update_client("Wayne Corp.")
42
```

- find_client(string client_name)
```python
>>> pd.find_client("Wayne Corp.")
42
```

- delete_client(int client_id)
```python
>>> pd.delete_client(42)
True
```

<h4>Project Endpoint</h4>

- get_projectlist()
```python
>>> pd.get_projectlist()
[[u'Project X', 10],[u'WikiTesting', 7], [u'Project B-25', 1], [u'Internal Pentest', 2]]
```

- get_project(int project_id)
```python
>>> pd.get_project(10)
{u'owners': [{u'email': u'pedro@example.com'}], u'name': u'Project X', u'created_at': u'2016-04-20T23:49:40.000Z', u'updated_at': u'2016-06-29T16:10:06.000Z', u'authors': [{u'email': u'pedro@example.com'}], u'id': 10}
```

- create_project(string project_name, int client_id=None)
```python
>>> pd.create_project("Project T",2)
26
```

- update_project(int project_id, string project_name, int new_client_id)
```python
>>> pd.update_project(26,"Project T1",42)
26
```

- find_project(string project_name)
```python
>>> pd.find_project("Project T1")
26
```

- delete_project(int project_id)
```python
>>> pd.delete_project(10)
True
```

<h4>Node Endpoint</h4>

- get_nodelist(int project_id)
```python
>>> pd.get_nodelist(1)
[[u'Dradis Professional Edition', 1], [u'Welcome', 2], [u'Getting Help', 3], [u"What's next?", 4]]
```

- get_node(int project_id, int node_id)
```python
>>> pd.get_node(1,1)
{u'type_id': 0, u'created_at': u'2012-06-09T10:25:57.000Z', u'updated_at': u'2014-03-12T14:19:37.000Z', u'label': u'Dradis Professional Edition', u'parent_id': None, u'notes': [{u'fields': {u'Title': u'Test Note #1'}, u'category_id': 6, u'text': u'#[Title]#\nTest Note #1', u'id': 1, u'title': u'Test Note #1'}], u'position': 0, u'evidence': [], u'id': 1}
```

- create_node(int project_id, string label, int type_id=0, int parent_id=None, position=1)
```python
>>> pd.create_node(1,"Testing #2",0,None,1)
590
```

- update_node(int project_id, int node_id, string label=None, int type_id=None, int parent_id=None, position=None)
```python
>>> pd.update_node(1,590,"Testing #2 - Mod",0,1,0)
590
```

- find_node(int project_id, string nodepath)
```python
>>> pd.find_node(1,"Dradis Professional Edition/Testing #2 - Mod")
590
```


- delete_node(int project_id, int node_id)
```python
>>> pd.delete_node(1,590)
True
```

<h4>Issues Endpoint</h4>

- get_issuelist(int project_id)
```python
>>> pd.get_issuelist(1)
[[u'Firewall Issue', 414], [u'Problem #1', 413]]
```

- get_issue(int project_id, int issue_id)
```python
>>> pd.get_issue(1,414)
{u'title': u'Firewall Issue', u'fields': {u'Description': u'The firewall is turned off', u'Title': u'Firewall Issue'}, u'created_at': u'2016-06-30T16:07:10.000Z', u'updated_at': u'2016-06-30T16:07:10.000Z', u'text': u'#[Title]#\r\nFirewall Issue\r\n\r\n#[Description]#\r\nThe firewall is turned off\r\n\r\n', u'id': 414}
```

- create_issue(int project_id, string title, string text, string[] tags=[])
```python
>>> pd.create_issue(1,"Main router issue", "Main router uses default admin & password", ["Internal","Networking"])
415
```

- update_issue(int project_id, int issue_id, string title, string text, string[] tags=[])
```python
>>> pd.update_issue(1,415,"Main router credentials", "Admin=root and password=abc123 ", ["Internal","Networking","Tag A"])
415
```

- find_issue(int project_id, string[] keywords)
```python
#Use with single keyword
>>> pd.find_issue(1,"router")
[[u'Main router credentials', 415]]
#Use with keyword list
>>> pd.find_issue(1,["issue","problem"])
[[u'Firewall Issue', 414], [u'Problem #1', 413]]
```

- delete_issue(int project_id, int issue_id)
```python
>>> pd.delete_issue(414)
True
```


<h4>Evidence Endpoint</h4>

- get_evidencelist(int project_id, int node_id)
```python
>>> pd.get_evidencelist(1,1)
[{u'content': u'#[Title]#\r\nFingerprints\r\n\r\n#[Description]#\r\nFoo Foo\r\n\r\n#[Tag B]#\r\n', u'fields': {u'Tag B': u'', u'Label': u'Dradis Professional Edition', u'Description': u'Foo Foo', u'Title': u'Fingerprints'}, u'issue': {u'url': u'https://dradis.waynecorp.at/pro/api/issues/415', u'id': 415, u'title': u'Main router credentials'}, u'id': 47}]
```

- get_evidence(int project_id, int node_id, int evidence_id)
```python
>>> pd.get_evidence(1,1,47)
{u'content': u'#[Title]#\r\nFingerprints\r\n\r\n#[Description]#\r\nFoo Foo\r\n\r\n#[Tag B]#\r\n', u'fields': {u'Tag B': u'', u'Label': u'Dradis Professional Edition', u'Description': u'Foo Foo', u'Title': u'Fingerprints'}, u'issue': {u'url': u'https://dradis.waynecorp.at/pro/api/issues/415', u'id': 415, u'title': u'Main router credentials'}, u'id': 47}
```

- create_evidence(int project_id, int node_id, int issue_id, string title, string text, string[] tags=[])
```python
>>> pd.create_evidence(1,1,415,"Some Evidence", "More Info",["Tag A"])
48
```

- update_evidence(int project_id, int node_id, int issue_id, int evidence_id, string title, string text, string[] tags=[])
```python
>>> pd.update_evidence(1,1,415,46,"Some Evidence #2", "More Info",["Internal"])
46
```

- find_evidence(int project_id, node_id, string[] keywords)
```python
>>> pd.find_evidence(1,1,["evidence #2"])
[{u'content': u'#[Title]#\r\nSome Evidence #2\r\n\r\n#[Description]#\r\nMore Info\r\n\r\n#[Internal]#\r\n', u'fields': {u'Internal': u'', u'Label': u'Dradis Professional Edition', u'Description': u'More Info', u'Title': u'Some Evidence #2'}, u'issue': {u'url': u'https://dradis.waynecorp.at/pro/api/issues/415', u'id': 415, u'title': u'Main router credentials'}, u'id': 46}]
```

- delete_evidence(int project_id, node_id, evidence_id)
```python
>>> pd.delete_evidence(1,1,46)
True
```

<h4>Note Endpoint</h4>

- get_notelist(int project_id, int node_id)
```python
>>> pd.get_notelist(1,1)
[[u'Use the tree on the left to browse through the items in this project.', 1], [u'Ready to try the new interface?', 2]]
```

- get_note(int project_id, int node_id, int note_id)
```python
pd.get_note(1,1,1)
{u'fields': {u'Title': u'Use the tree on the left to browse through the items in this project.'}, u'category_id': 6, u'text': u'#[Title]#\nUse the tree on the left to browse through the items in this project.', u'id': 1, u'title': u'Use the tree on the left to browse through the items in this project.'}
```

- create_note(int project_id, int node_id, string title, string text, string[] tags=[], category=0)
```python
>>>pd.create_note(1,1,"Possible Hosts", "foo.com, foo.org and foo.net",["External","OSINT"],0)
416
```

- update_note(int project_id, int node_id, int note_id, string title, string text, string[] tags=[], category=1)
```python
>>> pd.update_note(1,1,416," Possible Vulnerable Hosts", "foo.com, foo.org, foo.net, and foo.io",["External","OSINT"],1)
416
```

- find_note(int project_id, int node_id, string[] keywords)
```python
>>> pd.find_note(1,1,["foo.org","foo.net"])
[[u'Vulnerable Host', 416]
```

- delete_note(int project_id, int node_id, int note_id)
```python
>>> pd.delete_note(1,1,416)
True
```


<h3>License</h3>
Pydradis is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pydradis is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Pydradis.  If not, see <http://www.gnu.org/licenses/>.