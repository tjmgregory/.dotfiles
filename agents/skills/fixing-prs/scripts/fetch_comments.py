#!/usr/bin/env python3
"""
Fetch all PR review conversations, completely, in a compact token-efficient format.

Usage:
    fetch_comments.py <pr_url_or_number> [--all] [--json]

Uses the GraphQL reviewThreads API so every thread arrives as a complete
conversation (all replies, resolved/outdated state) with cursor pagination at
every level — nothing is missed, regardless of comment count.

Default output is a compact text digest designed for LLM consumption:
  - Each item leads with the exact reply target for post_replies_batch.py,
    e.g. `reply: {"comment_id": 123}`.
  - Threads/comments already handled by an agent (and resolved threads) are
    collapsed into counts. Pass --all to show them in full.
  - HTML comments (hidden bot markers) are stripped from bodies.

Statuses:
  NEEDS REPLY — no agent reply in the conversation yet
  FOLLOW-UP   — someone (human or reviewer bot) replied after our last reply
  HANDLED     — our reply is the last word; hidden unless --all
  INFO        — housekeeping bot comment, never needs a reply; hidden unless --all
  (resolved)  — thread marked resolved on GitHub; hidden unless --all

--json dumps the full structured data instead (all items, no truncation).
"""

import argparse
import json
import re
import subprocess
import sys

AGENT_PREFIX = "[🤖"
REPLY_MARKER_RE = re.compile(r"<!--\s*reply-to:\s*(issue_comment|review):(\d+)\s*-->")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
# Innermost <details> block (contains no nested <details>)
DETAILS_RE = re.compile(r"<details>(?:(?!<details).)*?</details>", re.DOTALL)
SUMMARY_RE = re.compile(r"<summary>(.*?)</summary>", re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")

# Issue-comment authors that only post housekeeping notifications, never
# feedback that needs a reply (ticket sync, deploy previews, coverage).
NOISE_BOT_LOGINS = {
    "linear", "vercel", "netlify", "codecov", "codecov-commenter",
    "github-actions", "sonarcloud",
}
# Body markers of informational bot comments from otherwise-real reviewers
NOISE_BODY_MARKERS = (
    "Rate limit exceeded",
    "<summary>📝 Walkthrough</summary>",
)


def die(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_pr_reference(pr_ref: str) -> tuple[str, str, int]:
    """Extract (owner, repo, number) from a PR URL or bare number + git remote."""
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)", pr_ref)
    if m:
        return m.group(1), m.group(2), int(m.group(3))

    if not pr_ref.isdigit():
        die(f"Invalid PR reference: {pr_ref}")

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError:
        die("Not in a git repository and no full PR URL provided")

    remote = result.stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+)/(.+?)(?:\.git)?$", remote)
    if not m:
        die(f"Could not parse GitHub owner/repo from remote: {remote}")
    return m.group(1), m.group(2), int(pr_ref)


def graphql(query: str, variables: dict) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if isinstance(value, int):
            cmd += ["-F", f"{key}={value}"]
        else:
            cmd += ["-f", f"{key}={value}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        die(f"GitHub API error: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    if data.get("errors"):
        die(f"GraphQL error: {json.dumps(data['errors'])}")
    return data["data"]


PR_QUERY = """
query($owner: String!, $repo: String!, $num: Int!, $threadCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $num) {
      number title url state isDraft
      headRefName baseRefName headRefOid
      author { login }
      reviewThreads(first: 50, after: $threadCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated path line originalLine
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              databaseId author { login } body createdAt
              isMinimized minimizedReason
            }
          }
        }
      }
    }
  }
}
"""

THREAD_COMMENTS_QUERY = """
query($threadId: ID!, $cursor: String) {
  node(id: $threadId) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          databaseId author { login } body createdAt
          isMinimized minimizedReason
        }
      }
    }
  }
}
"""

REVIEWS_QUERY = """
query($owner: String!, $repo: String!, $num: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $num) {
      reviews(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { databaseId author { login } body state createdAt }
      }
    }
  }
}
"""

ISSUE_COMMENTS_QUERY = """
query($owner: String!, $repo: String!, $num: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $num) {
      comments(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { databaseId author { login } body createdAt }
      }
    }
  }
}
"""


def fetch_all(owner: str, repo: str, num: int) -> dict:
    """Fetch PR info, all review threads (with complete comment lists),
    all reviews, and all issue comments, paginating everything."""
    print(f"Fetching PR #{num} from {owner}/{repo}...", file=sys.stderr)

    threads: list[dict] = []
    info: dict = {}
    cursor = ""
    while True:
        data = graphql(PR_QUERY, {
            "owner": owner, "repo": repo, "num": num, "threadCursor": cursor,
        })
        pr = data["repository"]["pullRequest"]
        if pr is None:
            die(f"PR #{num} not found in {owner}/{repo}")
        info = {k: pr[k] for k in (
            "number", "title", "url", "state", "isDraft",
            "headRefName", "baseRefName", "headRefOid", "author",
        )}
        conn = pr["reviewThreads"]
        for node in conn["nodes"]:
            comments = node["comments"]["nodes"]
            page = node["comments"]["pageInfo"]
            # Rare: a single thread with >100 comments — page through the rest
            while page["hasNextPage"]:
                extra = graphql(THREAD_COMMENTS_QUERY, {
                    "threadId": node["id"], "cursor": page["endCursor"],
                })["node"]["comments"]
                comments.extend(extra["nodes"])
                page = extra["pageInfo"]
            node["comments"] = comments
            threads.append(node)
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]

    reviews: list[dict] = []
    cursor = ""
    while True:
        conn = graphql(REVIEWS_QUERY, {
            "owner": owner, "repo": repo, "num": num, "cursor": cursor,
        })["repository"]["pullRequest"]["reviews"]
        reviews.extend(conn["nodes"])
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]

    issue_comments: list[dict] = []
    cursor = ""
    while True:
        conn = graphql(ISSUE_COMMENTS_QUERY, {
            "owner": owner, "repo": repo, "num": num, "cursor": cursor,
        })["repository"]["pullRequest"]["comments"]
        issue_comments.extend(conn["nodes"])
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]

    return {
        "owner": owner, "repo": repo, "info": info,
        "threads": threads, "reviews": reviews,
        "issue_comments": issue_comments,
    }


