import asyncio
import json
from playwright.async_api import async_playwright

async def search_google_for_quora(term):
    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(
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
            #print(results)
            return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    finally:
        if browser:
            await browser.close()

async def search_videos(term, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            results = await search_google_for_quora(term)
            # Drop the 'title' field from the results
            results = [result for result in results if 'title' not in result]
            
            # Use UTF-8 encoding and handle encoding errors
            encoded_results = json.dumps(results, ensure_ascii=False, indent=2).encode('utf-8', errors='ignore').decode('utf-8')
            
            if results:
                return results[0]
            else:
                print(f"No results found for: {term}")
                return None
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                print(f"Max retries reached. An error occurred while searching for videos: {str(e)}")
                return {
                    "title": "Error in searching for videos",
                    "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                }
