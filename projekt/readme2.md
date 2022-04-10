# Implementační dokumentace k 2. úloze do IPP 2021/2022

Jméno a příjmení: Jan Rodák
Login: xrodak00

## Cíl ```interpret.py```

Úkolem skriptu ```interpret.py``` je interpretovat XML reprezentaci jazyka ```IPPcode22``` generovanou ```parse.php```.

## Implementace ```interpret.py```

Skript ```interpret.py``` využívá návrhových vzorů a dalších objektově orientovaných principů a je rozdělen do několika logických částí, které jsou uloženy ve složce ```interpret_libs```. Řešení celého problému je rozděleno na jednotlivé podproblémy, kterými jsou: zpracování parametrů od uživatele na příkazové řádce, zpracování vstupní XML reprezentace kódu ```IPPCode22``` a vytvoření objektů instrukcí, interpretace jednotlivých instrukcí a vytvoření statistik o interpretovaném kódu.

### Zpracování argumentů od uživatele

Pro zpracování argumentů od uživatele byla vytvořena třída ```CommandLineApi```, která slouží jako adaptér pro třídu ```ArgumentParser``` z knihovny ```argparse``` a také jako rozhraní pro získávání informací o parametrech uvedených v příkazové řádce.

### Zpracování vstupní XML reprezentace kódu ```IPPCode22``` a vytvoření objektů instrukcí

Zpracování vstupní XML reprezentace kódu ```IPPCode22``` je implementováno třídou ```ParserXML```, která zpracovává xml pomocí knihovny ```lxml```, inicializuje objekty tříd pro příslušné instrukce a ukládá je do pole v pořadí, ve kterém budou provedeny. Instrukce v poli jsou seřazeny podle atributu ```order```.

#### Instrukce

Každá instrukce je potomkem třídy ```Instruction```, ve které jsou naimplementovaná rozhraní pro metodu provedení instrukce a další pomocné metody pro získání operandů, např. uložení symbolu do paměti atd. Zásobníkové instrukce jsou potomci jejich nezásobníkových verzí instrukcí.

#### Operandy Instrukcí

Implementace operandů je uložena v souboru ```instructions_args.py```,každý typ operandu instrukce je objekt se svými specifickými vlastnostmi a sémantickými kontrolami. Např. operand Symbolu implementuje metody pro přetížení matematických operátorů, takže se dají mezi nimi provádět matematické operace.

### Interpretace jednotlivých instrukcí

Pro interpretaci jednotlivých instrukcí je vytvořena třída ```InterpretrEngine```, která má na starosti správu paměťových rámců a spouštění jednotlivých instrukcí v daném pořadí.

### Vytvoření statistik o interpretovaném kódu

K tomuto účelu je vytvořena třída ```Stats```, která uchovává statistické informace o zpracovávaném kódu. Instance třídy dle parametrů zadaných uživatelem tiskne příslušné statistiky do souborů.

## Cíl ```test.php```

Úkolem skriptu ```test.php``` je otestovat skripty ```parse.php``` a ```interpretr.py``` pomocí testů vytvořených uživatelem a vytvořit zprávu o proběhnutých testech.

## Implementace ```test.php```

Skript ```test.py``` využívá návrhových vzorů a dalších objektově orientovaných principů a je rozdělen do několika logických částí, které jsou uloženy ve složce ```test_libs```. Řešení celého problému je rozděleno na jednotlivé podproblémy, kterými jsou: zpracování parametrů od uživatele na příkazové řádce, načtení testů, vytvoření objektové reprezentace testů, otestovaní skriptů a generace html reportu o provedených testech.

### Zpracování argumentů od uživatele

Zpracování argumentů od uživatele byla je vytvořena obdobným způsobem jako ve skriptu ```parse.php```. Je vytvořena třída ```ArgParser```. Samotné zpracování a kontrola správnosti parametrů a zkontrolování existence potřebných souborů je provedeno metodou ```parse()```.

### Načtení testů a vytvoření objektové reprezentace testů

Pro načtení testů a vytvoření objektové reprezentace je vytvořena třída ```TestEngine```, která má na starosti vytvoření objektové reprezentace testů, provedení testů a vygenerovaní html reportu s výsledky testů.

#### Testy

Každý objekt testu je potomek abstraktní třídy ```Test```, kde jsou implementovány jednotlivé části testu, jako je spuštění skriptu s danými parametry, porovnání výstupu s referenčními hodnotami a reprezentace testu v html.

#### Generace html reportu o provedených testech

Pro reprezentaci testu byl využit html5 tag ```details```, který po rozkliknutí zobrazí informace o testu. V případě, že test neprošel, bude již automaticky rozbalen, takže uživatel uvidí vstupy, výstupy a další informace o provedeném testu.
