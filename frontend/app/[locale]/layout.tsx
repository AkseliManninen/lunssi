import type { ReactNode } from "react";
import "@/styles/globals.css";
import { GoogleTagManager } from "@next/third-parties/google";
import type { Metadata } from "next";
import { Roboto } from "next/font/google";
import { notFound } from "next/navigation";
import { setRequestLocale } from "next-intl/server";
import Footer from "@/components/Footer";
import { routing } from "@/i18n/routing";

export const metadata: Metadata = {
  openGraph: {
    url: "https://lunssi.fi",
    type: "website",
    siteName: "Lunssi",
  },
};

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
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

  const gtmId = process.env.NEXT_PUBLIC_GTM_CONTAINER_ID ?? "";

  if (!routing.locales.includes(locale as any)) {
    notFound();
  }

  setRequestLocale(locale);

  return (
    <html lang={locale} className={roboto.className}>
      <GoogleTagManager gtmId={gtmId} />
      <body>
        {children}
        <Footer />
      </body>
    </html>
  );
}
