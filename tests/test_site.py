import os

import needle.cases
import pytest
import selenium.webdriver.chrome.options
from needle.cases import NeedleTestCase


def needle_fixup_get_screenshot():
    """When capturing screenshots, only the contents in the viewport are
    rendered. However, Needle insists in creating images which are as big
    as the actual element, which means that if the element is larger than
    the viewport the final image will contain black unrendered areas.
    This fixup limits the size of the image to the one of the viewport,
    trimming away any potential blank area."""
    import needle.driver

    orig_get_screenshot = needle.driver.NeedleWebElementMixin.get_screenshot

    def override_get_screenshot(self):
        image = orig_get_screenshot(self)
        width, height = image.size
        window_size = self.parent.get_window_size()
        width = min(width, window_size["width"])
        height = min(height, window_size["height"])
        image = image.crop((0, 0, width, height))
        return image

    needle.driver.NeedleWebElementMixin.orig_get_screenshot = orig_get_screenshot
    needle.driver.NeedleWebElementMixin.get_screenshot = override_get_screenshot


def webdriver_fixup_version_mode():
    """Set version_mode to a repeatable string to avoid test failures each time
    the version string is updated.
    """
    import selenium.webdriver.remote.webdriver

    orig_get = selenium.webdriver.remote.webdriver.WebDriver.get

    def override_get(self, url):
        orig_get(self, url)
        disable_transitions = """
            versionMode = document.getElementById('version_mode');
            versionMode.textContent = 'weboll x.y.z - mode: production';
        """
        self.execute_script(disable_transitions)

    selenium.webdriver.remote.webdriver.WebDriver.orig_get = orig_get
    selenium.webdriver.remote.webdriver.WebDriver.get = override_get


needle_fixup_get_screenshot()
webdriver_fixup_version_mode()

SITE_URL = os.environ.get("TEST_SITE_URL")


@pytest.mark.skipif(
    SITE_URL is None, reason="requires a running instance [$TEST_SITE_URL]"
)
class SiteTest(NeedleTestCase):
    engine_class = "needle.engines.perceptualdiff_engine.Engine"
    viewport_height = 2048

    @classmethod
    def get_web_driver(cls):
        options = selenium.webdriver.chrome.options.Options()
        options.headless = True
        options.add_argument("--no-sandbox")
        return needle.cases.NeedleChrome(options=options)

    def test_homepage(self):
        self.driver.get(SITE_URL)
        self.assertScreenshot("html", "homepage")
