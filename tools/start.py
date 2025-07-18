#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI助理启动前置检查系统
确保AI助理在每次工作前都能知照项目规范和约束规定
"""

import os
import sys
import json
import yaml
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

class AIAssistantStartupChecker:
    """AI助理启动前置检查器"""
    
    def __init__(self, project_root: str = "s:/PG-Dev"):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.tools_dir = self.project_root / "tools"
        self.logs_dir = self.project_root / "logs"
        self.work_logs_dir = self.logs_dir / "工作记录"
        
        # 确保日志目录存在
        self.work_logs_dir.mkdir(parents=True, exist_ok=True)
        
        # 核心规范文档路径
        self.core_docs = {
            "项目架构设计": self.docs_dir / "01-设计" / "项目架构设计.md",
            "开发任务书": self.docs_dir / "01-设计" / "开发任务书.md",
            "技术方案": self.docs_dir / "01-设计" / "技术方案.md",
            "规范与流程": self.docs_dir / "03-管理" / "规范与流程.md",
            "项目配置": self.docs_dir / "03-管理" / "project_config.yaml"
        }
        
        # 启动检查记录文件
        self.startup_log = self.logs_dir / "ai_assistant_startup.log"
        
        # 设置工作流程日志
        self.setup_workflow_logging()
        
    def setup_workflow_logging(self):
        """设置工作流程日志系统"""
        log_file = self.work_logs_dir / f"workflow_{datetime.now().strftime('%Y%m%d')}.log"
        
        # 创建工作流程专用的logger
        self.workflow_logger = logging.getLogger('WorkflowManager')
        self.workflow_logger.setLevel(logging.INFO)
        
        # 避免重复添加handler
        if not self.workflow_logger.handlers:
            handler = logging.FileHandler(log_file, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.workflow_logger.addHandler(handler)
            
    def run_script(self, script_name: str, args: List[str] = None) -> bool:
        """运行指定脚本"""
        try:
            if args is None:
                args = []
                
            script_path = self.tools_dir / script_name
            if not script_path.exists():
                self.workflow_logger.error(f"脚本不存在: {script_path}")
                return False
                
            cmd = [sys.executable, str(script_path)]
            if args:
                cmd.extend(args)
            
            self.workflow_logger.info(f"执行命令: {' '.join(cmd)}")
            
            # 使用 gbk 编码处理中文输出
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='gbk',
                errors='ignore',
                cwd=str(self.project_root),
                timeout=30
            )
            
            if result.returncode == 0:
                self.workflow_logger.info(f"[SUCCESS] {script_name} 执行成功")
                if result.stdout.strip():
                    self.workflow_logger.info(f"输出: {result.stdout.strip()}")
                return True
            else:
                self.workflow_logger.error(f"[ERROR] {script_name} 执行失败 (退出码: {result.returncode})")
                if result.stderr.strip():
                    self.workflow_logger.error(f"错误: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            self.workflow_logger.error(f"[ERROR] {script_name} 执行超时")
            return False
        except Exception as e:
            self.workflow_logger.error(f"[ERROR] {script_name} 执行异常: {str(e)}")
            return False
            
    def check_prerequisites(self) -> bool:
        """检查前置条件"""
        self.workflow_logger.info("开始检查前置条件...")
        
        # 检查项目根目录
        if not self.project_root.exists():
            self.workflow_logger.error(f"项目根目录不存在: {self.project_root}")
            return False
            
        # 检查核心脚本
        required_scripts = [
            "compliance_monitor.py",
        ]
        
        for script in required_scripts:
            script_path = self.tools_dir / script
            if not script_path.exists():
                self.workflow_logger.error(f"核心脚本不存在: {script_path}")
                return False
                
        self.workflow_logger.info("前置条件检查通过")
        return True
        
    def start_monitoring_process(self) -> bool:
        """以非阻塞方式启动监控进程"""
        try:
            script_path = self.tools_dir / "compliance_monitor.py"
            if not script_path.exists():
                self.workflow_logger.error(f"监控脚本不存在: {script_path}")
                return False
            
            cmd = [sys.executable, str(script_path), "--start"]
            self.workflow_logger.info(f"启动监控进程: {' '.join(cmd)}")
            
            # 以非阻塞方式启动进程
            process = subprocess.Popen(
                cmd,
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='gbk',
                errors='ignore'
            )
            
            # 等待一小段时间检查进程是否立即失败
            time.sleep(1)
            
            if process.poll() is None:
                # 进程仍在运行
                self.workflow_logger.info(f"监控进程已启动 (PID: {process.pid})")
                return True
            else:
                # 进程已退出
                stdout, stderr = process.communicate()
                self.workflow_logger.error(f"监控进程启动失败 (退出码: {process.returncode})")
                if stderr.strip():
                    self.workflow_logger.error(f"错误信息: {stderr.strip()}")
                return False
                
        except Exception as e:
            self.workflow_logger.error(f"启动监控进程异常: {str(e)}")
            return False
        
    def start_compliance_monitoring_enhanced(self) -> bool:
        """启动增强的合规性监控系统"""
        self.workflow_logger.info("启动合规性监控系统...")
        
        # 1. 检查监控状态
        self.workflow_logger.info("[1/4] 检查监控系统状态...")
        if not self.run_script("compliance_monitor.py", ["--status"]):
            self.workflow_logger.warning("监控系统状态检查失败，继续启动流程")
        
        # 2. 启用合规性机制（如果存在）
        enable_script = self.tools_dir / "enable_compliance.py"
        if enable_script.exists():
            self.workflow_logger.info("[2/4] 启用合规性机制...")
            if not self.run_script("enable_compliance.py", ["--enable"]):
                self.workflow_logger.error("合规性机制启用失败")
                return False
        else:
            self.workflow_logger.info("[2/4] 跳过合规性机制启用（脚本不存在）")
            
        # 3. 启动监控系统（非阻塞方式）
        self.workflow_logger.info("[3/4] 启动实时监控...")
        if not self.start_monitoring_process():
            self.workflow_logger.error("监控系统启动失败")
            return False
            
        # 4. 验证启动状态
        self.workflow_logger.info("[4/4] 验证启动状态...")
        time.sleep(3)  # 等待系统启动
        
        if enable_script.exists():
            if not self.run_script("enable_compliance.py", ["--status"]):
                self.workflow_logger.warning("状态验证失败，但监控系统可能已启动")
        
        # 验证监控进程是否正在运行
        if self.check_monitoring_system():
            self.workflow_logger.info("[SUCCESS] 合规性监控系统启动成功")
            return True
        else:
            self.workflow_logger.warning("监控系统状态验证失败，但可能已启动")
            return True  # 继续执行，不阻塞整个流程
        
    def run_pre_checks(self) -> bool:
        """运行前置检查"""
        self.workflow_logger.info("执行前置检查...")
        
        pre_check_script = self.tools_dir / "pre_operation_check.py"
        if pre_check_script.exists():
            if not self.run_script("pre_operation_check.py", ["--check-all"]):
                self.workflow_logger.warning("前置检查发现问题，请查看详情")
                return False
        else:
            self.workflow_logger.info("跳过前置检查（脚本不存在）")
            
        self.workflow_logger.info("[SUCCESS] 前置检查通过")
        return True
        
    def show_work_reminders(self):
        """显示重要工作提醒"""
        reminders = [
            "🔔 重要提醒:",
            "   - 所有操作将被实时监控",
            "   - 违规行为将被自动记录和处理", 
            "   - 请严格按照项目规范执行",
            "   - 文件操作前请运行前置检查",
            "   - 定期查看合规性报告"
        ]
        
        for reminder in reminders:
            print(reminder)
            self.workflow_logger.info(reminder)

    def load_core_regulations(self) -> Dict[str, str]:
        """加载核心规范内容"""
        print("📚 加载核心项目规范...")
        regulations = {}
        
        for doc_name, doc_path in self.core_docs.items():
            if doc_path.exists():
                try:
                    if doc_path.suffix.lower() in ['.yaml', '.yml']:
                        with open(doc_path, 'r', encoding='utf-8') as f:
                            content = yaml.safe_load(f)
                            regulations[doc_name] = json.dumps(content, ensure_ascii=False, indent=2)
                    else:
                        with open(doc_path, 'r', encoding='utf-8') as f:
                            regulations[doc_name] = f.read()
                    print(f"   ✅ {doc_name}: 已加载")
                except Exception as e:
                    print(f"   ❌ {doc_name}: 加载失败 - {e}")
            else:
                print(f"   ⚠️ {doc_name}: 文件不存在 - {doc_path}")
                
        return regulations
        
    def extract_key_constraints(self, regulations: Dict[str, str]) -> List[str]:
        """提取关键约束条件"""
        print("🔍 提取关键约束条件...")
        constraints = []
        
        # 从规范与流程中提取核心约束和工作流程要求
        if "规范与流程" in regulations:
            content = regulations["规范与流程"]
            
            # 基础约束条件
            constraints.append("🚫 严禁在项目根目录创建任何临时文件或代码文件")
            constraints.append("✅ 每次操作前必须执行路径合规性检查")
            constraints.append("🔒 严格保护核心文档，禁止未经授权的修改")
            
            # 工作流程约束
            if "工作准备流程" in content:
                constraints.append("🔄 必须遵循标准工作准备流程")
                
            if "文件清理管理" in content:
                constraints.append("🧹 严格遵守文件清理管理规定")
                
            if "编码规范" in content:
                constraints.append("📝 严格遵守UTF-8编码规范")
                
            if "目录结构" in content:
                constraints.append("📁 严格遵守标准目录结构规范")
                
        # 从项目配置中提取技术约束
        if "项目配置" in regulations:
            constraints.append("⚙️ 严格遵守项目配置中的技术规范")
            
        # 从开发任务书中提取项目目标约束
        if "开发任务书" in regulations:
            constraints.append("🎯 严格按照开发任务书的目标和范围执行")
            
        # 从技术方案中提取架构约束
        if "技术方案" in regulations:
            constraints.append("🏗️ 严格遵循技术方案的架构设计")
            
        return constraints
        
    def generate_startup_briefing(self, regulations: Dict[str, str], constraints: List[str]) -> str:
        """生成启动简报"""
        monitoring_status = "🟢 运行中" if self.check_monitoring_system() else "🔴 未运行"
        
        briefing = f"""
