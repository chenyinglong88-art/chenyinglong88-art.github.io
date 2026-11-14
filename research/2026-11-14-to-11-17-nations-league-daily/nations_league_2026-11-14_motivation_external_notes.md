# 欧国联战意分析外部记录（2026-11-14 13:30–13:47 CET）

## 数据源
- ESPN scoreboard API（DraftKings 1X2，12:30 UTC抓取）：https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.nations/scoreboard?dates=20261112 …20261117；本地 xg_data/raw/espn_nations_nov2026_asof1114/；快照 output/nations_league_2026-11-14_scoreboard_snapshot.csv
- ESPN standings API：https://site.api.espn.com/apis/v2/sports/soccer/uefa.nations/standings
- Elo（eloratings.net经international-football.net）2026-11-14：https://www.international-football.net/elo-ratings-table?year=2026&month=11&day=14&confed=UEFA&old-team= ；关键值 Germany 1895, Netherlands 1974, Greece 1804, Serbia 1683, Switzerland 1972, Scotland 1746, Slovenia 1690, North Macedonia 1536, Croatia 1861, Czechia 1658, Portugal 2055, Wales 1681, Bosnia 1672, Romania 1554
- UEFA规则（2026-11-12）：https://www.uefa.com/uefanationsleague/news/0298-1d6ef1acfaef-b54fcf1da859-1000--2026-27-uefa-nations-league-all-you-need-to-know/
  A：前2进八强；两个最好第3留A；两个较差第3+两个最好第4打A/B附加赛；两个最差第4降B。B：第1升A；第2打A/B附加赛；第3留B；第4打B/C附加赛。C：第1升B；第2打B/C附加赛；第3、4留C。D全部升C。抽签2026-11-20 12:00 CET；附加赛/八强2027-03-25–30。
- AS（2026-11-11）：https://en.as.com/soccer/how-the-uefa-nations-league-could-shape-euro-2028-qualification-and-seeding-f202611-n/ ——欧洲杯2028预选赛分档按本届欧国联联赛阶段排名；Pot1=A组1–3名，Pot2=A组第4+B组1–2名，Pot3=B组3–4名…；欧国联成绩较好的小组第一可获附加赛名额。
- Feddersen, Humphreys & Soebbing (2023), European Sport Management Quarterly 23(3):605–621, https://doi.org/10.1080/16184742.2021.1898432 ——约2.5万场欧洲8大联赛：博彩公司会针对无欲无求的中游球队、已降级球队、已夺冠球队调整收盘赔率（即市场已部分定价战意）。

## 第5轮已完赛比分（ESPN）
11-12：Armenia 1-1 Cyprus；Türkiye 1-2 Belgium；Albania 2-0 Finland；Czechia 0-2 Spain；England 2-1 Croatia；Italy 3-1 France；Montenegro 2-1 Latvia；San Marino 0-2 Belarus。
11-13：Moldova 2-1 Kazakhstan；Slovenia 0-0 Switzerland；Slovakia 2-2 Faroe Islands；Serbia 1-3 Germany；Scotland 2-1 North Macedonia；Liechtenstein 0-1 Azerbaijan；Luxembourg 0-1 Estonia；Bulgaria 0-5 Iceland；Andorra 2-0 Gibraltar；Netherlands 7-0 Greece。

## 11-14 13:30时剩余赛程DK价（主/平/客）
11-14：Kosovo–Israel 1.833/3.50/4.00；Georgia–Hungary 3.10/3.00/2.35；Norway–Wales 1.25/6.00/9.00；Romania–Poland 4.60/3.85/1.667；Portugal–Denmark 1.588/4.20/4.80；Sweden–Bosnia 1.444/4.20/6.50；Austria–Ireland 1.645/3.70/4.90；N.Ireland–Ukraine 2.50/2.80/3.05。
11-15：Cyprus–Montenegro 3.15/3.30/2.20；Latvia–Armenia 2.95/3.15/2.35；Belarus–Albania 未开；Finland–San Marino 1.012/14/46；Belgium–Italy 2.15/3.60/3.00；Croatia–Czechia 1.571/4.10/5.00；France–Türkiye 1.222/6.00/10.0；Spain–England 1.714/3.95/4.10。
11-16：Faroe–Moldova 1.80/3.35/4.40；Kazakhstan–Slovakia 4.80/3.75/1.645；Iceland–Luxembourg 1.312/5.00/8.50；Estonia–Bulgaria 2.20/3.00/3.40；Germany–Netherlands 1.833/4.00/3.50；Gibraltar–Malta 7.00/4.00/1.435；Greece–Serbia 1.435/4.50/6.00；North Macedonia–Slovenia 5.75/3.65/1.571；Switzerland–Scotland 1.667/3.65/5.00。
11-17：全部未开盘（Ukraine–Georgia, Bosnia–Romania, Denmark–Norway, Hungary–N.Ireland, Israel–Austria, Poland–Sweden, Ireland–Kosovo, Wales–Portugal）。

