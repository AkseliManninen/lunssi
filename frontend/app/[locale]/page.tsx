import { defaultRegion } from "@/utils/constants";
import Region from "./[region]/page";

export const revalidate = 21600;

type Props = {
  params: Promise<{ locale: string }>;
};

const Home = async (props: Props) => {
  const { locale } = await props.params;
  const regionParams = Promise.resolve({
    locale,
    region: defaultRegion,
  });
  return <Region params={regionParams} />;
};

// Reuse the metadata generation from the region page
export { generateMetadata } from "./[region]/page";

export default Home;
