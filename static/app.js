const form = document.querySelector("#splitForm");
const pdfInput = document.querySelector("#pdfInput");
const dropzone = document.querySelector("#dropzone");
const fileLabel = document.querySelector("#fileLabel");
const fileMeta = document.querySelector("#fileMeta");
const statusBadge = document.querySelector("#statusBadge");
const resultsPanel = document.querySelector("#resultsPanel");
const errorPanel = document.querySelector("#errorPanel");
const errorText = document.querySelector("#errorText");
const errorMeta = document.querySelector("#errorMeta");
const errorProgress = document.querySelector("#errorProgress");
const errorProgressList = document.querySelector("#errorProgressList");
const saveGeminiProfileButton = document.querySelector("#saveGeminiProfileButton");
const clearGeminiProfileButton = document.querySelector("#clearGeminiProfileButton");
const geminiProfileStatus = document.querySelector("#geminiProfileStatus");
const thumbGrid = document.querySelector("#thumbGrid");
const previewImage = document.querySelector("#previewImage");
const previewName = document.querySelector("#previewName");
const statsRow = document.querySelector("#statsRow");
const downloadButton = document.querySelector("#downloadButton");
const openFolderButton = document.querySelector("#openFolderButton");
const openErrorFolderButton = document.querySelector("#openErrorFolderButton");
const resetButton = document.querySelector("#resetButton");
const manifestLink = document.querySelector("#manifestLink");
const imageForm = document.querySelector("#imageForm");
const imageInput = document.querySelector("#imageInput");
const imageDropzone = document.querySelector("#imageDropzone");
const imageLabel = document.querySelector("#imageLabel");
const imageMeta = document.querySelector("#imageMeta");
const conversionBoard = document.querySelector("#conversionBoard");
const solutionsPanel = document.querySelector("#solutionsPanel");
const solutionForm = document.querySelector("#solutionForm");
const csvInput = document.querySelector("#csvInput");
const csvDropzone = document.querySelector("#csvDropzone");
const csvLabel = document.querySelector("#csvLabel");
const csvMeta = document.querySelector("#csvMeta");
const solutionsStatusBadge = document.querySelector("#solutionsStatusBadge");
const solutionMatchRow = document.querySelector("#solutionMatchRow");
const solutionViewer = document.querySelector("#solutionViewer");
const solutionAnswerDistribution = document.querySelector("#solutionAnswerDistribution");
const solutionNav = document.querySelector("#solutionNav");
const solutionImage = document.querySelector("#solutionImage");
const solutionImageEmpty = document.querySelector("#solutionImageEmpty");
const solutionImageName = document.querySelector("#solutionImageName");
const inlineImageInput = document.querySelector("#inlineImageInput");
const inlineImageUpload = document.querySelector("#inlineImageUpload");
const solutionTitle = document.querySelector("#solutionTitle");
const solutionAnswer = document.querySelector("#solutionAnswer");
const solutionMetrics = document.querySelector("#solutionMetrics");
const solutionDetails = document.querySelector("#solutionDetails");
const solutionOverview = document.querySelector("#solutionOverview");
const solutionQualityStrip = document.querySelector("#solutionQualityStrip");
const solutionOverviewTable = document.querySelector("#solutionOverviewTable");
const solutionClassificationOverview = document.querySelector("#solutionClassificationOverview");
const solutionClassificationPanel = document.querySelector("#solutionClassificationPanel");
const classificationTable = document.querySelector("#classificationTable");
const classificationTools = document.querySelector("#classificationTools");
const classificationSubjectSwitch = document.querySelector("#classificationSubjectSwitch");
const classificationStatus = document.querySelector("#classificationStatus");
const classificationFilenameInput = document.querySelector("#classificationFilename");
const exportClassificationButton = document.querySelector("#exportClassificationButton");
const saveSolutionsButton = document.querySelector("#saveSolutionsButton");
const solutionDirtyBadge = document.querySelector("#solutionDirtyBadge");
const archiveForm = document.querySelector("#archiveForm");
const archiveTitle = document.querySelector("#archiveTitle");
const archiveSubject = document.querySelector("#archiveSubject");
const archiveDate = document.querySelector("#archiveDate");
const archiveMemo = document.querySelector("#archiveMemo");
const archiveStatusBadge = document.querySelector("#archiveStatusBadge");
const archiveMessage = document.querySelector("#archiveMessage");
const refreshArchivesButton = document.querySelector("#refreshArchivesButton");
const archiveList = document.querySelector("#archiveList");
const cutForm = document.querySelector("#cutForm");
const cutSubject = document.querySelector("#cutSubject");
const cutMode = document.querySelector("#cutMode");
const historyExamSelect = document.querySelector("#historyExamSelect");
const loadHistoryButton = document.querySelector("#loadHistoryButton");
const cutModelBadge = document.querySelector("#cutModelBadge");
const cutRelation = document.querySelector("#cutRelation");
const cutPaste = document.querySelector("#cutPaste");
const applyPasteButton = document.querySelector("#applyPasteButton");
const fillDefaultPointsButton = document.querySelector("#fillDefaultPointsButton");
const cutInputGrid = document.querySelector("#cutInputGrid");
const cutResult = document.querySelector("#cutResult");
const cutCardGrid = document.querySelector("#cutCardGrid");
const cutMean = document.querySelector("#cutMean");
const cutError = document.querySelector("#cutError");
const cutScoreTable = document.querySelector("#cutScoreTable");
const cutHistoryTable = document.querySelector("#cutHistoryTable");
const cutRateTable = document.querySelector("#cutRateTable");
const cutWarning = document.querySelector("#cutWarning");
const geminiGenerationPanel = document.querySelector("#geminiGenerationPanel");
const geminiGenerationStatus = document.querySelector("#geminiGenerationStatus");
const geminiGenerationSummary = document.querySelector("#geminiGenerationSummary");
const geminiGenerationLinks = document.querySelector("#geminiGenerationLinks");
const geminiGenerationWarnings = document.querySelector("#geminiGenerationWarnings");
const geminiGenerationProgress = document.querySelector("#geminiGenerationProgress");
const geminiGenerationProgressList = document.querySelector("#geminiGenerationProgressList");
const geminiSubjectInput = form.querySelector('[name="gemini_subject"]');
const geminiApiKeyInput = form.querySelector('[name="gemini_api_key"]');
const geminiModelInput = form.querySelector('[name="gemini_model"]');
const geminiMaxRequestsInput = form.querySelector('[name="gemini_max_requests"]');
const geminiConcurrencyInput = form.querySelector('[name="gemini_concurrency"]');
const geminiPromptInput = form.querySelector('[name="gemini_prompt"]');
const questionSearchForm = document.querySelector("#questionSearchForm");
const questionBankBadge = document.querySelector("#questionBankBadge");
const questionSearchSubject = document.querySelector("#questionSearchSubject");
const questionExamSelect = document.querySelector("#questionExamSelect");
const questionYearFrom = document.querySelector("#questionYearFrom");
const questionYearTo = document.querySelector("#questionYearTo");
const questionSearchMonth = document.querySelector("#questionSearchMonth");
const questionNumber = document.querySelector("#questionNumber");
const questionDifficulty = document.querySelector("#questionDifficulty");
const questionMatchStatus = document.querySelector("#questionMatchStatus");
const questionSearchSort = document.querySelector("#questionSearchSort");
const wrongRateMin = document.querySelector("#wrongRateMin");
const wrongRateMax = document.querySelector("#wrongRateMax");
const questionKeyword = document.querySelector("#questionKeyword");
const questionRefreshButton = document.querySelector("#questionRefreshButton");
const questionSearchResetButton = document.querySelector("#questionSearchResetButton");
const questionPresetButtons = Array.from(document.querySelectorAll("[data-question-preset]"));
const questionSearchMeta = document.querySelector("#questionSearchMeta");
const questionResultGrid = document.querySelector("#questionResultGrid");
const geoToolTabs = Array.from(document.querySelectorAll("[data-geo-tab]"));
const geoToolPanels = Array.from(document.querySelectorAll("[data-geo-panel]"));
const geoToolArea = document.querySelector(".geo-tool-area");
const appJumpButtons = Array.from(document.querySelectorAll("[data-app-jump]"));

let currentJobId = null;
let currentQuestions = [];
let currentSolutions = [];
let currentFieldnames = [];
let currentEncoding = "utf-8-sig";
let currentSolutionNumber = null;
let solutionsDirty = false;
let unitCatalog = {};
let unitCatalogReady = false;
let errorJobId = null;
let errorProgressLog = [];
let splitProgressEventCount = 0;
const GEMINI_PROFILE_STORAGE_KEY = "testauto.gemini_profile_v1";
const appSelectStates = new WeakMap();
let cutModel = null;
let cutModelReady = null;
let lastCutResult = null;
let historicalExams = [];
let lastLoadedHistoryId = null;
let questionBankReady = false;
let questionAvailableExams = [];

const overviewFields = [
  ["예상 정답률", "예상 정답률"],
  ["예측 점수", "예측 점수"],
  ["추정 변별도", "변별도"],
  ["추정 타당도", "타당도"],
  ["오류 가능성", "오류 가능성"],
];

const metricFields = [
  ["예상 정답률", "예상 정답률"],
  ["예측 점수", "예측 점수"],
  ["추정 변별도", "변별도"],
  ["추정 타당도", "타당도"],
  ["오류 가능성", "오류 가능성"],
];

const detailFields = [
  ["해설", "해설"],
  ["정답 풀이", "정답 풀이"],
  ["오답 풀이", "오답 풀이"],
  ["선택 비율 예상", "선택 비율 예상"],
  ["검토 메모(장점)", "검토 메모(장점)"],
  ["검토 메모(약점)", "검토 메모(약점)"],
  ["수정 필요 여부", "수정 필요 여부"],
  ["수정 제안", "수정 제안"],
  ["Comment 제목", "Comment 제목"],
  ["Comment 내용", "Comment 내용"],
];

const classificationSubunitKeys = [1, 2, 3, 4, 5].map((rank) => `소단원 - ${rank}순위`);
const classificationObjectiveKey = "객(1)/주관식(0)";
const classificationKillerKey = "킬러여부\n(해당 없음/준킬러/킬러)";
const classificationDifficultyKey = "난이도\n(1(下下)~9(上上))";
const classificationSubjects = ["세계지리", "한국지리"];
const classificationKeys = [
  "배점",
  "선택과목",
  ...classificationSubunitKeys,
  classificationObjectiveKey,
  classificationKillerKey,
  classificationDifficultyKey,
];

const geminiModelAliases = {
  "gemini-3-flash": "gemini-3-flash-preview",
  "gemini-3-pro": "gemini-3-pro-preview",
  "gemini-3.1-pro": "gemini-3.1-pro-preview",
  "gemini-3.0-flash-preview": "gemini-3-flash-preview",
  "gemini-1.5-flash": "gemini-2.5-flash",
  "gemini-1.5-pro": "gemini-2.5-pro",
};

function normalizeGeminiProfileModel(model) {
  return geminiModelAliases[model] || model;
}

function getAutoGenerationPayload(data) {
  return data?.gemini_auto_generation || data?.auto_generation || null;
}

function clearGeminiGenerationPanel() {
  geminiGenerationPanel.hidden = true;
  geminiGenerationStatus.textContent = "대기";
  geminiGenerationStatus.classList.remove("is-solid");
  geminiGenerationSummary.innerHTML = "";
  geminiGenerationLinks.innerHTML = "";
  if (geminiGenerationProgressList) geminiGenerationProgressList.innerHTML = "";
  if (geminiGenerationProgress) geminiGenerationProgress.hidden = true;
  geminiGenerationWarnings.hidden = true;
  geminiGenerationWarnings.textContent = "";
}

function renderGeminiGenerationTimeline(autoGeneration = null) {
  const requests = Array.isArray(autoGeneration?.requests) ? autoGeneration.requests : [];
  if (!geminiGenerationProgressList || !geminiGenerationProgress) return;
  geminiGenerationProgressList.innerHTML = "";

  if (requests.length === 0) {
    const empty = document.createElement("li");
    const enabled = autoGeneration?.enabled !== false;
    const message = enabled
      ? "요청 로그가 아직 생성되지 않았습니다."
      : `진행 로그가 없습니다. ${autoGeneration?.error || "자동 생성이 미실행되었거나 즉시 실패했습니다."}`;
    empty.className = `app-error-progress-item is-${enabled ? "warning" : "error"}`;
    empty.innerHTML = `<span class="app-error-progress-time">-</span><span>${message}</span>`;
    geminiGenerationProgressList.appendChild(empty);
    geminiGenerationProgress.hidden = false;
    return;
  }

  requests.forEach((requestItem) => {
    const number = requestItem?.question_number ?? "-";
    const status = requestItem?.status || "unknown";
    const elapsed = Number(requestItem?.elapsed_ms);
    const label = status === "ok" ? "성공" : "실패";
    const step = document.createElement("li");
    step.className = `app-error-progress-item is-${status === "ok" ? "success" : "error"}`;

    const time = document.createElement("span");
    time.className = "app-error-progress-time";
    time.textContent = requestItem?.started_at || "";

    const detail = document.createElement("span");
    const elapsedText = Number.isFinite(elapsed) ? ` (${elapsed}ms)` : "";
    const baseText = status === "ok" ? (requestItem?.answer ? `정답 ${requestItem.answer}` : "") : (requestItem?.error || "");
    const attempts = Array.isArray(requestItem?.attempts) ? requestItem.attempts : [];
    const attemptText = attempts.length
      ? `시도: ${attempts.join(" | ")}`
      : "";
    const lineText =
      status === "ok"
        ? baseText || `처리 완료`
        : baseText || requestItem?.status_text || "요청 실패";
    const errorText = status === "ok" ? lineText : `${lineText}${attemptText ? ` / ${attemptText}` : ""}`;
    detail.textContent = `${number}번 문항: ${label} ${elapsedText}${errorText ? ` / ${errorText}` : ""}`;
    step.append(time, detail);
    geminiGenerationProgressList.appendChild(step);
  });
  geminiGenerationProgress.hidden = false;
}

function addGeminiGenerationLink(url, label) {
  if (!url) return;
  const link = document.createElement("a");
  link.className = "tw-button";
  link.textContent = label;
  link.href = url;
  link.target = "_blank";
  link.rel = "noreferrer";
  geminiGenerationLinks.appendChild(link);
}

