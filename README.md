# Guide til at se hvornår tider er booket for kapsejlads Google kalender 


**1. Find kalender logs**
- Logs kan findes på Google Takeout: https://takeout.google.com/
- For at kunne finde det, kræver det man er administrator (kapansvarlig). Umbi IT kan give adgang. 

På takeout
- Fravælg alle
- Søg efter Kalender, så skal du gerne kunne finde Google Kalender
- Tryk på knappen med "Alle kalendre medtages" og vælg kun Kapsejladsen 
- Scroll ned i bunden og tryk næste 
- Følg trinene, og modtag data i en zip. Jeg plejer få dem sendt på mail. 
- Du skulle gerne have en .ics fil (kalender fil)


**2. Sorter data**
- Data kan åbnes i excel, texteditor, vscode eller lignende. Det er klart nemmest i Excel.
- Alle bookninger står uden luft, men adskilles af "BEGIN:VEVENT" og "END:VEVENT". 
- De vigitge datapunkter er "CREATED" (tid bookning blev lavet), "DTSTART" (bookningens start), "DTEND" (bookningens slut) og "SUMMARY" (teskt, forening)
- Tidspunkter står i syntaxen "CREATED:20250323T185217Z", som her skal forstås som 2025/03/23 18:52:17, altså den 23. marts 2025 kl 18:52:17
- Der kan laves log for alle data, men det bliver MEGET, så sorter evt. efter kun en dag. F.eks hvis alle booker om søndagen. 
- Brug Excels søge funktion (ctr + f) på den ønskede dato "CREATED:20250323". Brug evt. udviddet søgning, hvis den brokker sig. 
- Bookningerne er i kronologisk rækkefølge efter "CREATED", så man kan nemt se hvilke rækker man skal slette fra

VIGTIGT! 
- Slet data fra første bookning, til det ønskede sted. 
- SLET ALTSÅ IKKE INFO I STARTEN 
- Led efter den første "BEGIN:VEVENT" fra toppen, disse linjer kommer før: 
![alt text](/images/image.png)

- Efter at have slettet de ønskede rækker gemmes filen ctr+s


**3. Tilføj datafil til mappen**
- Flyt filen til denne mappe
- Sørg for at der ikke er andre .ics filer på samme niveau. Hvis der er, læg dem i en mappe	


**4. Kør programmet**
- Programmet kan køres både i vscode og i terminalen. Brug terminalen for at kunne gemme en lækker pdf med ctr+p (se vedhæftet)
- Evt. importer re med pip om nødvendigt.
- Ellers kør med python3 ics_parser.py

**BEMÆRK**\
Tiden
- Hvis du ikke allerede har bemærket det, er det meget sandsynligt Google har tilrettet tiderne til en anden tidszone. 
- Dette program er tilrettet således: 
    - Der lægges 1 time til CREATED 
    - Der lægges 2 timer til DTSTART og DTEND
- Jeg ved ikke om dette vil være tilfældet altid 

Korekthed 
- Programmet er rigtig meget skrevet af claude.ai, så tager intet ansvar for det. 
