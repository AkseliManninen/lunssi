import type { ReactNode } from "react";
import "@/styles/globals.css";
import Footer from "@/components/Footer";
import { getStaticParams } from "@/locales/server";
import { GoogleTagManager } from "@next/third-parties/google";
import type { Metadata } from "next";
import { Roboto } from "next/font/google";

export const metadata: Metadata = {
  title: "Lunssi",
  openGraph: {
    title: "Lunssi",
    url: "https://lunssi.fi",
    type: "website",
    siteName: "Lunssi",
  },
};

export function generateStaticParams() {
  return getStaticParams();
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
