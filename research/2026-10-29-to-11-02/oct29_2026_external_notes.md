# 2026-10-29 本周（10/29–11/02）外部核验记录

核验时间：2026-10-28 22:56–23:05 CET（北京时间10月29日05:56–06:05）。欧洲已是冬令时（CET = UTC+1），北京时间 = 当地时间 + 7小时。

## 模型与赔率
- 模型：forecast_oct29_nov02_2026_asof1029.py，AS_OF 2026-10-29。Understat完成场次截至：英超/德甲10/25，西甲10/26，法甲10/25，意甲10/28。本轮新增完成比赛：E0 70、D1 63、I1 77、SP1 89、F1 64。共50场。
- 赔率：ESPN/DraftKings记分板接口 site.api.espn.com/apis/site/v2/sports/soccer/{eng.1,esp.1,ger.1,ita.1,fra.1}/scoreboard?dates=20261029…20261103。50场全部匹配，49场有价；Frankfurt–Hamburg未开盘。没有恰好主让−1.25的盘口。
- ClubElo Fixtures API 返回 “Fixtures API deactivated”。ClubElo网页 https://clubelo.com/Fixtures 的页面生成时间为2026-10-24，已过期，不能用作本周非五大联赛的独立概率来源。
- 非五大联赛（ESPN同一接口）：荷甲9场、葡超9场、英冠12场、比甲7场、土超7场有价，苏超4场无价。这些联赛没有冻结验证模型，只作记录。

## 上周（10/23–10/28）赛果（ESPN终场）
英超：Ipswich 1–1 Forest、Villa 2–1 Man City、Arsenal 2–0 Everton、Coventry 0–1 Fulham、Chelsea 0–2 Tottenham、Palace 0–2 Newcastle、Hull 1–1 Brentford、Liverpool 2–0 Brighton、Man United 0–3 Bournemouth、Sunderland 0–0 Leeds。
西甲：Alavés 1–1 Málaga、Rayo 0–3 Elche、Racing 2–1 Espanyol、Valencia 1–2 Villarreal、Atlético 1–0 Deportivo、Athletic 4–0 Getafe、Celta 0–0 Betis、Real Sociedad 2–1 Levante、Barcelona 1–2 Real Madrid、Sevilla 2–0 Osasuna。
法甲：Brest 1–2 Nice、Lens 2–1 Paris FC、Monaco 1–1 Lille、Auxerre 1–1 Le Mans、Angers 0–0 Lorient、Marseille 4–3 Le Havre、Rennes 3–0 Strasbourg、Toulouse 0–0 Troyes、PSG 2–0 Lyon。
德甲：Stuttgart 2–3 Gladbach、Augsburg 1–1 Union、Köln 0–0 Schalke、Mainz 2–3 Werder、Leipzig 4–0 Elversberg、Paderborn 1–0 Hamburg、Dortmund 1–0 Frankfurt、Freiburg 1–3 Bayern。
意甲：Torino 3–2 Monza、Cagliari 0–2 Bologna、Como 2–0 Sassuolo、Napoli 3–3 Roma、Lazio 2–1 Parma、Inter 2–1 Fiorentina、Atalanta 4–4 Frosinone、Genoa 1–0 Venezia、Lecce 0–2 Juventus、Udinese 0–2 Milan、Sassuolo 2–6 Lazio、Roma 4–2 Cagliari、Torino 1–3 Como、Milan 2–4 Bologna、Parma 0–0 Udinese、Venezia 0–2 Inter、Genoa 2–0 Juventus、Monza 1–4 Napoli。
来源：https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard?dates=20261024（同一接口，五个联赛，10/23–10/28）。

## 平局检验基线（来自10/14报告）
冻结贝叶斯历史预测 + 真实收盘平局赔率，2022年起8,053场：
- 贝叶斯平局EV≥0、不限赔率：开发期1,437笔，ROI +1.34%；留出期787笔，ROI −8.68%。
- EV≥0且赔率3.0–3.6：开发期104笔，ROI +16.25%；留出期18笔，ROI +55.6%。属于事后挑选，只能作为观察假设。
- 全部押平：全样本ROI −4.45%。
文件：output/draw_signal_quickcheck_2022_2026.csv
