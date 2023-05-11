# RPC

در RPC از سمت odoo (گیرنده) در خواست میاد و gateway thingsboard ( سرور ) به این درخواست پاسخ میده. 

هر در خواست باعث میشه تابع server_side_rpc_handler از یک connector صدازده بشه. اینکه کدوم connector باشه بستگی داره تو درخواست rpc از id کدوم گیرنده استفاده بشه.

هدف اینه هر درخواستی که از سمت odoo میاد یک متد با پارامترهاش را ارسال کنه. مطابق اون متد و پارامترها در gateway درخواست انجام میشه.

## Attendence

اگر فرض کنیم دستگاه موردنظر یک دستگاه حضور و غیاب باشد. ما نیاز داریم به درخواست:

### 1- ثبت کاربر جدید (متدcreate_user)

یعنی به ازای هر کاربری که درodoo ثبت میشه باید اون کاربر در دستگاه هم ثبت بشه

در خواست باید شامل نام متد create_user  و پارامترهای موردنیاز باشه

پارامترهای موردنیاز متدcreate_user : 
uid : کاربر uid  (int, required, )

name : نام کاربر (str)

privilege : امتیاز کاربر  (str)

password : رمز کاربر (str)

group_id : گروه id (str) 

user_id : کاربر id (str)

card : card (int, required, )

*نکته : ما فرض میکنیم uid همیشه با user_id برابر است. 



### نمونه ای از درخواست ارسالی


```json
{
  {
  "method": "create_user",
  "params": {
    "uid": "102",
    "name" : "",
    "privilege" : "",
    "password" : "",
    "group_id" : "",
    "user_id" : "",
    "card" : "0" 
  }
}
```

### نمونه ای از متد create_user

```
def create_user(self, uid, name, privilege, password, group_id, user_id, card):
        self.connection.set_user(uid=uid, name=name, privilege=privilege, password=password, group_id=group_id, user_id=user_id, card=card)
```

### 2- حذف کاربر (متد del_user)

یعنی به ازای هر کاربری که در odoo حذف میشه باید اون کاربر در دستگاه هم حذف بشه.

درخواست باید شامل نام متد del_user و پارامترهای موردنیاز آن باشد.

پارامترهای موردنیاز del_user :
user_id : کاربری که حذف شده user_id

### نمونه ای از درخواست ارسالی



```json
{
  "method": "del_user",
  "params": {
    "user_id_delete" : "102"
  }
}

```

### نمونه ای از متد del_user

```
def del_user(self , user_id_delete):
        self.connection.delete_user(user_id=user_id_delete)
```


### 3- به روزرسانی اطلاعات کاربر (متد update_user )

یعنی به ازای هر کاربری که در odoo به روز میشه اطلاعات اون کاربر در دستگاه هم باید به روز بشه.

درخواست باید شامل نام متد update_user و پارامترهای موردنیاز آن باشد.

پارامترهای مورد نیاز متد update_user :

user_id_change : کاربری که قراره اطلاعاتش تغییر کند id 

field_change : (uid, name, privilege, password, group_id, user_id, card) نام فیلدی که قرار هست تغییر کند

value_change : مقدار جدیدی که قرار هست فیلد موردنظر بگیره

### نمونه ای از درخواست ارسالی



```json
{
  "method": "update_user",
  "params": {
    "user_id_change" : "101",
    "field_change" : "name",
    "value_change" : "zahra"
  }
}
```

### نمونه ای از متد update_user


```
def update_user(self, user_id_change, field_change, value_change):
        # Find user
        users = self.connection.get_users()
        exist_user = 0
        for item in users:
            if item.user_id == user_id_change:
                exist_user = item
        # Change value of user
        setattr(exist_user, field_change, value_change)
        self.del_user(user_id_change)
        self.connection.set_user(uid=exist_user.uid,
                                 name=exist_user.name,
                                 privilege=exist_user.privilege, 
                                 password=exist_user.password,
                                 group_id=exist_user.group_id,
                                 user_id=exist_user.user_id,
                                 card=exist_user.card
                                 )
```



### نمونه ای از متد server_side_rpc_handler 

```
def server_side_rpc_handler(self, content):
    params = content["data"]["params"]
    method_name = content["data"]["method"]

    # create_user
    if method_name == "create_user":
        self.create_user(int(params["uid"]),
                        params["name"],
                        params["privilege"],
                        params["password"],
                        params["group_id"],
                        params["user_id"],
                        int(params["card"])
                        )

    # delete user
    if method_name == "del_user":
        params = content["data"]["params"]
        self.del_user(int(params["user_id_delete"]))

    # update user
    if method_name == "update_user":
        self.update_user(params["user_id_change"], params["field_change"],  params["value_change"])

    # change finger print
    if method_name == "change_fingerprint":
        self.change_fingerprint(params["user_id_change"])
```



## Printer

### 1-پرینت کردن فایل ( متد print_file)

از odoo یک درخواست پرینت به دستگاه ارسال میشه. 

درخواست باید شامل نام متد print_file و پارامترهای مورد نیاز متد باشه

پارامترهای مورد نیاز متد print_file : 

 printer_name : نام پرینتری که قراره پرینت کنه
 
 printer_file :آدرس فایلی که قرار هست پرینت بشه 
 

### نمونه ای از درخواست ارسالی
```json
{
  "method": "print_file",

  "params": {
    "printer_name": "RP-D10",
    "printer_file": "/home/sanaz/viraweb123/odoo-iot/vw-gateway/extensions/printer/cups/a.txt"
  }
}
```
### نمونه ای از خروجیه درخواست ارسال شده از odoo . این خروجی در gateway تحت عنوان content از متد server_side_rpc_handler بدست میاد
```
{'device': 'branch01 RP-D10',
  'data': {
    'id': 1, 
    'method': 'print_file',
    'params': {'printer_name': 'RP-D10', 'printer_file': '/home/sanaz/viraweb123/odoo-iot/vw-gateway/extensions/printer/cups/a.txt'}
    }
  }
```

### نمونه ای از متد print_file

```
def print_file(self, printer_name , printer_file):
        printid = self.connection.printFile(printer_name, printer_file ,'' , {})
```
