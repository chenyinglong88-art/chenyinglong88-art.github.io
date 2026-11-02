# 2026-11-02 本周（11-02至11-08）五大联赛外部数据记录

核验时间：2026-11-02 09:34–10:00 CET（北京时间16:34–17:00）

## 1. Understat 数据源故障
- `understat.com` 在 2026-11-02 无法解析：沙箱DNS（8.8.8.8）返回 NXDOMAIN；Google DoH `https://dns.google/resolve?name=understat.com&type=A` 返回 Status 2（SERVFAIL）；Cloudflare DoH 返回 `EDE(22): No Reachable Authority at delegation understat.com`。网页抓取通道也报 "could not resolve hostname"。
- 这是 Understat 域名授权服务器不可达，不是本地网络问题（ESPN、GitHub、Google 正常解析）。
- 正式模型因此使用 2026-10-29 的 Understat 缓存快照：EPL最后完赛 2026-10-25，西甲 2026-10-26，德甲 2026-10-25，意甲 2026-10-28，法甲 2026-10-25。缺少 10-29至11-01 共47场五大联赛完赛数据。

## 2. FotMob 补充（仅敏感性）
- 来源：`https://www.fotmob.com/api/data/matches?date=YYYYMMDD` 与 `https://www.fotmob.com/api/data/matchDetails?matchId=...`（原始JSON在 xg_data/raw/fotmob_nov02/）。
- 抓取 2026-10-18 至 11-02 五大联赛完赛125场，xG 缺失0场。
- 与 Understat 重叠78场校准：Understat/FotMob xG 总量比 1.0484；球队单场 xG 相关系数 0.943；平均绝对差 0.249；比分一致率 100%。
- 注入缺失的47场（英超9、西甲9、德甲9、意甲12、法甲8），xG = FotMob × 1.0484；生成敏感性模型 `nov02_nov09_2026_asof1102_fotmob_supp_models.csv`。
- 两版模型主胜概率差：B版平均0.98pp、最大6.34pp（Sevilla–Alaves）；贝叶斯平均1.32pp、最大3.0pp。
- 补充版不是正式模型，只用来检验排名是否稳健。

## 3. 改期场次（ESPN 2026-11-02 scoreboard 显示今日开赛，Understat缓存仍为旧日期）
- Deportivo La Coruña vs Osasuna：11-02 21:00 CET（原11-01）
- Lorient vs Brest：11-02 20:45 CET（原10-31）
- Sassuolo vs Fiorentina：11-02 18:30 CET（原11-01）
- Atalanta vs Parma：11-02 20:45 CET（原11-01）
来源：`https://site.api.espn.com/apis/site/v2/sports/soccer/{ita.1|fra.1|esp.1}/scoreboard?dates=20261102`

## 4. ESPN / DraftKings 赔率
- 来源：`https://site.api.espn.com/apis/site/v2/sports/soccer/{eng.1,esp.1,ger.1,ita.1,fra.1}/scoreboard?dates=20261102..20261109`，原始文件 xg_data/raw/espn_nov2026_asof1102/。
- 本周（11-02至11-08）53场，全部匹配模型；Frankfurt–Hamburg 无报价。

## 5. 上周观察榜终场（ESPN，FotMob比分一致）
| 比赛 | 比分 | FotMob xG |
|---|---|---|
| Leverkusen vs Stuttgart（10-31） | 2–4 | 1.79–2.61 |
| Bournemouth vs Leeds（10-31） | 2–0 | 1.29–0.71 |
| Hull vs Ipswich（10-31） | 2–2 | 0.78–1.06 |
| Athletic vs Real Sociedad（11-01） | 2–1 | 3.08–1.15 |
| Man City vs Brighton（10-31） | 0–1 | 1.64–1.00 |
| Como vs Venezia（11-01） | 1–0 | 1.63–0.19 |
| Lyon vs Angers（11-01） | 2–0 | 2.36–0.75 |
