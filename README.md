# Proiect Wordle ASC
## Echipa

* Bogdan Vlad-Mihai (grupa 152)
* Cocheci Cristiana (grupa 152)
* Dumitrescul Eduard (grupa 132)
* Pecheanu Anna-Angela (grupa 152)

#### Numărul mediu de încercări pentru ghicirea tuturor cuvintelor: 3.9802689016937314

## Scurtă descriere
Proiectul simulează bine-cunoscutul joc Wordle popularizat de NYTimes, fiind însoțit de un program-suport, care sugerează în timp real utilizatorului cuvântul optim pentru rezolvarea în număr minim de pași a puzzle-ului. Acesta se folosește de concepte din teoria informației, precum Entropia lui Shannon.

## Structură

* **cuvinte_wordle.txt**: lista tuturor cuvintelor de 5 litere din limba română, fără diacritice
* **dataSource.py**: gestionează fișierele text și analizează frecvența literelor a cuvintelor din dicționar
* **engine.py**: se ocupă cu calculul entropiei cuvintelor, selecția cuvântului optim și reducerea listei de răspunsuri posibile
* **game.py**: creează și controlează sesiunea de joc propriu-zisă
* **main.py**: se ocupă cu pornirea *Game-ului* și a *Engine-ului*, legătura dintre cele două făcându-se folosind librăria *multiprocessing*
* **second.txt**, **third.txt**: fișiere utilizate pentru o mai rapidă calculare a numărului mediu de încercări, în condițiile unui joc cu alegeri optime. Reprezintă o precalculare ale celor mai bune cuvinte pentru al doilea, respectiv pentru al treilea pas, în funcție de răspunsurile de la pașii anteriori.
* **soluții.txt**: fișier care conține soluțiile găsite de Engine pentru fiecare cuvânt din dicționar

## Algoritm 

Pentru fiecare cuvânt din lista de cuvinte posibile, algoritmul calculează cantitatea medie de informație pe care acesta o va obține, comparându-l cu toate cuvintele din lista de răspunsuri posibile, încercând să uniformizeze distribuția răspunsurilor primite. Pentru găsirea cuvintelor de la primii doi pași, se folosește un algoritm euristic pe două nivele, iar pentru pașii următori se alege cuvântul cu cea mai mare entropie.

## Referințe
* https://www.youtube.com/watch?v=TQx3IfCVvQ0&ab_channel=LucidProgramming
* https://www.youtube.com/watch?v=v68zYyaEmEA&ab_channel=3Blue1Brown
* https://www.youtube.com/watch?v=fRed0Xmc2Wg&ab_channel=3Blue1Brown
* https://towardsdatascience.com/information-theory-applied-to-wordle-b63b34a6538e
