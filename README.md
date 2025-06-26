# 🏡 Konut Fiyat Tahmin Sistemi

## 📌 Proje Tanıtımı

Bu proje, Bursa iline ait konut satış verilerini kullanarak makine öğrenmesi tabanlı bir fiyat tahmin sistemi geliştirmeyi amaçlamaktadır. Gerçek hayattan elde edilen veriler çeşitli veri işleme ve öznitelik mühendisliği adımlarından geçirilmiş, ardından farklı regresyon modelleri ile değerlendirilmiştir. En yüksek başarıyı sağlayan model (XGBoost) ile tahminleme sistemi kurulmuştur.

Proje sonunda geliştirilen sistem, kullanıcıların belirli konut özelliklerini (ilçe, mahalle, metrekare, bina yaşı, ısıtma tipi vb.) girdikleri bir arayüz üzerinden tahmini konut fiyatını öğrenmelerine imkân tanımaktadır. Bu arayüz, Python diliyle yazılmış ve **Streamlit** kütüphanesi kullanılarak görselleştirilmiştir.

## 🎯 Proje Amaçları

- Web scraping ile güvenilir bir emlak veri seti oluşturmak
- Veriyi temizleyip analiz ederek içgörü elde etmek
- Farklı makine öğrenmesi modellerini karşılaştırmak
- En iyi modeli seçip optimize etmek
- Tahmin sürecini görsel ve etkileşimli bir arayüzle sunmak

##  Kullanılan Teknolojiler ve Kütüphaneler

- **Python 3.10+**
- **pandas, numpy, seaborn, matplotlib** (Veri işlemleri ve görselleştirme)
- **scikit-learn, XGBoost, Random Forest, ElasticNet CatBoost, LightGBM, Optuna** (Makine öğrenmesi)
- **Streamlit** (Web arayüzü)
- **Selenium** (Web scraping)

  
---


  
## 1-) Verinin Çekilmesi (Web Scraping)

