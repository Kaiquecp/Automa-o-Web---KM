import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import os

async def scrape_site():
    download_dir = os.path.expanduser('~') + '/Downloads/KM'
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=False
        ) 
        context = await browser.new_context(
            accept_downloads=True  
        )
        page = await context.new_page()

        download_path = None
        page.on('download', lambda download: download.save_as(os.path.join(download_dir, download.suggested_filename)))
        
        print("Acessando o site...")
        await page.goto("link do site")
        await page.wait_for_load_state("load") 

        print("Preenchendo o email...")
        email_selector = "xpath=/html/body/div/div[2]/div[1]/div[1]/div/div/div[4]/div/div[1]/div[1]/div/input"
        await page.wait_for_selector(email_selector, timeout=10000)
        await page.locator(email_selector).fill("email")

        print("Preenchendo a senha...")
        password_selector = "xpath=/html/body/div/div[2]/div[1]/div[1]/div/div/div[4]/div/div[1]/div[2]/div/input"
        await page.wait_for_selector(password_selector, timeout=10000)
        await page.locator(password_selector).fill("senha")

        print("Fazendo login...")
        login_button_selector = "xpath=/html/body/div/div[2]/div[1]/div[1]/div/div/div[4]/div/div[1]/div[3]/button"
        await page.wait_for_selector(login_button_selector, timeout=10000)
        await page.locator(login_button_selector).click()
        await page.wait_for_load_state("networkidle")

        print("Abrindo filtros...")
        filter_button_selector = "xpath=/html/body/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div"
        await page.wait_for_selector(filter_button_selector, timeout=10000)
        await page.click(filter_button_selector)

        print("Preenchendo período inicial e final...")
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date_selector = "xpath=/html/body/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/input[1]"
        await page.wait_for_selector(start_date_selector, timeout=10000)
        await page.locator(start_date_selector).fill(start_date.strftime("%d/%m/%Y %H:%M"))
        
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        end_date_selector = "xpath=/html/body/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/input[2]"
        await page.wait_for_selector(end_date_selector, timeout=10000)
        await page.locator(end_date_selector).fill(end_date.strftime("%d/%m/%Y %H:%M"))

        print("Aplicando filtros...")
        filter_button_selector = "xpath=/html/body/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div[2]/a"
        await page.wait_for_selector(filter_button_selector, timeout=10000)
        await page.click(filter_button_selector)

        await asyncio.sleep(2)

        print("Iniciando download do CSV...")

        download_button_selector = "xpath=/html/body/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/a/i"
        await page.wait_for_selector(download_button_selector, timeout=10000)
        await page.click(download_button_selector)

        download_csv_selector = page.get_by_text("Exportar CSV")
        await download_csv_selector.click()

        await page.wait_for_load_state("load", timeout=15000)

        confirm_download_selector = page.locator("button.btn.btn-primary.btn-focus:has-text('Sim')")
        await confirm_download_selector.click()

        await asyncio.sleep(30)
        save_download_selector = page.locator("i.text-info.icon-download-alt >> nth=0")
        await save_download_selector.click()
        await asyncio.sleep(60)
        print("Download concluído.")
        await browser.close()
asyncio.run(scrape_site())
