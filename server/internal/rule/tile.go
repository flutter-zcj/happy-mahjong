// Package rule 实现四川血战到底麻将的牌面模型、胡牌判定与番型计算。
//
// 牌编码与客户端共享同一套整数约定，避免两侧各自维护映射表：
//
//	1..9    一万..九万
//	10..18  一筒..九筒
//	19..27  一条..九条
//
// 血战到底不使用字牌与花牌，整副牌为 108 张。
package rule

import (
	"fmt"
	"math/rand"
)

const (
	// TileMin 最小牌 id。
	TileMin = 1
	// TileMax 最大牌 id。
	TileMax = 27
	// SuitCount 花色数量：万、筒、条。
	SuitCount = 3
	// TileKinds 牌的种类数。
	TileKinds = 27
	// CopiesPerTile 每种牌的张数。
	CopiesPerTile = 4
	// WallSize 牌墙总张数。
	WallSize = TileKinds * CopiesPerTile
	// HandSize 起手张数。
	HandSize = 13
)

// Suit 返回牌的花色序号：0 万、1 筒、2 条。
func Suit(t int) int {
	if t < TileMin || t > TileMax {
		return -1
	}

	return (t - 1) / 9
}

// Rank 返回牌的点数：1..9。
func Rank(t int) int {
	if t < TileMin || t > TileMax {
		return 0
	}

	return (t-1)%9 + 1
}

// SuitName 返回花色中文名。
func SuitName(s int) string {
	switch s {
	case 0:
		return "万"
	case 1:
		return "筒"
	case 2:
		return "条"
	}

	return "?"
}

// Name 返回牌的中文名，例如 5 万、17 筒。
func Name(t int) string {
	if t < TileMin || t > TileMax {
		return "无效牌"
	}

	return fmt.Sprintf("%d%s", Rank(t), SuitName(Suit(t)))
}

// NewWall 生成一副洗好的牌墙。
func NewWall(rng *rand.Rand) []int {
	wall := make([]int, 0, WallSize)

	for t := TileMin; t <= TileMax; t++ {
		for i := 0; i < CopiesPerTile; i++ {
			wall = append(wall, t)
		}
	}

	rng.Shuffle(len(wall), func(i, j int) {
		wall[i], wall[j] = wall[j], wall[i]
	})

	return wall
}

// Counts 是手牌的计数表示，下标即牌 id，0 号位空置。
type Counts [TileMax + 1]int

// Add 增加一张牌。
func (p *Counts) Add(t int) {
	if t >= TileMin && t <= TileMax {
		p[t]++
	}
}

// Remove 移除一张牌，返回是否移除成功。
func (p *Counts) Remove(t int) bool {
	if t < TileMin || t > TileMax || p[t] <= 0 {
		return false
	}

	p[t]--

	return true
}

// Total 返回手牌总张数。
func (p *Counts) Total() int {
	total := 0

	for _, n := range p {
		total += n
	}

	return total
}

// Clone 复制一份计数。
func (p *Counts) Clone() Counts {
	var c Counts
	copy(c[:], p[:])

	return c
}

// Tiles 展开为牌列表（升序）。
func (p *Counts) Tiles() []int {
	out := make([]int, 0, p.Total())

	for t := TileMin; t <= TileMax; t++ {
		for i := 0; i < p[t]; i++ {
			out = append(out, t)
		}
	}

	return out
}

// MeldType 面子类型。
type MeldType int

const (
	// MeldPeng 碰。
	MeldPeng MeldType = 1
	// MeldMingGang 明杠（直杠，来自他家弃牌）。
	MeldMingGang MeldType = 2
	// MeldAnGang 暗杠。
	MeldAnGang MeldType = 3
	// MeldBuGang 补杠（巴杠，碰后补第四张）。
	MeldBuGang MeldType = 4
)

// Meld 已亮出的面子。
type Meld struct {
	Type MeldType `json:"type"`
	Tile int      `json:"tile"`
	From int      `json:"from"`
}

// IsGang 判断是否为杠。
func (m Meld) IsGang() bool {
	return m.Type == MeldMingGang || m.Type == MeldAnGang || m.Type == MeldBuGang
}

// MeldName 返回面子中文名。
func (m Meld) MeldName() string {
	switch m.Type {
	case MeldPeng:
		return "碰"
	case MeldMingGang:
		return "明杠"
	case MeldAnGang:
		return "暗杠"
	case MeldBuGang:
		return "补杠"
	}

	return "未知"
}
