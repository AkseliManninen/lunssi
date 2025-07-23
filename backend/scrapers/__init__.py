from scrapers.bruuveri import BruuveriScraper
from scrapers.faasai import FaasaiScraper
from scrapers.hamis import HamisScraper
from scrapers.hanken import HankenScraper
from scrapers.kansis import KansisScraper
from scrapers.karljohan import KarljohanScraper
from scrapers.plaza import PlazaScraper
from scrapers.pompier_albertinkatu import PompierAlbertinkatuScraper
from scrapers.queem import QueemScraper
from scrapers.stahlberg import StahlbergScraper
from scrapers.valssi import ValssiScraper


def get_all_scrapers():
    return {
        "bruuveri": BruuveriScraper(),
        "faasai": FaasaiScraper(),
        "hamis": HamisScraper(),
        "hanken": HankenScraper(),
        "kansis": KansisScraper(),
        "karljohan": KarljohanScraper(),
        "plaza": PlazaScraper(),
        "pompier_albertinkatu": PompierAlbertinkatuScraper(),
        "queem": QueemScraper(),
        "stahlberg": StahlbergScraper(),
        "valssi": ValssiScraper(),
    }
