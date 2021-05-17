FROM node:dubnium-buster as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build:stage

FROM nginx as production-stage
RUN mkdir /app
COPY default.conf.template /etc/nginx/conf.d/default.conf.template
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
CMD /bin/bash -c "envsubst '\$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf" && nginx -g 'daemon off;'