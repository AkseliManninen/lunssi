import LanguageChanger from "@/components/LanguageChanger";
import RegionChanger from "@/components/RegionChanger";
import RestaurantCard, {
  type RestaurantCardProps,
} from "@/components/RestaurantCard";
import TranslationsProvider from "@/components/TranslationProvider";
import i18nConfig from "@/i18nConfig";
import axios from "axios";
import type { Metadata } from "next";
import React from "react";
import initTranslations from "../i18n";

const getRestaurantData = async (
  locale: string,
  region?: string,
): Promise<RestaurantCardProps[]> => {
  const params = new URLSearchParams({ lang: locale });
  if (region) {
    params.append("region", region);
  }

  const restaurantData = await axios
    .get(`${process.env.BACKEND_API_URL}/restaurants?${params.toString()}`)
    .then((response) => response.data);
  return restaurantData;
};

// 6 hours
export const revalidate = 21600;

type Props = { params: { locale?: string } };

const i18nNamespaces = ["translation"];

export const generateMetadata = async ({
  params,
}: Props): Promise<Metadata> => {
  const locale = params.locale ?? i18nConfig.defaultLocale;
  const { t } = await initTranslations(locale, i18nNamespaces);
  return {
    description: t("metaDescription"),
    openGraph: {
      description: t("metaDescription"),
      locale,
    },
  };
};

const Home = async ({
  params,
  searchParams,
}: {
  params: { locale?: string };
  searchParams: { region?: string };
}) => {
  const locale = params.locale ?? i18nConfig.defaultLocale;
  const { region } = searchParams;
  const restaurants = await getRestaurantData(locale, region);
  const { resources } = await initTranslations(locale, i18nNamespaces);
  return (
    <TranslationsProvider
      namespaces={i18nNamespaces}
      locale={locale}
      resources={resources}
    >
      <div className="bg-gray-100 min-h-screen">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-8 text-center text-gray-800">
            Lunssi
          </h1>
          <div className="mt-8 mb-5 flex justify-end gap-4">
            <RegionChanger />
            <LanguageChanger />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {restaurants.map(({ name, lunchItems, lunchPrice, lunchTime }) => (
              <RestaurantCard
                key={name}
                name={name}
                lunchItems={lunchItems}
                lunchPrice={lunchPrice}
                lunchTime={lunchTime}
              />
            ))}
          </div>
        </div>
      </div>
    </TranslationsProvider>
  );
};

export default Home;
