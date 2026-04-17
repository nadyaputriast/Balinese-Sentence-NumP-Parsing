import json
import nltk
from nltk.corpus import wordnet as wn

def generate_target_words():
    print("📥 Menyiapkan kamus WordNet Indonesia...")
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    
    kata_target = {
        "V": [],
        "Noun": [],
        "Adj": [],
        "Adv": [],
        
        # --- 2. CLOSED CLASS & PROPER NOUN (Kita isi manual karena spesifik & terbatas) ---
        "Num": [
			"satu","dua","tiga","empat","lima","enam","tujuh","delapan","sembilan","sepuluh","sebelas",
			"puluh","ratus","ribu","juta",
			"nol","kosong",
			"dua belas","tiga belas","empat belas","lima belas","enam belas","tujuh belas","delapan belas","sembilan belas",
			"dua puluh","tiga puluh","empat puluh","lima puluh","enam puluh","tujuh puluh","delapan puluh","sembilan puluh",
			"seratus","seribu","sejuta",
			"miliar","triliun",
			"pertama","kedua","ketiga","keempat","kelima","keenam","ketujuh","kedelapan","kesembilan","kesepuluh",
			"setengah","seperempat","sepertiga"
		],

		"Prep": [
			"di","ke","dari","pada","kepada","bagi","untuk","buat","guna","demi","tentang","atas","bawah","samping","dengan",

			"oleh","terhadap","akan","antara","hingga","sampai","sejak","semenjak","menuju","melalui","tanpa","bersama",
			"sekitar","seputar","dalam","luar","atas","bawah","sebelum","sesudah","selama","sepanjang","di antara"
		],

		"Det": [
			"ini","itu","tersebut","segala","semua","beberapa","setiap","tiap",

			"para","sang","si",
			"sebuah","seorang","seekor",
			"banyak","sedikit","seluruh","sekalian",
			"masing-masing","tiap-tiap"
		],

		"Pronoun": [
			"saya","aku","kamu","engkau","dia","ia","beliau","mereka","kita","kami","anda",

			"gue","gua","lu","loe","kau","kalian","ente",
			"beta","hamba","patik","abdi",
			"ini","itu","sini","situ","sana",
			"siapa","apa","mana",
			"seseorang","sesuatu","semua","masing-masing",
			"diri","diriku","dirimu","dirinya","diri sendiri",
			"saling","satu sama lain",
			"yang"
		],

		"PropNoun": [
			"bali","denpasar","badung","gianyar","singaraja","indonesia",
			"wayan","made","nyoman","ketut","putu","gede","kadek","komang",

			"jakarta","bandung","surabaya","medan","makassar","yogyakarta","semarang","palembang","batam",
			"tabanan","klungkung","bangli","karangasem","buleleng",
			"jawa","sumatera","kalimantan","sulawesi","papua",

			"malaysia","singapura","jepang","korea","cina","india","amerika","kanada","inggris","australia","jerman","prancis","belanda",

			"budi","andi","siti","ani","rina","dian","agus","eko","joko","sri","dewi","putri","aditya","dimas","rangga","rizky","farhan",

			"google","microsoft","apple","amazon","meta","tokopedia","shopee","bukalapak","lazada",
			"bca","bri","mandiri","bni",

			"ui","ugm","itb","its","unair","undip","unpad","binus",

			"senin","selasa","rabu","kamis","jumat","sabtu","minggu",
			"januari","februari","maret","april","mei","juni","juli","agustus","september","oktober","november","desember",

			"ramadhan","idul fitri","idul adha","natal","nyepi","galungan","kuningan",

			"whatsapp","instagram","facebook","twitter","tiktok","youtube","telegram"
		],
  

		"Conj": [
			"dan","serta","atau","ataupun",
			"tetapi","tapi","namun","melainkan","sedangkan","padahal",
			"karena","sebab","oleh karena itu","oleh sebab itu",
			"sehingga","maka","jadi","akibatnya",
			"agar","supaya","biar",
			"ketika","saat","sewaktu","tatkala","selagi","sementara",
			"sebelum","sesudah","setelah","sejak","semenjak",
			"hingga","sampai",
			"jika","kalau","bila","apabila","asal","asalkan",
			"walaupun","meskipun","biarpun","kendati","sekalipun",
			"seolah","seakan","seakan-akan",
			"bahwa",
			"lalu","kemudian","selanjutnya",
			"yaitu","yakni",
			"bahkan","malah","apalagi",
			"lagipula","selain itu",
			"dengan demikian","oleh karena itu","oleh sebab itu",
			"di samping itu","di sisi lain",
			"andaikata","andaikan","sekiranya",
			"justru","padahal","toh"
		]
    }
    
    print("🔍 Mengekstrak kata dasar dari NLTK...")
    
    # Sedot Verb
    for lemma in wn.all_lemma_names(pos=wn.VERB, lang='ind'):
        if "_" not in lemma: kata_target["V"].append(lemma.lower())
            
    # Sedot Noun
    for lemma in wn.all_lemma_names(pos=wn.NOUN, lang='ind'):
        if "_" not in lemma: kata_target["Noun"].append(lemma.lower())
            
    # Sedot Adjective
    for lemma in wn.all_lemma_names(pos=wn.ADJ, lang='ind'):
        if "_" not in lemma: kata_target["Adj"].append(lemma.lower())
            
    # Sedot Adverbia (Adv)
    for lemma in wn.all_lemma_names(pos=wn.ADV, lang='ind'):
        if "_" not in lemma: kata_target["Adv"].append(lemma.lower())

    # Hapus duplikat
    kata_target["V"] = list(set(kata_target["V"]))
    kata_target["Noun"] = list(set(kata_target["Noun"]))
    kata_target["Adj"] = list(set(kata_target["Adj"]))
    kata_target["Adv"] = list(set(kata_target["Adv"]))
    
    # Simpan ke file perantara
    with open('target_indo.json', 'w', encoding='utf-8') as f:
        json.dump(kata_target, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Selesai! Tersimpan di 'target_indo.json'")
    print(f"📊 Ringkasan Data Open-Class:")
    print(f"   - Verba (V): {len(kata_target['V'])}")
    print(f"   - Nomina (Noun): {len(kata_target['Noun'])}")
    print(f"   - Adjektiva (Adj): {len(kata_target['Adj'])}")
    print(f"   - Adverbia (Adv): {len(kata_target['Adv'])}")

if __name__ == "__main__":
    generate_target_words()