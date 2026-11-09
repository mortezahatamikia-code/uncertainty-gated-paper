/* Rion Git — 由 esbuild 生成的产物，请勿直接编辑。 */
"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/main.ts
var main_exports = {};
__export(main_exports, {
  default: () => RionGitPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian7 = require("obsidian");

// src/autoCommit.ts
var AutoCommitManager = class {
  constructor(plugin) {
    this.plugin = plugin;
    this.intervalId = null;
  }
  register() {
    this.applySettings();
  }
  /** 定时器随设置变化重建；旧句柄先清掉，避免热重载后多份定时器叠加。 */
  applySettings() {
    if (this.intervalId !== null) {
      window.clearInterval(this.intervalId);
      this.intervalId = null;
    }
    const { autoCommitMode, autoCommitInterval } = this.plugin.settings;
    if (autoCommitMode !== "interval" || autoCommitInterval <= 0) return;
    this.intervalId = window.setInterval(
      () => void this.plugin.runAutoCommit(),
      autoCommitInterval * 6e4
    );
    this.plugin.registerInterval(this.intervalId);
  }
  dispose() {
    if (this.intervalId !== null) window.clearInterval(this.intervalId);
    this.intervalId = null;
  }
};

// src/commands.ts
function registerCommands(plugin) {
  plugin.addCommand({
    id: "open-panel",
    name: "\u6253\u5F00\u4FA7\u8FB9\u680F\u9762\u677F",
    callback: () => void plugin.activateView()
  });
  plugin.addCommand({
    id: "commit-all",
    name: "\u63D0\u4EA4\u5168\u90E8\u6539\u52A8",
    callback: () => void plugin.commitAll()
  });
  plugin.addCommand({
    id: "push",
    name: "\u63A8\u9001\u5230\u8FDC\u7AEF",
    callback: () => void plugin.push()
  });
  plugin.addCommand({
    id: "pull",
    name: "\u4ECE\u8FDC\u7AEF\u62C9\u53D6",
    callback: () => void plugin.pull()
  });
  plugin.addCommand({
    id: "commit-and-push",
    name: "\u63D0\u4EA4\u5E76\u63A8\u9001",
    callback: () => void plugin.commitAndPush()
  });
  plugin.addCommand({
    id: "history-stats",
    name: "\u6253\u5F00\u5386\u53F2\u7EDF\u8BA1",
    callback: () => void plugin.openStatsView()
  });
  plugin.addCommand({
    id: "show-changes",
    name: "\u67E5\u770B\u6539\u52A8",
    callback: () => void plugin.showChanges()
  });
  plugin.addCommand({
    id: "init-repo",
    name: "\u521D\u59CB\u5316\u4ED3\u5E93",
    callback: () => void plugin.initRepo()
  });
  plugin.addCommand({
    id: "refresh-status",
    name: "\u5237\u65B0\u72B6\u6001",
    callback: () => void plugin.refresh()
  });
}

// src/git/diff.ts
var import_node_fs = require("node:fs");
var import_node_path = __toESM(require("node:path"));

// src/git/exec.ts
var import_child_process = require("child_process");
function runGit(cwd, gitPath, args, options = {}) {
  return new Promise((resolve) => {
    var _a;
    (0, import_child_process.execFile)(
      gitPath,
      // quotepath=false：否则中文/空格路径会被输出成 "\346\225\264..." 这样的八进制转义。
      ["-c", "core.quotepath=false", ...args],
      {
        cwd,
        timeout: (_a = options.timeoutMs) != null ? _a : 3e4,
        maxBuffer: 32 * 1024 * 1024,
        windowsHide: true,
        env: {
          ...process.env,
          // 桌面端没有 TTY，交互式索要密码只会把进程挂死。
          GIT_TERMINAL_PROMPT: "0",
          GIT_OPTIONAL_LOCKS: "0"
        }
      },
      (error, stdout, stderr) => {
        if (!error) {
          resolve({ code: 0, stdout, stderr });
          return;
        }
        const err = error;
        const numericCode = typeof err.code === "number" ? err.code : -1;
        const spawnError = typeof err.code === "string" ? err.code : err.killed ? "timeout" : void 0;
        resolve({ code: numericCode, stdout, stderr, spawnError });
      }
    );
  });
}
var GitQueue = class {
  constructor() {
    this.tail = Promise.resolve();
  }
  add(task) {
    const run = this.tail.then(task, task);
    this.tail = run.catch(() => void 0);
    return run;
  }
};
function firstLine(text) {
  const line = text.split(/\r?\n/).find((l) => l.trim().length > 0);
  return line ? line.trim() : "";
}

// src/git/diff.ts
var META_PREFIXES = [
  "diff --git",
  "index ",
  "--- ",
  "+++ ",
  "new file mode",
  "deleted file mode",
  "old mode",
  "new mode",
  "similarity index",
  "rename from",
  "rename to",
  "Binary files",
  "GIT binary patch"
];
function parseDiff(raw) {
  const lines = [];
  for (const text of raw.split("\n")) {
    if (text.length === 0) continue;
    let kind = "context";
    if (text.startsWith("@@")) kind = "hunk";
    else if (META_PREFIXES.some((prefix) => text.startsWith(prefix))) kind = "meta";
    else if (text.startsWith("+")) kind = "add";
    else if (text.startsWith("-")) kind = "del";
    else if (text.startsWith("\\")) kind = "meta";
    lines.push({ kind, text });
  }
  return lines;
}
function diffStats(lines) {
  let additions = 0;
  let deletions = 0;
  for (const line of lines) {
    if (line.kind === "add") additions++;
    else if (line.kind === "del") deletions++;
  }
  return { additions, deletions };
}
async function readFileDiff(ctx, filePath) {
  let res = await runGit(ctx.cwd, ctx.gitPath, [
    "diff",
    "--no-color",
    "--unified=3",
    "HEAD",
    "--",
    filePath
  ]);
  if (res.code !== 0) {
    res = await runGit(ctx.cwd, ctx.gitPath, [
      "diff",
      "--no-color",
      "--unified=3",
      "--",
      filePath
    ]);
  }
  return res.code === 0 ? res.stdout : "";
}
var MAX_PREVIEW_BYTES = 2 * 1024 * 1024;
async function readCommitFileDiff(ctx, hash, filePath) {
  const res = await runGit(ctx.cwd, ctx.gitPath, [
    "show",
    "--no-color",
    "--unified=3",
    "--format=",
    hash,
    "--",
    filePath
  ]);
  return res.code === 0 ? res.stdout : "";
}
async function readUntrackedDiff(ctx, filePath) {
  const fullPath = import_node_path.default.join(ctx.cwd, ...filePath.split("/"));
  let size;
  try {
    const stat = await import_node_fs.promises.stat(fullPath);
    if (!stat.isFile()) return { text: "", note: "\u4E0D\u662F\u666E\u901A\u6587\u4EF6\uFF0C\u65E0\u6CD5\u9884\u89C8\u3002" };
    size = stat.size;
  } catch (e) {
    return { text: "", note: "\u6587\u4EF6\u4E0D\u5B58\u5728\u6216\u65E0\u6CD5\u8BFB\u53D6\u3002" };
  }
  if (size > MAX_PREVIEW_BYTES) {
    return { text: "", note: `\u6587\u4EF6\u8FC7\u5927\uFF08${Math.round(size / 1024)} KB\uFF09\uFF0C\u4E0D\u9884\u89C8\u3002` };
  }
  const content = await import_node_fs.promises.readFile(fullPath, "utf8");
  if (content.includes("\0")) return { text: "", note: "\u4E8C\u8FDB\u5236\u6587\u4EF6\uFF0C\u65E0\u6CD5\u9884\u89C8\u3002" };
  const normalized = content.replace(/\r\n/g, "\n");
  const body = normalized.endsWith("\n") ? normalized.slice(0, -1) : normalized;
  return {
    text: body.split("\n").map((line) => `+${line}`).join("\n")
  };
}

// src/git/historyData.ts
var FIELD = "";
var RECORD = "";
function pad2(value) {
  return value < 10 ? `0${value}` : String(value);
}
function toUTC(date) {
  const [y, m, d] = date.split("-").map(Number);
  return Date.UTC(y != null ? y : 1970, (m != null ? m : 1) - 1, d != null ? d : 1);
}
function fromUTC(timestamp) {
  const d = new Date(timestamp);
  return `${d.getUTCFullYear()}-${pad2(d.getUTCMonth() + 1)}-${pad2(d.getUTCDate())}`;
}
function parseNumstatLog(raw) {
  var _a;
  const commits = [];
  for (const record of raw.split(RECORD)) {
    const body = record.replace(/^\n+/, "");
    if (!body.trim()) continue;
    const lines = body.split("\n");
    const header = (_a = lines[0]) != null ? _a : "";
    const [hash, date = "", ...subjectParts] = header.split(FIELD);
    if (!hash || !date) continue;
    let files = 0;
    let total = 0;
    for (const line of lines.slice(1)) {
      if (!line.trim()) continue;
      const parts = line.split("	");
      const added = parts[0];
      const deleted = parts[1];
      if (added === void 0 || deleted === void 0) continue;
      files += 1;
      if (added === "-" || deleted === "-") continue;
      const a = Number.parseInt(added, 10);
      const d = Number.parseInt(deleted, 10);
      if (!Number.isNaN(a)) total += a;
      if (!Number.isNaN(d)) total += d;
    }
    commits.push({
      hash,
      date,
      subject: subjectParts.join(FIELD),
      files,
      lines: total
    });
  }
  return commits;
}
function eachDay(startDate, endDate) {
  const days = [];
  const end = toUTC(endDate);
  for (let t = toUTC(startDate); t <= end; t += 864e5) {
    days.push(fromUTC(t));
  }
  return days;
}
function aggregateDaily(commits, startDate, endDate) {
  const buckets = /* @__PURE__ */ new Map();
  for (const day of eachDay(startDate, endDate)) {
    buckets.set(day, { date: day, commits: 0, files: 0, lines: 0 });
  }
  for (const commit of commits) {
    const bucket = buckets.get(commit.date);
    if (!bucket) continue;
    bucket.commits += 1;
    bucket.files += commit.files;
    bucket.lines += commit.lines;
  }
  return [...buckets.values()];
}
function aggregateByWeek(daily) {
  const weeks = [];
  let currentKey = "";
  for (const day of daily) {
    const weekday = weekdayIndex(day.date);
    const weekStart = fromUTC(toUTC(day.date) - weekday * 864e5);
    if (weekStart !== currentKey) {
      currentKey = weekStart;
      weeks.push({ weekStart, commits: 0, files: 0, lines: 0 });
    }
    const bucket = weeks[weeks.length - 1];
    if (!bucket) continue;
    bucket.commits += day.commits;
    bucket.files += day.files;
    bucket.lines += day.lines;
  }
  return weeks;
}
function weekdayIndex(date) {
  return (new Date(toUTC(date)).getUTCDay() + 6) % 7;
}
function todayString() {
  const now = /* @__PURE__ */ new Date();
  return `${now.getFullYear()}-${pad2(now.getMonth() + 1)}-${pad2(now.getDate())}`;
}
function shiftDays(date, days) {
  return fromUTC(toUTC(date) + days * 864e5);
}

// src/git/history.ts
async function readCommitStats(ctx, maxCommits = 3e3) {
  const res = await runGit(ctx.cwd, ctx.gitPath, [
    "log",
    `--max-count=${maxCommits}`,
    "--date=short",
    "--numstat",
    "--pretty=format:%x1e%H%x1f%ad%x1f%s"
  ]);
  return res.code === 0 ? parseNumstatLog(res.stdout) : [];
}

// src/git/log.ts
var FIELD2 = "";
var RECORD2 = "";
function parseLogOutput(raw) {
  const entries = [];
  for (const record of raw.split(RECORD2)) {
    const trimmed = record.trim();
    if (!trimmed) continue;
    const [hash = "", shortHash = "", author = "", date = "", subject = "", refs = ""] = trimmed.split(FIELD2);
    entries.push({
      hash,
      shortHash,
      author,
      date,
      subject,
      refs: refs.split(",").map((ref) => ref.trim()).filter((ref) => ref.length > 0)
    });
  }
  return entries;
}
function parseNameStatus(raw) {
  var _a;
  const tokens = raw.split("\0");
  const files = [];
  let i = 0;
  while (i < tokens.length) {
    const status = (_a = tokens[i]) != null ? _a : "";
    if (!status) break;
    const isRename = status.startsWith("R") || status.startsWith("C");
    const first = tokens[i + 1];
    const second = isRename ? tokens[i + 2] : first;
    if (!first || !second) break;
    files.push({
      status: status.charAt(0),
      path: second,
      from: isRename ? first : void 0
    });
    i += isRename ? 3 : 2;
  }
  return files;
}
async function readLog(ctx, limit = 30) {
  const res = await runGit(ctx.cwd, ctx.gitPath, [
    "log",
    `--max-count=${limit}`,
    "--date=short",
    `--pretty=format:%H${FIELD2}%h${FIELD2}%an${FIELD2}%ad${FIELD2}%s${FIELD2}%D${RECORD2}`
  ]);
  return res.code === 0 ? parseLogOutput(res.stdout) : [];
}
async function readCommitFiles(ctx, hash) {
  const res = await runGit(ctx.cwd, ctx.gitPath, [
    "show",
    "--pretty=format:",
    "--name-status",
    "-z",
    hash
  ]);
  return res.code === 0 ? parseNameStatus(res.stdout) : [];
}

// src/git/ops.ts
var import_node_fs2 = require("node:fs");
var import_node_path2 = __toESM(require("node:path"));

// src/git/status.ts
var CONFLICT_PAIRS = /* @__PURE__ */ new Set(["DD", "AU", "UD", "UA", "DU", "AA", "UU"]);
function isConflict(change) {
  return CONFLICT_PAIRS.has(change.index + change.worktree);
}
function parseStatusOutput(raw, branch) {
  const tokens = raw.split("\0");
  const files = [];
  for (let i = 0; i < tokens.length; i++) {
    const entry = tokens[i];
    if (!entry || entry.length < 4) continue;
    const index = entry.charAt(0);
    const worktree = entry.charAt(1);
    const path4 = entry.slice(3);
    let origPath;
    if (index === "R" || index === "C" || worktree === "R" || worktree === "C") {
      i += 1;
      const next = tokens[i];
      if (next) origPath = next;
    }
    files.push({ path: path4, index, worktree, origPath });
  }
  return {
    branch,
    files,
    hasConflicts: files.some(isConflict)
  };
}
function statusLabel(change) {
  if (isConflict(change)) return "\u51B2\u7A81";
  if (change.index === "?" && change.worktree === "?") return "\u672A\u8DDF\u8E2A";
  if (change.index === "D" || change.worktree === "D") return "\u5DF2\u5220\u9664";
  if (change.index === "A") return change.worktree === " " ? "\u65B0\u589E" : "\u65B0\u589E(\u672A\u6682\u5B58)";
  if (change.index === "R") return "\u91CD\u547D\u540D";
  if (change.index === "C") return "\u590D\u5236";
  if (change.index !== " " && change.index !== "?") return "\u5DF2\u6682\u5B58";
  return "\u5DF2\u4FEE\u6539";
}
async function readStatus(ctx) {
  const branchRes = await runGit(ctx.cwd, ctx.gitPath, [
    "rev-parse",
    "--abbrev-ref",
    "HEAD"
  ]);
  const branch = branchRes.code === 0 ? branchRes.stdout.trim() : null;
  const statusRes = await runGit(ctx.cwd, ctx.gitPath, [
    "status",
    "--porcelain=v1",
    "-z",
    "--untracked-files=all"
  ]);
  return parseStatusOutput(statusRes.code === 0 ? statusRes.stdout : "", branch);
}

// src/git/ops.ts
var NETWORK_TIMEOUT_MS = 12e4;
function fail(res) {
  if (res.spawnError === "ENOENT") {
    return { ok: false, message: "\u627E\u4E0D\u5230 git \u53EF\u6267\u884C\u6587\u4EF6\uFF0C\u8BF7\u68C0\u67E5\u8BBE\u7F6E\u91CC\u7684\u8DEF\u5F84\u3002" };
  }
  if (res.spawnError === "timeout") {
    return { ok: false, message: "git \u64CD\u4F5C\u8D85\u65F6\uFF08\u7F51\u7EDC\u6216\u51ED\u636E\u53EF\u80FD\u6709\u95EE\u9898\uFF09\u3002" };
  }
  const detail = firstLine(res.stderr) || firstLine(res.stdout) || "\u672A\u77E5\u9519\u8BEF";
  return { ok: false, message: detail };
}
async function commitAll(ctx, message) {
  const status = await readStatus(ctx);
  if (status.files.length === 0) {
    return { ok: true, message: "\u6CA1\u6709\u9700\u8981\u63D0\u4EA4\u7684\u6539\u52A8\u3002", count: 0 };
  }
  const add = await runGit(ctx.cwd, ctx.gitPath, ["add", "-A"]);
  if (add.code !== 0) return fail(add);
  const commit = await runGit(ctx.cwd, ctx.gitPath, ["commit", "-m", message]);
  if (commit.code !== 0) return fail(commit);
  return { ok: true, message: `\u5DF2\u63D0\u4EA4 ${status.files.length} \u4E2A\u6539\u52A8\u3002`, count: status.files.length };
}
async function push(ctx) {
  const branchRes = await runGit(ctx.cwd, ctx.gitPath, [
    "rev-parse",
    "--abbrev-ref",
    "HEAD"
  ]);
  if (branchRes.code !== 0) {
    return { ok: false, message: "\u5F53\u524D\u4ED3\u5E93\u8FD8\u6CA1\u6709\u4EFB\u4F55\u63D0\u4EA4\u3002" };
  }
  const branch = branchRes.stdout.trim();
  const upstream = await runGit(ctx.cwd, ctx.gitPath, [
    "rev-parse",
    "--abbrev-ref",
    "--symbolic-full-name",
    "@{u}"
  ]);
  const args = upstream.code === 0 ? ["push"] : ["push", "-u", "origin", branch];
  const res = await runGit(ctx.cwd, ctx.gitPath, args, {
    timeoutMs: NETWORK_TIMEOUT_MS
  });
  if (res.code !== 0) return fail(res);
  return { ok: true, message: `\u5DF2\u63A8\u9001\u5230 ${upstream.code === 0 ? upstream.stdout.trim() : `origin/${branch}`}\u3002` };
}
async function pull(ctx) {
  const res = await runGit(
    ctx.cwd,
    ctx.gitPath,
    ["pull", "--no-rebase", "--no-edit"],
    { timeoutMs: NETWORK_TIMEOUT_MS }
  );
  if (res.code !== 0) return fail(res);
  const status = await readStatus(ctx);
  if (status.hasConflicts) {
    return { ok: false, message: "\u62C9\u53D6\u5B8C\u6210\uFF0C\u4F46\u5B58\u5728\u5408\u5E76\u51B2\u7A81\uFF0C\u9700\u8981\u624B\u52A8\u89E3\u51B3\u3002" };
  }
  return { ok: true, message: "\u5DF2\u4ECE\u8FDC\u7AEF\u62C9\u53D6\u3002" };
}
async function initRepo(ctx) {
  const res = await runGit(ctx.cwd, ctx.gitPath, ["init"]);
  if (res.code !== 0) return fail(res);
  return { ok: true, message: "\u5DF2\u521D\u59CB\u5316 git \u4ED3\u5E93\u3002" };
}
async function commitFile(ctx, filePath, message) {
  const add = await runGit(ctx.cwd, ctx.gitPath, ["add", "-A", "--", filePath]);
  if (add.code !== 0) return fail(add);
  const commit = await runGit(ctx.cwd, ctx.gitPath, [
    "commit",
    "-m",
    message,
    "--",
    filePath
  ]);
  if (commit.code !== 0) return fail(commit);
  return { ok: true, message: `\u5DF2\u63D0\u4EA4 ${filePath}` };
}
async function discardFile(ctx, change) {
  if (isConflict(change)) {
    return { ok: false, message: "\u51B2\u7A81\u6587\u4EF6\u4E0D\u652F\u6301\u4E00\u952E\u64A4\u9500\uFF0C\u8BF7\u624B\u52A8\u89E3\u51B3\u3002" };
  }
  if (change.index === "?" && change.worktree === "?") {
    const fullPath = import_node_path2.default.join(ctx.cwd, ...change.path.split("/"));
    try {
      await import_node_fs2.promises.unlink(fullPath);
      return { ok: true, message: `\u5DF2\u5220\u9664\u672A\u8DDF\u8E2A\u6587\u4EF6 ${change.path}` };
    } catch (error) {
      return {
        ok: false,
        message: `\u5220\u9664\u5931\u8D25\uFF1A${error.message}`
      };
    }
  }
  const restore = await runGit(ctx.cwd, ctx.gitPath, [
    "restore",
    "--source=HEAD",
    "--staged",
    "--worktree",
    "--",
    change.path
  ]);
  if (restore.code === 0) {
    const message = change.index === "A" ? `\u5DF2\u64A4\u9500\u65B0\u589E\u6587\u4EF6 ${change.path}` : `\u5DF2\u64A4\u9500 ${change.path} \u7684\u4FEE\u6539`;
    return { ok: true, message };
  }
  const reset = await runGit(ctx.cwd, ctx.gitPath, ["reset", "-q", "--", change.path]);
  if (reset.code === 0) {
    return {
      ok: true,
      message: `\u5DF2\u53D6\u6D88\u6682\u5B58 ${change.path}\uFF08\u5DE5\u4F5C\u533A\u5185\u5BB9\u5DF2\u4FDD\u7559\uFF09`
    };
  }
  return fail(restore);
}

// src/git/repo.ts
async function detectRepo(ctx) {
  const version = await runGit(ctx.cwd, ctx.gitPath, ["--version"]);
  if (version.spawnError === "ENOENT") {
    return {
      kind: "no-git",
      detail: `\u627E\u4E0D\u5230 git \u53EF\u6267\u884C\u6587\u4EF6\u300C${ctx.gitPath}\u300D\uFF0C\u8BF7\u5728\u63D2\u4EF6\u8BBE\u7F6E\u91CC\u586B\u5199\u5B8C\u6574\u8DEF\u5F84\u3002`
    };
  }
  if (version.code !== 0) {
    return {
      kind: "error",
      detail: `git \u65E0\u6CD5\u6267\u884C\uFF1A${version.stderr.trim() || version.stdout.trim() || "\u672A\u77E5\u9519\u8BEF"}`
    };
  }
  const inside = await runGit(ctx.cwd, ctx.gitPath, [
    "rev-parse",
    "--is-inside-work-tree"
  ]);
  if (inside.code !== 0 || inside.stdout.trim() !== "true") {
    return { kind: "no-repo", detail: "\u5F53\u524D vault \u4E0D\u662F git \u4ED3\u5E93\u3002" };
  }
  return { kind: "ok", detail: version.stdout.trim() };
}

// src/git/stats.ts
var import_node_fs3 = require("node:fs");
var import_node_path3 = __toESM(require("node:path"));
function sumNumstat(raw) {
  let total = 0;
  for (const line of raw.split("\n")) {
    if (!line.trim()) continue;
    const parts = line.split("	");
    const added = parts[0];
    const deleted = parts[1];
    if (added === void 0 || deleted === void 0) continue;
    if (added === "-" || deleted === "-") {
      total += 1;
      continue;
    }
    const a = Number.parseInt(added, 10);
    const d = Number.parseInt(deleted, 10);
    if (Number.isNaN(a) || Number.isNaN(d)) continue;
    total += a + d;
  }
  return total;
}
var MAX_UNTRACKED_FILES = 50;
var MAX_UNTRACKED_BYTES = 512 * 1024;
async function countChangedLines(ctx, untracked) {
  let res = await runGit(ctx.cwd, ctx.gitPath, ["diff", "--numstat", "HEAD"]);
  if (res.code !== 0) {
    res = await runGit(ctx.cwd, ctx.gitPath, ["diff", "--numstat"]);
  }
  let total = res.code === 0 ? sumNumstat(res.stdout) : 0;
  for (const file of untracked.slice(0, MAX_UNTRACKED_FILES)) {
    const fullPath = import_node_path3.default.join(ctx.cwd, ...file.split("/"));
    try {
      const stat = await import_node_fs3.promises.stat(fullPath);
      if (!stat.isFile() || stat.size > MAX_UNTRACKED_BYTES) continue;
      const content = await import_node_fs3.promises.readFile(fullPath, "utf8");
      if (content.includes("\0")) continue;
      const lines = content.split("\n");
      total += content.endsWith("\n") ? lines.length - 1 : lines.length;
    } catch (e) {
    }
  }
  return total;
}

// src/settings.ts
var import_obsidian = require("obsidian");
var DEFAULT_SETTINGS = {
  gitPath: "git",
  commitMessageTemplate: "vault backup: {{date}}",
  showStatusBar: true,
  autoOpenPanel: true,
  autoCommitMode: "interval",
  autoCommitInterval: 10,
  smartFileThreshold: 5,
  smartLineThreshold: 200,
  autoPush: false
};
var AUTO_COMMIT_MODES = [
  "off",
  "interval",
  "smart"
];
function normalizeSettings(stored) {
  const source = stored != null ? stored : {};
  const settings = { ...DEFAULT_SETTINGS };
  const target = settings;
  for (const key of Object.keys(DEFAULT_SETTINGS)) {
    const value = source[key];
    if (value !== void 0 && typeof value === typeof target[key]) {
      target[key] = value;
    }
  }
  if (source.autoCommitMode === void 0 && typeof source.autoCommitEnabled === "boolean") {
    settings.autoCommitMode = source.autoCommitEnabled ? "interval" : "off";
  }
  if (!AUTO_COMMIT_MODES.includes(settings.autoCommitMode)) {
    settings.autoCommitMode = DEFAULT_SETTINGS.autoCommitMode;
  }
  return settings;
}
function pad22(value) {
  return value < 10 ? `0${value}` : String(value);
}
function formatDate(date, pattern) {
  return pattern.replace(/YYYY/g, String(date.getFullYear())).replace(/MM/g, pad22(date.getMonth() + 1)).replace(/DD/g, pad22(date.getDate())).replace(/HH/g, pad22(date.getHours())).replace(/mm/g, pad22(date.getMinutes())).replace(/ss/g, pad22(date.getSeconds()));
}
function formatCommitMessage(template, date = /* @__PURE__ */ new Date()) {
  const text = template.trim() || DEFAULT_SETTINGS.commitMessageTemplate;
  return text.replace(/\{\{date\}\}/g, formatDate(date, "YYYY-MM-DD HH:mm:ss"));
}
var RionGitSettingTab = class extends import_obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    new import_obsidian.Setting(containerEl).setName("Git \u53EF\u6267\u884C\u6587\u4EF6").setDesc(
      "\u9ED8\u8BA4\u4E3A git\u3002\u82E5\u4ECE\u5FEB\u6377\u65B9\u5F0F\u542F\u52A8 Obsidian \u65F6\u63D0\u793A\u627E\u4E0D\u5230 git\uFF0C\u8BF7\u586B\u5199\u5B8C\u6574\u8DEF\u5F84\uFF0C\u4F8B\u5982 C:\\Program Files\\Git\\cmd\\git.exe"
    ).addText(
      (text) => text.setPlaceholder("git").setValue(this.plugin.settings.gitPath).onChange(async (value) => {
        this.plugin.settings.gitPath = value.trim() || "git";
        await this.plugin.saveSettings();
        await this.plugin.refresh();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u63D0\u4EA4\u6D88\u606F\u6A21\u677F").setDesc("{{date}} \u4F1A\u66FF\u6362\u4E3A\u5F53\u524D\u65F6\u95F4\u3002").addText(
      (text) => text.setPlaceholder(DEFAULT_SETTINGS.commitMessageTemplate).setValue(this.plugin.settings.commitMessageTemplate).onChange(async (value) => {
        this.plugin.settings.commitMessageTemplate = value.trim() || DEFAULT_SETTINGS.commitMessageTemplate;
        await this.plugin.saveSettings();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u81EA\u52A8\u5907\u4EFD").setHeading();
    new import_obsidian.Setting(containerEl).setName("\u81EA\u52A8\u63D0\u4EA4\u65B9\u5F0F").setDesc("\u4E09\u79CD\u65B9\u5F0F\u4E92\u65A5\uFF1A\u5173\u95ED\u3001\u5B9A\u65F6\uFF08\u56FA\u5B9A\u95F4\u9694\uFF09\u3001\u667A\u80FD\uFF08\u6539\u52A8\u8FBE\u5230\u9608\u503C\u65F6\uFF09\u3002").addDropdown(
      (dropdown) => dropdown.addOption("off", "\u5173\u95ED").addOption("interval", "\u5B9A\u65F6").addOption("smart", "\u667A\u80FD").setValue(this.plugin.settings.autoCommitMode).onChange(async (value) => {
        this.plugin.settings.autoCommitMode = value;
        await this.plugin.saveSettings();
        this.plugin.applyAutoSettings();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u5B9A\u65F6\u63D0\u4EA4\u95F4\u9694").setDesc("\u4EC5\u300C\u5B9A\u65F6\u300D\u6A21\u5F0F\u751F\u6548\u3002\u5355\u4F4D\u5206\u949F\uFF0C0 \u8868\u793A\u4E0D\u63D0\u4EA4\u3002").addSlider(
      (slider) => slider.setLimits(0, 60, 1).setValue(this.plugin.settings.autoCommitInterval).onChange(async (value) => {
        this.plugin.settings.autoCommitInterval = value;
        await this.plugin.saveSettings();
        this.plugin.applyAutoSettings();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u667A\u80FD\u6A21\u5F0F\uFF1A\u6539\u52A8\u6587\u4EF6\u6570\u9608\u503C").setDesc("\u4EC5\u300C\u667A\u80FD\u300D\u6A21\u5F0F\u751F\u6548\u3002\u6539\u52A8\u6587\u4EF6\u8FBE\u5230\u8BE5\u6570\u91CF\u5373\u81EA\u52A8\u63D0\u4EA4\uFF0C0 \u8868\u793A\u4E0D\u6309\u6587\u4EF6\u6570\u5224\u65AD\u3002").addSlider(
      (slider) => slider.setLimits(0, 30, 1).setValue(this.plugin.settings.smartFileThreshold).onChange(async (value) => {
        this.plugin.settings.smartFileThreshold = value;
        await this.plugin.saveSettings();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u667A\u80FD\u6A21\u5F0F\uFF1A\u6539\u52A8\u884C\u6570\u9608\u503C").setDesc("\u4EC5\u300C\u667A\u80FD\u300D\u6A21\u5F0F\u751F\u6548\u3002\u65B0\u589E\u4E0E\u5220\u9664\u884C\u6570\u4E4B\u548C\u8FBE\u5230\u8BE5\u503C\u5373\u81EA\u52A8\u63D0\u4EA4\uFF0C0 \u8868\u793A\u4E0D\u6309\u884C\u6570\u5224\u65AD\u3002").addSlider(
      (slider) => slider.setLimits(0, 2e3, 20).setValue(this.plugin.settings.smartLineThreshold).onChange(async (value) => {
        this.plugin.settings.smartLineThreshold = value;
        await this.plugin.saveSettings();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u81EA\u52A8\u63D0\u4EA4\u540E\u63A8\u9001").setDesc("\u9700\u8981\u5DF2\u7ECF\u914D\u7F6E\u597D\u8FDC\u7AEF\u3002\u63A8\u9001\u5931\u8D25\u540E\u4F1A\u81EA\u52A8\u6682\u505C 5 \u5206\u949F\u3002").addToggle(
      (toggle) => toggle.setValue(this.plugin.settings.autoPush).onChange(async (value) => {
        this.plugin.settings.autoPush = value;
        await this.plugin.saveSettings();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u754C\u9762").setHeading();
    new import_obsidian.Setting(containerEl).setName("\u542F\u52A8\u65F6\u81EA\u52A8\u6253\u5F00\u9762\u677F").setDesc("Obsidian \u542F\u52A8\u540E\u81EA\u52A8\u5728\u53F3\u4FA7\u8FB9\u680F\u6253\u5F00 Rion Git\u3002\u5173\u95ED\u540E\u53EF\u7528 Ribbon \u56FE\u6807\u3001\u72B6\u6001\u680F\u6216\u547D\u4EE4\u624B\u52A8\u6253\u5F00\u3002").addToggle(
      (toggle) => toggle.setValue(this.plugin.settings.autoOpenPanel).onChange(async (value) => {
        this.plugin.settings.autoOpenPanel = value;
        await this.plugin.saveSettings();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u663E\u793A\u72B6\u6001\u680F").setDesc("\u5728\u7A97\u53E3\u5E95\u90E8\u663E\u793A\u6539\u52A8\u6570\u91CF\u4E0E\u64CD\u4F5C\u72B6\u6001\uFF08\u91CD\u8F7D\u63D2\u4EF6\u540E\u751F\u6548\uFF09\u3002").addToggle(
      (toggle) => toggle.setValue(this.plugin.settings.showStatusBar).onChange(async (value) => {
        this.plugin.settings.showStatusBar = value;
        await this.plugin.saveSettings();
      })
    );
    new import_obsidian.Setting(containerEl).setName("\u4FA7\u8FB9\u680F\u9762\u677F").setDesc("\u5728\u53F3\u4FA7\u8FB9\u680F\u6253\u5F00 Rion Git \u9762\u677F\u3002").addButton(
      (button) => button.setButtonText("\u6253\u5F00").onClick(() => void this.plugin.activateView())
    );
    new import_obsidian.Setting(containerEl).setName("\u64CD\u4F5C").setHeading();
    new import_obsidian.Setting(containerEl).setName("\u63D0\u4EA4\u5168\u90E8\u6539\u52A8").addButton(
      (button) => button.setButtonText("\u63D0\u4EA4").onClick(() => void this.plugin.commitAll())
    );
    new import_obsidian.Setting(containerEl).setName("\u63D0\u4EA4\u5E76\u63A8\u9001").addButton(
      (button) => button.setButtonText("\u6267\u884C").onClick(() => void this.plugin.commitAndPush())
    );
    new import_obsidian.Setting(containerEl).setName("\u4ECE\u8FDC\u7AEF\u62C9\u53D6").addButton(
      (button) => button.setButtonText("\u62C9\u53D6").onClick(() => void this.plugin.pull())
    );
    new import_obsidian.Setting(containerEl).setName("\u521D\u59CB\u5316\u4ED3\u5E93").setDesc("\u4EC5\u5F53 vault \u8FD8\u4E0D\u662F git \u4ED3\u5E93\u65F6\u4F7F\u7528\u3002").addButton(
      (button) => button.setButtonText("\u521D\u59CB\u5316").onClick(() => void this.plugin.initRepo())
    );
  }
};

// src/ui/changesModal.ts
var import_obsidian2 = require("obsidian");
var MAX_ROWS = 100;
var ChangesModal = class extends import_obsidian2.Modal {
  constructor(app, plugin, status) {
    super(app);
    this.plugin = plugin;
    this.status = status;
  }
  onOpen() {
    var _a;
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("rion-git-modal");
    contentEl.createEl("h2", { text: `Git \u6539\u52A8\uFF08${this.status.files.length}\uFF09` });
    contentEl.createEl("p", {
      text: `\u5206\u652F\uFF1A${(_a = this.status.branch) != null ? _a : "\uFF08\u8FD8\u6CA1\u6709\u63D0\u4EA4\uFF09"}`,
      cls: "rion-git-branch"
    });
    const list = contentEl.createDiv({ cls: "rion-git-file-list" });
    if (this.status.files.length === 0) {
      list.createEl("p", { text: "\u5DE5\u4F5C\u533A\u662F\u5E72\u51C0\u7684\u3002" });
    }
    for (const file of this.status.files.slice(0, MAX_ROWS)) {
      const row = list.createDiv({ cls: "rion-git-file-row" });
      row.createSpan({ text: statusLabel(file), cls: "rion-git-file-state" });
      row.createSpan({ text: file.path, cls: "rion-git-file-path" });
    }
    if (this.status.files.length > MAX_ROWS) {
      list.createEl("p", {
        text: `\u8FD8\u6709 ${this.status.files.length - MAX_ROWS} \u4E2A\u6587\u4EF6\u672A\u663E\u793A\u2026`
      });
    }
    const actions = contentEl.createDiv({ cls: "rion-git-modal-actions" });
    const addButton = (label, action) => {
      const button = actions.createEl("button", { text: label });
      button.onclick = () => {
        this.close();
        action();
      };
    };
    addButton("\u63D0\u4EA4\u5168\u90E8", () => void this.plugin.commitAll());
    addButton("\u63A8\u9001", () => void this.plugin.push());
    addButton("\u62C9\u53D6", () => void this.plugin.pull());
  }
  onClose() {
    this.contentEl.empty();
  }
};

// src/ui/confirmModal.ts
var import_obsidian3 = require("obsidian");
var ConfirmModal = class extends import_obsidian3.Modal {
  constructor(app, message, onConfirm) {
    super(app);
    this.message = message;
    this.onConfirm = onConfirm;
  }
  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.createEl("h3", { text: "\u786E\u8BA4\u64CD\u4F5C" });
    contentEl.createEl("p", { text: this.message });
    const actions = contentEl.createDiv({ cls: "rion-git-modal-actions" });
    const cancel = actions.createEl("button", { text: "\u53D6\u6D88" });
    cancel.onclick = () => this.close();
    const confirm = actions.createEl("button", { text: "\u786E\u5B9A", cls: "mod-warning" });
    confirm.onclick = () => {
      this.close();
      this.onConfirm();
    };
  }
  onClose() {
    this.contentEl.empty();
  }
};

// src/ui/diffView.ts
var import_obsidian4 = require("obsidian");
var VIEW_TYPE_RION_GIT_DIFF = "rion-git-diff";
var DiffView = class extends import_obsidian4.ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.filePath = "";
    this.untracked = false;
    this.commitHash = "";
    this.renderToken = 0;
  }
  getViewType() {
    return VIEW_TYPE_RION_GIT_DIFF;
  }
  getDisplayText() {
    var _a;
    if (!this.filePath) return "Git \u5DEE\u5F02";
    const name = (_a = this.filePath.split("/").pop()) != null ? _a : this.filePath;
    return this.commitHash ? `\u5DEE\u5F02\uFF1A${name} @ ${this.commitHash.slice(0, 7)}` : `\u5DEE\u5F02\uFF1A${name}`;
  }
  getIcon() {
    return "file-diff";
  }
  getState() {
    return {
      path: this.filePath,
      untracked: this.untracked,
      commit: this.commitHash || void 0
    };
  }
  async setState(state, result) {
    var _a, _b, _c;
    this.filePath = (_a = state == null ? void 0 : state.path) != null ? _a : "";
    this.untracked = (_b = state == null ? void 0 : state.untracked) != null ? _b : false;
    this.commitHash = (_c = state == null ? void 0 : state.commit) != null ? _c : "";
    await super.setState(state, result);
    await this.render();
  }
  async onOpen() {
    await this.render();
  }
  async onClose() {
    this.contentEl.empty();
  }
  async render() {
    const token = ++this.renderToken;
    const el = this.contentEl;
    el.empty();
    el.addClass("rion-git-diff-view");
    const header = el.createDiv({ cls: "rion-git-diff-header" });
    const title = header.createSpan({ cls: "rion-git-diff-title" });
    title.createSpan({ text: this.filePath || "\u672A\u9009\u62E9\u6587\u4EF6" });
    if (this.commitHash) {
      title.createSpan({
        cls: "rion-git-diff-commit",
        text: ` @ ${this.commitHash.slice(0, 7)}`
      });
    }
    const meta = header.createDiv({ cls: "rion-git-diff-meta" });
    const actions = header.createDiv({ cls: "rion-git-diff-actions" });
    const addButton = (icon, label, handler) => {
      const button = actions.createEl("button", { cls: "clickable-icon" });
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
      (0, import_obsidian4.setIcon)(button, icon);
      button.onclick = () => handler();
    };
    addButton("refresh-cw", "\u91CD\u65B0\u8BFB\u53D6\u5DEE\u5F02", () => void this.render());
    if (!this.commitHash) {
      addButton("check", "\u63D0\u4EA4\u6B64\u6587\u4EF6", () => void this.commit());
      addButton("rotate-ccw", "\u64A4\u9500\u4FEE\u6539", () => void this.discard());
    }
    const body = el.createDiv({ cls: "rion-git-diff" });
    body.createDiv({ cls: "rion-git-empty", text: "\u8BFB\u53D6\u4E2D\u2026" });
    if (!this.filePath) return;
    const data = await this.plugin.loadDiff(this.filePath, this.untracked, this.commitHash);
    if (token !== this.renderToken) return;
    body.empty();
    meta.createSpan({ cls: "rion-git-add", text: `+${data.stats.additions}` });
    meta.createSpan({ cls: "rion-git-del", text: `-${data.stats.deletions}` });
    if (data.note) {
      body.createDiv({ cls: "rion-git-empty", text: data.note });
    }
    for (const line of data.lines.slice(0, 5e3)) {
      body.createDiv({
        cls: `rion-git-diff-line is-${line.kind}`,
        text: line.text
      });
    }
    if (data.lines.length > 5e3) {
      body.createDiv({
        cls: "rion-git-empty",
        text: `\u8FD8\u6709 ${data.lines.length - 5e3} \u884C\u672A\u663E\u793A\u2026`
      });
    }
  }
  async commit() {
    await this.plugin.commitFile(this.filePath);
    await this.render();
  }
  async discard() {
    await this.plugin.discardFile(this.plugin.findChange(this.filePath));
    await this.render();
  }
};

// src/ui/sidebarView.ts
var import_obsidian5 = require("obsidian");
var VIEW_TYPE_RION_GIT = "rion-git-sidebar";
var MAX_ROWS2 = 200;
function autoSummary(settings) {
  const push2 = settings.autoPush ? "\uFF0C\u5E76\u81EA\u52A8\u63A8\u9001" : "";
  if (settings.autoCommitMode === "interval") {
    return settings.autoCommitInterval > 0 ? `\u81EA\u52A8\u63D0\u4EA4\uFF1A\u6BCF ${settings.autoCommitInterval} \u5206\u949F${push2}` : "\u81EA\u52A8\u63D0\u4EA4\uFF1A\u5173\u95ED";
  }
  if (settings.autoCommitMode === "smart") {
    const parts = [];
    if (settings.smartFileThreshold > 0) {
      parts.push(`\u2265${settings.smartFileThreshold} \u4E2A\u6587\u4EF6`);
    }
    if (settings.smartLineThreshold > 0) {
      parts.push(`\u2265${settings.smartLineThreshold} \u884C`);
    }
    return parts.length > 0 ? `\u81EA\u52A8\u63D0\u4EA4\uFF1A${parts.join(" \u6216 ")}${push2}` : "\u81EA\u52A8\u63D0\u4EA4\uFF1A\u5173\u95ED";
  }
  return "\u81EA\u52A8\u63D0\u4EA4\uFF1A\u5173\u95ED";
}
function changeBadge(change) {
  if (isConflict(change)) return "!";
  if (change.index === "?" && change.worktree === "?") return "U";
  if (change.index === "D" || change.worktree === "D") return "D";
  if (change.index === "R" || change.worktree === "R") return "R";
  if (change.index === "A") return "A";
  return "M";
}
function splitPath(path4) {
  const index = path4.lastIndexOf("/");
  if (index === -1) return { name: path4, dir: "" };
  return { name: path4.slice(index + 1), dir: path4.slice(0, index) };
}
var RionGitView = class extends import_obsidian5.ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.collapsed = /* @__PURE__ */ new Set();
    this.expandedCommits = /* @__PURE__ */ new Set();
    this.commitFiles = /* @__PURE__ */ new Map();
    this.draft = "";
    this.messageEl = null;
    this.pendingRender = false;
    this.restoreFocus = false;
  }
  getViewType() {
    return VIEW_TYPE_RION_GIT;
  }
  getDisplayText() {
    return "Rion Git";
  }
  getIcon() {
    return "git-branch";
  }
  async onOpen() {
    this.render();
    void this.plugin.refresh();
  }
  async onClose() {
    this.contentEl.empty();
  }
  render(force = false) {
    if (!force && this.messageEl && document.activeElement === this.messageEl) {
      this.pendingRender = true;
      return;
    }
    this.pendingRender = false;
    const el = this.contentEl;
    el.empty();
    el.addClass("rion-git-sidebar");
    if (this.plugin.lastError) {
      el.createDiv({ cls: "rion-git-error", text: this.plugin.lastError });
    }
    this.renderCommitBox(el);
    this.renderChangesSection(el);
    this.renderHistorySection(el);
  }
  renderCommitBox(el) {
    var _a;
    const status = this.plugin.lastStatus;
    const box = el.createDiv({ cls: "rion-git-commit-box" });
    const input = box.createEl("textarea", {
      cls: "rion-git-message",
      attr: {
        rows: "2",
        placeholder: `\u6D88\u606F\uFF08Enter \u5728 "${(_a = status == null ? void 0 : status.branch) != null ? _a : "\u5F53\u524D\u5206\u652F"}" \u4E0A\u63D0\u4EA4\uFF09`
      }
    });
    input.value = this.draft;
    this.messageEl = input;
    if (this.restoreFocus) {
      this.restoreFocus = false;
      input.focus();
      input.setSelectionRange(input.value.length, input.value.length);
    }
    input.addEventListener("input", () => {
      this.draft = input.value;
    });
    input.addEventListener("blur", () => {
      if (!this.pendingRender) return;
      this.pendingRender = false;
      this.render(true);
    });
    input.addEventListener("keydown", (evt) => {
      if (evt.key !== "Enter" || evt.shiftKey) return;
      evt.preventDefault();
      void this.commit();
    });
    const actions = box.createDiv({ cls: "rion-git-commit-actions" });
    const commitButton = actions.createEl("button", { cls: "mod-cta rion-git-commit-btn" });
    (0, import_obsidian5.setIcon)(commitButton.createSpan({ cls: "rion-git-btn-icon" }), "check");
    commitButton.createSpan({ text: "\u63D0\u4EA4" });
    commitButton.onclick = () => void this.commit();
    const caret = actions.createEl("button", { cls: "mod-cta rion-git-caret" });
    caret.setAttribute("aria-label", "\u66F4\u591A\u63D0\u4EA4\u65B9\u5F0F");
    (0, import_obsidian5.setIcon)(caret, "chevron-down");
    caret.onclick = (evt) => {
      const menu = new import_obsidian5.Menu();
      menu.addItem(
        (item) => item.setTitle("\u63D0\u4EA4").setIcon("check").onClick(() => void this.commit())
      );
      menu.addItem(
        (item) => item.setTitle("\u63D0\u4EA4\u5E76\u63A8\u9001").setIcon("upload").onClick(() => void this.commitAndPush())
      );
      menu.showAtMouseEvent(evt);
    };
    box.createDiv({
      cls: "rion-git-auto-hint",
      text: autoSummary(this.plugin.settings)
    });
  }
  async commit() {
    const ok = await this.plugin.commitWithMessage(this.draft.trim());
    if (ok) {
      this.draft = "";
      this.restoreFocus = true;
      this.render(true);
    }
  }
  async commitAndPush() {
    const ok = await this.plugin.commitAndPush(this.draft.trim());
    if (ok) {
      this.draft = "";
      this.restoreFocus = true;
      this.render(true);
    }
  }
  renderChangesSection(el) {
    var _a;
    const status = this.plugin.lastStatus;
    const files = (_a = status == null ? void 0 : status.files) != null ? _a : [];
    const auto = this.plugin.settings.autoCommitMode !== "off";
    const body = this.createSection(
      el,
      "changes",
      "\u66F4\u6539",
      files.length > 0 ? String(files.length) : void 0,
      [
        {
          icon: auto ? "zap" : "zap-off",
          label: auto ? "\u81EA\u52A8\u63D0\u4EA4\uFF1A\u5F00\uFF08\u70B9\u51FB\u5173\u95ED\uFF09" : "\u81EA\u52A8\u63D0\u4EA4\uFF1A\u5173\uFF08\u70B9\u51FB\u5F00\u542F\uFF09",
          action: () => void this.plugin.toggleAutoCommit()
        },
        {
          icon: "refresh-cw",
          label: "\u5237\u65B0",
          action: () => void this.plugin.refresh()
        },
        {
          icon: "more-horizontal",
          label: "\u66F4\u591A\u64CD\u4F5C",
          action: (evt) => this.openMoreMenu(evt)
        }
      ]
    );
    if (!body) return;
    if (!status) {
      body.createDiv({ cls: "rion-git-empty", text: "\u6B63\u5728\u68C0\u6D4B\u4ED3\u5E93\u2026" });
      return;
    }
    if (files.length === 0) {
      body.createDiv({ cls: "rion-git-empty", text: "\u5DE5\u4F5C\u533A\u662F\u5E72\u51C0\u7684\u3002" });
      return;
    }
    for (const file of files.slice(0, MAX_ROWS2)) {
      this.renderFileRow(body, changeBadge(file), file.path, statusLabel(file), {
        onOpen: () => void this.plugin.showDiff(file),
        onCommit: () => void this.plugin.commitFile(file.path),
        onDiscard: () => void this.plugin.discardFile(file)
      });
    }
    if (files.length > MAX_ROWS2) {
      body.createDiv({
        cls: "rion-git-empty",
        text: `\u8FD8\u6709 ${files.length - MAX_ROWS2} \u4E2A\u6587\u4EF6\u672A\u663E\u793A\u2026`
      });
    }
  }
  renderHistorySection(el) {
    const log = this.plugin.lastLog;
    const body = this.createSection(
      el,
      "history",
      "\u5386\u53F2\u63D0\u4EA4",
      log.length > 0 ? String(log.length) : void 0,
      [
        { icon: "download", label: "\u62C9\u53D6", action: () => void this.plugin.pull() },
        { icon: "upload", label: "\u63A8\u9001", action: () => void this.plugin.push() },
        {
          icon: "activity",
          label: "\u5386\u53F2\u7EDF\u8BA1",
          action: () => void this.plugin.openStatsView()
        },
        {
          icon: "refresh-cw",
          label: "\u5237\u65B0\u5386\u53F2",
          action: () => void this.plugin.refresh()
        }
      ]
    );
    if (!body) return;
    if (log.length === 0) {
      body.createDiv({ cls: "rion-git-empty", text: "\u8FD8\u6CA1\u6709\u63D0\u4EA4\u8BB0\u5F55\u3002" });
      return;
    }
    for (const entry of log) this.renderCommitRow(body, entry);
  }
  renderCommitRow(parent, entry) {
    const expanded = this.expandedCommits.has(entry.hash);
    const item = parent.createDiv({ cls: "rion-git-commit-item" });
    const head = item.createDiv({ cls: "rion-git-commit-head" });
    head.createSpan({ cls: "rion-git-commit-dot" });
    const subject = head.createSpan({
      cls: "rion-git-commit-subject",
      text: entry.subject
    });
    subject.setAttribute("title", entry.subject);
    if (entry.refs.length > 0) {
      const refs = head.createSpan({ cls: "rion-git-refs" });
      for (const ref of entry.refs) {
        refs.createSpan({ cls: "rion-git-ref", text: ref });
      }
    }
    head.onclick = () => void this.toggleCommit(entry.hash);
    if (!expanded) return;
    const files = this.commitFiles.get(entry.hash);
    const filesEl = item.createDiv({ cls: "rion-git-commit-files" });
    if (!files) {
      filesEl.createDiv({ cls: "rion-git-empty", text: "\u8BFB\u53D6\u4E2D\u2026" });
      return;
    }
    if (files.length === 0) {
      filesEl.createDiv({ cls: "rion-git-empty", text: "\u6CA1\u6709\u6587\u4EF6\u53D8\u66F4\u3002" });
      return;
    }
    for (const file of files) {
      this.renderFileRow(filesEl, file.status, file.path, file.status, {
        onOpen: () => void this.plugin.showCommitDiff(entry.hash, file.path)
      });
    }
  }
  async toggleCommit(hash) {
    if (this.expandedCommits.has(hash)) {
      this.expandedCommits.delete(hash);
      this.render();
      return;
    }
    this.expandedCommits.add(hash);
    this.render();
    if (this.commitFiles.has(hash)) return;
    const files = await this.plugin.loadCommitFiles(hash);
    this.commitFiles.set(hash, files);
    this.render();
  }
  renderFileRow(parent, badge, path4, tooltip, actions) {
    const { name, dir } = splitPath(path4);
    const row = parent.createDiv({ cls: "rion-git-file-row" });
    row.setAttribute("title", tooltip);
    row.createSpan({ cls: `rion-git-file-badge mod-${badge}`, text: badge });
    row.createSpan({ cls: "rion-git-file-name", text: name });
    const end = row.createDiv({ cls: "rion-git-file-end" });
    if (dir) end.createSpan({ cls: "rion-git-file-dir", text: dir });
    if (!actions) return;
    row.addClass("is-clickable");
    row.onclick = () => actions.onOpen();
    if (!actions.onCommit && !actions.onDiscard) return;
    const buttons = end.createDiv({ cls: "rion-git-file-actions" });
    const addIcon = (icon, label, handler) => {
      if (!handler) return;
      const button = buttons.createEl("button", { cls: "clickable-icon" });
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
      (0, import_obsidian5.setIcon)(button, icon);
      button.onclick = (evt) => {
        evt.preventDefault();
        evt.stopPropagation();
        handler();
      };
    };
    addIcon("check", "\u63D0\u4EA4\u6B64\u6587\u4EF6", actions.onCommit);
    addIcon("rotate-ccw", "\u64A4\u9500\u4FEE\u6539", actions.onDiscard);
  }
  createSection(el, key, title, badge, actions) {
    const isCollapsed = this.collapsed.has(key);
    const section = el.createDiv({ cls: "rion-git-section" });
    const header = section.createDiv({ cls: "rion-git-section-header" });
    (0, import_obsidian5.setIcon)(
      header.createSpan({ cls: "rion-git-chevron" }),
      isCollapsed ? "chevron-right" : "chevron-down"
    );
    header.createSpan({ cls: "rion-git-section-title", text: title });
    if (badge !== void 0) {
      header.createSpan({ cls: "rion-git-badge", text: badge });
    }
    const actionsEl = header.createDiv({ cls: "rion-git-section-actions" });
    for (const action of actions) {
      const button = actionsEl.createEl("button", { cls: "clickable-icon" });
      button.setAttribute("aria-label", action.label);
      button.setAttribute("title", action.label);
      (0, import_obsidian5.setIcon)(button, action.icon);
      button.onclick = (evt) => {
        evt.preventDefault();
        evt.stopPropagation();
        action.action(evt);
      };
    }
    header.onclick = () => {
      if (isCollapsed) this.collapsed.delete(key);
      else this.collapsed.add(key);
      this.render();
    };
    return isCollapsed ? null : section.createDiv({ cls: "rion-git-section-body" });
  }
  openMoreMenu(evt) {
    const menu = new import_obsidian5.Menu();
    menu.addItem(
      (item) => item.setTitle("\u63D0\u4EA4\u5168\u90E8").setIcon("check").onClick(() => void this.commit())
    );
    menu.addItem(
      (item) => item.setTitle("\u63D0\u4EA4\u5E76\u63A8\u9001").setIcon("upload").onClick(() => void this.commitAndPush())
    );
    menu.addSeparator();
    menu.addItem(
      (item) => item.setTitle("\u62C9\u53D6").setIcon("download").onClick(() => void this.plugin.pull())
    );
    menu.addItem(
      (item) => item.setTitle("\u63A8\u9001").setIcon("upload").onClick(() => void this.plugin.push())
    );
    menu.addSeparator();
    menu.addItem(
      (item) => item.setTitle("\u521D\u59CB\u5316\u4ED3\u5E93").setIcon("git-branch").onClick(() => void this.plugin.initRepo())
    );
    menu.addItem(
      (item) => item.setTitle("\u6E05\u7A7A\u63D0\u4EA4\u6D88\u606F").setIcon("eraser").onClick(() => {
        this.draft = "";
        this.render();
      })
    );
    menu.showAtMouseEvent(evt);
  }
};

// src/ui/statsView.ts
var import_obsidian6 = require("obsidian");
var VIEW_TYPE_RION_GIT_STATS = "rion-git-stats";
var WEEK_OPTIONS = [13, 26, 52];
var WEEKDAY_LABELS = { 0: "\u4E00", 2: "\u4E09", 4: "\u4E94", 6: "\u65E5" };
function svgEl(tag, attrs = {}) {
  const el = createSvg(tag);
  for (const [key, value] of Object.entries(attrs)) {
    el.setAttribute(key, String(value));
  }
  return el;
}
function niceMax(value, divisions = 4) {
  var _a;
  if (value <= 0) return divisions;
  const rough = value / divisions;
  const exponent = Math.floor(Math.log10(rough));
  const base = 10 ** exponent;
  const normalized = rough / base;
  const step = (_a = [1, 2, 2.5, 5, 10].find((candidate) => normalized <= candidate)) != null ? _a : 10;
  return step * base * divisions;
}
var StatsView = class extends import_obsidian6.ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.weeks = 26;
    this.renderToken = 0;
    this.resizeTimer = null;
  }
  getViewType() {
    return VIEW_TYPE_RION_GIT_STATS;
  }
  getDisplayText() {
    return "\u5386\u53F2\u7EDF\u8BA1";
  }
  getIcon() {
    return "activity";
  }
  getState() {
    return { weeks: this.weeks };
  }
  async setState(state, result) {
    const weeks = Number(state == null ? void 0 : state.weeks);
    if (WEEK_OPTIONS.includes(weeks)) this.weeks = weeks;
    await super.setState(state, result);
    await this.render();
  }
  async onOpen() {
    this.registerDomEvent(window, "resize", () => {
      if (this.resizeTimer !== null) window.clearTimeout(this.resizeTimer);
      this.resizeTimer = window.setTimeout(() => {
        this.resizeTimer = null;
        void this.render();
      }, 250);
    });
    await this.render();
  }
  async onClose() {
    this.contentEl.empty();
  }
  async render() {
    const token = ++this.renderToken;
    const el = this.contentEl;
    el.empty();
    el.addClass("rion-git-stats-view");
    this.renderHeader(el);
    const body = el.createDiv({ cls: "rion-git-stats-body" });
    body.createDiv({ cls: "rion-git-empty", text: "\u7EDF\u8BA1\u4E2D\u2026" });
    const commits = await this.plugin.loadHistoryStats();
    if (token !== this.renderToken) return;
    const today = todayString();
    const start = shiftDays(today, -(this.weeks * 7 - 1));
    const daily = aggregateDaily(commits, start, today);
    const totalCommits = daily.reduce((sum, day) => sum + day.commits, 0);
    const totalLines = daily.reduce((sum, day) => sum + day.lines, 0);
    const totalFiles = daily.reduce((sum, day) => sum + day.files, 0);
    body.empty();
    if (totalCommits === 0) {
      body.createDiv({
        cls: "rion-git-empty",
        text: "\u8FD9\u6BB5\u65F6\u95F4\u6CA1\u6709\u63D0\u4EA4\u8BB0\u5F55\u3002"
      });
      return;
    }
    body.createDiv({
      cls: "rion-git-stats-summary",
      text: `\u8FD1 ${this.weeks} \u5468\uFF1A${totalCommits} \u6B21\u63D0\u4EA4 \xB7 ${totalLines} \u884C\u6539\u52A8 \xB7 ${totalFiles} \u4E2A\u6587\u4EF6`
    });
    body.createDiv({ cls: "rion-git-stats-section", text: "\u63D0\u4EA4\u65E5\u5386" });
    const heatmap = body.createDiv({ cls: "rion-git-heatmap" });
    this.renderHeatmap(heatmap, daily);
    body.createDiv({ cls: "rion-git-stats-section", text: "\u6539\u52A8\u8D8B\u52BF\uFF08\u6309\u5468\uFF09" });
    const chart = body.createDiv({ cls: "rion-git-line-chart" });
    this.renderLineChart(chart, aggregateByWeek(daily));
  }
  renderHeader(el) {
    const header = el.createDiv({ cls: "rion-git-stats-header" });
    header.createSpan({ cls: "rion-git-stats-title", text: "\u5386\u53F2\u7EDF\u8BA1" });
    const select = header.createEl("select", { cls: "dropdown" });
    for (const weeks of WEEK_OPTIONS) {
      const option = select.createEl("option", { text: `\u8FD1 ${weeks} \u5468` });
      option.value = String(weeks);
      option.selected = weeks === this.weeks;
    }
    select.onchange = () => {
      this.weeks = Number(select.value);
      void this.render();
    };
    const refresh = header.createEl("button", { cls: "clickable-icon" });
    refresh.setAttribute("aria-label", "\u91CD\u65B0\u7EDF\u8BA1");
    refresh.setAttribute("title", "\u91CD\u65B0\u7EDF\u8BA1");
    (0, import_obsidian6.setIcon)(refresh, "refresh-cw");
    refresh.onclick = () => void this.render();
  }
  renderHeatmap(container, daily) {
    const first = daily[0];
    if (!first) return;
    const LEFT = 22;
    const TOP = 18;
    const GAP = 3;
    const firstWeekday = weekdayIndex(first.date);
    const columns = Math.ceil((firstWeekday + daily.length) / 7);
    const available = Math.max(320, container.clientWidth || 640);
    const CELL = Math.max(9, Math.min(26, Math.floor((available - LEFT - GAP) / columns) - GAP));
    const width = LEFT + columns * (CELL + GAP) + GAP;
    const height = TOP + 7 * (CELL + GAP);
    const svg = svgEl("svg", {
      viewBox: `0 0 ${width} ${height}`,
      width,
      height,
      class: "rion-git-heatmap-svg"
    });
    for (const [rowText, label] of Object.entries(WEEKDAY_LABELS)) {
      const row = Number(rowText);
      const text = svgEl("text", {
        x: 0,
        y: TOP + row * (CELL + GAP) + CELL - 1,
        class: "rion-git-heatmap-label"
      });
      text.textContent = label;
      svg.appendChild(text);
    }
    const maxCommits = Math.max(1, ...daily.map((day) => day.commits));
    let lastMonth = "";
    daily.forEach((day, index) => {
      const column = Math.floor((firstWeekday + index) / 7);
      const row = weekdayIndex(day.date);
      const x = LEFT + column * (CELL + GAP);
      const y = TOP + row * (CELL + GAP);
      const level = day.commits === 0 ? 0 : Math.min(4, Math.max(1, Math.ceil(day.commits / maxCommits * 4)));
      const rect = svgEl("rect", {
        x,
        y,
        width: CELL,
        height: CELL,
        rx: 2,
        class: `rion-git-heat-cell level-${level}`
      });
      const title = svgEl("title");
      title.textContent = `${day.date}\uFF1A${day.commits} \u6B21\u63D0\u4EA4\uFF0C${day.lines} \u884C\uFF0C${day.files} \u4E2A\u6587\u4EF6`;
      rect.appendChild(title);
      svg.appendChild(rect);
      const month = day.date.slice(0, 7);
      if (month !== lastMonth) {
        lastMonth = month;
        const label = svgEl("text", {
          x,
          y: TOP - 6,
          class: "rion-git-heatmap-month"
        });
        label.textContent = `${Number(day.date.slice(5, 7))}\u6708`;
        svg.appendChild(label);
      }
    });
    container.appendChild(svg);
    const legend = container.createDiv({ cls: "rion-git-heatmap-legend" });
    legend.createSpan({ text: "\u5C11" });
    for (let level = 0; level <= 4; level++) {
      legend.createSpan({ cls: `rion-git-heat-cell level-${level}` });
    }
    legend.createSpan({ text: "\u591A" });
  }
  renderLineChart(container, weeks) {
    if (weeks.length === 0) return;
    const W = 760;
    const H = 240;
    const padL = 52;
    const padR = 56;
    const padT = 16;
    const padB = 28;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;
    const maxLines = niceMax(Math.max(1, ...weeks.map((week) => week.lines)));
    const maxFiles = niceMax(Math.max(1, ...weeks.map((week) => week.files)));
    const svg = svgEl("svg", {
      viewBox: `0 0 ${W} ${H}`,
      class: "rion-git-line-svg"
    });
    const xAt = (index) => padL + (weeks.length <= 1 ? plotW / 2 : index / (weeks.length - 1) * plotW);
    const yLines = (value) => padT + plotH - value / maxLines * plotH;
    const yFiles = (value) => padT + plotH - value / maxFiles * plotH;
    for (let step = 0; step <= 4; step++) {
      const y = padT + plotH / 4 * step;
      svg.appendChild(
        svgEl("line", {
          x1: padL,
          y1: y,
          x2: padL + plotW,
          y2: y,
          class: "rion-git-grid-line"
        })
      );
      const leftLabel = svgEl("text", {
        x: padL - 8,
        y: y + 4,
        class: "rion-git-axis-label",
        "text-anchor": "end"
      });
      leftLabel.textContent = String(Math.round(maxLines - maxLines / 4 * step));
      svg.appendChild(leftLabel);
      const rightLabel = svgEl("text", {
        x: padL + plotW + 8,
        y: y + 4,
        class: "rion-git-axis-label",
        "text-anchor": "start"
      });
      rightLabel.textContent = String(Math.round(maxFiles - maxFiles / 4 * step));
      svg.appendChild(rightLabel);
    }
    const buildPath = (values, scale) => values.map(
      (value, index) => `${index === 0 ? "M" : "L"}${xAt(index).toFixed(1)},${scale(value).toFixed(1)}`
    ).join(" ");
    svg.appendChild(
      svgEl("path", {
        d: buildPath(
          weeks.map((week) => week.lines),
          yLines
        ),
        class: "rion-git-line-series series-lines"
      })
    );
    svg.appendChild(
      svgEl("path", {
        d: buildPath(
          weeks.map((week) => week.files),
          yFiles
        ),
        class: "rion-git-line-series series-files"
      })
    );
    const labelStep = Math.max(1, Math.ceil(weeks.length / 8));
    weeks.forEach((week, index) => {
      if (index % labelStep !== 0) return;
      const text = svgEl("text", {
        x: xAt(index),
        y: H - 8,
        class: "rion-git-axis-label",
        "text-anchor": "middle"
      });
      text.textContent = `${Number(week.weekStart.slice(5, 7))}/${Number(week.weekStart.slice(8, 10))}`;
      svg.appendChild(text);
    });
    container.appendChild(svg);
    const legend = container.createDiv({ cls: "rion-git-chart-legend" });
    legend.createSpan({ cls: "dot series-lines" });
    legend.createSpan({ text: "\u63D0\u4EA4\u884C\u6570\uFF08\u5DE6\u8F74\uFF09" });
    legend.createSpan({ cls: "dot series-files" });
    legend.createSpan({ text: "\u63D0\u4EA4\u6587\u4EF6\u6570\uFF08\u53F3\u8F74\uFF09" });
  }
};

// src/ui/statusBar.ts
var GitStatusBar = class {
  constructor(plugin) {
    this.el = plugin.addStatusBarItem();
    this.el.addClass("rion-git-status");
    this.render("Git \u2026", "Rion Git \u6B63\u5728\u68C0\u6D4B\u4ED3\u5E93\u2026");
    this.el.onClickEvent(() => void plugin.activateView());
  }
  busy(label) {
    this.render(`Git \u27F3 ${label}`, label);
  }
  update(status) {
    var _a;
    const branch = (_a = status.branch) != null ? _a : "\u65E0\u63D0\u4EA4";
    if (status.hasConflicts) {
      this.render("Git \u26A0 \u51B2\u7A81", `\u5206\u652F ${branch}\uFF1A\u5B58\u5728\u5408\u5E76\u51B2\u7A81`);
      return;
    }
    if (status.files.length === 0) {
      this.render("Git \u2713", `\u5206\u652F ${branch}\uFF1A\u5DE5\u4F5C\u533A\u5E72\u51C0`);
      return;
    }
    this.render(
      `Git \u2022 ${status.files.length}`,
      `\u5206\u652F ${branch}\uFF1A${status.files.length} \u4E2A\u6539\u52A8\uFF08\u70B9\u51FB\u6253\u5F00\u9762\u677F\uFF09`
    );
  }
  showError(text) {
    this.render("Git \u26A0", text);
  }
  render(label, tooltip) {
    this.el.setText(label);
    this.el.setAttribute("aria-label", tooltip);
    this.el.setAttribute("title", tooltip);
  }
};

// src/vaultWatcher.ts
var VaultWatcher = class {
  constructor(plugin) {
    this.plugin = plugin;
    this.timer = null;
  }
  register() {
    const vault = this.plugin.app.vault;
    const onChange = (path4) => {
      if (isNoisePath(path4, vault.configDir)) return;
      this.schedule();
    };
    this.plugin.registerEvent(vault.on("modify", (file) => onChange(file.path)));
    this.plugin.registerEvent(vault.on("create", (file) => onChange(file.path)));
    this.plugin.registerEvent(vault.on("delete", (file) => onChange(file.path)));
    this.plugin.registerEvent(
      vault.on("rename", (file, oldPath) => {
        onChange(file.path);
        onChange(oldPath);
      })
    );
  }
  dispose() {
    if (this.timer !== null) window.clearTimeout(this.timer);
    this.timer = null;
  }
  schedule() {
    if (this.timer !== null) window.clearTimeout(this.timer);
    this.timer = window.setTimeout(() => {
      this.timer = null;
      void this.plugin.refreshStatusOnly();
    }, 700);
  }
};
function isNoisePath(path4, configDir) {
  if (path4.startsWith(".git/") || path4 === ".git") return true;
  if (path4.startsWith(".trash/") || path4 === ".trash") return true;
  if (path4.startsWith(configDir + "/plugins/")) return true;
  if (path4 === configDir + "/workspace.json") return true;
  if (path4 === configDir + "/workspace-mobile.json") return true;
  return false;
}

// src/main.ts
var AUTO_RETRY_COOLDOWN_MS = 5 * 6e4;
var HISTORY_LIMIT = 30;
var STATUS_REFRESH_MS = 3e4;
var RionGitPlugin = class extends import_obsidian7.Plugin {
  constructor() {
    super(...arguments);
    this.settings = { ...DEFAULT_SETTINGS };
    /** 侧边栏与状态栏共用的最新快照。 */
    this.lastStatus = null;
    this.lastLog = [];
    this.lastError = null;
    this.queue = new GitQueue();
    this.cwd = "";
    this.statusBar = null;
    this.autoCommit = null;
    this.watcher = null;
    this.autoCooldownUntil = 0;
    this.lastActiveMode = "interval";
  }
  async onload() {
    await this.loadSettings();
    this.cwd = this.app.vault.adapter.getBasePath();
    this.registerView(VIEW_TYPE_RION_GIT, (leaf) => new RionGitView(leaf, this));
    this.registerView(
      VIEW_TYPE_RION_GIT_DIFF,
      (leaf) => new DiffView(leaf, this)
    );
    this.registerView(
      VIEW_TYPE_RION_GIT_STATS,
      (leaf) => new StatsView(leaf, this)
    );
    this.addSettingTab(new RionGitSettingTab(this.app, this));
    this.addRibbonIcon("git-branch", "Rion Git: \u6253\u5F00\u9762\u677F", () => {
      void this.activateView();
    });
    if (this.settings.showStatusBar) {
      this.statusBar = new GitStatusBar(this);
    }
    registerCommands(this);
    this.autoCommit = new AutoCommitManager(this);
    this.autoCommit.register();
    this.watcher = new VaultWatcher(this);
    this.watcher.register();
    this.registerInterval(
      window.setInterval(() => {
        if (this.app.workspace.getLeavesOfType(VIEW_TYPE_RION_GIT).length === 0) {
          return;
        }
        void this.refresh();
      }, STATUS_REFRESH_MS)
    );
    this.app.workspace.onLayoutReady(() => {
      void this.refresh();
      if (this.settings.autoOpenPanel) void this.ensurePanelVisible();
    });
  }
  onunload() {
    var _a, _b;
    (_a = this.autoCommit) == null ? void 0 : _a.dispose();
    (_b = this.watcher) == null ? void 0 : _b.dispose();
  }
  get ctx() {
    return { cwd: this.cwd, gitPath: this.settings.gitPath };
  }
  async loadSettings() {
    this.settings = normalizeSettings(await this.loadData());
    if (this.settings.autoCommitMode !== "off") {
      this.lastActiveMode = this.settings.autoCommitMode;
    }
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
  applyAutoSettings() {
    var _a;
    (_a = this.autoCommit) == null ? void 0 : _a.applySettings();
  }
  async toggleAutoCommit() {
    if (this.settings.autoCommitMode === "off") {
      this.settings.autoCommitMode = this.lastActiveMode;
    } else {
      this.lastActiveMode = this.settings.autoCommitMode;
      this.settings.autoCommitMode = "off";
    }
    await this.saveSettings();
    this.applyAutoSettings();
    this.refreshViews();
  }
  async activateView() {
    const { workspace } = this.app;
    const existing = workspace.getLeavesOfType(VIEW_TYPE_RION_GIT);
    const first = existing[0];
    if (first) {
      await workspace.revealLeaf(first);
      return;
    }
    const leaf = workspace.getRightLeaf(false);
    if (!leaf) return;
    await leaf.setViewState({ type: VIEW_TYPE_RION_GIT, active: true });
    await workspace.revealLeaf(leaf);
  }
  /** 布局恢复后调用：只有面板确实不存在时才创建，避免覆盖用户的侧边栏布局。 */
  async ensurePanelVisible() {
    if (this.app.workspace.getLeavesOfType(VIEW_TYPE_RION_GIT).length > 0) {
      return;
    }
    await this.activateView();
  }
  async refresh() {
    await this.queue.add(() => this.refreshInQueue());
  }
  async loadCommitFiles(hash) {
    return this.queue.add(() => readCommitFiles(this.ctx, hash));
  }
  async loadHistoryStats() {
    return this.queue.add(() => readCommitStats(this.ctx));
  }
  async openStatsView() {
    const existing = this.app.workspace.getLeavesOfType(VIEW_TYPE_RION_GIT_STATS);
    const first = existing[0];
    if (first) {
      await this.app.workspace.revealLeaf(first);
      return;
    }
    const leaf = this.app.workspace.getLeaf("tab");
    await leaf.setViewState({ type: VIEW_TYPE_RION_GIT_STATS, active: true });
    await this.app.workspace.revealLeaf(leaf);
  }
  async commitAll() {
    return this.commitWithMessage("");
  }
  async commitWithMessage(message) {
    const text = message.trim() || formatCommitMessage(this.settings.commitMessageTemplate);
    let ok = false;
    await this.queue.add(async () => {
      var _a;
      if (!await this.ensureRepo()) return;
      (_a = this.statusBar) == null ? void 0 : _a.busy("\u63D0\u4EA4\u4E2D\u2026");
      const result = await commitAll(this.ctx, text);
      this.notify(result);
      await this.refreshInQueue();
      ok = result.ok;
    });
    return ok;
  }
  async push() {
    let ok = false;
    await this.queue.add(async () => {
      var _a;
      if (!await this.ensureRepo()) return;
      (_a = this.statusBar) == null ? void 0 : _a.busy("\u63A8\u9001\u4E2D\u2026");
      const result = await push(this.ctx);
      this.notify(result);
      await this.refreshInQueue();
      ok = result.ok;
    });
    return ok;
  }
  async pull() {
    let ok = false;
    await this.queue.add(async () => {
      var _a;
      if (!await this.ensureRepo()) return;
      (_a = this.statusBar) == null ? void 0 : _a.busy("\u62C9\u53D6\u4E2D\u2026");
      const result = await pull(this.ctx);
      this.notify(result);
      await this.refreshInQueue();
      ok = result.ok;
    });
    return ok;
  }
  async commitAndPush(message = "") {
    let ok = false;
    await this.queue.add(async () => {
      var _a, _b, _c;
      if (!await this.ensureRepo()) return;
      (_a = this.statusBar) == null ? void 0 : _a.busy("\u63D0\u4EA4\u4E2D\u2026");
      const text = message.trim() || formatCommitMessage(this.settings.commitMessageTemplate);
      const commit = await commitAll(this.ctx, text);
      if (!commit.ok) {
        this.notify(commit);
        await this.refreshInQueue();
        return;
      }
      (_b = this.statusBar) == null ? void 0 : _b.busy("\u63A8\u9001\u4E2D\u2026");
      const pushed = await push(this.ctx);
      this.notify({
        ok: pushed.ok,
        message: pushed.ok ? `\u5DF2\u63D0\u4EA4 ${(_c = commit.count) != null ? _c : 0} \u4E2A\u6539\u52A8\u5E76\u63A8\u9001\u3002` : pushed.message
      });
      await this.refreshInQueue();
      ok = pushed.ok;
    });
    return ok;
  }
  async showChanges() {
    var _a;
    const status = await this.queue.add(async () => {
      if (!await this.ensureRepo()) return null;
      return readStatus(this.ctx);
    });
    if (!status) return;
    this.lastStatus = status;
    (_a = this.statusBar) == null ? void 0 : _a.update(status);
    this.refreshViews();
    new ChangesModal(this.app, this, status).open();
  }
  async showDiff(change) {
    await this.openDiffView({
      path: change.path,
      untracked: change.index === "?" && change.worktree === "?"
    });
  }
  async showCommitDiff(hash, filePath) {
    await this.openDiffView({ path: filePath, untracked: false, commit: hash });
  }
  async openDiffView(state) {
    const leaf = this.app.workspace.getLeaf("tab");
    await leaf.setViewState({
      type: VIEW_TYPE_RION_GIT_DIFF,
      active: true,
      state
    });
    await this.app.workspace.revealLeaf(leaf);
  }
  async loadDiff(filePath, untracked, commit = "") {
    let raw = "";
    let note;
    if (commit) {
      raw = await this.queue.add(
        () => readCommitFileDiff(this.ctx, commit, filePath)
      );
      if (!raw.trim()) note = "\u8BE5\u63D0\u4EA4\u6CA1\u6709\u6539\u52A8\u8FD9\u4E2A\u6587\u4EF6\u3002";
    } else if (untracked) {
      const result = await readUntrackedDiff(this.ctx, filePath);
      raw = result.text;
      note = result.note;
    } else {
      raw = await this.queue.add(() => readFileDiff(this.ctx, filePath));
      if (!raw.trim()) note = "\u6CA1\u6709\u53EF\u663E\u793A\u7684\u5DEE\u5F02\uFF08\u6587\u4EF6\u53EF\u80FD\u5DF2\u6062\u590D\u6216\u4E3A\u7A7A\uFF09\u3002";
    }
    const lines = parseDiff(raw);
    return { lines, stats: diffStats(lines), note };
  }
  findChange(filePath) {
    var _a;
    const found = (_a = this.lastStatus) == null ? void 0 : _a.files.find((file) => file.path === filePath);
    return found != null ? found : { path: filePath, index: "M", worktree: "M" };
  }
  /** 供 vault 事件使用：只刷新状态，不读历史、不提交。 */
  async refreshStatusOnly() {
    await this.queue.add(async () => {
      var _a, _b;
      const detection = await detectRepo(this.ctx);
      if (detection.kind !== "ok") {
        this.lastStatus = null;
        this.lastError = detection.detail;
        (_a = this.statusBar) == null ? void 0 : _a.showError(detection.detail);
        this.refreshViews();
        return;
      }
      this.lastError = null;
      this.lastStatus = await readStatus(this.ctx);
      (_b = this.statusBar) == null ? void 0 : _b.update(this.lastStatus);
      this.refreshViews();
      await this.maybeSmartCommit(this.lastStatus);
    });
  }
  async commitFile(filePath) {
    await this.queue.add(async () => {
      var _a;
      if (!await this.ensureRepo()) return;
      (_a = this.statusBar) == null ? void 0 : _a.busy("\u63D0\u4EA4\u4E2D\u2026");
      const result = await commitFile(
        this.ctx,
        filePath,
        formatCommitMessage(this.settings.commitMessageTemplate)
      );
      this.notify(result);
      await this.refreshInQueue();
    });
  }
  async discardFile(change) {
    const untracked = change.index === "?" && change.worktree === "?";
    const message = untracked ? `\u5C06\u5220\u9664\u672A\u8DDF\u8E2A\u6587\u4EF6\u300C${change.path}\u300D\uFF0C\u6B64\u64CD\u4F5C\u4E0D\u53EF\u6062\u590D\u3002` : `\u5C06\u4E22\u5F03\u300C${change.path}\u300D\u7684\u6240\u6709\u6539\u52A8\uFF0C\u6B64\u64CD\u4F5C\u4E0D\u53EF\u6062\u590D\u3002`;
    new ConfirmModal(this.app, message, () => {
      void this.runDiscard(change);
    }).open();
  }
  async runDiscard(change) {
    await this.queue.add(async () => {
      if (!await this.ensureRepo()) return;
      const result = await discardFile(this.ctx, change);
      this.notify(result);
      await this.refreshInQueue();
    });
  }
  async initRepo() {
    let ok = false;
    await this.queue.add(async () => {
      var _a;
      (_a = this.statusBar) == null ? void 0 : _a.busy("\u521D\u59CB\u5316\u2026");
      const result = await initRepo(this.ctx);
      if (result.ok) await this.ensureDefaultGitignore();
      this.notify(result);
      await this.refreshInQueue();
      ok = result.ok;
    });
    return ok;
  }
  /** 定时提交入口（只有 autoCommitMode === "interval" 时会被调度）。 */
  async runAutoCommit() {
    await this.queue.add(async () => {
      if (this.settings.autoCommitMode !== "interval") return;
      if (Date.now() < this.autoCooldownUntil) return;
      const detection = await detectRepo(this.ctx);
      if (detection.kind !== "ok") {
        this.lastStatus = null;
        this.lastError = detection.detail;
        this.refreshViews();
        return;
      }
      await this.commitSilently();
    });
  }
  /** 智能提交：改动文件数或改动行数达到阈值时触发，与定时模式互斥。 */
  async maybeSmartCommit(status) {
    const settings = this.settings;
    if (settings.autoCommitMode !== "smart") return;
    if (status.files.length === 0) return;
    if (Date.now() < this.autoCooldownUntil) return;
    if (settings.smartFileThreshold > 0 && status.files.length >= settings.smartFileThreshold) {
      await this.commitSilently();
      return;
    }
    if (settings.smartLineThreshold <= 0) return;
    const untracked = status.files.filter((file) => file.index === "?" && file.worktree === "?").map((file) => file.path);
    const lines = await countChangedLines(this.ctx, untracked);
    if (lines < settings.smartLineThreshold) return;
    await this.commitSilently();
  }
  async commitSilently() {
    var _a;
    const result = await commitAll(
      this.ctx,
      formatCommitMessage(this.settings.commitMessageTemplate)
    );
    if (!result.ok) {
      this.autoCooldownUntil = Date.now() + AUTO_RETRY_COOLDOWN_MS;
      new import_obsidian7.Notice(
        `Rion Git \u81EA\u52A8\u63D0\u4EA4\u5931\u8D25\uFF1A${result.message}\uFF085 \u5206\u949F\u5185\u4E0D\u518D\u91CD\u8BD5\uFF09`,
        8e3
      );
      await this.refreshInQueue();
      return;
    }
    if (((_a = result.count) != null ? _a : 0) > 0 && this.settings.autoPush) {
      const pushed = await push(this.ctx);
      if (!pushed.ok) {
        this.autoCooldownUntil = Date.now() + AUTO_RETRY_COOLDOWN_MS;
        new import_obsidian7.Notice(`Rion Git \u81EA\u52A8\u63A8\u9001\u5931\u8D25\uFF1A${pushed.message}`, 8e3);
      }
    }
    await this.refreshInQueue();
  }
  async refreshInQueue() {
    var _a, _b;
    const detection = await detectRepo(this.ctx);
    if (detection.kind !== "ok") {
      this.lastStatus = null;
      this.lastLog = [];
      this.lastError = detection.detail;
      (_a = this.statusBar) == null ? void 0 : _a.showError(detection.detail);
      this.refreshViews();
      return;
    }
    this.lastError = null;
    this.lastStatus = await readStatus(this.ctx);
    this.lastLog = await readLog(this.ctx, HISTORY_LIMIT);
    (_b = this.statusBar) == null ? void 0 : _b.update(this.lastStatus);
    this.refreshViews();
  }
  refreshViews() {
    for (const leaf of this.app.workspace.getLeavesOfType(VIEW_TYPE_RION_GIT)) {
      if (leaf.view instanceof RionGitView) leaf.view.render();
    }
  }
  async ensureRepo() {
    const detection = await detectRepo(this.ctx);
    if (detection.kind === "ok") return true;
    if (detection.kind === "no-repo") {
      new import_obsidian7.Notice(
        "\u5F53\u524D vault \u8FD8\u4E0D\u662F git \u4ED3\u5E93\u3002\u53EF\u6267\u884C\u547D\u4EE4\u300CRion Git: \u521D\u59CB\u5316\u4ED3\u5E93\u300D\u3002",
        8e3
      );
    } else {
      new import_obsidian7.Notice(detection.detail, 8e3);
    }
    return false;
  }
  notify(result) {
    new import_obsidian7.Notice(
      result.ok ? result.message : `Rion Git: ${result.message}`,
      result.ok ? 3e3 : 8e3
    );
  }
  async ensureDefaultGitignore() {
    const adapter = this.app.vault.adapter;
    if (await adapter.exists(".gitignore")) return;
    const configDir = this.app.vault.configDir;
    await adapter.write(
      ".gitignore",
      [
        `${configDir}/workspace.json`,
        `${configDir}/workspace-mobile.json`,
        ".trash/",
        ""
      ].join("\n")
    );
  }
};

/* nosourcemap */