function renderGeminiGenerationPanel(autoGeneration) {
  if (!autoGeneration) {
    clearGeminiGenerationPanel();
    return;
  }

  geminiGenerationPanel.hidden = false;
  const enabled = autoGeneration.enabled !== false;
  geminiGenerationStatus.textContent = enabled ? "완료" : "미실행";
  geminiGenerationStatus.classList.toggle("is-solid", enabled);

  const requested = Number(autoGeneration.requested ?? 0) || 0;
  const processed = Number(autoGeneration.processed ?? 0) || 0;
  const success = Number(autoGeneration.success ?? 0) || 0;
  const failure = Number(autoGeneration.failure ?? 0) || 0;
  const concurrency = Number(autoGeneration.concurrency ?? 1) || 1;
  const subject = autoGeneration.subject || "미지정";
  const model = autoGeneration.model || "미지정";

  geminiGenerationSummary.innerHTML = "";
  [
    `과목 ${subject}`,
    `모델 ${model}`,
    `요청 ${requested}문항`,
    `동시 ${concurrency}개`,
    `처리 ${processed}문항`,
    `성공 ${success}개`,
    `실패 ${failure}개`,
  ].forEach((item) => {
    const badge = document.createElement("span");
    badge.className = "tw-badge";
    badge.textContent = item;
    geminiGenerationSummary.appendChild(badge);
  });

  geminiGenerationLinks.innerHTML = "";
  addGeminiGenerationLink(autoGeneration.auto_generated_solutions_url || autoGeneration.solutions_path, "auto_generated_solutions.csv");
  addGeminiGenerationLink(autoGeneration.gemini_execution_log_url, "gemini_execution_log.json");
  addGeminiGenerationLink(autoGeneration.predicted_cut_log_url, "predicted_cut_log.json");

  const warnings = [];
  if (autoGeneration.error) warnings.push(autoGeneration.error);
  if (Array.isArray(autoGeneration.warnings)) {
    warnings.push(...autoGeneration.warnings.filter(Boolean));
  }
  const hasNotFound = warnings.some((item) => String(item).includes("NOT_FOUND") || String(item).includes("404"));
  if (hasNotFound) {
    const badge = document.createElement("span");
    badge.className = "tw-badge is-solid";
    badge.textContent = "404 오류: 모델/버전 확인 필요";
    geminiGenerationSummary.appendChild(badge);
  }
  if (warnings.length) {
    geminiGenerationWarnings.hidden = false;
    geminiGenerationWarnings.textContent = warnings.join(" ");
    if (!geminiGenerationWarnings.classList.contains("cut-warning")) {
      geminiGenerationWarnings.classList.add("cut-warning");
    }
  } else {
    geminiGenerationWarnings.hidden = true;
    geminiGenerationWarnings.textContent = "";
  }

  renderGeminiGenerationTimeline(autoGeneration);

  if (autoGeneration.error_code && autoGeneration.enabled === false) {
    const badge = document.createElement("span");
    badge.className = "tw-badge is-solid";
    badge.textContent = `에러 코드: ${autoGeneration.error_code}`;
    geminiGenerationSummary.appendChild(badge);
  }
}

async function applyGeminiAutoResult(data) {
  const autoGeneration = getAutoGenerationPayload(data);
  if (!autoGeneration) {
    clearGeminiGenerationPanel();
    return;
  }

  renderGeminiGenerationPanel(autoGeneration);

  const solutionsPayload = autoGeneration.solutions_payload;
  if (solutionsPayload && solutionsPayload.solutions?.length) {
    renderSolutions(solutionsPayload, false);
  }
  if (autoGeneration.cut_result) {
    renderCutResult(autoGeneration.cut_result);
  } else if (solutionsPayload && solutionsPayload.cut_rates?.length) {
    await applySolutionsToCut(solutionsPayload);
  }
}

function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

function selectedOptionText(select) {
  const option = select?.options?.[select.selectedIndex];
  return option?.textContent?.trim() || select?.dataset?.placeholder || "선택";
}

function closeAppSelectMenus(except = null) {
  document.querySelectorAll(".app-select-menu.is-open").forEach((menu) => {
    if (menu !== except) menu.classList.remove("is-open");
  });
  document.querySelectorAll(".app-select-host.is-open").forEach((host) => {
    if (!except || host !== except.closest(".app-select-host")) host.classList.remove("is-open");
  });
}

function syncAppSelect(select) {
  const state = appSelectStates.get(select);
  if (!state) return;
  state.button.textContent = selectedOptionText(select);
  state.button.disabled = select.disabled;
  state.host.classList.toggle("is-disabled", select.disabled);
  state.menu.querySelectorAll(".app-select-option").forEach((button) => {
    button.classList.toggle("is-selected", button.dataset.value === select.value);
  });
}

function renderAppSelectOptions(select) {
  const state = appSelectStates.get(select);
  if (!state) return;
  state.menu.innerHTML = "";

  const options = Array.from(select.options || []);
  if (!options.length) {
    const empty = document.createElement("span");
    empty.className = "app-select-empty";
    empty.textContent = "선택 항목 없음";
    state.menu.appendChild(empty);
  }

  options.forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "app-select-option";
    button.dataset.value = option.value;
    button.textContent = option.textContent || option.value || "선택";
    button.disabled = option.disabled;
    button.addEventListener("click", () => {
      if (button.disabled) return;
      select.value = option.value;
      select.dispatchEvent(new Event("input", { bubbles: true }));
      select.dispatchEvent(new Event("change", { bubbles: true }));
      closeAppSelectMenus();
      syncAppSelect(select);
    });
    state.menu.appendChild(button);
  });

  syncAppSelect(select);
}

function enhanceAppSelect(select) {
  if (!select || appSelectStates.has(select)) return;
  const host = document.createElement("div");
  host.className = "app-select-host";
  select.before(host);
  host.appendChild(select);
  select.classList.add("app-select-native");

  const button = document.createElement("button");
  button.type = "button";
  button.className = "app-select-button";
  button.setAttribute("aria-haspopup", "listbox");

  const menu = document.createElement("div");
  menu.className = "app-select-menu";
  menu.setAttribute("role", "listbox");

  host.append(button, menu);
  appSelectStates.set(select, { host, button, menu });

  button.addEventListener("click", () => {
    if (select.disabled) return;
    const willOpen = !menu.classList.contains("is-open");
    closeAppSelectMenus(menu);
    menu.classList.toggle("is-open", willOpen);
    host.classList.toggle("is-open", willOpen);
  });
  select.addEventListener("change", () => syncAppSelect(select));

  const observer = new MutationObserver(() => renderAppSelectOptions(select));
  observer.observe(select, { childList: true, subtree: true, attributes: true });
  appSelectStates.get(select).observer = observer;
  renderAppSelectOptions(select);
}

function enhanceAppSelects(root = document) {
  root.querySelectorAll("select").forEach(enhanceAppSelect);
}

function refreshAppSelect(select) {
  if (!select) return;
  if (!appSelectStates.has(select)) {
    enhanceAppSelect(select);
    return;
  }
  renderAppSelectOptions(select);
}

function syncAppSelects(root = document) {
  root.querySelectorAll("select").forEach((select) => {
    if (appSelectStates.has(select)) syncAppSelect(select);
  });
}

function setNativeSelectValue(select, value) {
  if (!select) return;
  select.value = value;
  refreshAppSelect(select);
}

function filenameFromDisposition(disposition) {
  const encoded = String(disposition || "").match(/filename\*=UTF-8''([^;]+)/i);
  if (encoded?.[1]) {
    try {
      return decodeURIComponent(encoded[1].replace(/"/g, ""));
    } catch {
      return encoded[1].replace(/"/g, "");
    }
  }
  const plain = String(disposition || "").match(/filename="?([^";]+)"?/i);
  return plain?.[1] || "";
}

function formatFixed(value, digits = 1) {
  return Number(value).toFixed(digits);
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  }[char]));
}

function formatPercentValue(value) {
  const number = Number(value);
  return Number.isFinite(number) ? `${formatFixed(number)}%` : "-";
}

function formatSigned(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return "-";
  if (number > 0) return `+${number}`;
  return String(number);
}

function rateInputs() {
  return Array.from(cutInputGrid.querySelectorAll("[data-rate-input]"));
}

function pointInputs() {
  return Array.from(cutInputGrid.querySelectorAll("[data-point-input]"));
}

function renderCutRows() {
  cutInputGrid.innerHTML = "";
  for (let index = 0; index < 20; index += 1) {
    const row = document.createElement("div");
    row.className = "cut-row";
    row.innerHTML = `
      <span class="cut-number">${index + 1}</span>
      <label>
        <span>배점</span>
        <input data-point-input type="number" min="1" max="5" step="1" inputmode="numeric" />
      </label>
      <label>
        <span>정답률</span>
        <input data-rate-input type="number" min="0" max="100" step="0.1" inputmode="decimal" />
      </label>
    `;
    cutInputGrid.appendChild(row);
  }
}

function fillDefaultPoints() {
  if (!cutModel) return;
  const points = cutModel.default_points[cutSubject.value] || [];
  pointInputs().forEach((input, index) => {
    input.value = points[index] ?? "";
  });
}

function renderHistoryExamSelect(selectedId = null) {
  if (!historyExamSelect) return;
  const subjectExams = historicalExams.filter((exam) => exam.subject === cutSubject.value);
  historyExamSelect.innerHTML = "";
  if (!subjectExams.length) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "불러올 시험 없음";
    historyExamSelect.appendChild(option);
    historyExamSelect.disabled = true;
    loadHistoryButton.disabled = true;
    refreshAppSelect(historyExamSelect);
    return;
  }

  historyExamSelect.disabled = false;
  loadHistoryButton.disabled = false;
  subjectExams.forEach((exam) => {
    const option = document.createElement("option");
    const cuts = exam.cuts || {};
    const inferred = exam.inferred_count ? ` · 보충 ${exam.inferred_count}문항` : "";
    option.value = exam.id;
    option.textContent = `${exam.label} · ${cuts["1"]}/${cuts["2"]}/${cuts["3"]}${inferred}`;
    historyExamSelect.appendChild(option);
  });
  if (selectedId && subjectExams.some((exam) => exam.id === selectedId)) {
    historyExamSelect.value = selectedId;
  }
  refreshAppSelect(historyExamSelect);
}

function selectedHistoryExam() {
  return historicalExams.find((exam) => exam.id === historyExamSelect.value);
}

function applyHistoryExam() {
  const exam = selectedHistoryExam();
  if (!exam) return;
  lastLoadedHistoryId = exam.id;
  setNativeSelectValue(cutSubject, exam.subject);
  setNativeSelectValue(cutMode, "national");
  renderHistoryExamSelect(exam.id);
  renderRelation();
  pointInputs().forEach((input, index) => {
    input.value = exam.points[index] ?? "";
  });
  rateInputs().forEach((input, index) => {
    input.value = exam.rates[index] ?? "";
  });
  cutPaste.value = exam.rates.map((rate) => formatFixed(rate)).join(", ");
  runCutPrediction();
}

function renderRelation() {
  if (!cutModel) return;
  const rel = cutModel.academy_to_national_rate[cutSubject.value];
  const itemMap = cutModel.item_rate_mapping?.[cutSubject.value];
  let relationText = "문항 환산: 과목별 재종→전국 보정";
  if (
    itemMap?.usable_for_runtime_academy_conversion &&
    itemMap?.method === "pooled_empirical_quantile_with_subject_shrinkage" &&
    itemMap?.counts
  ) {
    const subjectWeight = Math.round((itemMap.subject_weight ?? 0) * 100);
    const counts = itemMap.pooled_counts || itemMap.counts;
    relationText = `문항 환산: 지리 전체 분위수 + 과목 ${subjectWeight}% 보정 · 전체 전국 ${counts.national_rates}개 / 재종 ${counts.academy_rates}개`;
  } else if (itemMap?.usable_for_runtime_academy_conversion && itemMap?.counts) {
    relationText = `문항 환산: 분위수 매칭 · 전국 ${itemMap.counts.national_rates}개 / 재종 ${itemMap.counts.academy_rates}개`;
  } else if (rel.method === "chance_floor_logit") {
    relationText = `${formatFixed(rel.chance_floor, 0)}% 하한 로짓 보정`;
  } else if (rel.method === "linear_with_chance_floor") {
    relationText = `전국 ≈ max(${formatFixed(rel.chance_floor, 0)}%, ${formatFixed(rel.intercept, 2)} + ${formatFixed(rel.slope, 3)}×재종)`;
  }
  cutRelation.innerHTML = `
    <span>${cutSubject.value}</span>
    <strong>${relationText}</strong>
  `;
}

function parseRatesFromPaste() {
  const matches = cutPaste.value.match(/-?\d+(?:\.\d+)?/g) || [];
  const values = matches.slice(0, 20).map(Number);
  rateInputs().forEach((input, index) => {
    if (values[index] !== undefined) input.value = values[index];
  });
}

function setRateInputsFromSolutions(cutRates) {
  const byNumber = new Map((cutRates || []).map((item) => [Number(item.number), item.rate]));
  const values = [];
  rateInputs().forEach((input, index) => {
    const value = byNumber.get(index + 1);
    if (value !== undefined) {
      input.value = value;
      values.push(value);
    } else {
      input.value = "";
    }
  });
  cutPaste.value = values.join(", ");
  return values.length;
}

function collectCutPayload() {
  return {
    subject: cutSubject.value,
    mode: cutMode.value,
    points: pointInputs().map((input) => input.value),
    rates: rateInputs().map((input) => input.value),
  };
}

function setCutBusy(isBusy) {
  cutForm.querySelectorAll("button, input, select, textarea").forEach((element) => {
    element.disabled = isBusy;
  });
  syncAppSelects(cutForm);
  cutModelBadge.textContent = isBusy
    ? "계산 중"
    : `${cutModel ? cutModel.training_records.total : 0}개 학습`;
  cutModelBadge.classList.add("is-solid");
}

function renderCutResult(data) {
  lastCutResult = data;
  cutResult.hidden = false;
  cutCardGrid.innerHTML = "";
  ["1", "2", "3"].forEach((cut) => {
    const item = data.predictions[cut];
    const card = document.createElement("div");
    card.className = "cut-card";
    card.innerHTML = `
      <p class="tw-kicker">${cut} CUT</p>
      <strong>${item.suggested_cut}점</strong>
      <span>연속값 ${formatFixed(item.predicted_cut)}점</span>
      <span>범위 ${item.range_low}~${item.range_high}점</span>
      <span>RMSE ±${formatFixed(item.rmse)}점</span>
    `;
    cutCardGrid.appendChild(card);
  });
  cutMean.textContent = `전국 평균 ${formatFixed(data.features.mean)}점 · 표준편차 ${formatFixed(data.features.nat_sd)}점`;
  cutError.textContent = `가중 정답률 ${formatFixed(data.features.weighted_rate)}%`;
  cutScoreTable.innerHTML = `
    <div class="cut-score-head">
      <span>원점수</span><span>표준점수</span><span>백분위</span><span>구간</span>
    </div>
    ${(data.score_table || []).map((row) => `
      <div class="cut-score-row${row.cut_label ? " is-cut" : ""}">
        <span>${row.raw_score}점</span>
        <span>${row.standard_score}</span>
        <span>${row.percentile}</span>
        <span>${row.cut_label || ""}</span>
      </div>
    `).join("")}
  `;
  cutHistoryTable.innerHTML = `
    <div class="cut-history-head">
      <span>시험</span><span>평균·표편</span><span>실제 컷</span><span>현재-실제</span>
    </div>
    ${(data.historical_matches || []).map((exam) => {
      const cuts = exam.cuts || {};
      const diffs = exam.cut_diffs || {};
      return `
        <div class="cut-history-match${exam.id === lastLoadedHistoryId ? " is-selected" : ""}">
          <span>${exam.exam_year}.${exam.month}</span>
          <span>${formatFixed(exam.mean)} · ${formatFixed(exam.nat_sd)}</span>
          <span>${cuts["1"]}/${cuts["2"]}/${cuts["3"]}</span>
          <span>${formatSigned(diffs["1"])} / ${formatSigned(diffs["2"])} / ${formatSigned(diffs["3"])}</span>
        </div>
      `;
    }).join("")}
  `;
  cutRateTable.innerHTML = `
    <div class="cut-rate-head">
      <span>문항</span><span>배점</span><span>전국</span><span>재종 환산</span>
    </div>
    ${data.conversion_rows.map((row) => `
      <div class="cut-rate-row">
        <span>${row.question}</span>
        <span>${formatFixed(row.points, 0)}</span>
        <span>${formatFixed(row.national_rate)}%</span>
        <span>${row.academy_rate_label}</span>
      </div>
    `).join("")}
  `;
  if (data.warnings.length) {
    cutWarning.textContent = data.warnings.join(" ");
    cutWarning.hidden = false;
  } else {
    cutWarning.hidden = true;
  }
}

async function runCutPrediction() {
  setCutBusy(true);
  try {
    const response = await fetch("/api/cut-predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectCutPayload()),
    });
    const data = await response.json();
    if (!response.ok) {
      cutWarning.textContent = data.error || "예측하지 못했습니다.";
      cutWarning.hidden = false;
      cutResult.hidden = false;
      return false;
    }
    renderCutResult(data);
    return true;
  } catch (error) {
    cutWarning.textContent = error.message;
    cutWarning.hidden = false;
    cutResult.hidden = false;
    return false;
  } finally {
    setCutBusy(false);
  }
}

async function loadCutModel() {
  renderCutRows();
  try {
    const response = await fetch("/api/cut-model");
    cutModel = await response.json();
    cutModelBadge.textContent = `${cutModel.training_records.total}개 학습`;
    cutModelBadge.classList.add("is-solid");
    fillDefaultPoints();
    renderRelation();
  } catch (error) {
    cutModelBadge.textContent = "모델 오류";
    cutRelation.textContent = error.message;
  } finally {
    refreshIcons();
  }
}

async function loadHistoricalExams() {
  try {
    const response = await fetch("/api/historical-exams");
    const data = await response.json();
    historicalExams = data.exams || [];
    renderHistoryExamSelect(lastLoadedHistoryId);
  } catch (error) {
    historicalExams = [];
    renderHistoryExamSelect();
  }
}

function fieldValue(element) {
  return String(element?.value || "").trim();
}

function renderQuestionExamSelect(selectedKey = questionExamSelect.value) {
  if (!questionExamSelect) return;
  const subject = fieldValue(questionSearchSubject);
  const exams = questionAvailableExams.filter((exam) => !subject || exam.subject === subject);
  questionExamSelect.innerHTML = '<option value="">시험 전체</option>';
  exams.forEach((exam) => {
    const option = document.createElement("option");
    const status = `${exam.exact_count}실측`;
    const inferred = exam.inferred_count ? ` · ${exam.inferred_count}보충` : "";
    const unmatched = exam.unmatched_count ? ` · ${exam.unmatched_count}정보없음` : "";
    option.value = exam.key;
    option.textContent = `${exam.label} · ${status}${inferred}${unmatched}`;
    questionExamSelect.appendChild(option);
  });
  if (selectedKey && exams.some((exam) => exam.key === selectedKey)) {
    questionExamSelect.value = selectedKey;
  }
  refreshAppSelect(questionExamSelect);
}

function questionSearchParams() {
  const params = new URLSearchParams();
  const values = [
    ["subject", fieldValue(questionSearchSubject)],
    ["exam_key", fieldValue(questionExamSelect)],
    ["year_from", fieldValue(questionYearFrom)],
    ["year_to", fieldValue(questionYearTo)],
    ["month", fieldValue(questionSearchMonth)],
    ["question", fieldValue(questionNumber)],
    ["difficulty", fieldValue(questionDifficulty)],
    ["match", fieldValue(questionMatchStatus)],
    ["sort", fieldValue(questionSearchSort)],
    ["wrong_min", fieldValue(wrongRateMin)],
    ["wrong_max", fieldValue(wrongRateMax)],
    ["q", fieldValue(questionKeyword)],
    ["limit", "36"],
  ];
  values.forEach(([key, value]) => {
    const text = String(value || "").trim();
    if (text) params.set(key, text);
  });
  return params;
}

function setQuestionSearchBusy(isBusy) {
  if (!questionSearchForm) return;
  questionSearchForm.querySelectorAll("button, input, select").forEach((element) => {
    element.disabled = isBusy;
  });
  syncAppSelects(questionSearchForm);
  if (isBusy) {
    questionBankBadge.textContent = "검색 중";
  }
  questionBankBadge.classList.toggle("is-solid", isBusy || questionBankReady);
}

function questionCardMeta(item) {
  const cuts = item.cuts || {};
  const cutText = cuts["1"] ? `${cuts["1"]}/${cuts["2"]}/${cuts["3"]}` : "-";
  return [
    { text: item.match_label || "정보 없음", className: `is-${item.match_status || "unmatched"}` },
    { text: item.difficulty_label || "난이도 정보 없음", className: `is-${item.difficulty || "unknown"}` },
    { text: `오답률 ${formatPercentValue(item.wrong_rate)}`, className: "is-strong" },
    { text: `정답률 ${formatPercentValue(item.correct_rate)}`, className: "" },
    { text: `${item.points ? formatFixed(item.points, 0) : "-"}점`, className: "" },
    { text: `컷 ${cutText}`, className: "" },
  ];
}

function questionChoiceRates(item) {
  const choices = item.choice_rates || [];
  if (!choices.length) return "";
  return `
    <details class="question-choice-rates">
      <summary>선지별 선택률</summary>
      <div class="question-choice-list">
        ${choices.map((choice) => {
          const rate = Number(choice.rate);
          const width = Number.isFinite(rate) ? Math.max(0, Math.min(100, rate)) : 0;
          const label = `${choice.choice}번${choice.is_answer ? " 정답" : ""}`;
          return `
            <div class="question-choice-rate${choice.is_answer ? " is-answer" : ""}">
              <span>${escapeHtml(label)}</span>
              <div class="question-choice-bar" aria-hidden="true">
                <i style="width: ${width}%"></i>
              </div>
              <strong>${formatPercentValue(rate)}</strong>
            </div>
          `;
        }).join("")}
      </div>
    </details>
  `;
}

function renderQuestionSearchResults(data) {
  questionBankReady = true;
  questionAvailableExams = data.available?.exams || questionAvailableExams;
  renderQuestionExamSelect();
  questionBankBadge.textContent = `${data.total || 0}문항 DB`;
  questionBankBadge.classList.add("is-solid");
  const summary = data.summary?.match || {};
  questionSearchMeta.textContent = `${data.count || 0}개 검색됨 · EBSi ${summary.exact || 0}개 · 보충 ${summary.inferred || 0}개 · 정보 없음 ${summary.unmatched || 0}개 · 최대 ${data.limit || 0}개 표시`;

  const items = data.items || [];
  if (!items.length) {
    questionResultGrid.innerHTML = `
      <div class="question-empty">
        <strong>검색 결과 없음</strong>
      </div>
    `;
    return;
  }

  questionResultGrid.innerHTML = items.map((item) => {
    const meta = questionCardMeta(item);
    return `
      <article class="question-card">
        <a class="question-image-frame" href="${escapeHtml(item.image_url)}" target="_blank" rel="noreferrer">
          <img src="${escapeHtml(item.image_url)}" alt="${escapeHtml(item.label)}" loading="lazy" />
        </a>
        <div class="question-card-body">
          <div class="question-card-title">
            <strong>${escapeHtml(item.subject)} ${item.question}번</strong>
            <span>${escapeHtml(item.exam_label || item.label)} · 시행 ${item.exam_year}.${item.month}</span>
          </div>
          <div class="question-card-badges">
            ${meta.map((badge) => `<span class="${badge.className}">${escapeHtml(badge.text)}</span>`).join("")}
          </div>
          ${questionChoiceRates(item)}
        </div>
      </article>
    `;
  }).join("");
}

async function runQuestionSearch(event = null, refresh = false) {
  if (event) event.preventDefault();
  if (!questionSearchForm) return;
  setQuestionSearchBusy(true);
  try {
    const params = questionSearchParams();
    if (refresh) params.set("refresh", "1");
    const response = await fetch(`/api/question-search?${params.toString()}`);
    const data = await response.json();
    if (!response.ok) {
      questionSearchMeta.textContent = data.error || "검색하지 못했습니다.";
      questionResultGrid.innerHTML = "";
      questionBankBadge.textContent = "DB 오류";
      return;
    }
    renderQuestionSearchResults(data);
  } catch (error) {
    questionSearchMeta.textContent = error.message;
    questionResultGrid.innerHTML = "";
    questionBankBadge.textContent = "DB 오류";
  } finally {
    setQuestionSearchBusy(false);
    refreshIcons();
  }
}

function resetQuestionSearch() {
  questionSearchForm.reset();
  syncAppSelects(questionSearchForm);
  renderQuestionExamSelect();
  runQuestionSearch();
}

function applyQuestionPreset(preset) {
  const subject = fieldValue(questionSearchSubject);
  questionSearchForm.reset();
  questionSearchSubject.value = subject;
  if (preset === "latest_exam") {
    questionSearchMonth.value = "11";
    questionSearchSort.value = "latest";
  } else if (preset === "hard_exact") {
    questionMatchStatus.value = "exact";
    wrongRateMin.value = "45";
    questionSearchSort.value = "wrong_desc";
  } else if (preset === "inferred") {
    questionMatchStatus.value = "inferred";
    questionSearchSort.value = "latest";
  } else if (preset === "unmatched") {
    questionMatchStatus.value = "unmatched";
    questionSearchSort.value = "latest";
  }
  syncAppSelects(questionSearchForm);
  renderQuestionExamSelect();
  runQuestionSearch();
}

function setGeoToolTab(tabName, updateHash = false) {
  const nextTab = tabName === "questions" ? "questions" : "cut";
  geoToolTabs.forEach((button) => {
    const isActive = button.dataset.geoTab === nextTab;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-selected", isActive ? "true" : "false");
  });
  geoToolPanels.forEach((panel) => {
    panel.hidden = panel.dataset.geoPanel !== nextTab;
  });
  setAppJumpActive(nextTab);

  if (updateHash && window.history?.replaceState) {
    window.history.replaceState(
      null,
      "",
      nextTab === "questions" ? "#question-bank" : "#cut-predictor",
    );
  }

  if (nextTab === "questions" && questionSearchForm && !questionBankReady) {
    runQuestionSearch();
  }
}

function setAppJumpActive(target) {
  appJumpButtons.forEach((button) => {
    const isActive = button.dataset.appJump === target;
    button.classList.toggle("is-active", isActive);
    if (isActive) {
      button.setAttribute("aria-current", "true");
    } else {
      button.removeAttribute("aria-current");
    }
  });
}

function scrollToSection(element) {
  if (!element) return;
  const prefersReducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
  element.scrollIntoView({
    block: "start",
    behavior: prefersReducedMotion ? "auto" : "smooth",
  });
}

function jumpToAppSection(target) {
  if (target === "cut" || target === "questions") {
    setGeoToolTab(target, true);
    scrollToSection(geoToolArea);
    return;
  }
  setAppJumpActive(target);
  if (target === "solutions") {
    scrollToSection(solutionsPanel);
    if (window.history?.replaceState) window.history.replaceState(null, "", "#csv-solutions");
    return;
  }
  scrollToSection(conversionBoard);
  if (window.history?.replaceState) window.history.replaceState(null, "", "#image-cutter");
}

function syncAppStateFromHash(hash = window.location.hash) {
  if (hash === "#question-bank") {
    setGeoToolTab("questions");
  } else if (hash === "#cut-predictor") {
    setGeoToolTab("cut");
  } else if (hash === "#csv-solutions") {
    setAppJumpActive("solutions");
  } else if (hash === "#image-cutter") {
    setAppJumpActive("cutter");
  }
}

function setStatus(text, solid = false) {
  statusBadge.textContent = text;
  statusBadge.classList.toggle("is-solid", solid);
}

function setSolutionsStatus(text, solid = false) {
  solutionsStatusBadge.textContent = text;
  solutionsStatusBadge.classList.toggle("is-solid", solid);
}

function setArchiveStatus(text, solid = false) {
  archiveStatusBadge.textContent = text;
  archiveStatusBadge.classList.toggle("is-solid", solid);
}

function showGeminiProfileStatus(message, isError = false) {
  if (!geminiProfileStatus) return;
  geminiProfileStatus.textContent = message || "";
  geminiProfileStatus.style.color = isError ? "var(--tw-ink)" : "";
}

function getGeminiProfileFromForm() {
  return {
    subject: (geminiSubjectInput?.value || "").trim(),
    apiKey: (geminiApiKeyInput?.value || "").trim(),
    model: (geminiModelInput?.value || "").trim(),
    maxRequests: (geminiMaxRequestsInput?.value || "").trim(),
    concurrency: (geminiConcurrencyInput?.value || "").trim(),
    prompt: (geminiPromptInput?.value || "").trim(),
    savedAt: new Date().toISOString(),
  };
}

function applyGeminiProfile(profile) {
  if (!profile || typeof profile !== "object") return;
  if (geminiSubjectInput && profile.subject) geminiSubjectInput.value = profile.subject;
  if (geminiApiKeyInput && profile.apiKey) geminiApiKeyInput.value = profile.apiKey;
  if (geminiModelInput && profile.model) geminiModelInput.value = normalizeGeminiProfileModel(profile.model);
  if (geminiMaxRequestsInput && profile.maxRequests) geminiMaxRequestsInput.value = profile.maxRequests;
  if (geminiConcurrencyInput && profile.concurrency) geminiConcurrencyInput.value = profile.concurrency;
  if (geminiPromptInput && profile.prompt) geminiPromptInput.value = profile.prompt;
  syncAppSelects(form);
}

function clampGeminiConcurrencyForModel() {
  if (!geminiConcurrencyInput || !geminiModelInput) return;
  const model = String(geminiModelInput.value || "").toLowerCase();
  const max = model.includes("pro") ? 2 : 5;
  geminiConcurrencyInput.max = String(max);
  const current = Number(geminiConcurrencyInput.value || 1);
  if (!Number.isFinite(current) || current < 1) {
    geminiConcurrencyInput.value = "1";
  } else if (current > max) {
    geminiConcurrencyInput.value = String(max);
  }
}

function saveGeminiProfile(manual = false) {
  if (!geminiApiKeyInput || !window.localStorage) return;
  const profile = getGeminiProfileFromForm();
  if (!profile.apiKey && !profile.prompt && !manual) return;
  try {
    localStorage.setItem(GEMINI_PROFILE_STORAGE_KEY, JSON.stringify(profile));
    showGeminiProfileStatus("저장했습니다.");
    return true;
  } catch (error) {
    showGeminiProfileStatus("저장 실패: 브라우저 저장소 권한을 확인하세요.", true);
    return false;
  }
}

function clearGeminiProfile() {
  if (!window.localStorage) return;
  try {
    localStorage.removeItem(GEMINI_PROFILE_STORAGE_KEY);
    if (geminiApiKeyInput) geminiApiKeyInput.value = "";
    if (geminiPromptInput) geminiPromptInput.value = "";
    showGeminiProfileStatus("저장 내용 삭제됨.");
    return true;
  } catch {
    showGeminiProfileStatus("삭제 실패: 브라우저 저장소 권한을 확인하세요.", true);
    return false;
  }
}

function restoreGeminiProfile() {
  if (!window.localStorage) return;
  try {
    const raw = localStorage.getItem(GEMINI_PROFILE_STORAGE_KEY);
    if (!raw) return;
    const profile = JSON.parse(raw);
    applyGeminiProfile(profile);
    showGeminiProfileStatus("저장된 Gemini 설정을 불러왔습니다.");
  } catch (error) {
    showGeminiProfileStatus("저장된 설정을 불러오지 못했습니다.", true);
  }
}

async function loadGeminiDefaults() {
  try {
    const response = await fetch("/api/gemini-defaults", { cache: "no-store" });
    if (!response.ok) return;
    const defaults = await response.json();
    if (geminiSubjectInput && defaults.subject) geminiSubjectInput.value = defaults.subject;
    if (geminiModelInput && defaults.model) geminiModelInput.value = normalizeGeminiProfileModel(defaults.model);
    if (geminiMaxRequestsInput && defaults.max_requests && !geminiMaxRequestsInput.value) {
      geminiMaxRequestsInput.value = defaults.max_requests;
    }
    if (geminiConcurrencyInput && defaults.concurrency) {
      geminiConcurrencyInput.value = defaults.concurrency;
    }
    clampGeminiConcurrencyForModel();
    if (geminiPromptInput && defaults.prompt) {
      geminiPromptInput.value = defaults.prompt;
    }
    if (geminiApiKeyInput && defaults.has_api_key) {
      geminiApiKeyInput.placeholder = "서버 기본 키 사용 중";
    }
    const keyStatus = defaults.has_api_key ? "서버 기본 키 적용됨" : "API 키를 입력하거나 저장하세요";
    showGeminiProfileStatus(`${keyStatus} · 기본 프롬프트 준비됨`);
    syncAppSelects(form);
  } catch {
    // 기본값 로딩 실패는 수동 입력 흐름을 막지 않는다.
  }
}

function setSolutionsDirty(isDirty) {
  solutionsDirty = isDirty;
  solutionDirtyBadge.hidden = !isDirty;
  saveSolutionsButton.disabled = !currentJobId || !currentSolutions.length || !isDirty;
  if (exportClassificationButton) {
    exportClassificationButton.disabled = !currentJobId || !currentSolutions.length;
  }
  if (isDirty) setSolutionsStatus("수정 중", false);
}

function hideError() {
  errorPanel.hidden = true;
  errorText.textContent = "";
  errorMeta.textContent = "";
  errorProgressLog = [];
  splitProgressEventCount = 0;
  if (errorProgressList) errorProgressList.innerHTML = "";
  errorJobId = null;
  openErrorFolderButton.hidden = true;
}

