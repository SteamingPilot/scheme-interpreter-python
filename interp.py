import sys
import numbers
import functools
 
# Global Variables to define some constant values
GLOABAL_ENV_ID = 0


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
    return slist

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

def makeclosure(formals, body, parent_env_id):
    return [">closure",formals, body, parent_env_id]

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

def minus(args):
    if (len(args) > 0):
        if (all(map(lambda a: isinstance(a,numbers.Number),args))):
            return functools.reduce(lambda a,b : a-b,args)
        else:
            raise RuntimeError("- applied to non-number: ",sexpr_to_str(args))
    else:
        raise RuntimeError("- must have at least one argument: (-)")


def multiply(args):
    if (len(args) > 0):
        if (all(map(lambda a: isinstance(a,numbers.Number),args))):
            return functools.reduce(lambda a,b : a*b,args)
        else:
            raise RuntimeError("* applied to non-number: ",sexpr_to_str(args))
    else:
        raise RuntimeError("* must have at least one argument: (*)")
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
# Return the a list of all but the first element of a list
# 
# args - a list of arguments to a call to rest
#

def rest(args):
    if (len(args) == 1):
        arg = args[0]
        if (isinstance(arg,list) and len(arg) > 0):
            return arg[1:len(arg)]
        else:
            raise RuntimeError("rest must be applied to a non-null list: ",sexpr_to_str(arg))
    else:
        raise RuntimeError("rest must have exactly one argument: ",sexpr_to_str(args))


#
# Returns a list of elements whose first element is the first element of the argument list, 
# and whose rest element is a list of the rest of the elements of the argument list
#
# args - a list of arguments to a call to cons
#
# This cons function is a replica of the cons function in the DrRacket Language Reference.

def cons(args):
    if (len(args) == 2):
        first = args[0]
        rest = args[1]
        if (isinstance(rest,list)):
            temp = []
            temp.append(first)
            return temp + rest
        else:
            raise RuntimeError("cons must have a list as the second argument: ",sexpr_to_str(rest))
    else:
        raise RuntimeError("cons must have exactly two arguments: ",sexpr_to_str(args))

# Return true if the argument is a null list
def null(args):
    if len(args) == 1:
        arg = args[0]
        if isinstance(arg,list) and len(arg) == 0:
            return True
        else:
            return False
    else:
        raise RuntimeError("null? must have exactly one argument: ",sexpr_to_str(args))

def eq_num(args):
    if len(args) > 0:
        for i in range(len(args)):
            arg = args[i]
            if isinstance(arg, list):
                if len(arg) == 1:
                    args[i] = arg[0]
                else:
                    return False
        if (all(map(lambda a: isinstance(a, numbers.Number),args))):
            res = []
            pre_item = args[0]
            for item in args[1:]:
                if type(pre_item) != type(item):
                    res.append(False)
                else:
                    res.append(pre_item == item)
            return all(res)
        else:
            raise RuntimeError("= applied to non-number: ", sexpr_to_str(args))
    else:
        raise RuntimeError("= must have at least one argument: ",sexpr_to_str(args))
    
def eq(args):
    if len(args) > 0:
        for i in range(len(args)):
            arg = args[i]
            if isinstance(arg, list):
                if len(arg) == 1:
                    args[i] = arg[0]
                else:
                    return False
                
        res = []
        pre_item = args[0]
        for item in args[1:]:
            if type(pre_item) != type(item):
                res.append(False)
            else:
                res.append(pre_item == item)
        return all(res)
    else:
        raise RuntimeError("= must have at least one argument: ",sexpr_to_str(args))
        
    

#
# Add a name, value pair to the base dictionary
#
# n - name
# v - value
#
def addbaseenv(n,v):
    base[n] = v


def addToEnv(key, value, env_id=GLOABAL_ENV_ID):
    globalenv[env_id][key] = value


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


base = {} # base environment dictionary
basenames = [">parent_env", "#t","#f","first","+", "rest", "cons",
             "null?", "=", "-", "*", "eq?"] # names in base environment
basevals = [None, True, False,makebuiltin(first),makebuiltin(plus), makebuiltin(rest), makebuiltin(cons),
            makebuiltin(null), makebuiltin(eq_num), makebuiltin(minus), makebuiltin(multiply), makebuiltin(eq)] # corresponding values


# environment containing Scheme functions
globalenv = [makebase(basenames,basevals)] # the global environment


