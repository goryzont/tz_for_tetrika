# Необходимо реализовать декоратор @strict Декоратор проверяет соответствие типов переданных в вызов функции 
# аргументов типам аргументов, объявленным в прототипе функции. (подсказка: аннотации типов аргументов можно 
# получить из атрибута объекта функции func.__annotations__ или с помощью модуля inspect) При несоответствии типов 
# бросать исключение TypeError Гарантируется, что параметры в декорируемых функциях будут следующих типов: bool, int,
# float, str Гарантируется, что в декорируемых функциях не будет значений параметров, заданных по умолчанию


#Решение через func.__code__
def strict(func):
    def wrapper(*args, **kwargs):
        #Получаем аннотации
        annotations = func.__annotations__
        # print(annotations)

        #Получаем имена параметров
        names_params = func.__code__.co_varnames
        # print(names_params)

        for i, arg in enumerate(args):
            name_param = names_params[i]
            type_ = annotations.get(name_param)

            if type_ and not isinstance(arg, type_):
                raise TypeError(f"Argument '{name_param}' must be of type {type_.__name__}, got {type(arg).__name__}")

        return func(*args, **kwargs)
    return wrapper



@strict
def sum_two(a: int, b: int) -> int:
    return a + b



print(sum_two(1, 2)) # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError