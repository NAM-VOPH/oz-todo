# -*- coding: utf-8 -*-
"""
Mapovani PSC -> okres -> kraj pro CR.
PSC_MAP  : presne 5-mistne PSC (pokryva vsechny adresy v datech)
PREFIX_MAP: fallback podle prvnich 3 cislic (pro nove zakazniky)
"""

OKRES_KRAJ = {
    "Praha": "Hlavní město Praha",
    # Stredocesky
    "Benešov": "Středočeský", "Beroun": "Středočeský", "Kladno": "Středočeský",
    "Kolín": "Středočeský", "Kutná Hora": "Středočeský", "Mělník": "Středočeský",
    "Mladá Boleslav": "Středočeský", "Nymburk": "Středočeský",
    "Praha-východ": "Středočeský", "Praha-západ": "Středočeský",
    "Příbram": "Středočeský", "Rakovník": "Středočeský",
    # Jihocesky
    "České Budějovice": "Jihočeský", "Český Krumlov": "Jihočeský",
    "Jindřichův Hradec": "Jihočeský", "Písek": "Jihočeský",
    "Prachatice": "Jihočeský", "Strakonice": "Jihočeský", "Tábor": "Jihočeský",
    # Plzensky
    "Domažlice": "Plzeňský", "Klatovy": "Plzeňský", "Plzeň-město": "Plzeňský",
    "Plzeň-jih": "Plzeňský", "Plzeň-sever": "Plzeňský", "Rokycany": "Plzeňský",
    "Tachov": "Plzeňský",
    # Karlovarsky
    "Cheb": "Karlovarský", "Karlovy Vary": "Karlovarský", "Sokolov": "Karlovarský",
    # Ustecky
    "Děčín": "Ústecký", "Chomutov": "Ústecký", "Litoměřice": "Ústecký",
    "Louny": "Ústecký", "Most": "Ústecký", "Teplice": "Ústecký",
    "Ústí nad Labem": "Ústecký",
    # Liberecky
    "Česká Lípa": "Liberecký", "Jablonec nad Nisou": "Liberecký",
    "Liberec": "Liberecký", "Semily": "Liberecký",
    # Kralovehradecky
    "Hradec Králové": "Královéhradecký", "Jičín": "Královéhradecký",
    "Náchod": "Královéhradecký", "Rychnov nad Kněžnou": "Královéhradecký",
    "Trutnov": "Královéhradecký",
    # Pardubicky
    "Chrudim": "Pardubický", "Pardubice": "Pardubický", "Svitavy": "Pardubický",
    "Ústí nad Orlicí": "Pardubický",
    # Vysocina
    "Havlíčkův Brod": "Vysočina", "Jihlava": "Vysočina", "Pelhřimov": "Vysočina",
    "Třebíč": "Vysočina", "Žďár nad Sázavou": "Vysočina",
    # Jihomoravsky
    "Blansko": "Jihomoravský", "Brno-město": "Jihomoravský",
    "Brno-venkov": "Jihomoravský", "Břeclav": "Jihomoravský",
    "Hodonín": "Jihomoravský", "Vyškov": "Jihomoravský", "Znojmo": "Jihomoravský",
    # Olomoucky
    "Jeseník": "Olomoucký", "Olomouc": "Olomoucký", "Prostějov": "Olomoucký",
    "Přerov": "Olomoucký", "Šumperk": "Olomoucký",
    # Zlinsky
    "Kroměříž": "Zlínský", "Uherské Hradiště": "Zlínský", "Vsetín": "Zlínský",
    "Zlín": "Zlínský",
    # Moravskoslezsky
    "Bruntál": "Moravskoslezský", "Frýdek-Místek": "Moravskoslezský",
    "Karviná": "Moravskoslezský", "Nový Jičín": "Moravskoslezský",
    "Opava": "Moravskoslezský", "Ostrava-město": "Moravskoslezský",
    # mimo CR
    "Bratislava": "Slovensko",
}

# --- presne 5-mistne PSC ---------------------------------------------------
PSC_MAP = {}

def _add(okres, *pscs):
    for p in pscs:
        PSC_MAP[str(p).zfill(5)] = okres

