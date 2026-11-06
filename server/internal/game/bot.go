package game

import (
	"github.com/zbcx/mahjong/internal/rule"
)

// BotQue 机器人的定缺选择：选手上张数最少的花色。
func (g *Game) BotQue(seat int) int {
	p := g.Players[seat]
	counts := [rule.SuitCount]int{}

	for t := rule.TileMin; t <= rule.TileMax; t++ {
		if p.Hand[t] > 0 {
			counts[rule.Suit(t)] += p.Hand[t]
		}
	}

	best := 0

	for s := 1; s < rule.SuitCount; s++ {
		if counts[s] < counts[best] {
			best = s
		}
	}

	return best
}

// BotSwap 机器人的换三张选择：取张数最多花色的三张。
func (g *Game) BotSwap(seat int) []int {
	p := g.Players[seat]
	bestSuit, bestCount := 0, -1

	for s := 0; s < rule.SuitCount; s++ {
		n := 0

		for t := rule.TileMin; t <= rule.TileMax; t++ {
			if p.Hand[t] > 0 && rule.Suit(t) == s {
				n += p.Hand[t]
			}
		}

		if n > bestCount {
			bestSuit, bestCount = s, n
		}
	}

	out := make([]int, 0, 3)

	for t := rule.TileMin; t <= rule.TileMax && len(out) < 3; t++ {
		for i := 0; i < p.Hand[t] && len(out) < 3; i++ {
			if rule.Suit(t) == bestSuit {
				out = append(out, t)
			}
		}
	}

	return out
}

// BotChoose 机器人决策：返回要执行的操作与牌。
//
// 策略刻意保守：能胡就胡，杠与碰按概率取舍，其余一律过，
// 目的是让单人练习局也能自然推进到结算。
func (g *Game) BotChoose(seat int) (string, int) {
	opts := g.pending[seat]

	for _, o := range opts {
		if o.Type == OpHu {
			return OpHu, o.Tile
		}
	}

	if seat == g.Turn && g.needDiscard {
		for _, o := range opts {
			if o.Type == OpAnGang && g.Rng.Float64() < 0.5 {
				return OpAnGang, o.Tile
			}
		}

		for _, o := range opts {
			if o.Type == OpBuGang {
				return OpBuGang, o.Tile
			}
		}

		return OpDiscard, g.suggestDiscard(g.Players[seat])
	}

	for _, o := range opts {
		if o.Type == OpGang && g.Rng.Float64() < 0.5 {
			return OpGang, o.Tile
		}
	}

	for _, o := range opts {
		if o.Type == OpPeng && g.Rng.Float64() < 0.6 {
			return OpPeng, o.Tile
		}
	}

	return OpPass, 0
}

// BotStep 执行一步机器人决策，返回是否有动作发生。
func (g *Game) BotStep(seat int) bool {
	op, tile := g.BotChoose(seat)

	switch op {
	case OpDiscard:
		if g.Turn != seat || !g.needDiscard {
			return false
		}

		g.Discard(seat, tile)

		return true
	case OpPass, OpHu, OpPeng, OpGang, OpAnGang, OpBuGang:
		g.Action(seat, op, tile)

		return true
	}

	return false
}
