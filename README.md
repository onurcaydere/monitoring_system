# Monioring System

Öncelikle merhabalar projemde adımlar hakkında bilgi vermek isterim.
* Django projesi OLUŞTUR
* Oluşturulan projede postgresql ile connection kur.
* Ekrandaki verileri uygulamayı geliştirdiğin cihaz üzerinden çekme.
* İnput alanı açarak shell üzerinden komut çalıştırıp çıktısını göster. !!Komutlar uygulamayı geliştirdiğin cihaz üzerinde çalışmalı!!
* Çalıştırılan komut ve çıktılarını veritabanı üzerinde kayıt et.
* Daha önce çalışmış komut ve çıktılarını gösterebileceğin bir alanda dashboarda ekle.

## Django Projesi Oluştur
Burada ilk olarak vs code üzerinde django projemi oluşturuyorum."django-admin startproject cekino".<br>
Daha sonrasında bir application ekliyorum "python manage.py startapp cek_app".<br>
Bu işlemler bittikten sonra oluşturacağım site için bir template oluşturuyorum.


## Oluşturulan projede postgresql ile connection kur
Bu işlem için ilk önce postgresql'i bilgisayarıma kurdum. <br>
Daha sonra Django projem içerisinde settings.py içerisinde postgresql i ayarlamam gerekiyordu.<br>![image](https://user-images.githubusercontent.com/63595177/190194294-8b38e0bf-7a57-4574-893d-6647d6cd7ad9.png)<br>
Ayarlamadan önce postgresql içerisinde deneme adında bir database oluşturuyorum.<br>
Daha sonrasında <br>![image](https://user-images.githubusercontent.com/63595177/190194500-26625230-89e9-4281-a7cf-e2a8443a5d4c.png)<br>
settings.py içerisinde DATABASES bölümünde yukarıdaki gibi database name, password,user,host ve port değerlerini veriyorum.<br>
Models.py içerisinde oluşturacağım scheması belirliyorum projemde shell üzerinde input ve output bilgilerini tutmam gerekiyor bu yüzden;<br>
![image](https://user-images.githubusercontent.com/63595177/190195344-31c140c7-63fc-47a3-bf5b-470a0992148e.png)<br>
 Bu şekilde yapıyorum.<br>
 Sonrasında site içerisinde adminpage içerisinde bu veritabanını görmeyi istediğim için admin.py içerisinde ;<br>
 ![image](https://user-images.githubusercontent.com/63595177/190195596-37779b92-5abf-4903-ac67-0da17ed6c789.png)<br>
 İşlemleri gerçekleştiriyorum.<br>
bu işlemleri bitirdikten sonra terminal üzerinde bu değişikleri djangoya da göstermem gerekiyor ve sırasıyla "python manage.py makemigrations" "python manage.py migrations" komutlarını çalıştırıp database içerisinde djangonun tablolarını ve models içerisinde benim oluşturduğum tabloyu görebiliyorum.<br>
![image](https://user-images.githubusercontent.com/63595177/190195801-df76ea9c-b559-4ab3-a248-838b4c15c7d8.png)<br>

##  Ekrandaki verileri uygulamayı geliştirdiğin cihaz üzerinden çekme
Burada yaptığım araştırmalar sonucu "PSUTİL" kütüphanesi kullanmaya karar verdim ve kullanırken "https://psutil.readthedocs.io/en/latest/" kendi dokümentasyon sayfasından yararlandım.Site içerisine bir dictionary olarak gönderdim ve html içerisinde Jinja ile projemden aldığım value değerlerini kullandım.Sadece psutil kütüphanesi memory üzerinde cached bilgisi vermediği daha doğrusu Linux/BSD işletim sisteminde bu değeri verdiği için cached değerini "ctypes" kütüphanesi kullanarak aldım.Burada internet üzerinden yaptığım araştırmalarda gördüğüm şekilde kullandım. <br>

Buradaki en önemli faktör dashboard içerisinde verilerimin sürekli yenilenmesi oldu çünkü sadece tek seferde gösterilen bir cpu,ram,takas bellek,disk bilgileri çokta anlamlı olmayacaktı ve direkt sayfanın yenilenmeside pek mantıklı bir çözüm değildi. Bu yüzden js ile yaptığım araştırmada belirli bir süre içerisinde belirtilen id ye sahip alanın yenilenmesi sağlayacak bir yapı üzerinde araştırma yaptım ve daha sonrasında kendi html sayfam içerinde uyguladım. <br>

Sayfa içerisine gönderdiğim değerler bazıları tek örneğin cpu için tek bir şekilde psutil.cpu_times_percent(interval=1) ile gönderdim fakat physicaldrive için baktığımızda birden fazla olacağı için ayrı ayrı göndermektense sayfa içerinde for döngüsüyle bilgileri aktardım.Daha sonrasında physicaldrive içerisinde bilgi olarak göstereceğim Okunan Zaman ve Yazılan zaman için gelen değer direk olarak bir value olduğundan ötürü cek_app içerisinde templatetags klasörü açıyorum ve dışardan erişebilmem için __init__.py ve fonksiyonumu içerecek olan tags_custom.py ı oluşturuyorum.  tags_custom.py içerisine;
<br>
![image](https://user-images.githubusercontent.com/63595177/190202112-023cd722-5fc9-4d3d-9fc4-d2b9ba363ec2.png)<br>
fonksiyonumu yazıyorum ve gelen değer saat dakika ve saniye olarak geri dönüyor.

Sonuç olarak bakıldığında ise dashboard 20 sn lik bir gif ile ;<br>

![20220914_184512](https://user-images.githubusercontent.com/63595177/190201447-535262b9-280b-4a88-a6dd-f20318d0eb20.gif)<br>


## İnput alanı açarak shell üzerinden komut çalıştırıp çıktısını göster. !!Komutlar uygulamayı geliştirdiğin cihaz üzerinde çalışmalı!!

Burada html içerine form alanımı oluşturdum ve django içerisinde request.method=="POST" olduğunda içerisinde işlemlere devam ettim. Burada site içerisinden kullanıcıdan aldığım inputu shell üzerinde çalıştırmayı hedefliyoruz bunun için subprocess kütüphanesini kullanıyorum. Html üzerinde request.POST.get('message') message id sine sahip olunan input area yı bana getiriyor daha sonrasında bu ifadeyi bir değişkene atıp subprocess.run(["powershell", "-Command", değişkene], capture_output=True) ile shell çıktısını alıyorum.Burada çıktı üzerinde ilk 7 satıra baktığımda column name ve info vardı bu yüzden 7. satırdan başlattım yazdırmaya. Daha sonrasında elde edilen çıktıyı Html e geri gönderdim ve alt tarafta gösterilmesini sağladım.<br>
Buradaki tek eksiğim satır bazında yazdırmak ve ajax üzerinde success de küçük bir dögü ile bunu başarıyorum.Çıktı olarak kontrol sağlayıp eğer komutun bir çıktısı varsa yazdırıyor.<br>
![image](https://user-images.githubusercontent.com/63595177/190248400-f00fafdb-eb33-48be-a3f0-9fa3776ae915.png)

## Çalıştırılan komut ve çıktılarını veritabanı üzerinde kayıt et
views.py içerisinde oluşturmuş olduğum model i kütüphane olarak kaydediyorum. Daha sonrasında models.py içerisinde değişken isimlerine göre yani p=viewer_cmd(cmd_input=degisken_giris,cmd_output=degisken_cıkıs) olarak veri tabanına ekleme yapıyoruz. Burada null değer olup olmadığını veritabanına eklemeden önce kontrol ediyoruz. <br>
![image](https://user-images.githubusercontent.com/63595177/190231747-4d861c9d-6b01-43a7-8029-8103ba53e17f.png) <br>
![image](https://user-images.githubusercontent.com/63595177/190231871-eddb46a5-ad03-44e5-abc9-72eb0bfb077f.png)<br>

##  Daha önce çalışmış komut ve çıktılarını gösterebileceğin bir alanda dashboarda ekle.
Bu işlemide views.py içerisinde models_func.objects.all().orderby('-id').[:10]
Son yapılan 10 kayıtı tabloya ekliyorum ve gösteriyoruz.

#### Not :
* Index sayfamda kullanılan tüm fonksiyonlar base.html içerisindedir.










