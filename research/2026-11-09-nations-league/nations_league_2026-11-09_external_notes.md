# 2026-11-09 欧国联第5–6轮 外部核验记录

审计时间：2026-11-09 23:21–23:28 CET（北京时间 11-10 06:21–06:28）。

## 赛程（UEFA官方，CET）
来源：https://www.uefa.com/uefanationsleague/news/02a2-1fea18abbcbc-456e846509e7-1000--2026-27-uefa-nations-league-all-the-league-phase-fixtures/
- 第5轮 11-12（周四）至 11-14；第6轮 11-15 至 11-17（联赛阶段 11-17 结束）。
- UEFA页面把第5轮周五 11-13 的比赛漏写在"Friday 13 November"标题下为空；ESPN显示 11-13 有 10 场（Moldova–Kazakhstan 18:00；Andorra–Gibraltar、Bulgaria–Iceland、Liechtenstein–Azerbaijan、Luxembourg–Estonia、Netherlands–Greece、Scotland–North Macedonia、Serbia–Germany、Slovakia–Faroe、Slovenia–Switzerland 均 20:45）。
- 注意：UEFA页把第1–4轮部分比赛日期写错；本次以ESPN接口的比赛日期为准。

## 赔率（DraftKings，经ESPN scoreboard API，美式→十进制）
来源：https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.nations/scoreboard?dates=20261112 （…13、14、15、16、17 同格式）；原始JSON存于 xg_data/raw/espn_nations_nov2026_asof1109/
- 52场中有25场开出完整1X2（11-12至11-14 第5轮场次），第6轮（11-15起）和 San Marino–Belarus 未开盘。
- 底表：output/nations_league_2026-11-12_to_11-17_lines_asof1109.csv

## Elo（eloratings.net，经 international-football.net，2026-11-09）
来源：https://www.international-football.net/elo-ratings-table?year=2026&month=11&day=09&confed=UEFA&old-team=
- Spain 2282、England 2144、France 2104、Portugal 2055、Netherlands 1974、Switzerland 1972、Belgium 1956、Italy 1910、Norway 1900、Germany 1895、Croatia/Denmark 1861、Austria 1841、Greece 1804、Sweden 1774、Turkey 1768、Scotland 1746、Hungary 1725、Ukraine 1724、Ireland 1711、Kosovo 1710、Slovenia 1690、Poland 1685、Serbia 1683、Wales 1681、Bosnia/N.Ireland 1672、Slovakia 1665、Czechia 1658、Georgia 1628、Israel 1619、Albania 1612、Iceland 1603、Romania 1554、Finland 1552、N.Macedonia 1536、Belarus 1515、Montenegro 1490、Luxembourg 1422、Bulgaria 1411、Estonia 1400、Kazakhstan 1393、Faroe 1392、Armenia 1354、Cyprus 1346、Azerbaijan 1326、Moldova 1301、Lithuania 1278、Malta 1263、Latvia 1246、Andorra 1056、Gibraltar 1036、Liechtenstein 887、San Marino 820。

## 前四轮赛果与积分榜（ESPN）
来源：ESPN scoreboard API 2026-09-24…10-06（104场全部 STATUS_FULL_TIME）；standings API https://site.api.espn.com/apis/v2/sports/soccer/uefa.nations/standings
- 底表：output/nations_league_2026-09-24_to_10-06_all_results_espn.csv、output/nations_league_2026-11-09_standings_espn.csv
- 10-06 最后一个比赛日：Croatia 1-2 Spain；England 3-0 Czechia；Scotland 1-2 Slovenia；Switzerland 3-0 N.Macedonia；Albania 2-1 San Marino；Belarus 1-0 Finland；Estonia 0-0 Iceland；Luxembourg 0-2 Bulgaria；Moldova 0-4 Slovakia；Kazakhstan 2-2 Faroe。
- 上轮（9/29–10/2）观察项：6项4中2失，累计观察8胜6负，真实下注0（见 output/oct06_2026_external_notes.md）。10-06当天比赛已到开球时点，未做推荐。

