/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    BACKEND_API_URL: process.env.BACKEND_API_URL,
  },
};

export default nextConfig;
