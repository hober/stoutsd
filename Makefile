deps: js/jquery.metadata.min.js js/jquery.validate.min.js

clean:
	rm -rf tmp
	mkdir tmp

js/jquery.metadata.min.js: tmp/jquery.metadata.2.0/jquery.metadata.min.js
	cp tmp/jquery.metadata.2.0/jquery.metadata.min.js js/jquery.metadata.min.js
tmp/jquery.metadata.2.0/jquery.metadata.min.js: tmp/jquery.metadata.2.0.zip
	cd tmp; unzip jquery.metadata.2.0.zip
tmp/jquery.metadata.2.0.zip:
	cd tmp; curl -O http://plugins.jquery.com/files/jquery.metadata.2.0.zip

js/jquery.validate.min.js: tmp/jquery-validate/jquery.validate.min.js
	cp tmp/jquery-validate/jquery.validate.min.js js/jquery.validate.min.js
tmp/jquery-validate/jquery.validate.min.js: tmp/jquery.validate_3.zip
	cd tmp; unzip jquery.validate_3.zip
tmp/jquery.validate_3.zip:
	cd tmp; curl -O http://plugins.jquery.com/files/jquery.validate_3.zip