## 小样本检验：9月截图完整1X2 vs 赛果（42场，40场有完整价）
- 热门≤1.50：11场9胜，平注ROI +8.1%；1.50–2.00：11场7胜，ROI +7.1%；>2.00：18场8胜，ROI +2.8%。
- 平局3.0–3.6：18场5平，ROI −11.1%。全部40场9平。
- 文件：output/nations_league_sep24_sep28_2026_screenshot_odds_vs_results.csv。样本极小，不能作为策略证据。

## 前八候选逐场核验（23:26–23:33 CET，子任务）
| 方向 | 可见最高价/来源 | 其他价 | 选择方缺阵 | 对手缺阵 | 关键背景 |
|---|---|---|---|---|---|
| 瑞士客胜 | 1.70 22bet/Shangrila（https://www.wincomparator.com/predictions/slovenia-switzerland-8318388/） | bet365 1.62–1.65、Sky Bet 1.53、FanDuel 1.571 | 扎卡（小腿）、巴尔加斯、穆海姆 | 谢什科、埃尔什尼克伤；扬扎、泽茨停赛 | 瑞士平局即直接升A（SRF）；比赛移至马里博尔 |
| 奥地利主胜 | 1.62 Shangrila（https://www.sportytrader.com/en/odds/austria-ireland-8318364/） | YesPlay 1.57、bet365 1.54、Sky Bet 1.44 | 阿拉巴、萨比策、维默、沃伯、万纳、格里利奇、楚克武埃梅卡、格吕尔 | 卡伦、弗格森、巴祖努 | 奥地利主场胜即升A（ORF） |
| 瑞典主胜 | 1.58 Stake（https://www.sportytrader.com/en/odds/sweden-bosnia-herzegovina-8318452/） | 1xBet 1.55、bet365 1.50–1.53；Oddschecker 13:42 1.55 | 霍尔姆、斯塔费尔特、泽内利、贝里瓦尔 | 穆哈雷莫维奇停赛、门将瓦西利；哲科已退役 | 瑞典胜即升A |
| 科索沃主胜 | 2.05 Stake（https://www.sportytrader.com/en/odds/kosovo-israel-8318363/） | Shangrila 1.98、BetMGM 1.952、bet365 1.82 | 拉赫马尼、哈伊达里、穆斯利亚 | 佩雷茨、巴里博、哈利拉伊利 | 科索沃争第二 |
| 法国客胜 | 1.99 Pinnacle（https://www.pinnacle.com/en/soccer/uefa-nations-league-a/italy-vs-france/1639766748/） | bet365 1.95；ESPN赔率页显示DK −125=1.80（scoreboard API仍为1.741） | 登贝莱、萨利巴、孔德、拉克鲁瓦、科内、阿克利乌什、勒保罗、卡卢卢 | 迪洛伦佐、基恩、拉斯帕多里、曼奇尼等 | 法国平局即进八强（Reuters） |
| 冰岛客胜 | 2.08 Stake/1xbet（https://www.sportytrader.com/en/odds/bulgaria-iceland-8318403/） | bet365 2.05、Sportsbet 1.82、Bovada 1.813 | 阿尔伯特·古德蒙德松、英加松、奥拉夫松 | 明切夫退出；德斯波多夫、克拉斯捷夫、季米特罗夫未入选 | 冰岛领先第二2分 |
| 阿尔巴尼亚主胜 | 2.17 1xBet（https://www.sportytrader.com/en/odds/albania-finland-8318439/） | bet365 2.02、YesPlay 1.98、DK 1.80、Caesars 1.87 | 斯特拉科沙、布罗亚（巴柳退役） | 洛德；卡马拉纪律原因未入选 | 首回合芬兰2-1；芬兰称是"决赛" |
| 比利时客胜 | 2.00 Mozzart（Futbol24，未直接核验） | YesPlay 1.94；ESPN赔率页DK −110=1.909 | 库尔图瓦、奥纳纳、拉维亚停赛、德巴斯特、奥彭达 | 伊尔迪兹、巴尔达克奇停赛、阿克蒂尔科格鲁未入选 | 土耳其新帅亚尔琴首秀 |
所有队伍首发均未公布。比价网站报价仅为页面展示值，不代表可成交。
