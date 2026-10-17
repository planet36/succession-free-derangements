# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: MPL-2.0

PREFIX ?= $(HOME)/.local
BINDIR ?= $(PREFIX)/bin
PYTHONDIR ?= $(PREFIX)/lib/python

MODULE = succession_free_derangements.py
BIN = succession-free-derangements

# There is nothing to build, but a parent Makefile may run these in every directory it builds.
all:

clean:

# This uses install rather than cp because install replaces a symlink at the destination.  cp
# would write through it, so where these files used to be linked in from elsewhere, it would
# overwrite the link's target, or recreate it if the link dangles.
install:
	install -D -m 644 $(MODULE) "$(DESTDIR)$(PYTHONDIR)/$(MODULE)"
	install -D -m 755 $(BIN) "$(DESTDIR)$(BINDIR)/$(BIN)"

uninstall:
	@$(RM) --verbose -- "$(DESTDIR)$(PYTHONDIR)/$(MODULE)" "$(DESTDIR)$(BINDIR)/$(BIN)"

lint:
	-ruff check $(MODULE) $(BIN)
	-mypy --ignore-missing-imports $(MODULE) $(BIN)
	-pylint $(MODULE) $(BIN)

# https://www.gnu.org/software/make/manual/make.html#Phony-Targets
.PHONY: all clean install uninstall lint

# https://www.gnu.org/software/make/manual/html_node/Special-Targets.html#index-removing-targets-on-failure
.DELETE_ON_ERROR:
