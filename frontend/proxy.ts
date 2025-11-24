import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

export default createMiddleware(routing);

export const config = {
  matcher: [
    "/",
    "/(en)/:path*",
    "/((?!api|static|.*\\..*|_next|favicon.ico|robots.txt).*)",
  ],
};
