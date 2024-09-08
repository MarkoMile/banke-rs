# Banke-RS - Alat za analizu bankarskog tržišta

Alat za analizu bankarskog tržišta i uspeha pojedinačnih banaka, razvijen u okviru seminara Računarskih finansija u Istraživačkoj stanici Petnici 2024. godine.

Napravili: [Jovan Ivković](https://github.com/jovanivko), Đorđe Simić, [Marko Milenković](https://github.com/MarkoMile) i mentor Jasna Atanasijević.

 * Pogledajte [Upotreba](#Upotreba) za uputstvo kako koristiti ovaj repozitorijum.
 * Pogledajte [Primer](#Primer) za primer programa.

# Sposobnosti

Program prikuplja podatke sa sajta NBS (Narodna banka Srbije) o bilansima stanja i uspeha pojedinačnih banaka za 2022. i 2023. godinu. Ovi podaci se analiziraju, obrađuju i vizualizuju u programu. Banke se grupišu korišćenjem k-means i PCA metoda.

Podaci prikazani za celo tržište:
* UKUPNA AKTIVA 2023, RAST AKTIVE, UKUPAN DEPOZIT 2023, RAST DEPOZITA, UKUPAN KREDIT 2023, RAST KREDITA

Podaci prikazani za pojedinačne banke:
* RANG PO AKTIVI, UKUPNA AKTIVA, NETO KAMATNA MARŽA, POVRAĆAJ NA SOPSTVENI KAPITAL, KOEFICIJENT LIKVIDNOSTI, STOPA OBEZVREĐENJA

# Primer

<p align="center">
<img src="media/banke-rs-example-hq.gif" alt="banke-rs-example">
</p>

# Upotreba

### Preduslovi
Pre nego što pokrenete program, uverite se da imate sledeće:

* Python 3.x
* Instalirajte potrebne pakete iz `requirements.txt`

Da biste instalirali pakete, pokrenite sledeću komandu: ```pip install -r requirements.txt```

### Pokretanje programa
Nakon instalacije paketa, možete pokrenuti program sa sledećom komandom: ```python ./gui.py```.

Napomena: Prilikom prvog pokretanja programa, može potrajati dok se podaci ne preuzmu i obrade.
