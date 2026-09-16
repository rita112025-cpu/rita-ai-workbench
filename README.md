# Rita AI 工作台

這是一個整理 Codex、Claude Code、Prompt、工作自動化與工程工具的一頁式導航網站。

副標：Codex、Claude Code、Prompt 與工作自動化工具入口

## 功能

- 工具分類：常用 Prompt / Codex 工具 / Claude Code 分工 / 工作自動化工具 / AI 實驗 / Demo / 工程 / 報價工具 / 學習與資源
- 分類篩選：點分類只看該分類
- **GitHub 更新狀態**：每張卡片自動顯示最後 Push、Open Issues、更新狀態（近期有更新 / 穩定 / 久未更新 / 無法讀取）
- GitHub 狀態篩選：可依更新狀態篩選
- 搜尋工具：可搜尋名稱、用途、說明、標籤、更新狀態
- GitHub 連結：每張卡片都有 GitHub 按鈕
- Demo 連結：有 GitHub Pages 的才顯示 Demo 按鈕
- 狀態標籤：常用 / 可用 / 整理中
- **暗色 / 淺色切換**：未手動切換前會持續跟隨系統偏好，手動切換後自動記憶選擇
- 手機版友善：單欄，字體可讀，卡片好點選；桌機 2-3 欄

## GitHub 更新狀態功能

每個 GitHub repo 卡片自動顯示：
- 最後 Push 時間
- Open Issues 數量
- 更新狀態

狀態判斷規則（依 `pushed_at`）：
- 30 天內有 push：近期有更新
- 31～180 天內有 push：穩定
- 超過 180 天未 push：久未更新
- API 讀取失敗：無法讀取

API（同一帳號一次抓完，不逐一查 repo）：
```
https://api.github.com/users/rita112025-cpu/repos?per_page=100&sort=pushed
```

非本帳號的 repo（例如 upstream fork 來源）才走單一查詢：
```
https://api.github.com/repos/{owner}/{repo-name}
```

欄位：`name, html_url, description, updated_at, pushed_at, open_issues_count, stargazers_count, forks_count, archived, disabled`

前端：
1. 載入時先讀 localStorage 快取，未命中的才呼叫 API
2. 成功更新卡片
3. 失敗顯示「無法讀取」，不中斷頁面
4. loading「讀取 GitHub 狀態中...」
5. localStorage 快取 60 分鐘
6. 無 token、無登入、無後端

**為什麼不逐一查 repo**：未登入的 GitHub API 每小時每 IP 只有 60 次。43 個工具逐一查，一次冷載入就用掉 43 次，重新整理一次就全部變「無法讀取」。改成列表端點後，一次載入只花 1～2 次。

## 目前收錄工具 (43 個)

常用 Prompt：PROMPT-LIBRARY, gpt6-astra-prompts, ai-prompt-deck, work-prompts, ai-web-design-cheatsheet
Codex 工具：codex-skills-hub, local-workspace-mcp（upstream：arumwu/local-workspace-mcp，Alpha／研究中）, rita-codex-skills, vibe-coding-work-db, dsh-starter
Claude Code 分工：claude-dual-session-prompts, claude-skill-deck, claude-guide-presbyopia-friendly, Six-Skills-Dashboard, i-have-adhd（fork）, fable5-agent-battle
工作自動化：daily-report-viewer, line-summary-docx, subtitle_burner
AI 實驗 / Demo：zsgc-store, TradingAgents（fork）, LongCat-Avatar-Cloud, gods-eye-view（fork）
工程 / 報價：taiwan-construction-quote-tools (實際 repo: construction-quote-tools), tw-construction-quote-parser, boq-quote-cleaner, mep-boq-toolkit
學習與資源：revit-low-voltage-learning-guide, revit-low-voltage-learning-guide-Literary-Edition, revit-weak-guide, astra-3d-resource-hub, taiwan-learning-hub, stock-prompt-lab, stock_public, ai-resource-hub, fullstack-blueprint, markdown-upgrade-guide, Ssdc-Glossary-V5-Final-Unfrozen_-
生活 / 其他：tainan-trip, tainan-trip_meta, japan_travel, japan_travel_meta, yijing

**未收錄**：private repo（stock, verus, ssdc-glossary, pm-tracker-v7, segreene-ai-pilot）與本站自身 rita-ai-workbench

## 本機開啟

```bash
open index.html
# 或
python3 -m http.server 8000
```

## 部署到 GitHub Pages

1. 將 4 個檔案推到 repo，例如 `rita-ai-workbench`
2. Settings > Pages > Source: Deploy from a branch, Branch: main / root
3. 等待部署

若下載後檔名變成 `.txt` 或帶編號：

```powershell
Rename-Item "Index(8).html" "index.html"
Rename-Item "Styles(4).css" "styles.css"
Rename-Item "App(5).js" "app.js"
Rename-Item "README(20260914-011527).md" "README.md"
# 或
Rename-Item styles.css.txt styles.css
Rename-Item app.js.txt app.js
```

只提交：

```bash
git add index.html styles.css app.js README.md
git commit -m "release: Rita AI 工作台 v1"
git push -u origin main
```

## 工具資料修改

`app.js` 的 `tools` 陣列，格式：

```js
{
  name: "PROMPT-LIBRARY",
  repo: "PROMPT-LIBRARY",
  owner: "rita112025-cpu",
  category: "常用 Prompt",
  description: "...",
  detail: "...",
  tags: ["Prompt", "Library"],
  status: "常用",
  github: "https://github.com/rita112025-cpu/PROMPT-LIBRARY",
  demo: ""
}
```

## 重要

- `Rita-Ai-V1.html` 為 React 預覽展示頁，含 `rita-ai-lab` 測試帳號與非正式工具，不列入正式 v1，請勿推送
- 正式版無 Google Fonts，無外部依賴，帳號皆為 `rita112025-cpu`