# Praha
_add("Praha", 10000,10100,10800,11000,11101,11800,12000,13000,14000,14100,14200,
     14800,14900,15500,15531,16200,16300,17000,18200,18600,19000,19011,19300,19600,19800)
# Stredocesky
_add("Praha-východ", 25001,25067,25087,25088,25092,25162,25164,25166)
_add("Praha-západ", 25206,25225,25230,25241,25242,25244,25263,25266,25301)
_add("Benešov", 25601,25721,25726,25744,25751,25756,25801)
_add("Příbram", 25791,26101,26272,26301,26401)
_add("Beroun", 26601,26706,26707,26753,26801)
_add("Rakovník", 26901,27004,27101)
_add("Kladno", 27061,27201,27204,27303,27305,27309,27351)
_add("Mělník", 25070,27601,27706,27711,27713,27742,27744,27746,27801)
_add("Kolín", 28002,28104,28121,28123,28126,28127,28144,28201,28911)
_add("Kutná Hora", 28401,28547)
_add("Nymburk", 28802,28912,28924,29001)
_add("Mladá Boleslav", 29301,29421,29429,29471)
# Plzensky
_add("Plzeň-město", 30100,31200,32200,32300,32600,33003,33202)
_add("Plzeň-sever", 33012,33021,33022,33023,33151,33165)
_add("Plzeň-jih", 33301,33401,33453)
_add("Rokycany", 33701,33828,33844)
_add("Klatovy", 33901,34034,34101,34192)
_add("Domažlice", 34522,34534,34545,34561,34601)
_add("Tachov", 34701,34806,34813,34901,34953,34961)
# Karlovarsky
_add("Cheb", 35201,36461)
_add("Sokolov", 35601,35731,35735,35751,35801)
_add("Karlovy Vary", 36001,36004,36221,36222,36235,36301,36401,36471)
# Jihocesky
_add("České Budějovice", 37001,37005,37006,37010,37341,37344,37401)
_add("Jindřichův Hradec", 37701,37810,37821,37856,37883,37901)
_add("Český Krumlov", 38101,38203,38241,38273)
_add("Prachatice", 38301,38402,38411,38421,38422,38451,38481,38486,38501)
_add("Strakonice", 38601,38701,38715,38731,38733,38743,38801)
_add("Tábor", 39001,39002,39005,39101,39102,39111,39126,39131,39155,39161,39175,39181,39201)
_add("Pelhřimov", 39301,39403,39464,39501,39601)
_add("Písek", 39701,39801,39806,39842,39901)
# Ustecky
_add("Ústí nad Labem", 40001,40004,40007,40010,40011,40331,40335)
_add("Děčín", 40502,40505,40701,40721,40742,40744,40746,40747,40753,40761,40777,40779,40801)
_add("Litoměřice", 41002,41108,41112,41117,41119,41172,41174,41181,41201,41301)
_add("Teplice", 41501,41503,41705,41712,41801,41901)
_add("Chomutov", 43111,43151,43201)
_add("Most", 43401,43511,43601,43603)
_add("Louny", 43801,43907,43921,43923,44001,44101)
# Liberecky
_add("Liberec", 46001,46006,46014,46312,46331,46342,46343,46352,46365,46401)
_add("Jablonec nad Nisou", 46601,46604,46811)
_add("Česká Lípa", 47001,47006,47107,47124,47127,47154,47301)
_add("Semily", 51246)
# Kralovehradecky
_add("Hradec Králové", 50002,50012,50346)
_add("Jičín", 50601,50723,50781,50901)
_add("Rychnov nad Kněžnou", 51701,51750,51773)
_add("Trutnov", 54102,54103,54232,54242,54401)
_add("Náchod", 54901,54921,54941,54952,54957)
# Pardubicky
_add("Pardubice", 53009,53304,53312,53341,53401)
_add("Chrudim", 53701,53803,53804,53842,53851,53901,53944,53952)
_add("Ústí nad Orlicí", 56161,56401,56601)
_add("Svitavy", 56902,56955)
# Vysocina
_add("Havlíčkův Brod", 58266,58283,58291)
_add("Jihlava", 58601,58813,58851,58861)
_add("Žďár nad Sázavou", 59101,59231)
_add("Třebíč", 67401,67505)
# Jihomoravsky
_add("Brno-město", 60200,61600,62100,62700,62800,63800)
_add("Brno-venkov", 66424,66471,66701)
_add("Znojmo", 66902)
_add("Blansko", 67801,68001)
_add("Vyškov", 68301,68501)
_add("Břeclav", 69105,69106,69163)
_add("Hodonín", 69501,69661,69662)
# Zlinsky
_add("Uherské Hradiště", 68601,68703,68801)
_add("Zlín", 76005,76312,76321,76502)
_add("Kroměříž", 76701,76805,76821,76901)
# Olomoucky
_add("Přerov", 75002,75301,75353)
_add("Olomouc", 77900,78335,78344,78386)
_add("Šumperk", 78805,78815,78901,78969)
_add("Jeseník", 79001,79084)
_add("Prostějov", 79601,79823)
# Moravskoslezsky
_add("Ostrava-město", 70030,70800,70900,71600)
_add("Karviná", 73401,73506,73601,73701)
_add("Frýdek-Místek", 73801)
_add("Nový Jičín", 74235,74265)
_add("Opava", 74705)
_add("Bruntál", 79326,79401)
# mimo CR
_add("Bratislava", 81104)

