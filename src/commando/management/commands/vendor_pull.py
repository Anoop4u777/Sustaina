import helpers

from django.conf import settings
from django.core.management .base import BaseCommand


STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')

VENDOR_STATICFILES = {
    "flowbite.min.css":"https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css",
    "flowbite.min.js":"https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js",
}

class Command(BaseCommand):


    def handle(self, *args, **options):
        completed_urls = []
        
        self.stdout.write("Downloading vendor static files")

        for name, url in VENDOR_STATICFILES.items():
            outpath = STATICFILES_VENDOR_DIR / name
            dl_success = helpers.download_to_local(url, outpath)
            if dl_success:
                completed_urls.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f"Downloading vendor static files failed in url {url}"))
        
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                    self.style.SUCCESS("Downloading vendor static files completed successfully"))
        else:
            self.stdout.write(
                    self.style.WARNING("Some files were not downloaded"))