def is_agent(body: str) -> bool:
    """Any agent-authored comment (author replies AND agent reviewer feedback)."""
    return body.lstrip().startswith(AGENT_PREFIX)


def is_our_reply(body: str) -> bool:
    """An agent reply that HANDLES feedback. `[🤖 Reviewer - ...]` comments are
    incoming review feedback (posted by the reviewing-prs skill), not handling —
    a thread containing only one still needs a reply."""
    stripped = body.lstrip()
    return stripped.startswith(AGENT_PREFIX) and not stripped.startswith("[🤖 Reviewer")


def collapse_details(body: str) -> str:
    """Replace each <details> block with a one-line `▸ summary [collapsed]`.
    Bots wrap kilobytes of boilerplate in these; the summary line is enough
    for assessment and --json always has the full body."""
    def replace(match: re.Match) -> str:
        summary = SUMMARY_RE.search(match.group(0))
        text = TAG_RE.sub("", summary.group(1)).strip() if summary else "details"
        return f"▸ {text} [collapsed]"

    prev = None
    while prev != body:
        prev = body
        body = DETAILS_RE.sub(replace, body)
    return body


def clean_body(body: str) -> str:
    """Strip hidden HTML comments, collapse <details>, squeeze blank runs."""
    body = HTML_COMMENT_RE.sub("", body or "")
    body = collapse_details(body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def is_noise(comment: dict) -> bool:
    """Informational bot comment that never needs a reply."""
    if login(comment) in NOISE_BOT_LOGINS:
        return True
    body = comment.get("body") or ""
    return any(marker in body for marker in NOISE_BODY_MARKERS)


def conversation_status(bodies: list[str]) -> str:
    """Status from an ordered list of comment bodies."""
    last_ours = -1
    for i, body in enumerate(bodies):
        if is_our_reply(body):
            last_ours = i
    if last_ours == -1:
        return "NEEDS REPLY"
    if any(not is_our_reply(b) for b in bodies[last_ours + 1:]):
        return "FOLLOW-UP"
    return "HANDLED"


def annotate(data: dict) -> dict:
    """Attach statuses; link marker-based replies to their review / issue-comment
    targets so those conversations get statuses too."""
    for thread in data["threads"]:
        thread["status"] = conversation_status(
            [c["body"] or "" for c in thread["comments"]]
        )

    # Marker replies live in the issue-comment stream; group them by target.
    marker_replies: dict[tuple[str, int], list[dict]] = {}
    plain_comments = []
    for comment in data["issue_comments"]:
        m = REPLY_MARKER_RE.search(comment["body"] or "")
        if m:
            marker_replies.setdefault((m.group(1), int(m.group(2))), []).append(comment)
        else:
            plain_comments.append(comment)

    for review in data["reviews"]:
        review["replies"] = marker_replies.get(("review", review["databaseId"]), [])
        review["status"] = conversation_status(
            [review["body"] or ""] + [r["body"] or "" for r in review["replies"]]
        )

    for comment in plain_comments:
        comment["replies"] = marker_replies.get(
            ("issue_comment", comment["databaseId"]), []
        )
        if is_noise(comment):
            comment["status"] = "INFO"
        else:
            comment["status"] = conversation_status(
                [comment["body"] or ""] + [r["body"] or "" for r in comment["replies"]]
            )

    data["issue_comments"] = plain_comments
    return data


def login(comment: dict) -> str:
    author = comment.get("author")
    return author["login"] if author else "ghost"


def render_comment(comment: dict, out: list[str]) -> None:
    tag = " (minimized)" if comment.get("isMinimized") else ""
    out.append(f"@{login(comment)}{tag}:")
    out.append(clean_body(comment["body"]))


def render(data: dict, show_all: bool) -> str:
    info = data["info"]
    out: list[str] = []

    draft = " draft" if info["isDraft"] else ""
    out.append(
        f'PR #{info["number"]} {data["owner"]}/{data["repo"]} '
        f'[{info["state"]}{draft}] {info["title"]}'
    )
    out.append(
        f'branch: {info["headRefName"]} -> {info["baseRefName"]} '
        f'@ {info["headRefOid"][:9]}'
    )

    threads = data["threads"]
    resolved = [t for t in threads if t["isResolved"]]
    open_threads = [t for t in threads if not t["isResolved"]]
    handled = [t for t in open_threads if t["status"] == "HANDLED"]
    actionable = [t for t in open_threads if t["status"] != "HANDLED"]

    # Reviews: skip pending (invisible to others) and empty bodies
    reviews = [
        r for r in data["reviews"]
        if r["state"] != "PENDING" and clean_body(r["body"])
        and not is_agent(r["body"] or "")
    ]
    review_action = [r for r in reviews if r["status"] != "HANDLED"]
    comments = [c for c in data["issue_comments"] if not is_agent(c["body"] or "")]
    info_comments = [c for c in comments if c["status"] == "INFO"]
    comment_action = [c for c in comments if c["status"] not in ("HANDLED", "INFO")]

    hidden_bits = []
    if not show_all:
        if handled:
            hidden_bits.append(f"{len(handled)} handled threads")
        if resolved:
            hidden_bits.append(f"{len(resolved)} resolved threads")
        if info_comments:
            hidden_bits.append(
                f"{len(info_comments)} info bot comments "
                f"({', '.join(sorted({'@' + login(c) for c in info_comments}))})"
            )
    hidden = f' | hidden: {", ".join(hidden_bits)} (--all to show)' if hidden_bits else ""
    out.append(
        f"threads: {len(actionable)} actionable of {len(threads)}{hidden} | "
        f"reviews needing reply: {len(review_action)} | "
        f"issue comments needing reply: {len(comment_action)}"
    )

    shown_threads = threads if show_all else actionable
    if shown_threads:
        out.append("")
        out.append("=== REVIEW THREADS ===")
        for thread in shown_threads:
            root_id = thread["comments"][0]["databaseId"] if thread["comments"] else None
            line = thread["line"] or thread["originalLine"]
            loc = f'{thread["path"]}:{line}' if line else thread["path"]
            tags = []
            if thread["isOutdated"]:
                tags.append("outdated")
            if thread["isResolved"]:
                tags.append("resolved")
            tag_str = f' ({", ".join(tags)})' if tags else ""
            out.append("")
            out.append(
                f'--- reply: {{"comment_id": {root_id}}} | {loc}{tag_str} | '
                f'{thread["status"]}'
            )
            for comment in thread["comments"]:
                render_comment(comment, out)

    shown_reviews = reviews if show_all else review_action
    if shown_reviews:
        out.append("")
        out.append("=== REVIEW BODIES ===")
        for review in shown_reviews:
            out.append("")
            out.append(
                f'--- reply: {{"review_id": {review["databaseId"]}}} | '
                f'@{login(review)} {review["state"]} | {review["status"]}'
            )
            out.append(clean_body(review["body"]))
            for reply in review["replies"]:
                render_comment(reply, out)

    shown_comments = comments if show_all else comment_action
    if shown_comments:
        out.append("")
        out.append("=== ISSUE COMMENTS ===")
        for comment in shown_comments:
            out.append("")
            out.append(
                f'--- reply: {{"issue_comment_id": {comment["databaseId"]}}} | '
                f'@{login(comment)} | {comment["status"]}'
            )
            out.append(clean_body(comment["body"]))
            for reply in comment["replies"]:
                render_comment(reply, out)

    if not shown_threads and not shown_reviews and not shown_comments:
        out.append("")
        out.append("Nothing needs a reply.")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr", help="PR number or URL")
    parser.add_argument("--all", action="store_true",
                        help="include handled and resolved conversations")
    parser.add_argument("--json", action="store_true",
                        help="dump full structured JSON instead of the digest")
    args = parser.parse_args()

    owner, repo, num = parse_pr_reference(args.pr)
    data = annotate(fetch_all(owner, repo, num))

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(render(data, show_all=args.all))
    return 0


if __name__ == "__main__":
    sys.exit(main())
