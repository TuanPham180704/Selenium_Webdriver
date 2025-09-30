

import csv
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://duckduckgo.com/"
QUERIES = [
    "Python", "Selenium WebDriver", "OpenAI", "kotlin", "reactjs",
    "stress testing", "emoji 🐍🔥", "a" * 500,  
    "<script>alert('xss')</script>", "concurrency testing"
]
NUM_TABS = 100
WAIT_SECONDS = 15  
SCREENSHOT_DIR = "screenshots_stress"
REPORT_CSV = "stress_report.csv"


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def detect_bot_or_captcha(driver):
    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    except Exception:
        body_text = ""
    if "are you a robot" in body_text or "please verify" in body_text or "verify you're human" in body_text:
        return True, "verification_text_found"
    page_source_lower = driver.page_source.lower()
    if "captcha" in page_source_lower or "recaptcha" in page_source_lower:
        return True, "captcha_keyword_in_source"
    # try iframe scan
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for i, iframe in enumerate(iframes):
            try:
                src = iframe.get_attribute("src") or ""
                if "recaptcha" in src or "captcha" in src:
                    return True, f"captcha_iframe_src_{i}"
            except Exception:
                continue
    except Exception:
        pass
    return False, ""

def run_stress_test():
    results = []
    driver = None
    start_time_overall = time.perf_counter()
    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as e:
        print("ERROR: Could not start Chrome WebDriver:", e)
        return

    try:
        driver.get(BASE_URL)
        time.sleep(0.5)
        for i in range(NUM_TABS - 1):
            driver.execute_script("window.open('about:blank');")
            time.sleep(0.1)

        handles = driver.window_handles
        if len(handles) < NUM_TABS:
            print(f"Warning: only {len(handles)} tabs available, expected {NUM_TABS}")
        for idx in range(NUM_TABS):
            handle = handles[idx] if idx < len(handles) else handles[-1]
            query = QUERIES[idx] if idx < len(QUERIES) else f"auto query {idx}"
            driver.switch_to.window(handle)
            tab_info = {
                "tab_index": idx,
                "query": query,
                "start_time": None,
                "end_time": None,
                "duration_s": None,
                "status": "not_started",
                "notes": "",
                "screenshot": "",
                "exception": ""
            }
            try:
                search_url = BASE_URL + "?q=" + query
                tab_info["start_time"] = datetime.utcnow().isoformat() + "Z"
                t0 = time.perf_counter()
                driver.get(search_url)
                try:
                    wait = WebDriverWait(driver, WAIT_SECONDS)
                    wait.until(
                        EC.any_of(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "a.result__a")),
                            EC.presence_of_element_located((By.ID, "links")),  # fallback container
                            EC.presence_of_element_located((By.TAG_NAME, "body"))
                        )
                    )
                    t1 = time.perf_counter()
                    tab_info["end_time"] = datetime.utcnow().isoformat() + "Z"
                    tab_info["duration_s"] = round(t1 - t0, 3)
                    tab_info["status"] = "ok"
                except TimeoutException:
                    t1 = time.perf_counter()
                    tab_info["end_time"] = datetime.utcnow().isoformat() + "Z"
                    tab_info["duration_s"] = round(t1 - t0, 3)
                    tab_info["status"] = "timeout_waiting_results"
                    tab_info["notes"] += f" waited {WAIT_SECONDS}s, no results element."
                    fname = os.path.join(SCREENSHOT_DIR, f"tab_{idx}_timeout.png")
                    try:
                        driver.save_screenshot(fname)
                        tab_info["screenshot"] = fname
                    except Exception as e:
                        tab_info["exception"] = f"screenshot_failed:{e}"
                bot, reason = detect_bot_or_captcha(driver)
                if bot:
                    tab_info["status"] = "blocked_by_bot_detection"
                    tab_info["notes"] += f" bot_detected:{reason}"
                    fname = os.path.join(SCREENSHOT_DIR, f"tab_{idx}_bot.png")
                    try:
                        driver.save_screenshot(fname)
                        tab_info["screenshot"] = fname
                    except Exception as e:
                        tab_info["exception"] += f" screenshot_failed:{e}"
                else:
                    try:
                        els = driver.find_elements(By.CSS_SELECTOR, "a.result__a")
                        tab_info["notes"] += f" result_links={len(els)}"
                    except Exception:
                        pass
                time.sleep(0.2)
            except WebDriverException as ex:
                tab_info["status"] = "driver_exception"
                tab_info["exception"] = str(ex)
                try:
                    fname = os.path.join(SCREENSHOT_DIR, f"tab_{idx}_exception.png")
                    driver.save_screenshot(fname)
                    tab_info["screenshot"] = fname
                except Exception:
                    pass
            results.append(tab_info)

        try:
            _ = driver.title  
            driver_alive = True
        except Exception:
            driver_alive = False

        overall_duration = round(time.perf_counter() - start_time_overall, 3)
        print(f"\nOverall run time: {overall_duration}s. Driver alive: {driver_alive}")

    finally:
        try:
            driver.quit()
        except Exception:
            pass

    keys = ["tab_index", "query", "start_time", "end_time", "duration_s", "status", "notes", "screenshot", "exception"]
    with open(REPORT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    print("\n=== SUMMARY ===")
    for r in results:
        print(f"Tab {r['tab_index']:2d} | status={r['status']:30s} | dur={r.get('duration_s')}s | notes={r['notes']}")
    print(f"\nReport saved to: {REPORT_CSV}")
    print(f"Screenshots (if any) in: {os.path.abspath(SCREENSHOT_DIR)}")

if __name__ == "__main__":
    run_stress_test()
