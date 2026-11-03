FROM oven/bun:1.3.14 AS build

WORKDIR /app
COPY package.json package.json
COPY bun.lock bun.lock
RUN bun install --production --frozen-lockfile

COPY ./src ./src
ENV NODE_ENV=production
RUN bun build --compile --minify --outfile /app/server src/index.ts

FROM gcr.io/distroless/base

WORKDIR /app
COPY --chmod=0555 --from=build /app/server /app/server
COPY ./tickets /app/tickets

ENV NODE_ENV=production
CMD ["/app/server"]
EXPOSE 3000
