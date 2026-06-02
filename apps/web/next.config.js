/** @type {import('next').NextConfig} */
const apiProxyUrl = process.env.EXAMOS_API_PROXY_URL || 'http://localhost:8000';

const nextConfig = {
  allowedDevOrigins: ['127.0.0.1'],
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${apiProxyUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
