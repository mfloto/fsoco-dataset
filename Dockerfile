FROM sylhare/type-on-strap:jessie

WORKDIR /app/
COPY docs/. /app/

RUN bundle install

CMD ["bundle", "exec", "jekyll", "serve","--host", "0.0.0.0"]
