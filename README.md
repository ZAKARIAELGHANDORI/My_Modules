# My_Modules
If you want to use data from this odoo instance follow the steps bellow :
1) Create a python file and put inside the following lines :

------------------------------
## determine the odoo instance 
url = ipaddresse:8017
db = odoo16_test
username = 'admin'
password = 'admin'

import xmlrpc.client

uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

##  Option de création des demandes 

id = models.execute_kw(db, uid, password, 'kzm.instance.request', 'create', [{'cpu': "new cpu", 'ram': "new ram", 'disk': "new disk", 'odoo_id'; "one of 14 or 15 or 16"
,'limit_date' : "mm/jj/yy", 'url'; "new url"}])
print("the new record ID created is : ", id)

## Options de récupération de toutes les demandes
instances = models.execute_kw(db, uid, password, 'kzm.instance.request', 'search_read', [[]], {'fields': ['name', 'cpu', 'ram', 'disk', 'odoo_id', 'tl_id', 'tl_user_id'
, 'address', 'limit_date', 'treat_date', 'treat_duration', 'url']})
for rec in instances
   print(rec)
   
## Option de récupération des commandes par statut 

commandes = models.execute_kw(db, uid, password, 'kzm.instance.request', 'search_read', [[['state' , '=', 'state you want']]])
for rec in commandes
   print(rec)


 
 

