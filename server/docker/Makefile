alerts_src_dir ?= $(CURDIR)/alerts

image_tag := povilasb/iptund

.PHONY: image
image:
	docker build -t $(image_tag) .

.PHONY: container
container:
	docker run --name iptund -v `pwd`/..:/opt/iptund -d --cap-add=NET_ADMIN $(image_tag)
