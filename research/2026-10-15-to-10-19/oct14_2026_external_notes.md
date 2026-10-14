# 2026-10-14 本周外部核验记录（GMT+2 22:11–22:23）

## 上周观察赛果（ESPN终场 + Understat xG）
- Man United 1–1 Tottenham（10/10，ESPN 401878773；xG 0.87–2.03）→ 观察第1名曼联主胜未中
- RB Leipzig 6–0 Eintracht Frankfurt（10/10，ESPN 401884780；xG 4.74–1.96）→ 观察第2名莱比锡主胜命中
- 被拒高EV：Lens 2–1 Lyon（主胜）；Levante 3–3 Sevilla（平）；Alavés 1–2 Atlético（客胜）；Brest 5–1 Angers（主胜）；Köln 2–1 Gladbach（主胜）
- 平局巡检：PSG 3–1 Le Mans；Augsburg 2–2 Bayern（平）；Real Madrid 1–0 Villarreal；Monaco 2–2 Toulouse（平）；Lille 1–0 Le Havre；Napoli 3–0 Frosinone
- 真实下注0笔，账户10,836.26元不变。

## 本周模型与赔率
- 模型：forecast_oct15_oct20_2026_asof1014.py，AS_OF 2026-10-14，48场（10/16–10/19）；Understat新增完赛 E0 50, D1 45, I1 51, SP1 68, F1 46（累计计数）。
- ESPN/DraftKings接口 48/48匹配，47场有价（Hamburg vs Stuttgart无价）。URL模式 https://site.api.espn.com/apis/site/v2/sports/soccer/{eng.1|esp.1|ger.1|ita.1|fra.1}/scoreboard?dates=202610DD
- 无主让−1.25盘口（-0.5×22, +0.5×17, -1.5×5, +1.5×2, -2.5×1）。

## 候选1：Osasuna vs Racing Santander（西甲，10/18 14:00 GMT+2，El Sadar）
- DraftKings 1.952/3.60/3.65（ESPN 401882840）
- Oddschecker（最后更新 2026-10-14 20:17 英国）：主胜多数19/20–1/1（1.95–2.00），最低20/23（1.87）；交易所21/20（2.05）；oddschecker+ AI概率 Osasuna 44%/平27%/Racing 29%
  https://www.oddschecker.com/football/spain/la-liga-primera/osasuna-v-racing-santander/winner
- TheStatsZone（2026-10-14）：Osasuna近5场仅1分、失17球，上轮5–2负Betis；新帅Luis Miguel Ramis；缺Herrando、Bonel、Del Castillo、Raúl Moro；Oroz、Raúl García、Kike Barja存疑。Racing升班马，8轮36球，上轮2–2 Valencia；Prati、Eriksson存疑。
  https://www.thestatszone.com/osasuna-vs-racing-santander-preview-team-news-prediction-230535
- FotMob：Osasuna缺Herrando（存疑）、Oroz、Barja、Moro、Del Castillo（至10月下旬）；Racing缺Prati、Eriksson。Osasuna近5：负Betis 2–5、平Rayo 1–1、负Atlético 0–4、负Espanyol 0–2、负Alavés 2–5。Racing近5：平Valencia 2–2、负Celta 0–5、负Barça 2–7、胜Alavés 2–1、负Rayo 2–3。H2H 4胜4负。
  https://www.fotmob.com/matches/osasuna-vs-racing-santander/2epysq
- Forebet摘要：两队同为8分。

## 候选2：Bournemouth vs Sunderland（英超，10/18 15:00 GMT+2，Vitality）
- DraftKings 2.00/3.55/3.55（ESPN 401879263）
- Oddschecker（最后更新 2026-10-14 20:17 英国）：主胜多数1/1–21/20（2.00–2.05），最高11/10（2.10）；交易所10/9；AI概率 Bournemouth 45%/平26%/Sunderland 29%
  https://www.oddschecker.com/football/english/premier-league/bournemouth-v-sunderland/winner
- Squawka（2026-10-14）：Bournemouth缺6人：Alex Scott（大腿）、Eli Kroupi（脚踝）、Julian Araujo（大腿）、Amine Adli（小腿）、Veljko Milosavljevic（膝）、Justin Kluivert；Sunderland缺Brobbey（头号射手3球，大腿）、Mundle（膝）、Ballard（大腿），Meunier、Habib Diarra存疑。积分：Sunderland第17（6场4分，1胜1平4负，6–12）、Bournemouth第18（6场3分，0胜3平3负，7–13）。Bournemouth近况：1–5负Chelsea、0–1负Liverpool、2–2 Brentford、2–2 Newcastle、1–1 Everton。Sunderland：0–2 Brighton、3–5 Man City、0–2 Arsenal、1–1 Brentford、1–0 Fulham。Squawka模型 Bournemouth 47%（市场48%）。
  https://www.squawka.com/us/news/premier-league/match-preview-bournemouth-vs-sunderland-18-10-26-premier-league/

## 欧战10/15（仅市场观察）
- 欧联18场、欧协联18场已开盘：Lyon–Crystal Palace 2.20/3.75/3.05；Salzburg–Milan 3.35/3.75/2.05；Celta–Juventus 3.50/3.40/2.15；Hoffenheim–Besiktas 2.00/4.10/3.35；Marseille–Olympiacos 2.30/3.55/3.00；Atalanta–Pafos 1.364；Freiburg–Jablonec 1.286；Bournemouth–Sturm 1.190；Rennes–OFI 1.25。

## 平局快速检验（output/draw_signal_quickcheck_2022_2026.csv）
- 数据：dynamic_bayes_frozen_predictions.csv.gz，2022-01起8,053场，真实收盘平局均价AvgCD；全部押平ROI −4.45%，平局基础率25.16%。
- 贝叶斯平局EV≥0、无赔率限制：开发期1,437笔ROI +1.34%；留出期787笔ROI −8.68%（失败）。
- EV≥0且平局赔率3.0–3.6：开发期104笔ROI +16.25%；留出期18笔ROI +55.6%（样本过小）；全样本122笔命中35.25%、ROI +22.05%。按年：2022 n56 +16.5%；2023 n37 +12.5%；2024 n14 +50.9%；2025 n12 +45.0%；2026 n3 +17.3%。
- 本周该观察带（3.0–3.6）所有平局贝叶斯EV均为负（最高Celta–Alavés −6.7%）→ 无平局观察信号。
