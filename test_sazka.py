import pytest 
from playwright.sync_api import sync_playwright

@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=1000
        )  # Set headless=False to see the browser actions
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

#test_case_001
def test_sportka_jackpot(page):
    page.goto("https://www.sazka.cz/")
    refuse_btn = page.locator(".consent-bar__actions button.consent-bar__more")
    refuse_btn.click()

    cookie_bar = page.locator("body > div:nth-child(30) > div")
    assert cookie_bar.is_visible() == False

    sportka = page.locator("[alt='Sportka - obrázek']")
    sportka.click()

    title = page.title()
    assert "Sportka" in title

    jackpot = page.locator(
        "body > main > div.lottery-header.sportka > div > div.bs-row\
        > div > div.wrapper > div:nth-child(1) > h1 > strong")
    raw_amount = jackpot.inner_text()
    cl_amount = raw_amount.replace("\u00a0", "")
    cl_amount = cl_amount.replace("Kč", "")
    amount = int(cl_amount)
    assert amount > 30000000

#test_case_002
def test_check_apps(page):
    app_list = ["Sazka Online", "Sazka Hry", "Sazkabet", "Sazka Klub"]
    query = "Mobilni aplikace"
    page.goto("https://www.sazka.cz/")
    refuse_btn = page.locator(".consent-bar__actions button.consent-bar__more")
    refuse_btn.click()

    cookie_bar = page.locator("body > div:nth-child(30) > div")
    assert cookie_bar.is_visible() == False

    search_btn = page.locator("#quick-search-submit")
    search_btn.click()

    page.fill("#quick-search-input", query)
    autocomplete = page.locator("#quick-search-autocomplete")
    autocomplete.wait_for(state="visible", timeout=5000)
    assert autocomplete
    autocomplete.click()

    heading_list = page.locator(".application-item__content-top > h2")
    headings = heading_list.all()

    for item in headings:
        assert item.inner_text() in app_list
    
    content_list = page.locator(".application-item__content")
    content = content_list.all()

    for item in content:
        gp_img = item.locator("[alt='Google Play']")
        assert gp_img.is_visible() == True

#test_case_003
@pytest.mark.parametrize("col_1_p, col_1_s, col_2_p, col_2_s, extra_6", [
    ((2, 4, 15, 27, 40), (5, 11), (18, 34, 37, 40, 47), (1, 6), 303635),
    ((2, 9, 11, 16, 22), (2, 6), (1, 2, 10, 15, 36), (1, 12), 997031),
    ((21, 22, 37, 38, 49), (2, 7), (12, 28, 29, 32, 50), (1, 7), 191206)
])
def test_ticket_check_EJ(page, col_1_p, col_1_s, col_2_p, col_2_s, extra_6):
    page.goto("https://www.sazka.cz/")
    refuse_btn = page.locator(".consent-bar__actions button.consent-bar__more")
    refuse_btn.click()

    cookie_bar = page.locator("body > div:nth-child(30) > div")
    assert cookie_bar.is_visible() == False

    ej = page.locator("[alt='Eurojackpot - obrázek']")
    ej.click()

    check_ticket = page.locator(
        "#result-buttons > div > div > div.l-result__col-buttons__row\
        > div.l-result__col-buttons__check > a")
    check_ticket.click()

    submit_button = page.locator("#btnCheckTicket")
    assert submit_button.is_disabled() == True

    column_1 = page.locator("[data-columnindex='1']")
    primary_number_list = column_1.locator("[data-test='number-primary']")
    secondary_number_list = column_1.locator("[data-test='number-secondary']")
    for item in col_1_p:
        primary_number_list.get_by_text(str(item), exact=True).click()
    for item in col_1_s:
        secondary_number_list.get_by_text(str(item), exact=True).click()
    
    assert submit_button.is_disabled() == False

    column_2 = page.locator("[data-columnindex='2']")
    primary_number_list = column_2.locator("[data-test='number-primary']")
    secondary_number_list = column_2.locator("[data-test='number-secondary']")
    for item in col_2_p:
        primary_number_list.get_by_text(str(item), exact=True).click()
    for item in col_2_s:
        secondary_number_list.get_by_text(str(item), exact=True).click()

    extra_6_button = page.locator("#addonField") 
    extra_6_button.fill(str(extra_6))
    new_class = extra_6_button.get_attribute("class")
    assert new_class == "form-control sance-correct"

    submit_button.click()

    overview = page.locator(".responsive-table-wrapper")
    assert overview.first.is_visible() == True

#test_case_004
def test_check_scratch_card_rules(page):
    christmas_scratchies = [
        ("adventnikalendar", "313"),
        ("vanocniprani", "314"),
        ("zlateprasatko", "315"),
        ("zlatasupina", "316"),
        ("svatecnikalendar", "317"),
        ("vanocnizlatarybka", "318")
        ]
    page.goto("https://www.sazka.cz/losy/stiraci-losy/")
    refuse_btn = page.locator(".consent-bar__actions button.consent-bar__more")
    refuse_btn.click()

    cookie_bar = page.locator("body > div:nth-child(30) > div")
    assert cookie_bar.is_visible() == False

    for name, emission in christmas_scratchies:
        scr = page.locator(f"#{name}-banner")
        scr.first.click()

        game_plan = page.locator("div.ticket-content__grid-after-images > div:nth-child(2) a")
        assert game_plan.is_visible() == True
        game_plan.click()
        
        url = page.url
        assert emission in url
        page.go_back()
        page.go_back()