Bu projenin ilk adımında, **Bursa ilinin ilçelerine ait satılık konut ilanları** [EmlakJet.com](https://www.emlakjet.com) üzerinden Python ve Selenium kullanılarak otomatik olarak çekilmiştir. Kod, **Jupyter Notebook** ortamında yazılmış olup, veri çekme işlemleri adım adım çalıştırılabilir.

###  **Kullanılan Teknolojiler ve Kütüphaneler**
- **Python 3.10**: Proje dili olarak tercih edilmiştir.
- **Selenium**: Tarayıcı otomasyonu için kullanılır. EmlakJet web sitesinden verileri toplamak için kullanıldı. ChromeDriver ile birlikte çalışır.
- **Pandas**: Çekilen verileri düzenlemek, işlemek ve Excel dosyasına kaydetmek için kullanılır.
- **openpyxl**: Veriyi Excel dosyasına yazmak için kullanılır.
- **ChromeDriver**: Selenium ile tarayıcıyı kontrol etmek için kullanılır.

###  **Kodun Çalışma Mantığı**
1. **WebDriver Ayarları**: 
   - `chromedriver` ile Google Chrome tarayıcısı açılır.
   - `Options` kullanılarak, tarayıcının user-agent'ı özelleştirilir ve Jupyter Notebook üzerinden tarayıcı başlatılır.
   - `Service` ve `WebDriverWait` kullanılarak, sayfaların yüklenmesi için 10 saniye beklenir.

2. **URL Listesi ve Sayfa Sayısı**:
   - Her ilçeye ait **URL**'ler ve o ilçedeki sayfa sayısı belirlenir. Bu sayfalarda her bir ilan sayfası otomatik olarak ziyaret edilir.
   - Her sayfa üzerinden ilan bilgileri toplanır.

3. **Veri Çekme İşlemi**:
   - Selenium kullanılarak, her ilanın detay sayfasına girilir. 
   - `find_element` ve `find_elements` metotlarıyla, sayfada yer alan fiyat, m², oda sayısı gibi bilgiler çekilir.
   - İlanın konumu (İl, İlçe, Mahalle) ayrıştırılarak, **string işlemleri** ile parçalanır.

4. **Site Durumu Kontrolü**:
   - Sayfa üzerinde "Site İçerisinde" gibi etiketler kontrol edilerek, ilanların site içinde olup olmadığına karar verilir.

5. **Verilerin Kaydedilmesi**:
   - Çekilen her ilan verisi bir **dictionary** yapısına kaydedilir.
   - Veriler, Pandas DataFrame'e dönüştürülür ve `to_excel` fonksiyonu ile Excel dosyasına kaydedilir.

###  **Teknik Detaylar ve Performans**
- **Sayfalar Arası Gezinme**: 
   - Her ilçeye ait **sayfa sayısı** belirli bir sınırda tutulmuştur (örneğin, Nilüfer ilçesi 50 sayfa). Bu, sitenin limitlerini aşmamak ve verinin doğruluğunu korumak içindir.
   - Sayfa başına ortalama **36 ilan** çekilmektedir. Bu sayede aşırı yüklenmeden veri toplanmıştır.

- **Bekleme Stratejisi**: 
   - `WebDriverWait` ve `EC.presence_of_all_elements_located` kullanılarak, her sayfa tamamen yüklendikten sonra veriler çekilmeye başlanır. Bu, **dinamik web sayfalarında** verilerin eksik ya da hatalı çekilmesini engeller.
   - `time.sleep(1)` gibi komutlarla, her sayfa arasında kısa beklemeler yapılır.

- **Veri İstikrarı**:
   - Veritabanındaki **boş linkler** veya **geçersiz ilanlar** kontrol edilerek, sadece geçerli veriler çekilir. 
   - Hatalı sayfalarda `try-except` blokları kullanılarak, hata durumunda kod çalışmaya devam eder.

###  **Çıktı:**
- **Excel Dosyası**: 
   - Veriler `"DENEMEVERİLER.xlsx"` dosyasına kaydedilir.
   - Excel dosyasındaki her satır bir ilanı temsil eder ve **toplamda 12 farklı veri sütunu** bulunmaktadır.

###  **Önemli Notlar**:
- **Sayfa Sayısı Sınırlamaları**: EmlakJet'in bazı ilçelerinde, sayfa sayısının 50'yi geçtiği durumlarda, sistem **sayfa başa dönme problemi** yaşayabilir. Bu, belirli ilçelerde dikkat edilmesi gereken bir durumdur.
- **IP Kısıtlamaları**: Web scraping işlemi sırasında IP kısıtlamalarına karşı önlem almak için, zaman zaman **bekleme sürelerini artırmak** ve **proxy kullanmak** önerilir.

###  **Örnek Veri Çıktısı**:

| Fiyat        | Net m² | Brüt m² | Oda Sayısı | Bina Yaşı | Kat   | Toplam Kat | Isıtma Tipi | İl    | İlçe    | Mahalle   | Site İçinde mi? |
|--------------|--------|---------|------------|-----------|-------|------------|-------------|-------|---------|-----------|-----------------|
| 2.500.000 TL | 110    | 130     | 3+1        | 5         | 2.Kat | 5 Katlı    | Kombi       | Bursa | Nilüfer | İhsaniye | Evet            |

---




## 2-) Veriyi Hazırlama (Temizleme ve Dönüştürme)

Bu aşamada, web scraping ile elde edilen ham veriler **veri temizleme, dönüştürme ve eksik veri tamamlama** işlemlerine tabi tutulmuştur. Tüm adımlar, **Jupyter Notebook** ortamında çalıştırılmış ve `pandas` kütüphanesi ile gerçekleştirilmiştir.

###  Amaç
- Tekrarlayan ve hatalı kayıtları silmek
- Metinsel verileri sayısal forma dönüştürmek
- Eksik değerleri analiz edip uygun biçimde doldurmak
- Modellemeye uygun, tutarlı bir veri seti elde etmek

###  Uygulanan İşlemler

1. **Kopya Verilerin Silinmesi**  
   - `drop_duplicates()` ile aynı ilanlar kaldırıldı.

2. **Fiyat ve Metrekare Temizliği**  
   - `Fiyat`, `Net m²`, `Brüt m²` sütunlarından `TL`, `m²`, `.` gibi karakterler temizlendi ve sayısal değerlere çevrildi.

3. **Oda ve Salon Ayrıştırması**  
   - `3+1` formatındaki değerler iki ayrı sütun olarak `Oda` ve `Salon` biçiminde ayrıldı.

4. **Bina Yaşı Normalizasyonu**  
   - `"Yeni"` değerleri `0` olarak alındı, `"5-10"` gibi aralıklar ortalaması alınarak dönüştürüldü, `"21 ve üzeri"` gibi ifadeler sayıya çevrildi.

5. **Hatalı Isıtma Tipi Düzeltmeleri**  
   - Bazı ilanlarda `Isıtma Tipi` bilgisi `Toplam Kat` sütununa karışmıştı. Bu satırlar tespit edilerek doğru sütuna taşındı.

6. **Kat Bilgisi Sayılaştırma**  
   - `Bahçe`, `Zemin`, `Çatı`, `Dubleks` gibi ifadeler sayısal kat numaralarına çevrildi (`0` veya `Toplam Kat`).

7. **Eksik Değer Doldurma**  
   - `Kat (Sayı)` için mod ile doldurma yapıldı.
   - `Toplam Kat` eksikleri, `Kat (Sayı) + 1` kuralıyla tamamlandı.

8. **Site Durumu Dengeleme**  
   - `Toplam Kat ≥ 4` ve `Site İçinde mi? = Hayır` olan bazı veriler, **gerçek oranlara göre** yeniden dengelendi.

9. **Isıtma Tipi Atamaları (Eksik Değerler İçin)**  
   - `Isıtma Tipi` eksik olan satırlara, sitedeki genel dağılıma göre rastgele şu oranlarla veri atandı:
     - Kombi Doğalgaz (%63.03)
     - Merkezi Doğalgaz (%22)
     - Isıtma Yok (%14.97)

10. **Gereksiz Sütunların Silinmesi**  
    - `Kat` ve `Oda Sayısı` gibi analizde tekrarlanan veya türevlenen sütunlar kaldırıldı.

11. **Yeni Dosyanın Kaydedilmesi**  
    - Temizlenmiş ve işlenmiş veri `temizVeri_Bursa.xlsx` adlı dosyaya kaydedildi.

###  Çıktı:
- `"temizVeri_Bursa.xlsx"`: Modelleme ve analiz işlemlerine uygun, eksiksiz ve temiz veri seti.

###  Önemli Notlar
- Veriler hem eksik değer analizi (`isnull().sum()`), hem de tekrar eden kayıtlar (`duplicated`) açısından kontrol edilmiştir.
- Sayısallaştırma işlemleri (örneğin: `Kat`, `Oda`, `Isıtma`) model uyumluluğu düşünülerek yapılmıştır.

---

## 3-) Veri Görselleştirme 

Bu aşamada, temizlenmiş ve dönüştürülmüş konut verileri üzerinde çeşitli görselleştirme teknikleri kullanılarak verinin genel yapısı analiz edilmiştir. Görselleştirmeler Python'da `matplotlib` ve `seaborn` kütüphaneleri ile yapılmıştır.

###  Amaç  
- Değişkenler arasındaki ilişkiyi keşfetmek  
- Aykırı değerleri ve genel dağılımları tespit etmek  
- İlçelere, katlara, metrekareye ve bina yaşına göre fiyat farklarını görsel olarak yorumlamak

###  Uygulanan İşlemler

**Veri Ön Kontrolü**  
- `df.info()`, `df.describe()`, `df.isnull().sum()` gibi temel analiz fonksiyonları ile veri incelendi.  
- Fiyat sütununda 35 milyon TL üzeri değerler veri dışı bırakıldı.

**Korelasyon Matrisi**  
- Sayısal değişkenler arası korelasyon `df.corr()` ile hesaplandı.  
- `sns.heatmap()` ile görsel ısı haritası oluşturularak ilişki dereceleri analiz edildi.

**İlçelere Göre Ortalama Fiyat**  
- `sns.barplot()` ile her ilçedeki ortalama konut fiyatları karşılaştırıldı.  
- Ayrıca her ilçe için ayrı ayrı `sns.histplot()` kullanılarak fiyat dağılımı grafikleri üretildi.

**Net m² ile Fiyat İlişkisi**  
- `plt.scatter()` kullanılarak Net m² ile Fiyat ilişkisi görselleştirildi.  
- Aykırı değerler filtrelenerek daha temiz bir dağılım elde edildi.

**Oda Sayısına Göre Fiyat**  
- `sns.barplot()` ile oda sayısı arttıkça ortalama fiyatın nasıl değiştiği analiz edildi.

**Kat Bilgisine Göre Fiyat Dağılımı**  
- `sns.boxplot()` ile "Kat (Sayı)" değişkeni ile "Fiyat" arasındaki dağılım analiz edildi.  
- 0-20 kat arası değerler kullanılarak uç değerler elendi.

**Bina Yaşı ve Fiyat İlişkisi**  
- `plt.plot()` ile bina yaşı arttıkça ortalama fiyatın nasıl değiştiği grafikle gösterildi.

**Çoklu Değişken İlişkisi**  
- `sns.pairplot()` ile Fiyat, Net m², Brüt m², Oda, Salon ve Bina Yaşı değişkenleri arasındaki ilişkiler topluca görselleştirildi.

###  Notlar  
- Grafiklerin görünürlüğünü artırmak için `figsize`, `tight_layout` gibi ayarlamalar yapıldı.  
- Fiyat sütununa uygulanan filtreleme (35M TL üstü ayıklama) tüm görselleştirme işlemleri öncesinde tekrarlandı.  
- Görselleştirmeler sırasında eksik veriler dikkate alınmadı veya önceden işlenmiş hali kullanıldı.

---

## 4-) Makine Öğrenmesi 

Bu aşamada, konut fiyat tahmini amacıyla çeşitli makine öğrenmesi modelleri uygulanmış ve sonuçları karşılaştırılmıştır. Tüm işlemler Jupyter Notebook ortamında gerçekleştirilmiştir.

###  Amaç
- Emlak verileri üzerinden fiyat tahmini yapmak
- Farklı regresyon algoritmalarının performansını değerlendirmek
- Log dönüşümü ve uygun encoding işlemleriyle modeli iyileştirmek

###  Uygulanan Adımlar

**Veri Hazırlığı**
- Temizlenmiş veriler `temizVeri_Bursa.xlsx` dosyasından yüklendi.
- `İl` sütunu çıkarıldı, eksik değerler ve 35 milyon TL üzerindeki aykırı fiyatlar elendi.
- Hedef değişken olarak `Fiyat` logaritmik dönüşüme tabi tutuldu (`log1p`).

**Özellik Mühendisliği ve Encoding**
- Kategorik sütunlar: `Isıtma Tipi`, `İlçe`, `Mahalle`, `Site İçinde mi?`
- Bu sütunlar **TargetEncoder** ile sayısal forma dönüştürüldü.
- Sayısal sütunlar ise **StandardScaler** ile ölçeklendirildi.
- Bütün bu işlemler `ColumnTransformer` içinde birleştirildi.

**Kullanılan Modeller**
- Random Forest Regressor
- CatBoost Regressor
- XGBoost Regressor
- LightGBM Regressor
- ElasticNet Regressor

**Pipeline Oluşturma**
- Her model için ayrı `Pipeline` tanımlandı.
- Pipeline: Ön işlem (`prep`) + Model (`model`) adımlarından oluştu.
- Tüm modeller ortak veri seti ile aynı ön işlemden geçirildi.

**Veri Seti Bölme**
- Veri seti %80 eğitim, %20 test olarak ayrıldı.
- `train_test_split` ile ayrım yapıldı ve rastgelelik sabitlendi (`random_state=42`).

**Model Eğitimi ve Değerlendirme**
- Tüm modeller sırasıyla eğitildi ve test verisi üzerinde tahmin yapıldı.
- Tahminler `expm1()` ile log dönüşümünden geri çevrildi.
- Kullanılan performans metrikleri:
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)
  - R² (Determination Coefficient)