## 第5轮后积分（ESPN）
A1 Italy10 France10 Belgium9 Türkiye0；A2 Netherlands11 Greece8 Germany8 Serbia0；A3 Spain15 England12 Croatia3 Czechia0；A4(4赛) Portugal12 Denmark6 Norway3 Wales3；B1 Switzerland13 Slovenia8 Scotland7 NMacedonia0；B2(4赛) NIreland8 Hungary7 Ukraine4 Georgia2；B3(4赛) Austria8 Kosovo5 Ireland5 Israel2；B4(4赛) Sweden10 Bosnia8 Poland4 Romania0；C1 Albania12 Belarus10 Finland7 SanMarino0；C2 Montenegro13 Hungary? (C2: Montenegro13 Cyprus? see CSV) ；C3 Slovakia11 Moldova7 Faroe5 Kazakhstan2；C4 Iceland11 Estonia9 Bulgaria4 Luxembourg3；D1 Malta7 Andorra4 Gibraltar2；D2 Azerbaijan8 Lithuania4 Liechtenstein1。
A2交锋：NED 1-1 GER；GRE 0-0 GER（主希腊）；GER 0-1 GRE（主德国）；GRE 2-2 NED；NED 7-0 GRE。B1交锋：SVN 0-0 SCO；SVN 0-0 SUI。

## 14:14–14:16 CET refresh for 14–17 Nov (user asked "today and next few days")
- ESPN scoreboard API re-fetched 14:14 CET (raw: xg_data/raw/espn_nations_nov2026_asof1114_1415/). All 34 remaining fixtures still SCHEDULED; 26 have DraftKings 1X2. Changes vs 13:30: Kosovo–Israel 1.741/3.60/4.30 (was 1.833/3.50/4.00); Romania–Poland 4.60/3.95/1.645; Finland–San Marino 1.025/14/31; Kazakhstan–Slovakia 4.70/3.70/1.667; Estonia–Bulgaria 2.10/3.05/3.65 (was 2.20/3.00/3.40); Iceland–Luxembourg 1.303/5.00/8.50; Lithuania–Liechtenstein now 1.083/9.00/21.00. 17 Nov fixtures: no DraftKings line yet. https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.nations/scoreboard?dates=20261114
- Five big leagues (eng.1/esp.1/ger.1/ita.1/fra.1) and UCL: 0 events 14–18 Nov (international break). fifa.friendly: only non-European friendlies plus Azerbaijan at Andorra 16 Nov 19:00.
- Oddschecker 17 Nov win market (fractional lists, sportsbooks), fetched 14:15 CET:
  - Bosnia and Herzegovina v Romania (page last updated Sat 14 Nov 01:06): best 8/11 / 13/5 / 15/4; home list 8/11 7/10 8/11 7/10 8/11 7/10 4/6 8/11 8/11 8/11 7/10 8/11 8/11 5/7 4/6 7/10. https://www.oddschecker.com/football/uefa-nations-league/bosnia-and-herzegovina-v-romania/winner
  - Denmark v Norway (updated 14 Nov 01:07): best Denmark 17/10, Draw 14/5, Norway 31/20. https://www.oddschecker.com/football/uefa-nations-league/denmark-v-norway/winner
  - Poland v Sweden (updated 14 Nov 01:07): best Poland 27/20, Draw 13/5, Sweden 194/100. https://www.oddschecker.com/football/uefa-nations-league/poland-v-sweden/winner
  - Hungary v Northern Ireland (updated 13 Nov 05:19 — stale): best 7/8 / 12/5 / 7/2. https://www.oddschecker.com/football/uefa-nations-league/hungary-v-northern-ireland/winner
  - Wales v Portugal: only goalscorer markets shown, no 1X2 (updated 13 Nov 05:19). https://www.oddschecker.com/football/uefa-nations-league/wales-v-portugal/winner
- Not yet priced anywhere checked: Israel–Austria, Ireland–Kosovo, Ukraine–Georgia, Wales–Portugal (1X2), Belarus–Albania (15 Nov).
