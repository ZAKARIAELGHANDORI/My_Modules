# My_Modules
Si vous souhaitez utiliser les données de cette instance odoo, suivez les étapes ci-dessous :
1) Créez un fichier python et placez-y les lignes suivantes :

------------------------------
## determine the odoo instance 
url = ipaddresse:8017 <br>
##### url c'est l'address de serveur odoo

db = odoo16_test <br>
##### db c'est le nom de database que vous voulez utiliser

username = 'admin' <br>
password = 'admin' <br>
##### username et password sont les informations d'identification utilisées pour se connecter au serveur

import xmlrpc.client

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

##  Option de création des demandes 
```
id = models.execute_kw(db, uid, password, 'kzm.instance.request', 'create', [{'cpu': "new cpu", 'ram': "new ram", 'disk': "new disk", 'odoo_id'; "one of 14 or 15 or 16"
,'limit_date' : "mm/jj/yy", 'url'; "new url"}]).
print("the new record ID created is : ", id)
```
## Options de récupération de toutes les demandes
```
instances = models.execute_kw(db, uid, password, 'kzm.instance.request', 'search_read', [[]], {'fields': ['name', 'cpu', 'ram', 'disk', 'odoo_id', 'tl_id', 'tl_user_id'
, 'address', 'limit_date', 'treat_date', 'treat_duration', 'url']}) 
for rec in instances: 
   print(rec)
```
   
## Option de récupération des commandes par statut 

```
commandes = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [[['state' , '=', 'state you want']]], {
    'fields': ['name', 'partner_id', 'create_date', 'user_id', 'amount_total', 'state']})
for x in commandes:
   print(x) 
```   
 