**Sonuçlar**  
Aşağıdaki tablo, tüm modellerin performans kıyaslamasını göstermektedir:

| Model        | RMSE         | MAE          | R² Score   |
|--------------|--------------|--------------|------------|
| RandomForest | 2,271,019    | 1,103,704    | 0.624      |
| CatBoost     | 2,193,628    | 1,040,914    | 0.649      |
| XGBoost      | 2,165,644    | 1,025,246    | 0.658      |
| LightGBM     | 2,180,148    | 1,032,308    | 0.653      |
| ElasticNet   | 3,794,315    | 2,037,110    | -0.050     |


(*Not: Gerçek sonuçlar çalışma sırasında oluşan `results_df` üzerinden görüntülenir.*)

###  Notlar
- Hedef değişkenin logaritması alınarak model kararlılığı artırılmıştır.
- Target encoding yöntemi sayesinde kategorik değişkenler, modele bilgi taşır şekilde dönüştürülmüştür.
- Tüm modeller aynı veri ve pipeline üzerinden test edilerek adil bir kıyaslama sağlanmıştır.

---

## 5-) Model Optimizasyonu ve Kaydetme

Bu bölümde, önceki modelleme adımlarına ek olarak **özellik mühendisliği**, **Optuna ile hiperparametre optimizasyonu**, ve **final modelin kaydedilmesi** işlemleri gerçekleştirilmiştir.

