<template>
  <view class="hall">
    <!-- 背景：白天城市天台 -->
    <image class="hall__bg" :src="bgImage" mode="aspectFill" />

    <!-- 顶部：返回、玩家信息、豆子钻石、邮箱设置 -->
    <view class="topbar">
      <view class="tbn" @click="logout">
        <image class="tbn__ico" :src="native('ico_back')" mode="aspectFit" />
      </view>

      <view class="user">
        <view class="user__frame">
          <image class="user__face" :src="avatar" mode="aspectFill" />
          <view class="user__lv">{{ levelNo }}</view>
        </view>
        <view class="user__meta">
          <text class="user__nick">{{ profile.nick || '玩家' }}</text>
          <view class="user__tags">
            <text class="tag tag--rank">{{ levelText }}</text>
            <text class="tag tag--lv">Lv.{{ levelNo }}</text>
          </view>
        </view>
      </view>

      <view class="topbar__fill"></view>

      <view class="res" @click="openSheet('shop')">
        <image class="res__ico" :src="beanIcon" mode="aspectFit" />
        <text class="res__num">{{ beanText }}</text>
        <image class="res__add" :src="plusIcon" mode="aspectFit" />
      </view>
      <view class="res" @click="openSheet('shop')">
        <image class="res__ico" :src="diamondIcon" mode="aspectFit" />
        <text class="res__num">{{ diamond }}</text>
        <image class="res__add" :src="plusIcon" mode="aspectFit" />
      </view>
      <view class="tbn tbn--round" @click="openSheet('records')">
        <image class="tbn__ico" :src="icon('mail')" mode="aspectFit" />
        <view class="tbn__dot"></view>
      </view>
      <view class="tbn tbn--round" @click="openSheet('setting')">
        <image class="tbn__ico" :src="native('ico_setting')" mode="aspectFit" />
      </view>
    </view>

    <!-- 左侧好友列 -->
    <view class="friends">
      <view class="friend" v-for="(f, i) in friends" :key="f.nick" @click="openSheet('friend')">
        <view class="friend__frame" :style="`background:${f.bg}`">
          <text class="friend__face">{{ f.nick.slice(0, 1) }}</text>
          <view class="friend__crown" v-if="i < 2">
            <image class="friend__crown-ico" :src="icon('crown')" mode="aspectFit" />
          </view>
        </view>
        <text class="friend__name">{{ f.nick }}</text>
        <view class="friend__dot" v-if="f.online"></view>
      </view>
      <view class="friends__invite" @click="openSheet('friend')">
        <text class="friends__invite-text">邀请</text>
        <text class="friends__invite-text">好友</text>
      </view>
    </view>

    <!-- 左侧圆形入口列 -->
    <view class="entries">
      <view class="entry" v-for="item in entries" :key="item.key" @click="openSheet(item.key)">
        <view class="entry__btn" :class="`entry__btn--${item.tone}`">
          <image class="entry__bg" :src="native(`round_${item.tone}`)" mode="aspectFill" />
          <image class="entry__ico" :src="icon(item.icon)" mode="aspectFit" />
        </view>
        <view class="entry__dot" v-if="item.dot"></view>
        <text class="entry__label" v-if="item.label">{{ item.label }}</text>
      </view>
    </view>

    <!-- 中央角色 -->
    <view class="hero__shadow"></view>
    <image class="hero" :src="girlImage" mode="aspectFit" />

    <!-- 吉祥物发仔 -->
    <view class="penpen" @click="toast('发仔：今天也要胡大牌哦！')">
      <view class="penpen__bubble">
        <text class="penpen__bubble-text">三缺一，来搓一局！</text>
      </view>
      <image class="penpen__img" :src="fazaiImage" mode="aspectFit" />
    </view>

    <!-- 右侧玩法卡 -->
    <view class="plays">
      <view
        v-for="item in playCards"
        :key="item.key"
        class="play"
        :class="`play--${item.tone}`"
        :style="`height:${item.h}rpx`"
        @click="pickPlay(item)">
        <view class="play__body">
          <view class="play__chars">
            <text class="play__char" v-for="(ch, ci) in item.chars" :key="ci">{{ ch }}</text>
          </view>
          <text class="play__tail">{{ item.tail }}</text>
        </view>
        <view class="play__foot" v-if="item.online">
          <image class="play__fire" :src="icon('crown')" mode="aspectFit" />
          <text class="play__num">{{ item.online }}</text>
        </view>
        <view class="play__lock" v-else>
          <image class="play__lock-ico" :src="icon('lock')" mode="aspectFit" />
        </view>
      </view>
    </view>

    <!-- 更多玩法角标 -->
    <view class="more" @click="toast('更多玩法陆续开放')">
      <text class="more__text">更多玩法</text>
    </view>

    <!-- 活动横幅 -->
    <view class="banner" @click="openSheet('sign')">
      <image class="banner__bg" :src="native('banner_red')" mode="aspectFill" />
      <image class="banner__ico" :src="icon('gift')" mode="aspectFit" />
      <text class="banner__text">百变万能血流</text>
      <view class="banner__go">
        <text class="banner__go-text">GO</text>
      </view>
    </view>

    <!-- 场次切换 -->
    <view class="ranks">
      <view
        v-for="(item, index) in rankList"
        :key="item.name"
        :class="pickedRank === index ? 'rank rank--on' : 'rank'"
        @click="pickRank(index)">
        <text class="rank__text">{{ item.short }}</text>
      </view>
    </view>

    <!-- 快速开始 -->
    <view class="start" @click="quickStart">
      <view class="start__glow"></view>
      <image class="start__bg" :src="native('btn_gold')" mode="stretch" />
      <view class="start__btn">
        <text class="start__title">快速开始</text>
        <text class="start__sub">{{ currentRank.name }} · {{ currentPlay.name }}</text>
      </view>
    </view>

    <!-- 底部导航 -->
    <view class="dock">
      <image class="dock__bg" :src="native('bar_dark')" mode="stretch" />
      <view class="dock__item" v-for="(tab, index) in tabs" :key="tab.key" @click="switchTab(index)">
        <view class="dock__icon-wrap">
          <image class="dock__icon" :src="icon(tab.icon)" mode="aspectFit" :style="pickedTab === index ? '' : 'opacity:.72'" />
          <view class="dock__dot" v-if="tab.dot"></view>
        </view>
        <text :class="pickedTab === index ? 'dock__text dock__text--on' : 'dock__text'">{{ tab.label }}</text>
      </view>
    </view>

    <!-- 通用弹层 -->
    <view class="mj-mask" v-if="sheet" @click="closeSheet">
      <view class="panel" :class="sheet === 'join' || sheet === 'records' ? 'panel--tall' : ''" @click.stop>
        <view class="panel__head">
          <text class="panel__title">{{ sheetTitle }}</text>
          <image class="panel__close" :src="native('close')" mode="aspectFit" @click="closeSheet" />
        </view>

        <!-- 创建房间 -->
        <view class="panel__body" v-if="sheet === 'create'">
          <text class="field__label">玩法</text>
          <view class="chips">
            <view
              v-for="(play, index) in plays"
              :key="play.key"
              :class="pickedPlay === index ? 'chip chip--on' : 'chip'"
              @click="pickedPlay = index; audio.play('click')">
              <text class="chip__text">{{ play.name }}</text>
            </view>
          </view>

          <text class="field__label">局数</text>
          <view class="chips">
            <view
              v-for="n in [4, 8, 16]"
              :key="n"
              :class="rounds === n ? 'chip chip--on' : 'chip'"
              @click="rounds = n; audio.play('click')">
              <text class="chip__text">{{ n }} 局</text>
            </view>
          </view>

          <text class="field__label">底分</text>
          <view class="chips">
            <view
              v-for="(item, index) in rankList"
              :key="item.base"
              :class="pickedRank === index ? 'chip chip--on' : 'chip'"
              @click="pickRank(index)">
              <text class="chip__text">{{ item.base }} 分</text>
            </view>
          </view>

          <view class="switch-row">
            <text class="switch-row__label">换三张</text>
            <switch :checked="swap3" color="#E0B75C" @change="onSwapChange" />
          </view>

          <view class="panel__ok" @click="createRoom">
            <text class="panel__ok-text">创建并入座</text>
          </view>
        </view>

        <!-- 加入房间 -->
        <view class="panel__body" v-if="sheet === 'join'">
          <view class="code">
            <input class="code__input" v-model="roomCode" type="number" maxlength="6" placeholder="输入 6 位房号" placeholder-class="code__ph" />
            <view class="code__btn" @click="joinByCode">
              <text class="code__btn-text">加入</text>
            </view>
          </view>

          <text class="field__label">在线房间</text>
          <scroll-view class="room-list" scroll-y v-if="rooms.length">
            <view class="room" v-for="room in rooms" :key="room.roomId" @click="joinRoom(room)">
              <view class="room__info">
                <text class="room__id">房号 {{ room.roomId }}</text>
                <text class="room__meta">{{ room.seats }}/4 人 · 第 {{ room.round }}/{{ room.maxRound }} 局 · 底分 {{ room.base }}</text>
              </view>
              <text class="room__act">{{ room.playing ? '观战' : '加入' }}</text>
            </view>
          </scroll-view>
          <view class="empty" v-else>
            <text class="empty__text">暂无房间，创建一个吧</text>
          </view>
        </view>

        <!-- 商城 -->
        <view class="panel__body" v-if="sheet === 'shop'">
          <view class="shop-tabs">
            <view
              v-for="(tab, index) in shopTabs"
              :key="tab"
              :class="shopTab === index ? 'shop-tab shop-tab--on' : 'shop-tab'"
              @click="shopTab = index">
              <text class="shop-tab__text">{{ tab }}</text>
            </view>
          </view>
          <view class="goods" v-for="item in goodsList" :key="item.id">
            <view class="goods__left">
              <image class="goods__icon" :src="shopTab === 0 ? beanIcon : diamondIcon" mode="aspectFit" />
              <view class="goods__text">
                <text class="goods__name">{{ item.name }}</text>
                <text class="goods__desc">{{ item.desc }}</text>
              </view>
            </view>
            <view class="goods__btn" @click="buy(item)">
              <text class="goods__price">¥ {{ item.price }}</text>
            </view>
          </view>
        </view>

        <!-- 每日签到 -->
        <view class="panel__body" v-if="sheet === 'sign'">
          <text class="panel__tip">连续签到 7 天可领豪华礼包</text>
          <view class="sign-grid">
            <view
              v-for="(day, index) in signDays"
              :key="day.day"
              :class="signState(index)"
              @click="doSign(index)">
              <text class="sign__day">第 {{ day.day }} 天</text>
              <image class="sign__icon" :src="day.icon === 'bean' ? beanIcon : diamondIcon" mode="aspectFit" />
              <text class="sign__num">×{{ day.amount }}</text>
              <text class="sign__state">{{ signDone(index) ? '已领' : '领取' }}</text>
            </view>
          </view>
        </view>

        <!-- 每日任务 -->
        <view class="panel__body" v-if="sheet === 'task'">
          <view class="task" v-for="item in tasks" :key="item.id">
            <view class="task__left">
              <text class="task__name">{{ item.name }}</text>
              <view class="task__bar">
                <view class="task__fill" :style="`width:${Math.min(100, item.now / item.need * 100)}%`"></view>
              </view>
              <text class="task__progress">{{ item.now }}/{{ item.need }}</text>
            </view>
            <view :class="item.now >= item.need ? 'task__btn task__btn--on' : 'task__btn'" @click="claimTask(item)">
              <text class="task__btn-text">{{ item.claimed ? '已领' : '领取' }}</text>
            </view>
          </view>
        </view>

        <!-- 排行榜 -->
        <view class="panel__body" v-if="sheet === 'rank'">
          <text class="panel__tip">本周积分榜（演示数据，含机器人）</text>
          <view class="rank-row" v-for="(row, index) in rankRows" :key="row.uid">
            <text :class="index < 3 ? 'rank-row__no rank-row__no--top' : 'rank-row__no'">{{ index + 1 }}</text>
            <image class="rank-row__avatar" :src="row.me ? avatar : avatarDefault" mode="aspectFill" />
            <text class="rank-row__name">{{ row.nick }}{{ row.me ? '（我）' : '' }}</text>
            <text class="rank-row__score">{{ row.score }}</text>
          </view>
        </view>

        <!-- 战绩 -->
        <view class="panel__body" v-if="sheet === 'records'">
          <view class="record" v-for="item in records" :key="item.id">
            <view class="record__left">
              <text class="record__room">房号 {{ item.roomId }}</text>
              <text class="record__time">{{ item.createdAt }}</text>
            </view>
            <text :class="item.score >= 0 ? 'record__score record__score--win' : 'record__score'">
              {{ item.score >= 0 ? '+' : '' }}{{ item.score }}
            </text>
          </view>
          <view class="empty" v-if="!records.length">
            <text class="empty__text">还没有战绩，先来一局</text>
          </view>
        </view>

        <!-- 设置 -->
        <view class="panel__body" v-if="sheet === 'setting'">
          <view class="switch-row">
            <text class="switch-row__label">背景音乐</text>
            <switch :checked="bgmOn" color="#E0B75C" @change="onBgmChange" />
          </view>
          <view class="switch-row">
            <text class="switch-row__label">游戏音效</text>
            <switch :checked="soundOn" color="#E0B75C" @change="onSoundChange" />
          </view>
          <view class="panel__ok panel__ok--ghost" @click="logout">
            <text class="panel__ok-text panel__ok-text--ghost">退出登录</text>
          </view>
          <text class="panel__ver">欢乐麻将 H5 复刻版 v1.2.0</text>
        </view>

        <!-- 好友 / 我的（占位说明） -->
        <view class="panel__body" v-if="sheet === 'friend' || sheet === 'mine'">
          <view class="empty">
            <text class="empty__text">该功能在 App 内为原生模块，H5 版暂以好友房替代</text>
          </view>
          <view class="panel__ok" @click="openSheet('create')">
            <text class="panel__ok-text">去创建好友房</text>
          </view>
        </view>

        <!-- 未开放玩法 -->
        <view class="panel__body" v-if="sheet === 'todo'">
          <view class="empty">
            <text class="empty__text">{{ todoText }}</text>
          </view>
          <view class="panel__ok" @click="openSheet('join')">
            <text class="panel__ok-text">去好友房开搓</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 全局提示 -->
    <view class="toast" v-if="toastText">
      <text class="toast__text">{{ toastText }}</text>
    </view>

    <!-- 退出确认 -->
    <view class="confirm" v-if="confirmVisible">
      <view class="confirm__card">
        <text class="confirm__title">退出登录</text>
        <text class="confirm__text">确定要退出当前账号吗？</text>
        <view class="confirm__btns">
          <view class="confirm__btn confirm__btn--ghost" @click="confirmVisible = false">
            <text class="confirm__btn-text confirm__btn-text--ghost">取消</text>
          </view>
          <view class="confirm__btn" @click="doLogout">
            <text class="confirm__btn-text">退出</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 开局等待 -->
    <view class="loading" v-if="busy">
      <text class="loading__text">{{ busyText }}</text>
    </view>
  </view>