function formatErrorTime() {
  return new Date().toLocaleTimeString("ko-KR", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function formatProgressTime(value) {
  if (!value) return formatErrorTime();
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return String(value).slice(11, 19) || formatErrorTime();
  return parsed.toLocaleTimeString("ko-KR", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function addErrorProgress(message, level = "info", timestamp = null) {
  const text = String(message || "").trim();
  if (!errorProgressList) return;
  if (!text) return;

  const step = document.createElement("li");
  step.className = `app-error-progress-item is-${level}`;

  const time = document.createElement("span");
  time.className = "app-error-progress-time";
  time.textContent = timestamp ? formatProgressTime(timestamp) : formatErrorTime();

  const content = document.createElement("span");
  content.textContent = text;

  step.append(time, content);
  errorProgressList.appendChild(step);
  errorProgressList.scrollTop = errorProgressList.scrollHeight;

  errorProgressLog.push({ time: time.textContent, message: text, level });
  if (errorProgressLog.length > 60) {
    errorProgressLog = errorProgressLog.slice(-60);
    while (errorProgressList.children.length > 60) {
      errorProgressList.removeChild(errorProgressList.children[0]);
    }
  }
}

function showProgressPanel() {
  errorPanel.hidden = false;
  errorText.textContent = "";
  errorMeta.textContent = "작업 준비 중";
  openErrorFolderButton.hidden = true;
  window.requestAnimationFrame(() => scrollToSection(errorPanel));
}

function sleep(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function renderSplitProgress(progress) {
  if (!progress || typeof progress !== "object") return;
  const events = Array.isArray(progress.events) ? progress.events : [];
  events.slice(splitProgressEventCount).forEach((event) => {
    addErrorProgress(event.message, event.level || "info", event.time);
  });
  splitProgressEventCount = events.length;

  const percent = Number(progress.progress);
  const percentText = Number.isFinite(percent) ? `진행률: ${Math.max(0, Math.min(100, percent))}%` : "";
  const stage = progress.stage ? `단계: ${progress.stage}` : "";
  const job = progress.job_id ? `Job ID: ${progress.job_id}` : "";
  errorMeta.textContent = [stage, percentText, job].filter(Boolean).join(" | ");

  if (progress.status === "completed") {
    setStatus("완료", true);
  } else if (progress.status === "failed") {
    setStatus("오류", false);
  } else if (progress.stage === "GEMINI") {
    setStatus("Gemini 생성 중", true);
  } else {
    setStatus("처리 중", true);
  }
}

async function pollSplitJob(statusUrl) {
  while (true) {
    const response = await fetch(statusUrl, { cache: "no-store" });
    const progress = await response.json();
    if (!response.ok) {
      throw Object.assign(new Error(progress.error || "작업 상태를 읽지 못했습니다."), {
        details: {
          stage: "상태 확인",
          status: response.status,
          statusText: response.statusText,
          url: statusUrl,
        },
      });
    }
    renderSplitProgress(progress);
    if (progress.status === "completed") {
      if (!progress.result) {
        throw Object.assign(new Error("완료된 작업 결과를 찾지 못했습니다."), {
          jobId: progress.job_id,
          details: { stage: "결과 확인", url: statusUrl },
        });
      }
      return progress.result;
    }
    if (progress.status === "failed") {
      const errorPayload = progress.error || {};
      throw Object.assign(new Error(errorPayload.error || progress.message || "작업이 실패했습니다."), {
        jobId: progress.job_id,
        details: {
          stage: errorPayload.error_stage || progress.stage || "작업 실행",
          status: errorPayload.status,
          error_code: errorPayload.error_code,
          debug_url: errorPayload.debug_url,
          message: errorPayload.error || progress.message || "",
          url: statusUrl,
        },
      });
    }
    await sleep(850);
  }
}

function normalizeNetworkError(error) {
  const text = String(error?.message || error || "");
  if (text.includes("Failed to fetch") || text === "Load failed") {
    return {
      message: "127.0.0.1:5057 에 연결하지 못했습니다. 서버가 중지되어 있거나 포트가 열리지 않았습니다.",
      hint: "로컬 터미널에서 python3 app.py 를 실행한 뒤 브라우저를 다시 열어주세요. 기본 URL은 http://127.0.0.1:5057/ 입니다.",
      stage: "요청 전송",
      url: "/api/split",
      status: 0,
    };
  }
  if (text === "NetworkError when attempting to fetch resource.") {
    return {
      message: "네트워크 요청이 중단되었습니다. 파일 크기, 프록시, 방화벽 설정을 확인해 주세요.",
      stage: "요청 전송",
      url: "/api/split",
      status: 0,
    };
  }
  return { message: text, stage: "요청 전송", url: "/api/split" };
}

function showError(message, jobId = null, details = null) {
  errorJobId = jobId;
  const normalized = String(message || "오류가 발생했습니다.");
  errorText.textContent = normalized;
  const summary = [];
  if (details?.stage) summary.push(`단계: ${details.stage}`);
  if (details?.status) summary.push(`HTTP: ${details.status}${details?.statusText ? ` ${details.statusText}` : ""}`);
  if (jobId) summary.push(`Job ID: ${jobId}`);
  if (details?.error_code) summary.push(`ErrorCode: ${details.error_code}`);
  if (details?.url) summary.push(`URL: ${details.url}`);
  if (details?.debug_url) summary.push(`DEBUG: ${details.debug_url}`);
  if (details?.hint) summary.push(`조치: ${details.hint}`);
  if (details?.message) summary.push(`원인: ${details.message}`);
  errorMeta.textContent = summary.join(" | ");
  addErrorProgress(normalized, "error");
  if (details?.stage) addErrorProgress(`실패 단계: ${details.stage}`, "warning");
  if (details?.debug_url) addErrorProgress(`디버그 경로: ${details.debug_url}`, "info");
  if (details?.hint) addErrorProgress(`권장 조치: ${details.hint}`, "warning");
  openErrorFolderButton.hidden = !jobId;
  errorPanel.hidden = false;
  window.requestAnimationFrame(() => scrollToSection(errorPanel));
  setStatus("오류", false);
  refreshIcons();
}

function formatBytes(bytes) {
  if (!bytes && bytes !== 0) return "";
  const units = ["B", "KB", "MB", "GB"];
  let value = bytes;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value.toFixed(unit === 0 ? 0 : 1)} ${units[unit]}`;
}

function updateFileLabel(file) {
  if (!file) {
    fileLabel.textContent = "PDF 선택";
    fileMeta.textContent = "파일을 여기에 놓아도 됩니다";
    return;
  }
  fileLabel.textContent = file.name;
  fileMeta.textContent = formatBytes(file.size);
}

function updateCsvLabel(file) {
  if (!file) {
    csvLabel.textContent = "CSV 선택";
    csvMeta.textContent = "문항 번호 기준 매칭";
    return;
  }
  csvLabel.textContent = file.name;
  csvMeta.textContent = formatBytes(file.size);
}

function updateImageLabel(files) {
  const list = Array.from(files || []);
  if (!list.length) {
    imageLabel.textContent = "문항 이미지 선택";
    imageMeta.textContent = "파일명 순서대로 q01, q02… 저장";
    return;
  }
  imageLabel.textContent = `${list.length}개 이미지 선택`;
  imageMeta.textContent = list.map((file) => file.name).slice(0, 3).join(", ")
    + (list.length > 3 ? ` 외 ${list.length - 3}개` : "");
}

function setBusy(isBusy) {
  form.querySelectorAll("button, input, select, textarea").forEach((element) => {
    if (element !== resetButton) element.disabled = isBusy;
  });
  setStatus(isBusy ? "처리 중" : "대기", isBusy);
}

function setSolutionsBusy(isBusy) {
  solutionForm.querySelectorAll("button, input").forEach((element) => {
    element.disabled = isBusy;
  });
  saveSolutionsButton.disabled = isBusy || !currentJobId || !currentSolutions.length || !solutionsDirty;
  if (isBusy) {
    setSolutionsStatus("적용 중", true);
  }
}

function setImageBusy(isBusy) {
  imageForm.querySelectorAll("button, input").forEach((element) => {
    element.disabled = isBusy;
  });
  if (inlineImageInput) inlineImageInput.disabled = isBusy;
  if (inlineImageUpload) inlineImageUpload.classList.toggle("is-busy", isBusy);
  setStatus(isBusy ? "이미지 적용 중" : "대기", isBusy);
}

function setPreview(item, button) {
  previewImage.src = item.url;
  previewName.textContent = item.name;
  thumbGrid.querySelectorAll(".app-thumb").forEach((node) => {
    node.classList.remove("is-active");
  });
  if (button) button.classList.add("is-active");
}

function renderStats(data) {
  statsRow.innerHTML = "";
  [
    `${data.count}개`,
    `${data.dpi} dpi`,
    data.job_id,
  ].forEach((text, index) => {
    const badge = document.createElement("span");
    badge.className = `tw-badge${index === 0 ? " is-solid" : ""}`;
    badge.textContent = text;
    statsRow.appendChild(badge);
  });
}

function resetSolutions(keepPanel = false) {
  currentSolutions = [];
  currentFieldnames = [];
  currentEncoding = "utf-8-sig";
  currentSolutionNumber = null;
  csvInput.value = "";
  solutionViewer.hidden = true;
  solutionMatchRow.hidden = true;
  solutionMatchRow.innerHTML = "";
  solutionNav.innerHTML = "";
  solutionMetrics.innerHTML = "";
  solutionDetails.innerHTML = "";
  solutionOverview.hidden = true;
  if (solutionAnswerDistribution) {
    solutionAnswerDistribution.hidden = true;
    solutionAnswerDistribution.innerHTML = "";
  }
  if (solutionQualityStrip) {
    solutionQualityStrip.hidden = true;
    solutionQualityStrip.innerHTML = "";
  }
  solutionOverviewTable.innerHTML = "";
  if (solutionClassificationOverview) solutionClassificationOverview.hidden = true;
  if (solutionClassificationPanel) solutionClassificationPanel.innerHTML = "";
  if (classificationTable) classificationTable.innerHTML = "";
  if (exportClassificationButton) exportClassificationButton.disabled = true;
  solutionImage.removeAttribute("src");
  solutionImage.hidden = true;
  solutionImageEmpty.hidden = false;
  solutionImageName.textContent = "q01.png";
  if (inlineImageInput) inlineImageInput.value = "";
  updateCsvLabel(null);
  setSolutionsStatus("대기", false);
  setSolutionsDirty(false);
}

function questionForNumber(number) {
  return currentQuestions.find((item) => Number(item.number) === Number(number));
}

function solutionForNumber(number) {
  return currentSolutions.find((item) => Number(item.number) === Number(number));
}

function createMatchBadge(text, solid = false) {
  const badge = document.createElement("span");
  badge.className = `tw-badge${solid ? " is-solid" : ""}`;
  badge.textContent = text;
  return badge;
}

function parseQuestionNumber(text) {
  const match = String(text || "").match(/\d+/);
  return match ? Number(match[0]) : null;
}

function parseRatePercent(text) {
  const match = String(text || "").match(/\d+(?:\.\d+)?/);
  if (!match) return null;
  const value = Number(match[0]);
  return value >= 0 && value <= 100 ? value : null;
}

function normalizeAnswerValue(value) {
  const text = String(value ?? "").trim();
  if (!text) return "";
  const circled = {
    "①": "1",
    "②": "2",
    "③": "3",
    "④": "4",
    "⑤": "5",
    "❶": "1",
    "❷": "2",
    "❸": "3",
    "❹": "4",
    "❺": "5",
    "➀": "1",
    "➁": "2",
    "➂": "3",
    "➃": "4",
    "➄": "5",
    "１": "1",
    "２": "2",
    "３": "3",
    "４": "4",
    "５": "5",
  };
  for (const [symbol, digit] of Object.entries(circled)) {
    if (text.includes(symbol)) return digit;
  }
  const match = text.match(/[1-5]/);
  return match ? match[0] : text;
}

function normalizeScoreValue(value) {
  const text = String(value ?? "").trim();
  if (!text) return "";
  const match = text.match(/\d+(?:\.\d+)?/);
  return match ? match[0] : text;
}

function normalizeRiskValue(value) {
  const text = String(value ?? "").trim();
  if (!text) return "";
  const compact = text.replace(/\s+/g, "");
  if (
    compact.includes("낮")
    || compact.includes("없")
    || compact.includes("높지않")
    || compact.includes("높지는않")
  ) {
    return "낮음";
  }
  if (compact.includes("높") || compact.includes("큼")) return "높음";
  if (compact.includes("중") || compact.includes("보통")) return "보통";
  return text.split(/[\s,./:;|]+/, 1)[0];
}

function normalizeSolutionField(key, value) {
  if (key === "정답") return normalizeAnswerValue(value);
  if (key === "추정 변별도" || key === "추정 타당도") return normalizeScoreValue(value);
  if (key === "오류 가능성") return normalizeRiskValue(value);
  return String(value ?? "");
}

function normalizeSolutionRecord(solution) {
  const fields = { ...(solution.fields || {}) };
  Object.keys(fields).forEach((key) => {
    fields[key] = normalizeSolutionField(key, fields[key]);
  });
  return { ...solution, fields };
}

function ensureClassificationFieldnames() {
  currentFieldnames = Array.from(new Set(["문항 번호", ...currentFieldnames, ...classificationKeys]));
}

function defaultClassificationSubject() {
  const fromCurrent = solutionForNumber(currentSolutionNumber)?.fields?.["선택과목"];
  const fromArchive = archiveSubject?.value;
  const subject = [fromCurrent, fromArchive].find((item) =>
    classificationSubjects.includes(String(item || "").trim()),
  );
  return subject || "세계지리";
}

function normalizeClassificationFilename(value) {
  let filename = String(value || "").trim().replace(/[\\/:*?"<>|]+/g, "_");
  filename = filename.replace(/\s+/g, " ").replace(/^\.+|\.+$/g, "");
  if (!filename) filename = "문항분류표.xlsx";
  if (!filename.toLowerCase().endsWith(".xlsx")) filename = `${filename}.xlsx`;
  return filename;
}

function ensureClassificationFilename() {
  if (!classificationFilenameInput) return "문항분류표.xlsx";
  const filename = normalizeClassificationFilename(classificationFilenameInput.value);
  if (!classificationFilenameInput.value.trim()) classificationFilenameInput.value = filename;
  return filename;
}

function classificationSubjectForSolution(solution) {
  const subject = String(solution?.fields?.["선택과목"] || "").trim();
  return classificationSubjects.includes(subject) ? subject : defaultClassificationSubject();
}

function defaultPointForSolution(solution) {
  const subject = classificationSubjectForSolution(solution);
  const number = Number(solution?.number);
  const points = cutModel?.default_points?.[subject] || [];
  const value = points[number - 1];
  return value === undefined || value === null ? "" : String(value);
}

function ensureClassificationFields(solution) {
  if (!solution) return;
  ensureClassificationFieldnames();
  solution.fields ||= {};
  if (!solution.fields["선택과목"]) solution.fields["선택과목"] = defaultClassificationSubject();
  if (!solution.fields["배점"]) solution.fields["배점"] = defaultPointForSolution(solution);
  if (!solution.fields[classificationObjectiveKey]) solution.fields[classificationObjectiveKey] = "1";
  classificationSubunitKeys.forEach((key) => {
    if (solution.fields[key] === undefined) solution.fields[key] = "";
  });
  if (solution.fields[classificationKillerKey] === undefined) solution.fields[classificationKillerKey] = "";
  if (solution.fields[classificationDifficultyKey] === undefined) solution.fields[classificationDifficultyKey] = "";
}

function ensureAllClassificationFields() {
  ensureClassificationFieldnames();
  currentSolutions.forEach(ensureClassificationFields);
}

function unitsForSubject(subject) {
  return unitCatalog?.[subject]?.units || [];
}

function compactUnitLabel(value) {
  return String(value || "").replace(/^(\d+-\d+-\d+)\.\s+/, "$1.");
}

function unitDisplayText(unit) {
  return compactUnitLabel(unit?.label || unit?.name || "");
}

function closeClassificationMenus(except = null) {
  document.querySelectorAll(".classification-unit-menu.is-open").forEach((menu) => {
    if (menu !== except) menu.classList.remove("is-open");
  });
}

function renderUnitMenuOptions(menu, solution, key, filterText = "") {
  const list = menu.querySelector(".classification-unit-options");
  if (!list) return;
  const subject = classificationSubjectForSolution(solution);
  const query = String(filterText || "").trim().toLowerCase();
  const units = unitsForSubject(subject).filter((unit) => {
    const haystack = [unit.code, unit.name, unit.label, unitDisplayText(unit)].filter(Boolean).join(" ").toLowerCase();
    return !query || haystack.includes(query);
  });

  list.innerHTML = "";
  const emptyButton = document.createElement("button");
  emptyButton.type = "button";
  emptyButton.className = "classification-unit-option is-empty";
  emptyButton.textContent = "선택 해제";
  emptyButton.addEventListener("click", () => {
    setClassificationField(solution, key, "", { refreshOverview: true });
    closeClassificationMenus();
  });
  list.appendChild(emptyButton);

  units.forEach((unit) => {
    const option = document.createElement("button");
    option.type = "button";
    option.className = "classification-unit-option";
    option.textContent = unitDisplayText(unit);
    option.title = unitDisplayText(unit);
    option.addEventListener("click", () => {
      setClassificationField(solution, key, unitDisplayText(unit), { refreshOverview: true });
      closeClassificationMenus();
    });
    list.appendChild(option);
  });

  if (!units.length) {
    const empty = document.createElement("span");
    empty.className = "classification-unit-empty";
    empty.textContent = "검색 결과 없음";
    list.appendChild(empty);
  }
}

function buildUnitPicker(solution, key, label = "") {
  const wrapper = document.createElement("div");
  wrapper.className = "classification-unit-cell";
  if (label) {
    const span = document.createElement("span");
    span.className = "classification-unit-label";
    span.textContent = label;
    wrapper.appendChild(span);
  }

  const button = document.createElement("button");
  button.type = "button";
  button.className = "classification-unit-picker";
  const current = solution.fields?.[key] || "";
  button.textContent = current || "소단원 선택";
  button.title = current || "소단원 선택";

  const menu = document.createElement("div");
  menu.className = "classification-unit-menu";

  const search = document.createElement("input");
  search.type = "search";
  search.className = "classification-unit-search";
  search.placeholder = "소단원 검색";

  const options = document.createElement("div");
  options.className = "classification-unit-options";
  menu.append(search, options);
  renderUnitMenuOptions(menu, solution, key);

  button.addEventListener("click", () => {
    const willOpen = !menu.classList.contains("is-open");
    closeClassificationMenus(menu);
    menu.classList.toggle("is-open", willOpen);
    if (willOpen) {
      search.value = "";
      renderUnitMenuOptions(menu, solution, key);
      search.focus();
    }
  });

  search.addEventListener("input", () => renderUnitMenuOptions(menu, solution, key, search.value));

  wrapper.append(button, menu);
  return wrapper;
}

function setClassificationSubjectForAll(subject) {
  if (!classificationSubjects.includes(subject)) return;
  currentSolutions.forEach((solution) => {
    ensureClassificationFields(solution);
    if (solution.fields["선택과목"] !== subject) {
      solution.fields["선택과목"] = subject;
      classificationSubunitKeys.forEach((key) => {
        solution.fields[key] = "";
      });
      const defaultPoint = defaultPointForSolution(solution);
      if (defaultPoint) solution.fields["배점"] = defaultPoint;
    }
  });
  setSolutionsDirty(true);
  closeClassificationMenus();
  renderClassificationOverview();
  const current = solutionForNumber(currentSolutionNumber);
  if (current) renderClassificationPanel(current);
}

function renderClassificationSubjectSwitch() {
  if (!classificationSubjectSwitch) return;
  const activeSubject = defaultClassificationSubject();
  classificationSubjectSwitch.innerHTML = "";
  classificationSubjects.forEach((subject) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `classification-subject-button${subject === activeSubject ? " is-active" : ""}`;
    button.textContent = subject;
    button.addEventListener("click", () => setClassificationSubjectForAll(subject));
    classificationSubjectSwitch.appendChild(button);
  });
}

function setClassificationField(solution, key, value, options = {}) {
  if (!solution) return "";
  ensureClassificationFields(solution);
  const nextValue = options.normalize ? normalizeSolutionField(key, value) : String(value ?? "");
  solution.fields[key] = nextValue;
  if (key === "정답" && Number(solution.number) === Number(currentSolutionNumber)) {
    solutionAnswer.textContent = `정답 ${nextValue || "-"}`;
  }
  if (key === "정답") {
    updateSolutionNavAnswer(solution, nextValue);
    renderAnswerDistribution();
  }
  if (key === "선택과목") {
    classificationSubunitKeys.forEach((subunitKey) => {
      if (!solution.fields[subunitKey]) solution.fields[subunitKey] = "";
    });
  }
  setSolutionsDirty(true);
  if (options.refreshOverview !== false) {
    renderClassificationOverview();
  }
  if (options.refreshPanel !== false && Number(solution.number) === Number(currentSolutionNumber)) {
    renderClassificationPanel(solution);
  }
  return nextValue;
}

function buildClassificationControl(solution, key, label, options = {}) {
  const wrapper = document.createElement("label");
  wrapper.className = `classification-field${options.wide ? " is-wide" : ""}`;
  const span = document.createElement("span");
  span.textContent = label;

  let input;
  if (options.type === "select") {
    input = document.createElement("select");
    (options.choices || []).forEach(([value, text]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = text;
      input.appendChild(option);
    });
  } else {
    input = document.createElement("input");
    input.type = options.type || "text";
    if (options.list) input.setAttribute("list", options.list);
    if (options.min) input.min = options.min;
    if (options.max) input.max = options.max;
    if (options.step) input.step = options.step;
  }

  input.value = solution.fields?.[key] || "";
  input.addEventListener("input", () => setClassificationField(solution, key, input.value, {
    refreshOverview: false,
    refreshPanel: false,
  }));
  input.addEventListener("change", () => {
    input.value = setClassificationField(solution, key, input.value, {
      normalize: key === "정답",
      refreshPanel: key === "선택과목",
    });
  });

  wrapper.append(span, input);
  if (input.tagName === "SELECT") enhanceAppSelect(input);
  return wrapper;
}

function renderClassificationPanel(solution) {
  if (!solutionClassificationPanel || !solution) return;
  ensureClassificationFields(solution);
  const subject = classificationSubjectForSolution(solution);
  solutionClassificationPanel.innerHTML = "";

  const head = document.createElement("div");
  head.className = "classification-panel-head";
  head.innerHTML = `
    <div>
      <p class="tw-kicker">CLASSIFICATION</p>
      <h4>분류표 입력</h4>
    </div>
  `;
  const subjectSwitch = document.createElement("div");
  subjectSwitch.className = "classification-panel-subjects";
  classificationSubjects.forEach((item) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `classification-subject-button${item === subject ? " is-active" : ""}`;
    button.textContent = item;
    button.addEventListener("click", () => setClassificationSubjectForAll(item));
    subjectSwitch.appendChild(button);
  });
  head.appendChild(subjectSwitch);

  const grid = document.createElement("div");
  grid.className = "classification-field-grid";
  grid.append(
    buildClassificationControl(solution, "배점", "배점", { type: "number", min: "1", max: "5", step: "1" }),
    buildClassificationControl(solution, "정답", "정답"),
    buildClassificationControl(solution, classificationObjectiveKey, "객/주관", {
      type: "select",
      choices: [["1", "객관식(1)"], ["0", "주관식(0)"]],
    }),
    buildClassificationControl(solution, classificationKillerKey, "킬러여부", {
      type: "select",
      choices: [["", "미지정"], ["해당 없음", "해당 없음"], ["준킬러", "준킬러"], ["킬러", "킬러"]],
    }),
    buildClassificationControl(solution, classificationDifficultyKey, "난이도", {
      type: "select",
      choices: [
        ["", "미지정"],
        ...Array.from({ length: 9 }, (_, index) => [String(index + 1), `${index + 1}`]),
      ],
    }),
  );

  classificationSubunitKeys.forEach((key, index) => {
    const picker = buildUnitPicker(solution, key, `소단원 ${index + 1}순위`);
    picker.classList.add("is-wide");
    grid.appendChild(picker);
  });

  solutionClassificationPanel.append(head, grid);
}

function renderClassificationOverview() {
  if (!solutionClassificationOverview || !classificationTable) return;
  if (!currentSolutions.length) {
    solutionClassificationOverview.hidden = true;
    exportClassificationButton.disabled = true;
    return;
  }
  ensureAllClassificationFields();
  solutionClassificationOverview.hidden = false;
  exportClassificationButton.disabled = false;
  classificationTable.innerHTML = "";
  ensureClassificationFilename();
  renderClassificationSubjectSwitch();

  const headers = ["문항", "배점", "정답", "1순위", "2순위", "3순위", "4순위", "5순위", "객", "킬러", "난이도"];
  const table = document.createElement("div");
  table.className = "classification-matrix";

  headers.forEach((header) => {
    const cell = document.createElement("span");
    cell.className = "classification-head-cell";
    cell.textContent = header;
    table.appendChild(cell);
  });

  currentSolutions.forEach((solution) => {
    ensureClassificationFields(solution);
    const numberButton = document.createElement("button");
    numberButton.type = "button";
    numberButton.className = "classification-number-cell";
    numberButton.textContent = `${solution.number}`;
    numberButton.addEventListener("click", () => selectSolutionByNumber(solution.number));
    table.appendChild(numberButton);

    const controls = [
      ["배점", { type: "number", min: "1", max: "5", step: "1" }],
      ["정답", {}],
      ...classificationSubunitKeys.map((key) => [key, { type: "unit" }]),
      [classificationObjectiveKey, { type: "select", choices: [["1", "1"], ["0", "0"]] }],
      [classificationKillerKey, { type: "select", choices: [["", "-"], ["해당 없음", "해당 없음"], ["준킬러", "준킬러"], ["킬러", "킬러"]] }],
      [classificationDifficultyKey, {
        type: "select",
        choices: [["", "-"], ...Array.from({ length: 9 }, (_, index) => [String(index + 1), `${index + 1}`])],
      }],
    ];

    controls.forEach(([key, options]) => {
      if (options.type === "unit") {
        table.appendChild(buildUnitPicker(solution, key));
        return;
      }

      let input;
      if (options.type === "select") {
        input = document.createElement("select");
        (options.choices || []).forEach(([value, text]) => {
          const option = document.createElement("option");
          option.value = value;
          option.textContent = text;
          input.appendChild(option);
        });
      } else {
        input = document.createElement("input");
        input.type = options.type || "text";
        if (options.list) input.setAttribute("list", options.list);
        if (options.min) input.min = options.min;
        if (options.max) input.max = options.max;
        if (options.step) input.step = options.step;
      }
      input.value = solution.fields?.[key] || "";
      input.addEventListener("focus", () => selectSolutionByNumber(solution.number));
      input.addEventListener("input", () => setClassificationField(solution, key, input.value, {
        refreshOverview: false,
        refreshPanel: false,
      }));
      input.addEventListener("change", () => {
        input.value = setClassificationField(solution, key, input.value, {
          normalize: key === "정답",
          refreshPanel: key === "선택과목",
        });
      });
      const cell = document.createElement("label");
      cell.className = `classification-edit-cell${classificationSubunitKeys.includes(key) ? " is-unit" : ""}`;
      cell.appendChild(input);
      if (input.tagName === "SELECT") enhanceAppSelect(input);
      table.appendChild(cell);
    });
  });

  classificationTable.appendChild(table);
  if (classificationStatus) {
    const subject = defaultClassificationSubject();
    const unitCount = unitsForSubject(subject).length;
    classificationStatus.textContent = unitCatalogReady
      ? `${subject} 단원 ${unitCount}개 · 현재 선택값으로 XLSX 내보내기 가능`
      : "단원 목록을 불러오지 못했습니다. 직접 입력은 가능합니다.";
  }
}

async function loadUnitCatalog() {
  try {
    const response = await fetch("/api/unit-catalog", { cache: "no-store" });
    if (!response.ok) throw new Error("단원 목록을 불러오지 못했습니다.");
    unitCatalog = await response.json();
    unitCatalogReady = true;
    if (classificationStatus) {
      const subject = defaultClassificationSubject();
      classificationStatus.textContent = `${subject} 단원 ${unitsForSubject(subject).length}개 로딩됨`;
    }
  } catch (error) {
    unitCatalog = {};
    unitCatalogReady = false;
    if (classificationStatus) classificationStatus.textContent = error.message;
  } finally {
    if (currentSolutions.length) renderClassificationOverview();
  }
}

function rateTone(value) {
  const rate = parseRatePercent(value);
  if (rate === null) return "";
  if (rate <= 40) return "critical";
  if (rate <= 55) return "warning";
  return "";
}

function riskTone(value) {
  const risk = normalizeRiskValue(value);
  if (risk === "높음") return "critical";
  if (risk === "보통") return "warning";
  return "";
}

function metricTone(key, value) {
  if (key === "예상 정답률") return rateTone(value);
  if (key === "오류 가능성") return riskTone(value);
  return "";
}

function applyToneClass(element, tone) {
  element.classList.remove("is-warning", "is-critical");
  if (tone) element.classList.add(`is-${tone}`);
}

function updateMetricTone(element, key, value) {
  applyToneClass(element, metricTone(key, value));
}

function solutionQuality(solution) {
  const fields = solution.fields || {};
  const rate = rateTone(fields["예상 정답률"]);
  const risk = riskTone(fields["오류 가능성"]);
  return {
    critical: rate === "critical" || risk === "critical",
    warning: rate === "warning" || risk === "warning",
    rate,
    risk,
  };
}

function solutionFlagLabel(solution) {
  const fields = solution.fields || {};
  const labels = [];
  if (rateTone(fields["예상 정답률"])) labels.push("정답률");
  if (riskTone(fields["오류 가능성"])) labels.push("오류");
  return labels.join(" · ");
}

function updateSolutionNavAnswer(solution, value = null) {
  if (!solutionNav || !solution) return;
  const button = solutionNav.querySelector(`[data-number="${solution.number}"]`);
  const answer = button?.querySelector("[data-solution-nav-answer]");
  if (answer) answer.textContent = value ? `정답 ${value}` : "정답 -";
}

function answerDistribution() {
  const counts = { "1": 0, "2": 0, "3": 0, "4": 0, "5": 0 };
  let missing = 0;
  currentSolutions.forEach((solution) => {
    const answer = normalizeAnswerValue(solution.fields?.["정답"]);
    if (counts[answer] !== undefined) {
      counts[answer] += 1;
    } else {
      missing += 1;
    }
  });
  return { counts, missing, total: currentSolutions.length };
}

function renderAnswerDistribution() {
  if (!solutionAnswerDistribution) return;
  if (!currentSolutions.length) {
    solutionAnswerDistribution.hidden = true;
    solutionAnswerDistribution.innerHTML = "";
    return;
  }

  const { counts, missing, total } = answerDistribution();
  solutionAnswerDistribution.innerHTML = "";

  const head = document.createElement("div");
  head.className = "solution-answer-head";
  head.innerHTML = `
    <p class="tw-kicker">ANSWER COUNT</p>
    <h3 class="app-subtitle">정답 분포</h3>
  `;

  const grid = document.createElement("div");
  grid.className = "solution-answer-grid";
  ["1", "2", "3", "4", "5"].forEach((choice) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "solution-answer-count";
    item.innerHTML = `<span>${choice}번</span><strong>${counts[choice]}개</strong>`;
    item.addEventListener("click", () => {
      const matched = currentSolutions.find((solution) => normalizeAnswerValue(solution.fields?.["정답"]) === choice);
      if (matched) selectSolutionByNumber(matched.number);
    });
    grid.appendChild(item);
  });

  const meta = document.createElement("span");
  meta.className = "solution-answer-meta";
  meta.textContent = missing ? `총 ${total}문항 · 미입력 ${missing}개` : `총 ${total}문항`;

  solutionAnswerDistribution.append(head, grid, meta);
  solutionAnswerDistribution.hidden = false;
}

function syncSolutionNavQuality() {
  currentSolutions.forEach((solution) => {
    const button = solutionNav.querySelector(`[data-number="${solution.number}"]`);
    if (!button) return;
    const quality = solutionQuality(solution);
    button.classList.toggle("has-critical", quality.critical);
    button.classList.toggle("has-warning", !quality.critical && quality.warning);
    const flag = button.querySelector(".solution-nav-flag");
    if (flag) {
      const label = solutionFlagLabel(solution);
      flag.textContent = label;
      flag.hidden = !label;
    }
  });
}

function selectSolutionByNumber(number) {
  const navButton = solutionNav.querySelector(`[data-number="${number}"]`);
  selectSolution(number, navButton);
}

function syncOverviewActive() {
  solutionOverviewTable.querySelectorAll("[data-number]").forEach((node) => {
    node.classList.toggle("is-active", Number(node.dataset.number) === Number(currentSolutionNumber));
  });
}

function renderQualityStrip() {
  if (!solutionQualityStrip) return;
  syncSolutionNavQuality();
  solutionQualityStrip.innerHTML = "";

  const lowRates = [];
  const warningRates = [];
  const highRisks = [];
  const warningRisks = [];

  currentSolutions.forEach((solution) => {
    const fields = solution.fields || {};
    const rate = rateTone(fields["예상 정답률"]);
    const risk = riskTone(fields["오류 가능성"]);
    if (rate === "critical") lowRates.push(solution.number);
    if (rate === "warning") warningRates.push(solution.number);
    if (risk === "critical") highRisks.push(solution.number);
    if (risk === "warning") warningRisks.push(solution.number);
  });

  const items = [
    ["낮은 정답률", lowRates, "critical"],
    ["주의 정답률", warningRates, "warning"],
    ["오류 검토", highRisks, "critical"],
    ["오류 주의", warningRisks, "warning"],
  ].filter(([, numbers]) => numbers.length);

  if (!items.length) {
    solutionQualityStrip.hidden = true;
    return;
  }

  items.forEach(([label, numbers, tone]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `solution-quality-pill is-${tone}`;
    button.textContent = `${label} ${numbers.map((number) => `${number}번`).join(", ")}`;
    button.addEventListener("click", () => selectSolutionByNumber(numbers[0]));
    solutionQualityStrip.appendChild(button);
  });

  solutionQualityStrip.hidden = false;
}

function solutionCutRates(solutions = currentSolutions) {
  return solutions
    .map((solution) => ({
      number: Number(solution.number),
      rate: parseRatePercent(solution.fields?.["예상 정답률"]),
    }))
    .filter((item) => item.rate !== null);
}

function currentSolutionsPayload() {
  currentSolutions = currentSolutions.map(normalizeSolutionRecord);
  ensureAllClassificationFields();
  const imageNumbers = new Set(currentQuestions.map((question) => Number(question.number)));
  const solutionNumbers = new Set(currentSolutions.map((solution) => Number(solution.number)));
  return {
    job_id: currentJobId,
    count: currentSolutions.length,
    has_images: currentQuestions.length > 0,
    encoding: currentEncoding,
    fieldnames: currentFieldnames,
    solutions: currentSolutions,
    questions: currentQuestions,
    cut_rates: solutionCutRates(),
    missing_images: currentQuestions.length
      ? [...solutionNumbers].filter((number) => !imageNumbers.has(number)).sort((a, b) => a - b)
      : [],
    missing_solutions: [...imageNumbers].filter((number) => !solutionNumbers.has(number)).sort((a, b) => a - b),
  };
}

function setSolutionField(solution, key, value, options = {}) {
  const nextValue = options.normalize ? normalizeSolutionField(key, value) : String(value ?? "");
  solution.fields[key] = nextValue;
  const isCurrentSolution = Number(solution.number) === Number(currentSolutionNumber);
  if (key === "문항 번호") {
    const parsed = parseQuestionNumber(nextValue);
    if (parsed) {
      solution.number = parsed;
      solution.label = nextValue;
      if (isCurrentSolution) {
        currentSolutionNumber = parsed;
        solutionTitle.textContent = `${parsed}번${nextValue !== String(parsed) ? ` · ${nextValue}` : ""}`;
      }
    }
  }
  if (key === "정답" && isCurrentSolution) {
    solutionAnswer.textContent = `정답 ${nextValue || "-"}`;
  }
  if (key === "정답") {
    updateSolutionNavAnswer(solution, nextValue);
    renderAnswerDistribution();
  }
  setSolutionsDirty(true);
  return nextValue;
}

function renderSolutionOverview() {
  solutionOverviewTable.innerHTML = "";
  if (!currentSolutions.length) {
    solutionOverview.hidden = true;
    if (solutionQualityStrip) solutionQualityStrip.hidden = true;
    return;
  }

  const metrics = [["정답", "정답"], ...overviewFields];
  const matrix = document.createElement("div");
  matrix.className = "solution-overview-matrix";
  matrix.style.setProperty("--overview-count", currentSolutions.length);

  const head = document.createElement("div");
  head.className = "solution-overview-row solution-overview-head";
  const metricHead = document.createElement("span");
  metricHead.className = "solution-overview-label";
  metricHead.textContent = "지표";
  head.appendChild(metricHead);

  currentSolutions.forEach((solution) => {
    const questionButton = document.createElement("button");
    questionButton.type = "button";
    questionButton.className = "solution-overview-question";
    questionButton.dataset.number = solution.number;
    questionButton.textContent = `${solution.number}번`;
    questionButton.addEventListener("click", () => selectSolutionByNumber(solution.number));
    head.appendChild(questionButton);
  });
  matrix.appendChild(head);

  metrics.forEach(([key, label]) => {
    if (!currentFieldnames.includes(key)) return;

    const row = document.createElement("div");
    row.className = "solution-overview-row solution-overview-field-row";
    row.dataset.metric = key;

    const labelCell = document.createElement("span");
    labelCell.className = "solution-overview-label";
    labelCell.textContent = label;
    row.appendChild(labelCell);

    currentSolutions.forEach((solution) => {
      const cell = document.createElement("label");
      cell.className = "solution-overview-cell";
      cell.dataset.number = solution.number;
      cell.dataset.metric = key;

      const input = document.createElement("input");
      input.value = solution.fields?.[key] || "";
      updateMetricTone(cell, key, input.value);
      input.addEventListener("focus", () => selectSolutionByNumber(solution.number));
      input.addEventListener("input", () => {
        setSolutionField(solution, key, input.value);
        updateMetricTone(cell, key, input.value);
        renderQualityStrip();
      });
      input.addEventListener("change", () => {
        input.value = setSolutionField(solution, key, input.value, { normalize: true });
        updateMetricTone(cell, key, input.value);
        renderQualityStrip();
      });

      cell.appendChild(input);
      row.appendChild(cell);
    });

    matrix.appendChild(row);
  });

  solutionOverviewTable.appendChild(matrix);

  solutionOverview.hidden = false;
  renderQualityStrip();
  syncOverviewActive();
}

function renderSolutionMatchRow(data) {
  solutionMatchRow.innerHTML = "";
  solutionMatchRow.appendChild(createMatchBadge(`${data.solutions.length}개 해설`, true));
  solutionMatchRow.appendChild(
    createMatchBadge(data.has_images ? `${data.questions.length}개 이미지` : "이미지 없이 보기"),
  );
  if (data.cut_rates && data.cut_rates.length) {
    solutionMatchRow.appendChild(createMatchBadge(`${data.cut_rates.length}개 정답률 → 1컷`));
  }
  solutionMatchRow.appendChild(createMatchBadge(data.encoding));

  if (data.missing_solutions.length) {
    solutionMatchRow.appendChild(
      createMatchBadge(`해설 없음: ${data.missing_solutions.map((n) => `${n}번`).join(", ")}`),
    );
  }
  if (data.missing_images.length) {
    solutionMatchRow.appendChild(
      createMatchBadge(`이미지 없음: ${data.missing_images.map((n) => `${n}번`).join(", ")}`),
    );
  }
  solutionMatchRow.hidden = false;
}

function renderSolutionMetrics(fields) {
  solutionMetrics.innerHTML = "";
  const solution = solutionForNumber(currentSolutionNumber);
  [["문항 번호", "문항 번호"], ["정답", "정답"], ...metricFields].forEach(([key, label]) => {
    if (!currentFieldnames.includes(key)) return;
    const item = document.createElement("div");
    item.className = "solution-metric";

    const labelNode = document.createElement("span");
    labelNode.textContent = label;
    const valueNode = document.createElement("input");
    valueNode.type = "text";
    valueNode.value = fields[key] || "";
    updateMetricTone(item, key, valueNode.value);
    valueNode.addEventListener("input", () => {
      if (solution) {
        setSolutionField(solution, key, valueNode.value);
        updateMetricTone(item, key, valueNode.value);
        renderQualityStrip();
      }
    });
    valueNode.addEventListener("change", () => {
      if (solution) {
        valueNode.value = setSolutionField(solution, key, valueNode.value, { normalize: true });
        updateMetricTone(item, key, valueNode.value);
        renderQualityStrip();
      }
    });

    item.append(labelNode, valueNode);
    solutionMetrics.appendChild(item);
  });
}

function renderSolutionDetails(fields) {
  solutionDetails.innerHTML = "";
  detailFields.forEach(([key, label]) => {
    if (!currentFieldnames.includes(key)) return;
    const solution = solutionForNumber(currentSolutionNumber);

    const block = document.createElement("section");
    block.className = "solution-detail-block";

    const heading = document.createElement("h4");
    heading.textContent = label;
    const body = document.createElement("textarea");
    body.rows = key.includes("풀이") || key === "해설" ? 5 : 3;
    body.value = fields[key] || "";
    body.addEventListener("input", () => {
      if (solution) setSolutionField(solution, key, body.value);
    });

    block.append(heading, body);
    solutionDetails.appendChild(block);
  });

  const renderedKeys = new Set(detailFields.map(([key]) => key));
  currentFieldnames.forEach((key) => {
    if (
      renderedKeys.has(key)
      || classificationKeys.includes(key)
      || key === "문항 번호"
      || key === "정답"
      || metricFields.some(([metricKey]) => metricKey === key)
    ) {
      return;
    }
    const solution = solutionForNumber(currentSolutionNumber);
    const block = document.createElement("section");
    block.className = "solution-detail-block";
    const heading = document.createElement("h4");
    heading.textContent = key;
    const body = document.createElement("textarea");
    body.rows = 3;
    body.value = fields[key] || "";
    body.addEventListener("input", () => {
      if (solution) setSolutionField(solution, key, body.value);
    });
    block.append(heading, body);
    solutionDetails.appendChild(block);
  });
}

function selectSolution(number, button = null) {
  const solution = solutionForNumber(number);
  if (!solution) return;
  currentSolutionNumber = Number(solution.number);

  const fields = solution.fields || {};
  const image = questionForNumber(number);
  if (image) {
    solutionImage.src = image.url;
    solutionImage.alt = `${number}번 문항 이미지`;
    solutionImage.hidden = false;
    solutionImageEmpty.hidden = true;
    solutionImageName.textContent = image.name;
  } else {
    solutionImage.removeAttribute("src");
    solutionImage.alt = `${number}번 문항 이미지 없음`;
    solutionImage.hidden = true;
    solutionImageEmpty.hidden = false;
    solutionImageName.textContent = "이미지 없이 보기";
  }

  const label = solution.label && solution.label !== String(number) ? ` · ${solution.label}` : "";
  solutionTitle.textContent = `${number}번${label}`;
  solutionAnswer.textContent = `정답 ${fields["정답"] || "-"}`;
  renderClassificationPanel(solution);
  renderSolutionMetrics(fields);
  renderSolutionDetails(fields);

  solutionNav.querySelectorAll(".solution-nav-button").forEach((node) => {
    node.classList.remove("is-active");
  });
  if (button) button.classList.add("is-active");

  syncOverviewActive();
}

function renderSolutions(data, shouldApplyCut = true) {
  currentJobId = data.job_id || currentJobId;
  currentQuestions = data.questions || currentQuestions;
  currentFieldnames = data.fieldnames || currentFieldnames;
  currentEncoding = data.encoding || currentEncoding;
  currentSolutions = (data.solutions || []).map(normalizeSolutionRecord);
  ensureAllClassificationFields();
  renderSolutionMatchRow(data);
  solutionNav.innerHTML = "";

  currentSolutions.forEach((solution, index) => {
    const fields = solution.fields || {};
    const button = document.createElement("button");
    button.type = "button";
    button.className = "solution-nav-button";
    button.dataset.number = solution.number;
    const quality = solutionQuality(solution);
    button.classList.toggle("has-critical", quality.critical);
    button.classList.toggle("has-warning", !quality.critical && quality.warning);

    const number = document.createElement("strong");
    number.textContent = `${solution.number}번`;
    const answer = document.createElement("span");
    answer.dataset.solutionNavAnswer = "true";
    answer.textContent = fields["정답"] ? `정답 ${fields["정답"]}` : "정답 -";
    const flagText = solutionFlagLabel(solution);
    const flag = document.createElement("span");
    flag.className = "solution-nav-flag";
    flag.textContent = flagText;
    flag.hidden = !flagText;

    button.append(number, answer, flag);
    button.addEventListener("click", () => selectSolution(solution.number, button));
    solutionNav.appendChild(button);
    if (index === 0) selectSolution(solution.number, button);
  });

  renderSolutionOverview();
  renderAnswerDistribution();
  renderClassificationOverview();
  solutionViewer.hidden = false;
  setSolutionsStatus("완료", true);
  setSolutionsDirty(false);
  if (shouldApplyCut) applySolutionsToCut(data);
}

async function applySolutionsToCut(data) {
  const importedCount = setRateInputsFromSolutions(data.cut_rates || []);
  if (!importedCount) return;

  if (cutModelReady) {
    await cutModelReady.catch(() => {});
  }
  if (!cutModel) {
    cutWarning.textContent = "1컷 모델을 아직 불러오지 못했습니다.";
    cutWarning.hidden = false;
    cutResult.hidden = false;
    return;
  }

  fillDefaultPoints();
  if (importedCount === 20) {
    await runCutPrediction();
  } else {
    cutWarning.textContent = `CSV에서 정답률 ${importedCount}개를 가져왔습니다. 20개가 채워지면 예측할 수 있습니다.`;
    cutWarning.hidden = false;
    cutResult.hidden = false;
  }
}

function renderResults(data, options = {}) {
  currentJobId = data.job_id;
  currentQuestions = data.questions || [];
  resultsPanel.hidden = false;
  if (!options.preserveSolutions) {
    resetSolutions(true);
  }
  downloadButton.href = data.download_url;
  manifestLink.href = data.manifest_url;
  renderStats(data);
  thumbGrid.innerHTML = "";

  data.questions.forEach((item, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "app-thumb";
    button.innerHTML = `
      <img src="${item.url}" alt="${item.name}" loading="lazy" />
      <span>${item.name}</span>
    `;
    button.addEventListener("click", () => setPreview(item, button));
    thumbGrid.appendChild(button);
    if (index === 0) setPreview(item, button);
  });

  setStatus("완료", true);
  if (options.preserveSolutions && currentSolutions.length) {
    renderSolutions(currentSolutionsPayload(), false);
  }
}

function fillArchiveForm(archive) {
  archiveTitle.value = archive?.title || "";
  archiveSubject.value = archive?.subject || "";
  archiveDate.value = archive?.exam_date || "";
  archiveMemo.value = archive?.memo || "";
}

function archiveMetaFromCard(card) {
  return {
    title: card.querySelector("[data-archive-title]").value,
    subject: card.querySelector("[data-archive-subject]").value,
    exam_date: card.querySelector("[data-archive-date]").value,
    memo: card.querySelector("[data-archive-memo]").value,
  };
}

function createArchiveField(label, element) {
  const wrapper = document.createElement("label");
  wrapper.className = "archive-card-field";
  const span = document.createElement("span");
  span.textContent = label;
  wrapper.append(span, element);
  return wrapper;
}

function renderArchiveList(archives) {
  archiveList.innerHTML = "";
  if (!archives.length) {
    const empty = document.createElement("div");
    empty.className = "archive-empty";
    empty.textContent = "저장된 모의고사가 아직 없습니다.";
    archiveList.appendChild(empty);
    return;
  }

  archives.forEach((archive) => {
    const card = document.createElement("article");
    card.className = "archive-card";
    card.dataset.archiveId = archive.archive_id;

    const head = document.createElement("div");
    head.className = "archive-card-head";
    const title = document.createElement("strong");
    title.textContent = archive.title || "제목 없음";
    const meta = document.createElement("span");
    meta.textContent = `${archive.subject || "과목 미지정"} · ${archive.exam_date || "날짜 없음"} · 이미지 ${archive.image_count || 0} · 해설 ${archive.solution_count || 0}`;
    head.append(title, meta);

    const fields = document.createElement("div");
    fields.className = "archive-card-grid";

    const titleInput = document.createElement("input");
    titleInput.value = archive.title || "";
    titleInput.dataset.archiveTitle = "true";
    const subjectInput = document.createElement("input");
    subjectInput.value = archive.subject || "";
    subjectInput.dataset.archiveSubject = "true";
    const dateInput = document.createElement("input");
    dateInput.type = "date";
    dateInput.value = archive.exam_date || "";
    dateInput.dataset.archiveDate = "true";
    const memoInput = document.createElement("textarea");
    memoInput.rows = 2;
    memoInput.value = archive.memo || "";
    memoInput.dataset.archiveMemo = "true";

    fields.append(
      createArchiveField("시험명", titleInput),
      createArchiveField("과목", subjectInput),
      createArchiveField("시행일", dateInput),
      createArchiveField("메모", memoInput),
    );

    const actions = document.createElement("div");
    actions.className = "archive-card-actions";

    const loadButton = document.createElement("button");
    loadButton.type = "button";
    loadButton.className = "tw-button app-primary";
    loadButton.textContent = "불러오기";
    loadButton.addEventListener("click", () => loadArchive(archive.archive_id));

    const saveButton = document.createElement("button");
    saveButton.type = "button";
    saveButton.className = "tw-button";
    saveButton.textContent = "정보 저장";
    saveButton.addEventListener("click", () => updateArchiveMetadata(archive.archive_id, card));

    const openButton = document.createElement("button");
    openButton.type = "button";
    openButton.className = "tw-button";
    openButton.textContent = "폴더 열기";
    openButton.addEventListener("click", async () => {
      await fetch(`/api/archives/${archive.archive_id}/open`, { method: "POST" });
    });

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "tw-button";
    deleteButton.textContent = "삭제";
    deleteButton.addEventListener("click", async () => {
      if (!window.confirm(`'${archive.title || "제목 없음"}' 아카이브를 삭제할까요?`)) return;
      const response = await fetch(`/api/archives/${archive.archive_id}`, { method: "DELETE" });
      if (response.ok) {
        setArchiveStatus("삭제됨", true);
        await loadArchives();
      } else {
        const data = await response.json();
        archiveMessage.textContent = data.error || "삭제하지 못했습니다.";
        setArchiveStatus("오류", false);
      }
    });

    actions.append(loadButton, saveButton, openButton, deleteButton);
    card.append(head, fields, actions);
    archiveList.appendChild(card);
  });
}

async function loadArchives() {
  try {
    const response = await fetch("/api/archives");
    const data = await response.json();
    renderArchiveList(data.archives || []);
  } catch (error) {
    archiveList.innerHTML = "";
    const empty = document.createElement("div");
    empty.className = "archive-empty";
    empty.textContent = error.message;
    archiveList.appendChild(empty);
  }
}

async function updateArchiveMetadata(archiveId, card) {
  setArchiveStatus("수정 중", true);
  archiveMessage.textContent = "";
  try {
    const response = await fetch(`/api/archives/${archiveId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ metadata: archiveMetaFromCard(card) }),
    });
    const data = await response.json();
    if (!response.ok) {
      archiveMessage.textContent = data.error || "아카이브 정보를 저장하지 못했습니다.";
      setArchiveStatus("오류", false);
      return;
    }
    archiveMessage.textContent = `${data.title || "제목 없음"} 정보 저장`;
    setArchiveStatus("수정됨", true);
    await loadArchives();
  } catch (error) {
    archiveMessage.textContent = error.message;
    setArchiveStatus("오류", false);
  }
}

