# Proje: Akademik Veri Seti ile Graf Analizleri

![Ekran görüntüsü 2025-01-04 042530](https://github.com/user-attachments/assets/b48acf5c-3901-47ec-80ae-c858c06d3ace)


## Proje Hakkında
Bu proje, yazarlar arasındaki iş birliği ilişkilerini modellemek ve bu model üzerinden veri yapısı ve algoritma konseptlerini uygulamak amacıyla geliştirilmiştir. Projede kısa yol bulma için Dijkstra, uzun yol bulma için DFS (Derinlik Öncelikli Arama) algoritmaları kullanılmıştır. Ayrıca kuyruğa ekleme ve çıkarma işlemleri bir İkili Arama Ağacı (BST) ile gerçekleştirilmiştir.

Projede HTML, CSS, ve JavaScript ile bir web arayüzü oluşturulmuş, Python'daki Webview API'si ile bu arayüz üzerinden algoritmalar etkileşimli olarak çalıştırılmıştır.

## Kullanılan Teknolojiler ve Araçlar
- **Python**: Algoritmaların geliştirilmesi ve veri işleme.
  - **Pandas**: Excel dosyalarından veri çekmek ve işlemek için.
  - **Pyvis**: Graf yapısının görselleştirilmesi için.
  - **webview API**: HTML tabanlı arayüz ile Python arasındaki etkileşimi sağlamak için.
- **HTML, CSS, JavaScript**: Web arayüzü tasarımı ve kullanıcı etkileşimleri.

## Proje Özellikleri
1. **Graf Oluşturma**:
   - Yazarları düğüm, iş birliği ilişkilerini kenar olarak temsil eden bir graf modeli oluşturulmuştur.
2. **Görselleştirme**:
   - Pyvis kullanılarak graf görselleştirilmiştir.
   - Alt grafiklerin HTML formatında sunumu sağlanmıştır.
3. **Kısa ve Uzun Yol Hesaplama**:
   - **Dijkstra** algoritması ile en kısa yol hesaplamaları yapılmıştır.
   - **DFS** algoritması ile belirli bir düğümden en uzun yol hesaplanmıştır.
4. **BST İşlemleri**:
   - En kısa yol verileri kullanılarak bir İkili Arama Ağacı (BST) oluşturulmuş, düğüm ekleme ve silme işlemleri gerçekleştirilmiştir.
5. **Dinamik Web Arayüzü**:
   - Kullanıcı, web arayüzündeki butonlar ile algoritmaları çalıştırabilir ve sonuçları görselleştirebilir.

## Algoritmalar
### 1. Dijkstra Algoritması
Graf üzerindeki iki düğüm arasındaki en kısa yolu hesaplamak için kullanılmıştır. Kuyruk yapısı ile en küçük mesafeli düğümler işlenmiştir.

### 2. DFS (Derinlik Öncelikli Arama)
Belirli bir düğümden başlayarak en uzun yolu bulmak için uygulanmıştır. LIFO prensibi ile çalışarak tüm yolları derinlemesine taramıştır.

### 3. İkili Arama Ağacı (BST)
En kısa yol sonuçlarının saklanması ve işlemleri için BST kullanılmıştır. Kuyruğa ekleme ve çıkarma işlemleri verimli bir şekilde gerçekleştirilmiştir.

## Kullanım Talimatları
1. **Veri Yükleme**: Excel dosyasındaki veri, Python betiği ile okunur ve graf oluşturulur.
2. **Arayüz Başlatma**: `webview` modülü ile web arayüzü başlatılır.
3. **Algoritmaları Çalıştırma**:
   - Web arayüzünde ilgili butona tıklayarak Dijkstra veya DFS algoritmasını başlatabilirsiniz.
4. **Sonuçların Görselleştirilmesi**:
   - Pyvis ile görselleştirilen graf sonuçları tarayıcıda görüntülenir.

## Deneysel Sonuçlar ve Karşılaşılan Zorluklar
- **Performans Sorunları**: Python'un yorumlanan bir dil olması nedeniyle büyük veri kümelerinde yavaşlık yaşanmıştır.
- **Görselleştirme Sorunları**: Tarayıcı tabanlı Pyvis görselleştirmeleri, büyük graf dosyalarında çökme sorunlarına yol açmıştır.Ardından veri setinin küçülmesi ile bu sorunlar giderilmiştir.

## Geliştiriciler
- **Sadık Gölpek**: Algoritmaların geliştirilmesi ve görselleştirme süreçleri.
- **Abdullah Önder**: Graf yapısının oluşturulması ve modelleme.

## Lisans
Bu proje **MIT Lisansı** altında sunulmaktadır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasını inceleyebilirsiniz.
