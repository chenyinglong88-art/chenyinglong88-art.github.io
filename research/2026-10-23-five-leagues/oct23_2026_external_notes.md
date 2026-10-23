# 2026-10-23 五大联赛本周（10/23–10/29）外部核验记录

核验时间：2026-10-23 06:47–07:05 CEST（北京时间12:47–13:05）。注意：10月25日欧洲结束夏令时，25日起西甲/意甲本地时间为CET（UTC+1），北京时间=本地+7小时；24日及以前为CEST（UTC+2），北京时间=本地+6小时。

## 模型与赔率
- 模型：forecast_oct23_oct29_2026_asof1023.py，AS_OF 2026-10-23，Understat完成场次截至10/19（新增E0 60、D1 54、I1 61、SP1 78、F1 55场），58场。
- 赔率：ESPN/DraftKings 赛程接口 site.api.espn.com/apis/site/v2/sports/soccer/{eng.1,esp.1,ger.1,ita.1,fra.1}/scoreboard?dates=20261023…20261029，58场全部匹配，56场有价（Paderborn–Hamburg、Venezia–Inter未开盘）。无恰好主让−1.25盘口。

## 五场条件观察候选的逐场核验（workflow 5f3b681dda3f）
1. Como vs Sassuolo（意甲，10/24 15:00 CEST，北京21:00）
   - 价格：DK 1.50（开盘1.40）、bet365 1.50、BetMGM 1.526、Fanatics 1.476、BetRivers 1.444、FanDuel 1.455。https://www.oddschecker.com/us/soccer/serie-a/como-v-sassuolo ；https://sportsbook.fanduel.com/soccer/italian-serie-a/sassuolo-como-36209510
   - 伤停：Como缺Chalobah、Jesús Rodríguez、Diao，Liberali小腿、Kean存疑；Sassuolo缺Koné、Idzes、Boloca、Leysen（十字韧带）。https://www.sportsmole.co.uk/football/como/preview/como-vs-sassuolo-prediction-team-news-lineups_607472.html
   - 近况：Como 10/21欧冠4–1胜曼联、10/18客3–1 Fiorentina、10/14欧冠2–3负Feyenoord、0–0 Roma、0–2 Frosinone；第5名14分。Sassuolo 2–4 Frosinone、1–1 Milan、1–2 Monza、3–2 Juventus、2–2 Bologna；第13名8分。https://www.espn.com/soccer/match/_/gameId/401874961
   - 关键风险：Como周三欧冠后仅休3天，可能轮换；Berardi是Sassuolo主要威胁。
2. Rayo Vallecano vs Elche（西甲，10/24 14:00 CEST，北京20:00）
   - 价格：DK 1.769（开盘1.741）、BetMGM 1.769、Bovada 1.78。https://tips.gg/matches/football/24-10-2026/rayo-vallecano-vs-elche/08-00/odds/ ；https://oddspedia.com/football/elche-rayo-vallecano-75331
   - 伤停：Rayo缺Luiz Felipe（十字韧带）、Batalla（腿骨折），Ratiu、Nteka存疑，Pathé Ciss停赛说法冲突；Elche缺Aguado。https://www.sportsmole.co.uk/football/rayo-vallecano/preview/rayo-vallecano-vs-elche-prediction-team-news-lineups_607489.html
   - 近况：Rayo 1–1 Getafe、1–1 Osasuna、2–1 Espanyol、1–4 Real Madrid、3–2 Racing；第14名9分。Elche 0–0 Villarreal、0–0 Celta、3–1 Espanyol、2–3 Real Madrid、1–1 Athletic；第18名7分。两队本周无欧战/杯赛。https://www.laliga.com/en-GB/laliga-easports/standing
