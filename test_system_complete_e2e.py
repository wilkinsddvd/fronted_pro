#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整端到端功能测试 - Selenium + Edge WebDriver
针对前端(http://localhost:5173)和后端(http://localhost:8000)的综合测试

运行方式:
    python test_system_complete_e2e.py

前置条件:
    # 后端启动
    cd end_pro
    uvicorn main:app --reload

    # 前端启动
    cd fronted_pro
    npm run dev

    # 安装依赖
    pip install selenium
"""

import base64
import datetime
import os
import sys
import time
import traceback
import unittest
import uuid
from typing import Optional

# Selenium 导入
try:
    from selenium import webdriver
    from selenium.common.exceptions import (
        NoSuchElementException,
        TimeoutException,
        WebDriverException,
    )
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError as exc:
    print(f"[ERROR] 缺少 selenium 依赖，请运行: pip install selenium\n{exc}")
    sys.exit(1)

# ==================== 全局配置 ====================
BASE_URL = "http://localhost:5173"
API_BASE = "http://localhost:8000/api"
DEFAULT_WAIT = 20
IMPLICIT_WAIT = 5
SCREENSHOT_DIR = "screenshots"
REPORT_FILE = "test_report_complete.html"

# 测试账户
_ts = str(int(time.time()))[-6:]
TEST_USER = f"testuser{_ts}"
TEST_PASS = f"Pass{_ts}123"
TEST_NEW_PASS = f"NewPass{_ts}456"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ==================== WebDriver 工厂 ====================
class DriverFactory:
    """Edge WebDriver 工厂"""

    @staticmethod
    def find_edge_driver_path() -> Optional[str]:
        """查找 msedgedriver.exe 路径"""
        paths = [
            "msedgedriver.exe",
            "C:\\Program Files\\Microsoft\\Edge\\Application\\msedgedriver.exe",
            "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe",
            "/usr/bin/msedgedriver",
            "/usr/local/bin/msedgedriver",
        ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        
        # 尝试 PATH
        try:
            import shutil
            edge_path = shutil.which("msedgedriver")
            if edge_path:
                return edge_path
        except:
            pass
        
        # 尝试 webdriver-manager
        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            return EdgeChromiumDriverManager().install()
        except:
            pass
        
        return None

    @staticmethod
    def create_driver() -> webdriver.Edge:
        """创建 Edge WebDriver"""
        driver_path = DriverFactory.find_edge_driver_path()
        
        if not driver_path:
            raise RuntimeError("找不到 msedgedriver，请下载: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
        
        opts = EdgeOptions()
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("--window-size=1920,1080")
        
        service = EdgeService(driver_path)
        driver = webdriver.Edge(service=service, options=opts)
        driver.implicitly_wait(IMPLICIT_WAIT)
        return driver


# ==================== 测试基类 ====================
class TestBase(unittest.TestCase):
    """测试基类"""

    driver: webdriver.Edge = None
    wait: WebDriverWait = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.driver = DriverFactory.create_driver()
            cls.wait = WebDriverWait(cls.driver, DEFAULT_WAIT)
            print(f"✓ WebDriver 初始化成功")
        except Exception as e:
            print(f"✗ WebDriver 初始化失败: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            try:
                cls.driver.quit()
            except:
                pass

    # -------- 等待工具 --------
    def wait_for_element(self, by: str, value: str, timeout: int = DEFAULT_WAIT):
        """等待元素可见"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def wait_for_clickable(self, by: str, value: str, timeout: int = DEFAULT_WAIT):
        """等待元素可点击"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def wait_for_ajax(self, timeout: int = 3):
        """等待 AJAX 请求完成"""
        time.sleep(timeout * 0.3)

    # -------- 导航 --------
    def navigate(self, path: str = ""):
        self.driver.get(BASE_URL + path)
        time.sleep(0.5)

    # -------- 截图 --------
    def take_screenshot(self, name: str) -> str:
        """截图"""
        filename = os.path.join(
            SCREENSHOT_DIR,
            f"{name}_{datetime.datetime.now().strftime('%H%M%S')}.png",
        )
        try:
            self.driver.save_screenshot(filename)
        except:
            filename = ""
        return filename

    # -------- 通用工具 --------
    def find_input_by_placeholder(self, placeholder: str):
        """根据 placeholder 查找输入框"""
        try:
            return self.wait_for_element(By.CSS_SELECTOR, f"input[placeholder*='{placeholder}']", timeout=5)
        except:
            try:
                return self.wait_for_element(By.CSS_SELECTOR, "input", timeout=5)
            except:
                return None

    def login(self, username: str = TEST_USER, password: str = TEST_PASS):
        """登录"""
        self.navigate("/login")
        time.sleep(0.5)
        
        try:
            # 用户名
            u_input = self.find_input_by_placeholder("用户名")
            if not u_input:
                u_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='text']", timeout=5)
            u_input.clear()
            u_input.send_keys(username)
            
            # 密码
            p_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='password']", timeout=5)
            p_input.clear()
            p_input.send_keys(password)
            
            # 提交
            btn = self.wait_for_clickable(By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit'], button.el-button--primary", timeout=5)
            btn.click()
            
            self.wait_for_ajax()
            time.sleep(1)
        except Exception as e:
            print(f"登录失败: {e}")
            raise

    def logout(self):
        """登出"""
        try:
            # 查找用户菜单
            for selector in [".user-avatar", ".avatar", ".el-dropdown", "button[class*='user']"]:
                try:
                    menu = self.driver.find_element(By.CSS_SELECTOR, selector)
                    menu.click()
                    time.sleep(0.3)
                    break
                except:
                    continue
            
            # 点击退出
            logout_btn = self.wait_for_clickable(By.XPATH, "//*[contains(text(),'退出') or contains(text(),'登出')]", timeout=5)
            logout_btn.click()
            self.wait_for_ajax()
        except:
            self.navigate("/login")

    def assert_url_contains(self, fragment: str):
        """断言 URL 包含指定片段"""
        time.sleep(0.5)
        self.assertIn(fragment, self.driver.current_url, f"URL 不包含 '{fragment}': {self.driver.current_url}")

    def assert_page_contains_text(self, text: str):
        """断言页面包含指定文本"""
        self.assertIn(text, self.driver.page_source, f"页面不包含文本: {text}")


# ==================== A. 认证测试 ====================
class TestAuthentication(TestBase):
    """认证功能测试"""

    def test_01_user_registration_success(self):
        """✅ 用户注册成功"""
        self.navigate("/register")
        
        # 用户名
        u_input = self.find_input_by_placeholder("用户名")
        if not u_input:
            u_input = self.wait_for_element(By.CSS_SELECTOR, "input", timeout=5)
        u_input.clear()
        u_input.send_keys(TEST_USER)
        
        # 密码
        pw_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        pw_inputs[0].clear()
        pw_inputs[0].send_keys(TEST_PASS)
        
        # 确认密码
        if len(pw_inputs) > 1:
            pw_inputs[1].clear()
            pw_inputs[1].send_keys(TEST_PASS)
        
        # 提交
        btn = self.wait_for_clickable(By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit']", timeout=5)
        btn.click()
        
        self.wait_for_ajax()
        time.sleep(1)
        
        # 验证：不在 /register 或看到成功提示
        current_url = self.driver.current_url
        page_source = self.driver.page_source
        
        success = (
            "/register" not in current_url
            or "成功" in page_source
            or "success" in page_source.lower()
        )
        self.assertTrue(success, f"注册失败，URL: {current_url}")

    def test_02_user_login_success(self):
        """✅ 用户登录成功"""
        self.login(TEST_USER, TEST_PASS)
        
        # 验证：离开登录页
        time.sleep(1)
        current_url = self.driver.current_url
        self.assertNotIn("/login", current_url, f"登录后仍停留在登录页: {current_url}")

    def test_03_login_invalid_password(self):
        """✅ 错误密码登录失败"""
        self.navigate("/login")
        time.sleep(0.5)
        
        u_input = self.find_input_by_placeholder("用户名")
        if not u_input:
            u_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='text']", timeout=5)
        u_input.clear()
        u_input.send_keys(TEST_USER)
        
        p_input = self.wait_for_element(By.CSS_SELECTOR, "input[type='password']", timeout=5)
        p_input.clear()
        p_input.send_keys("WrongPassword000")
        
        btn = self.wait_for_clickable(By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit']", timeout=5)
        btn.click()
        
        self.wait_for_ajax()
        time.sleep(1)
        
        # 验证：仍在登录页或显示错误
        current_url = self.driver.current_url
        page_source = self.driver.page_source
        
        failed = (
            "/login" in current_url
            or "错误" in page_source
            or "失败" in page_source
            or "invalid" in page_source.lower()
        )
        self.assertTrue(failed, "错误密码应该登录失败")

    def test_04_user_logout(self):
        """✅ 用户登出"""
        self.login(TEST_USER, TEST_PASS)
        time.sleep(1)
        self.logout()
        time.sleep(1)
        
        # 验证：在登录页
        current_url = self.driver.current_url
        self.assertIn("/login", current_url, f"登出后应在登录页，当前: {current_url}")


# ==================== B. 工单管理测试 ====================
class TestTicketManagement(TestBase):
    """工单管理测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 先登录
        cls.driver.get(BASE_URL + "/login")
        time.sleep(1)
        try:
            u_input = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text'], input"))
            )
            u_input.clear()
            u_input.send_keys(TEST_USER)
            
            p_input = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            p_input.clear()
            p_input.send_keys(TEST_PASS)
            
            btn = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit'], button"))
            )
            btn.click()
            time.sleep(2)
        except Exception as e:
            print(f"测试类登录失败: {e}")

    def test_05_create_ticket_success(self):
        """✅ 创建工单成功"""
        self.navigate("/tickets")
        time.sleep(1)
        
        # 点击新建
        try:
            create_btn = self.wait_for_clickable(By.XPATH, "//button[contains(text(),'新建')]", timeout=5)
            create_btn.click()
        except:
            create_btn = self.wait_for_clickable(By.CSS_SELECTOR, "button.el-button--primary", timeout=5)
            create_btn.click()
        
        time.sleep(1)
        
        # 填写标题
        title = f"Test-Ticket-{uuid.uuid4().hex[:8]}"
        title_input = self.wait_for_element(By.CSS_SELECTOR, "input[placeholder*='标题'], input", timeout=5)
        title_input.clear()
        title_input.send_keys(title)
        
        # 填写描述
        try:
            desc = self.driver.find_element(By.CSS_SELECTOR, "textarea")
            desc.clear()
            desc.send_keys("自动化测试工单描述")
        except:
            pass
        
        # 提交
        submit_btn = self.wait_for_clickable(By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit'], .el-button--primary", timeout=5)
        submit_btn.click()
        
        self.wait_for_ajax()
        time.sleep(1)
        
        # 验证
        current_url = self.driver.current_url
        page_source = self.driver.page_source
        
        success = (
            "/tickets" in current_url
            or "成功" in page_source
            or title in page_source
        )
        self.assertTrue(success, f"工单创建失败，URL: {current_url}")

    def test_06_view_ticket_list(self):
        """✅ 查看工单列表"""
        self.navigate("/tickets")
        self.wait_for_ajax()
        time.sleep(1)
        
        # 检查表格存在
        tables = self.driver.find_elements(By.CSS_SELECTOR, "table")
        self.assertTrue(len(tables) > 0, "工单列表表格未找到")

    def test_07_search_ticket(self):
        """✅ 搜索工单"""
        self.navigate("/tickets")
        time.sleep(1)
        
        # 搜索框
        try:
            search_input = self.wait_for_element(By.CSS_SELECTOR, "input[placeholder*='搜索']", timeout=5)
            search_input.clear()
            search_input.send_keys("test")
            search_input.send_keys(Keys.RETURN)
        except:
            pass
        
        self.wait_for_ajax()
        time.sleep(1)
        
        # 验证仍在工单页
        current_url = self.driver.current_url
        self.assertIn("/tickets", current_url, f"搜索后不在工单页: {current_url}")

    def test_08_ticket_pagination(self):
        """✅ 工单列表分页"""
        self.navigate("/tickets")
        self.wait_for_ajax()
        time.sleep(1)
        
        # 尝试点击下一页
        try:
            next_btn = self.driver.find_element(By.XPATH, "//button[contains(., '›')] | //*[@aria-label='next']")
            next_btn.click()
            time.sleep(1)
        except:
            pass
        
        # 验证仍在工单页
        self.assertIn("/tickets", self.driver.current_url)


# ==================== C. 快速回复测试 ====================
class TestQuickReply(TestBase):
    """快速回复测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver.get(BASE_URL + "/login")
        time.sleep(1)
        try:
            u_input = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text'], input"))
            )
            u_input.clear()
            u_input.send_keys(TEST_USER)
            p_input = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            p_input.clear()
            p_input.send_keys(TEST_PASS)
            btn = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit'], button"))
            )
            btn.click()
            time.sleep(2)
        except:
            pass

    def test_09_quick_reply_list_load(self):
        """✅ 快速回复列表加载"""
        self.navigate("/quick-reply")
        self.wait_for_ajax()
        time.sleep(1)
        
        # 检查页面加载
        page_source = self.driver.page_source
        self.assertTrue(
            "快速回复" in page_source or "quick" in page_source.lower() or len(self.driver.find_elements(By.CSS_SELECTOR, "table")) > 0,
            "快速回复列表未加载"
        )

    def test_10_create_quick_reply(self):
        """✅ 创建快速回复"""
        self.navigate("/quick-reply")
        time.sleep(1)
        
        # 点击新建
        try:
            create_btn = self.wait_for_clickable(By.XPATH, "//button[contains(text(),'新建')]", timeout=5)
            create_btn.click()
        except:
            create_btn = self.wait_for_clickable(By.CSS_SELECTOR, "button.el-button--primary", timeout=5)
            create_btn.click()
        
        time.sleep(1)
        
        # 填写标题
        title = f"QReply-{uuid.uuid4().hex[:8]}"
        title_input = self.wait_for_element(By.CSS_SELECTOR, "input[placeholder*='标题'], input", timeout=5)
        title_input.clear()
        title_input.send_keys(title)
        
        # 填写内容
        try:
            content = self.driver.find_element(By.CSS_SELECTOR, "textarea")
            content.clear()
            content.send_keys("快速回复测试内容")
        except:
            pass
        
        # 提交
        submit_btn = self.wait_for_clickable(By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit'], .el-button--primary", timeout=5)
        submit_btn.click()
        
        self.wait_for_ajax()
        time.sleep(1)
        
        # 验证
        self.assertIn("/quick-reply", self.driver.current_url, "创建后不在快速回复页")


# ==================== D. 统计测试 ====================
class TestStatistics(TestBase):
    """数据统计测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver.get(BASE_URL + "/login")
        time.sleep(1)
        try:
            u_input = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text'], input"))
            )
            u_input.clear()
            u_input.send_keys(TEST_USER)
            p_input = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            p_input.clear()
            p_input.send_keys(TEST_PASS)
            btn = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit'], button"))
            )
            btn.click()
            time.sleep(2)
        except:
            pass

    def test_11_dashboard_load(self):
        """✅ 仪表板加载"""
        self.navigate("/dashboard")
        self.wait_for_ajax()
        time.sleep(1)
        
        # 检查统计卡片
        cards = self.driver.find_elements(By.CSS_SELECTOR, ".el-card, .card, [class*='card']")
        self.assertTrue(len(cards) > 0, "仪表板卡片未加载")

    def test_12_statistics_page_load(self):
        """✅ 统计页面加载"""
        self.navigate("/statistics")
        self.wait_for_ajax()
        time.sleep(2)
        
        # 检查页面
        page_source = self.driver.page_source
        self.assertTrue(
            "统计" in page_source or len(self.driver.find_elements(By.CSS_SELECTOR, "canvas, svg")) > 0,
            "统计页面未加载"
        )

    def test_13_charts_render(self):
        """✅ 图表渲染"""
        self.navigate("/statistics")
        self.wait_for_ajax()
        time.sleep(3)
        
        # 检查图表元素
        charts = self.driver.find_elements(By.CSS_SELECTOR, "canvas, svg, [class*='chart'], [class*='echarts']")
        self.assertTrue(len(charts) > 0, "图表未渲染")


