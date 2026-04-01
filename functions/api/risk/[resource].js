const ALLOWED_RESOURCES = new Set(['exploits', 'interventions']);

function json(data, init = {}) {
  return new Response(JSON.stringify(data), {
    status: init.status || 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=300',
      ...(init.headers || {}),
    },
  });
}

export async function onRequestGet(context) {
  const { params, env, request } = context;
  const resource = typeof params.resource === 'string' ? params.resource : '';

  if (!ALLOWED_RESOURCES.has(resource)) {
    return json({ message: 'Not found' }, { status: 404 });
  }

  const apiBaseUrl = (env.AUK_API_BASE_URL || 'https://api.parametrig.com').replace(/\/$/, '');

  const upstreamUrl = new URL(`${apiBaseUrl}/auk/v1/public/lif/${resource}`);
  const incomingUrl = new URL(request.url);

  for (const [key, value] of incomingUrl.searchParams.entries()) {
    upstreamUrl.searchParams.set(key, value);
  }
  if (!upstreamUrl.searchParams.has('limit')) {
    upstreamUrl.searchParams.set('limit', '1000');
  }
  if (!upstreamUrl.searchParams.has('offset')) {
    upstreamUrl.searchParams.set('offset', '0');
  }

  let upstream;
  try {
    upstream = await fetch(upstreamUrl.toString(), {
      headers: {
        'Accept': 'application/json',
      },
      cf: {
        cacheTtl: 300,
        cacheEverything: false,
      },
    });
  } catch (_) {
    return json({ message: 'Upstream AUK API unavailable', code: 'UPSTREAM_UNREACHABLE' }, { status: 502 });
  }

  const payload = await upstream.json().catch(() => ({}));
  if (!upstream.ok) {
    return json({
      message: payload?.detail?.message || payload?.message || 'AUK API request failed',
      code: payload?.detail?.code || payload?.code || 'UPSTREAM_ERROR',
      status: upstream.status,
    }, { status: upstream.status });
  }

  return json({
    records: Array.isArray(payload.items) ? payload.items : [],
    pageInfo: payload.pageInfo || null,
    source: 'auk_api',
    resource,
  });
}
