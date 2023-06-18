# نحوه استفاده از input_oca  و output_oca

از این پروتکل به عنوان رابط دستگاه و odoo استفاده میشود

# چه کسی بخواند؟

این سند مناسب برنامه نویسی است که قصد دارد برای ماژول iot ورودی یا خروجی ای را در odoo ایجاد کند.



# نصب ماژول های موردنیاز
ابتدا ماژول های زیر را نصب کنبد

IoT AMQP - IoT Input - IoT Base - IoT Output - Iot ThingsBoard


### تنظیمات odoo برای input

گزینهinput زمانی استفاده میشود که قصد داریم اطلاعاتی را از دستگاه به odoo وارد کنیم. مثلا برای دستگاه حضور و غیاب داده های حضور و غیاب دستگاه را وارد جدول attendance در odoo کنیم.

در این حالت نیاز است که دستگاهی در ماژول iot ساخته شود که input آن موارد زیر را داشته باشد

گزینه call_model :نام جدولی که قرار هست داده ها در آن وارد شود مثلا برای داده های حضور و غیاب در ویراوب ما جدول shadow table را انتخاب میکنیم

گزینه Call Function :نام متدی که قرار هست در کد سمت odoo هنگام دریافت داده اجرا شود

گزینه serial و گزینه passphrase :  این سریال و پسورد در thingsboard زمانی که میخواهید به odoo درخواست ارسال کنید استفاده میشود. برای مثال url شما در گره restapi در rule chain تینگزبرد باید مقدار زیر را داشته باشد


http://HOST_NAME/iot/123/action?passphrase=123

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


اطلاعات کامل گره های تصویر بالا در [این لینک](https://s29.picofile.com/file/8464763434/attendance_2_.json.html)
