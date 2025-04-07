from playwright.sync_api import sync_playwright
from datetime import datetime
import time

with sync_playwright() as p:
    # Запускаем браузер
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Переходим на HH.ru
    page.goto("https://cheboksary.hh.ru/")
    page.get_by_role("link", name="Войти").click()

    # Логин в аккаунт
    page.get_by_label("Электронная почта или телефон").fill("dix.05@bk.ru")
    page.locator("a").filter(has_text="Войти с паролем").click()
    page.get_by_label("Пароль").fill("Har52864079")
    page.get_by_role("button", name="Войти").click()

    # Ждем авторизацию
    page.wait_for_url("https://cheboksary.hh.ru/applicant/*")

    # Проверяем успешность авторизации
    if not page.query_selector('a[href="/logout"]'):
        print("Авторизация не удалась")
        exit(1)

    # Переходим к разделу откликов
    page.get_by_role("link", name="Отклики и приглашения").click()

    # Ждем загрузку страницы
    page.wait_for_load_state("networkidle")

    today_responses = 0
    processed_pages = set()
    current_page = 1

    while True:
        # Добавляем небольшую паузу для стабилизации страницы
        time.sleep(2)
        
        # Ждем элементы откликов
        try:
            page.wait_for_selector('[data-qa="negotiations-item"]', timeout=10000)
        except Exception as e:
            print(f"Элементы откликов не найдены: {e}")
            break

        # Получаем все элементы откликов на странице
        responses = page.query_selector_all('[data-qa="negotiations-item"]')
        
        # Если на странице нет откликов, прерываем цикл
        if not responses:
            break

        for response in responses:
            # Извлекаем дату отклика
            date_element = response.query_selector('[data-qa="negotiations-item-date"]')
            if date_element:
                date_text = date_element.inner_text().strip()
                if "Сегодня" in date_text:
                    today_responses += 1

        # Проверяем наличие следующей страницы
        next_button = page.query_selector('[data-qa="pager-next"]')
        if not next_button or "disabled" in next_button.get_attribute("class"):
            break
            
        # Получаем номер текущей страницы
        active_page = page.query_selector('.bloko-pagination-page.bloko-pagination-page_active')
        if active_page:
            current_page = int(active_page.inner_text())
            
        # Если мы уже обрабатывали эту страницу, прерываем цикл
        if current_page in processed_pages:
            break
            
        processed_pages.add(current_page)
        
        # Кликаем на следующую страницу
        next_button.click()
        page.wait_for_load_state("networkidle")

    print(f"Количество откликов сегодня: {today_responses}")

    # Закрываем браузер
    browser.close()