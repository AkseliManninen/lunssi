from scrapers.bistro_tammer import BistroTammerScraper
from scrapers.faasai import FaasaiScraper
from scrapers.hamis import HamisScraper
from scrapers.hanken import HankenScraper
from scrapers.kansis import KansisScraper
from scrapers.karljohan import KarljohanScraper
from scrapers.plaza import PlazaScraper
from scrapers.pompier_albertinkatu import PompierAlbertinkatuScraper
from scrapers.puisto import PuistoScraper
from scrapers.queem import QueemScraper
from scrapers.stahlberg import StahlbergScraper
from scrapers.valssi import ValssiScraper


def get_all_scrapers():
    return {
        "bistro_tammer": BistroTammerScraper(),
        "faasai": FaasaiScraper(),
        "hamis": HamisScraper(),
        "hanken": HankenScraper(),
        "kansis": KansisScraper(),
        "karljohan": KarljohanScraper(),
        "plaza": PlazaScraper(),
        "pompier_albertinkatu": PompierAlbertinkatuScraper(),
        "puisto": PuistoScraper(),
        "queem": QueemScraper(),
        "stahlberg": StahlbergScraper(),
        "valssi": ValssiScraper(),
    }