</template>

<script>
/**
 * 组件名称：mahjongLobby
 * 功能说明：麻将大厅，按原版首页布局提供玩法入口、场次选择、快速开始、好友房、商城、签到、任务、排行与设置
 * 研发时间：2026/11/03
 * 研发人员：郑朝军
 *
 * 变量说明：
 * @data {Object}  profile      - 玩家资料
 * @data {Array}   plays        - 玩法配置
 * @data {Array}   rooms        - 在线房间
 * @data {Number}  pickedRank   - 当前场次下标
 * @data {Number}  pickedPlay   - 当前玩法下标
 * @data {Number}  rounds       - 房间局数
 * @data {Boolean} swap3        - 是否开启换三张
 * @data {String}  sheet        - 当前弹层标识
 * @data {Array}   records      - 战绩
 * @data {Boolean} busy         - 连接或开局中
 *
 * 事件说明：
 * @event ensureSocket - 建立长连接
 * @event quickStart   - 快速开局
 * @event createRoom   - 创建好友房
 * @event joinRoom     - 加入房间
 * @event openSheet    - 打开弹层
 *
 * 插槽说明：
 */

/**
 * 修改时间       人员        说明
 * 2026/11/03     郑朝军      初始创建
 * 2026/11/03     郑朝军      重做首页：还原原版大厅布局、原版字体与音效，补齐商城/签到/任务/排行/设置
 * 2026/11/04     郑朝军      二次重做：改为原版白天城市天台风格，补齐好友列、圆形入口列、角色立绘、玩法卡片与底部导航
 * 2026/11/04     郑朝军      横屏版：整体布局按 16:9 横屏重排，退出确认改为页面内弹层
 */
