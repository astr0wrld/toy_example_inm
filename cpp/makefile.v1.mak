CXX      ?= g++
STD      ?= c++17
CXXFLAGS ?= -std=$(STD) -O2 -Wall -Wextra -pedantic -MMD -MP
CPPFLAGS ?=
LDFLAGS  ?=
LDLIBS   ?=
RM       ?= rm -f

OUT     ?= demo

APPSRC  := demo.cpp
LIBNAME ?= mylib
LIBSRC  ?= mylib.cpp

HDR     := mylib.hpp

APPOBJ  := $(APPSRC:.cpp=.o)
LIBOBJ  := $(LIBSRC:.cpp=.o)
LIB     := lib$(LIBNAME).a

OBJ     := $(APPOBJ) $(LIBOBJ)
DEPS    := $(OBJ:.o=.d)

all: $(LIB) $(OUT)

$(LIB): $(LIBOBJ)
	@echo "AR $@"
	ar rcs $@ $^

$(OUT): $(APPOBJ) $(LIB)
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) $(LDFLAGS) $(APPOBJ) $(LIB) -o $@ $(LDLIBS)

%.o: %.cpp $(HDR)
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c $< -o $@

-include $(DEPS)

run: $(OUT)
	./$(OUT)

clean:
	$(RM) $(OUT) $(OBJ) $(DEPS) $(LIB)

.DEFAULT_GOAL := run
.PHONY: all run clean