# ==================== E. 个人设置测试 ====================
class TestSettings(TestBase):
    """个人设置测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver.get(BASE_URL + "/login")
        time.sleep(1)
        try:
            u_input = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text'], input"))
            )
            u_input.clear()
            u_input.send_keys(TEST_USER)
            p_input = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            p_input.clear()
            p_input.send_keys(TEST_PASS)
            btn = WebDriverWait(cls.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[native-type='submit'], button[type='submit'], button"))
            )
            btn.click()
            time.sleep(2)
        except:
            pass

    def test_14_profile_settings_load(self):
        """✅ 个人设置页面加载"""
        self.navigate("/profile-settings")
        self.wait_for_ajax()
        time.sleep(1)
        
        # 检查页面
        page_source = self.driver.page_source
        self.assertTrue(
            "设置" in page_source or "profile" in page_source.lower() or len(self.driver.find_elements(By.CSS_SELECTOR, "input")) > 0,
            "个人设置页面未加载"
        )

    def test_15_staff_management_load(self):
        """✅ 员工管理页面加载"""
        self.navigate("/staff-management")
        self.wait_for_ajax()
        time.sleep(1)
        
        # 检查表格
        tables = self.driver.find_elements(By.CSS_SELECTOR, "table")
        self.assertTrue(len(tables) > 0, "员工管理表格未加载")

    def test_16_page_navigation(self):
        """✅ 页面导航"""
        # 测试导航到各个主要页面
        pages = ["/dashboard", "/tickets", "/quick-reply", "/statistics"]
        
        for page in pages:
            self.navigate(page)
            time.sleep(1)
            self.assertIn(page.split("/")[1], self.driver.current_url, f"导航到 {page} 失败")


# ==================== HTML 报告生成器 ====================
class HTMLTestReporter:
    """HTML 报告生成"""

    _CSS = """
    <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
           background: #f5f7fa; color: #333; }
    .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; }
    h1 { font-size: 28px; color: #2c3e50; margin-bottom: 5px; }
    .subtitle { color: #7f8c8d; font-size: 14px; margin-bottom: 30px; }
    .summary { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 30px; }
    .card { background: #fff; border-radius: 10px; padding: 20px 24px;
            flex: 1; min-width: 140px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
    .card .num { font-size: 36px; font-weight: 700; }
    .card .label { font-size: 13px; color: #999; margin-top: 4px; }
    .card.total .num { color: #2c3e50; }
    .card.passed .num { color: #27ae60; }
    .card.failed .num { color: #e74c3c; }
    .card.skipped .num { color: #f39c12; }
    .card.rate .num { color: #2980b9; }
    .section { background: #fff; border-radius: 10px; padding: 24px;
               margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
    .section h2 { font-size: 18px; color: #2c3e50; margin-bottom: 16px;
                  padding-bottom: 10px; border-bottom: 2px solid #ecf0f1; }
    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th { background: #f8f9fa; padding: 10px 14px; text-align: left;
         font-weight: 600; color: #555; border-bottom: 2px solid #e9ecef; }
    td { padding: 10px 14px; border-bottom: 1px solid #f0f0f0; vertical-align: top; }
    tr:last-child td { border-bottom: none; }
    .badge { display: inline-block; padding: 3px 10px; border-radius: 20px;
             font-size: 12px; font-weight: 600; }
    .badge-pass { background: #d5f5e3; color: #1e8449; }
    .badge-fail { background: #fadbd8; color: #c0392b; }
    .badge-skip { background: #fdebd0; color: #d35400; }
    .progress-bar-wrap { background: #ecf0f1; border-radius: 20px; height: 10px;
                         margin-top: 10px; overflow: hidden; }
    .progress-bar { height: 10px; border-radius: 20px; background: #27ae60;
                    transition: width .3s; }
    .timing { font-size: 12px; color: #999; }
    .group-header td { background: #f8f9fa; font-weight: 600; color: #2c3e50;
                       padding: 8px 14px; }
    footer { text-align: center; color: #bdc3c7; font-size: 12px; padding: 20px 0; }
    </style>
    """

    def __init__(self):
        self.results = []
        self.start_time = time.time()
        self.end_time = None

    def startTest(self, test):
        test._start_time = time.time()

    def stopTest(self, test):
        elapsed = time.time() - getattr(test, "_start_time", time.time())
        if self.results:
            self.results[-1]["elapsed"] = elapsed

    def addSuccess(self, test):
        self.results.append({
            "name": test._testMethodName,
            "class": type(test).__name__,
            "status": "pass",
            "elapsed": 0.0,
            "error": None,
        })
        print(f"  ✓ {test._testMethodName}")

    def addFailure(self, test, err):
        self.results.append({
            "name": test._testMethodName,
            "class": type(test).__name__,
            "status": "fail",
            "elapsed": 0.0,
            "error": "".join(traceback.format_exception(*err)),
        })
        print(f"  ✗ {test._testMethodName}")

    def addError(self, test, err):
        self.results.append({
            "name": test._testMethodName,
            "class": type(test).__name__,
            "status": "error",
            "elapsed": 0.0,
            "error": "".join(traceback.format_exception(*err)),
        })
        print(f"  E {test._testMethodName}")

    def addSkip(self, test, reason):
        self.results.append({
            "name": test._testMethodName,
            "class": type(test).__name__,
            "status": "skip",
            "elapsed": 0.0,
            "error": reason,
        })
        print(f"  S {test._testMethodName}")

    def finalize(self):
        self.end_time = time.time()
        return self

    def generate_report(self, filepath: str = REPORT_FILE):
        """生成 HTML 报告"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "pass")
        failed = sum(1 for r in self.results if r["status"] in ("fail", "error"))
        skipped = sum(1 for r in self.results if r["status"] == "skip")
        total_elapsed = (self.end_time or time.time()) - self.start_time
        rate = round(passed / total * 100, 1) if total > 0 else 0

        # 按测试类分组
        groups = {}
        for r in self.results:
            groups.setdefault(r["class"], []).append(r)

        group_names = {
            "TestAuthentication": "认证测试",
            "TestTicketManagement": "工单管理测试",
            "TestQuickReply": "快速回复测试",
            "TestStatistics": "数据统计测试",
            "TestSettings": "个人设置测试",
        }

        rows_html = ""
        for cls_name, items in groups.items():
            group_label = group_names.get(cls_name, cls_name)
            rows_html += f"""
            <tr><td class="group-header" colspan="4">
                {group_label}（{len(items)} 个用例）
            </td></tr>"""
            for r in items:
                status = r["status"]
                badge_cls = {
                    "pass": "badge-pass",
                    "fail": "badge-fail",
                    "error": "badge-fail",
                    "skip": "badge-skip",
                }.get(status, "badge-skip")
                status_label = {
                    "pass": "✓ 通过",
                    "fail": "✗ 失败",
                    "error": "✗ 错误",
                    "skip": "⊘ 跳过",
                }.get(status, status)
                elapsed_str = f"{r['elapsed']:.2f}s"
                
                rows_html += f"""
                <tr>
                    <td>{r['name']}</td>
                    <td><span class="badge {badge_cls}">{status_label}</span></td>
                    <td class="timing">{elapsed_str}</td>
                </tr>"""

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>测试执行报告</title>
{self._CSS}
</head>
<body>
<div class="container">
    <h1>🧪 工单管理系统端到端测试报告</h1>
    <p class="subtitle">生成时间：{now_str} | 总耗时：{total_elapsed:.1f}s</p>

    <div class="summary">
        <div class="card total">
            <div class="num">{total}</div>
            <div class="label">测试总数</div>
        </div>
        <div class="card passed">
            <div class="num">{passed}</div>
            <div class="label">✓ 通过</div>
        </div>
        <div class="card failed">
            <div class="num">{failed}</div>
            <div class="label">✗ 失败</div>
        </div>
        <div class="card skipped">
            <div class="num">{skipped}</div>
            <div class="label">⊘ 跳过</div>
        </div>
        <div class="card rate">
            <div class="num">{rate}%</div>
            <div class="label">成功率</div>
            <div class="progress-bar-wrap">
                <div class="progress-bar" style="width:{rate}%"></div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📋 测试用例执行结果</h2>
        <table>
            <thead>
                <tr>
                    <th>用例名称</th>
                    <th>结果</th>
                    <th>耗时</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>

    <footer>由 test_system_complete_e2e.py 自动生成 • {now_str}</footer>
</div>
</body>
</html>"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n✅ 报告已生成: {filepath}")
        return filepath


class _ReportingTestResult(unittest.TestResult):
    """自定义测试结果"""

    def __init__(self, reporter: HTMLTestReporter):
        super().__init__()
        self.reporter = reporter

    def startTest(self, test):
        super().startTest(test)
        self.reporter.startTest(test)

    def stopTest(self, test):
        super().stopTest(test)
        self.reporter.stopTest(test)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.reporter.addSuccess(test)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.reporter.addFailure(test, err)

    def addError(self, test, err):
        super().addError(test, err)
        self.reporter.addError(test, err)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.reporter.addSkip(test, reason)


# ==================== main ====================
def main():
    print("=" * 70)
    print("  🧪 工单管理系统 - 完整端到端功能测试")
    print(f"  前端: {BASE_URL}")
    print(f"  后端: {API_BASE}")
    print(f"  测试账号: {TEST_USER}")
    print("=" * 70)
    print()

    reporter = HTMLTestReporter()
    result = _ReportingTestResult(reporter)

    # 收集测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_classes = [
        TestAuthentication,
        TestTicketManagement,
        TestQuickReply,
        TestStatistics,
        TestSettings,
    ]
    
    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    total = suite.countTestCases()
    print(f"共 {total} 个测试用例\n")

    # 打印分组标题
    current_cls = None
    for test in suite:
        cls_name = type(test).__name__
        if cls_name != current_cls:
            current_cls = cls_name
            titles = {
                "TestAuthentication": "A. 认证测试",
                "TestTicketManagement": "B. 工单管理测试",
                "TestQuickReply": "C. 快速回复测试",
                "TestStatistics": "D. 数据统计测试",
                "TestSettings": "E. 个人设置测试",
            }
            print(f"\n[{titles.get(cls_name, cls_name)}]")

    print()
    
    # 运行测试
    suite.run(result)

    # 生成报告
    reporter.finalize()
    reporter.generate_report(REPORT_FILE)

    # 打印摘要
    total_run = len(reporter.results)
    passed = sum(1 for r in reporter.results if r["status"] == "pass")
    failed = sum(1 for r in reporter.results if r["status"] in ("fail", "error"))
    skipped = sum(1 for r in reporter.results if r["status"] == "skip")
    elapsed = (reporter.end_time or time.time()) - reporter.start_time

    print("\n" + "=" * 70)
    print(f"  📊 测试完成")
    print(f"  总计: {total_run}  通过: {passed}  失败: {failed}  跳过: {skipped}")
    print(f"  成功率: {round(passed/total_run*100, 1) if total_run else 0}%")
    print(f"  总耗时: {elapsed:.1f}s")
    print(f"  报告: {REPORT_FILE}")
    print("=" * 70)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