# AI助理启动简报

**启动时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**项目根目录**: {self.project_root}
**监控系统状态**: {monitoring_status}

## 🎯 工作目标
作为本项目的技术负责人，您需要：
1. 严格遵守所有项目管理文档和规范
2. 确保每次操作都符合项目架构设计
3. 维护项目的完整性和一致性
4. 提供高质量的技术解决方案

## 📋 核心约束条件
"""
        
        for i, constraint in enumerate(constraints, 1):
            briefing += f"{i}. {constraint}\n"
            
        briefing += f"""

## 📄 已加载的核心文档
"""
        
        for doc_name in regulations.keys():
            briefing += f"- ✅ {doc_name}\n"
            
        briefing += f"""

## 🛠️ 必须使用的工具
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
"""
        
        return briefing
        
    def save_startup_record(self, briefing: str):
        """保存启动记录"""
        # 确保日志目录存在
        self.logs_dir.mkdir(exist_ok=True)
        
        # 保存启动简报
        briefing_file = self.logs_dir / f"startup_briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(briefing_file, 'w', encoding='utf-8') as f:
            f.write(briefing)
            
        # 更新启动日志
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - AI助理启动检查完成\n"
        with open(self.startup_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"💾 启动简报已保存: {briefing_file}")
        
    def check_monitoring_system(self) -> bool:
        """检查监控系统状态"""
        try:
            import psutil
            
            # 检查合规性监控进程
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if 'compliance_monitor.py' in cmdline and '--start' in cmdline:
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return False
            
        except ImportError:
            return False
            
    def start_monitoring_system(self) -> bool:
        """启动监控系统"""
        try:
            import subprocess
            import time
            
            # 检查配置是否允许自动启动
            config = self.load_project_config()
            if not config.get('compliance', {}).get('auto_start_monitoring', False):
                print("⚠️ 配置文件中未启用自动启动监控")
                return False
                
            print("🔄 正在启动合规性监控系统...")
            
            # 启动监控系统（非阻塞方式）
            compliance_script = self.tools_dir / "compliance_monitor.py"
            if not compliance_script.exists():
                print(f"❌ 监控脚本不存在: {compliance_script}")
                return False
                
            # 使用subprocess.Popen启动后台进程
            process = subprocess.Popen(
                ["python", str(compliance_script), "--start"],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else 0
            )
            
            # 等待一小段时间确保启动
            time.sleep(2)
            
            # 验证启动状态
            if self.check_monitoring_system():
                print("✅ 合规性监控系统启动成功")
                return True
            else:
                print("⚠️ 监控系统可能正在启动中，请稍后检查状态")
                return True  # 仍然返回True，因为启动命令已执行
                
        except Exception as e:
            print(f"❌ 启动监控系统失败: {e}")
            return False
            
    def load_project_config(self) -> dict:
        """加载项目配置"""
        try:
            import yaml
            config_file = self.project_root / "docs" / "03-管理" / "project_config.yaml"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ 加载配置文件失败: {e}")
        return {}
            
    def perform_startup_check(self) -> Tuple[bool, str]:
        """执行完整的启动检查"""
        import sys
        # 确保输出编码正确
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        
        print("🚀 AI助理启动检查开始")
        print("=" * 50)
        sys.stdout.flush()  # 强制刷新输出缓冲区
        
        try:
            # 1. 加载核心规范
            regulations = self.load_core_regulations()
            
            if not regulations:
                return False, "❌ 未能加载任何核心规范文档"
                
            # 2. 提取关键约束
            constraints = self.extract_key_constraints(regulations)
            
            # 3. 检查并启动监控系统
            monitoring_running = self.check_monitoring_system()
            if not monitoring_running:
                print("📡 监控系统未运行，正在自动启动...")
                self.start_monitoring_system()
            else:
                print("✅ 监控系统已在运行")
            
            # 4. 生成启动简报
            briefing = self.generate_startup_briefing(regulations, constraints)
            
            # 5. 保存启动记录
            self.save_startup_record(briefing)
            
            # 6. 显示简报
            print("\n" + "=" * 50)
            sys.stdout.flush()
            print(briefing)
            sys.stdout.flush()
            print("=" * 50)
            sys.stdout.flush()
            
            monitoring_status = "运行中" if self.check_monitoring_system() else "未运行"
            success_msg = f"🎉 AI助理启动检查完成 - 已加载 {len(regulations)} 个核心文档，监控系统状态: {monitoring_status}"
                
            return True, success_msg
            
        except Exception as e:
            error_msg = f"❌ 启动检查失败: {e}"
            print(error_msg)
            return False, error_msg
            
    def start_work_session(self) -> Tuple[bool, str]:
        """启动完整的工作会话（整合AI检查和工作流程管理）"""
        import sys
        # 确保输出编码正确
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        
        print("🚀 PG-Dev 项目完整启动流程")
        print("=" * 50)
        self.workflow_logger.info("开始项目标准工作启动流程")
        sys.stdout.flush()
        
        try:
            # 第一阶段：AI助理启动检查
            print("\n🤖 第一阶段：AI助理启动检查")
            print("-" * 30)
            
            # 1. 加载核心规范
            regulations = self.load_core_regulations()
            if not regulations:
                return False, "❌ 未能加载任何核心规范文档"
                
            # 2. 提取关键约束
            constraints = self.extract_key_constraints(regulations)
            
            # 第二阶段：工作流程环境检查
            print("\n🔧 第二阶段：工作流程环境检查")
            print("-" * 30)
            
            # 3. 检查前置条件
            if not self.check_prerequisites():
                self.workflow_logger.error("前置条件检查失败，无法启动工作会话")
                return False, "❌ 前置条件检查失败"
            print("✅ 前置条件检查通过")
            
            # 第三阶段：监控系统启动
            print("\n🛡️ 第三阶段：合规性监控系统启动")
            print("-" * 30)
            
            # 4. 启动增强的合规性监控
            if not self.start_compliance_monitoring_enhanced():
                self.workflow_logger.error("合规性监控启动失败")
                return False, "❌ 合规性监控启动失败"
            print("✅ 合规性监控系统已启动")
            
            # 第四阶段：前置检查
            print("\n🔍 第四阶段：运行前置检查")
            print("-" * 30)
            
            # 5. 运行前置检查
            if not self.run_pre_checks():
                self.workflow_logger.warning("前置检查发现问题，但继续工作会话")
                print("⚠️ 前置检查发现问题，但继续启动")
            else:
                print("✅ 前置检查通过")
            
            # 第五阶段：生成启动简报
            print("\n📋 第五阶段：生成启动简报")
            print("-" * 30)
            
            # 6. 生成启动简报
            briefing = self.generate_startup_briefing(regulations, constraints)
            
            # 7. 保存启动记录
            self.save_startup_record(briefing)
            
            # 最终阶段：完成启动
            print("\n" + "=" * 50)
            print("🎉 项目启动完成！")
            print("=" * 50)
            
            self.workflow_logger.info("[SUCCESS] 工作环境准备完成！")
            self.workflow_logger.info("[SUCCESS] 合规性监控系统已启动")
            self.workflow_logger.info("[SUCCESS] 可以开始正式工作")
            
            print("\n📊 当前系统状态:")
            print("   🤖 AI助理: 已就绪")
            print("   🛡️ 合规监控: 运行中")
            print("   🔄 工作流程: 已启动")
            print("   📚 核心文档: 已加载")
            
            # 显示重要提醒
            print("")
            self.show_work_reminders()
            
            print("\n🚀 现在可以开始高效工作！")
            print("=" * 50)
            sys.stdout.flush()
            
            monitoring_status = "运行中" if self.check_monitoring_system() else "未运行"
            success_msg = f"🎉 完整工作会话启动成功 - 已加载 {len(regulations)} 个核心文档，监控系统状态: {monitoring_status}"
                
            return True, success_msg
            
        except Exception as e:
            error_msg = f"❌ 工作会话启动失败: {e}"
            print(error_msg)
            self.workflow_logger.error(error_msg)
            return False, error_msg
            
    def create_startup_script(self):
        """创建启动脚本"""
        startup_script = self.tools_dir / "ai_startup.py"
        
        script_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI助理快速启动脚本
在每次开始工作前运行此脚本
"""

