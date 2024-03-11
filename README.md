# SNOMED-CT-PAT-FI-EN
status: draft


## Käyttöohjeet
Vain englanninkielisten rivien (lang = en) päivittäminen on mahdollista.

### Huomioita edelliseen versioon verrattuna
- Alkamis- ja päättymispäiviä ei tarvitse enää määritellä. Kone hoitaa ne automaattisesti. Niiden arvot päätetään erikseen päivityksen yhteydessä siten, että ne ovat yhdenmukaiset.
- Käsite ja termi muutosten yhteydessä tyhjennetään/muokataan vain sct sarake. Siitä tulee ns master sarake. Aiemmin päivittäjän täytyi muuttaa myös legacy sarakkeen loppu osaa.


## Uudet rivit
status sarakkeen arvon tulee olla "new"

## Inaktivoitavat rivit
status sarakkeen arvon tulee olla "inactivate"

## Muokattavat rivit

#### Pakolliset
- en-rivin alle tehdään uusi rivi jolla täytyy olla sama lineid kuin editoitavalla rivillä. status sarakkeen arvon tulee olla "edit"!
- Älä myöskään koske vanhan rivin sct_temid_en sarakkeeseen!
- Muista laitaa inaktivoinnin selitys sarakkeeseen reason_for_inactivation.
- Ei tarvitse laittaa päättymispäivää tai alkamispäivää, koska kone hoitaa sen automaattisesti. Määritellään erikseen päivityksen yhteydessä.

#### Käsite muutos
- Tyhjennä käsitteen sct_conceptid sarake. Tai laita uusi arvo jos tiedossa.
- Jos ei tapahdu termi muutosta, niin ei tarvitse koskea termid sarakkeisiin. Kone hoitaa termid muutokset automaattisesti käsitteen muutoksen yhteydessä.
- Termin muuttuessa jos haluat uudet generoidut termid:t, niin tyhjennä sct_termid sarakke. Tai laita uusi arvo sct_termid sarakkeeseen jos tiedossa.

#### termi
- Laita uusi termi sct_term sarakkeseen. Jätä sct_termid sarake tyhjäksi jos haluat generoidun id:n. Voit laitaa myös uuden termid:n tilalle.


### Logiikka
- Ota Excelistä vain englanninkieliset rivit.
- Filtteröi ja jaottele rivit status sarakkeen arvon mukaan (new, edit, inactivate).
- New on suht triviaali. Luodaan tarvittavat id:t jne ja sitten luodaan identtiset kielirivit suomeksi ja ruotsiksi.
- Inactivate on myös suht triviaali. Inaktivoi englanninkielinen rivi ja sitten inaktivoi suomen- ja ruotsinkieliset rivit.
- Edit on hieman vaikeampi tapaus. Ensi ajatuksella olisi parasta liputtaa muutos tyypi ja sitten määritellä "hoitopolku".
- Käsite muutos eli sct_conceptid on tyhjä. 
    - 


new_concept
new_term
nationalize_concept
nationalize_term
fsn
administrative
new
inactivate
activate
other



```mermaid
    classDiagram
    direction LR
    Matias --|> Koulu
    Matias --|> Tärkein-eli-Noora
    Koulu --|> HY
    Koulu --|> Aalto
    HY --|> Tietojenkäsittelytiede
    HY --|> Matematiikka
    Tietojenkäsittelytiede --|> Kandi
    Matematiikka --|> Koneoppimisen matematiikan perusteet I
    Matematiikka --|> Koneoppimisen matematiikan perusteet II
    Matematiikka --|> Tilastollinen päättely I
    Aalto --|> Yrityksen talouden johtaminen ja raportointi
    Aalto --|> Tilinpäätösraportointi
    Matias --|> HUS
    HUS --|> Kandi
    HUS --|> OMOP Arkkitehtuuri
    Matias --|> Datasta voimaa sote-järjestelmään työryhmä
    Sitra --|> Datasta voimaa sote-järjestelmään työryhmä
    STM --|> Datasta voimaa sote-järjestelmään työryhmä
    LANU --|> Datasta voimaa sote-järjestelmään työryhmä
    Koulu --|> AMC
    AMC --|> Pre-masters
    AMC --|> Asunto
    Pre-masters --|> Basics of Medicine
    Pre-masters --|> Biostatistics
    Pre-masters --|> Medical process and Medical decision making
    Pre-masters --|> Organisation of Healthcare
    Pre-masters --|> eHealth UX research 
    Pre-masters --|> Mathematics and Logic
    Pre-masters --|> Medical Record Keeping and Terminology Systems
    Pre-masters --|> Health Information Systems - Architectures and Strategy
    Pre-masters --|> Medical Images
    Pre-masters --|> Academic skills
    Pre-masters --|> Database Systems
    Matias --|> THL
    THL --|> SNOMED CT
    Mami-kannustaa --|> Matias
```

