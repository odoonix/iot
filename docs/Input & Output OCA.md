# نحوه استفاده از input_oca  و output_oca

از این پروتکل به عنوان رابط دستگاه و odoo استفاده میشود

# چه کسی بخواند؟

این سند مناسب فردی است که میخواهد دستگاه ها را در odooمعرفی کند و اطلاعات دستگاه ها را وارد نماید.

# Attendence



# نصب ماژول های موردنیاز

ابتدا ماژول های زیر را نصب کنبد

IoT AMQP - IoT Input - IoT Base - IoT Output - Iot ThingsBoard

# ایجاد یک دستگاه در ماژول iot

وارد ماژول iot شوید گزینه new را انتخاب کنید

اطلاعات دستگاه را وارد کنید

تنها فیلد اجباری فیلد device_id_thingsboard است که برای استفاده از output استفاده میشود



# inout_oca
برای ارسال درخواست از دستگاه به سمت odoo استفاده میشود


### تنظیمات odoo برای input

نام متدی که قرار هست در کد سمت odoo هنگام دریافت داده اجرا شود اینجا نوشته میشود


### تنظیمات thingsboard برای input

در قسمت rule chain باید گره rest api call را اضافه کنیم. چیزی شبیه به تصویر زیر:

![alt text](https://s8.uupload.ir/files/screenshot_from_2023-05-23_13-17-53_82c.png)

جزپیات گره script : برای تبدیل داده ورودی به json

```
return {
    msg:{"value":{"user_id": msg.user_id,
        "timestamp": msg.timestamp,
        "punch": msg.punch}
        
    },
    metadata: metadata, 
    msgType: msgType
};

```

جزپیات گره rest api call: 

end poinr url pattern: http://odoo16:8069/iot/123/action?passphrase=123      =>    برابر با 123 است passphrae و serial با فرض اینکه 

request method : POST

Header :

Content-Type : application/json     =>    قبول میکند json فقط thingsboard چون

X-Odoo-dbfilter : ^demo\Z        =>      است  demo  مخصوص

HTTP_X_ODOO_DBFILTER : ^demo\Z    =>     است  demo  مخصوص





# output_oca

برای ارسال درخواست از odoo به دستگاه استفاده میشود.  

### تنظیمات odoo برای output


برای استفاده از output_oca از منو گزینه iot را انتخاب کنید

روی دستگاه مورد نظر کلیک کنید . فیلد device_id_thingsboard را برابر با id دستگاه در thingsboard قرار دهید. 

برای دریافت id دستگاه در thingsboard به آدرس https://iot.yuccasoft.com/devices رفته روی دستگاه موردنظر کلیک کنید id دستگاه را کپی کنید

سپس از تب configuration گزینه iot thingsboard را انتخاب کنید.

در اینجا باید username و password ای که در حساب thingsboard دارید را وارد کنید

مقدار domain را برابر باhttps://iot.yuccasoft.com/api/auth/login قرار دهید.


### تنظیمات thingsboard برای output

نیاز به یک گره rpc call مطابق تصویر زیر داریم


![alt text](https://s8.uupload.ir/files/screenshot_from_2023-05-23_14-38-15_qclz.png)





### تصویر کامل از rule chain attendence


![alt text](https://s8.uupload.ir/files/screenshot_from_2023-05-23_14-37-15_6v6d.png)

