const tools = [
  {name:"PROMPT-LIBRARY",repo:"PROMPT-LIBRARY",owner:"rita112025-cpu",category:"常用 Prompt",description:"集中管理常用 Prompt。",detail:"放置可重複使用的 Prompt，例如工作分析、報告整理、程式審查、工具規劃等。",tags:["Prompt","Library","AI 工作流"],status:"常用",github:"https://github.com/rita112025-cpu/PROMPT-LIBRARY",demo:"https://rita112025-cpu.github.io/PROMPT-LIBRARY/"},
  {name:"gpt6-astra-prompts",repo:"gpt6-astra-prompts",owner:"rita112025-cpu",category:"常用 Prompt",description:"Astra / GPT-6 相關提示詞整理。",detail:"整理 GPT-6 Astra 使用場景、工具連接、工作流程與進階 Prompt。",tags:["GPT-6","Astra","Prompt"],status:"可用",github:"https://github.com/rita112025-cpu/gpt6-astra-prompts",demo:"https://rita112025-cpu.github.io/gpt6-astra-prompts/"},
  {name:"ai-prompt-deck",repo:"ai-prompt-deck",owner:"rita112025-cpu",category:"常用 Prompt",description:"AI Prompt 簡報與教材素材。",detail:"適合整理成教學、簡報或內部分享內容。",tags:["Prompt","Deck","教材"],status:"可用",github:"https://github.com/rita112025-cpu/ai-prompt-deck",demo:"https://rita112025-cpu.github.io/ai-prompt-deck/"},
  {name:"work-prompts",repo:"work-prompts",owner:"rita112025-cpu",category:"常用 Prompt",description:"工作用 AI 提示詞範本庫。",detail:"日常工作場景的提示詞範本，例如信件、報告、會議紀錄與交辦整理。",tags:["Prompt","工作","範本"],status:"常用",github:"https://github.com/rita112025-cpu/work-prompts",demo:""},
  {name:"ai-web-design-cheatsheet",repo:"ai-web-design-cheatsheet",owner:"rita112025-cpu",category:"常用 Prompt",description:"AI 網頁設計快速參考手冊。",detail:"8 大靈感庫對照表，附可直接貼給 Codex / Claude / Cursor 的通用 Prompt，讓 AI 依規則改現有網站。",tags:["網頁設計","Prompt","工作流"],status:"可用",github:"https://github.com/rita112025-cpu/ai-web-design-cheatsheet",demo:"https://rita112025-cpu.github.io/ai-web-design-cheatsheet/"},
  {name:"chatgpt-cheatsheet-zh-TW",repo:"chatgpt-cheatsheet-zh-TW",owner:"rita112025-cpu",category:"常用 Prompt",description:"100 個 ChatGPT 指令大全。",detail:"繁中優化的 100 個開箱即用模板，10 大分類，可搜尋、分類篩選、一鍵複製，支援深色模式。",tags:["ChatGPT","Prompt","繁中"],status:"可用",github:"https://github.com/rita112025-cpu/chatgpt-cheatsheet-zh-TW",demo:"https://rita112025-cpu.github.io/chatgpt-cheatsheet-zh-TW/"},
  {name:"awesome-gpt-image-2",repo:"awesome-gpt-image-2",owner:"rita112025-cpu",category:"常用 Prompt",description:"GPT Image 2 提示詞與案例庫。",detail:"fork 自上游，530+ 個案例、20+ 套模板與可複用 Skills，附完整提示詞與生成紀錄，當生圖 Prompt 參考。",tags:["GPT Image","Prompt","Fork"],status:"研究中",github:"https://github.com/rita112025-cpu/awesome-gpt-image-2",demo:""},
  {name:"codex-skills-hub",repo:"codex-skills-hub",owner:"rita112025-cpu",category:"Codex 工具",description:"Codex Skills 入口。",detail:"整理可用的 Codex skills、使用情境、安裝與應用方向。",tags:["Codex","Skills","AI 工具"],status:"常用",github:"https://github.com/rita112025-cpu/codex-skills-hub",demo:"https://rita112025-cpu.github.io/codex-skills-hub/"},
  {name:"local-workspace-mcp",repo:"local-workspace-mcp",owner:"arumwu",category:"Codex 工具",description:"讓 AI 透過 MCP 存取本機檔案、終端程序、Office 文件與多台裝置。",detail:"⚠️ 原生 Windows 不建議使用（含 Unix 專用依賴）；安全性與相容性評估中。Alpha 研究用，勿裝進正式環境；來源為 upstream。",tags:["MCP","本機工作區","Alpha"],status:"研究中",github:"https://github.com/arumwu/local-workspace-mcp",demo:""},
  {name:"rita-codex-skills",repo:"rita-codex-skills",owner:"rita112025-cpu",category:"Codex 工具",description:"個人 Codex Skills 集合。",detail:"集中管理、備份與跨電腦安裝常用 Skills，目前含 security（安全審查）、retro（回顧復盤）與 Windows 一鍵安裝腳本。",tags:["Codex","Skills","備份"],status:"常用",github:"https://github.com/rita112025-cpu/rita-codex-skills",demo:"https://rita112025-cpu.github.io/rita-codex-skills/"},
  {name:"vibe-coding-work-db",repo:"vibe-coding-work-db",owner:"rita112025-cpu",category:"Codex 工具",description:"實用 Skills 與 MCP 篩選清單。",detail:"從 mcpservers.org 篩出真正能放進日常開發流程的 Skills 與 MCP，拒絕玩具型工具。",tags:["MCP","Skills","篩選"],status:"可用",github:"https://github.com/rita112025-cpu/vibe-coding-work-db",demo:"https://rita112025-cpu.github.io/vibe-coding-work-db/"},
  {name:"dsh-starter",repo:"dsh-starter",owner:"rita112025-cpu",category:"Codex 工具",description:"DeepSeek Harness 入門模板。",detail:"下載、填入 API Key、雙擊啟動，幾分鐘內就能使用並試用「文件摘要」技能。",tags:["DeepSeek","模板","入門"],status:"可用",github:"https://github.com/rita112025-cpu/dsh-starter",demo:"https://rita112025-cpu.github.io/dsh-starter/"},
  {name:"local-notebook",repo:"local-notebook",owner:"rita112025-cpu",category:"Codex 工具",description:"本機知識庫 + MCP server。",detail:"匯入 PDF／TXT／MD，用 SQLite FTS5 全文搜尋（支援中文），結果附檔名、頁碼、行號出處；提供本機網頁 UI 與 MCP server，讓 Claude 直接查你的資料。",tags:["MCP","知識庫","本機"],status:"可用",github:"https://github.com/rita112025-cpu/local-notebook",demo:""},
  {name:"openchatx-mcp",repo:"openchatx-mcp",owner:"rita112025-cpu",category:"Codex 工具",description:"讓 ChatGPT 變成本機 Agent 執行環境。",detail:"fork 自上游，透過一個 MCP 連線操作電腦、使用本機工具、探索 MCP servers 並委派給自有模型。研究用。",tags:["MCP","ChatGPT","Fork"],status:"研究中",github:"https://github.com/rita112025-cpu/openchatx-mcp",demo:""},
  {name:"open-code-review",repo:"open-code-review",owner:"rita112025-cpu",category:"Codex 工具",description:"混合架構程式碼審查工具。",detail:"fork 自上游（阿里巴巴），確定性管線 + LLM Agent，逐行評論，內建 NPE、執行緒安全、XSS、SQL injection 等多語言規則，相容 OpenAI 與 Anthropic。",tags:["Code Review","LLM","Fork"],status:"研究中",github:"https://github.com/rita112025-cpu/open-code-review",demo:""},
  {name:"claude-dual-session-prompts",repo:"claude-dual-session-prompts",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude Code 多視窗分工 Prompt。",detail:"支援不同 Claude Code 視窗分別負責讀程式、改程式、驗收、整合報告。",tags:["Claude Code","分工","Prompt"],status:"常用",github:"https://github.com/rita112025-cpu/claude-dual-session-prompts",demo:"https://rita112025-cpu.github.io/claude-dual-session-prompts/"},
  {name:"claude-skill-deck",repo:"claude-skill-deck",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude Skill 教材與簡報。",detail:"適合整理 Claude Skills 的概念、應用方式與展示內容。",tags:["Claude","Skill","Deck"],status:"可用",github:"https://github.com/rita112025-cpu/claude-skill-deck",demo:"https://rita112025-cpu.github.io/claude-skill-deck/"},
  {name:"claude-guide-presbyopia-friendly",repo:"Claude-Guide-Presbyopia-Friendly",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude 使用指南。",detail:"整理 Claude 使用方式、分工模式與實務操作說明，適合長時間閱讀。",tags:["Claude","Guide","Workflow"],status:"可用",github:"https://github.com/rita112025-cpu/Claude-Guide-Presbyopia-Friendly",demo:"https://rita112025-cpu.github.io/Claude-Guide-Presbyopia-Friendly/"},
  {name:"agent-skills-dashboard",repo:"agent-skills-dashboard",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Agent Skill 總覽儀表板。",detail:"16 個 skill（6 核心 + 10 堆疊）集中管理，含階段篩選、互動評分、一鍵複製安裝路徑與 7 步工作流程圖。單檔 HTML、零依賴。",tags:["Skill","Dashboard","Agent"],status:"常用",github:"https://github.com/rita112025-cpu/agent-skills-dashboard",demo:"https://rita112025-cpu.github.io/agent-skills-dashboard/"},
  {name:"i-have-adhd",repo:"i-have-adhd",owner:"rita112025-cpu",category:"Claude Code 分工",description:"ADHD 友善輸出 Skill。",detail:"fork 自上游，讓 coding agent 不要把答案埋在長篇說明裡：先給下一步動作、步驟編號、結尾一個具體行動。",tags:["Skill","輸出","ADHD"],status:"常用",github:"https://github.com/rita112025-cpu/i-have-adhd",demo:""},
  {name:"fable5-agent-battle",repo:"fable5-agent-battle",owner:"rita112025-cpu",category:"Claude Code 分工",description:"AI Agent 對比驗收工作流。",detail:"獨立提案、隔離實作、共同驗收與證據裁決，用來比較多個 agent 的解法並留下可稽核的決策紀錄。",tags:["Agent","驗收","工作流"],status:"研究中",github:"https://github.com/rita112025-cpu/fable5-agent-battle",demo:""},
  {name:"daily-report-viewer",repo:"daily-report-viewer",owner:"rita112025-cpu",category:"工作自動化工具",description:"日報查看器。",detail:"用於查看、整理或展示工作日報與進度資料。",tags:["日報","Viewer","工作追蹤"],status:"常用",github:"https://github.com/rita112025-cpu/daily-report-viewer",demo:"https://rita112025-cpu.github.io/daily-report-viewer/"},
  {name:"line-summary-docx",repo:"line-summary-docx",owner:"rita112025-cpu",category:"工作自動化工具",description:"LINE 對話摘要轉文件。",detail:"將 LINE 對話或文字紀錄整理成文件格式，適合做會議紀錄、工作摘要或交辦追蹤。",tags:["LINE","DOCX","摘要"],status:"可用",github:"https://github.com/rita112025-cpu/line-summary-docx",demo:""},
  {name:"subtitle_burner",repo:"subtitle_burner",owner:"rita112025-cpu",category:"工作自動化工具",description:"字幕工具。",detail:"處理字幕、逐字稿或影音文字內容，支援燒錄與格式轉換。",tags:["字幕","逐字稿","影音"],status:"可用",github:"https://github.com/rita112025-cpu/subtitle_burner",demo:""},
  {name:"evidence-ingestion-final-bilingual",repo:"evidence-ingestion-final-bilingual",owner:"rita112025-cpu",category:"工作自動化工具",description:"evidence-first 文件擷取模板。",detail:"原檔才是證據，Markdown 只是衍生。整合 MarkItDown、Crawl4AI、Browser Use、Scrapy，附繁中/EN 與暗亮版雙切換官網。",tags:["Evidence","擷取","Python"],status:"可用",github:"https://github.com/rita112025-cpu/evidence-ingestion-final-bilingual",demo:"https://rita112025-cpu.github.io/evidence-ingestion-final-bilingual/"},
  {name:"evidence-first-document-review",repo:"evidence-first-document-review",owner:"rita112025-cpu",category:"工作自動化工具",description:"證據導向文件審查管線。",detail:"執行資訊清單、結構化審查結果、來源追溯、證據驗證關卡與可重製報告，讓 AI 審查結論都能回查原文。",tags:["Evidence","文件審查","Python"],status:"可用",github:"https://github.com/rita112025-cpu/evidence-first-document-review",demo:"https://rita112025-cpu.github.io/evidence-first-document-review/"},
  {name:"zsgc-store",repo:"zsgc-store",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"全端電商示範站。",detail:"Next.js 16 + React 19 + Prisma + PostgreSQL，含商品目錄、購物車、願望清單、結帳、禮物卡、點數與後台。可當全端專案參考實作。",tags:["Next.js","全端","電商"],status:"可用",github:"https://github.com/rita112025-cpu/zsgc-store",demo:"https://zsgc-store.vercel.app"},
  {name:"TradingAgents",repo:"TradingAgents",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"多 Agent LLM 金融交易框架。",detail:"研究用 fork，觀察多 Agent 分工（分析、研究、交易、風控）如何協作。僅供研究，非投資建議。",tags:["Multi-Agent","LLM","研究"],status:"研究中",github:"https://github.com/rita112025-cpu/TradingAgents",demo:""},
  {name:"LongCat-Avatar-Cloud",repo:"LongCat-Avatar-Cloud",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"雲端 GPU 數位人 Demo。",detail:"LongCat-Video-Avatar 1.5 talking-head 示範，支援 Colab / RunPod / Docker，權重由 Hugging Face 下載。需要 GPU 環境。",tags:["Avatar","GPU","Hugging Face"],status:"研究中",github:"https://github.com/rita112025-cpu/LongCat-Avatar-Cloud",demo:""},
  {name:"gods-eye-view",repo:"gods-eye-view",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"3D 地球開源情報視覺化。",detail:"fork 自上游，在瀏覽器裡用真實公開資料呈現衛星模擬視角，適合當地理資料視覺化的參考。",tags:["3D","OSINT","視覺化"],status:"研究中",github:"https://github.com/rita112025-cpu/gods-eye-view",demo:""},
  {name:"Prd-Governance",repo:"Prd-Governance",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"PRD 治理工作台原型。",detail:"以 Next.js 16、TypeScript、Tailwind CSS、Drizzle 與 Zod 建立的 PRD 管理與治理原型。",tags:["Next.js","PRD","原型"],status:"可用",github:"https://github.com/rita112025-cpu/Prd-Governance",demo:"https://rita112025-cpu.github.io/Prd-Governance/"},
  {name:"rita-ai-workbench-cli-edition",repo:"rita-ai-workbench-cli-edition",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"Rita AI 工作台 CLI／全端版。",detail:"本工作台的 Next.js 全端實驗版本，含 Dockerfile、Caddy 與資料庫設定。",tags:["Next.js","全端","實驗"],status:"整理中",github:"https://github.com/rita112025-cpu/rita-ai-workbench-cli-edition",demo:"https://rita112025-cpu.github.io/rita-ai-workbench-cli-edition/"},
  {name:"taiwan-construction-quote-tools",repo:"construction-quote-tools",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"台灣工程報價工具。",detail:"用於工程報價、材料項目、估價資料整理與比對。",tags:["工程","報價","台灣"],status:"常用",github:"https://github.com/rita112025-cpu/construction-quote-tools",demo:""},
  {name:"tw-construction-quote-parser",repo:"tw-construction-quote-parser",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"工程報價解析器。",detail:"解析工程報價資料，適合搭配 BOQ、標單或廠商報價整理。",tags:["工程","Parser","BOQ"],status:"可用",github:"https://github.com/rita112025-cpu/tw-construction-quote-parser",demo:""},
  {name:"boq-quote-cleaner",repo:"boq-quote-cleaner",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"BOQ 報價清理工具。",detail:"清理 BOQ、報價表、材料項目與格式混亂的工程資料。",tags:["BOQ","報價","清理"],status:"常用",github:"https://github.com/rita112025-cpu/boq-quote-cleaner",demo:""},
  {name:"mep-boq-toolkit",repo:"mep-boq-toolkit",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"機電標單工具組。",detail:"機電標單清整、預算覆核、系統別造價分析與 SAP 對帳的 Python 工具，含 Tkinter GUI。",tags:["機電","標單","Python"],status:"可用",github:"https://github.com/rita112025-cpu/mep-boq-toolkit",demo:""},
  {name:"scada-evidence-site",repo:"scada-evidence-site",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"SCADA 三套 AI 知識庫入口。",detail:"第一套告訴 AI「SCADA 要什麼」，第二套告訴 AI「業主允許怎麼佈」，第三套告訴 AI「哪個證據現在可以信」。",tags:["SCADA","Evidence","知識庫"],status:"常用",github:"https://github.com/rita112025-cpu/scada-evidence-site",demo:"https://rita112025-cpu.github.io/scada-evidence-site/"},
  {name:"evidence-first",repo:"evidence-first",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"SCADA BOQ 分析與證據擷取。",detail:"SCADA 標單分析器、證據資料庫 schema 與擷取模板（Python + SQL），附測試。",tags:["SCADA","BOQ","Python"],status:"整理中",github:"https://github.com/rita112025-cpu/evidence-first",demo:""},
  {name:"scada-revit-guide",repo:"scada-revit-guide",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"Revit MEP／SCADA 開工前設定檢查。",detail:"正式繪製 Cable Tray、Conduit、SCADA 設備前的設定與檢查，每步說明去哪裡按、要檢查什麼、完成標準是什麼。",tags:["Revit","SCADA","Checklist"],status:"可用",github:"https://github.com/rita112025-cpu/scada-revit-guide",demo:"https://rita112025-cpu.github.io/scada-revit-guide/"},
  {name:"navisworks-scada-routing-guide",repo:"navisworks-scada-routing-guide",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"Navisworks SCADA 線槽配置實戰指南。",detail:"現場判斷線槽能否配置：中英對照按鈕位置、剖分／框選、淨空量測與 Clash 檢查，附暗色模式網頁教材。",tags:["Navisworks","SCADA","Clash"],status:"可用",github:"https://github.com/rita112025-cpu/navisworks-scada-routing-guide",demo:"https://rita112025-cpu.github.io/navisworks-scada-routing-guide/"},
  {name:"ct-expansion-guide",repo:"ct-expansion-guide",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"Revit 2027 電纜槽伸縮節族教學。",detail:"從族類別、參數表、參考平面、連接器到載入驗證連通性；每項結論標示官方確認／推測／待實機驗證。數值為示意。",tags:["Revit","Cable Tray","Family"],status:"可用",github:"https://github.com/rita112025-cpu/ct-expansion-guide",demo:"https://rita112025-cpu.github.io/ct-expansion-guide/"},
  {name:"cable-tray-designer",repo:"cable-tray-designer",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"電纜架配置設計器。",detail:"Connector 連接驗證、Route 分析、Auto Elbow 90° 自動插彎頭、2D 草圖 DXF 匯出。純 HTML/JS，免安裝。",tags:["Cable Tray","DXF","工具"],status:"可用",github:"https://github.com/rita112025-cpu/cable-tray-designer",demo:"https://rita112025-cpu.github.io/cable-tray-designer/"},
  {name:"cable-tray-dynamic-block",repo:"cable-tray-dynamic-block",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"AutoCAD 電纜架動態圖塊教學。",detail:"13 步做出長度、角度可變的 Dynamic Block，含預覽、流程圖與卡關排解。",tags:["AutoCAD","Dynamic Block","教學"],status:"可用",github:"https://github.com/rita112025-cpu/cable-tray-dynamic-block",demo:"https://rita112025-cpu.github.io/cable-tray-dynamic-block/"},
  {name:"cable-tray-router",repo:"cable-tray-router",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"AutoLISP Cable Tray 自動路由。",detail:"依路徑自動產生 Straight、Elbow、Tee、Cross 等 fitting，支援不同 SCADA profile 與 tray width。",tags:["AutoLISP","Cable Tray","自動化"],status:"可用",github:"https://github.com/rita112025-cpu/cable-tray-router",demo:"https://rita112025-cpu.github.io/cable-tray-router/"},
  {name:"autocad-router-diagnostics",repo:"autocad-router-diagnostics",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"AutoCAD Router 幾何診斷。",detail:"唯讀擷取 Router fitting、PATH、XDATA、vertices、junction topology 與 connection error，輸出 JSON／CSV／TXT 給人或 AI 分析。",tags:["AutoCAD","診斷","Python"],status:"可用",github:"https://github.com/rita112025-cpu/autocad-router-diagnostics",demo:"https://rita112025-cpu.github.io/autocad-router-diagnostics/"},
  {name:"dwg_batch_tool",repo:"dwg_batch_tool",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"DWG/DXF 批次檢查工具。",detail:"以真實 DWG/DXF 做 100 項 regression 測試，處理誤判／漏判、來源追溯、物件層級彙整、GUI 部分失敗與編碼品質。",tags:["DWG","DXF","批次"],status:"可用",github:"https://github.com/rita112025-cpu/dwg_batch_tool",demo:""},
  {name:"revit-low-voltage-learning-guide",repo:"revit-low-voltage-learning-guide",owner:"rita112025-cpu",category:"學習與資源",description:"Revit 弱電學習指南。",detail:"整理 Revit 弱電系統學習內容，適合工程與 BIM 學習，已有線上展示。",tags:["Revit","弱電","學習"],status:"常用",github:"https://github.com/rita112025-cpu/revit-low-voltage-learning-guide",demo:"https://rita112025-cpu.github.io/revit-low-voltage-learning-guide/"},
  {name:"revit-low-voltage-learning-guide-Literary-Edition",repo:"revit-low-voltage-learning-guide-Literary-Edition",owner:"rita112025-cpu",category:"學習與資源",description:"Revit 弱電學習指南・文學版。",detail:"同一套 Revit 弱電教材的改寫版本，敘事與排版重新設計，適合長時間閱讀與自學。",tags:["Revit","弱電","教材"],status:"可用",github:"https://github.com/rita112025-cpu/revit-low-voltage-learning-guide-Literary-Edition",demo:"https://rita112025-cpu.github.io/revit-low-voltage-learning-guide-Literary-Edition/"},
  {name:"revit-weak-guide",repo:"revit-weak-guide",owner:"rita112025-cpu",category:"學習與資源",description:"Revit 弱電教材。",detail:"Revit 弱電相關補充教材與學習內容。",tags:["Revit","BIM","教材"],status:"可用",github:"https://github.com/rita112025-cpu/revit-weak-guide",demo:"https://rita112025-cpu.github.io/revit-weak-guide/"},
  {name:"astra-3d-resource-hub",repo:"astra-3d-resource-hub",owner:"rita112025-cpu",category:"學習與資源",description:"Astra 3D 資源站。",detail:"整理 Astra、3D、AutoCAD、Revit 或相關 AI 工具資源，已有線上展示。",tags:["Astra","3D","資源"],status:"可用",github:"https://github.com/rita112025-cpu/astra-3d-resource-hub",demo:"https://rita112025-cpu.github.io/astra-3d-resource-hub/"},
  {name:"taiwan-learning-hub",repo:"taiwan-learning-hub",owner:"rita112025-cpu",category:"學習與資源",description:"台灣學習資源入口。",detail:"整理學習資源、工具、教材或技能路線。",tags:["學習","Hub","台灣"],status:"整理中",github:"https://github.com/rita112025-cpu/taiwan-learning-hub",demo:""},
  {name:"stock-prompt-lab",repo:"stock-prompt-lab",owner:"rita112025-cpu",category:"學習與資源",description:"股票 Prompt 實驗工具。",detail:"用於股票分析 Prompt、投資研究流程與資料整理。",tags:["股票","Prompt","Research"],status:"可用",github:"https://github.com/rita112025-cpu/stock-prompt-lab",demo:"https://rita112025-cpu.github.io/stock-prompt-lab/"},
  {name:"stock_public",repo:"stock_public",owner:"rita112025-cpu",category:"學習與資源",description:"台股個股技術分析工作台。",detail:"單一 HTML 檔、零依賴、瀏覽器本機執行。支援 CSV/Big5 匯入，MA/KD/RSI/MACD/布林通道與互動式 K 線圖。",tags:["台股","技術分析","單檔 HTML"],status:"可用",github:"https://github.com/rita112025-cpu/stock_public",demo:"https://rita112025-cpu.github.io/stock_public/tw-stock-analyzer.html"},
  {name:"ai-resource-hub",repo:"ai-resource-hub",owner:"rita112025-cpu",category:"學習與資源",description:"AI 資源整合入口。",detail:"把 Astra 3D Resource Hub 與 Codex Skills Hub 整併成同一套視覺、同一個導覽列與搜尋入口。",tags:["資源","Hub","3D"],status:"可用",github:"https://github.com/rita112025-cpu/ai-resource-hub",demo:"https://rita112025-cpu.github.io/ai-resource-hub/"},
  {name:"fullstack-blueprint",repo:"fullstack-blueprint",owner:"rita112025-cpu",category:"學習與資源",description:"全端自學藍圖。",detail:"全端進階學習藍圖、Git 協作 Checklist 與 SQL 練習台，三份離線可用的自學資料。",tags:["全端","學習","SQL"],status:"可用",github:"https://github.com/rita112025-cpu/fullstack-blueprint",demo:"https://rita112025-cpu.github.io/fullstack-blueprint/"},
  {name:"markdown-upgrade-guide",repo:"markdown-upgrade-guide",owner:"rita112025-cpu",category:"學習與資源",description:"Markdown 教學網站。",detail:"適合初學者學習、可直接部署 GitHub Pages 的一頁式教學網站。",tags:["Markdown","教學","Pages"],status:"可用",github:"https://github.com/rita112025-cpu/markdown-upgrade-guide",demo:"https://rita112025-cpu.github.io/markdown-upgrade-guide/"},
  {name:"Ssdc-Glossary-V5-Final-Unfrozen_-",repo:"Ssdc-Glossary-V5-Final-Unfrozen_-",owner:"rita112025-cpu",category:"學習與資源",description:"技術名詞對照表。",detail:"通用軟體工程術語表，附大字版互動頁，適合查詢與內部溝通對齊用語。",tags:["術語","對照表","軟體工程"],status:"可用",github:"https://github.com/rita112025-cpu/Ssdc-Glossary-V5-Final-Unfrozen_-",demo:"https://rita112025-cpu.github.io/Ssdc-Glossary-V5-Final-Unfrozen_-/"},
  {name:"talkflow-speaking",repo:"talkflow-speaking",owner:"rita112025-cpu",category:"學習與資源",description:"台灣人英語口說練習 App。",detail:"出國情境對話、台式發音特訓、影子跟讀，打開網頁就能開口練。",tags:["英語","口說","PWA"],status:"可用",github:"https://github.com/rita112025-cpu/talkflow-speaking",demo:"https://rita112025-cpu.github.io/talkflow-speaking/"},
  {name:"free-ai-learning-roadmap-tw",repo:"free-ai-learning-roadmap-tw",owner:"rita112025-cpu",category:"學習與資源",description:"免費 AI 課程學習路線。",detail:"10 大官方驗證免費 AI 課程（Anthropic、Google、Microsoft、OpenAI、Hugging Face 等）+ 30 天台北／新北行動計畫，零付費牆。",tags:["AI 課程","免費","學習路線"],status:"可用",github:"https://github.com/rita112025-cpu/free-ai-learning-roadmap-tw",demo:"https://rita112025-cpu.github.io/free-ai-learning-roadmap-tw/"},
  {name:"ai-dev-repo-directory",repo:"ai-dev-repo-directory",owner:"rita112025-cpu",category:"學習與資源",description:"48 個 AI／開發 GitHub 專案導覽。",detail:"涵蓋 AI 核心框架、Agent 自動化、聊天介面、開發工具、學習資源、記憶體與 RAG、資安與 OSINT 七大分類，可搜尋。",tags:["GitHub","導覽","AI"],status:"可用",github:"https://github.com/rita112025-cpu/ai-dev-repo-directory",demo:"https://rita112025-cpu.github.io/ai-dev-repo-directory/"},
  {name:"vibe-coding-vault",repo:"vibe-coding-vault",owner:"rita112025-cpu",category:"學習與資源",description:"Vibe Coding 資源清單儀表板。",detail:"把一張爆紅資源清單截圖整理成可搜尋、可點擊、中英對照的 Notion 風格儀表板。",tags:["Vibe Coding","資源","儀表板"],status:"可用",github:"https://github.com/rita112025-cpu/vibe-coding-vault",demo:"https://rita112025-cpu.github.io/vibe-coding-vault/"},
  {name:"ai-coding-welfare",repo:"ai-coding-welfare",owner:"rita112025-cpu",category:"學習與資源",description:"AI Coding 福利站導航。",detail:"fork 自上游，整理 Claude Code／Codex 中轉站與公益站的額度、模型與價格。第三方服務請自行評估安全性。",tags:["Claude Code","Codex","Fork"],status:"研究中",github:"https://github.com/rita112025-cpu/ai-coding-welfare",demo:""},
  {name:"tainan-trip",repo:"tainan-trip",owner:"rita112025-cpu",category:"生活 / 其他",description:"台南行程 PWA・藍晒圖版。",detail:"工程藍圖紙風格大字版，支援離線、地圖導航、加入主畫面，行程住宿交通一鍵查看。",tags:["PWA","旅遊","離線"],status:"可用",github:"https://github.com/rita112025-cpu/tainan-trip",demo:"https://rita112025-cpu.github.io/tainan-trip/"},
  {name:"tainan-trip_meta",repo:"tainan-trip_meta",owner:"rita112025-cpu",category:"生活 / 其他",description:"台南行程 PWA・溫暖版。",detail:"同一份台南行程的大字溫暖版配色，支援離線、地圖導航與加入主畫面。",tags:["PWA","旅遊","大字版"],status:"可用",github:"https://github.com/rita112025-cpu/tainan-trip_meta",demo:"https://rita112025-cpu.github.io/tainan-trip_meta/"},
  {name:"japan_travel",repo:"japan_travel",owner:"rita112025-cpu",category:"生活 / 其他",description:"沖繩自駕行程 PWA。",detail:"沖繩南國自駕慢遊行程表，離線可用、可加入手機主畫面。",tags:["PWA","沖繩","自駕"],status:"可用",github:"https://github.com/rita112025-cpu/japan_travel",demo:"https://rita112025-cpu.github.io/japan_travel/"},
  {name:"japan_travel_meta",repo:"japan_travel_meta",owner:"rita112025-cpu",category:"生活 / 其他",description:"沖繩自駕行程 PWA・可愛版。",detail:"同一份沖繩行程的可愛版視覺，離線可用、可加入手機主畫面。",tags:["PWA","沖繩","改版"],status:"可用",github:"https://github.com/rita112025-cpu/japan_travel_meta",demo:"https://rita112025-cpu.github.io/japan_travel_meta/"},
  {name:"yijing",repo:"yijing",owner:"rita112025-cpu",category:"生活 / 其他",description:"易經象徵性解讀工具。",detail:"僅供個人自我反思參考，不構成醫療、法律、財務或心理診斷建議。",tags:["易經","自我反思","工具"],status:"可用",github:"https://github.com/rita112025-cpu/yijing",demo:"https://rita112025-cpu.github.io/yijing/"},
  {name:"curated-internet-explorer",repo:"curated-internet-explorer",owner:"rita112025-cpu",category:"生活 / 其他",description:"50 個網路兔子洞。",detail:"50 個讓你一逛就掉進去幾小時的傳奇網站，純靜態前端、中英對照。",tags:["網站","探索","休閒"],status:"可用",github:"https://github.com/rita112025-cpu/curated-internet-explorer",demo:"https://rita112025-cpu.github.io/curated-internet-explorer/"},
  {name:"rita-ai-workbench",repo:"rita-ai-workbench",owner:"rita112025-cpu",category:"工作自動化工具",description:"Rita AI 工作台。",detail:"集中整理 Codex、Claude Code、Prompt、工作自動化與工程工具的一頁式導航網站。",tags:["AI 工作台","工具集合","GitHub Pages"],status:"常用",github:"https://github.com/rita112025-cpu/rita-ai-workbench",demo:"https://rita112025-cpu.github.io/rita-ai-workbench/"},
  {name:"Hyperforge",repo:"Hyperforge",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"瀏覽器本機多模態內容處理實驗。",detail:"在瀏覽器本機整合 OCR、語音轉文字、向量嵌入、知識圖譜與內容變異流程。",tags:["OCR","知識圖譜","本機 AI"],status:"研究中",github:"https://github.com/rita112025-cpu/Hyperforge",demo:""},
  {name:"MEP_tray",repo:"MEP_tray",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"MEP 電纜架工程專案。",detail:"MEP 與 Cable Tray 配置相關的工程實作；目前 GitHub 尚未提供專案簡介。",tags:["MEP","Cable Tray","工程"],status:"整理中",github:"https://github.com/rita112025-cpu/MEP_tray",demo:""},
  {name:"Engineering_Route_Inspector",repo:"Engineering_Route_Inspector",owner:"rita112025-cpu",category:"SCADA / CAD 工程",description:"工程路徑檢查工具。",detail:"工程路徑與配置檢查相關工具；目前 GitHub 尚未提供專案簡介。",tags:["工程","Route","檢查"],status:"整理中",github:"https://github.com/rita112025-cpu/Engineering_Route_Inspector",demo:""},
  {name:"Meitu_Xiuxiu",repo:"Meitu_Xiuxiu",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"瀏覽器本機 AI 修圖與影片工具。",detail:"支援消除、去背、放大、調色與影片去水印，使用 WebGPU、WebCodecs 在瀏覽器內處理，無需上傳或註冊。",tags:["WebGPU","修圖","影片"],status:"可用",github:"https://github.com/rita112025-cpu/Meitu_Xiuxiu",demo:""},
  {name:"neon-serpent",repo:"neon-serpent",owner:"rita112025-cpu",category:"生活 / 其他",description:"霓虹風貪食蛇遊戲。",detail:"完成度高的小型 React 貪食蛇遊戲，適合休閒與前端互動實作參考。",tags:["React","遊戲","貪食蛇"],status:"可用",github:"https://github.com/rita112025-cpu/neon-serpent",demo:""},
  {name:"Pomodoro_Timer",repo:"Pomodoro_Timer",owner:"rita112025-cpu",category:"生活 / 其他",description:"番茄專注計時器。",detail:"以 React、Vite 與 Tailwind CSS 製作的單頁 Pomodoro 應用，協助專注與時間管理。",tags:["Pomodoro","React","生產力"],status:"可用",github:"https://github.com/rita112025-cpu/Pomodoro_Timer",demo:""},
  {name:"coffe_shop",repo:"coffe_shop",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"特色咖啡電商 Web 應用。",detail:"包含六個範例產品、搜尋、分類篩選、商品詳情、購物車、數量更新與模擬結帳，支援桌面與行動版。",tags:["電商","咖啡","響應式"],status:"可用",github:"https://github.com/rita112025-cpu/coffe_shop",demo:""},
  {name:"STAR-WARS-STRIKE",repo:"STAR-WARS-STRIKE",owner:"rita112025-cpu",category:"AI 實驗 / Demo",description:"Snake 改寫成太空射擊的 Web 遊戲。",detail:"保留 neon-serpent 吃光球成長的核心手感，光球改為 TIE 戰機，AI 蛇改為殲星艦。TypeScript + Vite，可直接在瀏覽器遊玩。",tags:["遊戲","TypeScript","Demo"],status:"可用",github:"https://github.com/rita112025-cpu/STAR-WARS-STRIKE",demo:"https://rita112025-cpu.github.io/STAR-WARS-STRIKE/"},
  {name:"aurora-shiftlog-web",repo:"aurora-shiftlog-web",owner:"rita112025-cpu",category:"工作自動化工具",description:"SCADA 工程師工時與任務儀表板。",detail:"Aurora ShiftLog Pro 是給 SCADA／系統整合工程師使用的現代化工時與任務紀錄 Web 應用。",tags:["SCADA","工時","任務管理"],status:"可用",github:"https://github.com/rita112025-cpu/aurora-shiftlog-web",demo:""},
];
const categories = ["常用 Prompt","Codex 工具","Claude Code 分工","工作自動化工具","AI 實驗 / Demo","工程 / 報價工具","SCADA / CAD 工程","學習與資源","生活 / 其他"];
const githubStatusOptions = ["全部狀態","近期有更新","穩定","久未更新","無法讀取","讀取中"];
const grid = document.getElementById("toolsGrid");
const filterRow = document.getElementById("filterRow");
const githubFilterRow = document.getElementById("githubFilterRow");
const searchInput = document.getElementById("searchInput");
const resultInfo = document.getElementById("resultInfo");
const statsRow = document.getElementById("statsRow");
const themeToggle = document.getElementById("themeToggle");
const githubHint = document.getElementById("githubHint");
let activeCategory = "全部";
let activeGithubStatus = "全部狀態";
const CACHE_KEY = "rita-github-cache";
// 未登入的 GitHub API 每小時 60 次，工具數已接近上限，快取拉長避免重新整理就讀不到
const CACHE_TTL = 60*60*1000;
const CACHE_CLOCK_SKEW = 60*1000;
const FUTURE_TIME_TOLERANCE = 24*60*60*1000;
const ISO_TIME_PATTERN = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$/;
const githubDataMap = new Map();
function getSystemTheme(){return window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";}
function getSavedTheme(){try{const saved=localStorage.getItem("rita-theme");return saved==="dark"||saved==="light"?saved:null;}catch{return null;}}
function applyTheme(theme,save){
  document.documentElement.setAttribute("data-theme",theme);
  if(save){try{localStorage.setItem("rita-theme",theme);}catch{}}
  const textEl = themeToggle?.querySelector(".toggle-text");
  if(textEl) textEl.textContent = theme==="dark"?"暗色":"淺色";
}
function initTheme(){
  const saved = getSavedTheme();
  if(saved){applyTheme(saved,true);}else{applyTheme(getSystemTheme(),false);}
  themeToggle?.addEventListener("click",()=>{
    const cur = document.documentElement.getAttribute("data-theme")||"light";
    const next = cur==="dark"?"light":"dark";
    applyTheme(next,true);
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change",(e)=>{
    if(!getSavedTheme()){
      applyTheme(e.matches?"dark":"light",false);
    }
  });
}
// localStorage 與 GitHub API 回應都是不可信輸入：驗證後才使用，畫面一律用 DOM API 寫入
function loadCache(){try{const raw=localStorage.getItem(CACHE_KEY);const cache=raw?JSON.parse(raw):{};return cache&&typeof cache==="object"&&!Array.isArray(cache)?cache:{};}catch{return {};}}
function saveCache(cache){try{localStorage.setItem(CACHE_KEY,JSON.stringify(cache));}catch{}}
function parseTime(value,now){
  if(typeof value!=="string"||!ISO_TIME_PATTERN.test(value)) return null;
  const time=Date.parse(value);
  if(!Number.isFinite(time)||time>now+FUTURE_TIME_TOLERANCE) return null;
  const iso=new Date(time).toISOString();
  return iso.slice(0,19)===value.slice(0,19)?iso:null;
}
function parseCount(value){
  if(typeof value==="string"&&!/^\d+$/.test(value)) return null;
  if(typeof value!=="number"&&typeof value!=="string") return null;
  const count=Number(value);
  return Number.isFinite(count)&&Number.isInteger(count)&&count>=0&&count<=Number.MAX_SAFE_INTEGER?count:null;
}
function normalizeRepoData(raw,now){
  if(!raw||typeof raw!=="object") return null;
  const pushed_at=parseTime(raw.pushed_at,now);
  const open_issues_count=parseCount(raw.open_issues_count);
  if(!pushed_at||open_issues_count===null) return null;
  return {
    name:typeof raw.name==="string"?raw.name:null,
    html_url:typeof raw.html_url==="string"?raw.html_url:null,
    description:typeof raw.description==="string"?raw.description:null,
    updated_at:parseTime(raw.updated_at,now),pushed_at,
    open_issues_count,
    stargazers_count:parseCount(raw.stargazers_count)??0,forks_count:parseCount(raw.forks_count)??0,
    archived:raw.archived===true,disabled:raw.disabled===true,
    error:false
  };
}
function readCachedRepo(cache,repoKey,now){
  const entry=cache[repoKey];
  if(!entry||typeof entry!=="object"||typeof entry.timestamp!=="number"||!Number.isFinite(entry.timestamp)) return null;
  const age=now-entry.timestamp;
  if(age<-CACHE_CLOCK_SKEW||age>=CACHE_TTL) return null;
  return normalizeRepoData(entry.data,now);
}
function getRepoActivityStatus(pushedAt){
  if(!pushedAt) return "無法讀取";
  const diffDays = Math.floor((Date.now()-new Date(pushedAt))/(1000*60*60*24));
  if(diffDays<=30) return "近期有更新";
  if(diffDays<=180) return "穩定";
  return "久未更新";
}
function getGithubActivity(gh){
  if(!gh||gh.loading) return "";
  if(gh.error) return "無法讀取";
  return getRepoActivityStatus(gh.pushed_at);
}
function formatDate(dateStr){if(!dateStr) return "-";try{return new Date(dateStr).toISOString().split("T")[0];}catch{return "-";}}
async function fetchRepoStatus(tool){
  const repoKey = `${tool.owner}/${tool.repo}`;
  const now = Date.now();
  const cached = readCachedRepo(loadCache(),repoKey,now);
  if(cached){githubDataMap.set(tool.repo,cached);return cached;}
  try{
    const url = `https://api.github.com/repos/${tool.owner}/${tool.repo}`;
    const res = await fetch(url,{headers:{"Accept":"application/vnd.github.v3+json"}});
    if(!res.ok){
      const data={error:true,status:res.status,repoKey};
      githubDataMap.set(tool.repo,data);
      return data;
    }
    const data = normalizeRepoData(await res.json(),now);
    if(!data){
      const invalid={error:true,status:res.status,repoKey};
      githubDataMap.set(tool.repo,invalid);
      return invalid;
    }
    githubDataMap.set(tool.repo,data);
    const latest=loadCache();
    latest[repoKey]={data,timestamp:now};
    saveCache(latest);
    return data;
  }catch(e){
    const data={error:true,repoKey,message:e.message};
    githubDataMap.set(tool.repo,data);
    return data;
  }
}
// 一次抓回帳號下所有公開 repo：逐一查 43 個會直接打爆未登入的每小時 60 次額度
async function fetchOwnerRepos(owner,now){
  try{
    const url = `https://api.github.com/users/${owner}/repos?per_page=100&sort=pushed`;
    const res = await fetch(url,{headers:{"Accept":"application/vnd.github.v3+json"}});
    if(!res.ok) return null;
    const list = await res.json();
    if(!Array.isArray(list)) return null;
    const map = new Map();
    const cache = loadCache();
    for(const raw of list){
      if(!raw||typeof raw.name!=="string") continue;
      const data = normalizeRepoData(raw,now);
      if(!data) continue;
      map.set(raw.name.toLowerCase(),data);
      cache[`${owner}/${raw.name}`]={data,timestamp:now};
    }
    saveCache(cache);
    return map;
  }catch{return null;}
}
async function fetchAllStatuses(){
  const now = Date.now();
  const total = tools.length;
  githubHint.textContent="讀取中...";
  const cache = loadCache();
  const pending = tools.filter(t=>{
    const cached = readCachedRepo(cache,`${t.owner}/${t.repo}`,now);
    if(cached){githubDataMap.set(t.repo,cached);return false;}
    return true;
  });
  renderTools();
  const owners = [...new Set(pending.map(t=>t.owner))];
  for(const owner of owners){
    const ownerTools = pending.filter(t=>t.owner===owner);
    // 單一 repo 直接查，多個才值得整批列出
    if(ownerTools.length===1){
      await fetchRepoStatus(ownerTools[0]);
    }else{
      const map = await fetchOwnerRepos(owner,now);
      ownerTools.forEach(t=>{
        const data = map?.get(t.repo.toLowerCase());
        githubDataMap.set(t.repo,data??{error:true,repoKey:`${owner}/${t.repo}`});
      });
    }
    renderTools();
  }
  const failed=[...githubDataMap.values()].filter(d=>d.error).length;
  githubHint.textContent=failed?`完成 ${total-failed}/${total} 成功，${failed} 無法讀取`:`完成 ${total} 個`;
  setTimeout(()=>{githubHint.textContent=`快取 60 分鐘`;},3000);
  renderTools();
}
function el(tag,className,text){
  const node=document.createElement(tag);
  if(className) node.className=className;
  if(text!==undefined) node.textContent=String(text);
  return node;
}
function renderStats(){
  const recent=tools.filter(t=>getGithubActivity(githubDataMap.get(t.repo))==="近期有更新").length;
  const statItem=(label,value)=>{
    const item=el("div","stat-item");
    item.append(el("div","value",value),el("div","label",label));
    return item;
  };
  const heroTotal=document.getElementById("heroTotal");
  if(heroTotal) heroTotal.textContent=String(tools.length);
  statsRow.replaceChildren(statItem("收錄工具",tools.length),statItem("工具分類",categories.length),statItem("30 天內更新",recent));
}
function createFilterButton(label,active,dataKey,onClick,count){
  const btn=el("button",active?"filter-btn active":"filter-btn",label);
  if(count!==undefined) btn.append(el("span","count",count));
  btn.dataset[dataKey]=label;
  btn.addEventListener("click",onClick);
  return btn;
}
function renderFilters(){
  const allCats=["全部",...categories];
  filterRow.replaceChildren(...allCats.map(c=>createFilterButton(c,c===activeCategory,"cat",()=>{
    activeCategory=c;
    renderFilters();
    renderTools();
  },c==="全部"?tools.length:tools.filter(t=>t.category===c).length)));
}
function renderGithubFilters(){
  githubFilterRow.replaceChildren(...githubStatusOptions.map(s=>createFilterButton(s,s===activeGithubStatus,"gh",()=>{
    activeGithubStatus=s;
    renderGithubFilters();
    renderTools();
  })));
}
function getFiltered(){
  const q=searchInput.value.trim().toLowerCase();
  return tools.filter(t=>{
    const matchCat=activeCategory==="全部"||t.category===activeCategory;
    if(!matchCat) return false;
    const gh=githubDataMap.get(t.repo);
    let matchGh=true;
    if(activeGithubStatus!=="全部狀態"){
      if(!gh){matchGh=activeGithubStatus==="讀取中";}
      else if(gh.loading){matchGh=activeGithubStatus==="讀取中";}
      else{matchGh=getGithubActivity(gh)===activeGithubStatus;}
    }
    if(!matchGh) return false;
    if(!q) return true;
    const hay=[t.name,t.repo,t.description,t.detail,t.tags.join(" "),t.category,getGithubActivity(gh)].join(" ").toLowerCase();
    return hay.includes(q);
  });
}
function createGithubLine(label,value,valueClass){
  const line=el("div","gh-line");
  line.append(el("span","gh-label",label),el("span",valueClass?`gh-value ${valueClass}`:"gh-value",value));
  return line;
}
function createGithubStatus(t,gh){
  if(!gh||gh.loading) return el("div","gh-status loading","讀取 GitHub 狀態中...");
  const box=el("div","gh-status");
  if(gh.error){
    box.append(createGithubLine("GitHub 狀態","無法讀取","error"),createGithubLine("Repo",t.repo));
    return box;
  }
  const activity=getGithubActivity(gh);
  box.append(createGithubLine("更新狀態",activity,`activity-${activity}`),createGithubLine("最後 Push",formatDate(gh.pushed_at)),createGithubLine("Issues",gh.open_issues_count));
  return box;
}
function createLinkButton(className,href,label){
  const link=el("a",className,label);
  link.href=href;
  link.target="_blank";
  link.rel="noopener";
  return link;
}
function createGithubCta(href){
  const link=createLinkButton("cta",href,"");
  link.setAttribute("aria-label","GitHub");
  link.append(el("span","cta-pill","GitHub"),el("span","cta-neck"),el("span","cta-dot","→"));
  return link;
}
// 9 格循環在 3 欄時會錯開成對角線，相鄰卡片不會同色
const CARD_COLORS=["orange","yellow","white","white","orange","yellow","yellow","white","orange"];
function createToolCard(t,i){
  const card=el("div",`card card-${CARD_COLORS[i%CARD_COLORS.length]}`);
  const top=el("div","card-top");
  top.append(el("span","card-category",t.category),el("span",`status status-${t.status}`,t.status));
  const tags=el("div","tags");
  tags.append(...t.tags.map(tag=>el("span","tag",tag)));
  const actions=el("div","card-actions");
  actions.append(createGithubCta(t.github));
  if(t.demo) actions.append(createLinkButton("btn-demo",t.demo,"Demo ↗"));
  card.append(top,el("h3","",t.name),el("div","purpose",t.description),el("div","detail",t.detail),tags,createGithubStatus(t,githubDataMap.get(t.repo)),actions);
  return card;
}
function renderTools(){
  const filtered=getFiltered();
  const loadedCount=githubDataMap.size;
  resultInfo.textContent=`顯示 ${filtered.length} / ${tools.length} 個工具${activeCategory!=="全部"?` · 分類：${activeCategory}`:""}${activeGithubStatus!=="全部狀態"?` · GitHub：${activeGithubStatus}`:""}${searchInput.value?` · 搜尋：${searchInput.value}`:""} ${loadedCount>0?`· 已載入 ${loadedCount}`:""}`;
  if(filtered.length===0){
    grid.replaceChildren(el("div","empty","沒有符合條件的工具，試試其他關鍵字或分類"));
    return;
  }
  renderStats();
  grid.replaceChildren(...filtered.map(createToolCard));
}
searchInput.addEventListener("input",renderTools);
initTheme();
renderStats();
renderFilters();
renderGithubFilters();
renderTools();
tools.forEach(t=>githubDataMap.set(t.repo,{loading:true}));
renderTools();
fetchAllStatuses();
