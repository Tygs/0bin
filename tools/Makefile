
zerobinpaste: zerobinpaste.js commander.js ../zerobin/static/js/sjcl.js ../zerobin/static/js/lzw.js
	echo '#!/usr/bin/env node' > zerobinpaste
	cat commander.js ../zerobin/static/js/sjcl.js ../zerobin/static/js/lzw.js >> zerobinpaste
	cat  zerobinpaste.js >> zerobinpaste
	chmod +x zerobinpaste

ugly: zerobinpaste
	uglifyjs=$$(PATH="$$(npm bin):$$PATH" which uglifyjs 2>/dev/null) \
		|| { npm install uglify-js; uglifyjs=$$(PATH="$$(npm bin):$$PATH" which uglifyjs); } \
		&& sed -i 1d zerobinpaste \
		&& $${uglifyjs} -o zerobinpaste.min zerobinpaste \
		&& echo '#!/usr/bin/env node' > zerobinpaste \
		&& cat zerobinpaste.min >> zerobinpaste \
		&& chmod +x zerobinpaste

clean:
	rm -f zerobinpaste{,.js,.min}

zerobinpaste.js: zerobinpaste.coffee
	coffee=$$(PATH="$$(npm bin):$$PATH" which coffee 2>/dev/null) \
		|| { npm install coffee-script; coffee=$$(PATH="$$(npm bin):$$PATH" which coffee); } \
		&& $$coffee -c zerobinpaste.coffee

.PHONY: uglify
