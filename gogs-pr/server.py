"""
Gogs Pull Request MCP Server
提供 6 个工具供 Claude 直接调用 Gogs PR API
"""

import os
import httpx
from fastmcp import FastMCP

GOGS_URL = os.environ.get("GOGS_URL", "http://127.0.0.1:3001")
GOGS_TOKEN = os.environ.get("GOGS_TOKEN", "")

mcp = FastMCP(
    name="gogs-pr",
    instructions=(
        "Gogs Pull Request 管理工具。"
        "当用户提到创建/查看/编辑/合并/列出/评论 PR 或 Pull Request 时，使用这些工具。"
        f"当前连接的 Gogs 实例：{GOGS_URL}"
    ),
)


def _client() -> httpx.Client:
    return httpx.Client(
        base_url=GOGS_URL,
        headers={
            "Authorization": f"token {GOGS_TOKEN}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )


def _handle(resp: httpx.Response) -> dict:
    if resp.status_code == 204:
        return {"success": True, "message": "操作成功"}
    if not resp.is_success:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise ValueError(f"HTTP {resp.status_code}: {detail}")
    return resp.json()


@mcp.tool(
    description=(
        "列出仓库的 Pull Request 列表。\n"
        "- owner: 仓库所有者用户名\n"
        "- repo: 仓库名称\n"
        "- state: open（默认）或 closed\n"
        "- page: 页码，默认 1"
    )
)
def gogs_list_pull_requests(
    owner: str,
    repo: str,
    state: str = "open",
    page: int = 1,
) -> list:
    with _client() as c:
        resp = c.get(
            f"/api/v1/repos/{owner}/{repo}/pulls",
            params={"state": state, "page": page},
        )
        return _handle(resp)


@mcp.tool(
    description=(
        "获取单个 Pull Request 的详情。\n"
        "- owner: 仓库所有者用户名\n"
        "- repo: 仓库名称\n"
        "- index: PR 序号（number 字段）"
    )
)
def gogs_get_pull_request(
    owner: str,
    repo: str,
    index: int,
) -> dict:
    with _client() as c:
        resp = c.get(f"/api/v1/repos/{owner}/{repo}/pulls/{index}")
        return _handle(resp)


@mcp.tool(
    description=(
        "创建一个新的 Pull Request。\n"
        "- owner: 目标仓库所有者用户名\n"
        "- repo: 目标仓库名称\n"
        "- head: 来源分支，同仓库传 'branch'，跨 fork 传 'username:branch'\n"
        "- base: 目标分支名\n"
        "- title: PR 标题（必填）\n"
        "- body: PR 描述（可选）\n"
        "- assignee: 负责人用户名（可选）\n"
        "- milestone: 里程碑 ID（可选）\n"
        "- labels: 标签 ID 列表（可选）"
    )
)
def gogs_create_pull_request(
    owner: str,
    repo: str,
    head: str,
    base: str,
    title: str,
    body: str = "",
    assignee: str = "",
    milestone: int = 0,
    labels: list[int] | None = None,
) -> dict:
    payload: dict = {"head": head, "base": base, "title": title}
    if body:
        payload["body"] = body
    if assignee:
        payload["assignee"] = assignee
    if milestone:
        payload["milestone"] = milestone
    if labels:
        payload["labels"] = labels

    with _client() as c:
        resp = c.post(f"/api/v1/repos/{owner}/{repo}/pulls", json=payload)
        return _handle(resp)


@mcp.tool(
    description=(
        "编辑 Pull Request（标题、描述、状态、负责人、里程碑）。\n"
        "所有字段均可选，只传需要修改的字段。\n"
        "- owner: 仓库所有者用户名\n"
        "- repo: 仓库名称\n"
        "- index: PR 序号\n"
        "- title: 新标题\n"
        "- body: 新描述（传空字符串可清空）\n"
        "- state: open 重开 / closed 关闭\n"
        "- assignee: 负责人用户名（传空字符串清除）\n"
        "- milestone: 里程碑 ID（传 0 清除）"
    )
)
def gogs_edit_pull_request(
    owner: str,
    repo: str,
    index: int,
    title: str = "",
    body: str | None = None,
    state: str | None = None,
    assignee: str | None = None,
    milestone: int | None = None,
) -> dict:
    payload: dict = {}
    if title:
        payload["title"] = title
    if body is not None:
        payload["body"] = body
    if state is not None:
        payload["state"] = state
    if assignee is not None:
        payload["assignee"] = assignee
    if milestone is not None:
        payload["milestone"] = milestone

    with _client() as c:
        resp = c.patch(f"/api/v1/repos/{owner}/{repo}/pulls/{index}", json=payload)
        return _handle(resp)


@mcp.tool(
    description=(
        "合并 Pull Request。需要对仓库有写权限。\n"
        "- owner: 仓库所有者用户名\n"
        "- repo: 仓库名称\n"
        "- index: PR 序号\n"
        "- merge_style: create_merge_commit（默认）或 rebase_before_merging\n"
        "- description: 合并 commit 的附加描述（可选）"
    )
)
def gogs_merge_pull_request(
    owner: str,
    repo: str,
    index: int,
    merge_style: str = "create_merge_commit",
    description: str = "",
) -> dict:
    payload: dict = {"merge_style": merge_style}
    if description:
        payload["description"] = description

    with _client() as c:
        resp = c.post(f"/api/v1/repos/{owner}/{repo}/pulls/{index}/merge", json=payload)
        return _handle(resp)


@mcp.tool(
    description=(
        "对 Pull Request 发表评论，可同时变更 PR 状态。\n"
        "- owner: 仓库所有者用户名\n"
        "- repo: 仓库名称\n"
        "- index: PR 序号\n"
        "- body: 评论内容（必填）\n"
        "- state: 不传仅评论；closed 评论并关闭；open 评论并重新开启（需写权限）"
    )
)
def gogs_create_pull_request_comment(
    owner: str,
    repo: str,
    index: int,
    body: str,
    state: str = "",
) -> dict:
    payload: dict = {"body": body}
    if state:
        payload["state"] = state

    with _client() as c:
        resp = c.post(f"/api/v1/repos/{owner}/{repo}/pulls/{index}/comments", json=payload)
        return _handle(resp)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
