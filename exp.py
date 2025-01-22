
import asyncio

import agentql as exp
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

# URL of the e-commerce website
# You can replace it with any other e-commerce website but the queries should be updated accordingly
URL = "https://app.civi.co.il/promo/id=821885&src=6069"
# url = "https://careers.mastercard.com/us/en/job/MASRUSR235796EXTERNALENUS/QA-Automation?utm_medium=phenom-feeds&source=LINKEDIN&utm_source=linkedin"
# url = "https://www.comeet.com/jobs/pango/59.002/qa-automation-engineer/E9.949"
# url = "https://bringoz.bamboohr.com/careers/44?source=aWQ9MTk%3D"
# url = "https://careers.varonis.com/careers?p=job%2FoEGbufwJ%2Fapply&jvs=LinkedInLimited&jvk=Apply&jvi=oEGbufwJ,Apply&j=oEGbufwJ&__jvst=Job%20Board&__jvsd=LinkedInLimited&nl=1"
# url = "https://app.civi.co.il/promo/id=821885&src=6069"
# url = "https://fa-eqnk-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_3001/job/20211369?utm_medium=jobshare&utm_source=linkedin"
# url ="https://app.ismartrecruit.com/jobDescription?x=E7pdXJiYW5yZWNydWl0cy5jby5pbF8xNTMxX0xJTktFRElOQ9e"


async def main():
    """Main function."""
    async with async_playwright() as playwright, await playwright.chromium.launch(
        headless=False
    ) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = await exp.wrap_async(browser.new_page())
        await page.goto(URL)  # open the target URL

        # form_query = """
        # {
        #     first_name
        #     last_name
        #     email
        #     subject_of_inquiry
        #     inquiry_text_box
        #     submit_btn
        # }
        # """
        form_query = """
        {
            submit_btn
        }
        """
        response = await page.query_elements(form_query)

        # await response.first_name.fill("John")
        # await response.last_name.fill("Doe")
        # await response.email.fill("johndoe@agentql.com")
        # await response.subject_of_inquiry.select_option(label="Sales Inquiry")
        # await response.inquiry_text_box.fill("I want to learn more about AgentQL")

        # Submit the form
        await response.submit_btn.click()

        # confirm form
        confirm_query = """
        {
            confirmation_btn
        }
        """

        response = await page.query_elements(confirm_query)
        await response.confirmation_btn.click()
        await page.wait_for_page_ready_state()
        await page.wait_for_timeout(3000)  # wait for 3 seconds
        print("Form submitted successfully!")


if __name__ == "__main__":
    asyncio.run(main())