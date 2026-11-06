# 欢乐麻将 · H5 复刻版

基于腾讯《欢乐麻将》Android 客户端（`com.qqgame.happymj` 8.19.111）逆向分析的四川麻将复刻实现。
牌桌使用 **Phaser 3** 渲染，前端为 **uni-app（Vue3 + Vite）**，服务端为 **Go + cherry** 框架。

- 在线体验：<https://60.204.248.157:8081/mahjong/>（横屏版，竖屏手机自动旋转为横屏显示）
- 玩法：血战到底（定缺 / 换三张 / 刮风下雨 / 查大叫 / 查花猪 / 退税）
- 授权说明：牌面、按钮、头像、BGM 与音效均来自原版 APK 资源，**仅用于学习研究，不得商用**

## 目录结构

```
server/                  Go 服务端（cherry v1.6.9）
  main.go                启动入口：HTTP 9105 + WebSocket 9106
  internal/rule/         牌型、胡牌判定、番型与计分
  internal/game/         牌局状态机、结算、机器人
  internal/server/       Actor：lobby / room、pomelo 路由、HTTP 接口
  internal/store/        PostgreSQL + Redis（不可用时自动降级内存）
web/                     uni-app 前端
  src/pages/mahjong/     登录 / 大厅 / 牌桌三页
  src/utils/mahjong/     socket、协议、音效、Phaser 牌桌场景
  src/static/mahjong/    牌面、头像、字体、音效、背景
deploy/                  nginx 与 systemd 配置示例
```

## 已还原的功能点

**大厅（对齐原版白天城市天台首页，横屏布局）**

- 背景：原版 APK 内提取的真实大厅夜景图（`scenes` 图集 `bg`，紫色夜空烟花宫灯中式建筑），中央火焰绸带为原版 `bg_02` 前景层
- 顶部：返回、圆形头像（等级角标）、昵称 + 段位 + Lv、豆子 / 钻石资源条、邮箱（战绩）、设置
- 左侧：好友头像列（含在线点与皇冠标记）+ 邀请好友；圆形功能入口列（红包 / 如意秘宝 / 赏金令 / 好友房 / 活动）
- 中部：Q 版「牌娘」立绘（`ui/girl.svg`，手写 SVG）、吉祥物发仔与气泡台词
- 右侧：2×3 玩法卡片 —— 血流换三张（6 万在线）、红中血流、大众麻将、赛事、排位、娱乐，`更多玩法` 斜角标
- 右下：`百变万能血流` 活动条、场次切换（菜鸟 / 初级 / 中级 / 高手）、金色 `快速开始` 大按钮
- 底部：七项导航（商城 / 背包 / 赏金令 / 活动 / 福利 / 直播 / 更多）
- 弹层（浅色卡片风格）：创建房（玩法 / 局数 / 底分 / 换三张）、加入房（房号 + 在线房间）、商城（豆子 / 钻石）、7 日签到、赏金令任务、排位榜、战绩、设置

**牌桌（对齐原版对局界面）**

- 深玉绿绒桌布 + 描金细线四角云纹（程序化生成，`tools/gen_table_top.py`），原版牌面与牌背
- 中央方位盘：外圈 16 格刻度、剩余牌数、大字号操作倒计时、东/南/西/北四方方位字（当前行动方高亮）
- 顶部：返回、第 N/M 局与房号底分、规则 / 音效 / 退出
- 底部：第几手 + 剩余张数、结束对局；碰 / 杠 / 胡 操作按钮与出牌按钮
- 横屏画布：逻辑分辨率 1334×750（16:9），`Scale.NONE` + 页面层 `fitStage()` 手动等比缩放居中铺满
- 横屏布局：我方手牌底部横排、对家暗牌顶部横排、左右两家牌墙竖放叠列，中央方位盘 + 四方弃牌堆
- 强制横屏：`src/utils/orientation.js` 检测竖屏时把 uni-app 根元素顺时针旋转 90 度（宽高互换），
  并通过 MutationObserver 在路由切换后自动补挂旋转样式；
  旋转后 Phaser 内建坐标换算失效，牌面点击改为「原生事件坐标 → 画布逻辑坐标」手动换算后矩形命中
- 定缺（万 / 筒 / 条）、换三张（同花色三张）、出牌、碰、杠、胡、过
- 四方副露与弃牌堆、行动方位高亮、碰杠胡特效大字与音效、单局结算面板（四家零和）

## 资源与一致性

| 资源 | 来源 |
| --- | --- |
| 牌面 `tile_*.png` | 原包 `recommendfanui` 图集的 `paiNN` 精灵，2 倍放大 |
| 按钮 / 头像 / 顶栏图标 | 原包 `commonui` 图集 |
| 字体 | 原包 `FZCuKaiJianTi`（标题）、`FZLanTingZhunHei`（正文），子集化为 woff2 |
| 音效 | 原包 FSB5 音频，用 vgmstream 解码后转 MP3（点击 / 选牌 / 出牌 / 摸牌 / 碰 / 杠 / 胡 / 倒计时 / 骰子） |
| 背景音乐 | 原包 `PlayingInGame` |

## 本地运行

```bash
# 服务端（Go 1.24）
cd server
go run . -profile config/mahjong.json       # HTTP 9105 / WS 9106

# 前端
cd web
npm install
npm run dev:h5                              # http://localhost:5173/mahjong/
```

服务端在无 PostgreSQL / Redis 时自动降级内存模式，`/health` 返回 `memory:true`。

环境变量：

| 变量 | 说明 | 默认 |
| --- | --- | --- |
| `MJ_HTTP_ADDR` | HTTP 监听地址 | `127.0.0.1:9105` |
| `MJ_DSN` | PostgreSQL 连接串 | 空（内存模式） |
| `MJ_REDIS_ADDR` | Redis 地址 | 空（内存模式） |
| `MJ_REDIS_DB` | Redis 库号 | `0` |

## 部署

`deploy/` 下提供：

- `mahjong-api.service`：systemd 单元，参考 `/etc/systemd/system/`
- `nginx-mahjong.conf`：三条 location（`/mahjong/` 静态站点、`/mahjong-api/` 接口、`/mahjong-ws/` WebSocket）

构建与发布：

```bash
cd web && npm run build:h5                  # 产物 dist/build/h5
cd server && CGO_ENABLED=0 go build -o mahjong .
```

## 测试

```bash
cd server
go test ./...        # 规则 8 组用例 + 200 局随机模拟零和校验
```

## 说明

- 本项目为技术复刻，与原版无任何关联；
- H5 版不含语音聊天、支付、微信/QQ 登录等依赖原生 SDK 的能力；
- 商城、签到、任务为本地演示逻辑，数据存于 `localStorage`。