async function loadArchive(archiveId) {
  setArchiveStatus("불러오는 중", true);
  archiveMessage.textContent = "";
  try {
    const response = await fetch(`/api/archives/${archiveId}/load`, { method: "POST" });
    const data = await response.json();
    if (!response.ok) {
      archiveMessage.textContent = data.error || "아카이브를 불러오지 못했습니다.";
      setArchiveStatus("오류", false);
      return;
    }

    fillArchiveForm(data.archive);
    lastCutResult = data.archive?.cut_result || null;
    currentJobId = data.job?.job_id || null;
    currentQuestions = [];

    if (data.job?.questions?.length) {
      renderResults(data.job, { preserveSolutions: false });
    } else {
      resultsPanel.hidden = true;
      resetSolutions(false);
    }

    if (data.solutions) {
      renderSolutions(data.solutions, true);
    }

    archiveMessage.textContent = `${data.archive?.title || "제목 없음"} 불러옴`;
    setArchiveStatus("불러옴", true);
  } catch (error) {
    archiveMessage.textContent = error.message;
    setArchiveStatus("오류", false);
  }
}

pdfInput.addEventListener("change", () => {
  updateFileLabel(pdfInput.files[0]);
});

["dragenter", "dragover"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.add("is-dragging");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.remove("is-dragging");
  });
});

