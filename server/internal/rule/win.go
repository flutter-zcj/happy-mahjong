package rule

// CanWin 判断手牌在已有 meldCount 个明面子时是否成胡。
//
// 血战到底的胡牌结构只有两种：
//   - 标准型：4 个面子 + 1 对将（面子可为顺子或刻子）
//   - 七对：7 个对子（仅在无明面子时成立，四张相同算两对，即龙七对）
func CanWin(c Counts, meldCount int) bool {
	if meldCount < 0 || meldCount > 4 {
		return false
	}

	needMelds := 4 - meldCount
	if c.Total() != needMelds*3+2 {
		return false
	}

	if meldCount == 0 && IsSevenPairs(c) {
		return true
	}

	for t := TileMin; t <= TileMax; t++ {
		if c[t] < 2 {
			continue
		}

		c[t] -= 2
		ok := canFormMelds(&c, needMelds)
		c[t] += 2

		if ok {
			return true
		}
	}

	return false
}

// IsSevenPairs 判断是否为七对（含龙七对：四张相同算两对）。
func IsSevenPairs(c Counts) bool {
	if c.Total() != 14 {
		return false
	}

	pairs := 0

	for t := TileMin; t <= TileMax; t++ {
		if c[t]%2 != 0 {
			return false
		}

		pairs += c[t] / 2
	}

	return pairs == 7
}

// canFormMelds 判断剩余牌能否刚好拆成 need 个面子。
func canFormMelds(c *Counts, need int) bool {
	if need == 0 {
		return c.Total() == 0
	}

	first := 0

	for t := TileMin; t <= TileMax; t++ {
		if c[t] > 0 {
			first = t

			break
		}
	}

	if first == 0 {
		return false
	}

	if c[first] >= 3 {
		c[first] -= 3
		ok := canFormMelds(c, need-1)
		c[first] += 3

		if ok {
			return true
		}
	}

	if first+2 <= TileMax && Suit(first) == Suit(first+2) && c[first+1] > 0 && c[first+2] > 0 {
		c[first]--
		c[first+1]--
		c[first+2]--
		ok := canFormMelds(c, need-1)
		c[first]++
		c[first+1]++
		c[first+2]++

		if ok {
			return true
		}
	}

	return false
}

// TingList 返回当前手牌（3n+1 张）的听牌列表，升序去重。
func TingList(c Counts, meldCount int) []int {
	out := make([]int, 0, 9)

	for t := TileMin; t <= TileMax; t++ {
		if c[t] >= CopiesPerTile {
			continue
		}

		c[t]++

		if CanWin(c, meldCount) {
			out = append(out, t)
		}

		c[t]--
	}

	return out
}

// IsTing 判断手牌是否已听牌。
func IsTing(c Counts, meldCount int) bool {
	return len(TingList(c, meldCount)) > 0
}

// CanPeng 判断能否碰。
func CanPeng(c Counts, t int) bool {
	return t >= TileMin && t <= TileMax && c[t] >= 2
}

// CanMingGang 判断能否明杠他家弃牌。
func CanMingGang(c Counts, t int) bool {
	return t >= TileMin && t <= TileMax && c[t] >= 3
}

// AnGangTiles 返回可暗杠的牌。
func AnGangTiles(c Counts) []int {
	out := make([]int, 0, 4)

	for t := TileMin; t <= TileMax; t++ {
		if c[t] == CopiesPerTile {
			out = append(out, t)
		}
	}

	return out
}

// BuGangTiles 返回可补杠的牌（已碰且手上还有一张）。
func BuGangTiles(c Counts, melds []Meld) []int {
	out := make([]int, 0, 4)

	for _, m := range melds {
		if m.Type == MeldPeng && c[m.Tile] > 0 {
			out = append(out, m.Tile)
		}
	}

	return out
}

// AllTiles 汇总手牌与面子的全部牌，用于清一色、带幺九等判断。
func AllTiles(c Counts, melds []Meld) []int {
	out := c.Tiles()

	for _, m := range melds {
		n := 3
		if m.IsGang() {
			n = 4
		}

		for i := 0; i < n; i++ {
			out = append(out, m.Tile)
		}
	}

	return out
}
