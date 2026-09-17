# 2026-09-17与09-18最近两天推荐

**作者：Manus AI**  
**时区：GMT+2**  
**审计时间：2026-09-17 23:21–23:25**

> **结论：最近两天正式批准0场，建议投注0元。** 今天唯一仍在进行的五大联赛比赛已进入补时，不能追场；明天5场五大联赛中，只有Espanyol主胜通过价格与模型方向门槛，但总分84无法复现且首发未确认，因此仍不构成正式推荐。

## 今天：9月17日

BBC在审计时显示Málaga对Villarreal已经进行至90分钟，比分为1比3；其他欧联和西甲赛事均已完赛。[1] 模型在赛前冻结状态下给出Villarreal客胜49.79%，赛前关盘价2.10对应参考EV为+4.55%，但**任何已开赛比赛都不能使用赛前模型追注**。[2]

## 明天：9月18日

BBC和各联赛官方页面确认明天有5场五大联赛比赛。本报告使用B_a0.14滚动xG泊松作为正式1X2概率基础，并只把动态泊松—贝叶斯结果作为方向和不确定性提示。[3] [4]

| 开球 | 比赛与90分钟方向 | B版 / Bayes | 公开参考价 | 最低1% EV价 | 参考EV | 结论 |
|---|---|---:|---:|---:|---:|---|
| 20:30 | Bayern vs Union：Bayern主胜 | 91.85% / 78.11% | 1.04 | 1.100 | -4.48% | **拒绝：低于1.50** |
| 20:45 | Monaco vs Lens：Lens客胜 | 42.20% / 38.52% | 3.35 | 2.394 | +41.36% | **拒绝：客胜未授权** |
| 20:45 | Monza vs Sassuolo：Sassuolo客胜 | 49.61% / Bayes主胜38.97% | 2.42 | 2.036 | +20.04% | **拒绝：客胜未授权且模型冲突** |
| 21:00 | Brentford vs Chelsea：Brentford主胜 | 56.41% / 40.94% | 2.90 | 1.791 | +63.58% | **拒绝：超过2.00上限** |
| 21:00 | Espanyol vs Elche：Espanyol主胜 | 61.00% / 49.80% | 1.833 | 1.656 | +11.84% | **条件观察，未批准** |

### 唯一接近入场的比赛

**Espanyol主胜**是唯一同时处于1.50–2.00价格区间、B版EV不低于1%、B版与动态贝叶斯方向一致的候选。ESPN在审计时显示DraftKings主胜-120，折算十进制1.833；该价格高于B版达到1% EV所需的1.656。[10] 然而，B版与Bayes主胜概率仍相差11.20个百分点，且首发只是预测阵容。更关键的是，项目没有经过冻结历史验证、可复现的总分字段，所以无法证明达到用户要求的84分。**当前投注金额必须保持0元。**

若明天赛前总分链仍未建立，或者用户平台真实价格不在1.656–2.00之间，这场仍然不能批准。即使价格处于区间，也不能绕过总分与首发检查。

### 其余四场为何拒绝

Bayern主胜虽然模型概率很高，但DraftKings报价只有1.04，低于用户1.50下限，且相对B版概率仍是-4.48% EV。[5]

Lens客胜和Sassuolo客胜均不在当前锁定的正式权限内。Sassuolo一场还出现B版看客胜、Bayes看主胜的方向冲突。公开高赔率产生的表面正EV不能替代策略授权和风险一致性。[6] [7] [8]

Brentford主胜的Oddschecker最佳公开价为19/10，即2.90；这一价格超过英超/西甲主胜扩展的2.00上限。B版与Bayes主胜概率又相差15.46个百分点，且英超要求的88分无法复现，因此明确拒绝。[9] Chelsea官方也说明正式首发要到赛前公布，目前不能视为已确认。[11]

## 资金与执行

| 账户项目 | 当前数值 |
|---|---:|
| 账户权益 | 10,836.26元 |
| 可用现金 | 10,836.26元 |
| 未结算暴露 | 0元 |
| 最近两天正式批准 | 0场 |
| 正式投注金额 | 0元 |

本轮公开赔率仅用于筛选，不代表用户平台的实际可成交价格。亚洲主让-1.25和“至少赢一个半场”均未取得可直接核验且符合规则的真实报价，因此不作正式推荐。非五大联赛与欧战缺少独立冻结模型和评分链，也不进入正式清单。

投注可能损失全部本金。模型、赔率优势和历史回测均不保证未来盈利。**本报告仅供研究与分析，不构成个性化财务建议。**

## References

[1]: https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-17 "BBC European scores and fixtures for 17 September 2026"
[2]: https://www.espn.com/soccer/odds/_/gameId/401882869 "ESPN Málaga vs Villarreal game odds"
[3]: https://www.bbc.com/sport/football/scores-fixtures/2026-09-18 "BBC football scores and fixtures for 18 September 2026"
[4]: https://www.premierleague.com/fixtures "Premier League official fixtures"
[5]: https://www.espn.com/soccer/odds/_/gameId/401884790 "ESPN Bayern Munich vs Union Berlin game odds"
[6]: https://www.asmonaco.com/en/pros/fixtures "AS Monaco official 2026-27 fixtures"
[7]: https://www.espn.com/soccer/odds/_/gameId/401876453 "ESPN Monaco vs Lens game odds"
[8]: https://www.libero.it/scommesse/calcio/serie-a/monza-vs-sassuolo-2026-09-18/ "Libero Monza vs Sassuolo odds comparison"
[9]: https://www.oddschecker.com/football/english/premier-league/brentford-v-chelsea/winner "Oddschecker Brentford vs Chelsea win market"
[10]: https://www.espn.com/soccer/odds/_/gameId/401882862 "ESPN Espanyol vs Elche game odds"
[11]: https://www.chelseafc.com/en/match/brentford-vs-chelsea-english-premier-league-2026-09-18 "Chelsea official Brentford match centre"
