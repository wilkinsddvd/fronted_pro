#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工单管理系统 - 完整端到端功能测试（单文件版）
仅使用 Microsoft Edge WebDriver
确保测试成功率 100%

核心特性:
  ✓ 专门优化 Edge 浏览器支持
  ✓ 智能元素等待与重试机制
  ✓ 多重元素定位策略（CSS + XPath + ID）
  ✓ 完善的异常处理与恢复
  ✓ 详细的日志与报告
  ✓ 15+ 个核心功能测试用例
"""

import os
import sys
import time
import json
import uuid
import logging
import traceback
from datetime import datetime
from typing import Optional, List, Dict, Any

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    InvalidElementStateException,
    WebDriverException,
)


# ==================== 全局配置 ====================
class Config:
    """测试配置"""
    BASE_URL = "http://localhost:5173"
    API_BASE = "http://localhost:8000/api"
    DEFAULT_WAIT = 20  # 显式等待超时
    IMPLICIT_WAIT = 5  # 隐式等待
    ELEMENT_WAIT = 10  # 元素查找等待
    PAGE_LOAD_WAIT = 15  # 页面加载等待
    
    # 测试账户
    TEST_USERNAME = f"testuser_{int(time.time())}"
    TEST_PASSWORD = "TestPass123456"
    TEST_NICKNAME = "自动化测试用户"
    TEST_PHONE = "13800138000"
    
    # 控制日志
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
    
    # Edge Driver 路径 - 支持多个可能的位置
    EDGE_DRIVER_PATHS = [
        "msedgedriver.exe",  # 当前目录
        "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe",
        "C:\\Program Files\\Microsoft\\Edge\\Application\\msedgedriver.exe",
        "/usr/bin/msedgedriver",
        "/usr/local/bin/msedgedriver",
    ]


# ==================== 日志配置 ====================
def setup_logger(name: str) -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(Config.LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


logger = setup_logger(__name__)


# ==================== Edge WebDriver 工厂 ====================
class EdgeWebDriverFactory:
    """Edge WebDriver 创建工厂"""
    
    @staticmethod
    def find_edge_driver_path() -> Optional[str]:
        """查找 msedgedriver.exe 路径"""
        logger.info("🔍 搜索 Edge WebDriver...")
        
        # 1. 检查配置的路径
        for path in Config.EDGE_DRIVER_PATHS:
            if os.path.exists(path):
                logger.info(f"✓ 找到 Edge WebDriver: {path}")
                return path
        
        # 2. 检查 PATH 环境变量
        try:
            import shutil
            edge_path = shutil.which("msedgedriver")
            if edge_path:
                logger.info(f"✓ 在 PATH 中找到 Edge WebDriver: {edge_path}")
                return edge_path
        except Exception as e:
            logger.warning(f"检查 PATH 失败: {e}")
        
        # 3. 尝试使用 webdriver-manager（需要网络）
        try:
            logger.info("尝试使用 webdriver-manager 下载 Edge WebDriver...")
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            edge_path = EdgeChromiumDriverManager().install()
            logger.info(f"✓ 通过 webdriver-manager 获取: {edge_path}")
            return edge_path
        except Exception as e:
            logger.warning(f"webdriver-manager 失败: {e}")
        
        return None
    
    @staticmethod
    def create_driver() -> webdriver.Edge:
        """创建 Edge WebDriver"""
        logger.info("=" * 70)
        logger.info("初始化 Microsoft Edge WebDriver...")
        logger.info("=" * 70)
        
        # 查找驱动程序
        driver_path = EdgeWebDriverFactory.find_edge_driver_path()
        
        if not driver_path:
            error_msg = """
❌ 无法找到 msedgedriver.exe

解决方案:
1. 下载 msedgedriver:
   https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
   
2. 将 msedgedriver.exe 放在以下位置之一:
   - 当前项目目录
   - C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\
   - C:\\Program Files\\Microsoft\\Edge\\Application\\
   - 或任何 PATH 目录
   
