# Set-Up
pipenv install -r path/to/requirements.txt
------------------------------------------
Unter Umständen 'pipenv lock --clear'
https://stackoverflow.com/questions/56440090/pipenv-stuck-locking
"
Perhaps better terminology to describe this state would be 'Building and Locking...' or something similar.
This is especially likely to happen if you're installing numpy, opencv, pandas, or other large packages.
What's going on in the background is that pipenv is downloading your package and maybe building the wheel.
The remedy in this case is often a strong dose of patience.
"

# CodingTaskPricing
Programm-Aufbau:
Es gibt zwei Crawler: Einen für ToyForFun und einen für Amazon. 
Wichtig ist, dass das Script lego_princing_crawler.py zuerst ausgeführt wird.
Denn der Amazon-Crawler sucht nach den Artikeln, die bereits gefunden und in toysff.p abgelegt wurden.

Datenverarbeitung:
Die zwei Datensätze werden anhand der Artikel-Nummer gejoint,
um die Kalkulationen (Preisdifferenzes) durchzuführen.
Preissegmente werden anhand der Summe des Amazon- und ToysForFun-Preises bestimmt.
Prozentzahlen richten sich nach dem ToysForFun-Angebot.
Das Hauptscript kann mit (optionalen) Argumenten [--csv, --no-plot] über die Konsole gestartet werden.

Fazit:
Insgesamt liegt der Preis von Amazon durchschnittlich bei 7.9948 Euro weniger 
und durchschnitt 15.25 % unter dem ToysForFun-Angebot. 
Nur bei sehr erschwinglichen Produkten ist der Unterschied weniger auffällig.
Die Differenz liegt für das niedriges Preissegment nur bei 8,75%.
Bei den Subbrands ist die Differenz für NINJAGO (23.45%) und THE-MOVIE (21.32%) am höchsten.
Am niedrigsten fällt sie bei DISNEY-PRINCESS (11.53%) und ARCHITECTURE (10.32%) aus.  
Im Durchschnitt liegt die höchsten absolute Differenz bei THE-MOVIE (23.76 Euro) und TECHNIC (19.7 Euro),
die niedrigeste bei DISNEY PRINCESS (3.34 Euro) und CLASSIC (2.98 Euro).


# Bekannte Fehler
In zwei Fällen ist die Subbrand falsch,
da das falsche Listing schon auf der Toys-For-Fun Webseite passiert:

'https://www.toys-for-fun.com/de/legor-classic-10913-legor-duplor-steinebox.html'
'https://www.toys-for-fun.com/de/legor-classic-10914-legor-duplor-deluxe-steinebox.html'

Beide Artikel erscheinen fälschlicherweise unter 'https://www.toys-for-fun.com/de/kategorien/bauen-konstruieren/lego/classic.html'.