dropzone.addEventListener("drop", (event) => {
  const file = event.dataTransfer.files[0];
  if (!file) return;
  const transfer = new DataTransfer();
  transfer.items.add(file);
  pdfInput.files = transfer.files;
  updateFileLabel(file);
});

imageInput.addEventListener("change", () => {
  updateImageLabel(imageInput.files);
});

["dragenter", "dragover"].forEach((eventName) => {
  imageDropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    imageDropzone.classList.add("is-dragging");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  imageDropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    imageDropzone.classList.remove("is-dragging");
  });
});

imageDropzone.addEventListener("drop", (event) => {
  if (!event.dataTransfer.files.length) return;
  const transfer = new DataTransfer();
  Array.from(event.dataTransfer.files).forEach((file) => transfer.items.add(file));
  imageInput.files = transfer.files;
  updateImageLabel(imageInput.files);
});

async function uploadQuestionImages(files, options = {}) {
  hideError();

  const fileList = Array.from(files || []);
  if (!fileList.length) {
    showError("문항 이미지 파일을 선택해주세요.");
    return;
  }

  const payload = new FormData();
  fileList.forEach((file) => payload.append("images", file));
  if (options.questionNumber && fileList.length === 1) {
    payload.append("question_number", String(options.questionNumber));
  }

  const endpoint = currentJobId ? `/api/jobs/${currentJobId}/images` : "/api/images";
  const preserveSolutions = currentSolutions.length > 0;
  const selectedNumber = currentSolutionNumber;
  setImageBusy(true);

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      body: payload,
    });
    const data = await response.json();
    if (!response.ok) {
      showError(data.error || "이미지를 적용하지 못했습니다.");
      return;
    }
    renderResults(data, { preserveSolutions });
    if (preserveSolutions && selectedNumber) {
      const button = solutionNav.querySelector(`[data-number="${selectedNumber}"]`);
      selectSolution(selectedNumber, button);
    }
    updateImageLabel(null);
    imageInput.value = "";
    if (inlineImageInput) inlineImageInput.value = "";
  } catch (error) {
    showError(error.message);
  } finally {
    setImageBusy(false);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError();
  showProgressPanel();
  clearGeminiGenerationPanel();
  addErrorProgress("요청 시작: PDF 문항 분할 실행", "info");

  if (!pdfInput.files.length) {
    showError("PDF 파일을 선택해주세요.");
    return;
  }

  const payload = new FormData(form);
  if (payload.get("run_gemini_auto") === "on") {
    saveGeminiProfile();
  }
  if (payload.get("run_gemini_auto") === "on") {
    addErrorProgress("Gemini 자동 생성 예정: 문항별 요청 로그는 완료 후 진행 패널에서 표시됩니다.", "info");
  }
  addErrorProgress(`업로드 파일: ${pdfInput.files[0]?.name || "미확인"}`, "info");
  addErrorProgress(`기대 문항 수: ${payload.get("expected_questions")} / DPI: ${payload.get("dpi")} / 자동 해설: ${payload.get("run_gemini_auto") ? "ON" : "OFF"} / 동시 요청: ${payload.get("gemini_concurrency") || 1}`, "info");
  setBusy(true);
  resultsPanel.hidden = true;
  resetSolutions(false);
  currentJobId = null;
  currentQuestions = [];

  try {
    addErrorProgress("백그라운드 작업 생성 중...", "info");
    const response = await fetch("/api/split/start", {
      method: "POST",
      body: payload,
    });
    addErrorProgress(`작업 생성 응답: ${response.status} ${response.statusText}`, response.ok ? "success" : "error");
    let data;
    try {
      data = await response.json();
    } catch (error) {
      showError("서버 응답을 읽는 중 오류가 발생했습니다.", null, {
        stage: "응답 파싱",
        status: response.status,
        statusText: response.statusText,
        url: "/api/split/start",
        hint: "서버 로그에서 상세 에러를 확인하고, 작업을 다시 실행해 주세요.",
      });
      return;
    }

    if (!response.ok) {
      showError(data.error || "처리하지 못했습니다.", data.job_id || null, {
        stage: "응답 확인",
        status: response.status,
        statusText: response.statusText,
        error_code: data.error_code,
        url: "/api/split/start",
        debug_url: data.debug_url,
        message: data.error || "",
      });
      return;
    }
    currentJobId = data.job_id || null;
    errorJobId = currentJobId;
    openErrorFolderButton.hidden = !currentJobId;
    addErrorProgress(`작업 ID: ${currentJobId}`, "info");
    const statusUrl = data.status_url || `/api/jobs/${currentJobId}/status`;
    data = await pollSplitJob(statusUrl);
    addErrorProgress(`문항 분할 성공: ${data.count}개 저장`, "success");
    addErrorProgress("Gemini 자동 생성 결과 병합 중", "info");
    renderResults(data);
    await applyGeminiAutoResult(data);
  } catch (error) {
    if (error.jobId) {
      errorJobId = error.jobId;
      openErrorFolderButton.hidden = false;
    }
    const normalized = normalizeNetworkError(error);
    const details = error.details || normalized;
    if (normalized.status === 0) {
      addErrorProgress(`요청 단계에서 중단됨: ${normalized.stage}`, "error");
    } else {
      addErrorProgress(`처리 중 예외: ${normalized.message}`, "error");
    }
    showError(normalized.message, error.jobId || null, details);
  } finally {
    addErrorProgress("요청 종료", "info");
    setBusy(false);
  }
});

imageForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await uploadQuestionImages(imageInput.files);
});

inlineImageInput?.addEventListener("change", async () => {
  await uploadQuestionImages(inlineImageInput.files, {
    questionNumber: currentSolutionNumber,
  });
});

csvInput.addEventListener("change", () => {
  updateCsvLabel(csvInput.files[0]);
});

["dragenter", "dragover"].forEach((eventName) => {
  csvDropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    csvDropzone.classList.add("is-dragging");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  csvDropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    csvDropzone.classList.remove("is-dragging");
  });
});

csvDropzone.addEventListener("drop", (event) => {
  const file = event.dataTransfer.files[0];
  if (!file) return;
  const transfer = new DataTransfer();
  transfer.items.add(file);
  csvInput.files = transfer.files;
  updateCsvLabel(file);
});

solutionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  solutionMatchRow.hidden = true;

  if (!currentJobId) {
    currentQuestions = [];
  }
  if (!csvInput.files.length) {
    solutionMatchRow.innerHTML = "";
    solutionMatchRow.appendChild(createMatchBadge("CSV 파일을 선택해주세요."));
    solutionMatchRow.hidden = false;
    setSolutionsStatus("오류", false);
    return;
  }

  const payload = new FormData(solutionForm);
  setSolutionsBusy(true);

  try {
    const endpoint = currentJobId ? `/api/jobs/${currentJobId}/solutions` : "/api/solutions";
    const response = await fetch(endpoint, {
      method: "POST",
      body: payload,
    });
    const data = await response.json();
    if (!response.ok) {
      solutionMatchRow.innerHTML = "";
      solutionMatchRow.appendChild(createMatchBadge(data.error || "CSV를 적용하지 못했습니다."));
      solutionMatchRow.hidden = false;
      setSolutionsStatus("오류", false);
      return;
    }
    renderSolutions(data);
  } catch (error) {
    solutionMatchRow.innerHTML = "";
    solutionMatchRow.appendChild(createMatchBadge(error.message));
    solutionMatchRow.hidden = false;
    setSolutionsStatus("오류", false);
  } finally {
    setSolutionsBusy(false);
  }
});

async function saveCurrentSolutions() {
  if (!currentJobId || !currentSolutions.length) return false;
  const selectedNumber = currentSolutionNumber;
  setSolutionsStatus("저장 중", true);
  saveSolutionsButton.disabled = true;
  currentSolutions = currentSolutions.map(normalizeSolutionRecord);
  ensureAllClassificationFields();

  try {
    const response = await fetch(`/api/jobs/${currentJobId}/solutions/edit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fieldnames: currentFieldnames,
        encoding: currentEncoding,
        solutions: currentSolutions,
      }),
    });
    const data = await response.json();
    if (!response.ok) {
      solutionMatchRow.innerHTML = "";
      solutionMatchRow.appendChild(createMatchBadge(data.error || "수정 내용을 저장하지 못했습니다."));
      solutionMatchRow.hidden = false;
      setSolutionsStatus("오류", false);
      setSolutionsDirty(true);
      return false;
    }
    renderSolutions(data, true);
    if (selectedNumber) {
      const button = solutionNav.querySelector(`[data-number="${selectedNumber}"]`);
      selectSolution(selectedNumber, button);
    }
    setSolutionsStatus("저장됨", true);
    return true;
  } catch (error) {
    solutionMatchRow.innerHTML = "";
    solutionMatchRow.appendChild(createMatchBadge(error.message));
    solutionMatchRow.hidden = false;
    setSolutionsStatus("오류", false);
    setSolutionsDirty(true);
    return false;
  }
}

async function exportClassificationTable() {
  if (!currentJobId || !currentSolutions.length) return;
  currentSolutions = currentSolutions.map(normalizeSolutionRecord);
  ensureAllClassificationFields();
  const requestedFilename = ensureClassificationFilename();
  setSolutionsStatus("분류표 생성 중", true);
  if (exportClassificationButton) exportClassificationButton.disabled = true;

  try {
    const response = await fetch(`/api/jobs/${currentJobId}/classification/export`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fieldnames: currentFieldnames,
        encoding: currentEncoding,
        subject: defaultClassificationSubject(),
        filename: requestedFilename,
        solutions: currentSolutions,
      }),
    });
    if (!response.ok) {
      let message = "분류표를 내보내지 못했습니다.";
      try {
        const data = await response.json();
        message = data.error || message;
      } catch {
        message = `${message} HTTP ${response.status}`;
      }
      solutionMatchRow.innerHTML = "";
      solutionMatchRow.appendChild(createMatchBadge(message));
      solutionMatchRow.hidden = false;
      setSolutionsStatus("오류", false);
      return;
    }

    const blob = await response.blob();
    const disposition = response.headers.get("Content-Disposition") || "";
    const filename = filenameFromDisposition(disposition) || requestedFilename;
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    setSolutionsStatus("분류표 생성", true);
  } catch (error) {
    solutionMatchRow.innerHTML = "";
    solutionMatchRow.appendChild(createMatchBadge(error.message));
    solutionMatchRow.hidden = false;
    setSolutionsStatus("오류", false);
  } finally {
    if (exportClassificationButton) exportClassificationButton.disabled = !currentJobId || !currentSolutions.length;
  }
}

saveSolutionsButton.addEventListener("click", saveCurrentSolutions);
exportClassificationButton?.addEventListener("click", exportClassificationTable);

openFolderButton.addEventListener("click", async () => {
  if (!currentJobId) return;
  await fetch(`/api/jobs/${currentJobId}/open`, { method: "POST" });
});

openErrorFolderButton.addEventListener("click", async () => {
  if (!errorJobId) return;
  await fetch(`/api/jobs/${errorJobId}/open`, { method: "POST" });
});

if (saveGeminiProfileButton) {
  saveGeminiProfileButton.addEventListener("click", () => {
    saveGeminiProfile(true);
  });
}

if (clearGeminiProfileButton) {
  clearGeminiProfileButton.addEventListener("click", () => {
    clearGeminiProfile();
  });
}

if (geminiModelInput) {
  geminiModelInput.addEventListener("change", clampGeminiConcurrencyForModel);
}

document.addEventListener("click", (event) => {
  if (!event.target.closest(".classification-unit-cell")) {
    closeClassificationMenus();
  }
  if (!event.target.closest(".app-select-host")) {
    closeAppSelectMenus();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeClassificationMenus();
    closeAppSelectMenus();
  }
});

archiveForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!currentJobId) {
    archiveMessage.textContent = "CSV, PDF, 이미지 중 하나를 먼저 적용해주세요.";
    setArchiveStatus("오류", false);
    return;
  }

  setArchiveStatus("저장 중", true);
  archiveMessage.textContent = "";

  try {
    if (solutionsDirty) {
      const saved = await saveCurrentSolutions();
      if (!saved) {
        archiveMessage.textContent = "해설 수정 내용을 먼저 저장하지 못했습니다.";
        setArchiveStatus("오류", false);
        return;
      }
    }
    const response = await fetch(`/api/jobs/${currentJobId}/archive`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        metadata: {
          title: archiveTitle.value,
          subject: archiveSubject.value,
          exam_date: archiveDate.value,
          memo: archiveMemo.value,
        },
        cut_payload: collectCutPayload(),
        cut_result: lastCutResult,
      }),
    });
    const data = await response.json();
    if (!response.ok) {
      archiveMessage.textContent = data.error || "아카이브 저장에 실패했습니다.";
      setArchiveStatus("오류", false);
      return;
    }
    archiveMessage.textContent = `${data.title} · ${data.image_count}개 이미지 · ${data.solution_count}개 해설 저장`;
    setArchiveStatus("저장됨", true);
    await loadArchives();
  } catch (error) {
    archiveMessage.textContent = error.message;
    setArchiveStatus("오류", false);
  }
});

refreshArchivesButton.addEventListener("click", loadArchives);

resetButton.addEventListener("click", () => {
  form.reset();
  syncAppSelects(form);
  pdfInput.value = "";
  csvInput.value = "";
  imageInput.value = "";
  currentJobId = null;
  currentQuestions = [];
  errorJobId = null;
  resultsPanel.hidden = true;
  resetSolutions(false);
  clearGeminiGenerationPanel();
  hideError();
  updateFileLabel(null);
  updateImageLabel(null);
  setStatus("대기", false);
  archiveMessage.textContent = "";
  setArchiveStatus("대기", false);
});

cutSubject.addEventListener("change", () => {
  fillDefaultPoints();
  renderHistoryExamSelect();
  renderRelation();
  syncAppSelects(cutForm);
});

fillDefaultPointsButton.addEventListener("click", fillDefaultPoints);
applyPasteButton.addEventListener("click", parseRatesFromPaste);
loadHistoryButton.addEventListener("click", applyHistoryExam);

cutForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await runCutPrediction();
});

if (questionSearchForm) {
  questionSearchForm.addEventListener("submit", runQuestionSearch);
  questionSearchSubject.addEventListener("change", () => renderQuestionExamSelect());
  questionRefreshButton.addEventListener("click", () => runQuestionSearch(null, true));
  questionSearchResetButton.addEventListener("click", resetQuestionSearch);
  questionPresetButtons.forEach((button) => {
    button.addEventListener("click", () => applyQuestionPreset(button.dataset.questionPreset));
  });
}

appJumpButtons.forEach((button) => {
  button.addEventListener("click", () => jumpToAppSection(button.dataset.appJump));
});

geoToolTabs.forEach((button) => {
  button.addEventListener("click", () => setGeoToolTab(button.dataset.geoTab, true));
});

const initialHash = window.location.hash;
setGeoToolTab(initialHash === "#question-bank" ? "questions" : "cut");
if (!["#question-bank", "#cut-predictor"].includes(initialHash)) {
  setAppJumpActive("cutter");
}
window.addEventListener("hashchange", () => syncAppStateFromHash());

enhanceAppSelects();
refreshIcons();
cutModelReady = loadCutModel();
restoreGeminiProfile();
loadGeminiDefaults();
loadUnitCatalog();
loadHistoricalExams();
loadArchives();
