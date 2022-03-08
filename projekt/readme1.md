# Implementační dokumentace k 1. úloze do IPP 2021/2022

Jméno a příjmení: Jan Rodák
Login: xrodak00

## Cíl ```parse.php```

Úkolem skriptu ```parse.php``` je zpracovat ze standardního vstupu od uživatele kód v jazyce ```IPPcode22```. Nad vstupním kódem provede lexikální a syntaktickou analýzu a vygeneruje XML reprezentaci tohoto kódu, kterou tiskne na standardní výstup.

## Implementace ```parse.php```

Skript ```parse.php``` využívá návrhového vzoru abstraktní továrny a dalších objektově orientovaných principů a je rozdělen do několika logických částí, které jsou uloženy ve složce ```parse_libs```. Řešení celého problému je rozděleno na jednotlivé podproblémy, kterými jsou: zpracování parametrů od uživatele na příkazové řádce, zpracování vstupního kódu a vytvoření statistik o zpracovávaném kódu.

### Zpracování argumentů od uživatele

Pro zpracování argumentů od uživatele byla vytvořena třída ```ArgParser```. Samotné zpracování a kontrola správnosti parametrů je provedena metodou ```parse()```. Tato metoda vrací pole, kde je klíčem název souboru, do kterého se mají uložit statistiky, a hodnota pole parametrů statistik. V případě zadání chybného parametru nebo opakování názvu souboru vypíše chybovou hlášku, zobrazí nabídku help a ukončí skript s příslušným návratovým kódem.

### Zpracování vstupního kódu

Zpracování vstupního kódu je implementováno třídou ```CodeParser```, která inicializuje třídu pro práci se statistikou o zpracovávaném kódu a třídy pro generování XML.

Zpracování kódu je prováděno metodou ```parse()```, která zpracovává vstupní kód po řádku a je volaná rekurzivně. Zpracování řádku je prováděno tak, že se ze začátku a z konce řádku odstraní bílé znaky. Poté je odstraněn komentář. V případě, že po odstranění bílých znaků a komentáře řádek není prázdný, je provedeno zpracování instrukce. V případě konce souboru je vytisknuto XML na standardní výstup.

Pro zpracování instrukce je vytvořena abstraktní třída ```AbstractInstruction```, která slouží jako základ pro definování ostatních tříd instrukcí podle počtu jejich operandů. Definuje základní vlastnosti tříd instrukcí, jako jsou kontrola správného zápisu celé instrukce, validace jednotlivých typů operandů instrukcí, aktualizace statistiky a reprezentace v XML kódu. Jednotlivé kontroly operandů instrukcí jsou prováděny regulárními výrazy.

Zpracování jedné instrukce je provedeno tak, že je celý řádek rozdělen podle bílých znaků. Následně podle počtu operandů a operačního kódu instrukce je vytvořena příslušná instance instrukce a jsou zavolané metody pro kontrolu instrukce, aktualizaci statistik a reprezentaci v XML kódu.

### Vytvoření statistik o zpracovávaném kódu

K tomuto účelu je vytvořena třída ```Stats```, která uchovává statistické informace o zpracovávaném kódu. Instance třídy dle parametrů zadaných uživatelem tiskne příslušné statistiky do souborů.
