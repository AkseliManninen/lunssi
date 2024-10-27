import i18nConfig from "@/i18nConfig";
import { defaultRegion } from "@/utils/constants";
import Region from "./[region]/page";

type Props = {
  params: { locale: string };
};

const Home = ({ params }: Props) => {
  const locale = params.locale ?? i18nConfig.defaultLocale;
  return <Region params={{ locale, region: defaultRegion }} />;
};

// Reuse the metadata generation from the region page
export { generateMetadata } from "./[region]/page";

export default Home;
