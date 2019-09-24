# Spektrometer_GUI
GUI für das Infrarotspektrometer Experiment
Für die Analyse wird eine modifizierte Version von https://github.com/tonbut/RPiSpectrometer (MIT LICENSE) verwendet.

Bedienungsanleitung:
1. Spektrometer via USB mit dem entsprechenden Computer verbinden und ca. 45 Sekunden warten bis der Raspberry Pi betriebsbereit ist.
2. Die GUI starten und den Verbindungsknopf drücken. Bei einer erfolgreichen Verbindung zeigt das GUI Verbindung Aufgebaut an
3. Die Belichtungszeit einstellen und mittels OK bestätigen. Es dürfen nur ganze Zahlen eingegeben werden.
4. Spektrum aufnehmen und warten bis der Vorgang abgeschlossen ist und die Daten übertragen wurden. Die Daten sollten sich im Bilder Ordner des jeweiligen PC befinden. Die Software benennt dabei die Daten nach dem Schema Spektrum(NUMMER), die Nummer wird nach dem Neustart der GUI wieder auf 0 zurückgesetzt. Vor dem Neustart sollten die Daten daher gesichert werden, damit diese nicht überschrieben werden.
Die GUI zeigt dem Nutzer den Belichtungswert an, dieser sollte zwischen 0.15 und 0.3 liegen. Dieser Wert kann über die Belichtungszeit oder über die Helligkeit des Messobjekts eingestellt werden.
