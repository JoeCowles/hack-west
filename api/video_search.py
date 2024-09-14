import asyncio
import json
from playwright.async_api import async_playwright


async def search_google_for_quora(term):
    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--no-zygote",
                    "--single-process",
                    "--disable-extensions",
                ],
                headless=True,
            )
            page = await browser.new_page()

            url = f"https://www.google.com/search?q=site:youtube.com+{term}"
            await page.goto(url)

            await page.wait_for_selector("div.g")

            results = await page.evaluate(
                """
                () => Array.from(document.querySelectorAll('div.g')).slice(0, 15).map(result => {
                    const titleElement = result.querySelector('h3');
                    const linkElement = result.querySelector('a');
                    const snippetElement = result.querySelector('.VwiC3b');
                    return {
                        title: titleElement ? titleElement.innerText : '',
                        link: linkElement ? linkElement.href : '',
                        snippet: snippetElement ? snippetElement.innerText : ''
                    };
                }).filter(result => result.link.includes('youtube.com'))
            """
            )
            print(results)
            return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    finally:
        if browser:
            await browser.close()


async def search_videos(term):
    results = await search_google_for_quora(term)
    return results[0]
