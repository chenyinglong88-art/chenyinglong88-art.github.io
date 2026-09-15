# 2026-09-15与09-16赛前来源审计

## 审计范围与账户

审计时间为2026-09-15 20:41至20:46（GMT+2）。当前账户权益及可用现金均为10,836.26元，未结算暴露0元。用户规则要求非英超总分至少84、英超至少88且赔率不低于1.50；项目仍没有可复现的总分字段，因此即便有价格结构也不能正式批准。

## 赛程与当前状态

BBC 9月15日页面在审计时显示Rayo Vallecano对Espanyol已进行至81分钟，Alavés对Valencia进行至38分钟；本系统不允许把冻结赛前模型用于场中追注。今天仅剩Elche对Real Madrid尚未开赛。BBC 9月16日页面确认明天有9场欧联、4场西甲，另有瑞典及瑞士联赛。BBC时间为英国时间，本报告统一换算GMT+2。

来源：

- https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-15
- https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-16

## 最新冻结模型

模型以2026-09-15为AS_OF，纳入9月14日及此前已完赛Understat xG，同一预测窗口不写入未来赛果。七场西甲模型输出位于output/sep15_sep16_2026_frozen_models.csv。重点结果为：Elche对Real Madrid的B版客胜70.65%、Bayes客胜62.55%；Atletico主胜48.47%、Bayes主胜46.78%；Deportivo主胜50.95%、Bayes主胜43.88%；Barcelona主胜75.14%、Bayes主胜70.67%；Levante主胜63.87%、Bayes主胜42.81%。

## 最新90分钟赔率与阵容

| 日期 | 比赛 | 可核验90分钟价格 | 模型方向的B版EV | 阵容状态 | 审批含义 |
|---|---|---:|---:|---|---|
| 9月15日 | Elche vs Real Madrid | Real Madrid客胜-475，十进制1.211 | -14.48% | 两队首发已确认 | 低于模型1%EV最低价1.430及用户1.50下限，拒绝 |
| 9月16日 | Atletico vs Osasuna | Atletico主胜-255，十进制1.392 | -32.52% | 预测首发 | 价格过低，拒绝 |
| 9月16日 | Deportivo vs Sevilla | Deportivo主胜+148，十进制2.48 | +26.35% | 预测首发 | 高于锁定西甲扩展2.00上限，且评分不可验证，拒绝 |
| 9月16日 | Barcelona vs Racing | Barcelona主胜1.07 | -19.60% | 赛前 | 价格过低，拒绝 |
| 9月16日 | Levante vs Athletic | Levante主胜+230，十进制3.30 | +110.78% | 预测首发 | 高于扩展上限，且B/Bayes概率差21.06个百分点，拒绝 |

直接赔率与阵容来源：

- Elche vs Real Madrid：https://www.espn.com/soccer/odds/_/gameId/401882872 与 https://www.sportsgambler.com/betting-tips/football/elche-vs-real-madrid-prediction-lineups-odds-2026-09-15/
- Atletico vs Osasuna：https://www.espn.com/soccer/odds/_/gameId/401882875 与 https://www.sportsgambler.com/betting-tips/football/atletico-madrid-vs-osasuna-prediction-lineups-odds-2026-09-16/
- Deportivo vs Sevilla：https://www.sportsgambler.com/betting-tips/football/deportivo-la-coruna-vs-sevilla-prediction-lineups-odds-2026-09-16/ 与 https://www.toffeeweb.com/deportivo-a-coruna-vs-sevilla-predictions-picks-odds-16-09-2026/
- Barcelona vs Racing：https://www.toffeeweb.com/int/fc-barcelona-vs-racing-santander-predictions-picks-odds-16-09-2026/
- Levante vs Athletic：https://www.sportsgambler.com/betting-tips/football/levante-vs-athletic-club-prediction-lineups-odds-2026-09-16/ 与 https://tips.gg/article/levante-vs-athletic-bilbao-16-09-2026/

## 专项市场

Atletico对Osasuna可见的亚洲盘是主让-1.25、赔率-122（十进制1.820）。按B版泊松净胜球分布计算，该盘EV约-41.61%，未达到观察门槛7.5%，明确拒绝。其他页面列出的半场三项胜负赔率不是“球队至少赢一个半场”的同一市场；本窗口没有取得可直接核验的专项报价，因此不把推算价当作真实赔率。

明天9场欧联虽有公开市场赔率，但现有B版只冻结验证五大联赛常规联赛，不能跨赛事直接套用；缺少独立冻结欧战模型和可复现评分链，全部只作市场观察，不进入正式批准。
