/** @type {import('next').NextConfig} */
const nextConfig = {
  // For Vercel deployment
  trailingSlash: false,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        port: '',
        pathname: '/**',
      },
    ],
  },
  env: {
    NEXT_PUBLIC_API_URL:'https://asifabdulqadir-todo-backend.hf.space',
  },
};

module.exports = nextConfig;