# --- fallback podle 3 cislic (pro nove PSC, ktere zatim v datech nejsou) ----
PREFIX_MAP = {
    "100":"Praha","101":"Praha","102":"Praha","103":"Praha","104":"Praha","106":"Praha",
    "107":"Praha","108":"Praha","109":"Praha","110":"Praha","111":"Praha","112":"Praha",
    "113":"Praha","114":"Praha","115":"Praha","116":"Praha","117":"Praha","118":"Praha",
    "119":"Praha","120":"Praha","121":"Praha","122":"Praha","124":"Praha","125":"Praha",
    "126":"Praha","127":"Praha","128":"Praha","129":"Praha","130":"Praha","131":"Praha",
    "132":"Praha","133":"Praha","135":"Praha","140":"Praha","141":"Praha","142":"Praha",
    "143":"Praha","144":"Praha","145":"Praha","146":"Praha","147":"Praha","148":"Praha",
    "149":"Praha","150":"Praha","151":"Praha","152":"Praha","153":"Praha","154":"Praha",
    "155":"Praha","156":"Praha","158":"Praha","159":"Praha","160":"Praha","161":"Praha",
    "162":"Praha","163":"Praha","164":"Praha","165":"Praha","166":"Praha","167":"Praha",
    "169":"Praha","170":"Praha","171":"Praha","172":"Praha","180":"Praha","181":"Praha",
    "182":"Praha","183":"Praha","184":"Praha","185":"Praha","186":"Praha","190":"Praha",
    "191":"Praha","192":"Praha","193":"Praha","194":"Praha","195":"Praha","196":"Praha",
    "197":"Praha","198":"Praha","199":"Praha",
    "250":"Praha-východ","251":"Praha-východ","252":"Praha-západ","253":"Praha-západ",
    "254":"Praha-západ","255":"Praha-západ","256":"Benešov","257":"Benešov","258":"Benešov",
    "259":"Benešov","261":"Příbram","262":"Příbram","263":"Příbram","264":"Příbram",
    "265":"Příbram","266":"Beroun","267":"Beroun","268":"Beroun","269":"Rakovník",
    "270":"Rakovník","271":"Rakovník","272":"Kladno","273":"Kladno","274":"Kladno",
    "275":"Kladno","276":"Mělník","277":"Mělník","278":"Mělník","279":"Mělník",
    "280":"Kolín","281":"Kolín","282":"Kolín","283":"Kolín","284":"Kutná Hora",
    "285":"Kutná Hora","286":"Kutná Hora","288":"Nymburk","289":"Nymburk","290":"Nymburk",
    "291":"Mladá Boleslav","292":"Mladá Boleslav","293":"Mladá Boleslav","294":"Mladá Boleslav",
    "295":"Mladá Boleslav",
    "301":"Plzeň-město","302":"Plzeň-město","304":"Plzeň-město","305":"Plzeň-město",
    "306":"Plzeň-město","310":"Plzeň-město","312":"Plzeň-město","314":"Plzeň-město",
    "316":"Plzeň-město","318":"Plzeň-město","320":"Plzeň-město","322":"Plzeň-město",
    "323":"Plzeň-město","326":"Plzeň-město","330":"Plzeň-sever","331":"Plzeň-sever",
    "332":"Plzeň-jih","333":"Plzeň-jih","334":"Plzeň-jih","335":"Plzeň-jih",
    "336":"Plzeň-jih","337":"Rokycany","338":"Rokycany","339":"Klatovy","340":"Klatovy",
    "341":"Klatovy","342":"Klatovy","344":"Domažlice","345":"Domažlice","346":"Domažlice",
    "347":"Tachov","348":"Tachov","349":"Tachov",
    "350":"Cheb","351":"Cheb","352":"Cheb","353":"Cheb","354":"Cheb","355":"Sokolov",
    "356":"Sokolov","357":"Sokolov","358":"Sokolov","360":"Karlovy Vary","362":"Karlovy Vary",
    "363":"Karlovy Vary","364":"Karlovy Vary",
    "370":"České Budějovice","371":"České Budějovice","373":"České Budějovice",
    "374":"České Budějovice","375":"České Budějovice","376":"České Budějovice",
    "377":"Jindřichův Hradec","378":"Jindřichův Hradec","379":"Jindřichův Hradec",
    "380":"Jindřichův Hradec","381":"Český Krumlov","382":"Český Krumlov",
    "383":"Prachatice","384":"Prachatice","385":"Prachatice","386":"Strakonice",
    "387":"Strakonice","388":"Strakonice","389":"Strakonice","390":"Tábor","391":"Tábor",
    "392":"Tábor","393":"Pelhřimov","394":"Pelhřimov","395":"Pelhřimov","396":"Pelhřimov",
    "397":"Písek","398":"Písek","399":"Písek",
    "400":"Ústí nad Labem","403":"Ústí nad Labem","404":"Děčín","405":"Děčín","406":"Děčín",
    "407":"Děčín","408":"Děčín","410":"Litoměřice","411":"Litoměřice","412":"Litoměřice",
    "413":"Litoměřice","415":"Teplice","417":"Teplice","418":"Teplice","419":"Teplice",
    "430":"Chomutov","431":"Chomutov","432":"Chomutov","434":"Most","435":"Most",
    "436":"Most","437":"Most","438":"Louny","439":"Louny","440":"Louny","441":"Louny",
    "460":"Liberec","463":"Liberec","464":"Liberec","466":"Jablonec nad Nisou",
    "468":"Jablonec nad Nisou","470":"Česká Lípa","471":"Česká Lípa","472":"Česká Lípa",
    "473":"Česká Lípa","500":"Hradec Králové","501":"Hradec Králové","502":"Hradec Králové",
    "503":"Hradec Králové","504":"Hradec Králové","505":"Hradec Králové","506":"Jičín",
    "507":"Jičín","508":"Jičín","509":"Jičín","511":"Semily","512":"Semily","513":"Semily",
    "514":"Semily","516":"Rychnov nad Kněžnou","517":"Rychnov nad Kněžnou",
    "518":"Rychnov nad Kněžnou","530":"Pardubice","531":"Pardubice","532":"Pardubice",
    "533":"Pardubice","534":"Pardubice","535":"Pardubice","537":"Chrudim","538":"Chrudim",
    "539":"Chrudim","540":"Trutnov","541":"Trutnov","542":"Trutnov","543":"Trutnov",
    "544":"Trutnov","547":"Náchod","548":"Náchod","549":"Náchod","550":"Náchod",
    "551":"Náchod","552":"Náchod","560":"Ústí nad Orlicí","561":"Ústí nad Orlicí",
    "562":"Ústí nad Orlicí","563":"Ústí nad Orlicí","564":"Ústí nad Orlicí",
    "565":"Ústí nad Orlicí","566":"Ústí nad Orlicí","567":"Ústí nad Orlicí",
    "568":"Svitavy","569":"Svitavy","570":"Svitavy","571":"Svitavy","572":"Svitavy",
    "580":"Havlíčkův Brod","582":"Havlíčkův Brod","583":"Havlíčkův Brod",
    "584":"Havlíčkův Brod","585":"Havlíčkův Brod","586":"Jihlava","588":"Jihlava",
    "589":"Jihlava","591":"Žďár nad Sázavou","592":"Žďár nad Sázavou",
    "593":"Žďár nad Sázavou","594":"Žďár nad Sázavou","595":"Žďár nad Sázavou",
    "600":"Brno-město","602":"Brno-město","603":"Brno-město","604":"Brno-město",
    "612":"Brno-město","613":"Brno-město","614":"Brno-město","615":"Brno-město",
    "616":"Brno-město","617":"Brno-město","618":"Brno-město","619":"Brno-město",
    "620":"Brno-město","621":"Brno-město","623":"Brno-město","624":"Brno-město",
    "625":"Brno-město","627":"Brno-město","628":"Brno-město","634":"Brno-město",
    "635":"Brno-město","636":"Brno-město","637":"Brno-město","638":"Brno-město",
    "639":"Brno-město","641":"Brno-město","643":"Brno-město","644":"Brno-město",
    "648":"Brno-město","656":"Brno-město","657":"Brno-město","658":"Brno-město",
    "659":"Brno-město","664":"Brno-venkov","665":"Brno-venkov","666":"Brno-venkov",
    "667":"Brno-venkov","669":"Znojmo","671":"Znojmo","672":"Znojmo","674":"Třebíč",
    "675":"Třebíč","676":"Třebíč","677":"Třebíč","678":"Blansko","679":"Blansko",
    "680":"Blansko","682":"Vyškov","683":"Vyškov","684":"Vyškov","685":"Vyškov",
    "686":"Uherské Hradiště","687":"Uherské Hradiště","688":"Uherské Hradiště",
    "689":"Uherské Hradiště","690":"Břeclav","691":"Břeclav","692":"Břeclav",
    "693":"Břeclav","695":"Hodonín","696":"Hodonín","697":"Hodonín","698":"Hodonín",
    "700":"Ostrava-město","702":"Ostrava-město","703":"Ostrava-město","704":"Ostrava-město",
    "708":"Ostrava-město","709":"Ostrava-město","710":"Ostrava-město","711":"Ostrava-město",
    "712":"Ostrava-město","713":"Ostrava-město","715":"Ostrava-město","716":"Ostrava-město",
    "717":"Ostrava-město","718":"Ostrava-město","719":"Ostrava-město","720":"Ostrava-město",
    "721":"Ostrava-město","722":"Ostrava-město","723":"Ostrava-město","724":"Ostrava-město",
    "725":"Ostrava-město","730":"Karviná","733":"Karviná","734":"Karviná","735":"Karviná",
    "736":"Karviná","737":"Karviná","738":"Frýdek-Místek","739":"Frýdek-Místek",
    "742":"Nový Jičín","743":"Nový Jičín","744":"Nový Jičín","745":"Nový Jičín",
    "746":"Opava","747":"Opava","748":"Opava","749":"Opava","750":"Přerov","751":"Přerov",
    "752":"Přerov","753":"Přerov","756":"Vsetín","757":"Vsetín","758":"Vsetín",
    "760":"Zlín","763":"Zlín","765":"Zlín","766":"Zlín","767":"Kroměříž","768":"Kroměříž",
    "769":"Kroměříž","770":"Olomouc","772":"Olomouc","779":"Olomouc","783":"Olomouc",
    "784":"Olomouc","785":"Olomouc","787":"Šumperk","788":"Šumperk","789":"Šumperk",
    "790":"Jeseník","792":"Bruntál","793":"Bruntál","794":"Bruntál","795":"Bruntál",
    "796":"Prostějov","797":"Prostějov","798":"Prostějov","799":"Prostějov",
}


def psc_to_okres(psc):
    """Vrati (okres, kraj). Neznama PSC -> ('Neznámý', 'Neznámý')."""
    if not psc:
        return ("Neznámý", "Neznámý")
    p = str(psc).replace(" ", "").strip()
    if len(p) != 5 or not p.isdigit():
        return ("Neznámý", "Neznámý")
    okres = PSC_MAP.get(p) or PREFIX_MAP.get(p[:3])
    if not okres:
        return ("Neznámý", "Neznámý")
    return (okres, OKRES_KRAJ.get(okres, "Neznámý"))