import { ASSET_BASE } from '@/utils/mahjong/const.js'
import { fetchRecords, fetchProfile } from '@/utils/mahjong/api.js'
import { clearAuth, getToken, getUser, setUser } from '@/utils/mahjong/http.js'
import { setStore, getStore } from '@/utils/mahjong/store.js'
import socket from '@/utils/mahjong/socket.js'
import audio from '@/utils/mahjong/audio.js'

/** 场次配置：名称、简称、底分、封顶番数 */
const RANKS = [
  { name: '菜鸟场', short: '菜鸟', base: 1, cap: 4 },
  { name: '初级场', short: '初级', base: 2, cap: 5 },
  { name: '中级场', short: '中级', base: 5, cap: 6 },
  { name: '高手场', short: '高手', base: 10, cap: 8 }
]

/** 玩法卡：chars 为竖排大字，tail 为右侧小字 */
const PLAY_CARDS = [
  { key: 'blood', chars: ['血', '流'], tail: '换三张', online: 60000, h: 236, tone: 'red', play: '血流换三张' },
  { key: 'red', chars: ['红', '中'], tail: '血流', online: 10019, h: 236, tone: 'cyan', play: '红中血流' },
  { key: 'dazhong', chars: ['大', '众'], tail: '麻将', online: 17257, h: 168, tone: 'gold', play: '大众麻将' },
  { key: 'match', chars: ['赛', '事'], tail: '比赛', online: 0, h: 168, tone: 'sand', icon: 'trophy', todo: '赛事中心正在筹备，敬请期待' },
  { key: 'rank', chars: ['排', '位'], tail: '段位', online: 0, h: 148, tone: 'sand', icon: 'rank', sheet: 'rank' },
  { key: 'fun', chars: ['娱', '乐'], tail: '休闲', online: 0, h: 148, tone: 'sand', icon: 'dice', todo: '娱乐玩法正在筹备，敬请期待' }
]

/** 商城商品 */
const GOODS = {
  bean: [
    { id: 'b1', name: '豆子 10 万', desc: '新手补给', price: 6, amount: 100000 },
    { id: 'b2', name: '豆子 60 万', desc: '超值推荐', price: 30, amount: 600000 },
    { id: 'b3', name: '豆子 150 万', desc: '土豪专享', price: 68, amount: 1500000 }
  ],
  diamond: [
    { id: 'd1', name: '钻石 60', desc: '可开好友房', price: 6, amount: 60 },
    { id: 'd2', name: '钻石 300', desc: '赠送 30', price: 30, amount: 330 },
    { id: 'd3', name: '钻石 680', desc: '赠送 88', price: 68, amount: 768 }
  ]
}

