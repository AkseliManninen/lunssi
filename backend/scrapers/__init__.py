from scrapers.bierhaus import BierhausScraper
from scrapers.bruuveri import BruuveriScraper
from scrapers.faasai import FaasaiScraper
from scrapers.hamis import HamisScraper
from scrapers.hanken import HankenScraper
from scrapers.kansis import KansisScraper
from scrapers.karljohan import KarljohanScraper
from scrapers.meilin import MeilinScraper
from scrapers.mount_kailash import MountKailashScraper
from scrapers.pompier_albertinkatu import PompierAlbertinkatuScraper
from scrapers.puisto import PuistoScraper
from scrapers.queem import QueemScraper
from scrapers.stahlberg import StahlbergScraper
from scrapers.tampella import TampellaScraper
from scrapers.valssi import ValssiScraper
from scrapers.da_spizzico import DaSpizzicoScraper
from scrapers.via_tribunali import ViatribunaliScraper


def get_all_scrapers():
    return {
        "bierhaus": BierhausScraper(),
        "bruuveri": BruuveriScraper(),
        "faasai": FaasaiScraper(),
        "hamis": HamisScraper(),
        "hanken": HankenScraper(),
        "kansis": KansisScraper(),
        "karljohan": KarljohanScraper(),
        "meilin": MeilinScraper(),
        "mount_kailash": MountKailashScraper(),
        "pompier_albertinkatu": PompierAlbertinkatuScraper(),
        "puisto": PuistoScraper(),
        "queem": QueemScraper(),
        "stahlberg": StahlbergScraper(),
        "tampella": TampellaScraper(),
        "valssi": ValssiScraper(),
        "da_spizzico": DaSpizzicoScraper(),
        "via_tribunali": ViatribunaliScraper(),
    }
