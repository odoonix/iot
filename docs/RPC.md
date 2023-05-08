# RPC

در RPC از سمت odoo (گیرنده) در خواست میاد و gateway thingsboard ( سرور ) به این درخواست پاسخ میده. 

هر در خواست باعث میشه تابع server_side_rpc_handler از یک connector صدازده بشه. اینکه کدوم connector باشه بستگی داره تو درخواست rpc از id کدوم گیرنده استفاده بشه.

هدف اینه هر درخواستی که از سمت odoo میاد یک متد با پارامترهاش را ارسال کنه. مطابق اون متد و پارامترها در gateway درخواست انجام میشه.

## Attendence

اگر فرض کنیم دستگاه موردنظر یک دستگاه حضور و غیاب باشد. ما نیاز داریم به درخواست:

# 1- ثبت کاربر جدید (متد add_user)

یعنی به ازای هر کاربری که درodoo ثبت میشه باید اون کاربر در دستگاه هم ثبت بشه

در خواست باید شامل نام متد add_user و پارامترهای موردنیاز باشه

پارامترهای موردنیاز متد add_user : 

user_id : کاربر id

user_name : نام کاربر

### نمونه ای از درخواست ارسالی


```json
{
  "method": "add_user",

  "params": {
   "user_id" : "1",
   "user_name" : "ali"
  }
}
```

## نمونه ای از خروجیه درخواست ارسال شده از odoo . این خروجی در gateway تحت عنوان content از متد server_side_rpc_handler بدست میاد
```
{'device': 'zktec',
  'data': {
    'id': 1, 
    'method': 'add_user',
    'params': {'user_id': '1', 'user_name': 'ali'}
    }
  }
```

## نمونه ای از متد print_file

```
def add_user(self, user_id , user_name):
        conn.set_user(uid= '' , name=user_name , privilege= '', password='', group_id='', user_id='1', card=0)
```



## Printer

### 1-پرینت کردن فایل ( متد print_file)

از odoo یک درخواست پرینت به دستگاه ارسال میشه. 

درخواست باید شامل نام متد print_file و پارامترهای مورد نیاز متد باشه

پارامترهای مورد نیاز متد print_file : 

 printer_name : نام پرینتری که قراره پرینت کنه
 
 printer_file :آدرس فایلی که قرار هست پرینت بشه 
 

## نمونه ای از درخواست ارسالی
```json
{
  "method": "print_file",

  "params": {
    "printer_name": "RP-D10",
    "printer_file": "/home/sanaz/viraweb123/odoo-iot/vw-gateway/extensions/printer/cups/a.txt"
  }
}
```
## نمونه ای از خروجیه درخواست ارسال شده از odoo . این خروجی در gateway تحت عنوان content از متد server_side_rpc_handler بدست میاد
```
{'device': 'branch01 RP-D10',
  'data': {
    'id': 1, 
    'method': 'print_file',
    'params': {'printer_name': 'RP-D10', 'printer_file': '/home/sanaz/viraweb123/odoo-iot/vw-gateway/extensions/printer/cups/a.txt'}
    }
  }
```

## نمونه ای از متد print_file

```
def print_file(self, printer_name , printer_file):
        printid = self.connection.printFile(printer_name, printer_file ,'' , {})
```
