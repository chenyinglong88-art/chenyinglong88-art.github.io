# 2026-09-14至09-18赛程与赔率来源审计

## 时间与账户

研究窗口为2026-09-14至2026-09-18（GMT+2）。当前账户权益10,836.26元、可用现金10,836.26元、未结算暴露0元。普通信号单笔上限541.81元，激进观察规则单日12%上限1,300.35元；远期观察池不预占资金。

## 赛程日期交叉核验

BBC赛程页面直接确认：

- 9月14日：Villarreal vs Real Betis；Como vs Parma；Torino vs Roma；Inter vs Udinese，以及其他主流联赛比赛。
- 9月15日：Vallecano vs Espanyol；Alaves vs Valencia；Elche vs Real Madrid；Coppa Italia和其他主要赛事。
- 9月16日：欧联首轮9场；西甲Atletico Madrid vs Osasuna、Deportivo La Coruna vs Sevilla、Barcelona vs Racing Santander、Levante vs Athletic Club。
- 9月17日：欧联首轮9场；西甲Real Betis vs Getafe、Malaga vs Villarreal。
- 9月18日：Espanyol vs Elche；Bayern Munich vs Union Berlin；Monza vs Sassuolo；Monaco vs Lens；Brentford vs Chelsea，另有其他主流联赛比赛。

来源：
- https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-14
- https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-15
- https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-16
- https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-17
- https://www.bbc.com/sport/football/european/scores-fixtures/2026-09-18

Sky Sports 9月17和18日页面可作辅助，但正文抽取包含大量日历噪音，正式比赛清单以BBC正文为主。

## 第一轮公开赔率

并行核验于2026-09-13约21:55 GMT+2完成。主要可见报价包括：

- 9月15日：Alaves主胜约1.971；Bristol City主胜约2.02（非五大联赛候选需独立模型）。
- 9月16日：Barcelona主胜约1.082；Leverkusen主胜Celje约1.185；Olympiacos主胜约1.40；Atletico Madrid主胜约1.505；Sunderland主胜AZ约1.663；Everton杯赛主胜约1.66；Manchester United杯赛主胜约1.84。
- 9月17日：Crystal Palace主胜约1.36；Juventus主胜约1.22；Celtic主胜约1.67；Betis主胜约1.80；Villarreal客胜约1.95。
- 9月18日：Espanyol主胜约1.91；Bayern主胜约1.10；Monaco主胜约2.19；Monza主胜约2.75；Chelsea客胜约2.25。

9月14日并行子任务漏列Inter vs Udinese且未获取赔率；BBC确认该场存在，必须单独刷新。远期赔率仅作前瞻，比赛日仍需重新读取实际平台价格、首发与总分84。

## 2026-09-14模型刷新与直接赔率复核

冻结模型以2026-09-14为AS_OF，整个9月14日至18日窗口使用9月14日前状态一次性预测，远期赛果不反向更新状态。Understat五大联赛覆盖18场；B_a0.14与动态贝叶斯仅作概率对照，后者不是独立下注策略。

- 9月14日 Villarreal vs Betis：ESPN/DraftKings 90分钟主胜-105（十进制1.9524）、平局+290（3.90）、客胜+265（3.65）。B主胜58.23%，1% EV最低价1.7344，当前价格EV约13.6%；Bayes主胜54.72%，方向一致。该场仅进入西甲主胜扩展“临场复核”，因为当前总分84字段不可复现，且需最终首发与用户平台实际价格。来源：https://www.espn.com/soccer/odds/_/gameId/401882877
- Inter vs Udinese：Sportsgambler/BetMGM页面显示90分钟Inter主胜-417（十进制约1.2398）、平局+500、Udinese+1050；亚洲Inter -1.75为-125。B主胜76.15%，1% EV最低价1.3264，主胜当前负EV约-5.6%，拒绝；-1.75并非已验证的恰好-1.25观察规则。来源：https://www.sportsgambler.com/betting-tips/football/inter-milan-vs-udinese-prediction-lineups-odds-2026-09-14/
- Como vs Parma：Mozzart公开页面显示Como约1.22，低于B主胜最低价1.3306，拒绝。来源：https://www.mozzartsport.co.ke/football/news/betting-guide-inter-milan-vs-udinese-match-preview-team-news-and-prediction/68940
- Torino vs Roma：同一公开页列Roma客胜约1.55。B客胜65.92%，最低价1.5321，表面EV仅约2.18%；但锁定扩展只允许英超/西甲主胜，意甲客胜无正式权限，列观察而不批准。

## 9月15日至18日关键报价复核

- 9月15日 Rayo Vallecano vs Espanyol：ESPN/DraftKings主胜+105（十进制2.05）；WinComparator显示Bet365 2.10、比较区约2.02至2.16。B主胜52.44%，最低价1.9260，虽为正EV，但现价高于锁定扩展2.00上限，当前拒绝；只有用户平台回落到[1.926, 2.00]且总分、首发均通过时才可重新审核。来源：https://www.espn.com/soccer/odds/_/gameId/401882868 与 https://www.wincomparator.com/predictions/rayo-vallecano-espanyol-8586471/
- 9月18日 Espanyol vs Elche：WinComparator显示Bet365主胜1.75，比较区约1.75至2.05；为避免选择性使用最高价，审批情景采用可明确识别的Bet365 1.75。B主胜62.22%，最低价1.6233，1.75时EV约8.89%，Bayes主胜50.86%，方向一致但概率差11.36个百分点。该场进入西甲主胜扩展临场复核，仍因总分84不可验证而不批准。来源：https://www.wincomparator.com/predictions/espanyol-elche-8586477/
- 9月18日 Brentford vs Chelsea：ESPN/DraftKings主胜+180（2.80）、平局+280（3.80）、Chelsea+125（2.25）。B模型反向看好Brentford主胜56.75%，Bayes仅40.28%；价格超过英超扩展2.00上限且概率差16.47个百分点，拒绝。来源：https://www.espn.com/soccer/odds/_/gameId/401879275

亚洲-1.25与“至少赢一个半场”在本窗口尚未找到同时满足真实可核验报价、历史观察规则和临场条件的候选；不得把推算价写成真实平台报价。欧联、联赛杯、英冠和其他非五大联赛没有本系统冻结跨联赛模型与84分评分链，全部只能列市场观察，不得批准。

## 网站预览验收

本地生产数据预览已确认页面顶部显示：账户权益10,836.26元、可用现金10,836.26元、未结算暴露0元、未来五日2场条件观察、当前0场正式批准、批准金额0元。Villarreal与Espanyol卡片均明确写为临场复核且当前0元；Rayo、Inter、Brentford均显示价格或模型分歧拒绝原因，没有被误标为已批准。页面同时保留三笔已执行并结算记录。