#
# Lookup an id in an environment
#
# env - a stack of dictionaries
# id - a program id
#
def lookup(env, id):
    if (not env):
        raise RuntimeError("undefined variable reference: ",id)
    else:
        rec = env[0]
        val = rec.get(id)
        if (val == None):
            return lookup(env[1:len(env)],id)
        else:
            return val

def lookup_value(key, env):
    if env is None:
        raise RuntimeError("undefined reference: ", key)
    else:
        val = env.get(key)
        if val is not None:
            return val
        else:
            return lookup_value(key, env[">parent_env"])


#
# Interpret a Scheme expression in an environment
#
# exp - an sexpr
# env - a stack of dictionaries
#
def interp(exp, env_id = GLOABAL_ENV_ID):
    if (isinstance(exp,numbers.Number)):
        return exp
    elif (isinstance(exp,str)):
        return lookup_value(exp, globalenv[env_id])
    elif (isinstance(exp,list)):
        if (exp[0] == "quote"):
            return exp[1]
        elif (exp[0] == "if"):
            if (interp(exp[1], env_id)):
                return interp(exp[2],env_id)
            else:
                return interp(exp[3],env_id)
        elif (exp[0] == "begin"):
            # Interpret each expressions in the list, except the last one.
            for i in range(1,len(exp)-1):
                interp(exp[i], env_id)
            
            # Interpret the last expression and return the result
            return interp(exp[len(exp)-1], env_id)
        elif (exp[0] == "define"):
            # Define a variable
            if not isinstance(exp[1],list):
                var_name = exp[1]
                var_value = interp(exp[2], env_id)
                addToEnv(var_name, var_value, env_id)

            elif (isinstance(exp[1],list) and len(exp[1]) == 1):
                var_name = exp[1][0]
                var_value = interp(exp[2], env_id)
                addToEnv(var_name, var_value, env_id)

            else:
                # Define a function
                # exp example: ['define', ['func', 'arg1', 'arg2'], ['Body']]
                func_name = exp[1][0]
                func_args = exp[1][1:]
                for arg in func_args:
                    if not isinstance(arg, str):
                        raise RuntimeError("function argument must be symbol: ", arg)
                    elif arg in func_args[func_args.index(arg)+1:]:
                        raise RuntimeError("function argument must be unique: ", arg)
                    elif arg == func_name:
                        raise RuntimeError("function argument must be different from function name: ", arg)

                

                func_body = exp[2]
                func = makeclosure([func_name, func_args], func_body, env_id)
                addToEnv(func_name, func, env_id)

        elif (exp[0] == "let"):
            return None # interpret a let expression
        else:
            mfunc = interp(exp[0], env_id)
            if (isbuiltin(mfunc)):  
                args = exp[1:len(exp)]
                margs = list(map(lambda e: interp(e, env_id),args))
                return mfunc[1](margs)
            elif isclosure(mfunc):
                # User Defined Function calls are here
                # mfunc example: [['func', ['arg1', 'arg2']], ['body'], env_id]
                func = mfunc[1][0]
                func_parameters = mfunc[1][1]
                func_body = mfunc[2]

                # Adding a new environment stack for the function call
                new_env = {}
                new_env[">parent_env"] = globalenv[env_id]
                globalenv.append(new_env)
                new_env_id = len(globalenv) - 1
                
                # Mapping the parameter
                for parameter in func_parameters:
                    try:
                        arg = exp[1]
                        new_env[parameter] = interp(arg, new_env_id)
                        exp = exp[1:]
                    except IndexError:
                        raise RuntimeError("Not enough arguments given to function: ", func)
                
                # Interpret the function body
                return interp(func_body, new_env_id)
            else:
                raise RuntimeError("Invalid function call: ",exp[0])

                
    else:
        raise RuntimeError("Invalid scheme syntax: ",sexpr_to_str(exp))

#
# Interpret an expression in the global environment
# This is the interface to the intpreter when passing the code in a string
#
# exp - an sexpr in string form
#
def interpret(exp):
    return sexpr_to_str(interp(parse(exp)))

#
# Interface to the interpreter when read the program from a file
#
# argv - the name of the file
#
def main(argv):
    # f = open(argv[1], "r")
    f = open("test.txt", "r")
    slist = read_sexpr(f)
    print(interpret(slist))
 
if __name__ == '__main__':
    main(sys.argv)
