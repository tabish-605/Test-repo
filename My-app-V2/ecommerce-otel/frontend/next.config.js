/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  images: {
    domains: ['via.placeholder.com'],
  },
  experimental: {
    instrumentationHook: true,
  },
  output: 'standalone', // ADD THIS LINE
}
