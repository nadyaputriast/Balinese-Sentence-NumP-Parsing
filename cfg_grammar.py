RULES_CFG = {
    "K": [["K1"], ["K1", "Pel"], ["K1", "Ket"], ["K1", "K2"]],
    "K1": [["S", "P"]],
    "K2": [["Pel", "Ket"]],
    "S": [["NP"]],
    "P": [["NumP"]],
    "Pel": [["AdjP"], ["VP"]],
    "Ket": [["PP"]],
    "NP": [["Noun"], ["NumP", "NP"], ["NP", "NP"], ["NP", "PropNoun"], ["NP", "Pronoun"], ["Pronoun"], ["PropNoun"], ["Adv", "NP"], ["NP", "Det"], ["NP", "AdjP"], ["NP", "Adv"]],
    "NumP": [["Num"], ["NumP", "Noun"], ["NumP", "NP", "Det"], ["NumP", "NumP"]],
    "AdjP": [["Adj"], ["AdjP", "AdjP"], ["AdjP", "Adv"], ["Adv", "AdjP"]],
    "VP": [["V"], ["VP", "NP"], ["VP", "AdjP"], ["VP", "NumP"], ["Adv", "VP"]],
    "PP": [["Prep", "NP"], ["Prep", "Det", "NP"], ["Prep", "AdjP"], ["Prep", "NumP"], ["Prep", "Adv"]],
    
    "PropNoun": [["indonesia"], ["indonesiane"], ["bali"], ["denpasar"], ["badung"], ["gianyar"], ["klungkung"], ["karangasem"], ["bangli"], ["buleleng"], ["tabanan"], ["jembrana"], ["singaraja"], ["negara"], ["ubud"], ["kuta"], ["sanur"], ["jimbaran"], ["canggu"], ["seminyak"], ["legian"], ["padangbai"], ["amed"], ["gilimanuk"], ["pemuteran"], ["menjangan"], ["candidasa"], ["tulamben"], ["kintamani"], ["bedugul"], ["lovina"], ["nusa"], ["surabaya"], ["jakarta"], ["bapa"], ["bapak"], ["bapakne"], ["bapan"], ["pak"], ["ibu"], ["bu"], ["meme"], ["memen"], ["jero"], ["putu"], ["i"], ["ni"], ["si"], ["wayan"], ["made"], ["kadek"], ["nengah"], ["komang"], ["nyoman"], ["ketut"], ["luh"], ["gede"], ["budi"], ["karma"], ["unda"], ["trunyan"], ["petitenget"], ["pejeng"], ["kerobokan"], ["tegalalang"], ["seririt"], ["kintamani"]],
    
    "Pronoun": [["aji"], ["awakne"], ["bapa"], ["beli"], ["betara"], ["bibi"], ["biang"], ["buyut"], ["cai"], ["cang"], ["canggah"], ["ci"], ["cokor"], ["dadong"], ["dane"], ["dewa"], ["dewek"], ["embok"], ["gantung"], ["gelah"], ["gusi"], ["hyang"], ["ia"], ["iba"], ["icang"], ["ida"], ["idane"], ["ikane"], ["ipun"], ["ipun-ipun"], ["ipuna"], ["ipune"], ["iraga"], ["iragane"], ["ira"], ["iragang"], ["jerone"], ["kai"], ["kami"], ["kakiang"], ["kelab"], ["klabang"], ["kumpi"], ["manira"], ["meme"], ["misan"], ["mindon"], ["nyai"], ["niang"], ["nikanne"], ["nira"], ["okane"], ["okan-okane"], ["palungguh"], ["parasane"], ["parasapasami"], ["parasapasira"], ["parasida"], ["parajana"], ["parajanma"], ["parajero"], ["parasami"], ["paranirane"], ["parasirasami"], ["pekak"], ["putrane"], ["putran-putrane"], ["ragane"], ["ragan-ragane"], ["rerama"], ["ratu"], ["samian"], ["samiyan"], ["sami"], ["sang"], ["sapasami"], ["sapasira"], ["sapunapi-sapunapi"], ["sekancan"], ["siwer"], ["sira"], ["sira-sira"], ["sinamian"], ["tiang"], ["tiange"], ["titiang"], ["uduh"], ["uwa"], ["wareng"], ["widhi"]],
    
    "Adv": [["adeng-adeng"], ["alon"], ["alon-alon"], ["asapunapi"], ["asapunika"], ["becik"], ["benjang"], ["bisa"], ["buin"], ["cepok"], ["dados"], ["dumun"], ["dibi"], ["durung"], ["enggal"], ["gelis"], ["gelis-gelis"], ["gati"], ["ibi"], ["jagi"], ["jani"], ["jenenga"], ["kapah"], ["kantun"], ["kadi"], ["kewala"], ["kejep"], ["lakar"], ["lantas"], ["malih"], ["malu"], ["mampuh"], ["mangda"], ["mangkin"], ["mara"], ["meled"], ["menawi"], ["meneng"], ["minab"], ["minakadi"], ["munguin"], ["nadaksara"], ["nantun"], ["nenten"], ["ngararis"], ["ngiring"], ["ngiring"], ["ngiring"], ["nyanan"], ["nyidayang"], ["para"], ["paling"], ["payu"], ["pateh"], ["patuh"], ["pepes"], ["pesan"], ["ping"], ["pisan"], ["puan"], ["prasida"], ["prajani"], ["raris"], ["rihin"], ["sakadi"], ["sajatine"], ["sajawi"], ["sadurung"], ["sampun"], ["sampunika"], ["sapunapi"], ["sapunika"], ["sabenehne"], ["sasidan"], ["sayuwakti"], ["sekadi"], ["sekat"], ["selid"], ["semeng"], ["semengan"], ["serod"], ["sesai"], ["sajatine"], ["setata"], ["soroh"], ["stata"], ["suba"], ["sujatine"], ["tengai"], ["ten"], ["terus"], ["tuni"], ["tutug"], ["tusing"], ["uwug"], ["wantah"], ["wau"], ["wawu"], ["wenten"], ["wiakti"], ["wusan"], ["yakti"]],

    "Det": [["niki"], ["nika"], ["puniki"], ["punika"], ["ene"], ["ento"], ["ne"], ["to"], ["anu"], ["ane"], ["punikine"], ["punikane"], ["punikune"], ["nikine"], ["nikane"], ["nikune"], ["niki-nika"], ["puniki-punika"], ["sekancan"]],
    
    "Noun": [["AC"], ["abing"], ["ading"], ["adi"], ["adin"], ["adine"], ["adeg"], ["alas"], ["alase"], ["alat"], ["aling-aling"], ["ampik"], ["anake"],["angkul-angkul"], ["arak"], ["arin"], ["aring"], ["arung"], ["ayam"], ["baju"], ["balian"], ["bangkung"], ["banjar"], ["banten"], ["bantang"], ["baris"], ["base"], ["basang"], ["bebed"], ["bebek"], ["bebungkilan"], ["begina"], ["beli"], ["belimbing"], ["bebung"], ["bengkuang"], ["berem"], ["besik"], ["bias"], ["bingin"], ["biu"], ["binatang"], ["buku"], ["bulan"], ["bulih"], ["buluh"], ["bunut"], ["busana"], ["buyung"], ["candi"], ["canang"], ["canangsari"], ["carikne"], ["cecepan"], ["celagih"], ["celeng"], ["cendekan"], ["cekalan"], ["cerorong"], ["cicing"], ["dangdang"], ["dapetan"], ["dedari"], ["delima"], ["demung"], ["desa"], ["desan"], ["desane"], ["dewa"], ["diri"], ["don"], ["dosen"], ["dulang"], ["ekor"], ["entik"], ["gedong"], ["gedang"], ["gamelan"], ["gangsa"], ["gajah"], ["gedang"], ["gendong"], ["gentong"], ["gerah"], ["gelang"], ["genta"], ["guru"], ["guruh"], ["guli"], ["harimau"], ["hektar"], ["ikat"], ["iga-iga"], ["jagung"], ["jalikan"], ["janger"], ["jangkep"], ["jasad"], ["jegog"], ["jegogan"], ["jempana"], ["juara"], ["jukut"], ["kadi"], ["kaleng"], ["kampil"], ["kebun"], ["kelir"], ["kepuh"], ["kiat"], ["kidung"], ["kiskis"], ["kleding"], ["kolam"], ["kota"], ["kori"], ["kursi"], ["layangan"], ["lampu"], ["lawar"], ["laptop"], ["legong"], ["lelembut"], ["lemari"], ["lemarine"], ["lengan"], ["lelawah"], ["lubung"], ["lusin"], ["marajan"], ["mas"], ["macan"], ["macanne"], ["margane"], ["meja"], ["memerine"], ["motor"], ["motorne"], ["muani"], ["napkin"], ["nyaman"], ["olahraga"], ["parang"], ["paon"], ["pasang"], ["payuk"], ["pemade"], ["pengubengan"], ["pecalang"], ["pecan"], ["pragina"], ["peteng"],["pinis"], ["pianakne"], ["prasi"], ["pulo"], ["punyan"], ["ratu"], ["rahang"], ["rebab"], ["sampah"], ["sampahe"], ["sanggah"], ["sawit"], ["segara"], ["sekolah"], ["sekolahne"], ["sentana"], ["sepatu"], ["setra"], ["sejarah"], ["sepeda"], ["semeng"], ["sinepe"], ["siap"], ["siape"], ["singa"], ["sisya"], ["sisya-sisyane"], ["sokasi"], ["sotong"], ["sopir"], ["suling"],["sunduk"], ["sungge"], ["taluh"], ["takud"], ["tanah"], ["tapel"], ["tegul"], ["teken"],["tembaga"], ["temu"], ["terune"], ["tiang"], ["tiban"], ["tiing"], ["tingkat"], ["timpal"], ["topeng"], ["tirta"], ["tuak"], ["tukad"], ["tulis"], ["udeng"], ["ujan"], ["utan"], ["ukud"], ["untane"], ["untu"], ["umah"], ["waktu"], ["watek"], ["yusan"]],
    
    "Num": [["besik"], ["asiki"], ["siki"], ["kalih"], ["dadua"], ["duang"], ["dadue"], ["tiga"], ["tigang"], ["telung"], ["pat"], ["papat"], ["lalima"], ["lelima"], ["limang"], ["lima"], ["nem"], ["pitu"], ["pitung"], ["kutus"], ["ulu"], ["sia"], ["sanga"], ["dasa"], ["roras"], ["solas"], ["telulas"], ["limolas"], ["pitulas"], ["plekutus"], ["siangolas"], ["salikur"], ["likur"], ["selae"], ["pasaur"], ["setiman"], ["seket"], ["benang"], ["satus"], ["karobelah"], ["lebak"], ["satak"], ["atus"], ["samas"], ["domas"], ["bangsit"], ["sepaa"],  ["kapertama"], ["kaping"], ["adiri"], ["alaksa"], ["aketi"], ["ayutia"], ["abungkul"], ["akatih"], ["asiu"], ["ayu"], ["adasa"], ["aparo"], ["paro"], ["siu"], ["sewu"], ["ribuan"]],    
    
    "V": [["abane"], ["adepe"], ["ilang"], ["mejalan"], ["melaib"], ["negak"], ["teka"], ["ulung"], ["medem"], ["matangi"], ["nongos"], ["luas"], ["makecos"], ["makecog"], ["makeber"], ["nglayang"], ["nglangi"], ["ngeling"], ["makarya"], ["magae"], ["megae"], ["masare"], ["mesuryak"], ["makejer"], ["mekekeh"], ["meluah"], ["ngendih"], ["majemuh"], ["masisigan"], ["ngoyong"], ["mabanten"], ["muspa"], ["masemadi"], ["mayoga"], ["masekar"], ["megending"], ["makekawin"], ["ngigel"], ["magebur"], ["merebah"], ["mebikas"], ["megedi"], ["makuuk"], ["manting"], ["masemu"], ["mekipe"], ["mekedek"], ["melali"], ["mengkeb"], ["menjit"], ["mentik"], ["mesiat"], ["melajah"], ["masepedaan"], ["metimpuh"], ["dados"], ["makelimat"], ["maplisahan"], ["mekumpul"], ["mejejaitan"],  ["mepaluing"], ["merengin"], ["mesangih"], ["mesaut"], ["meturut"], ["mawangsit"], ["masayuban"], ["masemayan"], ["masesangi"], ["masesapan"], ["matektekan"], ["matirtayan"], ["mayasakala"], ["malajah"], ["tinggal"], ["majajal"], ["mekeber"], ["ngelangi"], ["maca"], ["ngangge"], ["nganggon"], ["dadi"],["meli"], ["numbas"], ["meliang"], ["ngajeng"], ["madaar"], ["madagang"], ["ngamah"], ["minum"], ["nginem"], ["nyemak"], ["ngejang"], ["ngaba"], ["nyuun"], ["ngisinin"], ["ngutang"], ["nyangih"], ["ngorahang"], ["nuturang"], ["ngaukin"], ["nulungin"], ["nguruk"], ["ngajahin"], ["nunden"], ["mapitulung"], ["nyagjagin"], ["ngortain"], ["ngae"], ["ngaenang"], ["nulis"], ["nyurat"], ["ngukir"], ["metanding"], ["ngocek"], ["ngadukang"], ["ningalin"], ["ngerasang"], ["ningeh"], ["ngadek"], ["ngecap"], ["memaca"], ["ngaturang"], ["ngisidang"], ["nyangkepang"], ["ngubadin"], ["ngupayang"], ["nguratiang"], ["ngidih"], ["nyilih"], ["ngadep"], ["negul"], ["nguberin"], ["ngebah"], ["nyangkol"], ["ngateh"], ["nyarup"], ["ngecum"], ["nyiksik"], ["nyangket"], ["ngebug"], ["nyiup"], ["negakin"], ["nyampat"], ["ngumbah"], ["ngetep"], ["nulad"], ["nyangkil"], ["nengok"], ["ningting"], ["ngetok"], ["ngibukang"], ["nyarmin"], ["ngangget"], ["ngutgut"], ["ngesges"], ["ngebut"], ["ngepung"], ["nyemuh"], ["nguyak"], ["ngungkab"], ["ngebet"], ["nguncab"], ["ngebang"], ["nyedut"], ["ngampik"], ["ngejer"], ["ngengap"], ["ngukud"], ["ngenahang"], ["ngorahin"], ["nyemakang"], ["ngadanin"], ["nyelepin"], ["ngelengin"], ["ngamaang"], ["nampedang"], ["nampenin"], ["nampiang"], ["nandesang"], ["nandiang"], ["nandingang"], ["nandurin"], ["nanenayang"], ["nanggapin"], ["nangkenang"], ["nangkidang"], ["nangkilin"], ["ngamenekang"], ["ngedengang"], ["ngedilang"], ["ngejotin"], ["ngekadang"], ["ngematiang"], ["ngemasin"], ["ngempelin"], ["ngempetin"], ["ngencakang"], ["ngendahang"], ["ngenjuhin"], ["ngentenang"], ["ngentikang"], ["ngenyudang"], ["ngerehang"], ["ngerusuhin"], ["ngesenggang"], ["ngetakang"], ["ngetelang"], ["ngetuhang"], ["ngewangang"], ["ngicenin"], ["ngidupang"], ["ngilehin"], ["ngilingin"], ["ngimpasin"], ["ngindayang"], ["ngintipang"], ["ngisiang"], ["ngitungang"], ["ngiwasin"], ["nglanturang"], ["nglemesin"], ["nglepasang"], ["nglinggihang"], ["ngojarang"], ["ngomong"], ["ngonemin"], ["ngosong"], ["ngubuhin"], ["nguduhin"], ["ngulapin"], ["ngulatin"], ["nguliang"], ["ngulurin"], ["ngumpulang"], ["ngumpulin"], ["ngundebang"], ["ngundigang"], ["nguntulang"], ["ngurukang"], ["ngutangag"], ["ngutsahayang"], ["nguwuhin"], ["nyelapang"], ["nyelempang"], ["merasa"], ["bangun"], ["maem"], ["nyapa"]],
    
    "Prep": [["ajaka"], ["ajeng"], ["ajak"], ["antuk"], ["ba"], ["bareng"], ["beten"], ["bucun"], ["daweg"], ["di"], ["duur"], ["duk"], ["duri"], ["dugas"], ["dugase"], ["jaba"], ["kaja"], ["ka"], ["kantos"], ["kanti"], ["kayang"], ["kauh"], ["ke"], ["kelawan"], ["kelod"], ["kebet"], ["kangin"], ["maring"], ["marep"], ["menek"], ["ngaja"], ["ngajak"], ["ngantos"], ["ngelod"], ["ngauh"], ["ngiring"], ["ngangin"], ["olih"], ["ring"], ["rikala"], ["ritatkala"], ["risedek"], ["sadurung"], ["sajabaning"], ["sajeroning"], ["saking"], ["sareng"], ["sedek"], ["sedekan"], ["samping"], ["sederung"], ["sedin"], ["sisi"], ["sisin"], ["teken"], ["tengahan"], ["tuun"], ["uli"]],
    
    "Adj": [["adil"], ["ajum"], ["alus"], ["akeh"], ["anteng"], ["anyar"], ["ayu"], ["bagus"], ["bajang"], ["banyol"], ["barak"], ["baru"], ["bawak"], ["bagia"], ["becik"], ["bedak"], ["berag"], ["beneh"], ["belog"], ["berek"], ["betek"], ["cupit"], ["cerik"], ["cenik"], ["darma"], ["demen"], ["dalem"], ["dingin"], ["dueg"], ["endah"], ["endep"], ["galak"], ["galak-galak"], ["gede"], ["gede-gede"], ["gelem"], ["gedeg"], ["ibuk"], ["inguh"], ["jaen"], ["jele"], ["jegeg"], ["jegeg-jegeg"],["jemet"], ["kelih"], ["kenyel"], ["kejem"], ["keras"], ["lacur"], ["lantang"], ["lanying"], ["lascarya"], ["luas"], ["luung"], ["lemah"], ["lemet"], ["linggah"], ["males"], ["mayus"], ["mati"], ["mebrarakan"], ["melah"], ["mokoh"], ["ngambul"], ["nyem"], ["panes"], ["putih"], ["poleng"], ["rame"], ["satya"], ["sakti"], ["sakit"], ["selem"], ["seleg"], ["seduk"], ["sebet"], ["sengsara"], ["seger"], ["siteng"], ["sugih"], ["suci"], ["sue"], ["suung"], ["wayah"], ["tabah"], ["tegeh"], ["tua"], ["tenget"], ["wisesa"], ["wikan"], ["pradnyan"], ["patut"], ["puntul"], ["podol"], ["polos"], ["ramah"]]
}