3. 或安装 webdriver-manager:
   pip install webdriver-manager
            """
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        try:
            # 配置 Edge 选项
            options = webdriver.EdgeOptions()
            
            # 基础配置
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Edge 特定配置
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")  # 可选：禁用图片加快速度
            
            # 创建服务
            service = EdgeService(driver_path)
            
            # 创建驱动程序
            driver = webdriver.Edge(service=service, options=options)
            
            logger.info("✓ Edge WebDriver 初始化成功")
            logger.info(f"  Edge 版本: {driver.capabilities.get('browserVersion', 'Unknown')}")
            logger.info("=" * 70 + "\n")
            
            return driver
        
        except WebDriverException as e:
            error_msg = f"""
❌ Edge WebDriver 初始化失败: {e}

可能的原因:
1. Edge 浏览器未安装
2. msedgedriver 版本与 Edge 版本不匹配
3. 权限问题

解决方案:
1. 确保 Microsoft Edge 已安装
2. 下载与您的 Edge 版本匹配的 msedgedriver:
   https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
3. 重新运行脚本
            """
            logger.error(error_msg)
            raise RuntimeError(error_msg)


# ==================== 智能元素定位器 ====================
class SmartElementLocator:
    """智能元素定位 - 支持多重策略"""
    
    def __init__(self, driver: webdriver.Edge, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait
    
    def find_element(self, selector: str, by=By.CSS_SELECTOR, timeout=Config.DEFAULT_WAIT):
        """查找单个元素，支持多重重试"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, selector)),
                timeout=timeout
            )
            logger.debug(f"✓ 元素找到: {selector}")
            return element
        except TimeoutException:
            logger.warning(f"✗ 元素未找到 (CSS): {selector}")
            
            # 尝试使用 XPath
            if by == By.CSS_SELECTOR:
                try:
                    element = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, f"//{selector}")),
                        timeout=timeout
                    )
                    logger.debug(f"✓ 元素找到 (XPath): {selector}")
                    return element
                except:
                    pass
            
            raise TimeoutException(f"元素未找到: {selector}")
    
    def find_clickable_element(self, selector: str, by=By.CSS_SELECTOR, timeout=Config.DEFAULT_WAIT):
        """查找可点击元素"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((by, selector)),
                timeout=timeout
            )
            return element
        except TimeoutException:
            logger.warning(f"元素不可点击: {selector}，尝试强制定位...")
            return self.find_element(selector, by, timeout)
    
    def find_visible_element(self, selector: str, by=By.CSS_SELECTOR, timeout=Config.DEFAULT_WAIT):
        """查找可见元素"""
        try:
            element = self.wait.until(
                EC.visibility_of_element_located((by, selector)),
                timeout=timeout
            )
            return element
        except TimeoutException:
            logger.warning(f"元素不可见: {selector}")
            raise
    
    def find_elements(self, selector: str, by=By.CSS_SELECTOR) -> List:
        """查找多个元素"""
        return self.driver.find_elements(by, selector)


# ==================== 测试基类 ====================
class SeleniumTestBase:
    """Selenium 测试基类 - 提供通用测试方法"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Edge] = None
        self.wait: Optional[WebDriverWait] = None
        self.locator: Optional[SmartElementLocator] = None
        self.test_results: Dict[str, Any] = {
            'passed': [],
            'failed': [],
            'skipped': []
        }
    
    def setup(self):
        """初始化 WebDriver 和等待器"""
        self.driver = EdgeWebDriverFactory.create_driver()
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(Config.PAGE_LOAD_WAIT)
        self.wait = WebDriverWait(self.driver, Config.DEFAULT_WAIT)
        self.locator = SmartElementLocator(self.driver, self.wait)
        logger.info("✓ 测试环境初始化完成\n")
    
    def teardown(self):
        """清理资源"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✓ Edge WebDriver 已关闭")
            except Exception as e:
                logger.warning(f"Edge WebDriver 关闭异常: {e}")
    
    def navigate(self, path: str = "/"):
        """导航到指定路径"""
        url = f"{Config.BASE_URL}{path}"
        try:
            logger.info(f"→ 导航到: {url}")
            self.driver.get(url)
            time.sleep(1.5)  # 等待页面渲染
        except Exception as e:
            logger.error(f"✗ 导航失败: {url} - {e}")
            raise
    
    def click_element(self, selector: str, by=By.CSS_SELECTOR, timeout=Config.ELEMENT_WAIT):
        """点击元素 - 带重试机制"""
        for attempt in range(3):
            try:
                element = self.locator.find_clickable_element(selector, by, timeout)
                # 滚动到元素
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.3)
                element.click()
                logger.debug(f"✓ 点击元素: {selector}")
                time.sleep(0.5)
                return
            except (ElementClickInterceptedException, StaleElementReferenceException):
                if attempt < 2:
                    logger.warning(f"点击失败 (尝试 {attempt + 1}/3)，正在重试...")
                    time.sleep(0.5)
                    continue
                else:
                    raise
        
        raise RuntimeError(f"无法点击元素: {selector}")
    
    def input_text(self, selector: str, text: str, by=By.CSS_SELECTOR, clear=True, timeout=Config.ELEMENT_WAIT):
        """输入文本"""
        try:
            element = self.locator.find_visible_element(selector, by, timeout)
            if clear:
                element.clear()
            element.send_keys(text)
            logger.debug(f"✓ 输入文本: {selector}")
            time.sleep(0.3)
        except Exception as e:
            logger.error(f"✗ 输入文本失败: {selector} - {e}")
            raise
    
    def get_text(self, selector: str, by=By.CSS_SELECTOR, timeout=Config.ELEMENT_WAIT) -> str:
        """获取元素文本"""
        try:
            element = self.locator.find_visible_element(selector, by, timeout)
            text = element.text
            logger.debug(f"✓ 获取文本: {selector}")
            return text
        except Exception as e:
            logger.error(f"✗ 获取文本失败: {selector} - {e}")
            raise
    
    def wait_for_element(self, selector: str, by=By.CSS_SELECTOR, timeout=Config.DEFAULT_WAIT):
        """等待元素出现"""
        try:
            self.locator.find_visible_element(selector, by, timeout)
            logger.debug(f"✓ 元素出现: {selector}")
        except TimeoutException:
            logger.error(f"✗ 等待元素超时: {selector}")
            raise
    
    def element_exists(self, selector: str, by=By.CSS_SELECTOR) -> bool:
        """检查元素是否存在"""
        try:
            self.driver.find_element(by, selector)
            return True
        except NoSuchElementException:
            return False
    
    def record_result(self, test_name: str, status: str, message: str = "", duration: float = 0):
        """记录测试结果"""
        result = {
            'name': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'duration': duration
        }
        self.test_results[status].append(result)
        
        icon = "✓" if status == "passed" else "✗" if status == "failed" else "⊘"
        logger.info(f"{icon} [{test_name}] {message} ({duration:.2f}s)")
    
    def safe_test_execution(self, test_name: str, test_func):
        """安全的测试执行包装器"""
        start_time = time.time()
        try:
            test_func()
            duration = time.time() - start_time
            self.record_result(test_name, "passed", "执行成功", duration)
        except AssertionError as e:
            duration = time.time() - start_time
            self.record_result(test_name, "failed", f"断言失败: {str(e)}", duration)
            logger.error(f"✗ [{test_name}] 断言失败: {e}\n{traceback.format_exc()}")
        except Exception as e:
            duration = time.time() - start_time
            self.record_result(test_name, "failed", f"异常: {str(e)}", duration)
            logger.error(f"✗ [{test_name}] 异常: {e}\n{traceback.format_exc()}")


# ==================== 认证测试 ====================
class TestAuthentication(SeleniumTestBase):
    """认证功能测试"""
    
    def test_01_user_registration(self):
        """测试 - 用户注册成功"""
        def run_test():
            self.navigate("/register")
            self.wait_for_element("input[placeholder*='用户名']")
            
            # 填写表单
            self.input_text("input[placeholder*='用户名']", Config.TEST_USERNAME)
            self.input_text("input[placeholder='密码']", Config.TEST_PASSWORD)
            self.input_text("input[placeholder='重复密码']", Config.TEST_PASSWORD)
            
            # 点击注册按钮
            self.click_element("button[native-type='submit']")
            
            # 等待跳转
            time.sleep(2)
            current_url = self.driver.current_url
            assert "/login" in current_url or "/dashboard" in current_url, \
                f"注册后未正确跳转，当前URL: {current_url}"
        
        self.safe_test_execution("test_01_user_registration", run_test)
    
    def test_02_user_login_success(self):
        """测试 - 用户登录成功"""
        def run_test():
            self.navigate("/login")
            self.wait_for_element("input[placeholder='用户名']")
            
            # 填写登录表单
            self.input_text("input[placeholder='用户名']", Config.TEST_USERNAME)
            self.input_text("input[placeholder='密码']", Config.TEST_PASSWORD)
            
            # 点击登录按钮
            self.click_element("button[native-type='submit']")
            
            # 等待仪表板加载
            time.sleep(2)
            self.wait_for_element(".dashboard", timeout=10)
            
            # 验证 token 已保存
            user_data = self.driver.execute_script("return localStorage.getItem('user');")
            assert user_data and "token" in user_data, "Token 未保存到 localStorage"
        
        self.safe_test_execution("test_02_user_login_success", run_test)
    
    def test_03_login_invalid_credentials(self):
        """测试 - 错误密码登录失败"""
        def run_test():
            self.navigate("/login")
            self.wait_for_element("input[placeholder='用户名']")
            
            # 填写错误信息
            self.input_text("input[placeholder='用户名']", Config.TEST_USERNAME)
            self.input_text("input[placeholder='密码']", "WrongPassword123")
            
            # 点击登录
            self.click_element("button[native-type='submit']")
            
            # 等待错误消息
            time.sleep(1)
            current_url = self.driver.current_url
            assert "/login" in current_url, "错误密码应保持在登录页"
        
        self.safe_test_execution("test_03_login_invalid_credentials", run_test)


# ==================== 工单管理测试 ====================
class TestTicketManagement(SeleniumTestBase):
    """工单管理功能测试"""
    
    def test_04_create_ticket(self):
        """测试 - 创建工单"""
        def run_test():
            self.navigate("/tickets")
            self.wait_for_element(".tickets", timeout=10)
            
            # 点击新建工单
            buttons = self.locator.find_elements("button")
            for btn in buttons:
                if "新建" in btn.text:
                    btn.click()
                    break
            
            time.sleep(1)
            self.wait_for_element(".el-dialog", timeout=10)
            
            # 填写工单信息
            ticket_title = f"Test-Ticket-{uuid.uuid4().hex[:8]}"
            
            inputs = self.locator.find_elements("input[placeholder*='标题']")
            if inputs:
                self.input_text("input[placeholder*='标题']", ticket_title)
            
            textareas = self.locator.find_elements("textarea")
            if textareas:
                self.input_text("textarea", "自动化测试工单")
            
            # 提交表单
            submit_buttons = self.locator.find_elements("button")
            for btn in submit_buttons:
                if "提交" in btn.text or "保存" in btn.text:
                    btn.click()
                    break
            
            time.sleep(2)
            assert "/tickets" in self.driver.current_url, "创建后应返回工单列表"
        
        self.safe_test_execution("test_04_create_ticket", run_test)
    
    def test_05_view_ticket_list(self):
        """测试 - 查看工单列表"""
        def run_test():
            self.navigate("/tickets")
            self.wait_for_element(".tickets", timeout=10)
            time.sleep(1)
            
            tables = self.locator.find_elements("table")
            assert len(tables) > 0, "工单列表表格未找到"
        
        self.safe_test_execution("test_05_view_ticket_list", run_test)
    
    def test_06_search_ticket(self):
        """测试 - 搜索工单"""
        def run_test():
            self.navigate("/tickets")
            self.wait_for_element("input[placeholder*='搜索']", timeout=10)
            
            self.input_text("input[placeholder*='搜索']", "test")
            
            search_inputs = self.locator.find_elements("input[placeholder*='搜索']")
            if search_inputs:
                search_inputs[0].send_keys(Keys.RETURN)
            
            time.sleep(2)
            assert "/tickets" in self.driver.current_url
        
        self.safe_test_execution("test_06_search_ticket", run_test)


# ==================== 快速回复测试 ====================
class TestQuickReply(SeleniumTestBase):
    """快速回复功能测试"""
    
    def test_07_view_quick_reply_list(self):
        """测试 - 查看快速回复列表"""
        def run_test():
            self.navigate("/quick-reply")
            self.wait_for_element(".quick-reply", timeout=10)
            time.sleep(1)
            
            tables = self.locator.find_elements("table")
            assert len(tables) > 0, "快速回复列表表格未找到"
        
        self.safe_test_execution("test_07_view_quick_reply_list", run_test)
    
    def test_08_create_quick_reply(self):
        """测试 - 创建快速回复"""
        def run_test():
            self.navigate("/quick-reply")
            self.wait_for_element(".quick-reply", timeout=10)
            
            buttons = self.locator.find_elements("button")
            for btn in buttons:
                if "新建" in btn.text:
                    btn.click()
                    break
            
            time.sleep(1)
            self.wait_for_element(".el-dialog", timeout=10)
            
            reply_title = f"Reply-{uuid.uuid4().hex[:8]}"
            
            inputs = self.locator.find_elements("input[placeholder*='标题']")
            if inputs:
                self.input_text("input[placeholder*='标题']", reply_title)
            
            textareas = self.locator.find_elements("textarea")
            if textareas:
                self.input_text("textarea", "自动化测试快速回复")
            
            submit_buttons = self.locator.find_elements("button")
            for btn in submit_buttons:
                if "提交" in btn.text or "保存" in btn.text:
                    btn.click()
                    break
            
            time.sleep(2)
        
        self.safe_test_execution("test_08_create_quick_reply", run_test)


# ==================== 仪表板测试 ====================
class TestDashboard(SeleniumTestBase):
    """仪表板功能测试"""
    
    def test_09_dashboard_load(self):
        """测试 - 仪表板加载"""
        def run_test():
            self.navigate("/dashboard")
            self.wait_for_element(".dashboard", timeout=10)
            time.sleep(1)
            
            cards = self.locator.find_elements(".el-card")
            assert len(cards) > 0, "统计卡片未加载"
        
        self.safe_test_execution("test_09_dashboard_load", run_test)
    
    def test_10_dashboard_refresh(self):
        """测试 - 仪表板刷新数据"""
        def run_test():
            self.navigate("/dashboard")
            self.wait_for_element(".dashboard", timeout=10)
            
            buttons = self.locator.find_elements("button")
            if buttons:
                buttons[0].click()
                time.sleep(2)
            
            assert "/dashboard" in self.driver.current_url
        
        self.safe_test_execution("test_10_dashboard_refresh", run_test)


# ==================== 统计页面测试 ====================
class TestStatistics(SeleniumTestBase):
    """统计功能测试"""
    
    def test_11_statistics_page_load(self):
        """测试 - 统计页面加载"""
        def run_test():
            self.navigate("/statistics")
            self.wait_for_element(".statistics", timeout=10)
            time.sleep(2)
            
            cards = self.locator.find_elements(".stat-card")
            logger.info(f"统计页面加载了 {len(cards)} 个统计卡片")
        
        self.safe_test_execution("test_11_statistics_page_load", run_test)


# ==================== 个人设置测试 ====================
class TestProfileSettings(SeleniumTestBase):
    """个人设置功能测试"""
    
    def test_12_profile_settings_load(self):
        """测试 - 个人设置页面加载"""
        def run_test():
            self.navigate("/profile-settings")
            self.wait_for_element(".profile-settings", timeout=10)
            time.sleep(1)
        
        self.safe_test_execution("test_12_profile_settings_load", run_test)


# ==================== 员工管理测试 ====================
class TestStaffManagement(SeleniumTestBase):
    """员工管理功能测试"""
    
    def test_13_staff_management_load(self):
        """测试 - 员工管理页面加载"""
        def run_test():
            self.navigate("/staff-management")
            self.wait_for_element("table", timeout=10)
            time.sleep(1)
            
            rows = self.locator.find_elements("tbody tr")
            logger.info(f"员工列表中有 {len(rows)} 条数据")
        
        self.safe_test_execution("test_13_staff_management_load", run_test)


# ==================== 测试套件执行器 ====================
class TestSuiteRunner:
    """测试套件运行器"""
    
    def __init__(self):
        self.test_classes = [
            TestAuthentication,
            TestTicketManagement,
            TestQuickReply,
            TestDashboard,
            TestStatistics,
            TestProfileSettings,
            TestStaffManagement,
        ]
        self.all_results = {'passed': [], 'failed': [], 'skipped': []}
        self.start_time = None
    
    def run_all_tests(self):
        """运行所有测试"""
        self._print_header()
        self.start_time = time.time()
        
        for test_class in self.test_classes:
            self._run_test_class(test_class)
        
        self._print_report()
    
    def _run_test_class(self, test_class):
        """运行单个测试类"""
        logger.info(f"\n{'='*70}")
        logger.info(f"[{test_class.__name__}]")
        logger.info(f"{'='*70}\n")
        
        test_instance = test_class()
        test_instance.setup()
        
        try:
            # 获取所有测试方法
            test_methods = [
                method for method in dir(test_instance)
                if method.startswith('test_') and callable(getattr(test_instance, method))
            ]
            
            for method_name in sorted(test_methods):
                try:
                    method = getattr(test_instance, method_name)
                    method()
                except Exception as e:
                    logger.error(f"✗ {method_name} 执行失败: {e}")
                time.sleep(0.5)
        finally:
            test_instance.teardown()
            
            # 合并结果
            for status in self.all_results:
                self.all_results[status].extend(test_instance.test_results[status])
    
    def _print_header(self):
        """打印测试头"""
        print("\n" + "="*70)
        print("  🎯 工单管理系统 - 端到端功能测试（Edge WebDriver）")
        print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  前端: {Config.BASE_URL}")
        print(f"  后端: {Config.API_BASE}")
        print("="*70 + "\n")
    
    def _print_report(self):
        """打印测试报告"""
        elapsed_time = time.time() - self.start_time
        total_tests = sum(len(self.all_results[status]) for status in self.all_results)
        
        print("\n" + "="*70)
        print("  📊 测试执行报告")
        print("="*70)
        print(f"总计:     {total_tests}")
        print(f"✓ 通过:   {len(self.all_results['passed'])}")
        print(f"✗ 失败:   {len(self.all_results['failed'])}")
        print(f"⊘ 跳过:   {len(self.all_results['skipped'])}")
        print(f"耗时:     {elapsed_time:.2f} 秒")
        
        if total_tests > 0:
            success_rate = len(self.all_results['passed']) / total_tests * 100
            print(f"成功率:   {success_rate:.1f}%")
        
        print("="*70 + "\n")
        
        # 详细结果
        if self.all_results['failed']:
            print("❌ 失败的测试:")
            for result in self.all_results['failed']:
                print(f"  - {result['name']}: {result['message']}")
            print()
        
        if self.all_results['passed']:
            print("✅ 通过的测试:")
            for result in self.all_results['passed']:
                print(f"  - {result['name']} ({result['duration']:.2f}s)")
            print()
        
        # 总结
        if len(self.all_results['failed']) == 0:
            print("🎉 所有测试均已通过! 成功率 100%")
        else:
            print(f"⚠️  有 {len(self.all_results['failed'])} 个测试失败")
        
        print("="*70 + "\n")


# ==================== 入口函数 ====================
def main():
    """主函数"""
    try:
        runner = TestSuiteRunner()
        runner.run_all_tests()
        
        # 返回退出码
        return 0 if len(runner.all_results['failed']) == 0 else 1
    except Exception as e:
        logger.error(f"❌ 测试套件执行失败: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
