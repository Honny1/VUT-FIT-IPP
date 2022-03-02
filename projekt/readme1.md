# Implementační dokumentace k 1. úloze do IPP 2021/2022

Jméno a příjmení: Jan Rodák
Login: xrodak00

## Cíl ```parse.php```

Úkolem skriptu ```parse.php``` je zpracovat ze standardního vstupu od uživatele kód v jazyce ```IPPcode22```. Nad vstupním kódem provede lexikální a syntaktickou analýzu a vygeneruje XML reprezentaci tohoto kódu, kterou tiskne na standardní vystup.

## Implementace ```parse.php```

Skript ```parse.php``` využívá návrhového vzoru abstraktní továrny a dalších objektově orientovaných principů a je rozdělen do několika logických částí, které jsou uloženy ve složce ```parse_libs```. Řešení celého problému je rozděleno na jednotlivé podproblémy, které jsou zpracování parametrů od uživatele na příkazové řádce, zpracování vstupního kódu a vytvoření statistik o zpracovávaném kódu.

### Zpracování argumentů od uživatele

Pro účel zpracování argumentů od uživatele byla vytvořena třída ```ArgParser```. Samotné zpracování a kontrola správnosti parametrů je provedena metodou ```parse()```. Tato metoda vrací pole kde klíč je název souboru kam se mají uložit statistiky a pole parametrů statistik, pro určení kterých statistik je třeba uložit do souboru. V případě zadání chybného parametru vypíše chybovou hlášku, zobrazí nabídku help a ukončí skript s příslušným návratovým kódem.

### Zpracování vstupního kódu

Zpracování vstupního kódu je implementováno třídou ```CodeParser```, která inicializuje třídu pro práci se statistikou o zpracovávaném kódu a třídy pro generování XML.

Zpracování kódu je prováděno metodou ```parse()```, která zpracovává vstupní kódu po řádku a je volaná rekurzivně. Zpracování řádku je prováděno tak že se odstraní bílé znaky ze začátku a konce řádku. Poté je odstraněn komentář. V případě že po odstranění komentáře a bílých znaků řádek není prázdný je provedeno zpracování instrukce. V případě konce souboru je vytisknuto XML na standardní výstup.

Pro zpracování instrukce je vytvořena abstraktní třída ```AbstractInstruction```, která slouží jako základ pro definování ostatních tříd instrukcí podle počtu jejich operandů. Definuje základní vlastnosti tříd instrukcí jako jsou kontrola správného zápisu celé instrukce, validace jednotlivých typů operandů instrukcí, aktualizace statistiky a reprezentace v XML kódu. Jednotlivé kontroly operandů instrukcí jsou prováděny regulárními výrazy.

Zpracování jedné instrukce je provedeno tak že je celý řádek rozdělen podle bílých znaků. A následně podle operačního kódu instrukce je vytvořena příslušná instance instrukce a jsou zavolané metody pro kontrolu instrukce, aktualizaci statistik a reprezentaci v XML kódu.

### Vytvoření statistik o zpracovávaném kódu

K tomuto účelu je vytvořena třída ```Stats```, která uchovává statistické informace o zpracovávaném kódu a ukládá tyto informace ukládá do souborů podle pole zadaných parametrů uživatelem.
