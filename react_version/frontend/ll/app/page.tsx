"use client";
import Head from 'next/head';
import ApiCall from '../components/ApiCall';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Next.js API Call App</title>
        <meta name="description" content="Next.js app with API call" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <h1 style={{ textAlign: 'center' }}>Next.js API Call App</h1>
        <ApiCall />
      </main>
      <footer>
        <p style={{ textAlign: 'center' }}>Footer content here</p>
      </footer>
    </div>
  );
}