export default
{
  data()
  {
    return {
      profile: { uid: '', nick: '玩家', score: 0, avatar: '' },
      plays: [],
      rooms: [],
      records: [],
      pickedRank: 0,
      pickedPlay: 0,
      pickedTab: 0,
      rounds: 4,
      swap3: true,
      sheet: '',
      shopTab: 0,
      shopTabs: ['豆子', '钻石'],
      roomCode: '',
      bean: 0,
      diamond: 0,
      todoText: '',
      friends: [
        { nick: '川妹子', bg: 'linear-gradient(160deg, #F28C8C 0%, #C0392B 100%)', online: true },
        { nick: '幺鸡王', bg: 'linear-gradient(160deg, #F0B856 0%, #C9862A 100%)', online: true },
        { nick: '老王', bg: 'linear-gradient(160deg, #6FA8DC 0%, #3A6EA8 100%)', online: true },
        { nick: '小满', bg: 'linear-gradient(160deg, #8A6BDF 0%, #5E44B8 100%)', online: false },
        { nick: '阿福', bg: 'linear-gradient(160deg, #52C08A 0%, #2A8A5A 100%)', online: true }
      ],
      entries: [
        { key: 'shop', icon: 'redpack', tone: 'red', label: '红包', dot: true },
        { key: 'sign', icon: 'chest', tone: 'gold', label: '如意秘宝', dot: false },
        { key: 'task', icon: 'medal', tone: 'orange', label: '', dot: true },
        { key: 'join', icon: 'friend', tone: 'green', label: '', dot: false },
        { key: 'activity', icon: 'activity', tone: 'blue', label: '', dot: true }
      ],
      signDays: [
        { day: 1, icon: 'bean', amount: 2000 },
        { day: 2, icon: 'bean', amount: 3000 },
        { day: 3, icon: 'bean', amount: 5000 },
        { day: 4, icon: 'diamond', amount: 20 },
        { day: 5, icon: 'bean', amount: 8000 },
        { day: 6, icon: 'diamond', amount: 30 },
        { day: 7, icon: 'diamond', amount: 60 }
      ],
      signed: [],
      claimed: [],
      tasks: [
        { id: 't1', name: '完成 1 局牌局', now: 0, need: 1, reward: 2000 },
        { id: 't2', name: '完成 3 局牌局', now: 0, need: 3, reward: 5000 },
        { id: 't3', name: '胡牌 1 次', now: 0, need: 1, reward: 3000 }
      ],
      bgmOn: true,
      soundOn: true,
      busy: false,
      busyText: '连接中…',
      confirmVisible: false,
      toastText: '',
      toastTimer: null,
      noticeTimer: null
    }
  },

  computed:
  {
    /** 大厅背景：白天城市天台 */
    bgImage()
    {
      return `${ASSET_BASE}/ui/native/hall_bg.jpg`
    },

    /** 角色立绘 */
    girlImage()
    {
      return `${ASSET_BASE}/ui/girl.svg`
    },

    /** 吉祥物 */
    fazaiImage()
    {
      return `${ASSET_BASE}/ui/native/fazai.png`
    },

    /** 头像 */
    avatar()
    {
      return this.profile.avatar || this.avatarDefault
    },

    /** 默认头像 */
    avatarDefault()
    {
      return `${ASSET_BASE}/ui/avatar.png`
    },

    /** 豆子图标 */
    beanIcon()
    {
      return `${ASSET_BASE}/ui/native/ico_bean.png`
    },

    /** 钻石图标 */
    diamondIcon()
    {
      return `${ASSET_BASE}/ui/native/ico_diamond.png`
    },

    /** 加号图标 */
    plusIcon()
    {
      return `${ASSET_BASE}/ui/native/ico_plus.png`
    },

    /** 场次列表 */
    rankList()
    {
      return RANKS
    },

    /** 当前场次 */
    currentRank()
    {
      return RANKS[this.pickedRank] || RANKS[0]
    },

    /** 玩法卡 */
    playCards()
    {
      return PLAY_CARDS
    },

    /** 当前玩法 */
    currentPlay()
    {
      return (this.plays[this.pickedPlay] && { name: this.plays[this.pickedPlay].name })
        || { name: PLAY_CARDS[0].play }
    },

    /** 豆子文案：超过一万用万作单位 */
    beanText()
    {
      const n = Number(this.bean) || 0

      return n >= 10000 ? `${(n / 10000).toFixed(n % 10000 === 0 ? 0 : 1)}万` : String(n)
    },

    /** 段位文案，按累计积分划分 */
    levelText()
    {
      const score = Number(this.profile.score) || 0

      if (score >= 500) return '雀神'
      if (score >= 200) return '大师'
      if (score >= 80) return '高手'
      if (score >= 20) return '老手'

      return '新手'
    },

    /** 等级数字，由积分折算，仅作展示 */
    levelNo()
    {
      return Math.max(1, Math.min(60, Math.floor((Number(this.profile.score) || 0) / 12) + 1))
    },

    /** 弹层标题 */
    sheetTitle()
    {
      const map = {
        create: '创建房间',
        join: '加入房间',
        shop: '商城',
        sign: '如意秘宝 · 签到',
        task: '赏金令',
        rank: '排位榜',
        records: '我的战绩',
        setting: '设置',
        friend: '好友',
        mine: '我的',
        activity: '福利活动',
        todo: '敬请期待'
      }

      return map[this.sheet] || ''
    },

    /** 底部导航：与原版一致，七项 */
    tabs()
    {
      return [
        { key: 'shop', label: '商城', icon: 'shopcart' },
        { key: 'mine', label: '背包', icon: 'bag' },
        { key: 'task', label: '赏金令', icon: 'medal', dot: this.tasks.some((t) => t.now >= t.need && !t.claimed) },
        { key: 'sign', label: '活动', icon: 'activity', dot: !this.signDoneToday },
        { key: 'activity', label: '福利', icon: 'gift', dot: true },
        { key: 'live', label: '直播', icon: 'live', dot: false },
        { key: 'more', label: '更多', icon: 'more', dot: false }
      ]
    },

    /** 商城当前分类商品 */
    goodsList()
    {
      return this.shopTab === 0 ? GOODS.bean : GOODS.diamond
    },

    /** 今日是否已签到 */
    signDoneToday()
    {
      return this.signed.includes(this.todayKey())
    },

    /** 本周期已签天数，最多 7 天 */
    signProgress()
    {
      return Math.min(this.signed.length, 7)
    },

    /** 排行榜：本人 + 机器人演示数据 */
    rankRows()
    {
      const rows = [
        { uid: 'b1', nick: '发仔', score: 1280 },
        { uid: 'b2', nick: '川妹子', score: 960 },
        { uid: 'b3', nick: '幺鸡大王', score: 735 },
        { uid: 'b4', nick: '血战老兵', score: 512 },
        { uid: 'me', nick: this.profile.nick || '我', score: Number(this.profile.score) || 0, me: true }
      ]

      return rows.sort((a, b) => b.score - a.score)
    }
  },

  onLoad()
  {
    if (!getToken())
    {
      uni.reLaunch({ url: '/pages/mahjong/login' })
      return
    }

    const cached = getUser()

    if (cached)
    {
      this.profile = {
        uid: cached.uid || '',
        nick: cached.nick || '玩家',
        score: cached.score || 0,
        avatar: cached.avatar || ''
      }
    }

    this.restoreLocal()
    this.injectFont()
    this.init()
  },

  onShow()
  {
    if (getToken() && !this.busy)
    {
      this.refreshTasks()
    }
  },

  onUnload()
  {
    audio.pauseBgm()
    clearInterval(this.noticeTimer)
  },

  onHide()
  {
    audio.pauseBgm()
  },

  methods:
  {
    /**
     * 取静态资源路径
     * @param {String} name 图标名
     * @returns {String} 完整路径
     */
    icon(name)
    {
      return `${ASSET_BASE}/icon/${name}.svg`
    },

    /**
     * 取原版素材路径
     * @param {String} name 素材名
     * @returns {String} 完整路径
     */
    native(name)
    {
      return `${ASSET_BASE}/ui/native/${name}.png`
    },

    /** 注入原版方正粗楷字体，仅标题使用 */
    injectFont()
    {
      if (typeof document === 'undefined' || document.getElementById('mj-font'))
      {
        return
      }

      const style = document.createElement('style')

      style.id = 'mj-font'
      style.textContent = `@font-face{font-family:'MJ Kai';src:url('${ASSET_BASE}/font/kai.woff2') format('woff2');font-display:swap;}`
      document.head.appendChild(style)
    },

    /** 读取本地保存的签到与任务状态 */
    restoreLocal()
    {
      this.signed = getStore('mj_signed', []) || []
      this.claimed = getStore('mj_claimed', []) || []
      this.bean = getStore('mj_bean', 8128) || 8128
      this.diamond = getStore('mj_diamond', 36) || 36
      this.bgmOn = getStore('mj_bgm', true) !== false
      this.soundOn = getStore('mj_sound', true) !== false

      audio.setBgmEnabled(this.bgmOn)
      audio.setEnabled(this.soundOn)
    },

    /** 持久化资源与任务状态 */
    persist()
    {
      setStore('mj_signed', this.signed)
      setStore('mj_claimed', this.claimed)
      setStore('mj_bean', this.bean)
      setStore('mj_diamond', this.diamond)
    },

    /** 今日日期键 */
    todayKey()
    {
      const d = new Date()

      return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`
    },

    /** 初始化：连接、进大厅、拉资料与战绩 */
    async init()
    {
      this.busy = true
      this.busyText = '连接中…'

      try
      {
        await this.ensureSocket()
        await this.enterLobby()

        if (this.bgmOn)
        {
          audio.playBgm()
        }

        this.refreshProfile()
      }
      catch (err)
      {
        this.toast(err.message || '连接失败')
      }
      finally
      {
        this.busy = false
      }
    },

    /** 建立长连接，已连接则复用 */
    async ensureSocket()
    {
      if (socket.connected)
      {
        return
      }

      await socket.connect(getToken())
    },

    /** 进入大厅并刷新快照 */
    async enterLobby()
    {
      const res = await socket.request('mahjong.lobby.enter')

      this.applyState(res)
    },

    /**
     * 应用大厅快照
     * @param {Object} state 含 profile、rooms、plays
     */
    applyState(state)
    {
      if (!state)
      {
        return
      }

      if (state.profile)
      {
        this.profile = {
          uid: state.profile.uid || this.profile.uid,
          nick: state.profile.nick || this.profile.nick,
          score: state.profile.score || 0,
          avatar: state.profile.avatar || ''
        }

        setUser({ ...getUser(), ...this.profile })
      }

      if (Array.isArray(state.rooms))
      {
        this.rooms = state.rooms
      }

      if (Array.isArray(state.plays) && state.plays.length)
      {
        this.plays = state.plays
      }
    },

    /** 拉取最新资料，用于刷新积分与段位 */
    async refreshProfile()
    {
      try
      {
        const res = await fetchProfile()

        if (res)
        {
          this.profile.nick = res.nick || this.profile.nick
          this.profile.score = res.score || 0
          this.profile.avatar = res.avatar || ''
          this.profile.uid = res.uid || this.profile.uid
          setUser({ ...getUser(), ...this.profile })
        }
      }
      catch (err)
      {
        console.warn('[mahjong] 资料拉取失败', err)
      }
    },

    /** 用战绩刷新任务进度 */
    async refreshTasks()
    {
      try
      {
        const list = await fetchRecords()

        this.records = list || []

        const total = this.records.length
        const wins = this.records.filter((r) => Number(r.score) > 0).length

        this.tasks[0].now = Math.min(total, 1)
        this.tasks[1].now = Math.min(total, 3)
        this.tasks[2].now = Math.min(wins, 1)
      }
      catch (err)
      {
        console.warn('[mahjong] 战绩拉取失败', err)
      }
    },

    /**
     * 选择场次
     * @param {Number} index 场次下标
     */
    pickRank(index)
    {
      this.pickedRank = index
      audio.play('click')
    },

    /**
     * 点击玩法卡：已接入的玩法直接切换，其余提示筹备中
     * @param {Object} item 玩法卡
     */
    pickPlay(item)
    {
      audio.play('click')

      if (item.sheet)
      {
        this.openSheet(item.sheet)
        return
      }

      if (item.todo)
      {
        this.todoText = item.todo
        this.openSheet('todo')
        return
      }

      const named = this.plays.findIndex((p) => p.name === item.play)
      const index = named >= 0 ? named : 0

      this.pickedPlay = index
      this.toast(`已选择 ${item.play}`)
    },

    /**
     * 切换换三张
     * @param {Object} e 事件对象
     */
    onSwapChange(e)
    {
      this.swap3 = e.detail.value
      audio.play('click')
    },

    /**
     * 打开弹层
     * @param {String} key 弹层标识
     */
    openSheet(key)
    {
      audio.play('click')

      if (key === 'activity' || key === 'live' || key === 'more' || key === 'mine')
      {
        const text = {
          activity: '福利活动页在 App 内为运营位，H5 版以签到替代',
          live: '直播观战暂未开放，可先进入好友房观战',
          more: '更多玩法陆续开放，先来一局血流换三张',
          mine: '背包在 App 内为服饰与道具仓库，H5 版暂未开放'
        }

        this.todoText = text[key]
        this.sheet = 'todo'
        return
      }

      this.sheet = key

      if (key === 'records')
      {
        this.refreshTasks()
      }

      if (key === 'join')
      {
        this.refreshRooms()
      }
    },

    /** 关闭弹层 */
    closeSheet()
    {
      audio.play('click')
      this.sheet = ''
    },

    /** 刷新在线房间 */
    async refreshRooms()
    {
      try
      {
        const res = await socket.request('mahjong.lobby.list')

        this.rooms = res.rooms || []
      }
      catch (err)
      {
        console.warn('[mahjong] 房间列表刷新失败', err)
      }
    },

    /** 快速开局：按当前场次与玩法直接匹配 */
    async quickStart()
    {
      if (this.busy)
      {
        return
      }

      audio.play('click')

      const play = this.plays[this.pickedPlay] || {}

      this.busy = true
      this.busyText = '正在开桌…'

      try
      {
        await this.ensureSocket()

        const res = await socket.request('mahjong.lobby.quickStart',
        {
          base: this.currentRank.base,
          rounds: 4,
          swap3: play.swap3 !== false,
          bots: 3
        })

        this.goTable(res.roomId)
      }
      catch (err)
      {
        this.toast(err.message || '开局失败')
      }
      finally
      {
        this.busy = false
      }
    },

    /** 创建好友房并入座 */
    async createRoom()
    {
      if (this.busy)
      {
        return
      }

      audio.play('click')

      const play = this.plays[this.pickedPlay] || {}

      this.busy = true
      this.busyText = '正在创建房间…'

      try
      {
        await this.ensureSocket()

        const res = await socket.request('mahjong.lobby.createRoom',
        {
          base: this.currentRank.base,
          rounds: this.rounds,
          swap3: this.swap3 && play.swap3 !== false,
          bots: 0
        })

        this.sheet = ''
        this.goTable(res.roomId)
      }
      catch (err)
      {
        this.toast(err.message || '创建失败')
      }
      finally
      {
        this.busy = false
      }
    },

    /** 按房号加入 */
    async joinByCode()
    {
      const code = String(this.roomCode || '').trim()

      if (code.length !== 6)
      {
        this.toast('请输入 6 位房号')
        return
      }

      await this.joinRoom({ roomId: code })
    },

    /**
     * 加入房间
     * @param {Object} room 房间信息
     */
    async joinRoom(room)
    {
      if (this.busy)
      {
        return
      }

      audio.play('click')

      this.busy = true
      this.busyText = '正在进入房间…'

      try
      {
        await this.ensureSocket()

        const res = await socket.request('mahjong.lobby.joinRoom', { roomId: room.roomId })

        this.sheet = ''
        this.goTable(res.roomId || room.roomId)
      }
      catch (err)
      {
        this.toast(err.message || '进入房间失败')
      }
      finally
      {
        this.busy = false
      }
    },

    /**
     * 跳转牌桌
     * @param {String} roomId 房间号
     */
    goTable(roomId)
    {
      audio.play('dice')
      uni.navigateTo({ url: `/pages/mahjong/table?roomId=${roomId}` })
    },

    /**
     * 签到：按已签天数顺序领取当格奖励
     * @param {Number} index 第几天
     */
    doSign(index)
    {
      const key = this.todayKey()

      if (this.signed.includes(key))
      {
        this.toast('今天已经签过啦')
        return
      }

      const day = this.signDays[index]

      this.signed.push(key)

      if (day.icon === 'bean')
      {
        this.bean += day.amount
      }
      else
      {
        this.diamond += day.amount
      }

      this.persist()
      audio.play('win')
      this.toast(`签到成功，获得 ${day.amount} ${day.icon === 'bean' ? '豆子' : '钻石'}`)
    },

    /**
     * 签到格样式
     * @param {Number} index 下标
     */
    signState(index)
    {
      return this.signDone(index) ? 'sign sign--done' : 'sign'
    },

    /**
     * 该格是否已领取
     * @param {Number} index 下标
     */
    signDone(index)
    {
      return index < this.signProgress
    },

    /**
     * 领取任务奖励
     * @param {Object} item 任务
     */
    claimTask(item)
    {
      if (item.claimed)
      {
        this.toast('该奖励已领取')
        return
      }

      if (item.now < item.need)
      {
        this.toast('任务尚未完成')
        return
      }

      item.claimed = true
      this.claimed.push(item.id)
      this.bean += item.reward
      this.persist()
      audio.play('win')
      this.toast(`领取成功，获得 ${item.reward} 豆子`)
    },

    /**
     * 购买商品
     * @param {Object} item 商品
     */
    buy(item)
    {
      audio.play('click')
      this.toast('演示环境暂未接入支付')
    },

    /**
     * 切换底部导航
     * @param {Number} index 下标
     */
    switchTab(index)
    {
      this.pickedTab = index
      audio.play('click')

      const tab = this.tabs[index]

      this.openSheet(tab.key)
    },

    /**
     * 背景音乐开关
     * @param {Object} e 事件对象
     */
    onBgmChange(e)
    {
      this.bgmOn = e.detail.value
      setStore('mj_bgm', this.bgmOn)
      audio.setBgmEnabled(this.bgmOn)
      audio.play('click')
    },

    /**
     * 音效开关
     * @param {Object} e 事件对象
     */
    onSoundChange(e)
    {
      this.soundOn = e.detail.value
      setStore('mj_sound', this.soundOn)
      audio.setEnabled(this.soundOn)

      if (this.soundOn)
      {
        audio.play('click')
      }
    },

    /** 退出登录：弹页面内确认框（系统弹窗不跟随横屏旋转） */
    logout()
    {
      this.confirmVisible = true
    },

    /** 确认退出并回到登录页 */
    doLogout()
    {
      this.confirmVisible = false
      socket.destroy()
      clearAuth()
      uni.reLaunch({ url: '/pages/mahjong/login' })
    },

    /**
     * 轻提示
     * @param {String} text 文案
     */
    toast(text)
    {
      this.toastText = text

      clearTimeout(this.toastTimer)
      this.toastTimer = setTimeout(() =>
      {
        this.toastText = ''
      }, 1800)
    }
  }
}
</script>

<style lang="scss" scoped>
/* 夜景大厅：原版紫色夜景背景 + 金色 UI */
$gold: #FFD98A;
$gold-deep: #D9A44C;
$gold-line: rgba(255, 216, 138, 0.45);
$cream: #FFF3D6;
$glass: rgba(26, 18, 48, 0.78);
$glass-deep: rgba(20, 14, 38, 0.9);

.hall { position: relative; width: 100%; height: 100%; overflow: hidden; background: #17102B; }

/* ===== 背景 ===== */
.hall__bg { position: absolute; left: 0; top: 0; width: 100%; height: 100%; }

/* ===== 顶栏 ===== */
.topbar { position: relative; display: flex; flex-direction: row; align-items: center; padding: 14rpx 18rpx 0; z-index: 6; }
.tbn { position: relative; display: flex; align-items: center; justify-content: center; width: 64rpx; height: 64rpx; }
.tbn__ico { position: relative; width: 44rpx; height: 44rpx; filter: drop-shadow(0 2rpx 6rpx rgba(0, 0, 0, 0.6)); }
.tbn--round { width: 68rpx; height: 68rpx; margin-left: 6rpx; background: $glass; border: 1rpx solid $gold-line; border-radius: 50%; }
.tbn--round .tbn__ico { width: 38rpx; height: 38rpx; }
.tbn__dot { position: absolute; right: 8rpx; top: 8rpx; width: 14rpx; height: 14rpx; background: #FF5A4E; border: 2rpx solid #FFFFFF; border-radius: 50%; }

.user { position: relative; display: flex; flex-direction: row; align-items: center; margin-left: 10rpx; padding: 8rpx 22rpx 8rpx 10rpx; background: $glass; border: 1rpx solid $gold-line; border-radius: 40rpx; }
.user__frame { position: relative; width: 76rpx; height: 76rpx; background: linear-gradient(160deg, #FFE9AE 0%, #D9A44C 100%); border-radius: 50%; padding: 3rpx; box-sizing: border-box; }
.user__face { position: relative; width: 100%; height: 100%; border-radius: 50%; }
.user__lv { position: absolute; left: 50%; bottom: -6rpx; display: flex; align-items: center; justify-content: center; min-width: 34rpx; height: 26rpx; padding: 0 6rpx; box-sizing: border-box; font-size: 16rpx; font-weight: 700; color: #5A3A06; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border-radius: 13rpx; transform: translateX(-50%); }
.user__meta { position: relative; display: flex; flex-direction: column; flex-shrink: 0; margin-left: 14rpx; }
.user__nick { position: relative; max-width: 200rpx; overflow: hidden; font-size: 26rpx; font-weight: 600; color: $cream; text-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.6); }
.user__tags { position: relative; display: flex; flex-direction: row; align-items: center; margin-top: 4rpx; white-space: nowrap; }
.tag { position: relative; flex-shrink: 0; display: inline-block; padding: 1rpx 10rpx; margin-right: 8rpx; font-size: 17rpx; line-height: 24rpx; white-space: nowrap; border-radius: 8rpx; }
.tag--rank { color: #5A3A06; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); }
.tag--lv { color: $cream; background: rgba(84, 96, 220, 0.55); }
.topbar__fill { position: relative; flex: 1; }

.res { position: relative; display: flex; flex-direction: row; align-items: center; height: 56rpx; margin-left: 14rpx; padding: 0 10rpx 0 6rpx; background: $glass-deep; border: 1rpx solid $gold-line; border-radius: 30rpx; }
.res__ico { position: relative; width: 40rpx; height: 40rpx; }
.res__num { position: relative; min-width: 86rpx; margin: 0 8rpx; font-size: 24rpx; font-weight: 600; color: $cream; text-align: right; text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.6); }
.res__add { position: relative; width: 32rpx; height: 32rpx; }

/* ===== 左侧好友列 ===== */
.friends { position: absolute; left: 0.4%; top: 14%; display: flex; flex-direction: column; align-items: center; z-index: 5; }
.friend { position: relative; display: flex; flex-direction: column; align-items: center; width: 72rpx; margin-bottom: 14rpx; }
.friend__frame { position: relative; width: 68rpx; height: 68rpx; background: linear-gradient(160deg, #FFE9AE 0%, #D9A44C 100%); border: 2rpx solid rgba(255, 233, 174, 0.8); border-radius: 16rpx; box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.5); }
.friend__face { position: relative; width: 100%; height: 100%; font-size: 28rpx; font-weight: 700; color: #FFFFFF; text-align: center; line-height: 60rpx; }
.friend__crown { position: absolute; right: -8rpx; top: -12rpx; width: 30rpx; height: 30rpx; }
.friend__crown-ico { position: relative; width: 100%; height: 100%; }
.friend__name { position: relative; max-width: 72rpx; margin-top: 4rpx; overflow: hidden; font-size: 17rpx; color: $cream; white-space: nowrap; text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.8); }
.friend__dot { position: absolute; left: 50rpx; top: 50rpx; width: 14rpx; height: 14rpx; background: #52E08A; border: 2rpx solid #FFFFFF; border-radius: 50%; }
.friends__invite { position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 68rpx; height: 54rpx; margin-top: 2rpx; background: $glass; border: 1rpx dashed $gold-line; border-radius: 12rpx; }
.friends__invite-text { position: relative; font-size: 16rpx; color: $gold; line-height: 19rpx; }

/* ===== 圆形入口列 ===== */
.entries { position: absolute; left: 8.6%; top: 14%; display: flex; flex-direction: column; align-items: center; z-index: 5; }
.entry { position: relative; display: flex; flex-direction: column; align-items: center; margin-bottom: 14rpx; }
.entry__btn { position: relative; display: flex; align-items: center; justify-content: center; width: 76rpx; height: 76rpx; filter: drop-shadow(0 6rpx 12rpx rgba(0, 0, 0, 0.5)); }
.entry__bg { position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: 50%; }
.entry__ico { position: relative; width: 38rpx; height: 38rpx; }
.entry__dot { position: absolute; right: 2rpx; top: -2rpx; width: 16rpx; height: 16rpx; background: #FF5A4E; border: 2rpx solid #FFFFFF; border-radius: 50%; z-index: 2; }
.entry__label { position: relative; padding: 1rpx 10rpx; margin-top: 2rpx; font-size: 15rpx; color: $cream; white-space: nowrap; background: rgba(20, 14, 38, 0.72); border-radius: 8rpx; }

/* ===== 中央角色 ===== */
.hero__shadow { position: absolute; left: 28%; bottom: 13%; width: 300rpx; height: 44rpx; background: radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0.45) 0%, rgba(0, 0, 0, 0) 70%); z-index: 2; }
.hero { position: absolute; left: 26.5%; bottom: 14%; width: 330rpx; height: 560rpx; z-index: 3; filter: drop-shadow(0 10rpx 24rpx rgba(0, 0, 0, 0.5)); }

/* ===== 发仔 ===== */
.penpen { position: absolute; left: 21%; bottom: 15%; display: flex; flex-direction: column; align-items: center; z-index: 4; }
.penpen__bubble { position: relative; padding: 10rpx 22rpx; background: rgba(255, 252, 244, 0.95); border: 2rpx solid #FFFFFF; border-radius: 22rpx; box-shadow: 0 6rpx 16rpx rgba(0, 0, 0, 0.4); animation: bob 2.6s ease-in-out infinite; }
.penpen__bubble-text { position: relative; font-size: 20rpx; color: #7A4A10; white-space: nowrap; }
.penpen__img { position: relative; width: 176rpx; height: 130rpx; margin-top: -4rpx; filter: drop-shadow(0 8rpx 16rpx rgba(0, 0, 0, 0.55)); }
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8rpx); } }

/* ===== 玩法卡 ===== */
.plays { position: absolute; right: 20%; top: 12%; display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; width: 37%; z-index: 5; }
.play { position: relative; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; width: 32.5%; margin-bottom: 12rpx; padding: 14rpx 12rpx; background: linear-gradient(165deg, rgba(64, 44, 110, 0.85) 0%, rgba(34, 22, 66, 0.9) 100%); border: 2rpx solid $gold-line; border-radius: 18rpx; box-shadow: 0 10rpx 24rpx rgba(0, 0, 0, 0.45), inset 0 1rpx 0 rgba(255, 233, 174, 0.25); }
.play--red { background: linear-gradient(165deg, rgba(168, 62, 52, 0.88) 0%, rgba(96, 26, 34, 0.92) 100%); border-color: rgba(255, 196, 120, 0.55); }
.play--cyan { background: linear-gradient(165deg, rgba(38, 110, 148, 0.88) 0%, rgba(18, 56, 92, 0.92) 100%); border-color: rgba(140, 214, 255, 0.4); }
.play--gold { background: linear-gradient(165deg, rgba(150, 112, 40, 0.9) 0%, rgba(94, 62, 20, 0.92) 100%); }
.play__body { position: relative; display: flex; flex-direction: row; align-items: flex-start; }
.play__chars { position: relative; display: flex; flex-direction: column; }
.play__char { position: relative; font-family: 'MJ Kai', 'PingFang SC', serif; font-size: 44rpx; font-weight: 700; line-height: 52rpx; color: #FFF6DC; text-shadow: 0 3rpx 8rpx rgba(0, 0, 0, 0.6); }
.play__tail { position: relative; margin: 6rpx 0 0 10rpx; font-size: 20rpx; color: rgba(255, 243, 214, 0.85); writing-mode: vertical-rl; letter-spacing: 4rpx; }
.play__foot { position: relative; display: flex; flex-direction: row; align-items: center; }
.play__fire { position: relative; width: 24rpx; height: 24rpx; }
.play__num { position: relative; margin-left: 6rpx; font-size: 19rpx; color: #FFD98A; }
.play__lock { position: relative; display: flex; }
.play__lock-ico { position: relative; width: 26rpx; height: 26rpx; opacity: 0.7; }

/* ===== 更多玩法 ===== */
.more { position: absolute; right: 20.5%; top: 63.5%; padding: 6rpx 18rpx; background: linear-gradient(180deg, #8A6BDF 0%, #5E44B8 100%); border: 1rpx solid rgba(255, 255, 255, 0.35); border-radius: 20rpx 20rpx 20rpx 4rpx; box-shadow: 0 6rpx 16rpx rgba(40, 20, 90, 0.5); z-index: 5; }
.more__text { position: relative; font-size: 20rpx; color: #FFF6DC; }

/* ===== 活动条 ===== */
.banner { position: absolute; right: 1.6%; bottom: 58%; display: flex; flex-direction: row; align-items: center; width: 300rpx; height: 88rpx; padding: 0 14rpx; box-sizing: border-box; border-radius: 16rpx; overflow: hidden; z-index: 5; }
.banner__bg { position: absolute; left: 0; top: 0; width: 100%; height: 100%; }
.banner__ico { position: relative; width: 40rpx; height: 40rpx; z-index: 1; }
.banner__text { position: relative; flex: 1; margin-left: 10rpx; font-size: 22rpx; font-weight: 600; color: #FFF6DC; text-shadow: 0 2rpx 6rpx rgba(80, 20, 0, 0.7); z-index: 1; }
.banner__go { position: relative; display: flex; align-items: center; justify-content: center; width: 52rpx; height: 40rpx; background: #FFF6DC; border-radius: 20rpx; z-index: 1; }
.banner__go-text { position: relative; font-size: 20rpx; font-weight: 700; color: #C0392B; }

/* ===== 场次 ===== */
.ranks { position: absolute; right: 1.6%; bottom: 31%; display: flex; flex-direction: row; flex-wrap: wrap; justify-content: flex-end; width: 344rpx; z-index: 5; }
.rank { position: relative; display: flex; align-items: center; justify-content: center; width: 150rpx; height: 52rpx; margin: 0 0 10rpx 16rpx; background: $glass; border: 1rpx solid rgba(255, 216, 138, 0.25); border-radius: 26rpx; }
.rank--on { position: relative; display: flex; align-items: center; justify-content: center; width: 150rpx; height: 52rpx; margin: 0 0 10rpx 16rpx; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border: 1rpx solid #FFFFFF; border-radius: 26rpx; box-shadow: 0 6rpx 16rpx rgba(240, 184, 86, 0.4); }
.rank__text { position: relative; font-size: 22rpx; color: rgba(255, 243, 214, 0.85); }
.rank--on .rank__text { color: #5A3A06; font-weight: 700; }

/* ===== 快速开始 ===== */
.start { position: absolute; right: 1.6%; bottom: 14%; z-index: 6; }
.start__glow { position: absolute; left: 50%; top: 50%; width: 400rpx; height: 200rpx; margin: -100rpx 0 0 -200rpx; background: radial-gradient(ellipse, rgba(255, 200, 90, 0.5) 0%, rgba(255, 200, 90, 0) 70%); animation: pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { opacity: 0.7; transform: scale(1); } 50% { opacity: 1; transform: scale(1.08); } }
.start__bg { position: relative; width: 300rpx; height: 128rpx; filter: drop-shadow(0 8rpx 20rpx rgba(0, 0, 0, 0.5)); }
.start__btn { position: absolute; left: 0; top: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 300rpx; height: 128rpx; }
.start__title { position: relative; font-family: 'MJ Kai', 'PingFang SC', serif; font-size: 42rpx; font-weight: 700; color: #6B3A05; text-shadow: 0 2rpx 0 rgba(255, 255, 255, 0.5); }
.start__sub { position: relative; margin-top: 2rpx; font-size: 19rpx; color: rgba(107, 58, 5, 0.75); }

/* ===== 底部导航 ===== */
.dock { position: absolute; left: 0; bottom: 0; display: flex; flex-direction: row; align-items: center; justify-content: space-around; width: 100%; height: 100rpx; z-index: 6; }
.dock__bg { position: absolute; left: 0; bottom: 0; width: 100%; height: 100%; }
.dock__item { position: relative; display: flex; flex-direction: column; align-items: center; }
.dock__icon-wrap { position: relative; }
.dock__icon { position: relative; width: 44rpx; height: 44rpx; filter: drop-shadow(0 2rpx 6rpx rgba(0, 0, 0, 0.7)); }
.dock__dot { position: absolute; right: -6rpx; top: -4rpx; width: 14rpx; height: 14rpx; background: #FF5A4E; border: 2rpx solid #FFFFFF; border-radius: 50%; }
.dock__text { position: relative; margin-top: 2rpx; font-size: 19rpx; color: rgba(255, 243, 214, 0.6); text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.8); }
.dock__text--on { color: $gold; font-weight: 700; }

/* ===== 弹层：夜色玻璃 ===== */
.mj-mask { position: absolute; left: 0; top: 0; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; background: rgba(8, 4, 20, 0.72); z-index: 30; }
.panel { position: relative; display: flex; flex-direction: column; width: 900rpx; max-height: 88%; padding: 30rpx 28rpx 28rpx; background: linear-gradient(170deg, rgba(52, 38, 92, 0.96) 0%, rgba(28, 18, 56, 0.96) 100%); border: 2rpx solid $gold-line; border-radius: 26rpx; box-shadow: 0 24rpx 60rpx rgba(0, 0, 0, 0.6), inset 0 1rpx 0 rgba(255, 233, 174, 0.2); }
.panel--tall { height: 84%; }
.panel__head { position: relative; display: flex; flex-direction: row; align-items: center; justify-content: space-between; margin-bottom: 14rpx; }
.panel__title { position: relative; font-family: 'MJ Kai', 'PingFang SC', serif; font-size: 38rpx; color: $gold; letter-spacing: 4rpx; text-shadow: 0 2rpx 10rpx rgba(240, 184, 86, 0.4); }
.panel__close { position: absolute; right: 0; top: 2rpx; width: 36rpx; height: 36rpx; opacity: 0.85; }
.panel__body { position: relative; flex: 1; min-height: 0; overflow-y: auto; }
.panel__tip { position: relative; display: block; margin-bottom: 16rpx; font-size: 22rpx; color: rgba(255, 243, 214, 0.6); }
.panel__ok { position: relative; display: flex; align-items: center; justify-content: center; height: 88rpx; margin-top: 22rpx; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 60%, #E0A442 100%); border: 2rpx solid #FFFFFF; border-radius: 44rpx; box-shadow: 0 8rpx 0 #B07E20, 0 14rpx 26rpx rgba(0, 0, 0, 0.45); }
.panel__ok-text { position: relative; font-size: 30rpx; font-weight: 700; color: #6B3A05; letter-spacing: 4rpx; }
.panel__ok--ghost { margin-top: 20rpx; background: rgba(255, 255, 255, 0.08); border: 1rpx solid $gold-line; box-shadow: none; }
.panel__ok-text--ghost { color: $gold; }
.panel__ver { position: relative; display: block; margin-top: 18rpx; font-size: 20rpx; color: rgba(255, 243, 214, 0.4); text-align: center; }

/* 表单 */
.field__label { position: relative; display: block; margin: 16rpx 0 12rpx; font-size: 24rpx; font-weight: 600; color: $gold; }
.chips { position: relative; display: flex; flex-direction: row; flex-wrap: wrap; }
.chip { position: relative; display: flex; align-items: center; justify-content: center; min-width: 140rpx; height: 64rpx; padding: 0 22rpx; margin: 0 12rpx 12rpx 0; background: rgba(255, 255, 255, 0.08); border: 1rpx solid rgba(255, 216, 138, 0.3); border-radius: 12rpx; }
.chip--on { background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border-color: #FFFFFF; }
.chip__text { position: relative; font-size: 24rpx; color: $cream; }
.chip--on .chip__text { color: #6B3A05; font-weight: 700; }
.switch-row { position: relative; display: flex; flex-direction: row; align-items: center; justify-content: space-between; height: 86rpx; margin-top: 8rpx; border-top: 1rpx solid rgba(255, 216, 138, 0.16); }
.switch-row__label { position: relative; font-size: 26rpx; color: $cream; }

/* 房号 */
.code { position: relative; display: flex; flex-direction: row; align-items: center; margin-bottom: 8rpx; }
.code__input { position: relative; flex: 1; height: 84rpx; padding: 0 22rpx; font-size: 30rpx; color: $gold; letter-spacing: 6rpx; background: rgba(0, 0, 0, 0.32); border: 1rpx solid $gold-line; border-radius: 14rpx; }
.code__ph { color: rgba(255, 243, 214, 0.32); font-size: 24rpx; letter-spacing: 0; }
.code__btn { position: relative; display: flex; align-items: center; justify-content: center; width: 160rpx; height: 84rpx; margin-left: 16rpx; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border-radius: 14rpx; }
.code__btn-text { position: relative; font-size: 28rpx; font-weight: 700; color: #6B3A05; }

/* 房间列表 */
.room-list { position: relative; height: 480rpx; }
.room { position: relative; display: flex; flex-direction: row; align-items: center; justify-content: space-between; height: 104rpx; margin-bottom: 12rpx; padding: 0 20rpx; background: rgba(255, 255, 255, 0.07); border: 1rpx solid rgba(255, 216, 138, 0.2); border-radius: 14rpx; }
.room__info { position: relative; display: flex; flex-direction: column; }
.room__id { position: relative; font-size: 26rpx; color: $gold; }
.room__meta { position: relative; margin-top: 4rpx; font-size: 20rpx; color: rgba(255, 243, 214, 0.55); }
.room__act { position: relative; font-size: 26rpx; font-weight: 600; color: #6B3A05; padding: 8rpx 24rpx; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border-radius: 24rpx; }
.empty { position: relative; display: flex; align-items: center; justify-content: center; padding: 60rpx 0; }
.empty__text { position: relative; font-size: 22rpx; color: rgba(255, 243, 214, 0.5); text-align: center; }

/* 商城 */
.shop-tabs { position: relative; display: flex; flex-direction: row; margin-bottom: 16rpx; border-radius: 12rpx; overflow: hidden; }
.shop-tab { position: relative; flex: 1; display: flex; align-items: center; justify-content: center; height: 68rpx; background: rgba(255, 255, 255, 0.08); }
.shop-tab--on { background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); }
.shop-tab__text { position: relative; font-size: 24rpx; color: rgba(255, 243, 214, 0.8); }
.shop-tab--on .shop-tab__text { color: #6B3A05; font-weight: 700; }
.goods { position: relative; display: flex; flex-direction: row; align-items: center; justify-content: space-between; height: 128rpx; margin-bottom: 14rpx; padding: 0 20rpx; background: rgba(255, 255, 255, 0.07); border: 1rpx solid rgba(255, 216, 138, 0.2); border-radius: 16rpx; }
.goods__left { position: relative; display: flex; flex-direction: row; align-items: center; }
.goods__icon { position: relative; width: 64rpx; height: 64rpx; }
.goods__text { position: relative; display: flex; flex-direction: column; margin-left: 16rpx; }
.goods__name { position: relative; font-size: 26rpx; font-weight: 600; color: $cream; }
.goods__desc { position: relative; margin-top: 4rpx; font-size: 20rpx; color: rgba(255, 243, 214, 0.5); }
.goods__btn { position: relative; display: flex; align-items: center; justify-content: center; min-width: 130rpx; height: 60rpx; padding: 0 20rpx; box-sizing: border-box; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border-radius: 30rpx; }
.goods__price { position: relative; font-size: 24rpx; font-weight: 700; color: #6B3A05; }

/* 签到 */
.sign-grid { position: relative; display: flex; flex-direction: row; flex-wrap: wrap; }
.sign { position: relative; display: flex; flex-direction: column; align-items: center; width: 178rpx; height: 196rpx; margin: 0 14rpx 16rpx 0; padding-top: 16rpx; box-sizing: border-box; background: rgba(255, 255, 255, 0.07); border: 1rpx solid rgba(255, 216, 138, 0.25); border-radius: 14rpx; }
.sign--done { background: rgba(240, 184, 86, 0.16); border-color: rgba(255, 216, 138, 0.5); opacity: 0.75; }
.sign__day { position: relative; font-size: 20rpx; color: rgba(255, 243, 214, 0.65); }
.sign__icon { position: relative; width: 52rpx; height: 52rpx; margin-top: 10rpx; }
.sign__num { position: relative; margin-top: 8rpx; font-size: 22rpx; font-weight: 600; color: $gold; }
.sign__state { position: relative; margin-top: 10rpx; padding: 4rpx 20rpx; font-size: 20rpx; color: #6B3A05; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border-radius: 18rpx; }

/* 任务 */
.task { position: relative; display: flex; flex-direction: row; align-items: center; justify-content: space-between; height: 132rpx; margin-bottom: 14rpx; padding: 0 20rpx; background: rgba(255, 255, 255, 0.07); border: 1rpx solid rgba(255, 216, 138, 0.2); border-radius: 16rpx; }
.task__left { position: relative; flex: 1; margin-right: 20rpx; }
.task__name { position: relative; font-size: 26rpx; color: $cream; }
.task__bar { position: relative; width: 100%; height: 10rpx; margin-top: 12rpx; overflow: hidden; background: rgba(0, 0, 0, 0.4); border-radius: 5rpx; }
.task__fill { position: relative; width: 0; height: 100%; background: linear-gradient(90deg, #F0B856 0%, #FFE9AE 100%); border-radius: 5rpx; }
.task__progress { position: relative; margin-top: 8rpx; font-size: 20rpx; color: rgba(255, 243, 214, 0.5); }
.task__btn { position: relative; display: flex; align-items: center; justify-content: center; width: 120rpx; height: 62rpx; background: rgba(255, 255, 255, 0.1); border: 1rpx solid $gold-line; border-radius: 31rpx; }
.task__btn--on { background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border-color: #FFFFFF; }
.task__btn-text { position: relative; font-size: 22rpx; color: rgba(255, 243, 214, 0.75); }
.task__btn--on .task__btn-text { color: #6B3A05; font-weight: 700; }

/* 排行 */
.rank-row { position: relative; display: flex; flex-direction: row; align-items: center; height: 94rpx; border-bottom: 1rpx solid rgba(255, 216, 138, 0.14); }
.rank-row__no { position: relative; width: 54rpx; font-size: 24rpx; color: rgba(255, 243, 214, 0.55); text-align: center; }
.rank-row__no--top { color: #FFD86B; font-weight: 700; }
.rank-row__avatar { position: relative; width: 60rpx; height: 60rpx; margin-left: 12rpx; border-radius: 50%; border: 1rpx solid $gold-line; }
.rank-row__name { position: relative; flex: 1; margin-left: 16rpx; font-size: 26rpx; color: $cream; }
.rank-row__score { position: relative; font-size: 26rpx; font-weight: 600; color: $gold; }

/* 战绩 */
.record { position: relative; display: flex; flex-direction: row; align-items: center; justify-content: space-between; height: 96rpx; border-bottom: 1rpx solid rgba(255, 216, 138, 0.14); }
.record__left { position: relative; display: flex; flex-direction: column; }
.record__room { position: relative; font-size: 26rpx; color: $cream; }
.record__time { position: relative; margin-top: 4rpx; font-size: 20rpx; color: rgba(255, 243, 214, 0.45); }
.record__score { position: relative; font-size: 30rpx; font-weight: 700; color: #7BE3A5; }
.record__score--win { color: #FF8A7A; }

/* 提示 / 确认 / 等待 */
.toast { position: absolute; left: 50%; bottom: 320rpx; transform: translateX(-50%); padding: 18rpx 34rpx; background: rgba(20, 14, 38, 0.92); border: 1rpx solid $gold-line; border-radius: 34rpx; z-index: 40; }
.toast__text { position: relative; font-size: 24rpx; color: $gold; }
.confirm { position: absolute; left: 0; top: 0; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; background: rgba(8, 4, 20, 0.72); z-index: 45; }
.confirm__card { position: relative; display: flex; flex-direction: column; align-items: center; width: 480rpx; padding: 40rpx 34rpx 34rpx; background: linear-gradient(170deg, rgba(52, 38, 92, 0.97) 0%, rgba(28, 18, 56, 0.97) 100%); border: 2rpx solid $gold-line; border-radius: 26rpx; }
.confirm__title { position: relative; font-family: 'MJ Kai', 'PingFang SC', serif; font-size: 34rpx; color: $gold; }
.confirm__text { position: relative; margin-top: 18rpx; font-size: 26rpx; color: $cream; }
.confirm__btns { position: relative; display: flex; flex-direction: row; width: 100%; margin-top: 32rpx; }
.confirm__btn { position: relative; display: flex; align-items: center; justify-content: center; flex: 1; height: 84rpx; background: linear-gradient(180deg, #FFE9AE 0%, #F0B856 100%); border-radius: 42rpx; }
.confirm__btn--ghost { margin-right: 20rpx; background: rgba(255, 255, 255, 0.08); border: 1rpx solid $gold-line; }
.confirm__btn-text { position: relative; font-size: 28rpx; font-weight: 700; color: #6B3A05; }
.confirm__btn-text--ghost { color: $gold; }
.loading { position: absolute; left: 0; top: 0; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; background: rgba(8, 4, 20, 0.6); z-index: 50; }
.loading__text { position: relative; padding: 24rpx 44rpx; font-size: 28rpx; color: $gold; background: rgba(20, 14, 38, 0.92); border: 1rpx solid $gold-line; border-radius: 20rpx; }
</style>
