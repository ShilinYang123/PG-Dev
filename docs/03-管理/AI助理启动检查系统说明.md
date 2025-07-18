# 🚀 AI助理启动检查系统

## 快速开始

### Windows用户（推荐）
双击运行：`ai_startup.bat`

### 命令行用户
```bash
python tools/ai_startup.py
```

## 📋 系统作用

这个启动检查系统确保AI助理在每次工作前都能：

✅ **自动加载**所有项目规范文档  
✅ **提取关键**约束条件和禁止行为  
✅ **检查监控**系统运行状态  
✅ **生成简报**包含工作指导  
✅ **记录历史**便于追溯检查  

## 🎯 解决的问题

> **问题**：怎么让AI助理在每次工作前都先知照项目规定？

> **解决方案**：自动化启动检查系统

- 🔄 **自动化**：无需手动查找和阅读文档
- 📚 **全面性**：一次性加载所有核心规范
- 🎯 **针对性**：提取关键约束和禁止行为
- 📊 **可视化**：生成清晰的启动简报
- 🔍 **监控性**：检查合规系统状态

## 📁 相关文件

```
s:/PG-Dev/
├── ai_startup.bat                           # Windows快速启动
├── tools/
│   ├── ai_startup.py                        # 快速启动脚本
│   └── ai_assistant_startup_check.py        # 完整检查系统
├── docs/03-管理/
│   └── AI助理启动检查使用指南.md              # 详细使用指南
└── logs/
    ├── ai_assistant_startup.log             # 启动历史日志
    └── startup_briefing_YYYYMMDD_HHMMSS.md  # 启动简报
```

## 🔧 使用方法

### 1. 每次工作前（必须）
```bash
# 方法一：双击批处理文件
ai_startup.bat

# 方法二：命令行
python tools/ai_startup.py
```

### 2. 查看详细指南
阅读：`docs/03-管理/AI助理启动检查使用指南.md`

### 3. 检查启动历史
查看：`logs/ai_assistant_startup.log`

## 📊 输出示例

```
🚀 AI助理启动检查开始
==================================================
📋 加载核心项目规范...
   ✅ 项目架构设计: 已加载
   ✅ 开发任务书: 已加载
   ✅ 技术方案: 已加载
   ✅ 规范与流程: 已加载
   ✅ AI助理行为约束规范: 已加载
   ✅ 项目配置: 已加载
🔍 提取关键约束条件...
🔍 检查监控系统状态...
   ✅ 合规性监控正在运行 (PID: 3504)
📄 启动简报已保存: logs/startup_briefing_20250712_143022.md

==================================================
# AI助理启动简报

**启动时间**: 2025-07-12 14:30:22
**项目根目录**: s:/PG-Dev

## 🎯 工作目标
作为本项目的技术负责人，您需要：
1. 严格遵守所有项目管理文档和规范
2. 确保每次操作都符合项目架构设计
3. 维护项目的完整性和一致性
4. 提供高质量的技术解决方案

## 📋 核心约束条件
1. 🚫 严禁违反禁止性行为清单中的任何规定
2. ✅ 每次操作前必须执行强制检查流程
3. 🔒 严格保护核心文档，禁止未经授权的修改
4. 📋 必须遵循标准工作准备流程
5. 🧹 严格遵守文件清理管理规定
6. ⚙️ 严格遵守项目配置中的技术规范

## 📚 已加载的核心文档
- ✅ 项目架构设计
- ✅ 开发任务书
- ✅ 技术方案
- ✅ 规范与流程
- ✅ AI助理行为约束规范
- ✅ 项目配置

## 🔧 必须使用的工具
- TaskManager: 任务分解和管理
- Memory: 重要内容记忆存储
- Context7: 技术文档查询
- Desktop-Commander: 终端命令执行
- 合规性检查工具: 确保操作合规

## ⚠️ 关键提醒
1. **每次工作前**: 必须检查项目规范
2. **每次操作前**: 必须执行前置检查
3. **每次工作后**: 必须进行自我检查
4. **文档命名**: 一律使用中文
5. **代码质量**: 必须通过flake8等工具检测

## 🚀 开始工作
现在您已经完成启动检查，可以开始按照项目规范进行工作。
请记住：您是高级软件专家和技术负责人，需要确保所有工作都符合最高标准。

==================================================

🎉 准备就绪，可以开始工作！
```

## 💡 最佳实践

1. **养成习惯**：每次开始工作前都运行启动检查
2. **仔细阅读**：认真查看生成的启动简报
3. **保持更新**：规范文档更新后及时重新检查
4. **配合监控**：确保合规性监控系统同时运行

---

**记住**：这个系统就像飞行员起飞前的安全检查清单，确保每次工作都在正确的轨道上！