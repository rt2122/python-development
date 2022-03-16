import ast
import sys
import inspect
import textwrap
import difflib
import importlib
import itertools

SIMILARITY_THR = 0.95

def get_processed_text(method:callable) -> str:
    '''
    Get source code for the method and replace all names with _.
    '''
    source = inspect.getsource(method)
    source = textwrap.dedent(source)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        for attr in ['name', 'id', 'arg', 'attr']:
            if attr in node._fields:
                setattr(node, attr, '_')
    output = ast.unparse(tree)
    return output

def scan_recursive(prefix:str, obj:object) -> list:
    '''
    Scan module, submodule or class recursively.
    '''
    functions = []
    for name, member in inspect.getmembers(obj):
        if inspect.isfunction(member):
            functions.append(['.'.join([prefix, name]), member])
        elif not name.startswith('_') and name != 'collections':
            functions.extend(scan_recursive('.'.join([prefix, name]), member))
    return functions

def scan_module(module_name:str) -> list:
    '''
    Get all functions of module in dictionary with processed source code: 
    {name[str] : processed_src[str]}
    '''
    module = importlib.import_module(module_name)
    functions = scan_recursive(module_name, module)
    for i in range(len(functions)):
        name, method = functions[i]
        functions[i] = name, get_processed_text(method)
    return functions

def compar(t1:str, t2:str) -> float:
    '''
    Compare processed source code.
    '''
    return difflib.SequenceMatcher(None, t1, t2).ratio()

def get_similar(func_src:str, functions:list) -> list:
    '''
    For source func_src find name of the most similar function in list functions.
    '''
    similar_name, similar_func = max(functions, key=lambda pair:compar(pair[1], func_src))
    similarity = compar(func_src, similar_func)
    if similarity > SIMILARITY_THR:
        return similar_name
    return ''


def compare_one_module(module_name:str) -> list:
    '''
    Get list of names for similar functions within one module.
    '''
    functions = scan_module(module_name)
    similar_names = []
    for i in range(len(functions) - 1):
        name, func_src = functions[i]
        similar_name = get_similar(func_src, functions[i+1:])
        if len(similar_name) > 0:
            similar_names.append([name, similar_name])
    return similar_names

def compare_two_modules(module_name1:str, module_name2:str) -> list:
    '''
    Get list of names for similar functions in two modules.
    '''
    functions1 = scan_module(module_name1)
    functions2 = scan_module(module_name2)
    similar_names = []
    for name, func_src in functions1:
        similar_name = get_similar(func_src, functions2)
        if len(similar_name) > 0:
            similar_names.append([name, similar_name])
    return similar_names

if __name__ == '__main__':
    if len(sys.argv) > 2:
        output = compare_two_modules(sys.argv[1], sys.argv[2])
        joint = ' '
    else:
        output = compare_one_module(sys.argv[1])
        joint = ' : '
    output = sorted(output, key=lambda x:x[0])
    output = map(lambda x: joint.join(x), output)
    print('\n'.join(output))
