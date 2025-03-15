# Python游戏合集

这是一个使用Python和Pygame开发的经典游戏合集项目，包含多个耳熟能详的小游戏。

## 游戏列表

- 俄罗斯方块 (Tetris)
- 贪吃蛇 (Snake)
- 扫雷 (Minesweeper)
- 飞机大战 (Plane Battle)
- 炸弹人 (Bomberman)
- 打砖块 (Breakout)
- 2048
- 连连看 (Memory Game)
- 五子棋 (Gomoku)
- 象棋 (Chinese Chess)
- 数独 (Sudoku)
- 丛林棋 (Jungle Chess)
- Flappy Bird
- 太空护盾 (Space Shield)
- 猜数字 (Guess Number)
- 井字棋 (Tic Tac Toe)
- 坦克大战 (Tank War)

## 功能特点

- 使用Pygame开发，具有良好的游戏性能和流畅的操作体验
- 保留经典游戏的核心玩法，同时加入现代化的界面设计
- 支持键盘控制，操作简单直观
- 包含分数统计、游戏难度调整等功能
- 代码结构清晰，易于理解和扩展

## 环境要求

- Python 3.10 或更高版本
- Pygame 2.5.2 或更高版本

## 安装说明

1. 克隆项目到本地：

```bash
git clone https://github.com/yourusername/game.git
cd game
```

2. 使用Poetry安装依赖：

```bash
poetry install
```

或者使用pip安装依赖：

```bash
pip install pygame
```

## 运行游戏

```bash
python src/main.py
```

## 游戏控制

每个游戏都有其特定的控制方式，一般遵循以下规则：

- 方向键：控制移动
- 空格键：发射/确认/暂停
- ESC键：返回主菜单
- R键：重新开始当前游戏

## 开发说明

项目使用Poetry进行依赖管理，开发环境配置如下：

```bash
poetry install --with dev  # 安装开发依赖
```

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。在提交PR之前，请确保：

1. 代码符合项目的编码规范（使用black进行格式化）
2. 添加必要的测试用例
3. 更新相关文档

## TODO 列表

### 新增游戏

- [ ] 魔方 (Rubik's Cube)
- [ ] 推箱子 (Sokoban)
- [ ] 斗地主 (Fight the Landlord)
- [ ] 黑白棋 (Reversi)
- [ ] 跳棋 (Checkers)
- [ ] 拼图 (Puzzle)
- [ ] 弹球 (Pinball)
- [ ] 吃豆人 (Pac-Man)

### 功能增强

- [ ] 多人对战模式
- [ ] 全局排行榜系统
- [ ] 游戏存档功能
- [ ] 游戏设置界面
- [ ] 成就系统
- [ ] 新手教程

### 体验优化

- [ ] 添加背景音乐和音效
- [ ] 优化UI界面设计
- [ ] 支持手柄控制
- [ ] 添加游戏动画效果
- [ ] 支持自定义主题
- [ ] 优化游戏性能

### 项目完善

- [ ] 添加单元测试
- [ ] 设置CI/CD流程
- [ ] 完善代码文档
- [ ] 添加游戏API文档
- [ ] 优化项目结构
- [ ] 制作项目官网

## 许可证

本项目采用Mozilla Public License Version 2.0许可证。详情请参见[LICENSE](LICENSE)文件。
