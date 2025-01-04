import pandas as pd
from pyvis.network import Network
import json
import webview
import os
# Manuel grafiği oluşturmak icin graf classimiz
class Graf:
    def __init__(self):
        self.nodes = {}  # Yazarları temsil eden düğüm yapısı
        self.edges = []  # Ortak makaleleri temsil eden kenar yapısı
        self.komsu_listesi = {}  # Komşuluk listesi

    def add_node(self, dugum_id, etiket=None, boyut=100, color="blue", bilgi="", agirlik=0):  # Düğüm ekleme
        if dugum_id not in self.nodes:
            self.nodes[dugum_id] = {
                "etiket": dugum_id,
                "boyut": boyut,
                "color": color,
                "bilgi": bilgi,
                "agirlik": agirlik,  # Düğüm ağırlığı (makale sayısı)
            }
            self.komsu_listesi[dugum_id] = []

    def add_edge(self, kaynak, hedef, agirlik=1):  # Kenar ekleme
        self.edges.append((kaynak, hedef, agirlik))
        self.komsu_listesi[kaynak].append((hedef, agirlik))
        self.komsu_listesi[hedef].append((kaynak, agirlik))


class BSTNode:
    def __init__(self, key, icerik):
        self.key = key
        self.icerik = icerik
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, icerik):
        self.root = self._insert(self.root, key, icerik)

    def _insert(self, node, key, icerik):
        if not node:
            return BSTNode(key, icerik)
        if key < node.key:
            node.left = self._insert(node.left, key, icerik)
        else:
            node.right = self._insert(node.right, key, icerik)
        return node

    def inorder(self):
        sonuc = []
        self._inorder(self.root, sonuc)
        return sonuc

    def _inorder(self, node, sonuc):
        if node:
            self._inorder(node.left, sonuc)
            sonuc.append((node.key, node.icerik))
            self._inorder(node.right, sonuc)

    def sil(self, key):
        self.root = self._sil(self.root, key)

    def _sil(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._sil(node.left, key)
        elif key > node.key:
            node.right = self._sil(node.right, key)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # Node with two children: Get inorder successor
            temp = self._min_dugum_bul(node.right)
            node.key = temp.key
            node.icerik = temp.icerik
            node.right = self._sil(node.right, temp.key)
        return node

    def _min_dugum_bul(self, node):
        mevcut = node
        while mevcut.left:
            mevcut = mevcut.left
        return mevcut





class Api:
    def __init__(self, graph):
        self.graph = graph
        self.minimum_mesafe = None
        self.kisa_yol_sozluk = None
        self.en_kisa_mesafe = None

    def enkisayolHesapla(self, start, end):
        # En kısa yolu hesapla
        yol, mesafe, yol_sozluk = en_kisa_yol(self.graph, start, end)
        if yol:
            self.minimum_mesafe = yol
            self.kisa_yol_sozluk = yol_sozluk
            self.en_kisa_mesafe = mesafe
            return f"En kısa yol: {' -> '.join(yol)}\nToplam mesafe: {mesafe}"
        else:
            self.minimum_mesafe = None
            self.kisa_yol_sozluk = None
            self.en_kisa_mesafe = None
            return "Başlangıç ve bitiş arasında uygun bir yol bulunamadı."

    def kisa_yol_gorsellestir(self):
        if not self.minimum_mesafe or not self.kisa_yol_sozluk:
            return "En kısa yol hesaplanmamış. Önce en kısa yolu hesaplayın."
    
        # Pyvis grafiğini oluştur
        ag = pyvis_gorsellestirme(self.graph)
        print("Kırmızı kenarlar (en kısa yol):", self.kisa_yol_sozluk)

        for kaynak, hedef in self.kisa_yol_sozluk.items():
            kaynak_temizle = str(kaynak).strip("'")  # Tırnakları kaldır
            hedef_temizle = str(hedef).strip("'")  # Tırnakları kaldır
        
            # Düğüm grafikte yoksa, önce düğümü ekle
            if kaynak_temizle not in ag.get_nodes():
                ag.add_node(kaynak_temizle)
            if hedef_temizle not in ag.get_nodes():
                ag.add_node(hedef_temizle)
        
            print(f"Kırmızı kenar ekleniyor: {kaynak_temizle} -> {hedef_temizle}")
            ag.add_edge(kaynak_temizle, hedef_temizle, color="red", width=6)

    
        # Görselleştirmeyi tam bir yol belirterek kaydet
        yazilacak_dosya = os.path.join(os.getcwd(), "C:\\Users\\sadik\\Desktop\\KOU CENG 2\\Prolab\\Prolab3\\1.ister.html")
        ag.write_html(yazilacak_dosya)
        return f"En kısa yol görselleştirildi ve {yazilacak_dosya} dosyasına kaydedildi."

        
        
    def enuzunyolHesapla(self, start):
        # En uzun yol fonksiyonunu çağır
        en_uzun_yol = self.en_uzun_yol_hesapla(start)
        if en_uzun_yol:
            return f"En uzun yol: {' -> '.join(en_uzun_yol)}\nGeçilen düğüm sayısı: {len(en_uzun_yol)}"
        else:
            return "Başlangıç yazarı graf içinde bulunamadı veya bağlantı yok."
   

    def en_uzun_yol_hesapla(self, baslangic_id):
        # Yazarın graf içinde olup olmadığını kontrol et
        if baslangic_id not in self.graph.komsu_listesi:
            return None

        def dfs(node, bakilanlar):
            bakilanlar.add(node)
            max_path = []

            for yan_dugum, _ in self.graph.komsu_listesi[node]:
                if yan_dugum not in bakilanlar:
                    path = dfs(yan_dugum, bakilanlar)
                    if len(path) > len(max_path):
                        max_path = path

            bakilanlar.remove(node)
            return [node] + max_path

        bakilanlar = set()
        return dfs(baslangic_id, bakilanlar) 




     
    
    def isbirlikKuyruguOlustur(self, orcid):
        if orcid not in self.graph.nodes:
            return f"Yazar ID bulunamadı: {orcid}"
    
        kuyruk = []
        islenen = set()
    
        # İşbirlikçi yazarları kuyrukta sıralama
        for komsu, _ in self.graph.komsu_listesi[orcid]:
            if komsu not in islenen:
                islenen.add(komsu)
                kuyruk.append((self.graph.nodes[komsu]["agirlik"], komsu))
    
        kuyruk.sort(reverse=True, key=lambda x: x[0])
    
    
        net = Network(directed=True)  # Yönlü grafik olacak şekilde ayarla
    
        onceki_dugum = None  # Kuyrukta önceki düğümü takip et
        for agirlik, komsu in kuyruk:
            net.add_node(komsu, label=f"{komsu}\n(Ağırlık: {agirlik})", size=20)
            if onceki_dugum:
                net.add_edge(onceki_dugum, komsu, color="blue", width=2)  # Kuyruk bağlantısı oluştur
            onceki_dugum = komsu  # Bir sonraki bağlantı için güncelle
    
        # Görselleştirme dosyasını kaydet
        yazilacak_dosya = "C:\\Users\\sadik\\Desktop\\KOU CENG 2\\Prolab\\Prolab3\\2.ister.html"
        net.write_html(yazilacak_dosya)
    
        kuyruk_str = "\n".join([f"Yazar: {yazar}, Ağırlık: {agirlik}" for agirlik, yazar in kuyruk])
        return f"Kuyruk başarıyla görselleştirildi: {yazilacak_dosya}\n\nKuyruk:\n{kuyruk_str}"




    def BSTolusturVeGorsellestir(self, remove_id):
        if not self.minimum_mesafe or not self.kisa_yol_sozluk:
            return "En kısa yol hesaplanmamış. Önce 1. butona tıklayarak en kısa yolu hesaplayın."
    
        if remove_id not in self.minimum_mesafe:
            return f"{remove_id} ID'si en kısa yol içinde bulunamadı."
    
        # BST'yi oluştur
        bst = BST()
        for i, yazar in enumerate(self.minimum_mesafe):
            bst.insert(i, yazar)
    
        # Kullanıcıdan alınan yazar ID'sini sil
        silinecek_indeks = self.minimum_mesafe.index(remove_id)
        bst.sil(silinecek_indeks)
    
        # BST'nin sıralı (inorder) durumu
        bst_sirasi = bst.inorder()
    
        # Pyvis görselleştirme
        from pyvis.network import Network
        net = Network(directed=True)
        
        # BST'yi Pyvis grafiği olarak ekle
        def kenarEkleBST(node):
            if not node:
                return
            net.add_node(node.key, label=str(node.icerik))
            if node.left:
                net.add_node(node.left.key, label=str(node.left.icerik))
                net.add_edge(node.key, node.left.key)
                kenarEkleBST(node.left)
            if node.right:
                net.add_node(node.right.key, label=str(node.right.icerik))
                net.add_edge(node.key, node.right.key)
                kenarEkleBST(node.right)
    
        # Kök düğümden başlayarak ağ yapısını oluştur
        kenarEkleBST(bst.root)
    
        # Pyvis dosyasını yazdır
        yazilacak_dosya = "C:\\Users\\sadik\\Desktop\\KOU CENG 2\\Prolab\\Prolab3\\3.ister.html"
        net.write_html(yazilacak_dosya)
    
        return f"BST başarıyla oluşturuldu ve görselleştirildi. İnorder Traversal: {bst_sirasi}\nGörselleştirme: {yazilacak_dosya}"



    def isbirlikYollariHesapla(self, author_id):
        if author_id not in self.graph.nodes:
            return f"Yazar ID bulunamadı: {author_id}"
    
        # Alt graf oluştur
        altgraf = self.isbirligiGrafiOlustur(author_id)
    
        # Alt grafiği görselleştir
        gorsel_mesaji = self.altgrafiGorsellestir(altgraf)
    
        # Alt graf içindeki en kısa yolları hesapla
        enKisaYolTablosu = self.tumEnKisaYollariHesapla(altgraf)
    
        # Sonuçları döndür
        return f"İşbirlikçi Graf ve En Kısa Yollar:\n{enKisaYolTablosu}\n\n{gorsel_mesaji}"
    
    
    def isbirligiGrafiOlustur(self, author_id):
        # Alt graf oluştur
        altgraf = Graf()
    
        # Ana yazar ve işbirlikçilerini ekle
        altgraf.add_node(author_id, **self.graph.nodes[author_id])
        for yan_dugum, agirlik in self.graph.komsu_listesi[author_id]:
            altgraf.add_node(yan_dugum, **self.graph.nodes[yan_dugum])
            altgraf.add_edge(kaynak=author_id, hedef=yan_dugum, agirlik=agirlik)
    
            # İşbirlikçilerin işbirlikçilerini ekle
            for alt_dugum, alt_agirlik in self.graph.komsu_listesi[yan_dugum]:
                if alt_dugum != author_id:
                    altgraf.add_node(alt_dugum, **self.graph.nodes[alt_dugum])
                    altgraf.add_edge(kaynak=yan_dugum, hedef=alt_dugum, agirlik=alt_agirlik)
    
        return altgraf
    
    
    def tumEnKisaYollariHesapla(self, altgraf):
        # Alt graf içindeki tüm düğümler arasında en kısa yolları hesapla
        tumEnKisaYollar = {}
        for kaynak_dugum in altgraf.nodes:
            en_kisa_yollar = {}
            for son_dugum in altgraf.nodes:
                if kaynak_dugum != son_dugum:
                    path, uzaklik, _ = en_kisa_yol(altgraf, kaynak_dugum, son_dugum)  # Üçüncü değeri görmezden gel
                    en_kisa_yollar[son_dugum] = {
                        "path": path if path else "Yol bulunamadı",
                        "uzaklik": uzaklik if uzaklik != float('inf') else "Ulaşılamaz"
                    }
            tumEnKisaYollar[kaynak_dugum] = en_kisa_yollar
    
        # Tabloyu oluştur
        sonuc = []
        for node, paths in tumEnKisaYollar.items():
            sonuc.append(f"{node}:\n" + "\n".join(
                [f"  -> {son_dugum}: Yol: {details['path']}, Mesafe: {details['uzaklik']}" for son_dugum, details in paths.items()]
            ))
        return "\n".join(sonuc)

    
    
    def altgrafiGorsellestir(self, altgraf):
        from pyvis.network import Network
    
        # PyVis grafiği oluştur
        net = Network(directed=True)
        for node, ozellikler in altgraf.nodes.items():
            net.add_node(node, label=node, **ozellikler)
    
        for kaynak, baglantilar in altgraf.komsu_listesi.items():
            for hedef, agirlik in baglantilar:
                net.add_edge(kaynak, hedef, label=str(agirlik))
    
        # Görselleştirme dosyasını kaydet
        yazilacak_dosya = "C:\\Users\\sadik\\Desktop\\KOU CENG 2\\Prolab\\Prolab3\\4.ister.html"
        net.write_html(yazilacak_dosya)
        return f"Alt graf görselleştirildi ve {yazilacak_dosya} dosyasına kaydedildi."



# Excel dosyasını okuma
def read_excel(excel_dosya):
    return pd.read_excel(excel_dosya) ## pandas ozel fonksiyonu ile dosyayi okur

# Ortalama makale sayısına göre düğüm özelliklerini belirleme
def dugum_ozellikleri_hesabi(benzersiz_orcid_sayisi, ortalama_makale_sayisi):
    ozellikler = {}
    for yazar, sayi in benzersiz_orcid_sayisi.items():
        if sayi > ortalama_makale_sayisi * 1.2:
            ozellikler[yazar] = {"boyut": 30, "color": "darkblue"}
        elif sayi < ortalama_makale_sayisi * 0.8:
            ozellikler[yazar] = {"boyut": 10, "color": "lightblue"}
        else:
            ozellikler[yazar] = {"boyut": 20, "color": "blue"}
    return ozellikler

# Graf oluşturma
def graf_olustur(data, limit):
    graf = Graf() # graf classindan graf nesnesi tanimlanir.
    data = data.iloc[:limit]

    # ORCID'e göre toplam makale sayısını hesaplama
    benzersiz_orcid_sayisi = data.groupby('orcid')['paper_title'].nunique().to_dict()
    ortalama_makale_sayisi = sum(benzersiz_orcid_sayisi.values()) / len(benzersiz_orcid_sayisi)
    
    # Düğüm özelliklerini hesapla
    dugum_ozellikler = dugum_ozellikleri_hesabi(benzersiz_orcid_sayisi, ortalama_makale_sayisi)

    for _, satir in data.iterrows():
        ana_yazar = satir['author_name'] ## ortak yazar
        orcid = satir['orcid']  ## orcid
        ortak_yazar_sutunu = str(satir['coauthors']) if not pd.isna(satir['coauthors']) else ""
        ortakyazarlar = [ortakyazar.strip() for ortakyazar in ortak_yazar_sutunu.strip("[]").split(',')]

        # ORCID'e göre yazarın tüm makalelerini bul
        makaleler = data[data['orcid'] == orcid]['paper_title'].tolist()
        makale_bilgisi = "\n".join(makaleler)

        # Ana yazarı ekle
        ozellikler = dugum_ozellikler.get(orcid, {"boyut": 20, "color": "blue"})
        graf.add_node(
            dugum_id=orcid,
            etiket=ana_yazar,
            boyut=ozellikler["boyut"],
            color=ozellikler["color"],
            bilgi=f"Yazar: {ana_yazar}\nORCID: {orcid}\nMakale Sayısı: {benzersiz_orcid_sayisi.get(orcid, 0)}\n\nMakale İsimleri:\n{makale_bilgisi}",
            agirlik=benzersiz_orcid_sayisi.get(orcid, 0)  # Düğüm ağırlığını doğru hesapla
        )

        # ana yazarin yardimci yazarlar ile yapmiş oldugu makaleler bulunur
        for ortakyazar in ortakyazarlar:
            if ortakyazar != ana_yazar:
                # Eş yazar ile ortak makaleleri bul
                ortak_makaleler = data[
                    (data['orcid'] == orcid) &  (data['coauthors'].str.contains(ortakyazar, na=False))]['paper_title'].tolist()
                ortak_makaleler_bilgi = "\n".join(ortak_makaleler)

                # Eş yazar düğümü oluştur
                graf.add_node(   
                    dugum_id=f"{ortakyazar}",
                    etiket=ortakyazar,
                    boyut=10,
                    color="gray",
                    bilgi=f"Ortak Yazar: {ortakyazar}\n\nOrtak Makaleler:\n{ortak_makaleler_bilgi}",
                    agirlik=len(ortak_makaleler)
                )

                # Ana düğümden eş yazara kenar ekle
                graf.add_edge(kaynak=orcid, hedef=f"{ortakyazar}", agirlik=len(ortak_makaleler))
                
                # Toplam düğüm ve kenar sayısını hesapla
                toplam_dugum = len(graf.nodes)
  

               
 

    return graf,toplam_dugum




def pyvis_gorsellestirme(graph, minimum_mesafe=None):
    net = Network(height="1000px", width="100%", bgcolor="#222222", font_color="white")
    net.toggle_physics(True)

    # Düğümleri ekleme
    for dugum_id, data in graph.nodes.items():
        net.add_node(
            dugum_id,
            label=data["etiket"],
            size=data["boyut"],
            color=data["color"],
            title=data["bilgi"]
        )

    # Kenarları ekleme
    for kaynak, hedef, agirlik in graph.edges:
        color = "FF0000" if minimum_mesafe and kaynak in minimum_mesafe and hedef in minimum_mesafe and (
            minimum_mesafe.index(kaynak) + 1 == minimum_mesafe.index(hedef) or
            minimum_mesafe.index(hedef) + 1 == minimum_mesafe.index(kaynak)
        ) else "white"

        net.add_edge(
            kaynak,
            hedef,
            icerik=agirlik,
            title=f"Ortak Makale Sayısı: {agirlik}",
            width=1,
            color=color  # Kısa yolu kırmızı renkle vurgula
        )


    return net

def en_kisa_yol(graph, start, end):
    # Mesafeleri ve önceki düğümleri başlat
    mesafeler = {dugum: float('inf') for dugum in graph.komsu_listesi}
    mesafeler[start] = 0
    onceki_dugumler = {dugum: None for dugum in graph.komsu_listesi}
    kuyruk = [(start, 0)]  # Kuyruk olarak liste kullanılıyor

    while kuyruk:
        # Kuyruktan en küçük mesafeye sahip düğümü seç
        kuyruk.sort(key=lambda x: x[1])
        mevcut_dugum, mevcut_mesafe = kuyruk.pop(0)

        if mevcut_mesafe > mesafeler[mevcut_dugum]:
            continue

        for komsu, agirlik in graph.komsu_listesi[mevcut_dugum]:
            mesafe = mevcut_mesafe + agirlik
            if mesafe < mesafeler[komsu]:
                mesafeler[komsu] = mesafe
                onceki_dugumler[komsu] = mevcut_dugum
                kuyruk.append((komsu, mesafe))

        


# Yol oluşturma
    yol = []
    yol_sozluk = {}  # Yol bağlantılarını tutacak sözlük
    mevcut = end
    while mevcut is not None:
        yol.insert(0, mevcut)
        onceki = onceki_dugumler[mevcut]
        if onceki is not None:
            yol_sozluk[onceki] = mevcut  # Mevcut düğümün önceki bağlantısını ekle
        mevcut = onceki

    if mesafeler[end] == float('inf'):
        return None, float('inf'), None  # Uygun bir yol bulunamadı

    return yol, mesafeler[end], yol_sozluk

def limitliIsbirlikHesapla(graph, limit):
    """
    Graf verisindeki yalnızca ORCID ID'lerine sahip düğümlerin işbirliği yaptığı yazar sayılarını hesaplar.
    :param graph: Graf nesnesi
    :param limit: İşlenecek ORCID ID sayısı limiti
    :return: ORCID ID'lerin anahtar olduğu ve işbirliği yapılan yazar sayılarını değer olarak döndüren bir sözlük
    """
    ortakliklar = {}
    sayac = 0

    for author_id, baglantilar in graph.komsu_listesi.items():
        if sayac >= limit:
            break
        if author_id.startswith("0000"):  # Sadece ORCID ID'lerini filtrele
            ortakliklar[author_id] = len(set(yan_dugum[0] for yan_dugum in baglantilar))
            sayac += 1
    
    
    return ortakliklar




def en_fazla_ortak_yazara_sahip(graph, data):  # 'data' parametresini ekledik
    # Her düğümün bağlantı (komşu) sayısını tutmak için sözlük
    ortak_yazar_sayilari = {}

    for dugum_id, komsular in graph.komsu_listesi.items():
        # Tekrar eden komşuları kaldırmak için küme kullanılır
        benzersiz_komsular = set(komsu[0] for komsu in komsular)
        ortak_yazar_sayilari[dugum_id] = len(benzersiz_komsular)

    # Sözlüğü bağlantı sayısına göre azalan şekilde sırala
    sirali_dugumler = sorted(ortak_yazar_sayilari.items(), key=lambda x: x[1], reverse=True)

    # En fazla bağlantıya sahip düğümü al
    en_fazla_ortak_yazar_orcid = sirali_dugumler[0][0]
    en_fazla_ortak_yazar_baglanti_sayisi = sirali_dugumler[0][1]

    # Orcid'den yazar ismini almak için 'data' üzerinde sorgu
    yazar_isim = data[data['orcid'] == en_fazla_ortak_yazar_orcid]['author_name'].iloc[0]

    # Tuple olarak döndür
    return en_fazla_ortak_yazar_orcid, en_fazla_ortak_yazar_baglanti_sayisi, yazar_isim






# Grafiği kaydetme
def grafik_kaydet(ag, cikti_gorsel):
    ag.write_html(cikti_gorsel)
    print(f"Grafik başarıyla kaydedildi: {cikti_gorsel}")

def main():
    # Gerekli dosyaların yolları
    excel_dosya = "C:\\Users\\sadik\\Desktop\\KOU CENG 2\\Prolab\\Prolab3\\230201040_230201099\\PROLAB 3 - GÜNCEL DATASET.xlsx"
    cikti_gorsel = "C:\\Users\\sadik\\Desktop\\manual_graph.html"
    html_arayuz = "C:\\Users\\sadik\\Desktop\\graph_interface.html"

    # Veri setini oku
    data = read_excel(excel_dosya)

    sinir = 1000# Buradaki limit değişkeni her değiştirildiğinde HTML'de güncellenecek

    # Graf oluştur
    graph,toplam_dugum = graf_olustur(data, sinir)
    
  
        

   # 5.ister
    orcidler=limitliIsbirlikHesapla(graph,sinir)
    
    # 6.ister,en fazla ortak yazara sahip orcidli dugumu bul     
    enfazlaortak=en_fazla_ortak_yazara_sahip(graph,data)
    

     
    

    
    
    # Pyvis ile grafiği oluştur ve kaydet
    ag = pyvis_gorsellestirme(graph)
    ag.write_html(cikti_gorsel)
    print(f"Pyvis grafiği başarıyla kaydedildi: {cikti_gorsel}")

    # HTML içeriğini bir değişkene yazın
    html_icerik = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Graph Visualization</title>
    <style>
        body {
            margin: 0;
            display: flex;
            flex-direction: row;
            height: 100vh;
            font-family: Arial, sans-serif;
        }
        #sol-panel {
            width: 20%;
            background-color: #2c3e50;
            padding: 20px;
            overflow-y: auto;
            border-right: 2px solid #bdc3c7;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        #cikti {
            padding: 10px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            background-color: #2c3e50; /* Sağdaki panelin rengi */
            color: white; /* Metin rengini beyaz yap */
            height: calc(100% - 40px);
            overflow-y: auto;
        }

        #graf-alani {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #1a1a1a;
            position: relative;
        }
        #limit-bilgi {
            position: absolute;
            bottom: 10px;
            right: 10px;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 12px;
        }
        #sag-panel {
            width: 20%;
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        #sag-panel button {
            padding: 10px;
            height: 90px;
            background-color: #3498db;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            font-size: 20px;
        }
        #sag-panel button:hover {
            background-color: #2980b9;
        }
       

    #graf-bilgi {
        position: absolute;
        bottom: 50px;
        left: 1250px;
        background-color: rgba(255, 165, 0, 0.8);
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
        color: #333;
    }
    
    </style>
