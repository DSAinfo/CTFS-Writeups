import travel from './travel.html';

const srv = Bun.serve({
  routes: {
    '/': travel,
    '/meta': () => {
      return Response.json({
        team: 'ACME Inc.',
      });
    },
    '/get-file': {
      POST: async (req) => {
        const url = new URL(req.url);
        const ticket = url.searchParams.get('pnr');

        const f = Bun.file('./tickets/' + ticket);
        try {
          return new Response(await f.text(), {
            headers: {
              'Content-Type': 'application/json',
            },
          });
        } catch (e) {
          return Response.json(
            {
              ok: false,
              error: 'Ticket not found.',
            },
            { status: 404 },
          );
        }
      },
    },
  },
  port: 3000,
});

console.log(`Listening on ${srv.url}`);

function shutdown() {
  console.log('Shutting down gracefully...');
  srv.stop();
  process.exit(0);
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
