"use client";
import Head from 'next/head';
import ApiCall from '../components/ApiCall';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Language Lilypad</title>
        <meta name="description" content="Next.js app with API call" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <h1 style={{ textAlign: 'center' }}>Language Lilypad</h1>
        <ApiCall/>
      </main>
      <footer>
        <p style={{ textAlign: 'center' }}>🪷 where words jump to life! 🌺🐸</p>
      </footer>
    </div>
  );
}