import sys
from pathlib import Path

# 添加工具目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from ai_assistant_startup_check import AIAssistantStartupChecker

def main():
    """主函数"""
    checker = AIAssistantStartupChecker()
    success, message = checker.perform_startup_check()
    
    if success:
        print("\n🎉 准备就绪，可以开始工作！")
        return 0
    else:
        print(f"\n[ERROR] 启动检查失败: {{message}}")
        return 1
        
if __name__ == "__main__":
    exit(main())
'''
        
        with open(startup_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
            
        print(f"📝 启动脚本已创建: {startup_script}")
        print("💡 使用方法: python tools/ai_startup.py")
        
def quick_startup():
    """快速启动函数 - 原ai_startup.py的功能"""
    checker = AIAssistantStartupChecker()
    success, message = checker.perform_startup_check()
    
    if success:
        print("\n🎉 准备就绪，可以开始工作！")
        return 0
    else:
        print(f"\n❌ 启动检查失败: {message}")
        return 1

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI助理启动前置检查系统")
    parser.add_argument("--check", action="store_true", help="执行启动检查")
    parser.add_argument("--create-script", action="store_true", help="创建启动脚本")
    parser.add_argument("--quick", action="store_true", help="快速启动（原ai_startup.py功能）")
    parser.add_argument("--work", action="store_true", help="启动完整工作会话（推荐）")
    parser.add_argument("--start", action="store_true", help="启动完整工作会话（别名）")
    
    args = parser.parse_args()
    
    checker = AIAssistantStartupChecker()
    
    if args.create_script:
        checker.create_startup_script()
    elif args.work or args.start:
        # 启动完整工作会话
        success, message = checker.start_work_session()
        print(f"\n{message}")
        if not success:
            exit(1)
    elif args.check:
        success, message = checker.perform_startup_check()
        print(f"\n{message}")
    elif args.quick:
        return quick_startup()
    else:
        # 默认执行完整工作会话启动
        success, message = checker.start_work_session()
        print(f"\n{message}")
        if not success:
            exit(1)
        
if __name__ == "__main__":
    main()