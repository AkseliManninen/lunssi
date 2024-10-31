import i18nConfig from "@/i18nConfig";
import type { ReactNode } from "react";
import "@/styles/globals.css";
import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import { notFound } from "next/navigation";

export const metadata: Metadata = {
  title: "Lunssi",
  openGraph: {
    title: "Lunssi",
    url: "https://lunssi.fly.dev",
    type: "website",
    siteName: "Lunssi",
  },
};

export function generateStaticParams() {
  return i18nConfig.locales.map((locale) => ({ locale }));
}

const roboto = Roboto({
  subsets: ["latin"],
  weight: "400",
  display: "swap",
});

export default async function RootLayout(props: {
  children: ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const params = await props.params;

  const { locale } = params;

  const { children } = props;

  if (!i18nConfig.locales.includes(locale)) {
    notFound();
  }

  return (
    <html lang={locale} className={roboto.className}>
      <body>{children}</body>
    </html>
  );
}
