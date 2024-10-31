import i18nConfig from "@/i18nConfig";
import { regions } from "@/utils/constants";
import { revalidatePath } from "next/cache";
import { NextResponse } from "next/server";

// Add a secret token to prevent unauthorized revalidation
const REVALIDATION_TOKEN = process.env.REVALIDATION_TOKEN;

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const token = searchParams.get("token");

  // Validate the token
  if (token !== REVALIDATION_TOKEN) {
    return NextResponse.json({ message: "Invalid token" }, { status: 401 });
  }

  try {
    // Revalidate the home page and all region pages for both languages
    for (const locale of i18nConfig.locales) {
      // Revalidate base paths
      revalidatePath(`/${locale}`);

      // Revalidate all region paths
      for (const region of regions) {
        revalidatePath(`/${locale}/${region.id}`);
      }
    }

    return NextResponse.json({
      revalidated: true,
      timestamp: Date.now(),
    });
  } catch (err) {
    return NextResponse.json(
      { message: "Error revalidating", error: err },
      { status: 500 },
    );
  }
}
