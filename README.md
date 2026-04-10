# Claude Plugins

Claude Code MCP 插件市场，收录可直接接入 Claude Code 的 MCP Server 插件。

## 插件列表

| 插件 | 类型 | 说明 |
|------|------|------|
| [gogs-pr](./gogs-pr/) | MCP Server | Gogs Pull Request 管理（列出/查看/创建/编辑/合并） |

## 插件目录结构

每个插件目录包含：

```
<plugin-name>/
  server.py        # MCP Server 入口（Python）
  requirements.txt # Python 依赖
  plugin.json      # 插件元数据（名称、版本、环境变量、工具列表等）
  README.md        # 安装与使用说明
```
