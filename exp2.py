import asyncio
import agentql as exp
from playwright.async_api import async_playwright
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


async def foo(URL):
    """Main function."""
    async with async_playwright() as playwright, await playwright.chromium.launch(
        headless=False
    ) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = await exp.wrap_async(browser.new_page())
        await page.goto(URL)  # open the target URL

        resume_keyword = "resume"
        submit_keyword = "submit_button"
        password_keyword = "password"

        # Define queries for form, show-form-button, and login
        # resume_query = f"{{ {resume_keyword} }}"
        # submit_query = f"{{ {submit_keyword} }}"
        # password_query = f"{{ {password_keyword} }}"
        resume_query = "{ resume }"
        submit_query = "{ submit_button }"
        password_query = "{ password }"

        # Check for the presence of form, show-form-button, or login
        resume_response = await page.query_elements(resume_query)
        submit_response = await page.query_elements(submit_query)
        password_response = await page.query_elements(password_query)

        # BLA
        resume_object = resume_response._response_data[resume_keyword]
        submit_object = submit_response._response_data[submit_keyword]
        password_object = password_response._response_data[password_keyword]

        if password_object:
            # Login page were user and password needed.
            print("Login page detected.")
            return

        if resume_object and submit_object:
            # Both resume and submit files are displayed, so maybe its direct application page.
            # Find elements that need to be filled.
            print("Direct application page detected.")
            return

        elif submit_object:
            # Submit button found, but not resume field, so maybe operation needed to display form.
            # Click button and determine details to fill.
            print("No Form detected, maybe operation requiered.")
            await submit_response.click()

        else:
            print("Related elements not found.")


def main():
    # URL of the e-commerce website
    URLS = [
        # "https://careers.mastercard.com/us/en/job/MASRUSR235796EXTERNALENUS/QA-Automation?utm_medium=phenom-feeds&source=LINKEDIN&utm_source=linkedin",
        # "https://www.comeet.com/jobs/pango/59.002/b2b-sales-manager/B1.B44",
        # "https://bringoz.bamboohr.com/careers/44?source=aWQ9MTk%3D",
        # "https://careers.varonis.com/careers?p=job%2FoEGbufwJ%2Fapply&jvs=LinkedInLimited&jvk=Apply&jvi=oEGbufwJ,Apply&j=oEGbufwJ&__jvst=Job%20Board&__jvsd=LinkedInLimited&nl=1",
        "https://app.civi.co.il/promo/id=821885&src=6069",
        # "https://fa-eqnk-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_3001/job/20211369?utm_medium=jobshare&utm_source=linkedin",
        # "https://app.ismartrecruit.com/jobDescription?x=E7pdXJiYW5yZWNydWl0cy5jby5pbF8xNTMxX0xJTktFRElOQ9e",
    ]

    for URL in URLS:
        domain = urlparse(URL).netloc
        print(domain)
        asyncio.run(foo(URL))
    
if __name__ == "__main__":
    main()