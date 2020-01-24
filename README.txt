SEMESTRÁLNÍ PRÁCE BI-PYT
Autor: Dominik Krisztof <kriszdom@fit.cvut.cz>

CLI aplikace pro editaci obrázků.
Pro použití zavolejte main.py soubor s parametry.

Pouzite knihovy: argparse, numpy, pillow, pytest, unittest

python main.py [přepínače] CESTA_VSTUPNIHO_SOUBORU CESTA_KAM_ULOZIT_VYSLEDEK

Přepínače slouží k řetězení příkazů, NA POŘADÍ ZÁLEŽÍ.

pri ukladani prepisuje soubory

seznam použitelných filtrů
-h --help = vypíše zkrácenou nápovědu
--version = vypíše verzi programu
--rotate = otočí obrázek o 90 stupňů doprava
--mirror = zrcadlí obrázek zleva doprava
--inverse = otočí barvy na jejich opak (udělá modrou z červené apod.)
--bw = udělá obrázek černobílý (dle ITU-R 601-2 luma), vícero použití toho filtru nemá žádný vliv
--lighten <0-inf> = zesvětlí obrázek dle zadané hodnoty(při vysokých hodnotách se obrázek může barevně splynout v bílou)
--darken <0-inf> = ztmaví obrázek dle zadané hodnoty(při vysokých hodnotách se obrázek může barevně splynout v černou)

dostupné jsou i konvoluční metody, avšak při velkých obrázcích mohou být časově náročně
--sharpen  = zostření obrázku
--blur_3x3 = rozmazání obrázku (gaussian blur)
--blur_5x5 = rozmazání obrázku (gaussian blur), pouzívá širší kernel, takže rozmazání bude více dle okolí
--edge_detection = detekce hran (zvýrazní hrany)
--embossing = ražení obrázku (udělá reliéf)

Psáno pro verze python 3.5 a vyšší, autor nezaručuje kompabilitu pro již nepodoporované verze pythonu,
veškeré nazené bugy a nestandartní chování můžete poslat na email.

TODO:
- vyresit proc je treba workaround na lighten/darken testy (je treba je ulozit aby sedeli, prob. fomat error)
- v testech mockovat on test, né naráz pro všechny testy
- použít scipy convolution function, místo té co je teď implementovaná (slow)
- udělat funkce izolované tak, že vezmou jenom vstup a nebudou se hrabat v args
