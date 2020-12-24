FROM sylhare/type-on-strap:latest

WORKDIR /app/
COPY docs/. /app/

RUN bundle install

CMD ["bundle", "exec", "jekyll", "serve","--host", "0.0.0.0"]
