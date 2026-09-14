const tools = [
  {name:"PROMPT-LIBRARY",repo:"PROMPT-LIBRARY",owner:"rita112025-cpu",category:"常用 Prompt",description:"集中管理常用 Prompt。",detail:"放置可重複使用的 Prompt，例如工作分析、報告整理、程式審查、工具規劃等。",tags:["Prompt","Library","AI 工作流"],status:"常用",github:"https://github.com/rita112025-cpu/PROMPT-LIBRARY",demo:""},
  {name:"gpt6-astra-prompts",repo:"gpt6-astra-prompts",owner:"rita112025-cpu",category:"常用 Prompt",description:"Astra / GPT-6 相關提示詞整理。",detail:"整理 GPT-6 Astra 使用場景、工具連接、工作流程與進階 Prompt。",tags:["GPT-6","Astra","Prompt"],status:"可用",github:"https://github.com/rita112025-cpu/gpt6-astra-prompts",demo:""},
  {name:"ai-prompt-deck",repo:"ai-prompt-deck",owner:"rita112025-cpu",category:"常用 Prompt",description:"AI Prompt 簡報與教材素材。",detail:"適合整理成教學、簡報或內部分享內容。",tags:["Prompt","Deck","教材"],status:"可用",github:"https://github.com/rita112025-cpu/ai-prompt-deck",demo:""},
    {name:"codex-skills-hub",repo:"codex-skills-hub",owner:"rita112025-cpu",category:"Codex 工具",description:"Codex Skills 入口。",detail:"整理可用的 Codex skills、使用情境、安裝與應用方向。",tags:["Codex","Skills","AI 工具"],status:"常用",github:"https://github.com/rita112025-cpu/codex-skills-hub",demo:""},
  {name:"local-workspace-mcp",repo:"local-workspace-mcp",owner:"rita112025-cpu",category:"Codex 工具",description:"本機工作區 MCP 工具。",detail:"用來連接本機工作區、檔案、工具或自動化流程。",tags:["MCP","Local","Automation"],status:"整理中",github:"https://github.com/rita112025-cpu/local-workspace-mcp",demo:""},
  {name:"claude-dual-session-prompts",repo:"claude-dual-session-prompts",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude Code 多視窗分工 Prompt。",detail:"支援不同 Claude Code 視窗分別負責讀程式、改程式、驗收、整合報告。",tags:["Claude Code","分工","Prompt"],status:"常用",github:"https://github.com/rita112025-cpu/claude-dual-session-prompts",demo:""},
  {name:"claude-skill-deck",repo:"claude-skill-deck",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude Skill 教材與簡報。",detail:"適合整理 Claude Skills 的概念、應用方式與展示內容。",tags:["Claude","Skill","Deck"],status:"可用",github:"https://github.com/rita112025-cpu/claude-skill-deck",demo:""},
  {name:"claude-guide-presbyopia-friendly",repo:"Claude-Guide-Presbyopia-Friendly",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude 使用指南。",detail:"整理 Claude 使用方式、分工模式與實務操作說明，適合長時間閱讀。",tags:["Claude","Guide","Workflow"],status:"可用",github:"https://github.com/rita112025-cpu/Claude-Guide-Presbyopia-Friendly",demo:""},
  {name:"daily-report-viewer",repo:"daily-report-viewer",owner:"rita112025-cpu",category:"工作自動化工具",description:"日報查看器。",detail:"用於查看、整理或展示工作日報與進度資料。",tags:["日報","Viewer","工作追蹤"],status:"常用",github:"https://github.com/rita112025-cpu/daily-report-viewer",demo:"https://rita112025-cpu.github.io/daily-report-viewer/"},
  {name:"line-summary-docx",repo:"line-summary-docx",owner:"rita112025-cpu",category:"工作自動化工具",description:"LINE 對話摘要轉文件。",detail:"將 LINE 對話或文字紀錄整理成文件格式，適合做會議紀錄、工作摘要或交辦追蹤。",tags:["LINE","DOCX","摘要"],status:"可用",github:"https://github.com/rita112025-cpu/line-summary-docx",demo:""},
  {name:"subtitle_burner",repo:"subtitle_burner",owner:"rita112025-cpu",category:"工作自動化工具",description:"字幕工具。",detail:"處理字幕、逐字稿或影音文字內容，支援燒錄與格式轉換。",tags:["字幕","逐字稿","影音"],status:"可用",github:"https://github.com/rita112025-cpu/subtitle_burner",demo:""},
  {name:"taiwan-construction-quote-tools",repo:"construction-quote-tools",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"台灣工程報價工具。",detail:"用於工程報價、材料項目、估價資料整理與比對。",tags:["工程","報價","台灣"],status:"常用",github:"https://github.com/rita112025-cpu/construction-quote-tools",demo:""},
  {name:"tw-construction-quote-parser",repo:"tw-construction-quote-parser",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"工程報價解析器。",detail:"解析工程報價資料，適合搭配 BOQ、標單或廠商報價整理。",tags:["工程","Parser","BOQ"],status:"可用",github:"https://github.com/rita112025-cpu/tw-construction-quote-parser",demo:""},
  {name:"boq-quote-cleaner",repo:"boq-quote-cleaner",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"BOQ 報價清理工具。",detail:"清理 BOQ、報價表、材料項目與格式混亂的工程資料。",tags:["BOQ","報價","清理"],status:"常用",github:"https://github.com/rita112025-cpu/boq-quote-cleaner",demo:""},
  {name:"revit-low-voltage-learning-guide",repo:"revit-low-voltage-learning-guide",owner:"rita112025-cpu",category:"學習與資源",description:"Revit 弱電學習指南。",detail:"整理 Revit 弱電系統學習內容，適合工程與 BIM 學習，已有線上展示。",tags:["Revit","弱電","學習"],status:"常用",github:"https://github.com/rita112025-cpu/revit-low-voltage-learning-guide",demo:"https://rita112025-cpu.github.io/revit-low-voltage-learning-guide/"},
  {name:"revit-weak-guide",repo:"revit-weak-guide",owner:"rita112025-cpu",category:"學習與資源",description:"Revit 弱電教材。",detail:"Revit 弱電相關補充教材與學習內容。",tags:["Revit","BIM","教材"],status:"可用",github:"https://github.com/rita112025-cpu/revit-weak-guide",demo:""},
  {name:"astra-3d-resource-hub",repo:"astra-3d-resource-hub",owner:"rita112025-cpu",category:"學習與資源",description:"Astra 3D 資源站。",detail:"整理 Astra、3D、AutoCAD、Revit 或相關 AI 工具資源，已有線上展示。",tags:["Astra","3D","資源"],status:"可用",github:"https://github.com/rita112025-cpu/astra-3d-resource-hub",demo:"https://rita112025-cpu.github.io/astra-3d-resource-hub/"},
  {name:"taiwan-learning-hub",repo:"taiwan-learning-hub",owner:"rita112025-cpu",category:"學習與資源",description:"台灣學習資源入口。",detail:"整理學習資源、工具、教材或技能路線。",tags:["學習","Hub","台灣"],status:"整理中",github:"https://github.com/rita112025-cpu/taiwan-learning-hub",demo:""},
  {name:"stock-prompt-lab",repo:"stock-prompt-lab",owner:"rita112025-cpu",category:"學習與資源",description:"股票 Prompt 實驗工具。",detail:"用於股票分析 Prompt、投資研究流程與資料整理。",tags:["股票","Prompt","Research"],status:"可用",github:"https://github.com/rita112025-cpu/stock-prompt-lab",demo:""}
];
const categories = ["常用 Prompt","Codex 工具","Claude Code 分工","工作自動化工具","工程 / 報價工具","學習與資源"];
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
const CACHE_TTL = 15*60*1000;
const githubDataMap = new Map();
function getSystemTheme(){return window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";}
function applyTheme(theme,save){
  document.documentElement.setAttribute("data-theme",theme);
  if(save){localStorage.setItem("rita-theme",theme);}
  const textEl = themeToggle?.querySelector(".toggle-text");
  if(textEl) textEl.textContent = theme==="dark"?"暗色":"淺色";
}
function initTheme(){
  const saved = localStorage.getItem("rita-theme");
  if(saved){applyTheme(saved,true);}else{applyTheme(getSystemTheme(),false);}
  themeToggle?.addEventListener("click",()=>{
    const cur = document.documentElement.getAttribute("data-theme")||"light";
    const next = cur==="dark"?"light":"dark";
    applyTheme(next,true);
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change",(e)=>{
    if(!localStorage.getItem("rita-theme")){
      applyTheme(e.matches?"dark":"light",false);
    }
  });
}
function loadCache(){try{const raw=localStorage.getItem(CACHE_KEY);return raw?JSON.parse(raw):{};}catch{return {};}}
function saveCache(cache){try{localStorage.setItem(CACHE_KEY,JSON.stringify(cache));}catch{}}
function getRepoActivityStatus(pushedAt){
  if(!pushedAt) return "無法讀取";
  const diffDays = Math.floor((Date.now()-new Date(pushedAt))/(1000*60*60*24));
  if(diffDays<=30) return "近期有更新";
  if(diffDays<=180) return "穩定";
  return "久未更新";
}
function formatDate(dateStr){if(!dateStr) return "-";try{return new Date(dateStr).toISOString().split("T")[0];}catch{return "-";}}
async function fetchRepoStatus(tool){
  const repoKey = `${tool.owner}/${tool.repo}`;
  const cache = loadCache();
  const now = Date.now();
  if(cache[repoKey] && (now-cache[repoKey].timestamp<CACHE_TTL)){return cache[repoKey].data;}
  try{
    const url = `https://api.github.com/repos/${tool.owner}/${tool.repo}`;
    const res = await fetch(url,{headers:{"Accept":"application/vnd.github.v3+json"}});
    if(!res.ok){
      const data={error:true,status:res.status,activityStatus:"無法讀取",repoKey};
      githubDataMap.set(tool.repo,data);
      return data;
    }
    const json = await res.json();
    const activityStatus = getRepoActivityStatus(json.pushed_at);
    const data={
      name:json.name,html_url:json.html_url,description:json.description,
      updated_at:json.updated_at,pushed_at:json.pushed_at,
      open_issues_count:json.open_issues_count,
      stargazers_count:json.stargazers_count,forks_count:json.forks_count,
      archived:json.archived,disabled:json.disabled,
      activityStatus,error:false
    };
    githubDataMap.set(tool.repo,data);
    cache[repoKey]={data,timestamp:now};
    saveCache(cache);
    return data;
  }catch(e){
    const data={error:true,activityStatus:"無法讀取",repoKey,message:e.message};
    githubDataMap.set(tool.repo,data);
    return data;
  }
}
async function fetchAllStatuses(){
  let completed=0;
  const total=tools.length;
  githubHint.textContent=`讀取中 0/${total}`;
  const promises = tools.map((tool,idx)=>new Promise(async(resolve)=>{
    await new Promise(r=>setTimeout(r,idx*180));
    const data = await fetchRepoStatus(tool);
    completed++;
    githubHint.textContent=`已讀取 ${completed}/${total}`;
    if(completed===total){
      const failed=[...githubDataMap.values()].filter(d=>d.error).length;
      githubHint.textContent=failed?`完成 ${total-failed}/${total} 成功，${failed} 無法讀取`:`完成 ${total} 個`;
      setTimeout(()=>{githubHint.textContent=`快取 15 分鐘`;},3000);
    }
    renderTools();
    resolve(data);
  }));
  await Promise.allSettled(promises);
}
function renderStats(){
  const counts={};
  categories.forEach(c=>counts[c]=tools.filter(t=>t.category===c).length);
  statsRow.innerHTML=categories.map(c=>`
    <div class="stat-item"><div class="label">${c}</div><div class="value">${counts[c]}</div></div>
  `).join("")+`<div class="stat-item stat-total"><div class="label">總工具數</div><div class="value">${tools.length}</div></div>`;
}
function renderFilters(){
  const allCats=["全部",...categories];
  filterRow.innerHTML=allCats.map(c=>{
    const active=c===activeCategory?"active":"";
    return `<button class="filter-btn ${active}" data-cat="${c}">${c}</button>`;
  }).join("");
  filterRow.querySelectorAll(".filter-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
      activeCategory=btn.dataset.cat;
      renderFilters();
      renderTools();
    });
  });
}
function renderGithubFilters(){
  githubFilterRow.innerHTML=githubStatusOptions.map(s=>{
    const active=s===activeGithubStatus?"active":"";
    return `<button class="filter-btn ${active}" data-gh="${s}">${s}</button>`;
  }).join("");
  githubFilterRow.querySelectorAll(".filter-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
      activeGithubStatus=btn.dataset.gh;
      renderGithubFilters();
      renderTools();
    });
  });
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
      else{matchGh=gh.activityStatus===activeGithubStatus;}
    }
    if(!matchGh) return false;
    if(!q) return true;
    const hay=[t.name,t.repo,t.description,t.detail,t.tags.join(" "),t.category,gh?.activityStatus||""].join(" ").toLowerCase();
    return hay.includes(q);
  });
}
function renderTools(){
  const filtered=getFiltered();
  const loadedCount=githubDataMap.size;
  resultInfo.textContent=`顯示 ${filtered.length} / ${tools.length} 個工具${activeCategory!=="全部"?` · 分類：${activeCategory}`:""}${activeGithubStatus!=="全部狀態"?` · GitHub：${activeGithubStatus}`:""}${searchInput.value?` · 搜尋：${searchInput.value}`:""} ${loadedCount>0?`· 已載入 ${loadedCount}`:""}`;
  if(filtered.length===0){
    grid.innerHTML=`<div class="empty">沒有符合條件的工具，試試其他關鍵字或分類</div>`;
    return;
  }
  grid.innerHTML=filtered.map(t=>{
    const gh=githubDataMap.get(t.repo);
    const demoBtn=t.demo?`<a class="btn btn-demo" href="${t.demo}" target="_blank" rel="noopener">Demo</a>`:"";
    let ghHtml="";
    if(!gh){ghHtml=`<div class="gh-status loading">讀取 GitHub 狀態中...</div>`;}
    else if(gh.loading){ghHtml=`<div class="gh-status loading">讀取 GitHub 狀態中...</div>`;}
    else if(gh.error){ghHtml=`<div class="gh-status"><div class="gh-line"><span class="gh-label">GitHub 狀態</span><span class="gh-value error">無法讀取</span></div><div class="gh-line"><span class="gh-label">Repo</span><span class="gh-value">${t.repo}</span></div></div>`;}
    else{ghHtml=`<div class="gh-status"><div class="gh-line"><span class="gh-label">更新狀態</span><span class="gh-value activity-${gh.activityStatus}">${gh.activityStatus}</span></div><div class="gh-line"><span class="gh-label">最後 Push</span><span class="gh-value">${formatDate(gh.pushed_at)}</span></div><div class="gh-line"><span class="gh-label">Open Issues</span><span class="gh-value">${gh.open_issues_count??0}</span></div></div>`;}
    return `
    <div class="card">
      <div class="card-top"><span class="card-category">${t.category}</span><span class="status status-${t.status}">${t.status}</span></div>
      <h3>${t.name}</h3>
      <div class="purpose">${t.description}</div>
      <div class="detail">${t.detail}</div>
      <div class="tags">${t.tags.map(tag=>`<span class="tag">${tag}</span>`).join("")}</div>
      ${ghHtml}
      <div class="card-actions"><a class="btn btn-github" href="${t.github}" target="_blank" rel="noopener">GitHub</a>${demoBtn}</div>
    </div>
    `;
  }).join("");
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
