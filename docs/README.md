# پروتکل ارتباط در شبکه اشیا برای مدیریت ورود و خرج

برای مدیریت ورود و خروج علاوه بر ساعت ورود و خروج کارهای دیگری مانند مدیریت افراد باید انجام شود. در این سند نحوه ارتباط اجزا برای انجام این کارها به صورت دقیق تعیین شده.

پروتکل بر اساس ساختارهای شبکه اینترنت اشیا طراحی شده. پروتکل پایه MQTT است.

TODO: تعیین دقیق نسه پروتکل

## چه کسی بخواند؟

در این سند پروتکل به صورت فنی بیان شده و برای توسعه دهندگان مناسب است.

## ویرایش‌ها

TODO: جدول تغییرات اضافه شود.



# معرفی تاپیک‌ها

سه تاپیک برای این پروتکل در نظر گرفته شده که عبارتند از:

* /attendences
* /employes
* /maintenances

## attendence

این تاپیک برای ثبت حضور و غیاب ها است.
داده های حضور و غیاب از دستگاه‌ها را در اودوو ثبت میکند.

ساختار داده ای که از دستگاه‌ها به تاپیک attedence وارد میشود باید ساختار داده‌ای زیر را داشته باشد.

نکته: این ساختار داده‌ای به فرمت JSON و با استاندارد UTF8  کدگذاری و در بدنه پیام ارسال می‌شود.

```json
{
  "things_id": "",
  "attendence":[{
    "employee_id": 1,
    "timestamp": "2022-10-15 08:45:15",
    "punch": "in"
  }]
}
```

نمونه بالا یک بسته ارسالی از سمت دستگاه‌های ورود خروج به تاپیک مورد نظر را نشان می‌دهد. در بخش ساختار داده‌ها به صورت دقیق نوع داده‌ها مشخص شده است.

به این نوع داده، داده ورود و خروج یا attendence می‌گوییم.



داده هایی که از تاپیک attendence  در odoo ثبت میشود. 
این داده ها صرفا در یک جدول به جز جدول hr_attendence در odoo ثبت میشوند.
این داده ها پس از چک شدن در جدول اصلی ذخیره میشوند.



## employee
این تاپیک برای ثبت نام کاربران است.  
ساختار داده هایی که از دستگاه‌ها وارد تاپیک employee و از تاپیک employee وارد odoo میشود. 
نکته: CRUD یک رشته شامل یکی از حروف CRUD است. هر حرف نشان دهنده یک اکشن است. 
 * / C : create
 * / R : read
 * / U : update
 * / D : delete


```json
{
  "things_id": "",
  "action" :[CRUD]
  "employee":[{
    "employee_id": 1,
    "employee_name": "ali ahmadi",
    "finger_print" : [{
                        "size": 638,
                        "uid": 2,
                        "fid": 6,
                        "valid": 1,
                        "template":
                        "mark":
    }]
  }]
}
```

ساختار داده هایی که از odoo وارد تاپیک employee و از تاپیک employee وارد دستگاه‌ها میشود، مشابه ساختار بالا است.


##  maintenance

اگر دستگاهی ارتباطش را به هر نحوی از دست داد از این تاپیک استفاده میشود.
اگر این اتفاق بیفته پس از وصل شدن دستگاه، odoo باید لیست کاربران را در تاپیک employee قرار بده و دستگاه جدید لیست کاربران را بخواند.


  

```json
{
  "things_id": "",
  "devices" :[{
    "serialnumber" : '2679811022038',
    "problem" : "syc"
  }]
}
```


#  ساختار داده‌ها

تمام ساختارهای داده ارسالی و دریافتی به فرمت JSON بوده و با استاندارد UTF-8  کد گذاری می‌شود.

## ساختار داده Attendence

این ساختار داده برای ارسال عملیات‌های ورود خروج ثبت شده در دستگاه‌ها استفاده می‌شود.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://viraweb123.ir/iot.attendence.schema.json",
  "title": "Attendence",
  "description": "An employee attendence",
  "type": "object",
  "properties": {
    "things_id": {
      "description": "The unique identifier for a things who send the message",
      "type": "string",
      "max_length": 
    },
    "employee_id" : {
      "description": "The unique identifier for a employee",
      "type": "string",
      "max_length": 
    },
    "timestamp" : {
      "description": "The date recorded in the device",
      "type": "datetime",
      "max_length": 
    },
    
    "punch" : {
      "description": "Indicates entry or exit. It accepts two values 'in' or 'out' ",
      "type": "string",
      "max_length": 
    },
    
  },
  "required": [ "things_id" ]
}
```

## ساختار داده employee
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://viraweb123.ir/iot.attendence.schema.json",
  "title": "employee",
  "description": "An employee ",
  "type": "object",
  "properties": {
    "things_id": {
      "description": "The unique identifier for a things who send the message",
      "type": "string",
      "max_length": 128
      },
      
    "employee_id" : {
      "description": "The unique identifier for a employee",
      "type": "string",
      "max_length": 10
      },
      
    "employee_name" : {
      "description": "name of employee",
      "type": "string",
      "max_length": 100
      },
      
    "password" : {
      "description": "Employee password",
      "type": "string",
      "max_length": 1000
      },
      
     "finger_prints" : {
      "description": "Employee finger_prints",
      "type": "array",
      "items" : 
          {
            "description": "A list of employee fingerprints ",
            
            "type": "object",
            "properties": {
                  "size": {"description": "Fingerprint size", "type": "int"}
                  "uid": {"description": "Employee uid", "type": "int"},
                  "fid": {"description": "Which finger of the registered employee can take up to 10 values", "type": "int"},
                  "valid": {"description": "validation fingerprint", "type": "int"},
                  "template":{"description": "fingerprint", "type": "bytes" }
                  "mark": {"description": "fingerprint", "type": "bytes" }
              }
          }
    },
    
  },
  "required": [ "things_id" ]
}
```

## ساختار داده maintenance
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://viraweb123.ir/iot.attendence.schema.json",
  "title": "maintenance",
  "description": "Device problems",
  "type": "object",
  "properties": {
    "things_id": {
      "description": "The unique identifier for a things who send the message",
      "type": "string",
      "max_length": 128
    },
    
    "serialnumber" : {
      "description": "The unique identifier for a device",
      "type": "string",
      "max_length": 100
    },
    
    "problem" : {
      "description": "Determines the type of problem",
      "type": "string",
      "max_length": 200
    },
    
  },
  "required": [ "things_id" ]
}
```


