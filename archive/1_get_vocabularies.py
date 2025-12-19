import re

def split_words(text):
    words = re.split(r'(?=[A-Z])', text)
    words = [w.strip() for w in words if w.strip()]
    return words

if __name__ == "__main__":
    print("Masukkan text (tekan Enter 2x untuk selesai):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    text = " ".join(lines)
    result = split_words(text)
    
    print("\nHasil split:")
    for word in result:
        print(f"  - {word}")
    
    with open("vocabularies_raw.txt", "a", encoding="utf-8") as f:
        for word in result:
            f.write(word + "\n")
    
    print(f"\nBerhasil ditambahkan ke vocabularies_raw.txt ({len(result)} kata)")