### Amaç
- XGBoost modelinin performansını artırmak için en uygun hiperparametreleri otomatik olarak bulmak
- Yeni özellikler oluşturarak modelin açıklayıcılığını artırmak
- Eğitim sonucunda elde edilen modeli `.pkl` dosyası olarak kaydetmek

### Yapılan İşlemler

**Veri Yükleme ve Temizleme**
- `temizVeri_Bursa.xlsx` dosyasından veri yüklendi
- `İl` sütunu çıkarıldı
- Eksik ve aykırı veriler elendi (`Fiyat < 35M`)

**Özellik Mühendisliği**
- Yeni özellikler oluşturuldu:
  - `Toplam_Oda_Salon` → Oda + Salon
  - `Kullanim_Orani` → Net m² / Brüt m²
  - `Kat_Orani` → Kat / Toplam Kat
  - `Bina_Yasi_Log` → log1p dönüşümü
  - `m2_basi_fiyat` → Fiyat / Net m²
- Hedef değişken olarak `Fiyat_Log` kullanıldı

**Encoding ve Ölçekleme**
- Kategorik sütunlar: `Isıtma Tipi`, `İlçe`, `Mahalle`, `Site İçinde mi?`
- `TargetEncoder` ile sayısal forma dönüştürüldü
- Sayısal sütunlar `StandardScaler` ile ölçeklendirildi
- Tüm işlemler `ColumnTransformer` içinde birleştirildi

