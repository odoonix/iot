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


<p align ='right'>
داده هایی که از تاپیک attendence  در odoo ثبت میشود. این داده ها صرفا در یک جدول به جز جدول hr_attendence در odoo ثبت میشود.  این داده ها پس از چک شدن در جدول اصلی ذخیره میشوند  <br />


تاپیک employee: این تاپیک برای ثبت نام کاربران است.  <br />
ساختار داده هایی که از دستگاه zk وارد تاپیک employee و از تاپیک employee وارد odoo میشود. <br />
</p>


<pre>
things_id = int 
employee{[ 
  employee_id = int 
  employee_name = str 
  password = (number or finger print) 
]} 
</pre>



<p align ='right'>
ساختار داده هایی که از odoo وارد تاپیک employee و از تاپیک employee وارد zk میشود. <br /> مشابه ساختار بالا است <br /> 

تاپیک maintenance: اگر دستگاه جدیدی وارد سیستم شود یا دستگاهی خراب شود از این تاپیک استفاده میشود <br />
مثلا اگر دستگاه جدیدی وصل شود<br /> 
  
</p>

<pre>
things_id = int 
devices [{
  problem = 'syc'
}]
</pre>

<p align ='right'>
اگر این اتفاق بیفته . odoo باید لیست کاربران را در تاپیک employee قرار بده و دستگاه zk جدید لیست کاربران را بخواند.
</p>


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
      "max_length": 128
    },
    "employee_id" : {
      "description": "The unique identifier for a employee",
      "type": "string",
      "max_length": 10
    },
    "timestamp" : {
      "description": "The date recorded in the device",
      "type": "datetime",
      "max_length": 
    },
    
    "punch" : {
      "description": "Indicates entry or exit. It accepts two values in or out ",
      "type": "string",
      "max_length": 3
    },
    
  },
  "required": [ "things_id" ]
}
```
