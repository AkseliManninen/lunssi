import LanguageChanger from "@/components/LanguageChanger";
import RestaurantCard from "@/components/RestaurantCard";
import TranslationsProvider from "@/components/TranslationProvider";
import i18nConfig from "@/i18nConfig";
import axios from "axios";
import React from "react";
import initTranslations from "../i18n";

const getRestaurantData = async (locale: string) => {
  const restaurantShorthands = [
    "bruuveri",
    "kansis",
    "plaza",
    "pompier_albertinkatu",
    "hämis",
    "queem",
  ];

  const restaurantData = await Promise.all(
    restaurantShorthands.map((shorthand) =>
      axios
        .get(
          `${process.env.BACKEND_API_URL}/restaurant?name=${shorthand}&lang=${locale}`,
        )
        .then((response) => response.data),
    ),
  );
  return restaurantData;
};

// 6 hours
export const revalidate = 21600;

type Props = { params: { locale?: string } };

const i18nNamespaces = ["translation"];

const Home = async ({ params }: Props) => {
  const locale = params.locale ?? i18nConfig.defaultLocale;
  const restaurants = await getRestaurantData(locale);
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
          <div className="mt-8 mb-5 flex justify-end">
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