3. Athletic Club vs Getafe（西甲，10/25 14:00 CET，北京21:00）
   - 价格：DK 1.606（当前−165；接口快照1.588，开盘1.625）、FanDuel 1.588。https://www.espn.com/soccer/odds/_/gameId/401882835
   - 伤停：Athletic缺Guruzeta（十字韧带）、Sancet（小腿）、Djaló（病）、Egiluz（十字韧带）；Getafe缺Zaid Romero、Mangala、Uche（十字韧带）、Juanmi，Ünal在欧协联脚踝受伤存疑。https://www.nytimes.com/athletic/football/game/athletic-club-vs-getafe/cANYlA1NB3JdIHaZ/ ；https://www.foxsports.com/soccer/la-liga-athletic-vs-getafe-oct-25-2026-game-boxscore-909042
   - 近况：Athletic 10/21客1–3负Levante、0–0 Valencia、0–0 Alavés、1–1 Elche、3–0 Atlético（近5场1胜，联赛4场不胜）；第13名9分。Getafe 10/22欧协联2–5负Lugano、1–1 Rayo、1–1 Craiova、0–3 Barcelona、1–0 Málaga；第15名9分。
4. Barcelona vs Real Madrid（西甲，10/25 21:00 CET，北京26日04:00）
   - 价格：DK 1.645（开盘1.526）、1xBet 1.65、bet365 1.613–1.62、Betway 1.62、BetMGM 1.625、FanDuel 1.588、Betsson 1.55。https://www.sportytrader.com/en/odds/barcelona-real-madrid-8586507/ ；https://www.oddschecker.com/us/soccer/la-liga-primera/barcelona-v-real-madrid
   - 伤停：巴萨缺Olmo、Bardghji、Christensen、Eric García，Koundé重大存疑；皇马缺Rodrygo、Mendy、Asencio，Vinícius国内四场禁赛。https://www.sportsmole.co.uk/football/barcelona/injury-news/injuries-and-suspensions/olmo-kounde-garcia-updates-barcelona-injury-suspension-list-vs-real-madrid_607443.html ；https://www.sportsmole.co.uk/football/barcelona/el-clasico/injuries-and-suspensions/rodrygo-mendy-updates-real-madrid-injury-suspension-news-vs-barcelona_607438.html
   - 近况：巴萨10/20欧冠2–4负PSG，此前4连胜，联赛9战全胜第1（27分）；皇马10/21欧冠4–1胜Leipzig，4连胜，第3（21分）。官方开球：https://www.realmadrid.com/en-US/news/football/first-team/latest-news/el-barcelona-real-madrid-se-jugara-el-domingo-25-de-octubre-a-las-21-00-h-01-09-2026
5. Real Sociedad vs Levante（西甲，10/25 18:30 CET = 17:30 UTC，北京26日01:30）
   - 价格：DK 1.667（开盘1.714）、FanDuel 1.588。https://sportsbook.fanduel.com/soccer/spanish-la-liga/real-sociedad-v-levante-36180861
   - 伤停：Sociedad缺Odriozola、Aramburu、Beitia、Yangel Herrera；Levante De La Fuente、Bardeli存疑。https://www.fotmob.com/matches/real-sociedad-vs-levante/2fh3cs
   - 近况：Sociedad 10/22客场欧联6–0 Lillestrøm、5–2 Málaga、1–1 Union SG、3–2 Deportivo、3–2 Valencia；第5（16分）。Levante 3–1 Athletic、1–1 Deportivo、3–3 Sevilla、1–3 Villarreal、2–4 Barcelona；第11（10分）。关键风险：Sociedad挪威客场后约72小时再战。

## 10月22日欧联/欧协联观察榜赛果（ESPN终场，未下注）
第1 Olympiacos 1–0 Sparta（命中）；第2 Midtjylland 0–1 Sint-Truiden（未中）；第3 Pafos 1–1 Riga（未中）；第4 Plzeň 1–2 Levski（未中）；第5 Celje 2–2 Salzburg（客胜未中）；第6 Braga 2–0 Gent（“不追”的表面高EV反而命中）；第7 Getafe 2–5 Lugano（未中）；第8 Bournemouth 3–0 Milan（命中）。前8名3中5不中；前3名1中。低于1.50被排除方向：Brighton 0–0（未中）、Leverkusen 2–0、Twente 4–1、Trabzonspor 2–0、Ferencváros 4–1、AZ 4–0、Union SG 4–0、Real Sociedad 6–0、Benfica 4–1。来源：https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.europa/scoreboard?dates=20261022 及 uefa.europa.conf 同参数。
