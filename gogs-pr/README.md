# gogs-pr

Gogs Pull Request 管理 MCP 插件，让 Claude 直接通过 Gogs API 操作 PR。

## 功能

| 工具 | 说明 |
|------|------|
| `gogs_list_pull_requests` | 列出仓库的 PR 列表（支持 open/closed 筛选） |
| `gogs_get_pull_request` | 获取单个 PR 详情 |
| `gogs_create_pull_request` | 创建新 PR |
| `gogs_edit_pull_request` | 编辑 PR（标题、描述、状态、负责人、里程碑） |
| `gogs_merge_pull_request` | 合并 PR |

## 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `GOGS_URL` | 否 | `http://127.0.0.1:3001` | Gogs 实例地址 |
| `GOGS_TOKEN` | 是 | — | Gogs API Token |

> 在 Gogs 用户设置 → 应用 → 生成令牌 处获取 Token。

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Claude Code

在 `~/.claude/claude_desktop_config.json`（或 `.claude/settings.json`）中添加：

```json
{
  "mcpServers": {
    "gogs-pr": {
      "command": "python",
      "args": ["/path/to/gogs-pr/server.py"],
      "env": {
        "GOGS_URL": "http://your-gogs-host:3000",
        "GOGS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## 使用示例

- "列出 liuende/gogs 的所有 open PR"
- "帮我把 dev 分支的改动创建一个 PR 合并到 main"
- "关闭第 3 号 PR"
- "合并 liuende/gogs 的第 5 号 PR"