# Metadata Sor Singgih untuk Numeralia
NUMERALIA_SOR_SINGGIH = {
    # Basa Kasar/Andap
    'besik': {'register': 'kasar', 'meaning': '1', 'alus': 'asiki'},
    'siki': {'register': 'kasar', 'meaning': '1', 'alus': 'asiki'},
    'dua': {'register': 'kasar', 'meaning': '2', 'alus': 'kalih'},
    'duang': {'register': 'kasar', 'meaning': '2', 'alus': 'kalih'},
    'dadua': {'register': 'kasar', 'meaning': '2', 'alus': 'kalih'},
    'dadue': {'register': 'kasar', 'meaning': '2', 'alus': 'kalih'},
    'telung': {'register': 'kasar', 'meaning': '3', 'alus': 'tiga'},
    'papat': {'register': 'kasar', 'meaning': '4', 'alus': 'sekawan'},
    'pat': {'register': 'kasar', 'meaning': '4', 'alus': 'sekawan'},
    'limang': {'register': 'kasar', 'meaning': '5', 'alus': 'panca'},
    'lelima': {'register': 'kasar', 'meaning': '5', 'alus': 'panca'},
    'lalima': {'register': 'kasar', 'meaning': '5', 'alus': 'panca'},
    'nem': {'register': 'kasar', 'meaning': '6', 'alus': 'enem'},
    'pitung': {'register': 'kasar', 'meaning': '7', 'alus': 'pitu'},
    'kutus': {'register': 'kasar', 'meaning': '8', 'alus': 'akutus'},
    'sia': {'register': 'kasar', 'meaning': '9', 'alus': 'asanga'},
    'sanga': {'register': 'kasar', 'meaning': '9', 'alus': 'asanga'},
    'dasa': {'register': 'kasar', 'meaning': '10', 'alus': 'adasa'},
    'satus': {'register': 'kasar', 'meaning': '100', 'alus': 'aatus'},
    'atus': {'register': 'kasar', 'meaning': '100', 'alus': 'aatus'},
    'satak': {'register': 'kasar', 'meaning': '100', 'alus': 'aatus'},
    'sewu': {'register': 'kasar', 'meaning': '1000', 'alus': 'asiu'},
    'siu': {'register': 'kasar', 'meaning': '1000', 'alus': 'asiu'},
    
    # Basa Alus/Singgih
    'asiki': {'register': 'alus', 'meaning': '1', 'kasar': 'besik/siki'},
    'kalih': {'register': 'alus', 'meaning': '2', 'kasar': 'duang/dua'},
    'sekawan': {'register': 'alus', 'meaning': '4', 'kasar': 'papat/pat'},
    'panca': {'register': 'alus', 'meaning': '5', 'kasar': 'limang/lima'},
    'enem': {'register': 'alus', 'meaning': '6', 'kasar': 'nem'},
    'akutus': {'register': 'alus', 'meaning': '8', 'kasar': 'kutus'},
    'asanga': {'register': 'alus', 'meaning': '9', 'kasar': 'sanga/sia'},
    'adasa': {'register': 'alus', 'meaning': '10', 'kasar': 'dasa'},
    'aatus': {'register': 'alus', 'meaning': '100', 'kasar': 'satus'},
    'asiu': {'register': 'alus', 'meaning': '1000', 'kasar': 'sewu/siu'},
    
    # Netral (bisa digunakan di semua register)
    'tiga': {'register': 'netral', 'meaning': '3'},
    'tigang': {'register': 'netral', 'meaning': '3'},
    'lima': {'register': 'netral', 'meaning': '5'},
    'pitu': {'register': 'netral', 'meaning': '7'},
    'ulu': {'register': 'netral', 'meaning': '9'},
    'roras': {'register': 'netral', 'meaning': '12'},
    'solas': {'register': 'netral', 'meaning': '13'},
    'telulas': {'register': 'netral', 'meaning': '14'},
    'limolas': {'register': 'netral', 'meaning': '15'},
    'pitulas': {'register': 'netral', 'meaning': '17'},
    'plekutus': {'register': 'netral', 'meaning': '18'},
    'siangolas': {'register': 'netral', 'meaning': '19'},
    'likur': {'register': 'netral', 'meaning': '20'},
    'salikur': {'register': 'netral', 'meaning': '21'},
    'selae': {'register': 'netral', 'meaning': '25'},
    'pasaur': {'register': 'netral', 'meaning': '35'},
    'setiman': {'register': 'netral', 'meaning': '50'},
    'seket': {'register': 'netral', 'meaning': '50'},
    'benang': {'register': 'netral', 'meaning': '80'},
    'karobelah': {'register': 'netral', 'meaning': '200'},
    'lebak': {'register': 'netral', 'meaning': '200'},
    'samas': {'register': 'netral', 'meaning': '400'},
    'domas': {'register': 'netral', 'meaning': '500'},
    'bangsit': {'register': 'netral', 'meaning': '800'},
    'ribuan': {'register': 'netral', 'meaning': 'thousands'},
    'kapertama': {'register': 'netral', 'meaning': 'pertama'},
    'kaping': {'register': 'netral', 'meaning': 'ke-'},
    'adiri': {'register': 'netral', 'meaning': 'sendiri'},
    'aparo': {'register': 'netral', 'meaning': '½'},
    'paro': {'register': 'netral', 'meaning': '½'},
    'ping': {'register': 'netral', 'meaning': 'kali'},
    'alaksa': {'register': 'netral', 'meaning': '100,000'},
    'aketi': {'register': 'netral', 'meaning': '10,000,000'},
    'ayutia': {'register': 'netral', 'meaning': '1,000,000'},
    'abungkul': {'register': 'netral', 'meaning': 'sebungkul'},
    'akatih': {'register': 'netral', 'meaning': 'sekatih'},
    'ayu': {'register': 'netral', 'meaning': 'seayu'},
    'sepaa': {'register': 'netral', 'meaning': 'seperempat'},
}

