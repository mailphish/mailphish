# Proč lidé klikají: poznámky k návrhu scénářů

Tyto poznámky shrnují, co z veřejně dostupných studií a benchmarků o
phishingu/security awareness trainingu dává smysl použít při návrhu
cvičných e-mailů v tomto repozitáři, a proč jsou šablony v této složce
postavené tak, jak jsou. Je to podklad pro tým (a pro budoucí vzdělávací
stránku zmíněnou v [README](../../README.md)), ne návod k útoku na reálné
cíle — viz oddíl *Etika a hranice použití* na konci.

## 1. Psychologické principy, které návnady využívají

Většina úspěšných phishingových předmětů dlouhodobě kombinuje jeden až dva
z klasických Cialdiniho principů persvaze:

- **Autorita** – zpráva vypadá, že přichází od IT, HR, vedení firmy nebo
  systému, kterému uživatel důvěřuje a nezpochybňuje jeho pokyny.
- **Urgence / časová tíseň** – krátká lhůta ("24 hodin", "dnes", "než se
  účet uzamkne") potlačuje racionální ověřování a vede k rychlému kliknutí.
- **Strach ze ztráty** – ztráta přístupu k účtu, zablokovaná schránka,
  neoprávněné přihlášení, penalizace rozpočtu.
- **Zvědavost / odměna** – sdílený dokument s citlivým názvem, bonusy,
  benefity, nečekaná zásilka.
- **Sociální důkaz** – "87 % kolegů už potvrdilo svou volbu" snižuje pocit,
  že je v pořádku akci odložit nebo se zeptat.
- **Izolace a tajnůstkářství** (typické pro CEO fraud / BEC) – žádost
  "neřeš to zatím s nikým dalším" znemožňuje standardní ověření druhou
  osobou.

## 2. Co z dat skutečně podporuje výběr témat

Primární zdroje s detailním rozpadem úspěšnosti podle konkrétní návnady
(heslo vs. faktura vs. sdílený dokument) jsou bohužel rozptýlené a často
nekonzistentní mezi dodavateli. Dohledatelné a vzájemně víceméně shodné
body:

- Dlouhodobé žebříčky nejúspěšnějších předmětů (opakovaně napříč lety u
  dodavatelů typu KnowBe4) stabilně obsazují témata: **vypršení/reset
  hesla, oznámení IT/mail systému (např. plná schránka), HR/mzdové a
  benefitní zprávy, notifikace o sdíleném dokumentu, a zprávy o doručení
  zásilky**. Proto je právě těchto pět témat jádrem šablon v této složce.
- Cvičné phishingové kampaně mají podle Verizon DBIR mediánovou míru
  prokliku řádově jen několik procent (často citováno okolo 1–3 %), což
  ukazuje, že i v reálných firmách funguje jen malá část zpráv – důležité
  je tedy mít víc různých návnad a sledovat trend v čase, ne jeden scénář.
- Školení má měřitelný efekt: benchmarky dodavatelů security awareness
  trainingu (např. KnowBe4) opakovaně uvádí výrazný pokles míry prokliku
  po opakovaném tréninku v průběhu 12 měsíců u stejné skupiny zaměstnanců
  – to je důvod, proč appka plánuje "aggregate counts" a opakovaná
  cvičení, ne jednorázovou kampaň.
- BEC/CEO fraud (cílená osobní zpráva "od vedení" s žádostí o platbu nebo
  citlivou akci) je samostatná kategorie s jiným mechanismem útoku
  (navázaná konverzace, ne jen klik na odkaz) – DBIR ji sleduje odděleně od
  klasického hromadného phishingu. Aktuální sada šablon v této složce se
  soustředí na hromadné, brandované návnady s měřitelným prokliknutím;
  BEC scénář je možné doplnit samostatně, až bude jasné, jak ho bude
  prototyp měřit (jde o konverzaci, ne o jeden odkaz).
- Nárůst AI-generovaných návnad je opakovaně zmiňovaný trend u více
  dodavatelů pro 2026, s tvrzením o výrazně vyšší míře prokliku než u
  šablonovitých zpráv — číselné odhady se mezi zdroji dost liší a nejsou
  jednotně verifikované, takže je zde neuvádíme jako přesná čísla, jen
  jako důvod, proč i cvičné šablony stojí za čas (osobní jméno, kontext
  oddělení, realistický jazyk) místo generického textu.

Zdroje k dalšímu ověření (vendor blogy, agregují data z primárních
reportů, čísla se mezi nimi liší – brát jako orientační, ne jako citaci do
závěrečné práce bez dohledání primárního reportu):

- Verizon Data Breach Investigations Report (DBIR) – aktuální ročník,
  sekce o social engineering a phishing simulation.
- KnowBe4 – výroční "Phishing by Industry Benchmarking Report" a seznamy
  "Top Clicked Phishing Email Subjects".
- Pistachio – "Phishing Behaviour Report".
- Proofpoint – "State of the Phish" (ověřit čísla o AI-generovaných
  zprávách přímo v reportu, ne přes druhotné zdroje).

## 3. Proč méně typů zpráv, ale více známých značek

Vlastní zkušenost i dostupná data (viz výše) ukazují, že účastníci
nerozpoznávají phishing primárně podle *druhu žádosti* (reset hesla vs.
faktura), ale podle toho, jestli zpráva *vypadá jako od firmy, které
důvěřují*. Proto je knihovna navržená opačně, než v první verzi: místo
mnoha různých fiktivních pretextů pod jednou neznámou fiktivní firmou
(*Nordex Trading*) používá jen **tři typy situací**, každý ve variantě pro
**dvě skutečné, celosvětově nebo lokálně velmi známé značky**. To
zvyšuje realističnost (účastníci tyto služby skutečně používají) a
zároveň umožňuje v debriefu porovnat, jak stejný trik vypadá pod různým
brandingem.

| Typ zprávy | Soubor | Napodobovaná značka | Hlavní spouštěč |
| --- | --- | --- | --- |
| Účet / bezpečnostní upozornění | [`01-microsoft-account-alert.html`](01-microsoft-account-alert.html) | Microsoft 365 | autorita + strach + urgence |
| Účet / bezpečnostní upozornění | [`02-google-account-alert.html`](02-google-account-alert.html) | Google | autorita + strach + urgence |
| Oznámení o doručení zásilky | [`03-zasilkovna-delivery.html`](03-zasilkovna-delivery.html) | Zásilkovna / Packeta | zvědavost + urgence + drobný poplatek |
| Oznámení o doručení zásilky | [`04-dhl-delivery.html`](04-dhl-delivery.html) | DHL | zvědavost + urgence + drobný poplatek |
| Sdílený dokument | [`05-google-drive-shared-file.html`](05-google-drive-shared-file.html) | Google Drive | důvěra + zvědavost + sociální důkaz |
| Sdílený dokument | [`06-onedrive-shared-file.html`](06-onedrive-shared-file.html) | Microsoft OneDrive | důvěra + zvědavost + sociální důkaz |

Výběr značek kombinuje globální (Microsoft, Google, DHL) a lokální české
(Zásilkovna) služby, protože cílová skupina cvičení jsou čeští
zaměstnanci a místně známá značka funguje jako návnada minimálně stejně
dobře jako globální.

Každý soubor má v HTML komentáři na začátku uvedené **red flags pro
debrief** – konkrétní varovné signály (hlavně look-alike doména
odesílatele, která nikdy neodpovídá reálné doméně dané značky), které
účastníkům po cvičení vysvětlí vzdělávací stránka zmíněná v plánovaném
prototypu. Tyto komentáře se při odesílání e-mailu nezobrazují, slouží jen
administrátorovi cvičení a autorům materiálů.

Vizuální styl (barvy, rozvržení, tón textu) každé šablony byl ověřen
pohledem na veřejné stránky dané značky (microsoft.com, workspace.google.com,
zasilkovna.cz, dhl.com) v listopadu 2026. Značkové logo samotné nikde
nepoužíváme jako obrázek – je nahrazeno jednoduchými CSS tvary nebo
barevným textem ve veřejně známé firemní barevné paletě, aby šablony
nereprodukovaly chráněné grafické aktivum dané firmy. Všechny domény
odesílatele jsou na `.example` (rezervovaná doména dle RFC 2606, nikde
reálně nenasměrovaná) a jsou stylizované jako typický look-alike vzor
(písmeno nahrazené číslicí, přidané slovo jako "verify"/"notify"/"security"
do subdomény), aby bylo jasné, že jde o cvičný materiál, a zároveň aby
demonstrovaly skutečný vzor, který útočníci používají.

## 4. Etika a hranice použití

- Tento repozitář je školní projekt a šablony jsou určené výhradně pro
  **vlastní, kontrolované cvičné prostředí** popsané v
  [README](../../README.md) – tedy pro účastníky, kteří jsou předem
  seznámeni s tím, že se v organizaci provádí awareness training (nebo je
  cvičení prováděno v rámci výuky s fiktivními účastníky), ne pro
  neautorizované testování reálných lidí mimo tento rámec.
- Šablony cíleně **nepožadují reálná citlivá data** (hesla, čísla karet)
  v samotném textu ani nikde neobsahují skutečné firmy, jména osob nebo
  funkční odkazy mimo cvičné prostředí.
- Při skutečném nasazení (i interním) je nutné mít předem schválení
  vedení/etické komise, informovaný souhlas v souladu s interní politikou
  organizace, a jasný proces okamžitého vzdělávacího zásahu po kliknutí
  (ne jen "sledování", ale vysvětlení, proč to byla návnada).
