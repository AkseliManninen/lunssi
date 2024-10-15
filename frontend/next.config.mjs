/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    BACKEND_API_URL: process.env.BACKEND_API_URL,
  },
  webpack: (config, { isServer }) => {
    // svgr-support
    config.module.rules.push({
      test: /\.svg$/i,
      use: ["@svgr/webpack"],
    });
    if (!isServer) {
      // set 'fs' to an empty module on the client to prevent this error on build --> Error: Can't resolve 'fs'
      config.resolve.fallback.fs = false;
    }
    return config;
  },
};

export default nextConfig;
