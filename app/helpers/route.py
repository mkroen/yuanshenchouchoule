import json
from functools import wraps
from typing import List
from flask import Blueprint, abort, g, request


class NoArgError(Exception):
    def __init__(self, name, message=None):
        if message:
            self.name = None
            self.message = message
        else:
            self.name = name
            self.message = "缺少参数'%s'" % name


class ArgTypeError(Exception):
    def __init__(self, name, value, required_type):
        self.name = name
        self.value = value
        self.required_type = required_type
        fmt = "参数'%s'的类型必须是'%s',而非'%s'"
        self.message = fmt % (name, required_type, value)


client_errors = (NoArgError, ArgTypeError)


class InvalidArgStatementError(Exception):
    def __init__(self, state):
        self.state = state
        fmt = "[Error] 参数申明错误:'%s',url:'%s'"
        self.message = fmt % (state, request.url)

    def __str__(self):
        return self.message

def _check_arg(state: str, optional: bool, source: dict):
    parts = state.split(":")
    if len(parts) is 0 or len(parts) > 2:
        raise InvalidArgStatementError(state)
    name = parts[0].strip()
    value = source.get(name)
    if value is None or value == "":
        if optional:
            return name, None
        else:
            raise NoArgError(name)
    # print("name:",name,"value:",value)
    if len(parts) is 2:
        type_ = parts[1].strip()
        try:
            if type_ in ("bool", "boolean"):
                if value not in (True, False):
                    raise ValueError()
                else:
                    return name, value

            elif type_ in ("int", "integer"):
                return name, int(value)

            elif type_ in ("float"):
                return name, float(value)

            elif type_ in ("str", "string"):
                if type(value) is not str:
                    raise ValueError()
                return name, value

            elif type_ == "list":
                if type(value) is str:
                    try:
                        value = json.loads(value)
                    except:
                        raise ValueError()
                if type(value) is not list:
                    raise ValueError()
                return name, value

            elif type_ in ("object", "obj", "dict"):
                if type(value) is str:
                    try:
                        value = json.loads(value)
                    except:
                        raise ValueError()
                if type(value) is not dict:
                    raise ValueError()
                return name, value

            else:
                raise InvalidArgStatementError(state)

            # TODO other types

        except ValueError:
            raise ArgTypeError(name, value, type_)
    else:
        return name, value


def check_request_args(*args_state: str):
    """Check args from request.args according to given args_state
    return checked data as a dict

    supported state types:
        "foo" : required key
        "?foo" : optional key
        "foo:int" : required key with specific type
        "?foo:int" : optional key with specific type
    """
    args_dict = {}
    for s in args_state:
        if type(s) is not str:
            raise TypeError("参数声明必须是字符串，而非 %s", s)
        optional = False
        if s.startswith("?"):
            s = s[1:]
            optional = True
        name, arg = _check_arg(s, optional, request.args)
        # 处理python关键字冲突的参数
        # 遇到此类参数会在结尾加下划线传入handler中
        # 此处理仅针对url参数，不影响post body的参数
        if name in ("type", "for", "from", "id"):
            name = name + "_"
        args_dict[name] = arg
    return args_dict

def _make_method_route(
    blueprint: Blueprint,
    method: str,
    api_path: str,
    check_query_args: List[str] = [],
    *,
    json: bool,
):
    """Make a route decorator that accept specific method
    also checks incoming args
    """
    if type(api_path) is not str:
        raise ValueError("route url must be string. found %s" % api_path)

    def decorator(func):
        def handle(args, kwargs):
            if not json:
                setattr(g, "is_non_json_handler", True)
            if check_query_args:
                try:
                    checked_args = check_request_args(*check_query_args)

                except InvalidArgStatementError as e:
                    print(e.message)
                    return abort(500)

                for k, v in checked_args.items():
                    # print("got arg:",k,v)
                    kwargs[k] = v

        @blueprint.route(api_path, methods=[method])
        @wraps(func)
        def wrapper_without_doc(*args, **kwargs):
            handle(args, kwargs)
            return func(*args, **kwargs)

        wrapper = wrapper_without_doc

        return wrapper

    return decorator


def get(blueprint: Blueprint, api_path: str, check_query_args: List[str] = [], *, json: bool):
    """@decorator
    define handler for GET method only
    """
    return _make_method_route(blueprint, "GET", api_path, check_query_args, json=json)


def post(blueprint: Blueprint, api_path: str, check_query_args: List[str] = [], *, json: bool):
    """@decorator
    define handler for POST method only
    """
    return _make_method_route(blueprint, "POST", api_path, check_query_args, json=json)


def put(blueprint: Blueprint, api_path: str, check_query_args: List[str] = [], *, json: bool):
    """@decorator
    define handler for PUT method only
    """
    return _make_method_route(blueprint, "PUT", api_path, check_query_args, json=json)


def delete(blueprint: Blueprint, api_path: str, check_query_args: List[str] = [], *, json: bool):
    """@decorator
    define handler for PUT method only
    """
    return _make_method_route(blueprint, "DELETE", api_path, check_query_args, json=json)
