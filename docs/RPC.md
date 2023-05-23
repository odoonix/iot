# RPC

در RPC از سمت odoo (گیرنده) در خواست میاد و gateway thingsboard ( سرور ) به این درخواست پاسخ میده. 

هر در خواست باعث میشه تابع server_side_rpc_handler از یک connector صدازده بشه. اینکه کدوم connector باشه بستگی داره تو درخواست rpc از id کدوم گیرنده استفاده بشه.

هدف اینه هر درخواستی که از سمت odoo میاد یک متد با پارامترهاش را ارسال کنه. مطابق اون متد و پارامترها در gateway درخواست انجام میشه.

## Attendence

اگر فرض کنیم دستگاه موردنظر یک دستگاه حضور و غیاب باشد. ما نیاز داریم به درخواست:

### 1- به روزرسانی همزمان چند کاربر  (متد update_user)

در این متد چک میشه. اگر کاربری با user_id ارسالی وجود داشت آن کاربر حذف میشه و کاربر جدیدی با داده های ارسالی ساخته میشه

اگر کاربری با user_id ارسالی وجود نداشت آن کاربر ساخته میشه


درخواست باید شامل نام متد update_user و پارامترهای موردنیاز آن باشد.


پارامترهای موردنیاز متد update_user : 



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
  "method": "update_user",
  "params": {
  
      "0" : {
      "uid": "33",
      "name": "zahra",
      "privilege":"",
      "password" : "",
      "group_id" : "",
      "user_id" : "33",
      "card" : "0"
      },

      "1" : {
      "uid": "38",
      "name": "fateme",
      "privilege":"",
      "password" : "",
      "group_id" : "",
      "user_id" : "38",
      "card" : "0"
      }
  }
}
```

### نمونه ای از متد create_user

```python
def update_user(self, uid, name, privilege, password, group_id, user_id, card):
        # Check user is exist
        users = self.connection.get_users()
        exist_user = 0
        
        for item in users:
            # user exist
            if item.user_id == user_id:
                exist_user = item
            
        # user not exist create
        if exist_user == 0:
            # user not exist Create user        
            self.connection.set_user(uid=uid,
                                name=name,
                                privilege=privilege,
                                password=password,
                                group_id=group_id,
                                user_id=user_id,
                                card=card
                                )
        else:
            # user is exist update / delete and create
            # save finger print
            
            fingers = self.connection.get_templates()
            
            save_fingers = []
            for finger in fingers:
                if finger.uid == uid:
                    save_fingers.append(finger)
            
            
            self.del_user(user_id)    
            self.connection.set_user(uid=uid,
                                    name=name,
                                    privilege=privilege,
                                    password=password,
                                    group_id=group_id,
                                    user_id=user_id,
                                    card=card
                                    )
            #add finger print
            self.connection.save_user_template(uid, save_fingers)
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

```python
def del_user(self , user_id_delete):
        self.connection.delete_user(user_id=user_id_delete)
```

### حذف همزمان چند کاربر

### نمونه ای از درخواست ارسالی برای حذف چند کاربر

```json
{
  "method": "del_user",
  "params": {
    
      "0" : {"user_id_delete" : "109"},
      "1" : {"user_id_delete" : "110"}
  }
}

```






# 4- ذخیره اثرانگشت ( متد save_fingerprint )

مثلا از طرف odoo درخواست ذخیره اثر انگشت یک کاربر مشخص وارد میشه.

درخواست باید شامل متد save_fingerprint و پارامترهای موردنیاز آن باشد.

پارامترهای مورد نیاز متد save_fingerprint :

uid_change : کاربری که قرار هست اثر انگشتش ذخیره بشه uid

*نکته : متد ذخیره اثرانگشت با uid کار میکنه

### نمونه ای از درخواست ارسالی

```json
{
  "method": "save_fingerprint",
  "params": {
    "user_id_change" : "199"
  }
}

```

### نمونه ای از متد update_fingerprint


```python
def update_fingerprint(self, params):
        if not self.connection:
            raise Exception("Device is not connected")
     
        self.connection.enroll_user(int(params["user_id_change"]))
        
        #template = self.connection.get_user_template(uid=int(params["user_id_change"]), temp_id=0)
        

```



### نمونه ای از متد server_side_rpc_handler 

```python
def server_side_rpc_handler(self, content):
        params = content["data"]["params"]
        method_name = content["data"]["method"]
        
        # update_user
        # TODO : Fixed the error of sending multiple data at the same time 
        if method_name == "update_user":
            for key, value in params.items():
                self.update_user(int(value["uid"]),
                                value["name"],
                                value["privilege"],
                                value["password"],
                                value["group_id"],
                                value["user_id"],
                                int(value["card"])
                                )
            
        # delete user
        if method_name == "del_user":
            #params = content["data"]["params"]
            #self.del_user(int(params["user_id_delete"]))
            for key, value in params.items():            
                self.del_user(value['user_id_delete'])
                
        # change finger print
        if method_name == "save_fingerprint":
            self.save_fingerprint(int(params["user_id_change"]))
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
