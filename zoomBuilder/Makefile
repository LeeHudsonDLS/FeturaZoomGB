#Makefile at top of application tree
TOP = .
include $(TOP)/configure/CONFIG
DIRS := $(DIRS) $(filter-out $(DIRS), configure)
DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard etc))
DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard iocs))
ifeq ($(wildcard etc),etc)  # If etc exists...
  include $(TOP)/etc/makeIocs/Makefile.iocs
  UNINSTALL_DIRS += documentation/doxygen $(IOC_DIRS)
endif

define DIR_template
 $(1)_DEPEND_DIRS = configure
endef
$(foreach dir, $(filter-out configure,$(DIRS)),$(eval $(call DIR_template,$(dir))))

include $(TOP)/configure/RULES_TOP