**Optuna ile Hiperparametre Optimizasyonu**
- 30 deneme (trial) ile en iyi `XGBoost` hiperparametreleri bulundu
- Hedef: 3-fold CV ile ortalama R² skorunu maksimize etmek
- Optuna'nın önerdiği en iyi parametrelerle final model oluşturuldu

**Eğitim ve Test Ayrımı**
- Veri %80 eğitim ve %20 test seti olarak ayrıldı
- `Pipeline` kullanılarak model eğitildi

**Model Değerlendirmesi**
- Tahminler `log` formdan `TL` cinsine çevrildi
- Performans metrikleri hesaplandı:
  - R² (Determinasyon Katsayısı)
  - RMSE (Ortalama Kare Kök Hatası)
  - MAE (Ortalama Mutlak Hata)

**Model Performansı (Test Verisi)**


 Test R² : 0.9657
 Test RMSE: 685,451 TL
 Test MAE : 158,607 TL

 
**Görselleştirme**
- Gerçek ve tahmin fiyatları `scatterplot` ile karşılaştırıldı
- Gerçek fiyata yakın tahminler çizgi üzerine yakın düşerken, sapmalar yukarıdan/sağdan ayrıldı
- Fiyat arttıkça tahmin sapmaları da artış göstermeye başladı