</head>
<body>
    <div id="graf-bilgi">
    <p>Toplam düğüm sayısı: <span id="total-nodes">{{toplam_dugum}}</span></p>
</div>

    <div id="sol-panel">
        <div id="cikti">Çıktı...</div>
    </div>
    <div id="graf-alani">
        <iframe src="manual_graph.html" frameborder="0" style="width: 100%; height: 100%;"></iframe>
        <div id="limit-bilgi"></div>
    </div>
    <div id="sag-panel">
        <button onclick="kisaYolHesaplaVeCiz()">1. İster:En kısa yol ve görselleştirme</button>
        <button onclick="isbirlikKuyrugunuCalistir()">2. İster:İşbirliği yapan yazarlar ve görselleştirme</button>
        <button onclick="BSTolusturVeGorsellestir()">3. İster: BST ile çıkarma işlemi ve görselleştirme</button>
        <button onclick="isbirligiYollariCalistir()">4. İster:Yazarlar ve işbirlikçiler arasında kısa yolların hesaplanması
</button>
        <button onclick="yazarBilgisiAl()">5. İster:İş birliği yapılan ortak yazarlar</button>
        <button onclick="enIsbirlikciYazariGoster()">6. İster:En fazla işbirliği yapılan yazar</button>
        <button onclick="enUzunYoluCalistir()">7. İster:En uzun yol</button>
        
    </div>
    <script>
        let enIsbirlikciYazar = "Henüz yüklenmedi";
        let maxisbirligiSayisi = "Henüz yüklenmedi";
        let enIsbirlikciOrcid = "Henüz yüklenmedi";
        
        
        function tumDugumleriGuncelle(totalNodes) {
        document.getElementById('total-nodes').textContent = totalNodes;
    }

    // Örnek: Dinamik olarak toplam düğüm sayısını güncelle
    tumDugumleriGuncelle({{toplam_dugum}});

        function butonTiklama(message) {
            const outputDiv = document.getElementById('cikti');
            const timestamp = new Date().toLocaleTimeString();
            outputDiv.innerHTML += `<p>[${timestamp}] ${message}</p>`;
            outputDiv.scrollTop = outputDiv.scrollHeight;
        }

        function setLimitInfo(limit) {
            const limitInfoDiv = document.getElementById('limit-bilgi');
            limitInfoDiv.textContent = `Limit: ${limit} satır`;
        }

        const BackenddenLimit = {{satir_sayisi}};
        setLimitInfo(BackenddenLimit);

        function fizigiGuncelle(enabled) {
            const iframe = document.querySelector('iframe');
            iframe.contentWindow.postMessage({ type: 'fizigiGuncelle', enabled }, '*');
        }

        function itmegucuGuncelle(icerik) {
            const iframe = document.querySelector('iframe');
            iframe.contentWindow.postMessage({ type: 'itmegucuGuncelle', icerik }, '*');
        }

        function yercekimiGuncelle(icerik) {
            const iframe = document.querySelector('iframe');
            iframe.contentWindow.postMessage({ type: 'yercekimiGuncelle', icerik }, '*');
        }

        function enIsbirlikciYazariGoster() {
            const outputDiv = document.getElementById('cikti');
            const timestamp = new Date().toLocaleTimeString();
            outputDiv.innerHTML += `<p>[${timestamp}] En çok işbirliği yapan yazar: ${enIsbirlikciYazar} (${maxisbirligiSayisi} bağlantı, ORCID: ${enIsbirlikciOrcid})</p>`;
            outputDiv.scrollTop = outputDiv.scrollHeight;
        }
        
        function kisaYolHesaplaVeCiz() {
        const start = prompt("Başlangıç yazarın ORCID'ini girin:");
        const end = prompt("Bitiş yazarın ORCID'ini girin:");
        if (start && end) {
            window.pywebview.api.enkisayolHesapla(start, end)
                .then(sonuc => {
                    const outputDiv = document.getElementById("cikti");
                    const timestamp = new Date().toLocaleTimeString();
                    outputDiv.innerHTML += `<p>[${timestamp}] ${sonuc}</p>`;
                    outputDiv.scrollTop = outputDiv.scrollHeight;

                    // En kısa yol görselleştirme işlemi
                    return window.pywebview.api.kisa_yol_gorsellestir();
                })
                .then(visualizationResult => {
                    const outputDiv = document.getElementById("cikti");
                    const timestamp = new Date().toLocaleTimeString();
                    outputDiv.innerHTML += `<p>[${timestamp}] ${visualizationResult}</p>`;
                    outputDiv.scrollTop = outputDiv.scrollHeight;
                })
                .catch(error => console.error("Hata:", error));
        }
    }
        
        
        function enUzunYoluCalistir() {
    const start = prompt("Başlangıç yazarın ORCID'ini girin:");

    if (start) {
        // Kullanıcı girdisini Python'a gönder
        window.pywebview.api.enuzunyolHesapla(start)
            .then(sonuc => {
                const outputDiv = document.getElementById("cikti");
                const timestamp = new Date().toLocaleTimeString();
                outputDiv.innerHTML += `<p>[${timestamp}] ${sonuc}</p>`;
                outputDiv.scrollTop = outputDiv.scrollHeight;
            })
            .catch(error => console.error("Hata:", error));
    }
}

        

        
        
      function yazarBilgisiAl() {
    const authorId = prompt("Yazarın ORCID'ini girin:");
    if (authorId) {
        const outputDiv = document.getElementById('cikti');
        const timestamp = new Date().toLocaleTimeString();
        const collaborationCount = isbirlikSayisiniAl(authorId);
        outputDiv.innerHTML += `<p>[${timestamp}] ${authorId} ID'li yazarın işbirliği yaptığı toplam yazar sayısı: ${collaborationCount}</p>`;
        outputDiv.scrollTop = outputDiv.scrollHeight;
    }
}

        
       function isbirlikSayisiniAl(authorId) {
    const orcidData = {{orcidler}}; // Python'dan gelen veri
    return orcidData[authorId] || "Bilinmiyor";
}
       
       
function isbirlikKuyrugunuCalistir() {
        const orcid = prompt("Yazarın ORCID'ini girin:");
        if (orcid) {
            window.pywebview.api.isbirlikKuyruguOlustur(orcid)
                .then(sonuc => {
                    const outputDiv = document.getElementById("cikti");
                    const timestamp = new Date().toLocaleTimeString();
                    outputDiv.innerHTML += `<p>[${timestamp}] ${sonuc}</p>`;
                    outputDiv.scrollTop = outputDiv.scrollHeight;
                })
                .catch(error => console.error("Hata:", error));
        }
    }
 
  function BSTolusturVeGorsellestir() {
        const removeId = prompt("Çıkarılacak yazarın ORCID'ini girin:");
        if (removeId) {
            window.pywebview.api.BSTolusturVeGorsellestir(removeId)
                .then(sonuc => {
                    const outputDiv = document.getElementById("cikti");
                    const timestamp = new Date().toLocaleTimeString();
                    outputDiv.innerHTML += `<p>[${timestamp}] ${sonuc}</p>`;
                    outputDiv.scrollTop = outputDiv.scrollHeight;
                })
                .catch(error => console.error("Hata:", error));
        }
    }
       
  
  function isbirligiYollariCalistir() {
        const authorId = prompt("A yazarının ORCID'ini girin:");
        if (authorId) {
            window.pywebview.api.isbirlikYollariHesapla(authorId)
                .then(sonuc => {
                    const outputDiv = document.getElementById("cikti");
                    const timestamp = new Date().toLocaleTimeString();
                    outputDiv.innerHTML += `<p>[${timestamp}] ${sonuc}</p>`;
                    outputDiv.scrollTop = outputDiv.scrollHeight;
                })
                .catch(error => console.error("Hata:", error));
        }
    }
       
       
       


        // Python'dan alınan en fazla ortak yazar bilgisi
        enIsbirlikciOrcid = "{{orcid_isim}}";
        maxisbirligiSayisi = "{{isbirligi_sayisi}}";
        enIsbirlikciYazar = "{{yazar_ismi}}";
        
    
    </script>
</body>
</html>

    """
    html_icerik = html_icerik.replace("{{satir_sayisi}}", str(sinir))
    html_icerik = html_icerik.replace("{{orcid_isim}}", (enfazlaortak[0])) # Orcid
    html_icerik = html_icerik.replace("{{isbirligi_sayisi}}", str(enfazlaortak[1]))  # Bağlantı sayısı
    html_icerik = html_icerik.replace("{{yazar_ismi}}", str(enfazlaortak[2])) # Yazar ismi
    html_icerik = html_icerik.replace("{{orcidler}}", json.dumps(orcidler))
    html_icerik = html_icerik.replace("{{toplam_dugum}}", str(toplam_dugum))  # Toplam düğüm
    
    
    # HTML dosyasını kaydedin
    with open(html_arayuz, "w", encoding="utf-8") as html_file:
        html_file.write(html_icerik)

    print(f"HTML arayüz başarıyla oluşturuldu: {html_arayuz}")
    
    
    
     # Webview API'yi başlat ve pencereyi aç
    api = Api(graph)  # Api sınıfını başlatıyoruz
    webview.create_window("Graf Görselleştirme", html_arayuz, js_api=api)
    webview.start()
   
    


if __name__ == "__main__":
    main()


