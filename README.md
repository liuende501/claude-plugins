# Claude Plugins

Claude Code MCP 插件市场，收录可直接接入 Claude Code 的 MCP Server 插件。

## 插件列表

| 插件 | 类型 | 说明 |
|------|------|------|
| [gogs-pr](./gogs-pr/) | MCP Server | Gogs Pull Request 管理（列出/查看/创建/编辑/合并） |

## 快速安装

以 `gogs-pr` 为例，在 `~/.claude/settings.json` 中添加：

```json
{
  "mcpServers": {
    "gogs-pr": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/liuende501/claude-plugins#subdirectory=gogs-pr",
        "gogs-pr"
      ],
      "env": {
        "GOGS_URL": "http://your-gogs-host:3000",
        "GOGS_TOKEN": "your_token_here"
      }
    }
  }
}
```

无需 clone 仓库，`uvx` 自动拉取安装，重启 Claude Code 即可使用。

## 插件目录结构

每个插件目录包含：

```
<plugin-name>/
  server.py        # MCP Server 入口（Python）
  requirements.txt # Python 依赖
  pyproject.toml   # 打包配置（支持 uvx 安装）
  plugin.json      # 插件元数据（名称、版本、环境变量、工具列表等）
  README.md        # 安装与使用说明
```
