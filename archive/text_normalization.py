kalimat = "S (Sepatu baru adin tiange) P (telung pasang) Pel (lakar abane) Ket (ka kota Surabaya). S (Sepeda motorne) P (dadue) Pel (luung gati). S (Carikne Pak Putu Karma) P (dasa hektar) Pel (adepe). S (Buku tulis timpal adin ange) P (duang lusin). S (Laptop bapak dosen punika) P (lelima). S (Adin tiange) P (duang diri) Pel (melali) Ket (ka Jakarta). S (Siap selem bapan ipune) P (pitung ukud) Pel (ilang) Ket (ibi peteng). S (Pianakne Pak Putu Gede) P (telung diri) Pel (jegeg-jegeg pisan). S (Umah timpal memen tiange) P (limang tingkat) Pel (paling becik) Ket (di desane). S (Baju baru tiange) P (dasa besik) Ket (di lemarine). S (Ragane) P (sampun mekarya) Ket (saking semeng pisan). S (Dane) P (setata manting) O ( baju akeh pisan) Ket (ka Tukad Unda). S (Bapan ipune) P (sampun dados) Pel (balian sakti) Ket (saking sue pisan). S (Jero balian puniki) P (sakti pisan) Pel (ngubadin sakit basang) Ket (di sekancan desan tiange). S (Titiang puniki) P (males pisan) Pel (melajah mejejaitan). S ( Bapakne I Putu Gede) P (guru olahraga)  Ket (di sekolah tiange). S (Anake luh ento) P (pragina) Pel (uli desan tiange). S (I Nyoman Budi) P (sopir motor) Pel (sane becik) Ket (saking desa Trunyan). S (Adin tiange) P (uli ibi semengan) Pel (melajah masepedaan). S (Bu guru punika) P (ka sekolah) Pel (nganggon sepeda)."

# 1st step: deleting paranthesis, dots, and capital letters
kalimat_bersih = kalimat.replace("(", "").replace(")", "").replace(".", "").replace("é", "e").lower()

# 2nd step: split the sentence into words
kata_kata = kalimat_bersih.split()

# 3rd step: removing 's', 'p', 'o', 'pel', 'ket' symbols
kata_utama = [kata for kata in kata_kata if kata not in ['s', 'p', 'o', 'pel', 'ket']]

# 4th step: remove duplicates and sort by first appearance
kata_unik = list(dict.fromkeys(kata_utama))

# 5th step: join the results and separate by comma
print(", ".join(kata_unik))