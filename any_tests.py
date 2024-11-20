
def decor(func):#sdfsdf
    def wrapper(*args):
        return f'Result of function is {func(args)}'
    return wrapper

@decor
def sale_stats(*args: list, revenue=None, quantity=None):
    if revenue:
        revenue = 0
        for _list in args:
            for arg in _list:
                revenue += arg[1]*arg[2]

    if quantity:
        name_dict=dict({})
        for _list in args:
            for arg in _list:
                if arg[0] in name_dict.keys():
                    quantity=name_dict.get(arg[0])+arg[1]
                    name_dict[arg[0]]=quantity
                else:
                    name_dict[arg[0]]=arg[1]
        quantity=name_dict
    return (revenue, quantity)


# sales_data = [["яблоки", 10, 20], ["груши", 5, 30], ["яблоки", 7, 20]]
sales_data=[('Apple', 10, 0.5), ('Orange', 5, 0.6)]
# print(len(sales_data[0][0]-))
print(sale_stats(sales_data, revenue=True))
