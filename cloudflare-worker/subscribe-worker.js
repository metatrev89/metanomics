/**
 * Metanomics Subscribe Worker
 * Proxies form submissions to the Beehiiv API to avoid CORS restrictions.
 * On successful subscription, sends a notification email via Resend.
 *
 * Environment variables (set in Cloudflare dashboard as secrets):
 *   BEEHIIV_API_KEY  — your Beehiiv API key
 *   BEEHIIV_PUB_ID   — pub_59c2ca48-ee87-4ee2-a4eb-cf9c022751ec
 *   RESEND_API_KEY   — your Resend API key for notification emails
 */

const ALLOWED_ORIGINS = [
  'https://metatrev89.github.io',
  'https://metanomics.org',
  'https://www.metanomics.org',
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const corsOrigin = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': corsOrigin,
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response('Invalid JSON', { status: 400 });
    }

    const payload = {
      email: body.email,
      reactivate_existing: true,
      send_welcome_email: false,
    };
    if (body.first_name) payload.first_name = body.first_name;
    if (body.last_name)  payload.last_name  = body.last_name;

    const beehiivRes = await fetch(
      `https://api.beehiiv.com/v2/publications/${env.BEEHIIV_PUB_ID}/subscriptions`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${env.BEEHIIV_API_KEY}`,
        },
        body: JSON.stringify(payload),
      }
    );

    const beehiivText = await beehiivRes.text();

    // Send notification email via Resend on successful subscription
    if (beehiivRes.status >= 200 && beehiivRes.status < 300 && env.RESEND_API_KEY) {
      const name = [body.first_name, body.last_name].filter(Boolean).join(' ') || 'No name provided';
      fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${env.RESEND_API_KEY}`,
        },
        body: JSON.stringify({
          from: 'Metanomics <onboarding@resend.dev>',
          to: ['trevorspencer89@gmail.com'],
          subject: `New Metanomics subscriber: ${body.email}`,
          text: `New subscriber!\n\nName: ${name}\nEmail: ${body.email}\n\nThey signed up via the Metanomics website.`,
        }),
      }).catch(() => {}); // fire-and-forget; don't block the response
    }

    return new Response(beehiivText, {
      status: beehiivRes.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': corsOrigin,
      },
    });
  },
};
