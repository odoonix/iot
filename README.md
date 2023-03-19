# iot-box
connect office devices into the ERP system

## سه تاپیک در broker داریم(attendence _ employees _ maintenance) 
<br />

<p align ='right'>
تاپیک attendence : 
<br />

این تاپیک برای ثبت حضور و غیاب ها است. داده های حضور و غیاب از دستگاه zk را در odoo ثبت میکند<br />
ساختار داده ای که از zk به تاپیک attedence وارد میشود. <br />

</p>
<pre>
thing_id = int (zk id)
attendence[{  
  employee_id = int  
  timestamp = datetime  
  punch = int [1,4] 1:in 4:out  
}, ]  
</pre>
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
