import sys
import numbers
import functools
 
#
# Read an sexpr line by line from the a file
#
# f - a file
#
def read_sexpr(f):
    slist = ''
    for line in f:
        slist += line
    f.close()
    return parse(slist)

#
# Turn a string into a list of tokens that are separated by a space
#
# char - a string of characters
#
def tokenize(chars: str):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


#
# Turn a string representation of an sexpr into a python list representation
#
# program - an sexpr in a string
#
def parse(program: str):
    return read_from_tokens(tokenize(program))

#
# Turn a string of tokens into a python list
#
# tokens - a string of tokens
#
def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

#
# Convert a string token into a number or leave as a string
#
# token - a sequence of characters
#
def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token
#
# Convert a python list as a string representation of a scheme list
#
# l - a python list
#
def sexpr_to_str(l):
    return str(l).replace('[', '(').replace(']', ')').replace(',','').replace('\'','')

# 
# Return a builtin function representation
#
# func - a Python function
#
def makebuiltin(func):
   return [">builtin",func]

#
# Return true if parameter is a builtin function representation
#
# l - anything
#
def isbuiltin(l):
    return isinstance(l,list) and len(l) > 0 and l[0] == ">builtin"

def makeclosure(formals, body, env):
    return [">closure",formals, body, env]

def isclosure(l):
    return isinstance(l,list) and len(l) > 0 and l[0] == ">closure"

#
# Add a list of numbers
#
# args - a list of numbers
#
def plus(args):
    if (len(args) > 0):
        if (all(map(lambda a: isinstance(a,numbers.Number),args))):
            return functools.reduce(lambda a,b : a+b,args)
        else:
            raise RuntimeError("+ applied to non-number: ",sexpr_to_str(args))
    else:
        raise RuntimeError("+ must have at least one argument: (+)")

#
# Return the first element of a list
# 
# args - a list of arguments to a call to first
#
def first(args):
    if (len(args) == 1):
        arg = args[0]
        if (isinstance(arg,list) and len(arg) > 0):
            return arg[0]
        else:
            raise RuntimeError("first must be applied to a non-null list: ",sexpr_to_str(arg))
    else:
        raise RuntimeError("first must have exactly one argument: ",sexpr_to_str(args))
#
# Add a name, value pair to the base dictionary
#
# n - name
# v - value
#
def addbaseenv(n,v):
    base[n] = v

#
# Create the base environment
#
# names - base names
# vals - base values
#
def makebase(names,vals):
    if (names):
        base[names[0]] = vals[0]
        return makebase(names[1:len(names)],vals[1:len(vals)])
    else:
        return base

# you must add #f and first to the bas environment 

base = {} # base environment dictionary
basenames = ["#t","#f","first","+"] # names in base environment
basevals = [True,False,makebuiltin(first),makebuiltin(plus)] # corresponding values

# environment containing Scheme functions
globalenv = [makebase(basenames,basevals)] # the global environment

#
# Lookup an id in an environment
#
# env - a stack of dictionaries
# id - a program id
#
def lookup (env,id):
    if (not env):
        raise RuntimeError("undefined variable reference: ",id)
    else:
        rec = env[0]
        val = rec.get(id)
        if (val == None):
            return lookup(env[1:len(env)],id)
        else:
            return val

#
# Interpret a Scheme expression in an environment
#
# exp - an sexpr
# env - a stack of dictionaries
#
def interp(exp,env):
    if (isinstance(exp,numbers.Number)):
        return exp
    elif (isinstance(exp,str)):
        return lookup(env,exp)
    elif (isinstance(exp,list)):
        if (exp[0] == "quote"):
            return exp[1]
        elif (exp[0] == "if"):
            if (interp(exp[1],env)):
                return interp(exp[2],env)
            else:
                return interp(exp[3],env)
        elif (exp[0] == "begin"):
            return None # interpret a begin expression
        elif (exp[0] == "define"):
            return None # interpret a define expression
        elif (exp[0] == "let"):
            return None # interpret a let expression
        else:
            mfunc = interp(exp[0],env)
            if (isbuiltin(mfunc)):  
                args = exp[1:len(exp)]
                margs = list(map(lambda e: interp(e,env),args))
                return mfunc[1](margs)
            else:
                return None # interpret a user-defined function call
    else:
        raise RuntimeError("Invalid scheme syntax: ",sexpr_to_str(exp))

#
# Interpret an expression in the global environment
# This is the interface to the intpreter when passing the code in a string
#
# exp - an sexpr in string form
#
def interpret(exp):
    return sexpr_to_str(interp(parse(exp),globalenv))

#
# Interface to the interpreter when read the program from a file
#
# argv - the name of the file
#
def main(argv):
    f = open(argv[1], "r")
    slist = read_sexpr(f)
    interpret(slist)
 
if __name__ == '__main__':
    main(sys.argv)