# Metadata Sor Singgih untuk Pronoun
PRONOUN_SOR_SINGGIH = {
    # Orang Pertama
    'tiang': {'register': 'alus', 'meaning': 'saya', 'person': '1st'},
    'tiange': {'register': 'alus', 'meaning': 'saya', 'person': '1st'},
    'titiang': {'register': 'alus', 'meaning': 'saya (sangat alus)', 'person': '1st'},
    'icang': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'cang': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'iang': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'awakne': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'dewek': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'iraga': {'register': 'madia', 'meaning': 'kita/kami', 'person': '1st-plural'},
    'iragane': {'register': 'madia', 'meaning': 'kita/kami', 'person': '1st-plural'},
    
    # Orang Kedua
    'cai': {'register': 'kasar', 'meaning': 'kamu', 'person': '2nd'},
    'ci': {'register': 'kasar', 'meaning': 'kamu', 'person': '2nd'},
    'iba': {'register': 'kasar', 'meaning': 'kamu', 'person': '2nd'},
    'ragane': {'register': 'madia', 'meaning': 'kamu', 'person': '2nd'},
    'ragan-ragane': {'register': 'madia', 'meaning': 'kamu', 'person': '2nd'},
    'jerone': {'register': 'alus', 'meaning': 'beliau', 'person': '2nd'},
    'ida': {'register': 'alus', 'meaning': 'beliau', 'person': '2nd'},
    'idane': {'register': 'alus', 'meaning': 'beliau', 'person': '2nd'},
    'dane': {'register': 'alus', 'meaning': 'dia/beliau', 'person': '2nd/3rd'},
    'cokor': {'register': 'alus', 'meaning': 'beliau', 'person': '2nd'},
    
    # Orang Ketiga
    'ia': {'register': 'kasar', 'meaning': 'dia', 'person': '3rd'},
    'ikane': {'register': 'kasar', 'meaning': 'dia', 'person': '3rd'},
    'ipun': {'register': 'alus', 'meaning': 'dia/beliau', 'person': '3rd'},
    'ipune': {'register': 'alus', 'meaning': 'dia/beliau', 'person': '3rd'},
    'ipuna': {'register': 'alus', 'meaning': 'dia/beliau', 'person': '3rd'},
    'ipun-ipun': {'register': 'alus', 'meaning': 'mereka', 'person': '3rd-plural'},
}

CLASSIFIER_METADATA = {
    'diri': {'meaning': 'classifier untuk orang', 'usage': 'manusia'},
    'ekor': {'meaning': 'classifier untuk hewan', 'usage': 'hewan'},
    'ukud': {'meaning': 'classifier untuk hewan (ekor)', 'usage': 'hewan'},
    'pasang': {'meaning': 'classifier untuk berpasangan', 'usage': 'benda berpasangan'},
    'lusin': {'meaning': 'classifier untuk lusin (12)', 'usage': 'satuan komersial'},
    'hektar': {'meaning': 'classifier untuk luas tanah', 'usage': 'tanah'},
    'tingkat': {'meaning': 'classifier untuk tingkat/lantai', 'usage': 'bangunan'},
    'batang': {'meaning': 'classifier untuk benda panjang', 'usage': 'benda panjang'},
}

def get_all_numerals():
    """Dapatkan semua numeralia dari grammar."""
    return [num[0] for num in RULES_CFG.get("Num", [])]

def get_all_pronouns():
    """Dapatkan semua pronoun dari grammar."""
    return [pron[0] for pron in RULES_CFG.get("Pronoun", [])]

def get_numeral_register(word):
    """Dapatkan register numeralia."""
    return NUMERALIA_SOR_SINGGIH.get(word.lower(), {}).get('register', None)

def get_pronoun_register(word):
    """Dapatkan register pronoun."""
    return PRONOUN_SOR_SINGGIH.get(word.lower(), {}).get('register', None)

def is_classifier(word):
    """Cek apakah kata adalah classifier."""
    return word.lower() in CLASSIFIER_METADATA