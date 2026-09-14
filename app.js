const tools = [
  {name:"PROMPT-LIBRARY",repo:"PROMPT-LIBRARY",owner:"rita112025-cpu",category:"常用 Prompt",description:"集中管理常用 Prompt。",detail:"放置可重複使用的 Prompt，例如工作分析、報告整理、程式審查、工具規劃等。",tags:["Prompt","Library","AI 工作流"],status:"常用",github:"https://github.com/rita112025-cpu/PROMPT-LIBRARY",demo:"https://rita112025-cpu.github.io/PROMPT-LIBRARY/"},
  {name:"gpt6-astra-prompts",repo:"gpt6-astra-prompts",owner:"rita112025-cpu",category:"常用 Prompt",description:"Astra / GPT-6 相關提示詞整理。",detail:"整理 GPT-6 Astra 使用場景、工具連接、工作流程與進階 Prompt。",tags:["GPT-6","Astra","Prompt"],status:"可用",github:"https://github.com/rita112025-cpu/gpt6-astra-prompts",demo:"https://rita112025-cpu.github.io/gpt6-astra-prompts/"},
  {name:"ai-prompt-deck",repo:"ai-prompt-deck",owner:"rita112025-cpu",category:"常用 Prompt",description:"AI Prompt 簡報與教材素材。",detail:"適合整理成教學、簡報或內部分享內容。",tags:["Prompt","Deck","教材"],status:"可用",github:"https://github.com/rita112025-cpu/ai-prompt-deck",demo:"https://rita112025-cpu.github.io/ai-prompt-deck/"},
    {name:"codex-skills-hub",repo:"codex-skills-hub",owner:"rita112025-cpu",category:"Codex 工具",description:"Codex Skills 入口。",detail:"整理可用的 Codex skills、使用情境、安裝與應用方向。",tags:["Codex","Skills","AI 工具"],status:"常用",github:"https://github.com/rita112025-cpu/codex-skills-hub",demo:"https://rita112025-cpu.github.io/codex-skills-hub/"},
  {name:"local-workspace-mcp",repo:"local-workspace-mcp",owner:"arumwu",category:"Codex 工具",description:"讓 AI 透過 MCP 存取本機檔案、終端程序、Office 文件與多台裝置。",detail:"⚠️ 原生 Windows 不建議使用（含 Unix 專用依賴）；安全性與相容性評估中。Alpha 研究用，勿裝進正式環境；來源為 upstream。",tags:["MCP","本機工作區","Alpha"],status:"研究中",github:"https://github.com/arumwu/local-workspace-mcp",demo:""},
  {name:"claude-dual-session-prompts",repo:"claude-dual-session-prompts",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude Code 多視窗分工 Prompt。",detail:"支援不同 Claude Code 視窗分別負責讀程式、改程式、驗收、整合報告。",tags:["Claude Code","分工","Prompt"],status:"常用",github:"https://github.com/rita112025-cpu/claude-dual-session-prompts",demo:"https://rita112025-cpu.github.io/claude-dual-session-prompts/"},
  {name:"claude-skill-deck",repo:"claude-skill-deck",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude Skill 教材與簡報。",detail:"適合整理 Claude Skills 的概念、應用方式與展示內容。",tags:["Claude","Skill","Deck"],status:"可用",github:"https://github.com/rita112025-cpu/claude-skill-deck",demo:"https://rita112025-cpu.github.io/claude-skill-deck/"},
  {name:"claude-guide-presbyopia-friendly",repo:"Claude-Guide-Presbyopia-Friendly",owner:"rita112025-cpu",category:"Claude Code 分工",description:"Claude 使用指南。",detail:"整理 Claude 使用方式、分工模式與實務操作說明，適合長時間閱讀。",tags:["Claude","Guide","Workflow"],status:"可用",github:"https://github.com/rita112025-cpu/Claude-Guide-Presbyopia-Friendly",demo:"https://rita112025-cpu.github.io/Claude-Guide-Presbyopia-Friendly/"},
  {name:"daily-report-viewer",repo:"daily-report-viewer",owner:"rita112025-cpu",category:"工作自動化工具",description:"日報查看器。",detail:"用於查看、整理或展示工作日報與進度資料。",tags:["日報","Viewer","工作追蹤"],status:"常用",github:"https://github.com/rita112025-cpu/daily-report-viewer",demo:"https://rita112025-cpu.github.io/daily-report-viewer/"},
  {name:"line-summary-docx",repo:"line-summary-docx",owner:"rita112025-cpu",category:"工作自動化工具",description:"LINE 對話摘要轉文件。",detail:"將 LINE 對話或文字紀錄整理成文件格式，適合做會議紀錄、工作摘要或交辦追蹤。",tags:["LINE","DOCX","摘要"],status:"可用",github:"https://github.com/rita112025-cpu/line-summary-docx",demo:""},
  {name:"subtitle_burner",repo:"subtitle_burner",owner:"rita112025-cpu",category:"工作自動化工具",description:"字幕工具。",detail:"處理字幕、逐字稿或影音文字內容，支援燒錄與格式轉換。",tags:["字幕","逐字稿","影音"],status:"可用",github:"https://github.com/rita112025-cpu/subtitle_burner",demo:""},
  {name:"taiwan-construction-quote-tools",repo:"construction-quote-tools",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"台灣工程報價工具。",detail:"用於工程報價、材料項目、估價資料整理與比對。",tags:["工程","報價","台灣"],status:"常用",github:"https://github.com/rita112025-cpu/construction-quote-tools",demo:""},
  {name:"tw-construction-quote-parser",repo:"tw-construction-quote-parser",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"工程報價解析器。",detail:"解析工程報價資料，適合搭配 BOQ、標單或廠商報價整理。",tags:["工程","Parser","BOQ"],status:"可用",github:"https://github.com/rita112025-cpu/tw-construction-quote-parser",demo:""},
  {name:"boq-quote-cleaner",repo:"boq-quote-cleaner",owner:"rita112025-cpu",category:"工程 / 報價工具",description:"BOQ 報價清理工具。",detail:"清理 BOQ、報價表、材料項目與格式混亂的工程資料。",tags:["BOQ","報價","清理"],status:"常用",github:"https://github.com/rita112025-cpu/boq-quote-cleaner",demo:""},
  {name:"revit-low-voltage-learning-guide",repo:"revit-low-voltage-learning-guide",owner:"rita112025-cpu",category:"學習與資源",description:"Revit 弱電學習指南。",detail:"整理 Revit 弱電系統學習內容，適合工程與 BIM 學習，已有線上展示。",tags:["Revit","弱電","學習"],status:"常用",github:"https://github.com/rita112025-cpu/revit-low-voltage-learning-guide",demo:"https://rita112025-cpu.github.io/revit-low-voltage-learning-guide/"},
  {name:"revit-weak-guide",repo:"revit-weak-guide",owner:"rita112025-cpu",category:"學習與資源",description:"Revit 弱電教材。",detail:"Revit 弱電相關補充教材與學習內容。",tags:["Revit","BIM","教材"],status:"可用",github:"https://github.com/rita112025-cpu/revit-weak-guide",demo:"https://rita112025-cpu.github.io/revit-weak-guide/"},
  {name:"astra-3d-resource-hub",repo:"astra-3d-resource-hub",owner:"rita112025-cpu",category:"學習與資源",description:"Astra 3D 資源站。",detail:"整理 Astra、3D、AutoCAD、Revit 或相關 AI 工具資源，已有線上展示。",tags:["Astra","3D","資源"],status:"可用",github:"https://github.com/rita112025-cpu/astra-3d-resource-hub",demo:"https://rita112025-cpu.github.io/astra-3d-resource-hub/"},
  {name:"taiwan-learning-hub",repo:"taiwan-learning-hub",owner:"rita112025-cpu",category:"學習與資源",description:"台灣學習資源入口。",detail:"整理學習資源、工具、教材或技能路線。",tags:["學習","Hub","台灣"],status:"整理中",github:"https://github.com/rita112025-cpu/taiwan-learning-hub",demo:""},
  {name:"stock-prompt-lab",repo:"stock-prompt-lab",owner:"rita112025-cpu",category:"學習與資源",description:"股票 Prompt 實驗工具。",detail:"用於股票分析 Prompt、投資研究流程與資料整理。",tags:["股票","Prompt","Research"],status:"可用",github:"https://github.com/rita112025-cpu/stock-prompt-lab",demo:"https://rita112025-cpu.github.io/stock-prompt-lab/"}
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
function el(tag,className,text){
  const node=document.createElement(tag);
  if(className) node.className=className;
  if(text!==undefined) node.textContent=String(text);
  return node;
}
function renderStats(){
  const counts={};
  categories.forEach(c=>counts[c]=tools.filter(t=>t.category===c).length);
  const statItem=(label,value,className)=>{
    const item=el("div",className);
    item.append(el("div","label",label),el("div","value",value));
    return item;
  };
  statsRow.replaceChildren(...categories.map(c=>statItem(c,counts[c],"stat-item")),statItem("總工具數",tools.length,"stat-item stat-total"));
}
function createFilterButton(label,active,dataKey,onClick){
  const btn=el("button",active?"filter-btn active":"filter-btn",label);
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
  })));
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
  box.append(createGithubLine("更新狀態",activity,`activity-${activity}`),createGithubLine("最後 Push",formatDate(gh.pushed_at)),createGithubLine("Open Issues",gh.open_issues_count));
  return box;
}
function createLinkButton(className,href,label){
  const link=el("a",className,label);
  link.href=href;
  link.target="_blank";
  link.rel="noopener";
  return link;
}
function createToolCard(t){
  const card=el("div","card");
  const top=el("div","card-top");
  top.append(el("span","card-category",t.category),el("span",`status status-${t.status}`,t.status));
  const tags=el("div","tags");
  tags.append(...t.tags.map(tag=>el("span","tag",tag)));
  const actions=el("div","card-actions");
  actions.append(createLinkButton("btn btn-github",t.github,"GitHub"));
  if(t.demo) actions.append(createLinkButton("btn btn-demo",t.demo,"Demo"));
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