**Modelin Kaydedilmesi**
- Final `Pipeline` yapısı `joblib.dump()` ile `"XGBoost_model.pkl"` dosyasına kaydedildi
- Model dosyası daha sonra Streamlit gibi bir arayüzde kolayca yüklenebilir

### Notlar
- Optuna, hiperparametre aramasını otomatikleştirerek zaman kazandırmıştır
- Özellik mühendisliği ile modelin öğrenebileceği daha anlamlı temsiller oluşturulmuştur
- Logaritmik hedef dönüşümü, büyük değerlerdeki varyansı azaltarak daha dengeli bir model sağlamıştır

---

## 6-) Arayüz (Streamlit)

Bu adımda, eğitim sonucunda elde edilen XGBoost modelini kullanarak kullanıcıdan alınan verilerle **interaktif fiyat tahmini** yapılabilen bir web arayüzü geliştirilmiştir. Arayüz, Python tabanlı **Streamlit** kütüphanesi ile oluşturulmuştur.

###  Amaç
- Kullanıcının girdiği konut bilgilerine göre tahmini satış fiyatını hesaplamak
- Tahmin sürecini anlaşılır ve kullanıcı dostu bir arayüzle sunmak

###  Özellikler

- İlçe ve mahalle seçimi dinamik olarak güncellenir
- Oda, salon, metrekare, kat, ısıtma tipi, bina yaşı ve site durumu gibi tüm parametreler kullanıcıdan alınır
- Kullanıcının girdiği verilere dayanarak gerekli **feature engineering** işlemleri arka planda otomatik olarak yapılır:
  - `Kullanim_Orani` → Net m² / Brüt m²
  - `Kat_Orani` → Kat / Toplam Kat
  - `Bina_Yasi_Log` → log1p dönüşümü
  - `Toplam_Oda_Salon` → Oda + Salon
  - `m2_basi_fiyat` → Ortalama değer olarak sabitlenmiştir (35581.88)

- Model tahmini logaritmik skordan TL cinsine çevrilir (`np.expm1`)

### Kullanım Adımları

1. Terminalde aşağıdaki komutla uygulamayı çalıştırın:

streamlit run gui.py



2. Tarayıcınızda otomatik olarak açılan sayfada aşağıdaki adımları izleyin:
   - İlçe ve mahalle seçin
   - Oda sayısı, metrekare bilgileri ve diğer detayları girin
   - "Tahmini Hesapla" butonuna tıklayın

3. Uygulama tahmini fiyatı aşağıdaki gibi gösterir:

 Tahmini Satış Fiyatı: 2,430,000 TL



###  Notlar

- Arayüzde kullanılan `model = joblib.load("XGBoost_model.pkl")` komutu ile daha önce eğitilmiş model yüklenir
- Ortalama m² başı fiyat (`m2_basi_fiyat`) sabit tutulmuştur; arayüzün sadeleştirilmiş versiyonudur
- Girdi verilerinin tutarlılığı ve eksiksizliği, modelin doğru çalışması için önemlidir

---

