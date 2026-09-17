# 2026-09-17与09-18赛前来源审计

## 审计范围与账户

审计时间为2026-09-17 23:21至23:25（GMT+2）。本次“最近两天”按2026年9月17日和9月18日处理。当前账户权益及可用现金均为10,836.26元，未结算暴露0元。用户规则要求非英超总分至少84、英超至少88且赔率不低于1.50；项目仍没有经过冻结历史验证且可复现的总分字段，因此任何候选均不能正式批准。

## 赛程与当前状态

BBC在审计时显示Málaga对Villarreal已进行至90分钟，比分1比3；ESPN随后显示比赛处于90+分钟。冻结赛前模型不得用于场中或补时追注。9月17日其余9场欧联、Real Betis对Getafe及塞尔维亚联赛赛事均已完赛。

9月18日五大联赛实际有5场：Bayern Munich对Union Berlin、Monza对Sassuolo、Monaco对Lens、Brentford对Chelsea、Espanyol对Elche。BBC时间为英国夏令时，本审计统一换算为GMT+2。

来源：

- https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-17
- https://www.bbc.com/sport/football/scores-fixtures/2026-09-18
- https://www.premierleague.com/fixtures

## 模型与数据质量

B_a0.14滚动xG泊松模型和动态泊松—贝叶斯风险提示均以2026-09-17为AS_OF。所有目标赛事使用9月17日之前的状态批量预测；同一日期先预测后更新，目标窗口赛果不会写入模型。

Understat原始赛程错误地把Monaco对Lens列为2026-09-19 13:00 UTC。AS Monaco官网、BBC和ESPN一致显示实际比赛为2026-09-18 20:45（GMT+2）。因此预测器只对该场的赛程日期和时间进行了审计覆盖，球队历史状态与模型参数保持冻结，未写入任何未来赛果。

直接赛程来源：

- https://www.asmonaco.com/en/pros/fixtures
- https://www.espn.com/soccer/odds/_/gameId/401876453

## 最新90分钟赔率、模型与审批

| 日期/开球（GMT+2） | 比赛与模型方向 | B版 / Bayes | 最新可核验公开价 | B版最低1% EV价 | 参考EV | 审批 |
|---|---|---:|---:|---:|---:|---|
| 9月17日 21:30 | Málaga vs Villarreal：客胜 | 49.79% / 45.87% | 2.10关盘价 | 2.029 | +4.55% | 已开赛，不追场 |
| 9月18日 20:30 | Bayern vs Union：主胜 | 91.85% / 78.11% | 1.04 | 1.100 | -4.48% | 低于1.50，拒绝 |
| 9月18日 20:45 | Monaco vs Lens：Lens客胜 | 42.20% / 38.52% | 3.35 | 2.394 | +41.36% | 客胜不在正式权限，拒绝 |
| 9月18日 20:45 | Monza vs Sassuolo：Sassuolo客胜 | 49.61% / Bayes主胜38.97% | 2.42 | 2.036 | +20.04% | 客胜越权且模型方向冲突，拒绝 |
| 9月18日 21:00 | Brentford vs Chelsea：主胜 | 56.41% / 40.94% | 2.90 | 1.791 | +63.58% | 超2.00上限、模型差15.46pp及评分缺失，拒绝 |
| 9月18日 21:00 | Espanyol vs Elche：主胜 | 61.00% / 49.80% | 1.833 | 1.656 | +11.84% | 条件观察；评分与首发阻断，未批准 |

本表的赔率均是公开参考价，不代表用户平台可成交价。Bayern、Monaco、Brentford和Espanyol使用ESPN所示DraftKings或公开比较价；Monza对Sassuolo使用Libero/GRC Media列出的Stake 2.42。Oddschecker的Brentford主胜最佳价为19/10，即2.90，但页面可访问文本未显示该最佳价对应的具体博彩公司，因此不能当作用户可成交价。

直接赔率与阵容来源：

- Málaga vs Villarreal：https://www.espn.com/soccer/odds/_/gameId/401882869
- Bayern vs Union：https://www.espn.com/soccer/odds/_/gameId/401884790
- Monaco vs Lens：https://www.espn.com/soccer/odds/_/gameId/401876453 与 https://www.asmonaco.com/en/pros/fixtures
- Monza vs Sassuolo：https://www.libero.it/scommesse/calcio/serie-a/monza-vs-sassuolo-2026-09-18/ 与 https://en.legaseriea.it/serie-a/match/3e2b413e28e941eaa67c235d56f0f49e/monza-vs-sassuolo
- Brentford vs Chelsea：https://www.oddschecker.com/football/english/premier-league/brentford-v-chelsea/winner 与 https://www.chelseafc.com/en/match/brentford-vs-chelsea-english-premier-league-2026-09-18
- Espanyol vs Elche：https://www.espn.com/soccer/odds/_/gameId/401882862 与 https://www.whoscored.com/matches/1994153/preview/spain-laliga-2026-2027-espanyol-elche

## 专项市场与其他联赛

本窗口没有取得“恰好主让-1.25”或“球队至少赢一个半场”的直接、可核验且适用候选报价。相邻让球盘、半场三项胜负或预测价格不能替代真实专项报价。

9月17日欧联及9月18日其他非五大联赛赛事没有独立冻结的联赛/跨赛事模型，也没有可复现评分链，因此只能作赛程观察，不进入正式批准。
